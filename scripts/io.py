"""
Input/Output utilities for the Crypto Market ETL Pipeline.
"""

import json
from pathlib import Path

import pandas as pd

from scripts.logger import logger


# ==========================================================
# JSON
# ==========================================================

def read_json(file_path: Path) -> dict:
    """
    Read a JSON file and return its contents.
    """

    logger.info(f"Reading JSON file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================================
# Parquet
# ==========================================================

def write_parquet(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> dict:
    """
    Write a DataFrame to a Parquet file.

    All timezone-aware datetime columns are converted to
    UTC-naive timestamps before writing.

    This ensures maximum compatibility with Snowflake's
    Parquet reader.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = dataframe.copy()

    logger.info("Preparing DataFrame for Parquet export...")

    # ------------------------------------------------------
    # Convert timezone-aware timestamps to UTC-naive
    # ------------------------------------------------------

    datetime_columns = df.select_dtypes(
        include=["datetimetz"]
    ).columns

    if len(datetime_columns) > 0:

        logger.info(
            f"Normalizing timezone columns: {list(datetime_columns)}"
        )

        for column in datetime_columns:

            df[column] = (
                df[column]
                .dt.tz_convert("UTC")
                .dt.tz_localize(None)
            )

    # ------------------------------------------------------
    # Write Parquet
    # ------------------------------------------------------

    df.to_parquet(
        output_path,
        engine="pyarrow",
        index=False,
        compression="snappy",
    )

    stats = {
        "path": str(output_path),
        "rows": len(df),
        "columns": len(df.columns),
        "size_mb": round(
            output_path.stat().st_size / (1024 * 1024),
            2,
        ),
    }

    logger.info(f"Parquet successfully written: {stats}")

    return stats