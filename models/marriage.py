"""Data model for Marriage relationships."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from utils.date_formatter import DateFormatter, DateParts, MonthStyle


@dataclass
class Marriage:
    """Represents a marriage relationship between two people."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    DEFAULT_MARRIAGE_TYPE: ClassVar[str] = "spouse"

    MARRIAGE_TYPE_SPOUSE: ClassVar[str] = "spouse"
    MARRIAGE_TYPE_PARTNER: ClassVar[str] = "partner"
    MARRIAGE_TYPE_COMMON_LAW: ClassVar[str] = "common-law"

    DISSOLUTION_DEATH: ClassVar[str] = "Death"
    DISSOLUTION_DIVORCE: ClassVar[str] = "Divorce"
    DISSOLUTION_ANNULMENT: ClassVar[str] = "Annulment"

    STATUS_ACTIVE: ClassVar[str] = "Active"
    STATUS_ENDED: ClassVar[str] = "Ended"

    DATE_UNKNOWN: ClassVar[str] = "Unknown"
    DATE_ONGOING: ClassVar[str] = "Ongoing"
    DURATION_UNKNOWN: ClassVar[str] = "Unknown duration"
    DURATION_ONGOING: ClassVar[str] = "Ongoing"
    DURATION_LESS_THAN_MONTH: ClassVar[str] = "Less than 1 month"

    APPROX_DAYS_PER_MONTH: ClassVar[int] = 30
    MONTHS_PER_YEAR: ClassVar[int] = 12
    DEFAULT_MONTH: ClassVar[int] = 1
    DEFAULT_DAY: ClassVar[int] = 1
    
    # Database Identity
    id: int | None = None
    
    # Spouses
    spouse1_id: int | None = None
    spouse2_id: int | None = None
    
    # Marriage Date
    marriage_year: int | None = None
    marriage_month: int | None = None
    marriage_day: int | None = None
    
    # Dissolution Date
    dissolution_year: int | None = None
    dissolution_month: int | None = None
    dissolution_day: int | None = None
    dissolution_reason: str = ""
    
    # Marriage Type
    marriage_type: str = "spouse"
    
    # Notes
    notes: str = ""
    
    # ------------------------------------------------------------------
    # Computed Properties - Status
    # ------------------------------------------------------------------
    
    @property
    def is_active(self) -> bool:
        """Check if the marriage is currently active (not dissolved)."""
        return self.dissolution_year is None
    
    @property
    def status_string(self) -> str:
        """Get marriage status as readable string."""
        if self.is_active:
            return self.STATUS_ACTIVE
        
        if self.dissolution_reason:
            return f"{self.STATUS_ENDED} ({self.dissolution_reason})"
        
        return self.STATUS_ENDED
    
    # ------------------------------------------------------------------
    # Computed Properties - Date Formatting
    # ------------------------------------------------------------------
    
    @property
    def marriage_date_string(self) -> str:
        """Format marriage date as readable string."""
        if self.marriage_year is None:
            return self.DATE_UNKNOWN
        
        date_parts: DateParts = DateParts(
            year=self.marriage_year,
            month=self.marriage_month,
            day=self.marriage_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            month_style=MonthStyle.FULL_NAME,
            separator=" "
        )
    
    @property
    def dissolution_date_string(self) -> str:
        """Format dissolution date as readable string."""
        if self.dissolution_year is None:
            return ""
        
        date_parts: DateParts = DateParts(
            year=self.dissolution_year,
            month=self.dissolution_month,
            day=self.dissolution_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            month_style=MonthStyle.FULL_NAME,
            separator=" "
        )
    
    # ------------------------------------------------------------------
    # Computed Properties - Duration
    # ------------------------------------------------------------------
    
    @property
    def duration_years(self) -> int | None:
        """Calculate marriage duration in years only (for sorting/filtering)."""
        if self.marriage_year is None or self.is_active or self.dissolution_year is None:
            return None
        
        return self.dissolution_year - self.marriage_year
    
    @property
    def duration_string(self) -> str:
        """Calculate marriage duration as readable string with years, months, days."""
        if self.marriage_year is None:
            return self.DURATION_UNKNOWN
        
        if self.is_active or self.dissolution_year is None:
            return self.DURATION_ONGOING
        
        start_year: int = self.marriage_year
        start_month: int = self.marriage_month or self.DEFAULT_MONTH
        start_day: int = self.marriage_day or self.DEFAULT_DAY
        
        end_year: int = self.dissolution_year
        end_month: int = self.dissolution_month or self.DEFAULT_MONTH
        end_day: int = self.dissolution_day or self.DEFAULT_DAY
        
        years: int = end_year - start_year
        months: int = end_month - start_month
        days: int = end_day - start_day
        
        if days < 0:
            months -= 1
            days += self.APPROX_DAYS_PER_MONTH
        
        if months < 0:
            years -= 1
            months += self.MONTHS_PER_YEAR
        
        parts: list[str] = []
        
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        
        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        
        if days > 0 and self.marriage_day and self.dissolution_day:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        
        if not parts:
            return self.DURATION_LESS_THAN_MONTH
        
        return ", ".join(parts)