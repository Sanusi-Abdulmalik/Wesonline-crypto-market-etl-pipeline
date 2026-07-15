import json
import time

import requests

from config.config import (
    RAW_DATA_DIR,
    COINGECKO_API,
    VS_CURRENCY,
    PER_PAGE,
    PAGE,
    PIPELINE_NAME,
    PIPELINE_VERSION,
    ENVIRONMENT,
)

from scripts.logger import logger
from scripts.utils import (
    timestamp,
    current_datetime,
    create_partition_path,
    generate_batch_id,
)

def fetch_market_data():
    """
    Fetch live cryptocurrency market data from CoinGecko.
    """

    endpoint = f"{COINGECKO_API}/coins/markets"

    params = {
        "vs_currency": VS_CURRENCY,
        "order": "market_cap_desc",
        "per_page": PER_PAGE,
        "page": PAGE,
        "sparkline": "false",
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "fintech-etl-pipeline/1.0",
    }

    logger.info("Fetching market data from CoinGecko API...")

    start_time = time.perf_counter()

    try:
        response = requests.get(
            endpoint,
            params=params,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:
        logger.exception(f"Failed to fetch market data: {error}")
        raise

    response_time = round(time.perf_counter() - start_time, 2)

    logger.info(
        f"Successfully fetched {len(data)} records "
        f"in {response_time} seconds."
    )

    return data, response_time


def save_raw_data(
    data,
    response_time,
    batch_id,
):
    """
    Save raw API response together with extraction metadata.
    """

    partition_path = create_partition_path(RAW_DATA_DIR)

    filename = partition_path / f"crypto_market_{timestamp()}.json"

    payload = {
        "metadata": {
            "batch_id": batch_id,
            "pipeline": PIPELINE_NAME,
            "version": PIPELINE_VERSION,
            "environment": ENVIRONMENT,
            "source": "CoinGecko API",
            "endpoint": "/coins/markets",
            "extracted_at": current_datetime().isoformat(),
            "currency": VS_CURRENCY,
            "page": PAGE,
            "records": len(data),
            "api_response_time_seconds": response_time,
            "status": "SUCCESS",
        },
        "data": data,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4)

    logger.info(f"Raw data saved to {filename}")

    return {
        "batch_id": batch_id,
        "file_path": str(filename),
        "record_count": len(data),
        "response_time": response_time,
    }


def extract():
    """
    Execute the extraction pipeline.
    """

    logger.info("Starting extraction pipeline...")

    batch_id = generate_batch_id()

    data, response_time = fetch_market_data()

    result = save_raw_data(
        data=data,
        response_time=response_time,
        batch_id=batch_id,
    )

    logger.info("Extraction pipeline completed successfully.")

    return result


if __name__ == "__main__":
    extract()