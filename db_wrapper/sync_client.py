"""Wrapper on aiopg to simplify connecting to & interacting with db."""

from __future__ import annotations
from typing import (
    Any,
    TypeVar,
    Union,
    Optional,
    Hashable,
    List,
    Dict)

from psycopg2.extras import register_uuid
# importing for the sole purpose of re-exporting
# pylint: disable=unused-import
from psycopg2 import sql
from psycopg2._psycopg import cursor

from .connection import (
    sync_connect,
    ConnectionParameters,
)

# add uuid support to psycopg2 & Postgres
register_uuid()


# Generic doesn't need a more descriptive name
# pylint: disable=invalid-name
T = TypeVar('T')

Query = Union[str, sql.Composed]


class Client:
    """Class to manage database connection & expose necessary methods to user.

    Stores connection parameters on init, then exposes methods to
    asynchronously connect & disconnect the database, as well as execute SQL
    queries.
    """

    _connection_params: ConnectionParameters
    _connection: Any

    def __init__(self, connection_params: ConnectionParameters) -> None:
        self._connection_params = connection_params

    def connect(self) -> None:
        """Connect to the database."""
        self._connection = sync_connect(self._connection_params)

    def disconnect(self) -> None:
        """Disconnect from the database."""
        self._connection.close()

    @staticmethod
    def _execute_query(
        cursor: cursor,
        query: Query,
        params: Optional[Dict[Hashable, Any]] = None,
    ) -> None:
        if params:
            cursor.execute(query, params)  # type: ignore
        else:
            cursor.execute(query)

    def execute(
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
        with self._connection.cursor() as cursor:
            self._execute_query(cursor, query, params)

    def execute_and_return(
        self,
        query: Query,
        params: Optional[Dict[Hashable, Any]] = None,
    ) -> List[T]:
        """Execute the given SQL query & return the result.

        Arguments:
            query (Query)   -- the SQL query to execute
            params (dict)  -- a dictionary of parameters to interpolate when
                              executing the query

        Returns:
            List containing all the rows that matched the query.
        """
        with self._connection.cursor() as cursor:
            self._execute_query(cursor, query, params)

            result: List[T] = cursor.fetchall()
            return result
