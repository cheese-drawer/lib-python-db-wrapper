"""Synchronous Model objects."""

from typing import Any, Dict, List, Type
from uuid import UUID

from psycopg2.extras import RealDictRow

from db_wrapper.client import SyncClient
from .base import (
    ensure_exactly_one,
    sql,
    T,
    CreateABC,
    DeleteABC,
    ReadABC,
    UpdateABC,
    ModelABC,
)


class SyncCreate(CreateABC[T]):
    """Create methods designed to use a SyncClient."""

    # pylint: disable=too-few-public-methods

    _client: SyncClient

    def __init__(
        self,
        client: SyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    def one(self, item: T) -> T:
        """Create one new record with a given item."""
        query_result: List[RealDictRow] = self._client.execute_and_return(
            self._query_one(item))
        result: T = self._return_constructor(**query_result[0])

        return result


class SyncRead(ReadABC[T]):
    """Create methods designed to use an SyncClient."""

    # pylint: disable=too-few-public-methods

    _client: SyncClient

    def __init__(
        self,
        client: SyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    def one_by_id(self, id_value: UUID) -> T:
        """Read a row by it's id."""
        query_result: List[RealDictRow] = self._client.execute_and_return(
            self._query_one_by_id(id_value))

        # Should only return one item from DB
        ensure_exactly_one(query_result)

        result: T = self._return_constructor(**query_result[0])

        return result


class SyncUpdate(UpdateABC[T]):
    """Create methods designed to use an SyncClient."""

    # pylint: disable=too-few-public-methods

    _client: SyncClient

    def __init__(
        self,
        client: SyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    def one_by_id(self, id_value: UUID, changes: Dict[str, Any]) -> T:
        """Apply changes to row with given id.

        Arguments:
            id_value (string) - the id of the row to update
            changes (dict)    - a dictionary of changes to apply,
                                matches keys to column names & values to values

        Returns:
            full value of row updated
        """
        query_result: List[RealDictRow] = self._client.execute_and_return(
            self._query_one_by_id(id_value, changes))

        ensure_exactly_one(query_result)

        result: T = self._return_constructor(**query_result[0])

        return result


class SyncDelete(DeleteABC[T]):
    """Create methods designed to use an SyncClient."""

    # pylint: disable=too-few-public-methods

    _client: SyncClient

    def __init__(
        self,
        client: SyncClient,
        table: sql.Composable,
        return_constructor: Type[T]
    ) -> None:
        super().__init__(table, return_constructor)
        self._client = client

    def one_by_id(self, id_value: str) -> T:
        """Delete one record with matching ID."""
        query_result: List[RealDictRow] = self._client.execute_and_return(
            self._query_one_by_id(id_value))

        ensure_exactly_one(query_result)

        result: T = self._return_constructor(**query_result[0])

        return result


class SyncModel(ModelABC[T]):
    """Class to manage execution of database queries for a model."""

    # Properties don't need docstrings
    # pylint: disable=missing-function-docstring

    client: SyncClient

    _create: SyncCreate[T]
    _read: SyncRead[T]
    _update: SyncUpdate[T]
    _delete: SyncDelete[T]

    def __init__(
        self,
        client: SyncClient,
        table: str,
        return_constructor: Type[T],
    ) -> None:
        super().__init__(client, table)

        self._create = SyncCreate[T](
            self.client, self.table, return_constructor)
        self._read = SyncRead[T](
            self.client, self.table, return_constructor)
        self._update = SyncUpdate[T](
            self.client, self.table, return_constructor)
        self._delete = SyncDelete[T](
            self.client, self.table, return_constructor)

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
