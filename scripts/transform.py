"""
Transform raw CoinGecko JSON into a curated Parquet dataset.
"""

import pandas as pd

from config.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    PIPELINE_NAME,
    PIPELINE_VERSION,
    ENVIRONMENT,
    PROCESSED_FILE_PREFIX,
)

from config.schemas import (
    get_selected_columns,
    get_dtype_mapping,
    get_datetime_columns,
)

from scripts.io import (
    read_json,
    write_parquet,
)

from scripts.logger import logger

from scripts.utils import (
    current_datetime,
    get_latest_file,
    create_file_path,
)

from scripts.validations import (
    validate_dataframe,
    validation_summary,
)

DATASET = "crypto_market"


# ==========================================================
# Extract Records
# ==========================================================

def load_raw_payload():
    """
    Load the latest raw JSON payload.
    """

    raw_file = get_latest_file(
        RAW_DATA_DIR,
        "json",
    )

    logger.info(f"Latest raw file: {raw_file}")

    return read_json(raw_file)


# ==========================================================
# Create DataFrame
# ==========================================================

def build_dataframe(payload: dict) -> pd.DataFrame:
    """
    Convert JSON payload into a DataFrame.
    """

    records = payload["data"]

    df = pd.DataFrame(records)

    logger.info(f"Loaded {len(df)} records.")

    return df


# ==========================================================
# Select Required Columns
# ==========================================================

def select_columns(df: pd.DataFrame) -> pd.DataFrame:

    columns = get_selected_columns(DATASET)

    return df[columns]


# ==========================================================
# Apply Schema
# ==========================================================

def apply_schema(df: pd.DataFrame) -> pd.DataFrame:

    logger.info("Applying schema...")

    dtype_map = get_dtype_mapping(DATASET)

    df = df.astype(dtype_map)

    for column in get_datetime_columns(DATASET):

        df[column] = pd.to_datetime(
            df[column],
            utc=True,
            errors="coerce",
        )

    return df


# ==========================================================
# Add Metadata
# ==========================================================

def add_pipeline_metadata(
    df: pd.DataFrame,
    metadata: dict,
) -> pd.DataFrame:
    """
    Add ETL metadata columns.
    """

    df["batch_id"] = metadata["batch_id"]

    df["pipeline_name"] = PIPELINE_NAME

    df["pipeline_version"] = PIPELINE_VERSION

    df["environment"] = ENVIRONMENT

    df["ingested_at"] = current_datetime()

    return df


# ==========================================================
# Save Silver Layer
# ==========================================================

def save_dataframe(df: pd.DataFrame):

    output_path = create_file_path(
        PROCESSED_DATA_DIR,
        PROCESSED_FILE_PREFIX,
        "parquet",
    )

    stats = write_parquet(
        df,
        output_path,
    )

    logger.info(
        f"Silver dataset saved to {output_path}"
    )

    return stats


# ==========================================================
# Main Pipeline
# ==========================================================

def transform():

    logger.info("=" * 60)
    logger.info("Starting Transformation Pipeline")
    logger.info("=" * 60)

    payload = load_raw_payload()

    metadata = payload["metadata"]

    df = build_dataframe(payload)

    df = select_columns(df)

    df = apply_schema(df)

    df = add_pipeline_metadata(
        df,
        metadata,
    )

    validate_dataframe(
        df,
        DATASET,
    )

    validation_summary(df)

    stats = save_dataframe(df)

    logger.info("=" * 60)
    logger.info("Transformation Completed Successfully")
    logger.info("=" * 60)

    return stats


if __name__ == "__main__":
    transform()