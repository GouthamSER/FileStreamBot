from pymongo import MongoClient, errors
from bot.config import Telegram

client = MongoClient(Telegram.MONGO_URL)
db = client[Telegram.DB_NAME]
users = db["Users"]


def add_user(user_id: int, name: str):
    try:
        users.insert_one({"_id": user_id, "name": name})
        return True
    except errors.DuplicateKeyError:
        return False


def get_all_users():
    return users.find()


def remove_user(user_id: int):
    users.delete_one({"_id": user_id})