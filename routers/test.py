import json

from fastapi import APIRouter

from models.items import Item
from database import cur

router = APIRouter(
    prefix="/table",

)


@router.get("/", status_code=200)
async def root():
    return {"message": "hello word"}



@router.get("/items")
async def get_items():
    list_items = cur.execute("SELECT * FROM items").fetchall()

    list_response = []
    for name, amount, value in list_items:

        list_response.append(Item(name, amount, value).__dict__)
    
    return {"items": list_response}