"""Asynchronous Model objects."""

from typing import Any, Dict, List, Type
from uuid import UUID

from psycopg2.extras import RealDictRow

from db_wrapper.client import AsyncClient
from .base import (
    ensure_exactly_one,
    sql,
    T,
    CreateABC,
    ReadABC,
    UpdateABC,
    DeleteABC,
    ModelABC,
)


class AsyncCreate(CreateABC[T]):
    """Create methods designed to use an AsyncClient."""

    # pylint: disable=too-few-public-methods

    _client: AsyncClient

    def __init__(
        self,
        client: AsyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    async def one(self, item: T) -> T:
        """Create one new record with a given item."""
        query_result: List[RealDictRow] = \
            await self._client.execute_and_return(self._query_one(item))
        result: T = self._return_constructor(**query_result[0])

        return result


class AsyncRead(ReadABC[T]):
    """Create methods designed to use an AsyncClient."""

    # pylint: disable=too-few-public-methods

    _client: AsyncClient

    def __init__(
        self,
        client: AsyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    async def one_by_id(self, id_value: UUID) -> T:
        """Read a row by it's id."""
        query_result: List[RealDictRow] = \
            await self._client.execute_and_return(
                self._query_one_by_id(id_value))

        # Should only return one item from DB
        ensure_exactly_one(query_result)

        result: T = self._return_constructor(**query_result[0])

        return result


class AsyncUpdate(UpdateABC[T]):
    """Create methods designed to use an AsyncClient."""

    # pylint: disable=too-few-public-methods

    _client: AsyncClient

    def __init__(
        self,
        client: AsyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    async def one_by_id(self, id_value: UUID, changes: Dict[str, Any]) -> T:
        """Apply changes to row with given id.

        Arguments:
            id_value (string) - the id of the row to update
            changes (dict)    - a dictionary of changes to apply,
                                matches keys to column names & values to values

        Returns:
            full value of row updated
        """
        query_result: List[RealDictRow] = \
            await self._client.execute_and_return(
                self._query_one_by_id(id_value, changes))

        ensure_exactly_one(query_result)
        result: T = self._return_constructor(**query_result[0])

        return result


class AsyncDelete(DeleteABC[T]):
    """Create methods designed to use an AsyncClient."""

    # pylint: disable=too-few-public-methods

    _client: AsyncClient

    def __init__(
        self,
        client: AsyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    async def one_by_id(self, id_value: str) -> T:
        """Delete one record with matching ID."""
        query_result: List[RealDictRow] = \
            await self._client.execute_and_return(
                self._query_one_by_id(id_value))

        # Should only return one item from DB
        ensure_exactly_one(query_result)
        result = self._return_constructor(**query_result[0])

        return result


class AsyncModel(ModelABC[T]):
    """Class to manage execution of database queries for a model."""

    # Properties don't need docstrings
    # pylint: disable=missing-function-docstring

    client: AsyncClient

    _create: AsyncCreate[T]
    _read: AsyncRead[T]
    _update: AsyncUpdate[T]
    _delete: AsyncDelete[T]

    def __init__(
        self,
        client: AsyncClient,
        table: str,
        return_constructor: Type[T],
    ) -> None:
        super().__init__(client, table)

        self._create = AsyncCreate[T](
            self.client, self.table, return_constructor)
        self._read = AsyncRead[T](
            self.client, self.table, return_constructor)
        self._update = AsyncUpdate[T](
            self.client, self.table, return_constructor)
        self._delete = AsyncDelete[T](
            self.client, self.table, return_constructor)

    @property
    def create(self) -> AsyncCreate[T]:
        """Methods for creating new records of the Model."""
        return self._create

    @create.setter
    def create(self, creator: AsyncCreate[T]) -> None:
        if isinstance(creator, AsyncCreate):
            self._create = creator
        else:
            raise TypeError('Model.create must be an instance of AsyncCreate.')

    @property
    def read(self) -> AsyncRead[T]:
        """Methods for reading records of the Model."""
        return self._read

    @read.setter
    def read(self, reader: AsyncRead[T]) -> None:
        if isinstance(reader, AsyncRead):
            self._read = reader
        else:
            raise TypeError('Model.read must be an instance of AsyncRead.')

    @property
    def update(self) -> AsyncUpdate[T]:
        """Methods for updating records of the Model."""
        return self._update

    @update.setter
    def update(self, updater: AsyncUpdate[T]) -> None:
        if isinstance(updater, AsyncUpdate):
            self._update = updater
        else:
            raise TypeError('Model.update must be an instance of AsyncUpdate.')

    @property
    def delete(self) -> AsyncDelete[T]:
        """Methods for deleting records of the Model."""
        return self._delete

    @delete.setter
    def delete(self, deleter: AsyncDelete[T]) -> None:
        if isinstance(deleter, AsyncDelete):
            self._delete = deleter
        else:
            raise TypeError('Model.delete must be an instance of AsyncDelete.')
