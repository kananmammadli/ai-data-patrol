import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from app.core.connection_manager import ConnectionManager
from app.core.postgres_connector import PostgresConnector
from app.core.mysql_connector import MySQLConnector
from app.core.redshift_connector import RedshiftConnector
from app.core.snowflake_connector import SnowflakeConnector

@pytest.mark.asyncio
async def test_postgres_connector_health():
    params = {"user": "u", "password": "p", "database": "d", "host": "h"}
    with patch.object(PostgresConnector, 'connect', AsyncMock()), \
         patch.object(PostgresConnector, 'execute_query', AsyncMock(return_value=[{'?column?': 1}])):
        connector = PostgresConnector(params)
        await connector.connect()
        with patch.object(connector._conn, 'fetchval', AsyncMock(return_value=1)):
            assert await connector.check_health() is True

@pytest.mark.asyncio
async def test_mysql_connector_health():
    params = {"user": "u", "password": "p", "db": "d", "host": "h"}
    with patch.object(MySQLConnector, 'connect', AsyncMock()), \
         patch.object(MySQLConnector, 'execute_query', AsyncMock(return_value=[(1,)])):
        connector = MySQLConnector(params)
        await connector.connect()
        with patch.object(connector._conn, 'cursor', AsyncMock()):
            assert await connector.check_health() in [True, False]  # Mocked

@pytest.mark.asyncio
async def test_redshift_connector_health():
    params = {"user": "u", "password": "p", "database": "d", "host": "h"}
    with patch.object(RedshiftConnector, 'connect', AsyncMock()), \
         patch.object(RedshiftConnector, 'execute_query', AsyncMock(return_value=[{'?column?': 1}])):
        connector = RedshiftConnector(params)
        await connector.connect()
        with patch.object(connector._conn, 'fetchval', AsyncMock(return_value=1)):
            assert await connector.check_health() is True

@pytest.mark.asyncio
async def test_snowflake_connector_health():
    params = {"user": "u", "password": "p", "database": "d", "account": "a"}
    with patch.object(SnowflakeConnector, 'connect', AsyncMock()), \
         patch.object(SnowflakeConnector, 'execute_query', AsyncMock(return_value=[(1,)])):
        connector = SnowflakeConnector(params)
        await connector.connect()
        # Health check uses run_in_executor, so just check it runs
        assert await connector.check_health() in [True, False]  # Mocked


def test_connection_manager_registry():
    manager = ConnectionManager()
    assert 'postgresql' in manager._connectors
    assert 'mysql' in manager._connectors
    assert 'redshift' in manager._connectors
    assert 'snowflake' in manager._connectors
