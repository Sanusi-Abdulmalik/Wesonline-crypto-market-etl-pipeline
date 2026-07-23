CREATE OR REPLACE TABLE crypto_market.audit.etl_audit (

    audit_id INTEGER AUTOINCREMENT,

    pipeline_name STRING,

    stage STRING,

    batch_id STRING,

    run_id STRING,

    status STRING,

    files_executed INTEGER,

    rows_processed INTEGER,

    started_at TIMESTAMP_NTZ,

    completed_at TIMESTAMP_NTZ,

    duration_seconds FLOAT,

    executed_by STRING,

    error_message STRING,

    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()

);