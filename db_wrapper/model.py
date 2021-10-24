"""Convenience class to simplify database interactions for given interface."""

# std lib dependencies
from __future__ import annotations
from typing import (
    TypeVar,
    Generic,
    Union,
    Any,
    Tuple,
    List,
    Dict,
)
from uuid import UUID

# third party dependencies
from psycopg2 import sql

from pydantic import BaseModel

# internal dependency
from .client import (
    Client,
    AsyncClient,
    SyncClient,
)


class ModelData(BaseModel):
    """Base interface for ModelData to be used in Model."""

    # PENDS python 3.9 support in pylint
    # pylint: disable=inherit-non-class
    # pylint: disable=too-few-public-methods

    id: UUID


# Generic doesn't need a more descriptive name
# pylint: disable=invalid-name
T = TypeVar('T', bound=ModelData)


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


# pylint: disable=too-few-public-methods
class CreateABC(Generic[T]):
    """Encapsulate Create operations for Model.read."""

    _table: sql.Composable

    def __init__(self, table: sql.Composable) -> None:
        self._table = table

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


class CreateAsync(CreateABC[T]):
    """Create methods designed to use an AsyncClient."""

    _client: AsyncClient

    def __init__(self, client: AsyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    async def one(self, item: T) -> T:
        """Create one new record with a given item."""
        result: List[T] = await self._client.execute_and_return(
            self._query_one(item))

        return result[0]


class SyncCreate(CreateABC[T]):
    """Create methods designed to use a SyncClient."""

    _client: SyncClient

    def __init__(self, client: SyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    def one(self, item: T) -> T:
        """Create one new record with a given item."""
        result: List[T] = self._client.execute_and_return(
            self._query_one(item))

        return result[0]


def _ensure_exactly_one(result: List[T]) -> None:
    if len(result) > 1:
        raise UnexpectedMultipleResults(result)
    if len(result) == 0:
        raise NoResultFound()


class ReadABC(Generic[T]):
    """Encapsulate Read operations for Model.read."""

    _table: sql.Composable

    def __init__(self, table: sql.Composable) -> None:
        self._table = table

    def _query_one_by_id(self, id_value: str) -> sql.Composed:
        """Build query to read a row by it's id."""
        query = sql.SQL(
            'SELECT * '
            'FROM {table} '
            'WHERE id = {id_value};'
        ).format(
            table=self._table,
            id_value=sql.Literal(id_value)
        )

        return query


class ReadAsync(ReadABC[T]):
    """Create methods designed to use an AsyncClient."""

    _client: AsyncClient

    def __init__(self, client: AsyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    async def one_by_id(self, id_value: str) -> T:
        """Read a row by it's id."""
        result: List[T] = await self._client.execute_and_return(
            self._query_one_by_id(id_value))

        # Should only return one item from DB
        _ensure_exactly_one(result)

        return result[0]


class SyncRead(ReadABC[T]):
    """Create methods designed to use an SyncClient."""

    _client: SyncClient

    def __init__(self, client: SyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    def one_by_id(self, id_value: str) -> T:
        """Read a row by it's id."""
        result: List[T] = self._client.execute_and_return(
            self._query_one_by_id(id_value))

        # Should only return one item from DB
        _ensure_exactly_one(result)

        return result[0]


class UpdateABC(Generic[T]):
    """Encapsulate Update operations for Model.read."""

    _table: sql.Composable

    def __init__(self, table: sql.Composable) -> None:
        self._table = table

    def _query_one_by_id(
        self,
        id_value: str,
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
            id_value=sql.Literal(id_value),
        )

        return query


class UpdateAsync(UpdateABC[T]):
    """Create methods designed to use an AsyncClient."""

    _client: AsyncClient

    def __init__(self, client: AsyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    async def one_by_id(self, id_value: str, changes: Dict[str, Any]) -> T:
        """Apply changes to row with given id.

        Arguments:
            id_value (string) - the id of the row to update
            changes (dict)    - a dictionary of changes to apply,
                                matches keys to column names & values to values

        Returns:
            full value of row updated
        """
        result: List[T] = await self._client.execute_and_return(
            self._query_one_by_id(id_value, changes))

        _ensure_exactly_one(result)

        return result[0]


class SyncUpdate(UpdateABC[T]):
    """Create methods designed to use an SyncClient."""

    _client: SyncClient

    def __init__(self, client: SyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    def one_by_id(self, id_value: str, changes: Dict[str, Any]) -> T:
        """Apply changes to row with given id.

        Arguments:
            id_value (string) - the id of the row to update
            changes (dict)    - a dictionary of changes to apply,
                                matches keys to column names & values to values

        Returns:
            full value of row updated
        """
        result: List[T] = self._client.execute_and_return(
            self._query_one_by_id(id_value, changes))

        _ensure_exactly_one(result)

        return result[0]


class DeleteABC(Generic[T]):
    """Encapsulate Delete operations for Model.read."""

    _table: sql.Composable

    def __init__(self, table: sql.Composable) -> None:
        self._table = table

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


class DeleteAsync(DeleteABC[T]):
    """Create methods designed to use an AsyncClient."""

    _client: AsyncClient

    def __init__(self, client: AsyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    async def one_by_id(self, id_value: str) -> T:
        """Delete one record with matching ID."""
        result: List[T] = await self._client.execute_and_return(
            self._query_one_by_id(id_value))

        # Should only return one item from DB
        _ensure_exactly_one(result)

        return result[0]


class SyncDelete(DeleteABC[T]):
    """Create methods designed to use an SyncClient."""

    _client: SyncClient

    def __init__(self, client: SyncClient, table: sql.Composable) -> None:
        super().__init__(table)
        self._client = client

    def one_by_id(self, id_value: str) -> T:
        """Delete one record with matching ID."""
        result: List[T] = self._client.execute_and_return(
            self._query_one_by_id(id_value))

        # Should only return one item from DB
        _ensure_exactly_one(result)

        return result[0]


class ModelABC(Generic[T]):
    """Class to manage execution of database queries for a model."""

    client: Client
    table: sql.Identifier

    def __init__(
        self,
        client: Client,
        table: str,
    ) -> None:
        self.client = client
        self.table = sql.Identifier(table)


class AsyncModel(ModelABC[T]):
    """Class to manage execution of database queries for a model."""

    # Properties don't need docstrings
    # pylint: disable=missing-function-docstring

    client: AsyncClient

    _create: CreateAsync[T]
    _read: ReadAsync[T]
    _update: UpdateAsync[T]
    _delete: DeleteAsync[T]

    # PENDS python 3.9 support in pylint
    # pylint: disable=unsubscriptable-object
    def __init__(
        self,
        client: AsyncClient,
        table: str,
    ) -> None:
        super().__init__(client, table)

        self._create = CreateAsync[T](self.client, self.table)
        self._read = ReadAsync[T](self.client, self.table)
        self._update = UpdateAsync[T](self.client, self.table)
        self._delete = DeleteAsync[T](self.client, self.table)

    @property
    def create(self) -> CreateAsync[T]:
        """Methods for creating new records of the Model."""
        return self._create

    @create.setter
    def create(self, creator: CreateAsync[T]) -> None:
        if isinstance(creator, CreateAsync):
            self._create = creator
        else:
            raise TypeError('Model.create must be an instance of CreateAsync.')

    @property
    def read(self) -> ReadAsync[T]:
        """Methods for reading records of the Model."""
        return self._read

    @read.setter
    def read(self, reader: ReadAsync[T]) -> None:
        if isinstance(reader, ReadAsync):
            self._read = reader
        else:
            raise TypeError('Model.read must be an instance of ReadAsync.')

    @property
    def update(self) -> UpdateAsync[T]:
        """Methods for updating records of the Model."""
        return self._update

    @update.setter
    def update(self, updater: UpdateAsync[T]) -> None:
        if isinstance(updater, UpdateAsync):
            self._update = updater
        else:
            raise TypeError('Model.update must be an instance of UpdateAsync.')

    @property
    def delete(self) -> DeleteAsync[T]:
        """Methods for deleting records of the Model."""
        return self._delete

    @delete.setter
    def delete(self, deleter: DeleteAsync[T]) -> None:
        if isinstance(deleter, DeleteAsync):
            self._delete = deleter
        else:
            raise TypeError('Model.delete must be an instance of DeleteAsync.')


class SyncModel(ModelABC[T]):
    """Class to manage execution of database queries for a model."""

    # Properties don't need docstrings
    # pylint: disable=missing-function-docstring

    client: SyncClient

    _create: SyncCreate[T]
    _read: SyncRead[T]
    _update: SyncUpdate[T]
    _delete: SyncDelete[T]

    # PENDS python 3.9 support in pylint
    # pylint: disable=unsubscriptable-object
    def __init__(
        self,
        client: SyncClient,
        table: str,
    ) -> None:
        super().__init__(client, table)

        self._create = SyncCreate[T](self.client, self.table)
        self._read = SyncRead[T](self.client, self.table)
        self._update = SyncUpdate[T](self.client, self.table)
        self._delete = SyncDelete[T](self.client, self.table)

    @property
    def create(self) -> SyncCreate[T]:
        """Methods for creating new records of the Model."""
        return self._create

    @create.setter
    def create(self, creator: SyncCreate[T]) -> None:
        if isinstance(creator, SyncCreate):
            self._create = creator
        else:
            raise TypeError('Model.create must be an instance of SyncCreate.')

    @property
    def read(self) -> SyncRead[T]:
        """Methods for reading records of the Model."""
        return self._read

    @read.setter
    def read(self, reader: SyncRead[T]) -> None:
        if isinstance(reader, SyncRead):
            self._read = reader
        else:
            raise TypeError('Model.read must be an instance of SyncRead.')

    @property
    def update(self) -> SyncUpdate[T]:
        """Methods for updating records of the Model."""
        return self._update

    @update.setter
    def update(self, updater: SyncUpdate[T]) -> None:
        if isinstance(updater, SyncUpdate):
            self._update = updater
        else:
            raise TypeError('Model.update must be an instance of SyncUpdate.')

    @property
    def delete(self) -> SyncDelete[T]:
        """Methods for deleting records of the Model."""
        return self._delete

    @delete.setter
    def delete(self, deleter: SyncDelete[T]) -> None:
        if isinstance(deleter, SyncDelete):
            self._delete = deleter
        else:
            raise TypeError('Model.delete must be an instance of SyncDelete.')
