FROM python:3.7-buster

COPY . /DatasetManagementService
WORKDIR /DatasetManagementService

RUN apt-get update

RUN apt-get install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD  python -m uvicorn --host=0.0.0.0 --port=8000 src.server:app
