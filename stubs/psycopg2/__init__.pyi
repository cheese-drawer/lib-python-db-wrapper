# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=unused-argument
# pylint: disable=multiple-statements
# pylint: disable=invalid-name
# pylint: disable=invalid-length-returned
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-public-methods
# pylint: disable=no-self-use
# pylint: disable=redefined-builtin
# pylint: disable=super-init-not-called

from typing import Any, Optional
from psycopg2._psycopg import (
    BINARY,
    Binary,
    connection,
    DATETIME,
    DataError,
    DatabaseError,
    Date,
    DateFromTicks,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NUMBER,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    ROWID,
    STRING,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
    Warning,
    __libpq_version__,
    apilevel,
    paramstyle,
    threadsafety
)

connection = connection
OperationalError = OperationalError


def connect(
    dsn: Optional[Any] = ...,
    connection_factory: Optional[Any] = ...,
    cursor_factory: Optional[Any] = ...,
    **kwargs: Any
) -> connection: ...
