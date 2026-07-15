"""
Data validation utilities for the Crypto Market ETL Pipeline.
"""

import pandas as pd

from scripts.logger import logger
from config.schemas import (
    get_schema,
    get_required_columns,
    get_dtype_mapping,
    PIPELINE_METADATA_SCHEMA,
)


class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass


# ==========================================================
# Validation Functions
# ==========================================================

def validate_dataframe(df: pd.DataFrame, dataset: str):
    """
    Run all validation checks.
    """

    logger.info("Starting dataframe validation...")

    validate_not_empty(df)
    validate_columns(df, dataset)
    validate_required_columns(df, dataset)
    validate_dtypes(df, dataset)
    validate_duplicates(df)

    logger.info("Data validation completed successfully.")

    return True


def validate_not_empty(df: pd.DataFrame):
    """
    Ensure dataframe contains data.
    """

    if df.empty:
        raise DataValidationError("DataFrame is empty.")

    logger.info(f"DataFrame contains {len(df)} records.")


def validate_columns(df: pd.DataFrame, dataset: str):
    """
    Check for missing or unexpected columns.
    """

    expected = (
    set(get_schema(dataset).keys())
    |
    set(PIPELINE_METADATA_SCHEMA.keys()))

    actual = set(df.columns)

    missing = expected - actual
    unexpected = actual - expected

    if missing:
        raise DataValidationError(
            f"Missing columns: {sorted(missing)}"
        )

    if unexpected:
        logger.warning(
            f"Unexpected columns found: {sorted(unexpected)}"
        )

    logger.info("Column validation passed.")


def validate_required_columns(df: pd.DataFrame, dataset: str):
    """
    Ensure required columns contain no null values.
    """

    required = get_required_columns(dataset)

    errors = []

    for column in required:

        if df[column].isna().any():

            null_count = int(df[column].isna().sum())

            errors.append(
                f"{column} ({null_count} null values)"
            )

    if errors:

        raise DataValidationError(
            "Required column validation failed:\n"
            + "\n".join(errors)
        )

    logger.info("Required column validation passed.")


def validate_dtypes(df: pd.DataFrame, dataset: str):
    """
    Verify dataframe dtypes.
    """

    expected = get_dtype_mapping(dataset)

    errors = []

    for column, expected_dtype in expected.items():

        actual_dtype = str(df[column].dtype)

        if actual_dtype != expected_dtype:

            errors.append(
                f"{column}: expected {expected_dtype}, got {actual_dtype}"
            )

    if errors:

        raise DataValidationError(
            "Data type validation failed:\n"
            + "\n".join(errors)
        )

    logger.info("Data type validation passed.")


def validate_duplicates(df: pd.DataFrame):
    """
    Check duplicate rows.
    """

    duplicates = int(df.duplicated().sum())

    if duplicates > 0:

        logger.warning(
            f"Found {duplicates} duplicate rows."
        )

    else:

        logger.info("No duplicate rows found.")


# ==========================================================
# Validation Summary
# ==========================================================

def validation_summary(df: pd.DataFrame):
    """
    Log useful dataset statistics.
    """

    logger.info("-" * 60)
    logger.info(f"Rows: {len(df):,}")
    logger.info(f"Columns: {len(df.columns)}")
    logger.info(
        f"Memory Usage: "
        f"{round(df.memory_usage(deep=True).sum() / 1024, 2)} KB"
    )
    logger.info("-" * 60)