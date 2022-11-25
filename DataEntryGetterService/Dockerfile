FROM python:3.9

COPY . /DataEntryGetterService
WORKDIR /DataEntryGetterService

RUN apt-get update

RUN apt-get install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "get_data_server.py"]
