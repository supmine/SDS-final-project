FROM python:3.7

COPY . /PrelabelService
WORKDIR /PrelabelService

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3", "ocr_consumer.py"]