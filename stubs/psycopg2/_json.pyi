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
# pylint: disable=too-many-arguments
# pylint: disable=no-self-use
# pylint: disable=redefined-builtin
# pylint: disable=super-init-not-called

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


def register_json(
    conn_or_curs: Optional[Any] = ...,
    globally: bool = ...,
    loads: Optional[Any] = ...,
    oid: Optional[Any] = ...,
    array_oid: Optional[Any] = ...,
    name: str = ...
) -> Any: ...


def register_default_json(
    conn_or_curs: Optional[Any] = ...,
    globally: bool = ...,
    loads: Optional[Any] = ...) -> Any: ...


def register_default_jsonb(
    conn_or_curs: Optional[Any] = ...,
    globally: bool = ...,
    loads: Optional[Any] = ...) -> Any: ...
