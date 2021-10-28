# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=unused-argument
# pylint: disable=multiple-statements
# pylint: disable=invalid-name
# pylint: disable=invalid-length-returned
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-public-methods
# pylint: disable=no-self-use
# pylint: disable=redefined-builtin
# pylint: disable=super-init-not-called
# pylint: disable=unused-import
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long

from typing import Any, Optional

from psycopg2.extensions import (
    QuotedString,
    new_array_type,
    new_type,
    register_adapter,
    register_type,
)

ipaddress: Any


def register_ipaddress(conn_or_curs: Optional[Any] = ...) -> None: ...
def cast_interface(s: Any, cur: Optional[Any] = ...) -> Any: ...
def cast_network(s: Any, cur: Optional[Any] = ...) -> Any: ...
def adapt_ipaddress(obj: Any) -> Any: ...
