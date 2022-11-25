import json
from webbrowser import get
from fastapi import APIRouter, Depends
import requests
from dotenv import load_dotenv
import os
from src.schema import RequestEntrySchema
from src.utils import validate_token
import compile_protos.get_data_entry_pb2_grpc
import compile_protos.get_data_entry_pb2
import time
import grpc


load_dotenv(".env")
GRPC_URL = os.environ.get("GRPC_URL")

grpc_router = APIRouter(
    prefix="/GRPC", tags=["GRPC"], responses={404: {"description": "Not Found"}}
)


@grpc_router.get("/{dataset_id}")
def request_data_entry(dataset_id: str, user = Depends(validate_token)):
    try:
        with grpc.insecure_channel(GRPC_URL) as channel:
            stub = compile_protos.get_data_entry_pb2_grpc.DataEntryGetterStub(channel)
            get_data_entry_request = compile_protos.get_data_entry_pb2.GetDataEntryRequest(
                dataset_id=dataset_id
            )
            get_data_entry_reply = stub.GetDataEntry(get_data_entry_request)
    except Exception as e:
        print(e)
        return {"message": "Something Error"}

    return {
        "entry_type": get_data_entry_reply.data_type,
        "entry": get_data_entry_reply.data,
        "entry_id": get_data_entry_reply.entry_id,
        "prelabel": get_data_entry_reply.prelabel
    }
