from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
from backend.core import menu as menu_core
import io
import json

router = APIRouter(prefix="/catalog", tags=["catalog"])

@router.post("/upload")
def upload_catalog(file: UploadFile = File(...)):
    """
    Store owner uploads a CSV or JSON menu/catalog.
    Parses and stores menu, generates shop_id, shop link, and QR code.
    """
    try:
        filename = file.filename.lower()
        if filename.endswith('.json'):
            # Handle JSON menu
            menu_items = json.load(file.file)
            if not isinstance(menu_items, list) or not menu_items:
                raise ValueError("JSON must be a non-empty list of menu items.")
            # Basic validation for required fields
            for row in menu_items:
                if not all(k in row for k in ("id", "name", "price", "currency")):
                    raise ValueError("Each menu item in JSON must have id, name, price, currency.")
        else:
            # Assume CSV
            text_file = io.TextIOWrapper(file.file, encoding="utf-8")
            menu_items = menu_core.parse_menu_csv(text_file)
            if not menu_items:
                raise ValueError("No valid menu items found in CSV.")
        shop_id = uuid.uuid4().hex[:8]
        menu_core.save_menu(shop_id, menu_items)
        # TODO: Generate real shop_link and qr_code_url
        shop_link = f"https://shopassist.ai/shop/{shop_id}"
        qr_code_url = f"https://shopassist.ai/qr/{shop_id}.png"
        return JSONResponse({
            "shop_id": shop_id,
            "shop_link": shop_link,
            "qr_code_url": qr_code_url
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 