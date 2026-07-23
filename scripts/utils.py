"""
General utility functions for the Crypto Market ETL Pipeline.
"""

from datetime import datetime, timezone
from pathlib import Path
import shutil
import uuid


# ==========================================================
# Date & Time Utilities
# ==========================================================

def current_datetime() -> datetime:
    """
    Return the current UTC datetime.
    """
    return datetime.now(timezone.utc)


def current_timestamp_string() -> str:
    """
    Return UTC timestamp formatted for Snowflake.

    Example:
        2026-07-23 10:30:45
    """
    return current_datetime().strftime("%Y-%m-%d %H:%M:%S")


def format_datetime(series):
    """
    Convert pandas datetime column into Snowflake format.

    Output:
        YYYY-MM-DD HH:MM:SS
    """

    return (
        series.dt.tz_convert("UTC")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )


def timestamp() -> str:
    """
    HHMMSS timestamp.

    Example:
        104530
    """
    return current_datetime().strftime("%H%M%S")


def run_id() -> str:
    """
    Pipeline run identifier.
    """

    return current_datetime().strftime("%Y%m%dT%H%M%SZ")


def generate_batch_id() -> str:
    """
    Generate unique batch identifier.
    """

    return str(uuid.uuid4())


# ==========================================================
# Partition Utilities
# ==========================================================

def create_partition_path(base_directory: Path) -> Path:

    now = current_datetime()

    partition = (
        base_directory
        / f"year={now:%Y}"
        / f"month={now:%m}"
        / f"day={now:%d}"
    )

    partition.mkdir(
        parents=True,
        exist_ok=True,
    )

    return partition


def create_file_path(
    base_directory: Path,
    prefix: str,
    extension: str,
) -> Path:

    partition = create_partition_path(base_directory)

    filename = (
        f"{prefix}_{timestamp()}.{extension}"
    )

    return partition / filename


# ==========================================================
# File Utilities
# ==========================================================

def get_latest_file(
    directory: Path,
    extension: str,
) -> Path:

    files = list(directory.rglob(f"*.{extension}"))

    if not files:
        raise FileNotFoundError(
            f"No .{extension} files found in {directory}"
        )

    return max(
        files,
        key=lambda file: file.stat().st_mtime,
    )


def archive_file(
    file_path: Path,
    archive_directory: Path,
) -> Path:

    archive_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = archive_directory / file_path.name

    shutil.move(
        str(file_path),
        str(destination),
    )

    return destination


# ==========================================================
# Metadata Utilities
# ==========================================================

def build_pipeline_metadata(
    *,
    batch_id: str,
    pipeline_name: str,
    pipeline_version: str,
    environment: str,
) -> dict:

    return {

        "batch_id": batch_id,

        "run_id": run_id(),

        "pipeline_name": pipeline_name,

        "pipeline_version": pipeline_version,

        "environment": environment,

        "ingested_at": current_timestamp_string(),

    }