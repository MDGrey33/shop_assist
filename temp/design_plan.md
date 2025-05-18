# AI Shop Assistant — Design & Architecture Plan

## 1. Overview

A conversational AI shop assistant platform enabling small businesses to sell via chat. Store owners upload a CSV menu/catalog, get a shareable link/QR, and customers can order and pay via chat with Stripe integration. The system minimizes friction and steps to complete a sale.

---

## 2. Actors & Roles

- **Store Owner**: Uploads catalog, receives shop link/QR.
- **Customer**: Interacts with AI assistant to place an order and pay.
- **AI Waiter Assistant**: Greets, answers questions, helps build order.
- **AI Cashier Assistant**: On order confirmation, generates final order JSON for Stripe.
- **System**: Orchestrates chat, payment, order storage, and delivery notification.

---

## 3. End-to-End User Flow

### A. Store Owner Onboarding
1. Store owner signs up/logs in.
2. Uploads CSV menu/catalog.
3. System parses and stores menu as JSON.
4. System generates unique shop link/QR code for sharing.

### B. Customer Ordering Experience
1. Customer opens shop link (mobile/web).
2. **Waiter Assistant** greets and loads menu in context.
3. Customer chats, asks questions, and builds order.
4. When customer confirms order ("that's all", "checkout", etc.):
    - System clones the thread and switches to **Cashier Assistant**.
    - Cashier Assistant generates a final order JSON (per schema).
5. System uses order JSON to:
    - Trigger Stripe Checkout (redirect or embedded).
    - On payment success, confirm order to customer.
    - Store order JSON in `/content/orders/` for delivery/fulfillment.

---

## 4. System Components & Responsibilities

| Component                | Responsibility                                                                 |
|--------------------------|-------------------------------------------------------------------------------|
| **Frontend**             | Chat UI, Stripe Checkout integration, order confirmation, QR code display      |
| **Backend (FastAPI)**    | API endpoints, file upload, menu parsing, order orchestration, webhook handling|
| **AI Assistants**        | Waiter: chat, recommend, build order; Cashier: generate final order JSON       |
| **Storage**              | Menus, orders, user/shop data (DB or file-based for MVP)                       |
| **Stripe Integration**   | Payment session creation, webhook for payment confirmation                     |

---

## 5. Directory Structure Proposal

```
shop_assist/
│
├── backend/
│   ├── api/                # FastAPI endpoints (catalog, chat, order, payment)
│   ├── assistants/         # Assistant prompt templates, OpenAI integration
│   ├── core/               # Business logic (order, menu, chat orchestration)
│   ├── db/                 # DB models, migrations (or file storage for MVP)
│   ├── services/           # Stripe, file storage, QR code, etc.
│   ├── content/
│   │   ├── menus/          # Uploaded menus per shop
│   │   └── orders/         # Order JSONs for delivery/fulfillment
│   ├── config/             # Settings, constants, environment
│   └── main.py             # FastAPI app entrypoint
│
├── frontend/
│   ├── public/             # Static files, QR code images
│   ├── src/                # React or HTML/JS chat UI
│   └── ...
│
├── data/                   # Example menus, assistant prompt docs
├── temp/                   # Design docs, plans, progress tracking
├── tests/                  # Unit and integration tests
├── pyproject.toml          # Poetry config
└── README.md
```

---

## 6. API & Service Design

### Endpoints
- `POST /api/catalog/upload` — Store owner uploads CSV or JSON, returns shop link.
- `GET /api/menu/{shop_id}` — Returns menu JSON for assistant context.
- `POST /api/chat/{shop_id}` — Handles chat messages, routes to Waiter or Cashier.
- `POST /api/order/{shop_id}` — Receives final order JSON, creates Stripe session.
- `POST /api/stripe/webhook` — Handles Stripe payment events.
- `GET /api/order/status/{order_id}` — Returns order/payment status.

---

## 7. Chat Flow & Cashier Handoff

- **Waiter Assistant** handles all customer interaction until the customer confirms the order (e.g., "that's all", "checkout", "order it").
- The backend detects confirmation intent using simple keyword matching (MVP) or more advanced NLP (future).
- On confirmation, the backend calls the **Cashier Assistant** with the full thread and menu context.
- The Cashier Assistant generates and returns the final order JSON (per schema), which is extracted from the assistant's reply.
- The backend returns the order JSON in the API response, ready for payment processing.

---

## 8. CQRS & Clean Architecture

- **Command**: Catalog upload, order creation, payment processing.
- **Query**: Menu retrieval, order status, chat history.
- **Domain Layer**: Entities for Product, Order, Shop, etc.
- **Application Layer**: Use cases for onboarding, chat, order, payment.
- **Infrastructure Layer**: Stripe, file storage, OpenAI API.
- **Presentation Layer**: REST API, WebSocket for chat.

---

## 9. Security & Privacy

- No payment data handled by us; Stripe Checkout only.
- Store owner authentication (email/magic link, MVP can be simple).
- Orders stored with minimal PII (just enough for fulfillment).

---

## 10. Observability & Logging

- Log all order/payment events with unique request IDs.
- Stripe webhook logs for debugging.
- No sensitive data in logs.

---

## 11. Testing

- Unit tests for all core logic (menu parsing, order building, Stripe integration).
- Integration tests for chat flow, payment, and order storage.
- No production code changes while writing/fixing tests.

---

## 12. Monitoring

- Optional: Stripe dashboard for payment monitoring.
- Simple admin dashboard for order tracking (future).

---

## 13. Open Questions

1. **Authentication**: Should store owners have a login, or is a magic link/shop code enough for MVP?
2. **Frontend**: Do you want a React-based chat UI, or is a simple HTML/JS widget sufficient for MVP?
3. **Order Fulfillment**: How will store owners receive/fulfill orders? (Email, dashboard, webhook, etc.)
4. **Multi-language**: Is English-only fine for MVP, or should we plan for localization?
5. **Hosting**: Any preferences for deployment (Vercel, Heroku, self-hosted, etc.)? 