from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from src.database import find_user_by_email
import os
from dotenv import load_dotenv
from jose import jwt
import urllib
import cv2
import numpy as np
import base64
import pika
import json

load_dotenv()
SECRET_KEY = os.environ.get("OAUTH_SECRET_KEY")
ALGORITHM = os.environ.get("OAUTH_ALGORITHM")
RABBITMQ_URL = os.environ.get("RABBITMQ_URL")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(http_authorization_credentials=Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(http_authorization_credentials.credentials,SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials",
        )
    user = await find_user_by_email(payload["email"])
    return user

def decode_jpg_from_string(encoded_string):  
    jpg_original = base64.b64decode(encoded_string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    image = cv2.imdecode(jpg_as_np, flags=1)
    return image

def encode_jpg_from_path(image_path):
    image = cv2.imread(image_path)
    encoded_image = base64.b64encode(cv2.imencode(".jpg", image)[1]).decode()
    return encoded_image

def encode_jpg_from_array(image):
    encoded_image = base64.b64encode(cv2.imencode(".jpg", image)[1]).decode()
    return encoded_image

def read_img_from_url(url):
    url_response = urllib.request.urlopen(url)
    image = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
    return image

def send_to_ocr_queue(url, dataset_id, entry_id):
    """
    Send an image to the ocr queue
    """
    image = read_img_from_url(url)
    encoded_image = encode_jpg_from_array(image)
    encoded_image = base64.b64encode(cv2.imencode(".jpg", image)[1]).decode()

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue="ocr")

    # send json with file name and encoded image
    channel.basic_publish(exchange="",
                          routing_key="ocr",
                          body=json.dumps({"image": encoded_image,
                                           "dataset_id": dataset_id,
                                           "entry_id": entry_id,}))

    print(" [x] Sent image to ocr queue")

    connection.close()
