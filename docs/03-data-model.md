# Data Model

## Users
| Field | Type / Notes |
|---|---|
| id | PK |
| tg_id | Unique |
| created_at | |

**Relations:**
- `Users.id` → `Payments.user_id`
- `Users.id` → `User settings.user_id`
- `Users.id` → `User sources.user_id`
- `Users.id` → `Post deliveries.user_id`
- `Users.id` → `User subscriptions.user_id`

---

## User settings
| Field | Type / Notes |
|---|---|
| user_id | FK, unique → Users.id |
| is_enabled | |
| price_per_km | |
| updated_at | |

---

## Payments
| Field | Type / Notes |
|---|---|
| id | PK |
| user_id | FK → Users.id |
| method_id | FK → Methods.id |
| amount | |
| status | enum: `pending`, `confirmed`, `rejected`, `expired` |
| external_id | unique |
| payload | |
| created_at | |
| confirmed_at | |

**Relations:**
- `Payments.method_id` → `Methods.id`
- `Payments.id` → `User subscriptions.payment_id` (nullable)

---

## Methods
| Field | Type / Notes |
|---|---|
| id | PK |
| name | |

---

## User subscriptions
| Field | Type / Notes |
|---|---|
| id | PK |
| user_id | FK, idx → Users.id |
| feature_id | FK, idx → Features.id |
| payment_id | FK, nullable → Payments.id |
| status | idx; enum: `active`, `expired`, `cancelled` |
| starts_at | |
| expires_at | idx |
| expiry_notified_at | |

---

## Features
| Field | Type / Notes |
|---|---|
| id | PK |
| name | |
| is_enabled | |
| price | |
| duration | |

**Relations:**
- `Features.id` → `User subscriptions.feature_id`

---

## User sources
| Field | Type / Notes |
|---|---|
| user_id | Composite PK, FK → Users.id |
| source_id | Composite PK, FK → Sources.id |
| is_enabled | |

---

## Sources
| Field | Type / Notes |
|---|---|
| id | PK |
| type | enum: `telegram` |
| is_enabled | |
| last_fetched_at | |
| chat_id | nullable |

**Relations:**
- `Sources.id` → `User sources.source_id`
- `Sources.id` → `Posts.source_id`

---

## Posts
| Field | Type / Notes |
|---|---|
| id | PK |
| source_id | FK, unique together (with external_id) → Sources.id |
| external_id | unique together (with source_id) |
| fingerprint | nullable, idx (sha256 hex от `from_norm`, `to_norm`, `price`) |
| raw_text | |
| from_location | |
| to_location | |
| price | |
| price_per_km | |
| published_at | |
| parsed_at | |
| status | enum: `new`, `ready`, `distributed`, `skipped`, `failed`, `duplicate` |
| from_norm | |
| to_norm | |
| duplicate_of_id | FK, nullable → Posts.id |

**Relations:**
- `Posts.id` → `Post deliveries.post_id`

---

## Post deliveries
| Field | Type / Notes |
|---|---|
| post_id | Composite PK, FK → Posts.id |
| user_id | Composite PK, FK → Users.id |
| tg_message_id | |
| created_at | |
| sent_at | nullable |
| status | enum: `pending`, `sent`, `failed`, `blocked` |

---

## Routes
| Field | Type / Notes |
|---|---|
| from_norm | Composite PK |
| to_norm | Composite PK |
| distance_km | |
| from_location | |
| to_location | |

*Note: no explicit connecting arrow shown to other tables in the diagram, but `from_norm`/`to_norm` appear to correspond to `Posts.from_norm`/`Posts.to_norm`.*