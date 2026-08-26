# Data Model

## Conventions

Where the models and migrations live: [Code structure](./09-code-structure.md).

- Columns use SQLAlchemy 2.0 typed style — the `Type` column below reads
  `Mapped[<python type>]` / `<SQL type>`, i.e. what goes into `mapped_column(...)`.
- Table names are the snake_case plural of the section heading: `## User settings` → `user_settings`.
- Enum columns map a `StrEnum` from `src/enums.py` to a native Postgres enum
  (`sa.Enum(..., native_enum=True)`); the `Type` column names the Python class.
- Money and decimals use `Numeric`, never float.
- Timestamps are `DateTime(timezone=True)` (`timestamptz`).
- Telegram `User.id` and `Chat.id` may exceed 32 significant bits (at most 52), so columns holding
  them are `BigInteger`. `message_id` carries no such guarantee — `BigInteger` there is headroom only.
- Relations use `relationship(back_populates=...)`; foreign keys use
  `ForeignKey("<table>.<column>", ondelete=...)`.

---

## Users
| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / BigInteger | PK |
| tg_id | `Mapped[int]` / BigInteger | unique, index |
| created_at | `Mapped[datetime]` / timestamptz | `server_default=now()` |
| card_token | `Mapped[str \| None]` / Text | nullable; Monobank card token for auto-renewal |
| wallet_id | `Mapped[str \| None]` / Text | nullable; Monobank wallet id |

**Relations:**
- `Users.id` → `Payments.user_id`
- `Users.id` → `User settings.user_id`
- `Users.id` → `User sources.user_id`
- `Users.id` → `Post deliveries.user_id`
- `Users.id` → `User subscriptions.user_id`

---

## User settings
| Field | Type | Notes |
|---|---|---|
| user_id | `Mapped[int]` / BigInteger | PK, FK → `users.id`; the PK gives the one-row-per-user constraint |
| is_enabled | `Mapped[bool]` / Boolean | `server_default=true` |
| price_per_km | `Mapped[Decimal]` / Numeric(10, 2) | default from config (`DEFAULT_PRICE_PER_KM`) |
| updated_at | `Mapped[datetime]` / timestamptz | `server_default=now()`, `onupdate=now()` |

---

## Payments
| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / BigInteger | PK |
| user_id | `Mapped[int]` / BigInteger | FK → `users.id`, index |
| method_id | `Mapped[int]` / Integer | FK → `methods.id` |
| amount | `Mapped[int]` / BigInteger | kopecks |
| status | `Mapped[PaymentStatus]` / Enum | `pending`, `confirmed`, `rejected`, `expired` |
| external_id | `Mapped[str]` / Text | unique; Monobank `invoiceId` — a string, not a number |
| payload | `Mapped[dict \| None]` / JSONB | nullable; raw webhook body, written before processing |
| created_at | `Mapped[datetime]` / timestamptz | `server_default=now()` |
| confirmed_at | `Mapped[datetime \| None]` / timestamptz | nullable |

> **TODO:** `07-payments.md` compares `modifiedDate` to drop out-of-order webhooks, but no
> `modified_date` column exists here. Undecided.

**Relations:**
- `Payments.method_id` → `Methods.id`
- `Payments.id` → `User subscriptions.payment_id` (nullable)

---

## Methods
| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / Integer | PK |
| name | `Mapped[str]` / Text | unique; seeded with `monobank` via an Alembic data migration |

---

## User subscriptions
| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / BigInteger | PK |
| user_id | `Mapped[int]` / BigInteger | FK → `users.id`, index |
| feature_id | `Mapped[int]` / Integer | FK → `features.id`, index |
| payment_id | `Mapped[int \| None]` / BigInteger | FK → `payments.id`, nullable |
| status | `Mapped[SubscriptionStatus]` / Enum | index; `active`, `expired`, `cancelled` |
| starts_at | `Mapped[datetime]` / timestamptz | |
| expires_at | `Mapped[datetime]` / timestamptz | index; extended on renewal, never overwritten |
| expiry_notified_at | `Mapped[datetime \| None]` / timestamptz | nullable; reset to `null` on renewal |

---

## Features
| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / Integer | PK |
| name | `Mapped[str]` / Text | |
| is_enabled | `Mapped[bool]` / Boolean | `server_default=true` |
| price | `Mapped[int]` / BigInteger | kopecks, same unit as `payments.amount` |
| duration | `Mapped[timedelta]` / Interval | added to `expires_at` on activation and renewal |

The MVP plan row is seeded via an Alembic data migration.

**Relations:**
- `Features.id` → `User subscriptions.feature_id`

---

## User sources
| Field | Type | Notes |
|---|---|---|
| user_id | `Mapped[int]` / BigInteger | composite PK, FK → `users.id` |
| source_id | `Mapped[int]` / Integer | composite PK, FK → `sources.id` |
| is_enabled | `Mapped[bool]` / Boolean | `server_default=true` |

---

## Sources
| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / Integer | PK |
| type | `Mapped[SourceType]` / Enum | `telegram` |
| is_enabled | `Mapped[bool]` / Boolean | `server_default=true` |
| last_fetched_at | `Mapped[datetime \| None]` / timestamptz | nullable; parser resumes from here |
| chat_id | `Mapped[int \| None]` / BigInteger | nullable |

**Relations:**
- `Sources.id` → `User sources.source_id`
- `Sources.id` → `Posts.source_id`

---

## Posts
| Field | Type | Notes |
|---|---|---|
| id | `Mapped[int]` / BigInteger | PK |
| source_id | `Mapped[int]` / Integer | FK → `sources.id`; unique together with `external_id` |
| external_id | `Mapped[int]` / BigInteger | unique together with `source_id`; Telegram message id |
| fingerprint | `Mapped[str \| None]` / String(64) | nullable; sha256 hex of `from_norm`, `to_norm`, `price`. Index covers `(fingerprint, published_at)` — the dedupe scan is windowed to 24h |
| raw_text | `Mapped[str]` / Text | |
| from_location | `Mapped[str \| None]` / Text | nullable until parsed |
| to_location | `Mapped[str \| None]` / Text | nullable until parsed |
| price | `Mapped[Decimal \| None]` / Numeric(12, 2) | nullable until parsed; UAH |
| price_per_km | `Mapped[Decimal \| None]` / Numeric(10, 2) | nullable until computed; 2 decimals |
| published_at | `Mapped[datetime]` / timestamptz | source-side timestamp |
| parsed_at | `Mapped[datetime \| None]` / timestamptz | nullable until processed |
| status | `Mapped[PostStatus]` / Enum | index; `new`, `ready`, `distributed`, `skipped`, `failed`, `duplicate` |
| from_norm | `Mapped[str \| None]` / Text | nullable until normalized |
| to_norm | `Mapped[str \| None]` / Text | nullable until normalized |
| duplicate_of_id | `Mapped[int \| None]` / BigInteger | nullable; self-referential FK → `posts.id` |

> **TODO:** `08-errors.md` retries processing 3 times before leaving a post `failed`, but no retry
> counter column exists here. Undecided.

**Relations:**
- `Posts.id` → `Post deliveries.post_id`

---

## Post deliveries
| Field | Type | Notes |
|---|---|---|
| post_id | `Mapped[int]` / BigInteger | composite PK, FK → `posts.id` |
| user_id | `Mapped[int]` / BigInteger | composite PK, FK → `users.id` |
| tg_message_id | `Mapped[int \| None]` / BigInteger | nullable until sent |
| created_at | `Mapped[datetime]` / timestamptz | `server_default=now()` |
| sent_at | `Mapped[datetime \| None]` / timestamptz | nullable |
| status | `Mapped[DeliveryStatus]` / Enum | index; `pending`, `sent`, `failed`, `blocked` |

> **TODO:** `08-errors.md` allows up to 3 send retries before dropping a delivery, but no retry
> counter column exists here. Undecided.

---

## Routes
| Field | Type | Notes |
|---|---|---|
| from_norm | `Mapped[str]` / Text | composite PK |
| to_norm | `Mapped[str]` / Text | composite PK |
| distance_km | `Mapped[Decimal]` / Numeric(10, 2) | |
| from_location | `Mapped[str]` / Text | display name |
| to_location | `Mapped[str]` / Text | display name |

> **TODO:** the relation to `Posts.from_norm` / `Posts.to_norm` is undecided — real composite FK, or
> a pure lookup table with no constraint.
