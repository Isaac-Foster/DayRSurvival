import json

from fastapi import APIRouter

from models.items import Item, Types
from database import cur

router = APIRouter(
    prefix="/table",

)


@router.get("/items")
async def get_items(limit: int = 0, page: int = 0):
    
    list_items = (
        cur.execute("SELECT * FROM items").fetchall() if not limit or  limit <= 0 
        else cur.execute("SELECT * FROM items LIMIT ? OFFSET ?",
        [limit, page]
        ).fetchall()
    )

    list_response = [
        Item(name, amount, value, Types.item.value).__dict__ 
        for name, amount, value in list_items
        ]

    return {"items": list_response}


@router.get("/hunts")
async def get_items(limit: int = 0, page: int = 0):
    
    list_items = (
        cur.execute("SELECT * FROM hunts").fetchall() if not limit or  limit <= 0 
        else cur.execute("SELECT * FROM items LIMIT ? OFFSET ?",
        [limit, page]
        ).fetchall()
    )

    list_response = [
        Item(name, amount, value, Types.hunt.value).__dict__ 
        for name, amount, value in list_items
        ]

    return {"items": list_response}