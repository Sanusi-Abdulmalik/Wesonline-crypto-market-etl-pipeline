"""
Apache Airflow DAG for the Crypto Market ETL Pipeline.

Workflow

Extract
    ↓
Transform
    ↓
Upload to Amazon S3
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.extract import extract
from scripts.transform import transform
from scripts.load_to_s3 import upload_latest_parquet


default_args = {
    "owner": "Abdulmalik Sanusi",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="crypto_market_etl",
    description="Daily Crypto Market ETL Pipeline",
    default_args=default_args,
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=[
        "etl",
        "crypto",
        "aws",
        "s3",
        "airflow",
    ],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_market_data",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform_market_data",
        python_callable=transform,
    )

    upload_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_latest_parquet,
    )

    extract_task.doc_md = """
    ### Extract

    Downloads the latest cryptocurrency market data from the CoinGecko API
    and stores it as partitioned raw JSON.
    """

    transform_task.doc_md = """
    ### Transform

    Cleans, validates, enriches and converts the raw JSON
    into a partitioned Parquet dataset.
    """

    upload_task.doc_md = """
    ### Load

    Uploads the latest Parquet dataset
    into the configured Amazon S3 bucket.
    """

    (
        extract_task
        >> transform_task
        >> upload_task
    )