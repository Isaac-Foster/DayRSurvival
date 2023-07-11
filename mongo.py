from bson.objectid import ObjectId
import pymongo, dotenv, os


dotenv.load_dotenv(dotenv.find_dotenv())

# CONNECT db
connect = pymongo.MongoClient(os.getenv("url"))

cur = connect.database


def find_one(collection: str, data: dict) -> dict | None:
    """
    This argument `collection` is refer for collection access 
    and use in database

    This function is used for query using argument type
    dict `data` in search in mongoDb

    Your return if find `data` is dict if not None
    """
    return cur[collection].find_one(data)


def insert_one(collection: str, data: dict) -> None:
    """
    This argument `collection` is refer for collection access 
    and use in database

    This function is used for insert `data` argument
    type `dict` content data the `object` type user or others
    """

    cur[collection].insert_one(data)


def update_data(collection: str, data: dict, **kwargs):
    """
    This argument `collection` is refer for collection access 
    and use in database
    
    This function is used for update data in database 
    if data is exists in database
    """
    cur[collection].update_one(data, {'$set': {**kwargs}})

