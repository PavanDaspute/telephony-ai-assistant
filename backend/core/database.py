"""
Database utility helpers.

These are thin wrappers useful for health-check and connection-testing scripts.
The main DB connection is managed by Django via dj-database-url in settings.py.
"""

import logging
from django.db import connection, OperationalError

logger = logging.getLogger(__name__)


def check_db_connection() -> bool:
    """
    Verify that the database connection is alive.

    Returns True on success, False on failure.
    """
    try:
        connection.ensure_connection()
        logger.info("Database connection OK.")
        return True
    except OperationalError as exc:
        logger.error("Database connection failed: %s", exc)
        return False
