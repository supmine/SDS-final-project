import json
from webbrowser import get
from fastapi import APIRouter, Depends
import requests
from dotenv import load_dotenv
import os
from src.schema import RequestEntrySchema
from src.utils import validate_token
import time
import grpc


load_dotenv(".env")
GRPC_URL = os.environ.get("GRPC_URL")

grpc_router = APIRouter(
    prefix="/GRPC", tags=["GRPC"], responses={404: {"description": "Not Found"}}
)


@grpc_router.get("/{dataset_id}")
def request_data_entry(dataset_id: str, user = Depends(validate_token)):
    entry = requests.get(GRPC_URL+"/get_entry", params={"dataset_id": dataset_id})
    entry = entry.json()
    entry.pop("reward")
    if not entry["prelabel"]:
        entry["prelabel"] = ""
    return entry
