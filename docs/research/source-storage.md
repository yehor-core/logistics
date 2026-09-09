# Research: storing source channels

## Problem
`SOURCE_CHANNELS` in `.env` doesn't scale — production may have 100+ channels,
and `.env` is meant for scalars/secrets, not unbounded lists.

## Existing schema

The `Sources` table is already modeled in `docs/03-data-model.md`:

| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / Integer | PK |
| type | `Mapped[SourceType]` / Enum | `telegram` |
| is_enabled | `Mapped[bool]` / Boolean | `server_default=true` |
| last_fetched_at | `Mapped[datetime \| None]` / timestamptz | nullable; parser resumes from here |
| chat_id | `Mapped[int \| None]` / BigInteger | nullable |

## Migration plan (after DB setup)

1. Alembic migration for `sources` (already modeled, per `docs/03-data-model.md`).
2. One-time resolution step: current `SOURCE_CHANNELS` values are Telegram
   handles (e.g. channel_one), not numeric chat_id — resolve each handle to
   its chat_id via Telethon before seeding the table.
3. Replace `settings.source_channels` in the parser client with a query:
   select(Source.chat_id).where(Source.is_enabled.is_(True), Source.type == SourceType.TELEGRAM)
4. Add a minimal CRUD path (script or endpoint) for adding/disabling sources.

## Open question
`chat_id` is nullable — need to confirm whether that's for sources awaiting
resolution (handle not yet mapped to chat_id) or for future non-telegram
source types.
