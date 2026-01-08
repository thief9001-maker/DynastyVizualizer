"""Date formatting utilities for canonical and display-oriented date rendering."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MonthStyle(Enum):
    """Supported month rendering styles."""

    NUMERIC = "numeric"
    NUMERIC_PADDED = "numeric_padded"
    FULL_NAME = "full_name"
    ABBREVIATED = "abbreviated"


class DateOrder(Enum):
    """Supported date component ordering."""

    YMD = "YMD"
    DMY = "DMY"
    MDY = "MDY"


@dataclass(frozen=True)
class DateParts:
    """Normalized date components."""

    year: int
    month: Optional[int] = None
    day: Optional[int] = None

    def has_month(self) -> bool:
        """Return True if month component is present."""
        return self.month is not None

    def has_day(self) -> bool:
        """Return True if day component is present."""
        return self.day is not None

    def is_year_only(self) -> bool:
        """Return True if only year component is present."""
        return self.month is None and self.day is None

    def is_year_month(self) -> bool:
        """Return True if year and month are present without day."""
        return self.month is not None and self.day is None


class DateFormatter:
    """Render date components into canonical or display-oriented strings."""

    MONTHS_FULL: dict[int, str] = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December",
    }

    MONTHS_ABBREVIATED: dict[int, str] = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
    }

    MONTH_NAME_TO_INT: dict[str, int] ={
        name: month for month, name in MONTHS_FULL.items()
    }

    UNKNOWN_DATE: str = "?"

    # ------------------------------------------------------------------
    # Canonical formatting (non-configurable)
    # ------------------------------------------------------------------

    @staticmethod
    def format_iso(date: DateParts) -> str:
        """Return canonical ISO-8601 date string (YYYY-MM-DD)."""
        if not (date.has_month() and date.has_day()):
            raise ValueError("ISO format requires year, month, and day.")
        return f"{date.year:04d}-{date.month:02d}-{date.day:02d}"

    # ------------------------------------------------------------------
    # Display formatting (configurable)
    # ------------------------------------------------------------------

    @staticmethod
    def format_display(
        date: DateParts,
        *,
        order: DateOrder = DateOrder.YMD,
        separator: str = "/",
        month_style: MonthStyle = MonthStyle.NUMERIC,
        pad_day: bool = False,
    ) -> str:
        """Return a user-facing formatted date string."""
        if date.year is None:
            return DateFormatter.UNKNOWN_DATE

        components = DateFormatter._build_components(
            date=date,
            month_style=month_style,
            pad_day=pad_day,
        )

        ordered = DateFormatter._order_components(
            date=date,
            components=components,
            order=order,
        )

        return separator.join(ordered)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def month_name_to_int(month: str) -> int | None:
        """Convert full month name to integer value."""
        return DateFormatter.MONTH_NAME_TO_INT.get(month)

    @staticmethod
    def normalize_month(value: int | str | None) -> int | None:
        """Normalize month value to integer representation."""
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            if value.isdigit():
                return int(value)
            return DateFormatter.month_name_to_int(value)
        return None

    @staticmethod
    def _build_components(
        *,
        date: DateParts,
        month_style: MonthStyle,
        pad_day: bool,
    ) -> list[str]:
        """Build rendered date components."""
        parts: dict[str, str] = {"year": str(date.year)}

        if date.has_month():
            parts["month"] = DateFormatter._render_month(
                month=date.month,  # type: ignore[arg-type]
                style=month_style,
            )

        if date.has_day():
            parts["day"] = f"{date.day:02d}" if pad_day else str(date.day)

        return [parts[key] for key in ("year", "month", "day") if key in parts]

    @staticmethod
    def _order_components(
        *,
        date: DateParts,
        components: list[str],
        order: DateOrder,
    ) -> list[str]:
        """Order date components according to defined layout rules."""
        # Partial dates are always year-first
        if date.is_year_only() or date.is_year_month():
            return components

        if order is DateOrder.YMD:
            return components
        if order is DateOrder.DMY:
            return components[::-1]
        if order is DateOrder.MDY:
            year, month, day = components
            return [month, day, year]

        return components

    @staticmethod
    def _render_month(
        *,
        month: int,
        style: MonthStyle,
    ) -> str:
        """Render month according to requested style."""
        if style is MonthStyle.NUMERIC:
            return str(month)
        if style is MonthStyle.NUMERIC_PADDED:
            return f"{month:02d}"
        if style is MonthStyle.FULL_NAME:
            return DateFormatter.MONTHS_FULL.get(month, "")
        if style is MonthStyle.ABBREVIATED:
            return DateFormatter.MONTHS_ABBREVIATED.get(month, "")
        raise ValueError(f"Unsupported MonthStyle: {style}")
