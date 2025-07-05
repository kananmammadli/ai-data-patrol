import aiomysql
from typing import Any, Dict, Optional
from .connection_manager import BaseDBConnector

class MySQLConnector(BaseDBConnector):
    def __init__(self, connection_params: Dict[str, Any]):
        super().__init__(connection_params)
        self._conn: Optional[aiomysql.Connection] = None
        self._pool: Optional[aiomysql.Pool] = None

    async def connect(self):
        self._pool = await aiomysql.create_pool(**self.connection_params)
        self._conn = await self._pool.acquire()

    async def disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn = None
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None

    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        if not self._conn:
            raise RuntimeError("Not connected to the database.")
        async with self._conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query, tuple(params.values()) if params else ())
            return await cur.fetchall()

    async def check_health(self) -> bool:
        try:
            if not self._conn:
                await self.connect()
            async with self._conn.cursor() as cur:
                await cur.execute("SELECT 1")
                result = await cur.fetchone()
                return result and result[0] == 1
        except Exception:
            return False
