# AI Shop Assistant

A conversational AI shop assistant platform for small businesses. Store owners upload a CSV menu/catalog, get a shareable link/QR, and customers can order and pay via chat with Stripe integration. Built for minimal friction and easy onboarding.

## Features
- Chat-based ordering with OpenAI Assistants (Waiter & Cashier roles)
- Catalog upload (CSV), instant shop link/QR generation
- Stripe payment integration (secure, no card data handled by us)
- Order storage for fulfillment
- Simple, embeddable frontend UI

## Architecture
- **Backend:** FastAPI, modular clean architecture
- **AI:** OpenAI Assistants (menu-aware Waiter, order-building Cashier)
- **Payments:** Stripe Checkout
- **Frontend:** React or HTML/JS (embeddable chat UI)
- **Storage:** File-based for MVP (menus, orders)

See `/temp/design_plan.md` and `/temp/flow_diagram.md` for full design and flow details.

## Quickstart (Dev)
1. Clone repo
2. Install dependencies with Poetry: `poetry install`
3. Run backend: `poetry run uvicorn backend.main:app --reload`
4. (Optional) Start frontend dev server
5. See `/temp/` for API contracts and design docs

---

For more, see the detailed documentation in `/temp/`.
