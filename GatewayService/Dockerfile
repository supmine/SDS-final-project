FROM python:3.7-buster

COPY . /GatewayService
WORKDIR /GatewayService

RUN apt-get update

RUN apt-get install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8001

CMD  python -m uvicorn --host=0.0.0.0 --port=8001 src.main:app
