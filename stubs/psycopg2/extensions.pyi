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

from psycopg2._json import (
    register_default_json,
    register_default_jsonb
)

from psycopg2._psycopg import (
    AsIs,
    BINARYARRAY,
    BOOLEAN,
    BOOLEANARRAY,
    BYTES,
    BYTESARRAY,
    Binary,
    Boolean,
    Column,
    ConnectionInfo,
    DATE,
    DATEARRAY,
    DATETIMEARRAY,
    DECIMAL,
    DECIMALARRAY,
    DateFromPy,
    Diagnostics,
    FLOAT,
    FLOATARRAY,
    Float,
    INTEGER,
    INTEGERARRAY,
    INTERVAL,
    INTERVALARRAY,
    ISQLQuote,
    Int,
    IntervalFromPy,
    LONGINTEGER,
    LONGINTEGERARRAY,
    Notify,
    PYDATE,
    PYDATEARRAY,
    PYDATETIME,
    PYDATETIMEARRAY,
    PYDATETIMETZ,
    PYDATETIMETZARRAY,
    PYINTERVAL,
    PYINTERVALARRAY,
    PYTIME,
    PYTIMEARRAY,
    QueryCanceledError,
    ROWIDARRAY,
    STRINGARRAY,
    TIME,
    TIMEARRAY,
    TimeFromPy,
    TimestampFromPy,
    TransactionRollbackError,
    UNICODE,
    UNICODEARRAY,
    Xid,
    adapt,
    adapters,
    binary_types,
    connection,
    cursor,
    encodings,
    encrypt_password,
    get_wait_callback,
    libpq_version,
    lobject,
)
from psycopg2._range import Range

ISOLATION_LEVEL_AUTOCOMMIT: int
ISOLATION_LEVEL_READ_UNCOMMITTED: int
ISOLATION_LEVEL_READ_COMMITTED: int
ISOLATION_LEVEL_REPEATABLE_READ: int
ISOLATION_LEVEL_SERIALIZABLE: int
ISOLATION_LEVEL_DEFAULT: Any
STATUS_SETUP: int
STATUS_READY: int
STATUS_BEGIN: int
STATUS_SYNC: int
STATUS_ASYNC: int
STATUS_PREPARED: int
STATUS_IN_TRANSACTION = STATUS_BEGIN
POLL_OK: int
POLL_READ: int
POLL_WRITE: int
POLL_ERROR: int
TRANSACTION_STATUS_IDLE: int
TRANSACTION_STATUS_ACTIVE: int
TRANSACTION_STATUS_INTRANS: int
TRANSACTION_STATUS_INERROR: int
TRANSACTION_STATUS_UNKNOWN: int

QuotedString: Any
new_array_type: Any
new_type: Any
parse_dsn: Any
quote_ident: Any
register_type: Any
set_wait_callback: Any
string_types: Any


def register_adapter(typ: Any, callable: Any) -> None: ...


class SQL_IN:
    def __init__(self, seq: Any) -> None: ...
    def prepare(self, conn: Any) -> None: ...
    def getquoted(self) -> Any: ...


class NoneAdapter:
    def __init__(self, obj: Any) -> None: ...
    def getquoted(self, _null: bytes = ...) -> Any: ...


def make_dsn(dsn: Optional[Any] = ..., **kwargs: Any) -> Any: ...


JSON: Any
JSONARRAY: Any
JSONB: Any
JSONBARRAY: Any
k: Any
