```
logistics/
├─ CLAUDE.md
├─ README.md
├─ docker-compose.yml
├─ Dockerfile
├─ pyproject.toml
├─ .env.example
├─ crontab
├─ migrations/
├─ docs/
│  ├─ 01-mvp-scope.md
│  ├─ 02-architecture.md
│  ├─ 03-data-model.md
│  ├─ 04-bot-flow.md
│  ├─ 05-messages.md
│  ├─ 06-matching.md
│  ├─ 07-payments.md
│  ├─ 08-errors.md
│  └─ 09-code-structure.md
└─ app/
   ├─ config.py                # env settings
   ├─ enums.py                 # all statuses in one place
   ├─ db/
   │  ├─ session.py
   │  └─ models/               # users, settings, sources, user_sources, posts,
   │                           # deliveries, payments, methods, features,
   │                           # subscriptions, routes
   ├─ repositories/            # all SQL lives here
   │  ├─ posts.py
   │  ├─ users.py
   │  ├─ deliveries.py
   │  ├─ payments.py
   │  └─ subscriptions.py
   ├─ services/                # business logic, framework-free
   │  ├─ parsing.py            # price + route out of raw_text
   │  ├─ normalize.py          # city dictionary → from_norm / to_norm
   │  ├─ routes.py             # distance_km lookup, price_per_km
   │  ├─ dedupe.py             # fingerprint, 24h window
   │  ├─ matching.py           # ready post → matched users
   │  ├─ subscriptions.py      # activate / extend / expire
   │  └─ monobank.py           # API client, X-Sign verify
   ├─ parser/                  # telethon (MTProto)
   │  ├─ __main__.py
   │  └─ client.py
   ├─ worker/
   │  ├─ __main__.py           # runs both loops
   │  ├─ pipeline.py           # Posts(new) → ready/skipped/duplicate → deliveries
   │  └─ sender.py             # deliveries(pending) → Bot API
   ├─ bot/                     # aiogram
   │  ├─ __main__.py
   │  ├─ handlers/             # start, on_off, config, price, source, payment, card
   │  ├─ keyboards.py
   │  └─ texts.py              # {Greeting}, {Card}, {PaymentSuccess}, ...
   ├─ api/                     # fastapi
   │  ├─ __main__.py
   │  └─ webhooks/monobank.py
   └─ jobs/                    # one-shot cron scripts
      ├─ expire_invoices.py
      ├─ poll_invoices.py
      ├─ renew_subscriptions.py
      ├─ notify_expiry.py
      └─ expire_subscriptions.py
```