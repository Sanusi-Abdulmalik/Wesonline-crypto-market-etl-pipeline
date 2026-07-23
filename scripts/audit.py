"""
Audit logging utilities.
"""

from config.config import PIPELINE_NAME

from scripts.logger import logger
from scripts.snowflake_utils import get_connection


def log_audit(
    *,
    stage,
    batch_id,
    run_id,
    executed_by,
    result,
    rows_processed=None,
):

    sql = """
    INSERT INTO crypto_market.audit.etl_audit(

        pipeline_name,
        stage,
        batch_id,
        run_id,
        status,
        files_executed,
        rows_processed,
        started_at,
        completed_at,
        duration_seconds,
        executed_by,
        error_message

    )

    VALUES (

        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s

    )
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            sql,
            (
                PIPELINE_NAME,
                stage,
                batch_id,
                run_id,
                result["status"],
                result["files_executed"],
                rows_processed,
                result["started_at"],
                result["completed_at"],
                result["duration"],
                executed_by,
                result.get("error"),
            ),
        )

        connection.commit()

        logger.info("Audit record written.")

    finally:

        cursor.close()
        connection.close()