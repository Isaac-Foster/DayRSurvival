from dataclasses import dataclass
from base64 import b64encode

from bson import ObjectId

@dataclass
class User:
    login: str
    passwd: str

    def __post_init__(self):
        """
        This function is used to, as soon as the `user` object is invoked,
        go to post_init and encrypt the password to be sent to the database
        """

        self.passwd = b64encode(
            self.passwd.encode("utf-8")
            ).decode("utf-8")

@dataclass
class UserMongo:
    _id: ObjectId
    login: str
    passwd: str
    type: str