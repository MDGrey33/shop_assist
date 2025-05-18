# AI Shop Assistant — Progress Plan

| Task                                      | Status      | Notes/Next Steps                         |
|-------------------------------------------|-------------|------------------------------------------|
| Design & architecture documentation       | Complete    | See /temp/design_plan.md                 |
| Directory structure setup                 | Complete    | Initial folders and files created        |
| API contract sketching                    | Complete    | See /temp/api_contracts.md               |
| Backend skeleton & health endpoint        | In Progress | FastAPI app, CORS, health, routers       |
| Menu/catalog endpoints                    | In Progress | Placeholders, ready for business logic   |
| Menu/catalog upload & parsing             | Complete    | CSV to JSON, validation                  |
| AI Waiter Assistant integration           | In Progress | OpenAI Assistants API, threads used      |
| Chat endpoint                             | In Progress | /chat/{shop_id}, OpenAI thread mgmt      |
| AI Cashier Assistant integration          | Pending     | Thread cloning, order JSON generation    |
| Stripe payment integration                | Pending     | Checkout session, webhook, confirmation  |
| Order storage (content/orders)            | Pending     | Store order JSON on payment success      |
| Frontend chat UI (MVP)                    | Pending     | Simple, embeddable, Stripe redirect      |
| Store owner onboarding (MVP)              | Pending     | Auth, upload, QR/link generation         |
| Unit & integration tests                  | Pending     | Core logic, chat, payment, storage       |
| Deployment setup                          | Pending     | Docker, Poetry, hosting                  |

---

## Notes & Decisions
- .env file to be created for OpenAI API key (see env_info).
- Chat history is managed by OpenAI threads, not locally.
- All code and documentation to follow Cursor coding standards and project workflow. 