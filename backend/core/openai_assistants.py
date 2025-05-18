import os
import openai
from typing import Optional, Any, Dict
import re
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# These IDs should be configured per shop in a real system
WAITER_ASSISTANT_ID = os.getenv("WAITER_ASSISTANT_ID", "asst_jTLxa2xosPeoZMZ5raa6MOnv")
CASHIER_ASSISTANT_ID = os.getenv("CASHIER_ASSISTANT_ID", "asst_28YxUVRxwvOfsr5RK96nPlyy")

async def create_thread() -> str:
    """
    Create a new OpenAI thread and return its ID.
    Note: openai.beta.threads.create() is synchronous.
    """
    thread = openai.beta.threads.create()
    return thread.id

async def add_message(thread_id: str, role: str, content: str):
    """
    Add a message to an OpenAI thread.
    Note: openai.beta.threads.messages.create() is synchronous.
    """
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )

async def run_assistant(thread_id: str, assistant_id: str, extra_instructions: Optional[str] = None) -> str:
    """
    Run the assistant on the thread and return the latest reply.
    Note: openai.beta.threads.runs.create() and .retrieve() are synchronous.
    """
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=extra_instructions or None
    )
    # Wait for completion (polling for MVP)
    import asyncio
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status in ("completed", "failed", "cancelled"):
            break
        await asyncio.sleep(0.5)
    if run_status.status != "completed":
        raise RuntimeError(f"Assistant run failed: {run_status.status}")
    # Get the latest assistant message
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    # Sort messages by created_at descending to get the latest
    sorted_msgs = sorted(messages.data, key=lambda m: m.created_at, reverse=True)
    for msg in sorted_msgs:
        if msg.role == "assistant":
            return msg.content[0].text.value
    raise RuntimeError("No assistant reply found.")

async def run_cashier_and_extract_order_json(thread_id: str, menu: Any) -> Dict:
    """
    Run the Cashier Assistant on the thread and extract the first valid JSON object (order) from its reply.
    """
    menu_context = f"Always answer all questions based on the menu in context {{context: {menu}}}"
    reply = await run_assistant(thread_id, CASHIER_ASSISTANT_ID, extra_instructions=menu_context)
    # Extract first JSON object from reply
    match = re.search(r'\{[\s\S]*?\}', reply)
    if not match:
        raise RuntimeError("No JSON object found in cashier assistant reply.")
    try:
        order_json = json.loads(match.group(0))
    except Exception as e:
        raise RuntimeError(f"Failed to parse order JSON: {e}")
    return order_json 