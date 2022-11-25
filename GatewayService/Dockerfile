FROM python:3.7.3-alpine

COPY . /GatewayService
WORKDIR /GatewayService

RUN pip install -r requirements.txt

EXPOSE 8001

CMD  python -m uvicorn --host=0.0.0.0 --port=8000 src.main:app
