import bcrypt

from app.database import get_connection
from app.config import settings
from app.utils import logger
from fastapi import HTTPException


def get_customers():

    conn = None
    cursor = None

    try:

        logger.info("Fetching customers from Snowflake")

        conn = get_connection()

        cursor = conn.cursor()

        query = f"""
        SELECT
            CUSTOMER_ID,
            CUSTOMER_NAME,
            CITY,
            EMAIL
        FROM {settings.SNOWFLAKE_DATABASE}.{settings.SNOWFLAKE_SCHEMA}.CUSTOMER
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [col[0] for col in cursor.description]

        result = [
            dict(zip(columns, row))
            for row in rows
        ]

        logger.info(f"{len(result)} customers fetched successfully")

        return result

    except Exception as e:

        logger.exception("Error while fetching customers")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


def authenticate_user(username: str, password: str):

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = f"""
        SELECT
            USERNAME,
            PASSWORD_HASH,
            ROLE
        FROM {settings.SNOWFLAKE_DATABASE}.{settings.SNOWFLAKE_SCHEMA}.API_USERS
        WHERE USERNAME = %s
        AND STATUS='ACTIVE'
        """

        cursor.execute(query, (username,))

        row = cursor.fetchone()

        if row is None:
            return None

        db_username = row[0]
        db_password_hash = row[1]
        db_role = row[2]

        password_match = bcrypt.checkpw(
            password.encode("utf-8"),
            db_password_hash.encode("utf-8")
        )

        if not password_match:
            return None

        return {
            "username": db_username,
            "role": db_role
        }

    except Exception as e:

        logger.exception("Authentication Failed")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()