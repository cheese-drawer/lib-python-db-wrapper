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
from typing import Any, Optional

connection = connection
OperationalError = OperationalError


def connect(
    dsn: Optional[Any] = ...,
    connection_factory: Optional[Any] = ...,
    cursor_factory: Optional[Any] = ...,
    **kwargs: Any
) -> connection: ...
