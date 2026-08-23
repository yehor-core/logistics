# CLAUDE.md

## Project

Subscription service that helps/solves problems of Ukrainian logistics dispatchers

## Rules

### Global
- Always read docs for the related area you are editing/gathering context on.
- We are building MVP version of the project. You should not add features that are not listed in the `docs/01-mvp-scope.md`!
- Nearly for each task in the MVP you should read `docs/02-architecture.md`.
- Follow target file tree, described in the `docs/09-code-structure.md`
- Docs are always written in English
- Secrets via env only (`.env` is gitignored); keep `.env.example` in sync when adding a setting.
- Always run related tests + ruff before commit 

### Git
- Never run `git commit` or `git push` automatically. Only run `git commit` or `git push` if the user explicitly commands to run these commands.
- Branch name: `{username}`/`{changes}` - `{changes}` should always be shorter then 5 words

## Docs

| Doc | Answers |
|---|---|
| `docs/01-mvp-scope.md` | What is in/out of MVP |
| `docs/02-architecture.md` | Architecture of the project |
| `docs/03-data-model.md` | Every table, column, enum, relation |
| `docs/04-bot-flow.md` | Command tree, Reply vs Inline buttons |
| `docs/05-messages.md` | Exact user-facing copy (Russian) + placeholders |
| `docs/06-matching.md` | Parse → normalize → route → dedupe → match → deliver |
| `docs/07-payments.md` | Monobank invoices, webhook, activation, auto-renewal, cron |
| `docs/08-errors.md` | Edge cases per component — check here before inventing handling |
| `docs/09-code-structure.md` | Target file tree |

## Stack

- Python
- aiogram
- MTProto parser
- PostgreSQL
- FastAPI
- plain system cron
- Docker Compose

### Dependencies
- uv

### Tests
- pytest
- pytest-asyncio
- ruff

## Commands
- gh
- ruff check --diff
- ruff format --diff