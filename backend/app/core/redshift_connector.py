import asyncpg
from typing import Any, Dict, Optional
from .connection_manager import BaseDBConnector

class RedshiftConnector(BaseDBConnector):
    def __init__(self, connection_params: Dict[str, Any]):
        super().__init__(connection_params)
        self._conn: Optional[asyncpg.Connection] = None

    async def connect(self):
        self._conn = await asyncpg.connect(**self.connection_params)

    async def disconnect(self):
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        if not self._conn:
            raise RuntimeError("Not connected to the database.")
        if params:
            return await self._conn.fetch(query, *params.values())
        return await self._conn.fetch(query)

    async def check_health(self) -> bool:
        try:
            if not self._conn:
                await self.connect()
            result = await self._conn.fetchval("SELECT 1")
            return result == 1
        except Exception:
            return False
