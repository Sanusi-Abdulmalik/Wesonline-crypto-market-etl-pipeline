"""
Run Data Quality Checks against the Silver layer.
"""

from datetime import datetime

from config.config import (
    EXECUTED_BY,
    QUALITY_SQL_FILE,
    STAGE_QUALITY,
)

from scripts.audit import log_audit
from scripts.logger import logger
from scripts.snowflake_utils import get_connection


def run_quality_checks():
    """
    Execute the data quality SQL script.
    """

    logger.info("=" * 60)
    logger.info("Running Data Quality Checks")
    logger.info("=" * 60)

    start_time = datetime.utcnow()

    connection = get_connection()
    cursor = connection.cursor()

    passed = 0
    failed = 0

    try:

        with open(
            QUALITY_SQL_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            statements = [
                statement.strip()
                for statement in file.read().split(";")
                if statement.strip()
            ]

        for statement in statements:

            cursor.execute(statement)

            result = cursor.fetchone()

            if result is None:
                continue

            check_name = result[0]
            failed_records = result[1]

            if failed_records == 0:

                logger.info(f"✓ {check_name}")
                passed += 1

            else:

                logger.error(
                    f"✗ {check_name} ({failed_records} failed records)"
                )
                failed += 1

        logger.info("=" * 60)
        logger.info("Quality Summary")
        logger.info("=" * 60)
        logger.info(f"Checks Passed : {passed}")
        logger.info(f"Checks Failed : {failed}")

        end_time = datetime.utcnow()

        audit_result = {
            "status": "SUCCESS" if failed == 0 else "FAILED",
            "started_at": start_time,
            "completed_at": end_time,
            "duration": (
                end_time - start_time
            ).total_seconds(),
            "files_executed": len(statements),
            "error": (
                None
                if failed == 0
                else f"{failed} quality check(s) failed."
            ),
        }

        log_audit(
            stage=STAGE_QUALITY,
            batch_id="manual",
            run_id="manual",
            executed_by=EXECUTED_BY,
            result=audit_result,
            rows_processed=passed,
        )

        if failed > 0:
            raise ValueError(
                f"{failed} data quality check(s) failed."
            )

        logger.info("=" * 60)
        logger.info("All data quality checks passed.")
        logger.info("=" * 60)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    run_quality_checks()