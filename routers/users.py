from random import choice
from string import digits


from fastapi import APIRouter
from models.users import User, UserMongo


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
    
    account = find_one(dict(login=user.login))

    if account:

        if UserMongo(**account).passwd == user.passwd:
            return {"message": "login successful"}

        return {"message": "Your password is not correct"}

    return {"message": "account not found"}


@router.post("/register")
async def register(user: User):
    
    result = find_one(user.__dict__)
    if not result:
        user.type = "standard"

        insert_one(user.__dict__)
        return {"message": "login created successful"}

    return {"message": "account is exist"}