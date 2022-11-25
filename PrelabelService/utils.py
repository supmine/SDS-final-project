import cv2
import base64
import urllib.request
import numpy as np

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

