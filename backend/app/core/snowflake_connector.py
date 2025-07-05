import snowflake.connector
from typing import Any, Dict, Optional
from .connection_manager import BaseDBConnector
import asyncio

class SnowflakeConnector(BaseDBConnector):
    def __init__(self, connection_params: Dict[str, Any]):
        super().__init__(connection_params)
        self._conn: Optional[snowflake.connector.SnowflakeConnection] = None

    async def connect(self):
        loop = asyncio.get_event_loop()
        self._conn = await loop.run_in_executor(
            None, lambda: snowflake.connector.connect(**self.connection_params)
        )

    async def disconnect(self):
        if self._conn:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._conn.close)
            self._conn = None

    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        if not self._conn:
            raise RuntimeError("Not connected to the database.")
        loop = asyncio.get_event_loop()
        def run_query():
            with self._conn.cursor(snowflake.connector.DictCursor) as cur:
                cur.execute(query, params or {})
                return cur.fetchall()
        return await loop.run_in_executor(None, run_query)
