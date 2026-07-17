FROM apache/airflow:2.10.0

USER root

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC

RUN apt-get update -o Acquire::Check-Date=false -o Acquire::Check-Valid-Until=false && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

WORKDIR /opt/airflow

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt