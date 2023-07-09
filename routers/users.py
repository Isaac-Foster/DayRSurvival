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
async def login(user: User):
    result = find_one(user.__dict__)

    if result:
        return {"message": "login successful"}

    return {"message": "account not found"}


@router.post("/register")
async def register(user: User):
    
    result = find_one(user.__dict__)
    if not result:
        insert_one(user.__dict__)
        return {"message": "login created successful"}

    return {"message": "account is exist"}