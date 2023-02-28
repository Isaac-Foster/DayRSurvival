from pydantic import BaseModel


class User(BaseModel):
    login: str
    passwd: str


class UserMongo(User):
    type: str