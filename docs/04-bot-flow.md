# Bot flow

Legend:
- **Reply** - command/button
- **Inline** — inline button inside the message, contains a **Back** button
- For the answers - see [Messages](./05-messages.md)

---

## `/start` (Reply)
**Answer:** [`{Greeting}`](./05-messages.md)

Reply:
- `/on-off`
- `/config`
- `/source`
- `/payment`

---

## `/on-off` (Reply)
**Answer:** [`{On}`](./05-messages.md)/[`{Off}`](./05-messages.md)

---

## `/config` (Reply)
**Answer:** [`{Config}`](./05-messages.md)

Inline:
- `/price`
- **Back** → `/start`

### `/price` (Inline)
**Answer:** [`{PricePerKM}`](./05-messages.md)
**Reply:** [`{PriceUpdated}`](./05-messages.md)/[`{PriceInvalid}`](./05-messages.md)

Inline:
- **Back** → `/config`

---

## `/source` (Reply)
**Answer:** [`{Source}`](./05-messages.md)

Inline:
- `/{name}`
- **Back** → `/start`

### `/{name}` (Inline)
**Answer:** [`{SourceOn}`](./05-messages.md)/[`{SourceOff}`](./05-messages.md)

Inline:
- **Back** → `/source`

---

## `/payment` (Reply)
**Answer:** [`{Payment}`](./05-messages.md)

Inline:
- `/card`
- **Back** → `/start`

### `/card` (Inline)
**Answer:** [`{Card}`](./05-messages.md)
**Reply:** [`{PaymentSuccess}`](./05-messages.md)

Inline:
- **Back** → `/payment`

---

## Navigation tree

```
/start (Reply)
├─ /on-off (Reply)
├─ /config (Reply)
│   └─ /price (Inline, Back → /config)
├─ /source (Reply)
│   └─ /{name} (Inline, Back → /source)
└─ /payment (Reply)
    └─ /card (Inline, Back → /payment)
```