from dataclasses import dataclass
from base64 import b64encode

from bson import ObjectId

from mongo import find_one, insert_one


@dataclass
class Response:
    response: dict
    status: bool | None


@dataclass()
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
    

    def auth(self) -> Response:
        account = find_one("users", dict(login=self.login))
        if account:

            if UserMongo(**account).passwd == self.passwd:
                return Response({"message": "login successful"}, True)
            return Response({"message": "Your password is not correct"}, False)

        return Response({"message": "account not found"}, None)


    def register(self) -> Response:
        result = find_one("users", dict(login=self.login, passwd=self.passwd))

        if not result:
            self.type = "standard"
            insert_one("users", self.__dict__)
            return Response({"message": "login created successful"}, True)
        return Response({"message": "account is exist"}, False)


@dataclass
class UserMongo:
    _id: ObjectId
    login: str
    passwd: str
    type: str
