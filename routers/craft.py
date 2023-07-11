from fastapi import APIRouter, Response

from models.craft import Craft, Name, CraftCal
from mongo import insert_one

router = APIRouter(
    prefix="/craft",
)


@router.post("/register", tags=["admins"])
async def crafts(craft: Craft):
    insert_one("crafts", craft.__to_dict__())
    return craft


@router.post("/get", tags=["craft"])
async def crafts(craft: Name):
    return craft


@router.post("/calculator", tags=["craft"])
async def crafts(craft: CraftCal):
    craft.cost_items()
    return craft