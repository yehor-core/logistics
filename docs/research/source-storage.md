# Research: storing source channels

## Problem
`SOURCE_CHANNELS` in `.env` doesn't scale — production may have 100+ channels,
and `.env` is meant for scalars/secrets, not unbounded lists.

## Existing schema

The `Sources` table is already modeled in `docs/03-data-model.md`:

| Field | Notes |
|---|---|
| id | PK |
| type | enum: telegram |
| is_enabled | |
| last_fetched_at | |
| chat_id | nullable |

## Migration plan (after DB setup)

1. Alembic migration for `sources`.
2. One-time resolution step: current `SOURCE_CHANNELS` values are Telegram
   handles (e.g. channel_one), not numeric chat_id — resolve each handle to
   its chat_id via Telethon before seeding the table.
3. Replace `settings.source_channels` in the parser client with a query:
   select(Source.chat_id).where(Source.is_enabled.is_(True))
4. Add a minimal CRUD path (script or endpoint) for adding/disabling sources.
