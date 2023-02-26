from dataclasses import dataclass
from enum import Enum


class TypeUser(Enum):
    user = "user"
    admin = "admin"


@dataclass
class User:
    login: str
    passwd: str
    type: TypeUser