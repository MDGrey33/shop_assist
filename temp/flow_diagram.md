# AI Shop Assistant — System Flow Diagram

## Mermaid Sequence Diagram

```mermaid
sequenceDiagram
    participant Owner as Store Owner
    participant UI as Shop UI
    participant API as Backend API
    participant Waiter as AI Waiter Assistant
    participant Cashier as AI Cashier Assistant
    participant Stripe as Stripe
    participant Storage as Order Storage

    Owner->>UI: Uploads CSV menu
    UI->>API: POST /api/catalog/upload
    API->>API: Parse & store menu
    API->>Owner: Returns shop link/QR

    Customer->>UI: Opens shop link
    UI->>API: GET /api/menu/{shop_id}
    API->>UI: Returns menu JSON
    UI->>Waiter: Start chat (menu in context)
    Customer->>Waiter: Chat, build order
    Waiter->>Customer: Answers, recommends, confirms
    Customer->>Waiter: "That's all" (order confirmed)
    UI->>API: POST /api/chat/{shop_id} (order confirmation)
    API->>Cashier: Clone thread, generate order JSON
    Cashier->>API: Returns final order JSON
    API->>UI: Show order summary
    UI->>API: POST /api/order/{shop_id} (order JSON)
    API->>Stripe: Create Checkout Session
    Stripe->>UI: Redirect to payment
    Stripe->>API: Webhook on payment success
    API->>Storage: Store order JSON in /content/orders/
    API->>UI: Confirm order to customer
    API->>Owner: Notify new order (future: email/dashboard)
```

---

## Textual Flow (Step-by-Step)

1. **Store Owner Onboarding**
    - Uploads CSV menu via UI
    - Backend parses, stores menu, returns shop link/QR
2. **Customer Ordering**
    - Opens shop link, menu loaded in context
    - Chats with Waiter Assistant (menu Q&A, order building)
    - On order confirmation, thread is cloned to Cashier Assistant
    - Cashier outputs final order JSON
3. **Payment**
    - System creates Stripe Checkout Session
    - Customer completes payment on Stripe
    - Stripe webhook notifies backend
4. **Order Storage & Fulfillment**
    - Order JSON stored in `/content/orders/`
    - Customer receives confirmation
    - Store owner notified (future: email/dashboard) 