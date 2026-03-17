from datetime import datetime
from typing import NamedTuple, TypeVar


class DepthRow(NamedTuple):
    timestamp: datetime
    depth: float


class LocRow(NamedTuple):
    timestamp: datetime
    latitude: float
    longitude: float


T = TypeVar("T", DepthRow, LocRow)
