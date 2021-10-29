"""Base classes for building Async/SyncModel."""

# std lib dependencies
from __future__ import annotations
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Tuple,
    Type,
    TypeVar,
)
from uuid import UUID

# third party dependencies
from psycopg2 import sql
# pylint is unable to parse c module to check contents
from pydantic import BaseModel  # pylint: disable=no-name-in-module

# internal dependency
from db_wrapper.client import (
    Client,
)


class ModelData(BaseModel):
    """Base interface for ModelData to be used in Model."""

    # PENDS python 3.9 support in pylint
    # pylint: disable=inherit-non-class
    # pylint: disable=too-few-public-methods

    id: UUID


# Generic doesn't need a more descriptive name
T = TypeVar('T', bound=ModelData)  # pylint: disable=invalid-name


class UnexpectedMultipleResults(Exception):
    """Raised when query receives multiple results when only one expected."""

    def __init__(self, results: List[Any]) -> None:
        message = 'Multiple results received when only ' \
                  f'one was expected: {results}'
        super().__init__(self, message)


class NoResultFound(Exception):
    """Raised when query receives no results when 1+ results expected."""

    def __init__(self) -> None:
        message = 'No result was found'
        super().__init__(self, message)


def ensure_exactly_one(result: List[Any]) -> None:
    """Raise appropriate Exceptions if list longer than 1."""
    if len(result) > 1:
        raise UnexpectedMultipleResults(result)
    if len(result) == 0:
        raise NoResultFound()


class CRUDABC(Generic[T]):
    """Encapsulate object creation behavior for all CRUD objects."""

    # pylint: disable=too-few-public-methods

    _table: sql.Composable
    _return_constructor: Type[T]

    def __init__(
        self,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        self._table = table
        self._return_constructor = return_constructor


class CreateABC(CRUDABC[T]):
    """Encapsulate Create operations for Model.create."""

    # pylint: disable=too-few-public-methods

    def _query_one(self, item: T) -> sql.Composed:
        """Build query to create one new record with a given item."""
        columns: List[sql.Identifier] = []
        values: List[sql.Literal] = []

        for column, value in item.dict().items():
            values.append(sql.Literal(value))

            columns.append(sql.Identifier(column))

        query = sql.SQL(
            'INSERT INTO {table} ({columns}) '
            'VALUES ({values}) '
            'RETURNING *;'
        ).format(
            table=self._table,
            columns=sql.SQL(',').join(columns),
            values=sql.SQL(',').join(values),
        )

        return query


class ReadABC(CRUDABC[T]):
    """Encapsulate Read operations for Model.read."""

    # pylint: disable=too-few-public-methods

    def _query_one_by_id(self, id_value: UUID) -> sql.Composed:
        """Build query to read a row by it's id."""
        query = sql.SQL(
            'SELECT * '
            'FROM {table} '
            'WHERE id = {id_value};'
        ).format(
            table=self._table,
            id_value=sql.Literal(str(id_value))
        )

        return query


class UpdateABC(CRUDABC[T]):
    """Encapsulate Update operations for Model.read."""

    # pylint: disable=too-few-public-methods

    def _query_one_by_id(
        self,
        id_value: UUID,
        changes: Dict[str, Any]
    ) -> sql.Composed:
        """Build Query to apply changes to row with given id."""
        def compose_one_change(change: Tuple[str, Any]) -> sql.Composed:
            key = change[0]
            value = change[1]

            return sql.SQL("{key} = {value}").format(
                key=sql.Identifier(key), value=sql.Literal(value))

        def compose_changes(changes: Dict[str, Any]) -> sql.Composed:
            return sql.SQL(',').join(
                [compose_one_change(change) for change in changes.items()])

        query = sql.SQL(
            'UPDATE {table} '
            'SET {changes} '
            'WHERE id = {id_value} '
            'RETURNING *;'
        ).format(
            table=self._table,
            changes=compose_changes(changes),
            id_value=sql.Literal(str(id_value)),
        )

        return query


class DeleteABC(CRUDABC[T]):
    """Encapsulate Delete operations for Model.read."""

    # pylint: disable=too-few-public-methods

    def _query_one_by_id(self, id_value: str) -> sql.Composed:
        """Build query to delete one record with matching ID."""
        query = sql.SQL(
            'DELETE FROM {table} '
            'WHERE id = {id_value} '
            'RETURNING *;'
        ).format(
            table=self._table,
            id_value=sql.Literal(id_value)
        )

        return query


class ModelABC(Generic[T]):
    """Class to manage execution of database queries for a model."""

    # pylint: disable=too-few-public-methods

    client: Client
    table: sql.Identifier

    def __init__(
        self,
        client: Client,
        table: str,
    ) -> None:
        self.client = client
        self.table = sql.Identifier(table)
