from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bson

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.kodwang

user_collection = db.user
dataset_collection = db.dataset

async def find_user_by_email(email):
    user = user_collection.find_one({"email": email})
    if user:
        user["user_id"] = str(user.pop("_id"))
        return user
    else:
        return None


async def find_user_by_id(user_id):
    user = user_collection.find_one({"_id": bson.ObjectId(user_id)})
    if user:
        user["user_id"] = str(user.pop("_id"))
        return user
    else:
        return None


async def add_user(user):
    return user_collection.insert_one(user).inserted_id


async def set_user_balance(user_id, new_balance):
    return user_collection.update_one(
        {"_id": bson.ObjectId(user_id)},
        {"$set": {"balance": new_balance}},
    )


async def get_all_datasets():
    datasets = [e for e in dataset_collection.find({})]
    for dataset in datasets:
        dataset_id = str(dataset.pop("_id"))
        dataset["dataset_id"] = dataset_id
        for entry in dataset["entries"]:
            entry_id = entry.pop("entry_id")
            entry["entry_id"] = str(entry_id)
    return datasets


async def find_dataset_by_id(dataset_id):
    dataset = dataset_collection.find_one({"_id": bson.ObjectId(dataset_id)})
    if dataset:
        dataset["dataset_id"] = str(dataset.pop("_id"))
        for idx, entry in enumerate(dataset["entries"]):
            temp = entry.copy()
            temp["entry_id"] = str(temp.pop("entry_id"))
            dataset["entries"][idx] = temp
        return dataset
    return None


async def add_dataset(dataset):
    return dataset_collection.insert_one(dataset).inserted_id


async def delete_dataset_by_id(dataset_id):
    return dataset_collection.delete_one({"_id": bson.ObjectId(dataset_id)})


async def replace_dataset_by_id(dataset_id, new_dataset):
    return dataset_collection.replace_one(
        {"_id": bson.ObjectId(dataset_id)}, new_dataset
    )
