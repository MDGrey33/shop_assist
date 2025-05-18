from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import os
import json
from backend.core import menu as menu_core

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/{shop_id}")
def get_menu(shop_id: str):
    """
    Returns menu JSON for assistant context.
    Loads menu from storage by shop_id.
    """
    path = os.path.join(os.path.dirname(__file__), f"../content/menus/{shop_id}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Menu not found for this shop.")
    with open(path, "r", encoding="utf-8") as f:
        menu = json.load(f)
    return JSONResponse({"menu": menu}) 