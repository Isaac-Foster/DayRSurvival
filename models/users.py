from dataclasses import dataclass


@dataclass
class User:
    login: str
    passwd: str


@dataclass
class UserMongo(User):
    type: str