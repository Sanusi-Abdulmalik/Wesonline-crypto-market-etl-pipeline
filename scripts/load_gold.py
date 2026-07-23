"""
Build the Gold layer in Snowflake.
"""

from datetime import datetime

from config.config import (
    EXECUTED_BY,
    GOLD_SQL_FILE,
    STAGE_GOLD,
)

from scripts.audit import log_audit
from scripts.logger import logger
from scripts.snowflake_utils import execute_sql_file, get_connection


def load_gold():
    """
    Execute the Gold SQL script.
    """

    logger.info("=" * 60)
    logger.info("Building Gold Layer")
    logger.info("=" * 60)

    start_time = datetime.utcnow()
    connection = get_connection()
    cursor = connection.cursor()

    try:
        execute_sql_file(cursor, GOLD_SQL_FILE)
        connection.commit()

        end_time = datetime.utcnow()
        result = {
            "status": "SUCCESS",
            "started_at": start_time,
            "completed_at": end_time,
            "duration": (end_time - start_time).total_seconds(),
            "files_executed": 1,
        }

        log_audit(
            stage=STAGE_GOLD,
            batch_id="manual",
            run_id="manual",
            executed_by=EXECUTED_BY,
            result=result,
        )

        logger.info("=" * 60)
        logger.info("Gold layer refreshed successfully.")
        logger.info("=" * 60)

    except Exception as e:
        connection.rollback()
        end_time = datetime.utcnow()

        result = {
            "status": "FAILED",
            "started_at": start_time,
            "completed_at": end_time,
            "duration": (end_time - start_time).total_seconds(),
            "files_executed": 0,
            "error": str(e),
        }

        log_audit(
            stage=STAGE_GOLD,
            batch_id="manual",
            run_id="manual",
            executed_by=EXECUTED_BY,
            result=result,
        )

        logger.exception("Gold layer failed.")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_gold()