from pymongo import MongoClient
import os

my_secret = os.environ['DB_KEY']

cluster = MongoClient(
    f"mongodb+srv://user:{str(my_secret)}@cluster0.xjask.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)
db = cluster["tags"]
collection = db["tags"]


async def _create_tag(_id: str, owner: int, text: str):
    collection.insert_one({'_id': _id, 'owner': owner, 'text': text})


async def _update_tag_name(_id: str, new_id: str):
    data = collection.find_one({'_id': new_id})
    if not data:
        collection.update_one({'_id': _id}, {"$set": {'_id': new_id}})


async def _update_tag_text(_id: str, text: str):
    collection.update_one({'_id': _id}, {'$set': {'text': text}})


async def _delete_tag(_id: str):
    collection.delete_one({'_id': _id})


async def _tranfer_tag_ownership(_id: str, new_owner: int):
    collection.update_one({'_id': _id}, {"$set": {'owner': new_owner}})
