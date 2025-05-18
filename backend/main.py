"""
AI Shop Assistant Backend Entrypoint
See /temp/design_plan.md for architecture and flow details.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import catalog
from backend.api import menu
from backend.api import chat

app = FastAPI(title="AI Shop Assistant API")

# CORS setup (allow all for dev; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["system"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

app.include_router(catalog.router)
app.include_router(menu.router)
app.include_router(chat.router)

# TODO: Include order, payment routers
