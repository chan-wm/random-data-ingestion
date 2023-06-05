FROM python:3.9

RUN mkdir /random_data_ingestion

COPY src /random_data_ingestion/src

WORKDIR /random_data_ingestion

COPY setup.py /random_data_ingestion/setup.py

RUN pip install .

