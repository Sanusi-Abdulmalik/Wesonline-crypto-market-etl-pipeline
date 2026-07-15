import json
from pathlib import Path

import pandas as pd

from scripts.logger import logger


def read_json(file_path: Path) -> dict:
    """
    Read a JSON file.
    """

    logger.info(f"Reading JSON file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_parquet(dataframe, output_path):
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_parquet(
        output_path,
        engine="pyarrow",
        index=False,
    )

    stats = {
        "path": str(output_path),
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "size_mb": round(
            output_path.stat().st_size / (1024 * 1024),
            2,
        ),
    }

    logger.info(
        f"Parquet saved: {stats}"
    )

    return stats