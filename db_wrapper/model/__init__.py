"""Convenience objects to simplify database interactions w/ given interface."""

from .async_model import (
    AsyncModel,
    AsyncCreate,
    AsyncRead,
    AsyncUpdate,
    AsyncDelete
)
from .sync_model import (
    SyncModel,
    SyncCreate,
    SyncRead,
    SyncUpdate,
    SyncDelete
)
from .base import ModelData, sql
