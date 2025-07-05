from abc import ABC, abstractmethod
from typing import Any, Dict
from .postgres_connector import PostgresConnector
from .mysql_connector import MySQLConnector
from .redshift_connector import RedshiftConnector
from .snowflake_connector import SnowflakeConnector

class BaseDBConnector(ABC):
    """Abstract base class for all database connectors."""
    def __init__(self, connection_params: Dict[str, Any]):
        self.connection_params = connection_params

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """Return True if connection is healthy, else False."""
        pass

class ConnectionManager:
    """Manages multiple database connectors and connection pools by type and id."""
    def __init__(self):
        self._connectors = {}
        self._pools = {}  # {(db_type, conn_id): pool}
        # Register built-in connectors
        self.register_connector('postgresql', PostgresConnector)
        self.register_connector('mysql', MySQLConnector)
        self.register_connector('redshift', RedshiftConnector)
        self.register_connector('snowflake', SnowflakeConnector)

    def register_connector(self, db_type: str, connector_cls):
        self._connectors[db_type] = connector_cls

    def get_connector(self, db_type: str, connection_params: Dict[str, Any], pool_key: str = None) -> BaseDBConnector:
        connector_cls = self._connectors.get(db_type)
        if not connector_cls:
            raise ValueError(f"No connector registered for type: {db_type}")
        # Pool management for supported types
        if db_type in ("postgresql", "mysql") and pool_key:
            pool = self._pools.get((db_type, pool_key))
            if not pool:
                # Create and store pool (sync for now, can be made async if needed)
                # For demonstration, just store params; actual pool creation is in connector
                self._pools[(db_type, pool_key)] = connection_params
            # Pass pool params to connector
            return connector_cls(self._pools[(db_type, pool_key)])
        return connector_cls(connection_params)

    def clear_pools(self):
        self._pools.clear()
