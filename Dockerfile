FROM apache/airflow:2.10.0-python3.12

USER root

RUN apt-get update && apt-get install -y \
    default-jre \
    curl \
    gcc \
    g++ \
    build-essential \
    && apt-get clean

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

ENV PYTHONPATH=/opt/airflow

WORKDIR /opt/airflow