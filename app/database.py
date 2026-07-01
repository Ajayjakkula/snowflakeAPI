import snowflake.connector
from app.config import settings


def get_connection():
    """
    Creates and returns a Snowflake connection.

    Returns:
        snowflake.connector.connection: Active Snowflake connection
    """

    connection = snowflake.connector.connect(
        account=settings.SNOWFLAKE_ACCOUNT,
        user=settings.SNOWFLAKE_USER,
        password=settings.SNOWFLAKE_PASSWORD,
        warehouse=settings.SNOWFLAKE_WAREHOUSE,
        database=settings.SNOWFLAKE_DATABASE,
        schema=settings.SNOWFLAKE_SCHEMA
    )

    return connection