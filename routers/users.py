from random import choice
from string import digits


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


def generate_id():
    while 1:
        _id = int("".join([choice(digits) for _ in range(16)]))

        if not find_one(_id=_id):
            return _id


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
        user._id = generate_id()
        user.type = "standard"
        insert_one(user.__dict__)
        return {"message": "login created successful"}

    return {"message": "account is exist"}