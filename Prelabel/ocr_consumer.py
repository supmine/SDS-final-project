import pika, sys, os
import cv2
import json
import base64
import numpy as np
from utils import decode_jpg_from_string
from dotenv import load_dotenv
from models.ocr import OCR

from pymongo import MongoClient
import bson

load_dotenv
DATABASE_URL = os.environ.get("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client.kodwang

dataset_collection = db.dataset

# initial ocr model
model = OCR()

def main():
    """
    receive image from ocr queue and recognize it
    """

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="ocr")

    def callback(ch, method, properties, body):
        print(" [x] Received image for %r" % json.loads(body)["dataset_id"])
        image = decode_jpg_from_string(json.loads(body)["image"])
        prediction_result = model.predict(image)
        print("prediction result:", model.predict(image))

        # update dataset
        dataset_id = json.loads(body)["dataset_id"]
        entry_id = json.loads(body)["entry_id"]
        dataset = dataset_collection.find_one({"_id": bson.ObjectId(dataset_id)})
        for idx, entry in enumerate(dataset["entries"]):
            if entry["entry_id"] == bson.ObjectId(entry_id):
                print("added prelabel result to entry")
                dataset["entries"][idx]["prelabel"] = prediction_result.strip("\n").strip("/n/f")

        dataset_collection.update_one(
            {"_id": bson.ObjectId(dataset_id)},
            {"$set": {"entries": dataset["entries"]}},
        )
    
    channel.basic_consume(queue="ocr", on_message_callback=callback, auto_ack=True)
    
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
