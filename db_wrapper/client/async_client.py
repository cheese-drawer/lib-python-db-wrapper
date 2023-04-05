"""Wrapper on aiopg to simplify connecting to & interacting with db."""

from __future__ import annotations
from typing import (
    cast,
    Any,
    TypeVar,
    Union,
    Optional,
    Hashable,
    List,
    Dict)

import aiopg
from psycopg2.extras import register_uuid, RealDictCursor, RealDictRow  # type: ignore
from psycopg2 import sql

from db_wrapper.connection import ConnectionParameters, get_pool

# add uuid support to psycopg2 & Postgres
register_uuid()


Query = Union[str, sql.Composed]


class AsyncClient:
    """Class to manage database connection & expose necessary methods to user.

    Stores connection parameters on init, then exposes methods to
    asynchronously connect & disconnect the database, as well as execute SQL
    queries.
    """

    _connection_params: ConnectionParameters
    _pool: aiopg.Pool

    def __init__(self, connection_params: ConnectionParameters) -> None:
        self._connection_params = connection_params

    async def connect(self) -> None:
        """Create a database connection pool."""
        self._pool = await get_pool(self._connection_params)

    async def disconnect(self) -> None:
        """Close database connection pool."""
        self._pool.close()
        await self._pool.wait_closed()

    # PENDS python 3.9 support in pylint
    # pylint: disable=unsubscriptable-object
    @staticmethod
    async def _execute_query(
        cursor: aiopg.Cursor,
        query: Query,
        params: Optional[Dict[Hashable, Any]] = None,
    ) -> None:
        # aiopg type is incorrect & thinks execute only takes str
        # when in the query is passed through to psycopg2's
        # cursor.execute which does accept sql.Composed objects.
        query = cast(str, query)

        if params:
            await cursor.execute(query, params)
        else:
            await cursor.execute(query)

    # PENDS python 3.9 support in pylint
    # pylint: disable=unsubscriptable-object
    async def execute(
        self,
        query: Query,
        params: Optional[Dict[Hashable, Any]] = None,
    ) -> None:
        """Execute the given SQL query.

        Arguments:
            query (Query)   -- the SQL query to execute
            params (dict)  -- a dictionary of parameters to interpolate when
                              executing the query

        Returns:
            None
        """
        with (await self._pool.cursor(cursor_factory=RealDictCursor) ) as cursor:
            await self._execute_query(cursor, query, params)

    # PENDS python 3.9 support in pylint
    # pylint: disable=unsubscriptable-object
    async def execute_and_return(
        self,
        query: Query,
        params: Optional[Dict[Hashable, Any]] = None,
    ) -> List[RealDictRow]:
        """Execute the given SQL query & return the result.

        Arguments:
            query (Query)   -- the SQL query to execute
            params (dict)  -- a dictionary of parameters to interpolate when
                              executing the query

        Returns:
            List containing all the rows that matched the query.
        """
        with (await self._pool.cursor(cursor_factory=RealDictCursor) ) as cursor:
            await self._execute_query(cursor, query, params)

            result: List[RealDictRow] = await cursor.fetchall()
            return result
