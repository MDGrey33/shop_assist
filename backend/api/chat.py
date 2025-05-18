from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json
from typing import Optional
from backend.core import openai_assistants

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

ORDERS_DIR = os.path.join(os.path.dirname(__file__), '../../data/orders')
os.makedirs(ORDERS_DIR, exist_ok=True)

def is_checkout_intent(message: str) -> bool:
    """
    Simple keyword-based detection of order confirmation intent.
    """
    msg = message.lower()
    return any(kw in msg for kw in ["checkout", "that's all", "order it", "done", "pay now", "confirm order"])

@router.post("/{shop_id}")
async def chat_with_assistant(shop_id: str, req: ChatRequest = Body(...)):
    """
    Handles chat messages, routes to Waiter or Cashier assistant.
    Loads menu, manages thread, and calls OpenAI Assistant.
    If Waiter replies with 'Confirmed!', triggers Cashier Assistant, saves order JSON.
    """
    # Load menu
    menu_path = os.path.join(os.path.dirname(__file__), f"../content/menus/{shop_id}.json")
    if not os.path.exists(menu_path):
        raise HTTPException(status_code=404, detail="Menu not found for this shop.")
    with open(menu_path, "r", encoding="utf-8") as f:
        menu = json.load(f)
    # Thread management
    thread_id = req.thread_id
    if not thread_id:
        thread_id = await openai_assistants.create_thread()
    # Add user message
    print(f"[USER][{thread_id}]: {req.message}")
    await openai_assistants.add_message(thread_id, role="user", content=req.message)
    # Run Waiter Assistant
    menu_context = f"Always answer all questions based on the menu in context {{context: {menu}}}"  # can be improved
    try:
        reply = await openai_assistants.run_assistant(
            thread_id=thread_id,
            assistant_id=openai_assistants.WAITER_ASSISTANT_ID,
            extra_instructions=menu_context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")
    print(f"[AI][{thread_id}]: {reply}")
    # If reply is exactly 'Confirmed!', trigger Cashier Assistant
    if reply.strip() == "Confirmed!":
        print(f"[SYSTEM][{thread_id}]: Confirmed! detected, triggering cashier handoff.")
        try:
            order_json = await openai_assistants.run_cashier_and_extract_order_json(thread_id, menu)
            # Save order JSON to ./data/orders/{order_id}.json
            order_id = order_json.get("order_id")
            if order_id:
                order_path = os.path.join(ORDERS_DIR, f"{order_id}.json")
                with open(order_path, "w", encoding="utf-8") as f:
                    json.dump(order_json, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cashier error: {e}")
        return JSONResponse({
            "assistant": "cashier",
            "order_json": order_json,
            "thread_id": thread_id
        })
    # Otherwise, Waiter Assistant as before
    return JSONResponse({
        "assistant": "waiter",
        "reply": reply,
        "thread_id": thread_id
    }) 