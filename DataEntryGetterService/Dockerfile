FROM python:3.9

COPY . /DataEntryGetterService
WORKDIR /DataEntryGetterService

RUN apt-get update

RUN apt-get install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8002

CMD ["uvicorn", "get_data_server:app", "--host", "0.0.0.0", "--port", "8002"]
