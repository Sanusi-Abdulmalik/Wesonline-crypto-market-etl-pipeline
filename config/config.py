"""
Central configuration for the Crypto Market ETL Pipeline.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ARCHIVE_DIR = DATA_DIR / "archive"

LOGS_DIR = PROJECT_ROOT / "logs"
SQL_DIR = PROJECT_ROOT / "sql"

for directory in (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ARCHIVE_DIR,
    LOGS_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Pipeline Metadata
# ==========================================================

PIPELINE_NAME = "Crypto Market ETL"

PIPELINE_VERSION = "1.0.0"

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
)

# ==========================================================
# CoinGecko
# ==========================================================

COINGECKO_API = os.getenv(
    "COINGECKO_API",
    "https://api.coingecko.com/api/v3",
)

COINGECKO_MARKETS_ENDPOINT = "/coins/markets"

VS_CURRENCY = os.getenv(
    "VS_CURRENCY",
    "usd",
)

PER_PAGE = int(
    os.getenv(
        "PER_PAGE",
        100,
    )
)

PAGE = int(
    os.getenv(
        "PAGE",
        1,
    )
)

# ==========================================================
# HTTP Configuration
# ==========================================================

REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        30,
    )
)

MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        5,
    )
)

BACKOFF_FACTOR = float(
    os.getenv(
        "BACKOFF_FACTOR",
        1,
    )
)

# ==========================================================
# File Configuration
# ==========================================================

RAW_FILE_PREFIX = "crypto_market"

PROCESSED_FILE_PREFIX = "crypto_market"

PRETTY_PRINT_JSON = (
    os.getenv(
        "PRETTY_PRINT_JSON",
        "True",
    ).lower()
    == "true"
)

# ==========================================================
# AWS
# ==========================================================

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

S3_PREFIX = "silver"

# ==========================================================
# Snowflake
# ==========================================================

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")

SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")

SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")

SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")