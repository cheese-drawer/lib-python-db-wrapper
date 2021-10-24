from typing import Any, Optional

from psycopg2._psycopg import (
    ISQLQuote,
    QuotedString,
    new_array_type,
    new_type,
    register_type
)

JSON_OID: int
JSONARRAY_OID: int
JSONB_OID: int
JSONBARRAY_OID: int


class Json:
    adapted: Any = ...
    def __init__(self, adapted: Any, dumps: Optional[Any] = ...) -> None: ...
    def __conform__(self, proto: Any) -> Any: ...
    def dumps(self, obj: Any) -> Any: ...
    def prepare(self, conn: Any) -> None: ...
    def getquoted(self) -> Any: ...


def register_json(conn_or_curs: Optional[Any] = ..., globally: bool = ..., loads: Optional[Any]
                  = ..., oid: Optional[Any] = ..., array_oid: Optional[Any] = ..., name: str = ...) -> Any: ...


def register_default_json(
    conn_or_curs: Optional[Any] = ..., globally: bool = ..., loads: Optional[Any] = ...) -> Any: ...


def register_default_jsonb(
    conn_or_curs: Optional[Any] = ..., globally: bool = ..., loads: Optional[Any] = ...) -> Any: ...
