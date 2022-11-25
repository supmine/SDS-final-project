from concurrent import futures
import time
import grpc
import get_data_entry_pb2
import get_data_entry_pb2_grpc
from pymongo import MongoClient
import bson
import random as rnd
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.kodwang

user_collection = db.user
dataset_collection = db.dataset


def find_unlabel_entry(dataset_id):
    dataset = dataset_collection.find_one({"_id": bson.ObjectId(dataset_id)})
    for entry in dataset["entries"]:
        if "labeler_id" not in entry:
            return entry


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
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
