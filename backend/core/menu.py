import csv
import json
import os
from typing import List, Dict, IO

MENU_DIR = os.path.join(os.path.dirname(__file__), '../content/menus')


def parse_menu_csv(file: IO) -> List[Dict]:
    """
    Parse a CSV file-like object and return a list of menu items as dicts.
    Expects columns: id, name, price, currency, [optional fields]
    """
    reader = csv.DictReader(file)
    items = []
    for row in reader:
        # Basic validation: must have id, name, price, currency
        if not all(k in row for k in ("id", "name", "price", "currency")):
            continue
        # Convert price to float
        try:
            row["price"] = float(row["price"])
        except Exception:
            continue
        items.append(row)
    return items


def save_menu(shop_id: str, menu: List[Dict]):
    """
    Save the menu as JSON to backend/content/menus/{shop_id}.json
    """
    os.makedirs(MENU_DIR, exist_ok=True)
    path = os.path.join(MENU_DIR, f"{shop_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=2) 