"""Create a database Client for managing connections & executing queries."""

from typing import Union

from .async_client import AsyncClient
from .sync_client import SyncClient

Client = Union[AsyncClient, SyncClient]
