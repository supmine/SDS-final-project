FROM python:3.9

COPY . /DatasetManagementService
WORKDIR /DatasetManagementService

RUN apt-get update

RUN apt-get install -y git

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
