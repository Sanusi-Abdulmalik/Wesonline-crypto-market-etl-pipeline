"""
Schema registry for the Crypto Market ETL Pipeline.

This module defines the expected structure, data types,
nullability, and descriptions for each dataset.
"""

# ==========================================================
# Crypto Market Dataset Schema
# ==========================================================

CRYPTO_MARKET_SCHEMA = {
    "id": {
        "dtype": "string",
        "nullable": False,
        "description": "Unique cryptocurrency identifier"
    },
    "symbol": {
        "dtype": "string",
        "nullable": False,
        "description": "Trading symbol"
    },
    "name": {
        "dtype": "string",
        "nullable": False,
        "description": "Cryptocurrency name"
    },
    "current_price": {
        "dtype": "float64",
        "nullable": False,
        "description": "Current market price"
    },
    "market_cap": {
        "dtype": "float64",
        "nullable": False,
        "description": "Current market capitalization"
    },
    "market_cap_rank": {
        "dtype": "Int64",
        "nullable": True,
        "description": "Market capitalization rank"
    },
    "fully_diluted_valuation": {
        "dtype": "float64",
        "nullable": True,
        "description": "Fully diluted valuation"
    },
    "total_volume": {
        "dtype": "float64",
        "nullable": False,
        "description": "24-hour trading volume"
    },
    "high_24h": {
        "dtype": "float64",
        "nullable": True,
        "description": "Highest price in 24 hours"
    },
    "low_24h": {
        "dtype": "float64",
        "nullable": True,
        "description": "Lowest price in 24 hours"
    },
    "price_change_24h": {
        "dtype": "float64",
        "nullable": True,
        "description": "Absolute price change in 24 hours"
    },
    "price_change_percentage_24h": {
        "dtype": "float64",
        "nullable": True,
        "description": "Percentage price change in 24 hours"
    },
    "market_cap_change_24h": {
        "dtype": "float64",
        "nullable": True,
        "description": "Market cap change in 24 hours"
    },
    "market_cap_change_percentage_24h": {
        "dtype": "float64",
        "nullable": True,
        "description": "Market cap percentage change in 24 hours"
    },
    "circulating_supply": {
        "dtype": "float64",
        "nullable": True,
        "description": "Circulating supply"
    },
    "total_supply": {
        "dtype": "float64",
        "nullable": True,
        "description": "Total supply"
    },
    "max_supply": {
        "dtype": "float64",
        "nullable": True,
        "description": "Maximum supply"
    },
    "ath": {
        "dtype": "float64",
        "nullable": True,
        "description": "All-time high price"
    },
    "ath_change_percentage": {
        "dtype": "float64",
        "nullable": True,
        "description": "Percentage below ATH"
    },
    "ath_date": {
        "dtype": "datetime64[ns, UTC]",
        "nullable": True,
        "description": "Date of all-time high"
    },
    "atl": {
        "dtype": "float64",
        "nullable": True,
        "description": "All-time low price"
    },
    "atl_change_percentage": {
        "dtype": "float64",
        "nullable": True,
        "description": "Percentage above ATL"
    },
    "atl_date": {
        "dtype": "datetime64[ns, UTC]",
        "nullable": True,
        "description": "Date of all-time low"
    },
    "last_updated": {
        "dtype": "datetime64[ns, UTC]",
        "nullable": False,
        "description": "Last update timestamp"
    },
}

# ==========================================================
# Pipeline Metadata Columns
# ==========================================================

PIPELINE_METADATA_SCHEMA = {
    "batch_id": {
        "dtype": "string",
        "nullable": False,
        "description": "Unique batch identifier"
    },
    "pipeline_name": {
        "dtype": "string",
        "nullable": False,
        "description": "Pipeline name"
    },
    "pipeline_version": {
        "dtype": "string",
        "nullable": False,
        "description": "Pipeline version"
    },
    "environment": {
        "dtype": "string",
        "nullable": False,
        "description": "Execution environment"
    },
    "ingested_at": {
        "dtype": "datetime64[ns, UTC]",
        "nullable": False,
        "description": "Time loaded into Silver"
    }
}

# ==========================================================
# Schema Registry
# ==========================================================

SCHEMAS = {
    "crypto_market": CRYPTO_MARKET_SCHEMA,
}

# ==========================================================
# Helper Functions
# ==========================================================

def get_schema(dataset: str):
    """
    Return the schema dictionary for a dataset.
    """
    if dataset not in SCHEMAS:
        raise ValueError(f"Unknown dataset: {dataset}")

    return SCHEMAS[dataset]


def get_selected_columns(dataset: str):
    """
    Return the ordered list of business columns.
    """
    return list(get_schema(dataset).keys())


def get_dtype_mapping(dataset: str):
    """
    Return only pandas dtypes for astype().
    Datetime columns are excluded because they are
    handled with pd.to_datetime().
    """
    schema = get_schema(dataset)

    mapping = {}

    for column, properties in schema.items():
        dtype = properties["dtype"]

        if not dtype.startswith("datetime"):
            mapping[column] = dtype

    return mapping


def get_datetime_columns(dataset: str):
    """
    Return datetime columns.
    """
    schema = get_schema(dataset)

    return [
        column
        for column, properties in schema.items()
        if properties["dtype"].startswith("datetime")
    ]


def get_required_columns(dataset: str):
    """
    Return all non-nullable columns.
    """
    schema = get_schema(dataset)

    return [
        column
        for column, properties in schema.items()
        if not properties["nullable"]
    ]
