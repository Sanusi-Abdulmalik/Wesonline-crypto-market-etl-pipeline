"""
Crypto Market ETL Pipeline

Workflow
--------
Extract (CoinGecko API)
        ↓
Transform (JSON → Parquet)
        ↓
Upload Silver Layer to Amazon S3
"""

from datetime import datetime

from airflow.decorators import dag, task

from scripts.extract import extract
from scripts.transform import transform
from scripts.load_to_s3 import upload_latest_parquet


default_args = {
    "owner": "Abdulmalik Sanusi",
    "depends_on_past": False,
    "retries": 2,
}


@dag(
    dag_id="crypto_market_etl",
    description="Crypto Market ETL Pipeline (CoinGecko → S3)",
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=[
        "crypto",
        "fintech",
        "etl",
        "aws",
        "s3",
        "snowflake",
    ],
)
def crypto_market_pipeline():

    @task(task_id="extract_market_data")
    def run_extract():
        extract()

    @task(task_id="transform_market_data")
    def run_transform():
        transform()

    @task(task_id="upload_to_s3")
    def run_upload():
        upload_latest_parquet()

    extract_task = run_extract()
    transform_task = run_transform()
    upload_task = run_upload()

    extract_task >> transform_task >> upload_task


dag = crypto_market_pipeline()