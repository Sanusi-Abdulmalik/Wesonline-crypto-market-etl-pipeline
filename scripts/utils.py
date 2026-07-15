"""
Utility functions for the Crypto Market ETL Pipeline.
"""

from datetime import datetime, timezone
from pathlib import Path
import shutil
import uuid


# ==========================================================
# Date & Time Utilities
# ==========================================================

def current_datetime():
    """
    Return the current UTC datetime.
    """
    return datetime.now(timezone.utc)


def timestamp():
    """
    Return HHMMSS timestamp.

    Example:
        184530
    """
    return current_datetime().strftime("%H%M%S")


def run_id():
    """
    Human-readable pipeline run ID.

    Example:
        20260711T184530Z
    """
    return current_datetime().strftime("%Y%m%dT%H%M%SZ")


def generate_batch_id():
    """
    Generate a unique batch ID for each ETL run.
    """
    return str(uuid.uuid4())


# ==========================================================
# Partition Utilities
# ==========================================================

def create_partition_path(base_directory: Path) -> Path:
    """
    Create a Hive-style partition.

    Example:

    data/raw/

        year=2026/
            month=07/
                day=11/
    """

    now = current_datetime()

    partition_path = (
        base_directory
        / f"year={now:%Y}"
        / f"month={now:%m}"
        / f"day={now:%d}"
    )

    partition_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return partition_path


def create_file_path(
    base_directory: Path,
    prefix: str,
    extension: str,
) -> Path:
    """
    Generate a timestamped file path inside a Hive partition.

    Example:
    data/processed/
        year=2026/
            month=07/
                day=11/
                    crypto_market_184530.parquet
    """

    partition = create_partition_path(base_directory)

    filename = f"{prefix}_{timestamp()}.{extension}"

    return partition / filename


# ==========================================================
# File Discovery
# ==========================================================

def get_latest_file(directory: Path, extension: str) -> Path:
    """
    Return the latest file recursively.

    Example:

    get_latest_file(RAW_DATA_DIR, "json")
    """

    files = list(directory.rglob(f"*.{extension}"))

    if not files:
        raise FileNotFoundError(
            f"No .{extension} files found in {directory}"
        )

    return max(
        files,
        key=lambda file: file.stat().st_mtime,
    )


# ==========================================================
# Archive Utilities
# ==========================================================

def archive_file(file_path: Path, archive_directory: Path) -> Path:
    """
    Move a processed file into the archive directory,
    preserving the filename.
    """

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
):
    """
    Build standard ETL metadata.
    """

    return {
        "batch_id": batch_id,
        "run_id": run_id(),
        "pipeline": pipeline_name,
        "version": pipeline_version,
        "environment": environment,
        "ingested_at": current_datetime().isoformat(),
    }