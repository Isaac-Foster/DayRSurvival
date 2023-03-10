from bson.objectid import ObjectId
import pymongo


from models.users import UserMongo
from config import url

# CONNECT db
connect = pymongo.MongoClient(url)

cur = connect.database.users
    

def find_one(*args, **kwargs) -> None | dict:
    query_result = cur.find_one(args[0] if args else kwargs)
    if query_result:
        return query_result
    return None


def insert_one(*args, **kwargs) -> None:
    response = (
        dict(success=(cur.insert_one(args[0] if args else kwargs)) != None)
        if not find_one(*args or kwargs)
        else dict(error="existing User")
        )
    return response


def update_data(data: dict, update: dict):
    return cur.update_one(data, {'$set': update}, upsert=True)
