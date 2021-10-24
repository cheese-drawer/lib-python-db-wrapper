from typing import Union

from .async_client import AsyncClient
from .sync_client import SyncClient

Client = Union[AsyncClient, SyncClient]
