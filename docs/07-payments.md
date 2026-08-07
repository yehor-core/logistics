# Payments

## Model
- Provider: Monobank Acquiring. Currency UAH (`ccy = 980`), amounts in kopecks.
- Access after successful payment = row in `User subscriptions` with `status = active` and `expires_at > now()`.
- Plan (price, duration) comes from `Features`.

## 1. First payment
1. User taps `/card` → `POST /api/merchant/invoice/create`:
   - `amount = Features.price`, `ccy = 980`, `validity = 900` (15 min)
   - `merchantPaymInfo.reference = Payments.id`
   - `saveCardData: { saveCard: true, walletId: <user_id> }` — required for auto-renewal
   - `webHookUrl`, `redirectUrl`
2. Insert `Payments(status = pending, external_id = invoiceId, method_id = monobank)`.
3. Bot sends `pageUrl` inside `{Card}`.
4. Webhook `success` → activate subscription → `{PaymentSuccess}`.

## 2. Webhook
`POST /webhook/monobank` (FastAPI):
1. Verify `X-Sign` — ECDSA-SHA256 over the **raw** body, key from `GET /api/merchant/pubkey` (cached). Invalid → `403`.
2. Find `Payments` by `external_id = invoiceId`. Unknown → `200` + log.
3. Skip if payment is already in a final status (idempotency; webhooks repeat and can arrive out of order — compare `modifiedDate`).
4. Store raw body in `payload`, update `status`, set `confirmed_at`.
5. On `success` → activate/extend subscription.
6. Always return `200` — any other code makes mono retry.

### Status map
| Mono invoice status | `Payments.status` |
|---|---|
| `created`, `processing`, `hold` | `pending` |
| `success` | `confirmed` |
| `failure`, `reversed` | `rejected` |
| `expired` | `expired` |

## 3. Subscription activation
On `confirmed`:
- No active subscription → insert `User subscriptions(status = active, starts_at = now(), expires_at = now() + Features.duration, payment_id)`.
- Active subscription exists → `expires_at += Features.duration` (extend, never overwrite).
- Reset `expiry_notified_at = null`.

## 4. Auto-renewal
Cron, daily:
1. Select `status = active` AND `expires_at <= now() + 1 day`.
2. `POST /api/merchant/wallet/payment` — `cardToken`, `amount`, `ccy = 980`, `initiationKind = merchant`, new `reference`.
3. New `Payments` row → same webhook/status flow → extend `expires_at`.
4. Charge failed → retry once after 24h, then `status = expired` + message with `/card` link.

## 5. Cron jobs
| Job | Frequency | Action |
|---|---|---|
| Expire invoices | 5 min | `pending` older than 15 min → `expired` |
| Fallback polling | 5 min | `GET /api/merchant/invoice/status?invoiceId=` for `pending` without a webhook |
| Renewal | daily | token charge (see 4) |
| Expiry reminder | daily | `expires_at` within 3 days AND `expiry_notified_at is null` → notify, set field |
| Expire subscriptions | hourly | `expires_at < now()` → `status = expired`, deliveries stop |

## 6. Edge cases
- Duplicate webhook → idempotent by `external_id` + final-status check.
- Payment lands after invoice expiry → still `confirmed`, subscription activated.
- User pays twice → second payment extends `expires_at`.
- Webhook lost → fallback polling closes the gap.
- `reversed` / refund → `rejected`, subscription set to `cancelled` manually (no self-service refunds in MVP).