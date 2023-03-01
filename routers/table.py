from fastapi import APIRouter, Request
from fastapi.datastructures import FormData

from database import cur
from models.items import (
    Item, 
    ItemDB, 
    Items
    )

router = APIRouter(
    prefix="/table",
)

def sql_items(limit: int, page: int, type_item: str):
    if type_item == "all":
        return cur.execute("SELECT * FROM items ORDER BY name ASC").fetchall()
    
    elif type_item in ("hunt", "item") and  limit <=0:
        return cur.execute("SELECT * FROM items WHERE type = ? ORDER BY name ASC",[type_item]).fetchall()

    return cur.execute(
        "SELECT * FROM items WHERE type = ? ORDER BY name ASC LIMIT ?  OFFSET ?",
        [type_item, limit, page]
        ).fetchall()       


@router.get("/{type_item}", tags=["table"])
async def get_items(type_item: str , limit: int = 0, page: int = 0):
    if type_item not in ("all", "hunt", "item"):
        return {"error": f"type item '{type_item}' not exists"} 
    
    list_items = sql_items(limit, page, type_item)
    
    list_response = [ItemDB(*x).__dict__ for x in list_items]

    return {"items": list_response}


@router.post("/calc", tags=["table"])
async def calc_items(items: Items):
    return items.sum()


@router.post("/register/{type_item}", tags=["admins"])
async def register_item(type_item: str, item: Item):

    item.__dict__.pop("__initialised__")

    if type_item not in ["hunt", "item"]:
        return {"error": f"{type_item} is not exists"}
    
    return {"status": "Item is add in database", **item.__dict__}


@router.put("/update", tags=["admins"])
async def update_item(item: Item):
    return


@router.delete("/delete", tags=["admins"])
async def delete_item(item: Item):
    ...
