from fastapi import APIRouter, Response

from models.items import Craft, Name, CraftCal
from mongo import connect

router = APIRouter(
    prefix="/craft",
)

cur = connect.database.crafts

@router.post("/register", tags=["admins"])
async def crafts(craft: Craft):
    cur.insert_one(craft.__to_dict__())
    return craft


@router.post("/get", tags=["craft"])
async def crafts(craft: Name):
    return craft


@router.post("/calculator", tags=["craft"])
async def crafts(craft: CraftCal):
    craft.cost_items()
    return craft