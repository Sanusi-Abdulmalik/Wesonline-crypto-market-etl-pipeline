"""
Reusable Snowflake helper functions.
"""

from datetime import datetime
from pathlib import Path

import snowflake.connector

from config.config import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_ROLE,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_USER,
    SNOWFLAKE_WAREHOUSE,
)

from scripts.logger import logger


def get_connection():
    """
    Create a Snowflake connection.
    """

    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        role=SNOWFLAKE_ROLE,
    )


def execute_sql_file(cursor, sql_file: Path):
    """
    Execute every SQL statement contained in a SQL file.
    """

    logger.info(f"Executing {sql_file.name}")

    sql = sql_file.read_text(encoding="utf-8")

    # Execute each statement separately
    for statement in filter(
        None,
        (s.strip() for s in sql.split(";"))
    ):

        logger.info(statement.splitlines()[0])

        cursor.execute(statement)


def execute_sql_directory(sql_directory: Path):
    """
    Execute every SQL file inside a directory.
    """

    start_time = datetime.utcnow()

    connection = get_connection()
    cursor = connection.cursor()

    files_executed = 0

    try:

        sql_files = sorted(sql_directory.glob("*.sql"))

        if not sql_files:
            raise FileNotFoundError(
                f"No SQL files found in {sql_directory}"
            )

        logger.info(f"Found {len(sql_files)} SQL files.")

        for index, sql_file in enumerate(sql_files, start=1):

            logger.info(f"[{index}/{len(sql_files)}] {sql_file.name}")

            execute_sql_file(
                cursor,
                sql_file,
            )

            files_executed += 1

        connection.commit()

        end_time = datetime.utcnow()

        logger.info("Snowflake transaction committed.")

        return {
            "status": "SUCCESS",
            "started_at": start_time,
            "completed_at": end_time,
            "duration": (
                end_time - start_time
            ).total_seconds(),
            "files_executed": files_executed,
        }

    except Exception as error:

        connection.rollback()

        end_time = datetime.utcnow()

        logger.exception(error)

        return {
            "status": "FAILED",
            "started_at": start_time,
            "completed_at": end_time,
            "duration": (
                end_time - start_time
            ).total_seconds(),
            "files_executed": files_executed,
            "error": str(error),
        }

    finally:

        cursor.close()
        connection.close()