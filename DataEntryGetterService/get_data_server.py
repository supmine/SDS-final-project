from concurrent import futures
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import bson
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.kodwang

user_collection = db.user
dataset_collection = db.dataset


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


async def find_unlabel_entry(dataset_id):
    dataset = await find_dataset_by_id(dataset_id)
    for entry in dataset["entries"]:
        if "labeler_id" not in entry:
            return entry

@app.get("/")
async def root():
    return {"message": "Hello World"}

<<<<<<< HEAD
@app.get("/get_entry")
async def get_data(dataset_id):
    entry = await find_unlabel_entry(dataset_id)
    return entry
=======
class GetDataEntryServicer(get_data_entry_pb2_grpc.DataEntryGetterServicer):
    def GetDataEntry(self, request, context):
        response = get_data_entry_pb2.GetDataEntryResponse()
        entry = find_unlabel_entry(request.dataset_id)
        if entry:
            response.data_type = entry["entry_type"]
            response.data = entry["entry"]
            response.entry_id = str(entry["entry_id"])
            response.reward = entry["reward"]
            response.prelabel = ""
            if entry["prelabel"]:
                response.prelabel = entry["prelabel"]
        else:
            raise Exception("ALL ENTRIES IN THIS DATASET WERE LABELED")
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    get_data_entry_pb2_grpc.add_DataEntryGetterServicer_to_server(
        GetDataEntryServicer(), server
    )
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
>>>>>>> 96c55606d84913c4f951c70ab8f59795790d1475
