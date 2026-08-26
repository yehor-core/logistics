# Filtering & Matching

## Pipeline
`Posts.status = new` → parse → normalize → route lookup → dedupe → match users → `Post deliveries`

## 1. Parse
Extract `from_location`, `to_location`, `price` from `raw_text`.
- Price = number next to currency markers (`грн`, `₴`, `uah`); ignore phones, weights (`т`, `кг`), volumes (`м3`).
- No price or no route in text → `status = skipped`.

## 2. Normalize
- Lowercase, strip punctuation/emoji, drop prefixes (`м.`, `с.`, `смт`).
- Map through city dictionary → `from_norm`, `to_norm`.
- Unknown city → `status = skipped` (log it to extend the dictionary).

## 3. Route & price per km
- Lookup `Routes(from_norm, to_norm)` → `distance_km`.
- `price_per_km = price / distance_km` (2 decimals) → save to `Posts`.
- Route missing, `from_norm == to_norm`, or `distance_km = 0` → `status = skipped`.

## 4. Dedupe
- `fingerprint = sha256(from_norm + to_norm + price)`.
- Search posts with the same `fingerprint` and `published_at` within the last 24h.
- Found → `status = duplicate`, `duplicate_of_id = <canon post id>`, stop. No deliveries created.
- Not found → `status = ready`.

Two layers: `(source_id, external_id)` unique constraint blocks repeats inside one source; `fingerprint` blocks the same order reposted across different sources.

## 5. Match users
For a `ready` post, select users where **all** conditions hold — one ORM `select()` joining the four tables below, in `repositories/posts.py`:

| Condition | Check |
|---|---|
| Source subscribed | `User sources(user_id, post.source_id).is_enabled = true` |
| Bot enabled | `User settings.is_enabled = true` |
| Paid access | `User subscriptions.status = active` AND `expires_at > now()` |
| Price fits | `post.price_per_km >= User settings.price_per_km` |

## 6. Deliver
- Insert `Post deliveries(post_id, user_id, status = pending)` for each matched user.
- Composite PK `(post_id, user_id)` makes the insert idempotent via `postgresql.insert(...).on_conflict_do_nothing()` — one post reaches a user once.
- Then `Posts.status = distributed`. Zero matched users → still `distributed`.

## Status map for `Post`
| Status | Meaning |
|---|---|
| `new` | saved by parser, not processed |
| `ready` | parsed, normalized, `price_per_km` computed |
| `distributed` | matching done, deliveries created |
| `skipped` | business rule: no price / unknown city / no route |
| `failed` | technical error — retry later |
| `duplicate` | same `fingerprint` within 24h |