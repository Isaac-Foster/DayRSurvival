from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Response, Request
from models.users import User, UserMongo


router = APIRouter(
    prefix="/user",
    tags=["users"]
)


@router.post("/login")
async def login(user: User, response: Response, request: Request):
    resp =  user.auth()
    
    expire = (datetime.utcnow() + timedelta(seconds=15))

    if resp.status:
        response.set_cookie(
            key="access_token",
            value=uuid4(),
            expires=expire.strftime("%a, %d %b %Y %H:%M:%S GMT")
        )
    return resp.response


@router.post("/register")
async def register(user: User):
    resp = user.register()
    return resp.response