from typing import Any, Optional

from psycopg2._psycopg import (
    InterfaceError,
    ProgrammingError
)


class Range:
    def __init__(self, lower: Optional[Any] = ..., upper: Optional[Any]
                 = ..., bounds: str = ..., empty: bool = ...) -> None: ...

    @property
    def lower(self) -> Any: ...
    @property
    def upper(self) -> Any: ...
    @property
    def isempty(self) -> Any: ...
    @property
    def lower_inf(self) -> Any: ...
    @property
    def upper_inf(self) -> Any: ...
    @property
    def lower_inc(self) -> Any: ...
    @property
    def upper_inc(self) -> Any: ...
    def __contains__(self, x: Any) -> Any: ...
    def __bool__(self) -> Any: ...
    def __nonzero__(self) -> Any: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...
    def __lt__(self, other: Any) -> Any: ...
    def __le__(self, other: Any) -> Any: ...
    def __gt__(self, other: Any) -> Any: ...
    def __ge__(self, other: Any) -> Any: ...


def register_range(pgrange: Any, pyrange: Any,
                   conn_or_curs: Any, globally: bool = ...) -> Any: ...


class RangeAdapter:
    name: Any = ...
    adapted: Any = ...
    def __init__(self, adapted: Any) -> None: ...
    def __conform__(self, proto: Any) -> Any: ...
    def prepare(self, conn: Any) -> None: ...
    def getquoted(self) -> Any: ...


class RangeCaster:
    subtype_oid: Any = ...
    typecaster: Any = ...
    array_typecaster: Any = ...
    def __init__(self, pgrange: Any, pyrange: Any, oid: Any,
                 subtype_oid: Any, array_oid: Optional[Any] = ...) -> None: ...

    def parse(self, s: Any, cur: Optional[Any] = ...) -> Any: ...


class NumericRange(Range):
    ...


class DateRange(Range):
    ...


class DateTimeRange(Range):
    ...


class DateTimeTZRange(Range):
    ...


class NumberRangeAdapter(RangeAdapter):
    def getquoted(self) -> Any: ...


int4range_caster: Any
int8range_caster: Any
numrange_caster: Any
daterange_caster: Any
tsrange_caster: Any
tstzrange_caster: Any
