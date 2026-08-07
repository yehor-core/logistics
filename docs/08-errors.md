# Errors & Edge Cases

## 1. Parser (MTProto)
- FloodWait → sleep for the returned interval, retry; nothing lost (`Sources.last_fetched_at`).
- Session revoked / auth error → stop parser, alert, resume after re-auth.
- Channel private, deleted, or account kicked → `Sources.is_enabled = false` + log.
- Repeat message inside one source → blocked by unique `(source_id, external_id)`.
- Message edited or deleted after parsing → ignored in MVP; deliveries are not recalled.
- Parser downtime → on restart read from `last_fetched_at`; posts older than 24h skipped as stale.

## 2. Parsing & normalization
- No price or no route in text → `skipped`.
- Unknown city → `skipped` + log (feeds the dictionary).
- Multiple numbers in text → take the one next to a currency marker; ambiguous → `skipped`.
- Non-UAH price ($, €) → `skipped` (MVP is UAH only).
- Missing route, `from_norm == to_norm`, `distance_km = 0` → `skipped`.
- DB/network error mid-processing → `failed`, retried by cron (3 attempts, then left `failed`).

## 3. Dedupe
- Same order reposted in another source → `duplicate` + `duplicate_of_id`, no deliveries.
- Repost older than 24h → treated as new (orders legitimately get re-listed).
- Different orders with identical route + price → collide and get deduped; accepted MVP trade-off.
- Concurrent processing → single worker in MVP + row lock on `Posts.status = new`.

## 4. Delivery
- User blocked the bot (403) → delivery `blocked`, no retries for that user.
- Telegram 429 → respect `retry_after`, delivery stays `pending`.
- Network / 5xx → `failed`, up to 3 retries, then dropped.
- Subscription expired or bot switched off between matching and sending → re-check before send, skip.
- Duplicate delivery attempt → composite PK `(post_id, user_id)` makes it idempotent.
- Burst of posts → global send rate limit (~25 msg/s) to stay under Telegram limits.

## 5. Payments
- Duplicate webhook → idempotent by `external_id` + final-status check.
- Out-of-order webhook → compare `modifiedDate`, ignore older.
- Invalid `X-Sign` → `403`, nothing written.
- Unknown `invoiceId` → `200` + log.
- Payment lands after invoice expiry → still `confirmed`, subscription activated.
- User pays twice → second payment extends `expires_at`.
- Webhook lost → fallback polling closes the gap.
- `reversed` / refund → `rejected`, subscription set to `cancelled` manually (no self-service refunds in MVP).
- Internal error while handling webhook → store `payload` first, still return `200`; polling reconciles.

## 6. Subscription & auto-renewal
- Card token missing/expired or insufficient funds → retry once after 24h → `expired` + `/card` message.
- Renewal charged while still active → `expires_at += duration`, never overwritten.
- Manual payment right before renewal → re-check `expires_at` at charge time, skip the charge.
- Cron restart / double run → skip subscriptions that already have a `pending` payment.
- Expiry between hourly cron ticks → up to 1h of extra access, acceptable.

## 7. Bot & settings
- Non-numeric, negative, or empty price → `{PriceInvalid}`, value not saved.
- `price_per_km = 0` → valid, user receives every `ready` post.
- Price never set → default from config (65uah/km).
- No active subscription → commands work, deliveries are not created.
- Payment link opened after 15 min → invoice `expired`, user taps `/card` for a new one.
- Double tap on `/card` → reuse the existing `pending` invoice if not expired.

## 8. Infrastructure
- DB unavailable → retry with backoff; all status transitions are transactional.
- Container restart mid-processing → in-flight rows stay `new` / `pending`, picked up on next tick.
- Overlapping cron runs → Postgres advisory lock per job.
- All timestamps stored in UTC.