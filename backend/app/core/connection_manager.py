from abc import ABC, abstractmethod
from typing import Any, Dict
from .postgres_connector import PostgresConnector
from .mysql_connector import MySQLConnector

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

class ConnectionManager:
    """Manages multiple database connectors by type and id."""
    def __init__(self):
        self._connectors = {}
        # Register built-in connectors
        self.register_connector('postgresql', PostgresConnector)
        self.register_connector('mysql', MySQLConnector)

    def register_connector(self, db_type: str, connector_cls):
        self._connectors[db_type] = connector_cls

    def get_connector(self, db_type: str, connection_params: Dict[str, Any]) -> BaseDBConnector:
        connector_cls = self._connectors.get(db_type)
        if not connector_cls:
            raise ValueError(f"No connector registered for type: {db_type}")
        return connector_cls(connection_params)
