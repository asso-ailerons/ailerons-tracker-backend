import csv as csv_lib
from datetime import datetime, timedelta
from io import TextIOWrapper

from werkzeug.datastructures import FileStorage

from ailerons_tracker_backend.blueprints.csv.types import DepthRow, LocRow, T


def match_depths(
    loc_row: LocRow, depth_rows: tuple[DepthRow, ...], tolerance=timedelta(minutes=30)
) -> float | None:
    closest = min(
        depth_rows, key=lambda r: abs(r.timestamp - loc_row.timestamp), default=None
    )

    if closest and abs(closest.timestamp - loc_row.timestamp) <= tolerance:
        return closest.depth

    return None


def parse_timestamp(ts: str):
    return datetime.strptime(ts, "%d-%b-%Y %H:%M:%S")


def new_loc_row(row: dict) -> LocRow:
    timestamp = parse_timestamp(row.pop("Date"))
    latitude = float(row.pop("Most Likely Latitude"))
    longitude = float(row.pop("Most Likely Longitude"))

    return LocRow(timestamp=timestamp, latitude=latitude, longitude=longitude)


def new_depth_row(row: dict) -> DepthRow:
    timestamp = parse_timestamp(f"{row.pop('Day')} {row.pop('Time')}")
    depth = float(row.pop("Depth"))

    return DepthRow(timestamp=timestamp, depth=depth)


def sort_by_date(to_sort: list[T]) -> list[T]:
    return sorted(to_sort, key=lambda d: d.timestamp)


def prepare_locs(loc_rows: tuple[dict, ...]) -> tuple[LocRow, ...]:
    return tuple(sort_by_date([new_loc_row(row) for row in loc_rows]))


def prepare_depths(depth_rows: tuple[dict, ...]) -> tuple[DepthRow, ...]:
    return tuple(sort_by_date([new_depth_row(row) for row in depth_rows]))


def open_csv(file: FileStorage, header_pos: int):
    txt = TextIOWrapper(file.stream, encoding="utf-8")
    for _ in range(header_pos):
        next(txt)
    reader = csv_lib.DictReader(txt)

    return tuple(reader)
