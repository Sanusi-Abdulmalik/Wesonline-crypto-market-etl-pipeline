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
# Load Raw Payload
# ==========================================================

def load_raw_payload() -> dict:
    """
    Load the most recent raw CoinGecko payload.
    """

    raw_file = get_latest_file(
        RAW_DATA_DIR,
        "json",
    )

    logger.info(f"Latest raw file: {raw_file}")

    return read_json(raw_file)


# ==========================================================
# Build DataFrame
# ==========================================================

def build_dataframe(payload: dict) -> pd.DataFrame:
    """
    Convert JSON payload into a DataFrame.
    """

    df = pd.DataFrame(payload["data"])

    logger.info(f"Loaded {len(df)} records.")

    return df


# ==========================================================
# Select Required Columns
# ==========================================================

def select_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Keep only required columns.
    """

    return df[
        get_selected_columns(DATASET)
    ]


# ==========================================================
# Apply Schema
# ==========================================================

def apply_schema(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply data types and standardize datetime columns.
    """

    logger.info("Applying schema...")

    dtype_map = get_dtype_mapping(DATASET)

    datetime_columns = set(
        get_datetime_columns(DATASET)
    )

    # Apply non-datetime dtypes first
    non_datetime_dtypes = {
        column: dtype
        for column, dtype in dtype_map.items()
        if column not in datetime_columns
    }

    df = df.astype(non_datetime_dtypes)

    # Convert timestamps
    for column in datetime_columns:

        logger.info(f"Formatting {column}")

        df[column] = (
            pd.to_datetime(
                df[column],
                utc=True,
                errors="coerce",
            )
            .dt.strftime("%Y-%m-%d")
        )

    return df


# ==========================================================
# Add Pipeline Metadata
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

    df["ingested_at"] = current_datetime().strftime(
        "%Y-%m-%d"
    )

    return df


# ==========================================================
# Save Silver Dataset
# ==========================================================

def save_dataframe(
    df: pd.DataFrame,
):
    """
    Save transformed dataset to Parquet.
    """

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
    """
    Execute the transformation pipeline.
    """

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