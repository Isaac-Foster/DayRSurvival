from fastapi import APIRouter
from models.users import User

from mongo import (
    find_one,
    insert_one, 
    update_data
    )

router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/login")
async def login_user(user: User):
    result = find_one(user.dict())

    if result:
        return {"message": "login successful"}

    return {"message": "account not found"}


@router.post("/register")
async def login_user(user: User):
    result = find_one(user.dict())

    if not result:
        insert_one(user)
        return {"message": "login created successful"}

    return {"message": "account is exist"}