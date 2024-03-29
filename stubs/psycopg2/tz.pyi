import datetime
from typing import Any, Optional

ZERO: Any

class FixedOffsetTimezone(datetime.tzinfo):
    def __init__(self, offset: Optional[Any] = ..., name: Optional[Any] = ...) -> None: ...
    def __new__(cls, offset: Optional[Any] = ..., name: Optional[Any] = ...): ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __getinitargs__(self): ...
    def utcoffset(self, dt: Any): ...
    def tzname(self, dt: Any): ...
    def dst(self, dt: Any): ...

STDOFFSET: Any
DSTOFFSET: Any
DSTOFFSET = STDOFFSET
DSTDIFF: Any

class LocalTimezone(datetime.tzinfo):
    def utcoffset(self, dt: Any): ...
    def dst(self, dt: Any): ...
    def tzname(self, dt: Any): ...

LOCAL: Any
