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
    TypeVar,
    List,
    Tuple,
)
from uuid import uuid4
import unittest
from unittest import TestCase

import helpers

from db_wrapper.client import AsyncClient
from db_wrapper.model import (
    ModelData,
    AsyncModel,
    AsyncRead
)
from db_wrapper.model.base import (
    UnexpectedMultipleResults,
    NoResultFound,
)


# Generic doesn't need a more descriptive name
# pylint: disable=invalid-name
T = TypeVar('T', bound=ModelData)


def setup(query_result: List[T]) -> Tuple[AsyncModel[T], AsyncClient]:
    """Setup helper that returns instances of both a Model & a Client.

    Mocks the execute_and_return method on the Client instance to skip
    normal execution & just return the given query_result.

    Using this setup helper that requires manually calling in each test
    instance is better than unittest's setUpModule or setUpClass methods
    because it allows the caller to skip all the boilerplate contained
    here, but still specify a return value for the mocked method on the
    returned Client instance.
    """
    client = helpers.get_client()

    # mock client's sql execution method
    client.execute_and_return = helpers.AsyncMock(  # type:ignore
        return_value=query_result)

    # init model with mocked client
    model = AsyncModel[Any](client, 'test')

    return model, client


class TestReadOneById(TestCase):
    """Testing Model.read.one_by_id."""

    @helpers.async_test
    async def test_it_correctly_builds_query_with_given_id(self) -> None:
        item = ModelData(id=uuid4())
        model, client = setup([item])
        await model.read.one_by_id(str(item.id))
        query_composed = cast(
            helpers.AsyncMock, client.execute_and_return).call_args[0][0]
        query = helpers.composed_to_string(query_composed)

        self.assertEqual(query, "SELECT * "
                                "FROM test "
                                f"WHERE id = {item.id};")

    @helpers.async_test
    async def test_it_returns_a_single_result(self) -> None:
        item = ModelData(id=uuid4())
        model, _ = setup([item])
        result = await model.read.one_by_id(str(item.id))

        self.assertEqual(result, item)

    @ helpers.async_test
    async def test_it_raises_exception_if_more_than_one_result(self) -> None:
        item = ModelData(id=uuid4())
        model, _ = setup([item, item])

        with self.assertRaises(UnexpectedMultipleResults):
            await model.read.one_by_id(str(item.id))

    @ helpers.async_test
    async def test_it_raises_exception_if_no_result_to_return(self) -> None:
        model: AsyncModel[ModelData]
        model, _ = setup([])

        with self.assertRaises(NoResultFound):
            await model.read.one_by_id('id')


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
        model, client = setup([item])

        await model.create.one(item)
        query_composed = cast(
            helpers.AsyncMock, client.execute_and_return).call_args[0][0]
        query = helpers.composed_to_string(query_composed)

        self.assertEqual(query, 'INSERT INTO test (id,a,b) '
                                f"VALUES ({item.id},a,b) "
                                'RETURNING *;')

    @ helpers.async_test
    async def test_it_returns_the_new_record(self) -> None:
        item = TestCreateOne.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        model, _ = setup([item])

        result = await model.create.one(item)

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
        # cast required to avoid mypy error due to unpacking
        # TypedDict, see more on GitHub issue
        # https://github.com/python/mypy/issues/4122
        updated = TestUpdateOne.Item(**{**item.dict(), 'b': 'c'})
        model, client = setup([updated])

        await model.update.one_by_id(str(item.id), {'b': 'c'})
        query_composed = cast(
            helpers.AsyncMock, client.execute_and_return).call_args[0][0]
        query = helpers.composed_to_string(query_composed)

        self.assertEqual(query, 'UPDATE test '
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
        # cast required to avoid mypy error due to unpacking
        # TypedDict, see more on GitHub issue
        # https://github.com/python/mypy/issues/4122
        updated = TestUpdateOne.Item(**{**item.dict(), 'b': 'c'})
        model, _ = setup([updated])

        result = await model.update.one_by_id(str(item.id), {'b': 'c'})

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
        model, client = setup([item])

        await model.delete.one_by_id(str(item.id))

        query_composed = cast(
            helpers.AsyncMock, client.execute_and_return).call_args[0][0]
        query = helpers.composed_to_string(query_composed)

        self.assertEqual(query, 'DELETE FROM test '
                                f"WHERE id = {item.id} "
                                'RETURNING *;')

    @ helpers.async_test
    async def test_it_returns_the_deleted_record(self) -> None:
        item = TestDeleteOneById.Item(**{
            'id': uuid4(),
            'a': 'a',
            'b': 'b',
        })
        model, _ = setup([item])

        result = await model.delete.one_by_id(str(item.id))

        self.assertEqual(result, item)


class TestExtendingModel(TestCase):
    """Testing Model's extensibility."""
    model: AsyncModel[ModelData]

    def setUp(self) -> None:
        class ReadExtended(AsyncRead[ModelData]):
            """Extending Read with additional query."""

            def new_query(self) -> None:
                pass

        model = AsyncModel[ModelData](helpers.get_client(), 'test')
        model.read = ReadExtended(model.client, model.table)

        self.model = model

    def test_it_can_add_new_queries_by_replacing_a_crud_property(self) -> None:
        new_method = getattr(self.model.read, "new_query", None)

        with self.subTest():
            self.assertIsNotNone(new_method)
        with self.subTest():
            self.assertTrue(callable(new_method))

    def test_it_still_has_original_queries_after_extending(self) -> None:
        old_method = getattr(self.model.read, "one_by_id", None)

        with self.subTest():
            self.assertIsNotNone(old_method)
        with self.subTest():
            self.assertTrue(callable(old_method))


if __name__ == '__main__':
    unittest.main()
