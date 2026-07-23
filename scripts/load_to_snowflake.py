"""
Load the Silver layer into Snowflake.
"""

from config.config import (
    EXECUTED_BY,
    SILVER_SQL_DIR,
    STAGE_SILVER,
)

from scripts.audit import log_audit
from scripts.logger import logger
from scripts.snowflake_utils import execute_sql_directory


def load_to_snowflake():

    logger.info("=" * 60)
    logger.info("Loading Silver Layer")
    logger.info("=" * 60)

    result = execute_sql_directory(
        SILVER_SQL_DIR
    )

    log_audit(
        stage=STAGE_SILVER,
        batch_id="manual",
        run_id="manual",
        executed_by=EXECUTED_BY,
        result=result,
    )

    logger.info("=" * 60)
    logger.info("Silver Layer Loaded Successfully")
    logger.info("=" * 60)


if __name__ == "__main__":
    load_to_snowflake()