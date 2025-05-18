# AI Shop Assistant — API Contracts

## 1. Catalog Upload

**POST /api/catalog/upload**
- **Description:** Store owner uploads a CSV **or JSON** menu/catalog. Returns shop link/QR.
- **Request:**
  - **CSV:** File with columns: `id,name,price,currency` (and optional fields)
  - **JSON:** File containing a list of menu items, each with `id`, `name`, `price`, `currency` (and optional fields)
  - Example JSON:
    ```json
    [
      {"id": "big_mac", "name": "Big Mac®", "price": 4.95, "currency": "EUR"},
      {"id": "small_fries", "name": "French Fries (Small)", "price": 1.35, "currency": "EUR"}
    ]
    ```
- **Response:**
```json
{
  "shop_id": "string",
  "shop_link": "string",
  "qr_code_url": "string"
}
```
- **Notes:**
  - The endpoint auto-detects file type by extension (`.csv` or `.json`).
  - All menu items must have `id`, `name`, `price`, and `currency` fields.
  - The response is the same for both formats.

---

## 2. Get Menu

**GET /api/menu/{shop_id}**
- **Description:** Returns menu JSON for assistant context.
- **Response:**
```json
{
  "menu": [
    { "id": "string", "name": "string", "price": 0.0, ... }
  ]
}
```

---

## 3. Chat (Waiter/Cashier)

**POST /api/chat/{shop_id}**
- **Description:** Handles chat messages, routes to Waiter or Cashier assistant. Uses OpenAI Assistants API with threads; chat history is managed by OpenAI, not locally. Returns thread_id for continued conversation.
- **Request:**
```json
{
  "thread_id": "string", // optional, for ongoing chat
  "message": "string"
}
```
- **Response:**
```json
{
  "assistant": "waiter|cashier",
  "reply": "string",
  "thread_id": "string", // always returned for context
  "order_json": { ... } // only present if cashier outputs final order
}
```
- **Notes:**
  - Endpoint is async.
  - Pass thread_id on each request to maintain context.
  - No need to manage chat history locally; OpenAI stores all messages in the thread.

---

## 4. Create Order & Stripe Checkout

**POST /api/order/{shop_id}**
- **Description:** Receives final order JSON, creates Stripe session.
- **Request:**
```json
{
  "order": { ... } // order JSON from cashier assistant
}
```
- **Response:**
```json
{
  "checkout_url": "string",
  "order_id": "string"
}
```

---

## 5. Stripe Webhook

**POST /api/stripe/webhook**
- **Description:** Handles Stripe payment events.
- **Request:** Stripe event payload
- **Response:**
```json
{
  "status": "ok"
}
```

---

## 6. Order Status

**GET /api/order/status/{order_id}**
- **Description:** Returns order/payment status.
- **Response:**
```json
{
  "order_id": "string",
  "status": "pending|paid|failed|fulfilled",
  "details": { ... }
}
``` 