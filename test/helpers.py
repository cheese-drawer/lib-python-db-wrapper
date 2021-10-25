"""Test helpers."""

import asyncio
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterable,
)
from unittest.mock import MagicMock


def composed_to_string(seq: Iterable[Any]) -> str:
    """Test helper to convert a sql query to a string for comparison.

    Works for queries built with postgres.sql.Composable objects.
    From https://github.com/psycopg/psycopg2/issues/747#issuecomment-662857306
    """
    parts = str(seq).split("'")
    return "".join([p for i, p in enumerate(parts) if i % 2 == 1])


class AsyncMock(MagicMock):
    """Extend unittest.mock.MagicMock to allow mocking of async functions."""

    # pylint: disable=invalid-overridden-method
    # pylint: disable=useless-super-delegation

    async def __call__(self, *args, **kwargs):  # type: ignore
        return super().__call__(*args, **kwargs)


def async_test(
    test: Callable[[Any], Awaitable[None]]
) -> Callable[[Any], None]:
    """Decorate an async test method to run it in a one-off event loop."""
    def wrapped(instance: Any) -> None:
        asyncio.run(test(instance))

    return wrapped
