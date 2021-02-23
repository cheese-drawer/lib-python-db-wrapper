# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use
# pylint: disable=unused-argument
# pylint: disable=multiple-statements
# pylint: disable=super-init-not-called

from __future__ import annotations
from typing import Any, Optional, Union, Hashable, Iterable, List, Tuple


class Composable:
    # pylint: disable=unsubscriptable-object
    def __init__(
        self,
        wrapped: Union[str, List[Union[str, Composable]]]
    ) -> None: ...
    # pylint: disable=unsubscriptable-object
    def as_string(self, context: Any) -> Optional[str]: ...
    def __add__(self, other: Any) -> Composable: ...
    # pylint: disable=invalid-name
    def __mul__(self, n: Any) -> Composable: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...


class Composed(Composable):
    def __init__(self, seq: List[Composable]) -> None: ...
    @property
    def seq(self) -> List[str]: ...
    def as_string(self, context: Any) -> str: ...
    def __iter__(self) -> Iterable[str]: ...
    def __add__(self, other: Any) -> Composed: ...
    def join(self, joiner: Any) -> Composed: ...


class SQL(Composable):
    def __init__(self, string: str) -> None: ...
    @property
    def string(self) -> str: ...
    def as_string(self, context: Any) -> str: ...
    def format(self, *args: Any, **kwargs: Any) -> Composed: ...
    def join(self, seq: Any) -> Composed: ...


class Identifier(Composable):
    # pylint: disable=unsubscriptable-object
    def __init__(
        self,
        *strings: Union[str, Hashable]
    ) -> None: ...
    @property
    def strings(self) -> Tuple[Union[str, Hashable]]: ...
    @property
    # pylint: disable=unsubscriptable-object
    def string(self) -> Optional[str]: ...
    def as_string(self, context: Any) -> str: ...


class Literal(Composable):
    @property
    def wrapped(self) -> List[Composable]: ...
    def as_string(self, context: Any) -> str: ...


class Placeholder(Composable):
    # pylint: disable=unsubscriptable-object
    def __init__(self, name: Optional[str] = ...) -> None: ...
    @property
    def name(self) -> str: ...
    def as_string(self, context: Any) -> str: ...


NULL: Any
DEFAULT: Any
