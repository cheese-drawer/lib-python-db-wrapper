"""Tests for db_wrapper.model.

These tests are limited by mocking of Client's ability to query Postgres. This
means that actual SQL queries aren't being tested, just the processing of any
results received & the act of making a request.
"""
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods

from typing import (
    cast,
    Any,
    List,
    Tuple,
    TypeVar,
)
from uuid import uuid4
import unittest
from unittest import TestCase

import helpers

from db_wrapper import ConnectionParameters, AsyncClient, SyncClient
from db_wrapper.model import (
    ModelData,
    AsyncModel,
    AsyncRead,
    SyncModel,
    SyncRead
)
from db_wrapper.model.base import (
    UnexpectedMultipleResults,
    NoResultFound,
)


# Generic doesn't need a more descriptive name
# pylint: disable=invalid-name
T = TypeVar('T', bound=ModelData)


def setupAsync(query_result: List[T]) -> Tuple[AsyncModel[T], AsyncClient]:
    """Setup helper that returns instances of both a Model & a Client.

    Mocks the execute_and_return method on the Client instance to skip
    normal execution & just return the given query_result.

    Using this setup helper that requires manually calling in each test
    instance is better than unittest's setUpModule or setUpClass methods
    because it allows the caller to skip all the boilerplate contained
    here, but still specify a return value for the mocked method on the
    returned Client instance.
    """
    # create client with placeholder connection data
    conn_params = ConnectionParameters('a', 1, 'a', 'a', 'a')
    client = AsyncClient(conn_params)

    # mock client's sql execution method
    client.execute_and_return = helpers.AsyncMock(  # type:ignore
        return_value=query_result)

    # init a real model with mocked client
    model = AsyncModel[Any](client, 'test')

    return model, client


def setupSync(query_result: List[T]) -> Tuple[SyncModel[T], SyncClient]:
    """Setup helper that returns instances of both a Model & a Client.

    Mocks the execute_and_return method on the Client instance to skip
    normal execution & just return the given query_result.

    Using this setup helper that requires manually calling in each test
    instance is better than unittest's setUpModule or setUpClass methods
    because it allows the caller to skip all the boilerplate contained
    here, but still specify a return value for the mocked method on the
    returned Client instance.
    """
    # create client with placeholder connection data
    conn_params = ConnectionParameters('a', 1, 'a', 'a', 'a')
    client = SyncClient(conn_params)

    # mock client's sql execution method
    client.execute_and_return = helpers.MagicMock(  # type:ignore
        return_value=query_result)

    # init a real model with mocked client
    model = SyncModel[Any](client, 'test')

    return model, client


class TestReadOneById(TestCase):
    """Testing Model.read.one_by_id."""

    @helpers.async_test
    async def test_it_correctly_builds_query_with_given_id(self) -> None:
        item = ModelData(id=uuid4())
        async_model, async_client = setupAsync([item])
        sync_model, sync_client = setupSync([item])

        await async_model.read.one_by_id(str(item.id))
        sync_model.read.one_by_id(str(item.id))

        async_query_composed = cast(
            helpers.AsyncMock, async_client.execute_and_return).call_args[0][0]
        sync_query_composed = cast(
            helpers.AsyncMock, sync_client.execute_and_return).call_args[0][0]

        async_query = helpers.composed_to_string(async_query_composed)
        sync_query = helpers.composed_to_string(sync_query_composed)

        queries = [async_query, sync_query]

        for query in queries:
            with self.subTest():
                self.assertEqual(query, "SELECT * "
                                 "FROM test "
                                 f"WHERE id = {item.id};")

    @helpers.async_test
    async def test_it_returns_a_single_result(self) -> None:
        item = ModelData(id=uuid4())
        async_model, _ = setupAsync([item])
        sync_model, _ = setupSync([item])
        results = [await async_model.read.one_by_id(str(item.id)),
                   sync_model.read.one_by_id(str(item.id))]

        for result in results:
            with self.subTest():
                self.assertEqual(result, item)

    @helpers.async_test
    async def test_it_raises_exception_if_more_than_one_result(self) -> None:
        item = ModelData(id=uuid4())
        async_model, _ = setupAsync([item, item])
        sync_model, _ = setupSync([item, item])

        with self.subTest():
            with self.assertRaises(UnexpectedMultipleResults):
                await async_model.read.one_by_id(str(item.id))

        with self.subTest():
            with self.assertRaises(UnexpectedMultipleResults):
                sync_model.read.one_by_id(str(item.id))

    @ helpers.async_test
    async def test_it_raises_exception_if_no_result_to_return(self) -> None:
        async_model: AsyncModel[ModelData]
        sync_model: SyncModel[ModelData]
        async_model, _ = setupAsync([])
        sync_model, _ = setupSync([])

        with self.subTest():
            with self.assertRaises(NoResultFound):
                await async_model.read.one_by_id('id')

        with self.subTest():
            with self.assertRaises(NoResultFound):
                sync_model.read.one_by_id('id')


class TestCreateOne(TestCase):
    """Testing Model.create.one."""

    class Item(ModelData):
        """Example ModelData dataclass instance to define shape of data."""
        a: str
        b: str

    @ helpers.async_test
    async def test_it_correctly_builds_query_with_given_data(self) -> None:
        item = TestCreateOne.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        async_model, async_client = setupAsync([item])
        sync_model, sync_client = setupSync([item])

        await async_model.create.one(item)
        sync_model.create.one(item)

        async_query_composed = cast(
            helpers.AsyncMock, async_client.execute_and_return).call_args[0][0]
        sync_query_composed = cast(
            helpers.MagicMock, sync_client.execute_and_return).call_args[0][0]

        queries = [async_query_composed, sync_query_composed]

        for query in queries:
            with self.subTest():
                self.assertEqual(
                    helpers.composed_to_string(query),
                    'INSERT INTO test (id,a,b) '
                    f"VALUES ({item.id},a,b) "
                    'RETURNING *;')

    @ helpers.async_test
    async def test_it_returns_the_new_record(self) -> None:
        item = TestCreateOne.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        async_model, _ = setupAsync([item])
        sync_model, _ = setupSync([item])

        results = [await async_model.create.one(item),
                   sync_model.create.one(item)]

        for result in results:
            with self.subTest():
                self.assertEqual(result, item)


class TestUpdateOne(TestCase):
    """Testing Model.update.one_by_id."""

    class Item(ModelData):
        """Example ModelData Item for testing."""
        a: str
        b: str

    @ helpers.async_test
    async def test_it_correctly_builds_query_with_given_data(self) -> None:
        item = TestUpdateOne.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        async_model, async_client = setupAsync([item])
        sync_model, sync_client = setupSync([item])

        await async_model.update.one_by_id(str(item.id), {'b': 'c'})
        sync_model.update.one_by_id(str(item.id), {'b': 'c'})

        async_query_composed = cast(
            helpers.AsyncMock, async_client.execute_and_return).call_args[0][0]
        sync_query_composed = cast(
            helpers.AsyncMock, sync_client.execute_and_return).call_args[0][0]

        queries = [async_query_composed, sync_query_composed]

        for query in queries:
            with self.subTest():
                self.assertEqual(
                    helpers.composed_to_string(query),
                    'UPDATE test '
                    'SET b = c '
                    f"WHERE id = {item.id} "
                    'RETURNING *;')

    @ helpers.async_test
    async def test_it_returns_the_new_record(self) -> None:
        item = TestUpdateOne.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        # mock result
        updated = TestUpdateOne.Item(**{**item.dict(), 'b': 'c'})
        async_model, _ = setupAsync([updated])
        sync_model, _ = setupSync([updated])

        results = [
            await async_model.update.one_by_id(str(item.id), {'b': 'c'}),
            sync_model.update.one_by_id(str(item.id), {'b': 'c'})
        ]

        for result in results:
            with self.subTest():
                self.assertEqual(result, updated)


class TestDeleteOneById(TestCase):
    """Testing Model.delete.one_byid"""

    class Item(ModelData):
        """Example ModelData Item for testing."""
        a: str
        b: str

    @ helpers.async_test
    async def test_it_correctly_builds_query_with_given_data(self) -> None:
        item = TestDeleteOneById.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        async_model, async_client = setupAsync([item])
        sync_model, sync_client = setupSync([item])

        await async_model.delete.one_by_id(str(item.id))
        sync_model.delete.one_by_id(str(item.id))

        async_query_composed = cast(
            helpers.AsyncMock, async_client.execute_and_return).call_args[0][0]
        sync_query_composed = cast(
            helpers.AsyncMock, sync_client.execute_and_return).call_args[0][0]

        queries = [async_query_composed, sync_query_composed]

        for query in queries:
            with self.subTest():
                self.assertEqual(
                    helpers.composed_to_string(query),
                    'DELETE FROM test '
                    f"WHERE id = {item.id} "
                    'RETURNING *;')

    @ helpers.async_test
    async def test_it_returns_the_deleted_record(self) -> None:
        item = TestDeleteOneById.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        async_model, _ = setupAsync([item])
        sync_model, _ = setupSync([item])

        results = [await async_model.delete.one_by_id(str(item.id)),
                   sync_model.delete.one_by_id(str(item.id))]

        for result in results:
            with self.subTest():
                self.assertEqual(result, item)


class TestExtendingModel(TestCase):
    """Testing Model's extensibility."""

    models: List[Any]

    def setUp(self) -> None:
        class Item(ModelData):
            """An example model data object."""

        class AsyncReadExtended(AsyncRead[Item]):
            """Extending Read with additional query."""

            def new_query(self) -> None:
                pass

        class AsyncExtendedModel(AsyncModel[Item]):
            """A model with extended read queries."""
            read: AsyncReadExtended

            def __init__(self, client: AsyncClient) -> None:
                super().__init__(client, 'extended_model')
                self.read = AsyncReadExtended(self.client, self.table)

        class SyncReadExtended(SyncRead[Item]):
            """Extending Read with additional query."""

            def new_query(self) -> None:
                pass

        class SyncExtendedModel(SyncModel[Item]):
            """A model with extended read queries."""
            read: SyncReadExtended

            def __init__(self, client: SyncClient) -> None:
                super().__init__(client, 'extended_model')
                self.read = SyncReadExtended(self.client, self.table)

        _, async_client = setupAsync([Item(**{"id": uuid4()})])
        _, sync_client = setupSync([Item(**{"id": uuid4()})])
        self.models = [AsyncExtendedModel(async_client),
                       SyncExtendedModel(sync_client)]

    def test_it_can_add_new_queries_by_replacing_a_crud_property(self) -> None:
        new_methods = [getattr(model.read, "new_query", None)
                       for model in self.models]

        for method in new_methods:
            with self.subTest():
                self.assertIsNotNone(method)
            with self.subTest():
                self.assertTrue(callable(method))

    def test_it_still_has_original_queries_after_extending(self) -> None:
        old_methods = [getattr(model.read, "one_by_id", None)
                       for model in self.models]

        for method in old_methods:
            with self.subTest():
                self.assertIsNotNone(method)
            with self.subTest():
                self.assertTrue(callable(method))


if __name__ == '__main__':
    unittest.main()
