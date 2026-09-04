# Components
1. **Parser**\
MTProto - reads new messages from Telegram channels/chats, written in `Sources`. New message → `Posts`, dedupe by `(source_id, external_id)`.

2. **Normalizer + Matcher**\
Picks up `post.status = new` :
    1. parses `from_location`, `to_location` and `price` from `raw_text`
    2. normalizes cities into `from_norm/to_norm` via a lookup dictionary
    3. looks up `distance_km` in `Routes`, computes `price_per_km`
    4. calculates `fingerprint`, searches for a post with the same `fingerprint` for the last 24h; if found - `status = duplicate`, `duplicate_of_id = <canon id>`, processing stops, `Post deliveries` are not created.
    5. sets `status = ready/skipped/failed/duplicate`.\
     For `ready` posts, it finds matching users (`User settings.is_enabled = true`, active subscription, source enabled for that user, `price_per_km >= User settings.price_per_km`) and creates `Post deliveries`rows.

3. **Bot** 
Handles `/start`, `/on_off`, `/config`, `/price`, `/source`, `/payment`, `/card` - see the [Flow](./04-bot-flow.md)\
A separate delivery worker pulls `pending` rows from `Post deliveries` and sends messages to users, updating `status/sent_at/tg_message_id`.

4. Payment Service
HTTP endpoint for the Monobank webhook (verifies `X-Sign`, updates `Payments`, activates/renews `User subscriptions`) - see the [Payments](./07-payments.md)

5. Cron
    1. expires `pending` payments older than 15 minutes → `expired`
    2. fallback polling of `GET /invoice/status` for payments that never got a webhook
    3. subscription-expiry reminders (`expiry_notified_at`)
    4. flips expired subscriptions to `status = expired`

# Data flow
`Sources (MTProto)` → `Posts (raw)` → normalization/matching → `Post deliveries (pending)` → Bot API → user, while `Payments`/`User subscriptions` gate access to the broadcast in parallel.

# Stack
- Python: aiogram (bot) + Telethon/Pyrogram (MTProto parser)
- PostgreSQL — primary datastore; SQLAlchemy ORM over asyncpg, Alembic for migrations
- Plain system cron — scheduled jobs
- FastAPI — Monobank webhook receiver
- Docker Compose — 4 containers (bot, parser, worker, webhook-api) on a single VPS for MVP; no message broker needed, task "queueing" is just DB status columns