"""
Apache Airflow DAG for the Crypto Market ETL Pipeline.

Pipeline Flow

    CoinGecko API
          │
          ▼
      Extract
          │
          ▼
     Transform
          │
          ▼
     Upload to S3
          │
          ▼
   Load Silver Layer
      (MERGE)
          │
          ▼
   Data Quality Checks
          │
          ▼
    Build Gold Layer
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


# ==========================================================
# Default Arguments
# ==========================================================

default_args = {
    "owner": "Abdulmalik Sanusi",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


# ==========================================================
# DAG Definition
# ==========================================================

with DAG(
    dag_id="crypto_market_etl",
    description="End-to-end Crypto Market ETL Pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    max_active_runs=1,
    tags=[
        "crypto",
        "etl",
        "snowflake",
        "aws",
        "airflow",
    ],
) as dag:

    dag.doc_md = """
# Crypto Market ETL Pipeline

## Pipeline

1. Extract cryptocurrency data from the CoinGecko API.
2. Transform and enrich the dataset.
3. Save the processed data as Parquet.
4. Upload Parquet files to Amazon S3.
5. Load data into the Snowflake Silver layer using MERGE.
6. Execute data quality checks.
7. Build analytical Gold views.

---

## Technologies

- Python
- Apache Airflow
- Snowflake
- Amazon S3
- Pandas
- PyArrow
- CoinGecko API
"""

    # ======================================================
    # Extract
    # ======================================================

    extract_task = BashOperator(
        task_id="extract_data",
        bash_command="python -m scripts.extract",
    )

    # ======================================================
    # Transform
    # ======================================================

    transform_task = BashOperator(
        task_id="transform_data",
        bash_command="python -m scripts.transform",
    )

    # ======================================================
    # Upload to S3
    # ======================================================

    upload_task = BashOperator(
        task_id="upload_to_s3",
        bash_command="python -m scripts.load_to_s3",
    )

    # ======================================================
    # Load Silver Layer
    # ======================================================

    silver_task = BashOperator(
        task_id="load_silver_layer",
        bash_command="python -m scripts.load_to_snowflake",
    )

    # ======================================================
    # Data Quality
    # ======================================================

    quality_task = BashOperator(
        task_id="run_data_quality",
        bash_command="python -m scripts.data_quality",
    )

    # ======================================================
    # Build Gold Layer
    # ======================================================

    gold_task = BashOperator(
        task_id="build_gold_layer",
        bash_command="python -m scripts.load_gold",
    )

    # ======================================================
    # Pipeline Dependencies
    # ======================================================

    (
        extract_task
        >> transform_task
        >> upload_task
        >> silver_task
        >> quality_task
        >> gold_task
    )