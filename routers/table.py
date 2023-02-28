from fastapi import APIRouter, Request
from fastapi.datastructures import FormData

from models.items import Item, ItemDB, Items
from database import cur

router = APIRouter(
    prefix="/table",
    tags=["table"]

)

def sql_items(limit: int, page: int, table: str):
    return (
        cur.execute(f"SELECT * FROM {table}").fetchall() if not limit or limit <= 0 
        else cur.execute(f"SELECT * FROM {table} LIMIT ? OFFSET ?",
        [limit, page]
        ).fetchall()
    )


@router.get("/items")
async def get_items(limit: int = 0, page: int = 0):
    
    list_items = sql_items(limit, page, "items")
    
    list_response = [
        ItemDB(name, amount, value, "item").__dict__
        for name, amount, value in list_items
        ]

    return {"items": list_response}


@router.get("/hunts")
async def get_hunts(limit: int = 0, page: int = 0):
    
    list_items = sql_items(limit, page, "hunts")

    list_response = [
        ItemDB(name, amount, value, "hunt").__dict__
        for name, amount, value in list_items
        ]
    print(list_response[0])
    return {"hunts": list_response}



@router.post("/register/{name}")
async def register_item(name: str, item: Item):

    del item.__dict__["__initialised__"]

    if name not in ["hunt", "item"]:
        return {"error": f"{name} is not exists"}
    
    
    return {"status": "Item is add in database", **item.__dict__}


@router.post("/calc")
async def calc_items(data: Items):
    return data.sum()
