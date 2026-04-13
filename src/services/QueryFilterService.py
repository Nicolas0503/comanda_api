from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Any

from sqlalchemy.sql import Select


def append_equal_filter(filters: list[Any], column: Any, value: Any) -> None:
    if value is not None:
        filters.append(column == value)


def append_ilike_filter(filters: list[Any], column: Any, value: str | None) -> None:
    if value is not None and value.strip():
        filters.append(column.ilike(f"%{value.strip()}%"))


def append_range_filter(
    filters: list[Any],
    column: Any,
    *,
    equal: float | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
) -> None:
    if equal is not None:
        filters.append(column == equal)
        return

    if min_value is not None:
        filters.append(column >= min_value)

    if max_value is not None:
        filters.append(column <= max_value)


def append_datetime_interval_filter(
    filters: list[Any],
    column: Any,
    *,
    start_at: datetime | None = None,
    end_at: datetime | None = None,
) -> None:
    if start_at is not None:
        filters.append(column >= start_at)

    if end_at is not None:
        filters.append(column <= end_at)


def apply_filters(statement: Select[Any], filters: Sequence[Any]) -> Select[Any]:
    if filters:
        return statement.where(*filters)
    return statement


def apply_pagination(statement: Select[Any], *, skip: int, limit: int) -> Select[Any]:
    return statement.offset(skip).limit(limit)
