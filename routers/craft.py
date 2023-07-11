from fastapi import APIRouter, Response

from models.craft import Craft, Name, CraftCal
from mongo import insert_one, find_one

router = APIRouter(
    prefix="/craft",
)


@router.post("/register", tags=["admins"])
async def crafts(craft: Craft):
    print(craft)
    if not find_one("crafts", dict(name=craft.name)):
        #insert_one("crafts", craft.__to_dict__())
        return craft
    return {"message": f"This is `{craft.name}` is exists"}

@router.post("/get", tags=["craft"])
async def crafts(craft: Name):
    return craft


@router.post("/calculator", tags=["craft"])
async def crafts(craft: CraftCal):
    craft.cost_items()
    return craft