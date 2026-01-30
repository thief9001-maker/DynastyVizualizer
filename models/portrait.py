"""Data model for Portrait entities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from utils.date_formatter import DateFormatter, DateParts, MonthStyle


@dataclass
class Portrait:
    """Represents a portrait image for a person."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    DATE_UNKNOWN: ClassVar[str] = "Unknown"
    DATE_PRESENT: ClassVar[str] = "Present"

    DEFAULT_DISPLAY_ORDER: ClassVar[int] = 0
    
    # Database Identity
    id: int | None = None
    
    # Associated Person
    person_id: int | None = None
    
    # Image Path
    image_path: str = ""
    
    # Valid From Date
    valid_from_year: int | None = None
    valid_from_month: int | None = None
    valid_from_day: int | None = None
    
    # Valid To Date
    valid_to_year: int | None = None
    valid_to_month: int | None = None
    valid_to_day: int | None = None
    
    # Display Properties
    is_primary: bool = False
    display_order: int = 0
    
    # ------------------------------------------------------------------
    # Computed Properties - Date Formatting
    # ------------------------------------------------------------------
    
    @property
    def valid_from_date_string(self) -> str:
        """Format valid-from date as readable string."""
        if self.valid_from_year is None:
            return self.DATE_UNKNOWN
        
        date_parts: DateParts = DateParts(
            year=self.valid_from_year,
            month=self.valid_from_month,
            day=self.valid_from_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            month_style=MonthStyle.FULL_NAME,
            separator=" "
        )
    
    @property
    def valid_to_date_string(self) -> str:
        """Format valid-to date as readable string."""
        if self.valid_to_year is None:
            return self.DATE_PRESENT
        
        date_parts: DateParts = DateParts(
            year=self.valid_to_year,
            month=self.valid_to_month,
            day=self.valid_to_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            month_style=MonthStyle.FULL_NAME,
            separator=" "
        )
    
    @property
    def validity_range_string(self) -> str:
        """Get formatted validity range for display."""
        return f"{self.valid_from_date_string} - {self.valid_to_date_string}"
    
    # ------------------------------------------------------------------
    # Validity Checking
    # ------------------------------------------------------------------
    
    def is_valid_for_date(
        self,
        year: int,
        month: int | None = None,
        day: int | None = None
    ) -> bool:
        """Check if portrait is valid for a given date."""
        if not self._is_after_or_equal_to_start(year, month, day):
            return False
        
        if not self._is_before_or_equal_to_end(year, month, day):
            return False
        
        return True
    
    def _is_after_or_equal_to_start(
        self,
        year: int,
        month: int | None,
        day: int | None
    ) -> bool:
        """Check if date is after or equal to valid_from date."""
        if self.valid_from_year is None:
            return True
        
        if year < self.valid_from_year:
            return False
        
        if year > self.valid_from_year:
            return True
        
        if self.valid_from_month is None or month is None:
            return True
        
        if month < self.valid_from_month:
            return False
        
        if month > self.valid_from_month:
            return True
        
        if self.valid_from_day is None or day is None:
            return True
        
        return day >= self.valid_from_day
    
    def _is_before_or_equal_to_end(
        self,
        year: int,
        month: int | None,
        day: int | None
    ) -> bool:
        """Check if date is before or equal to valid_to date."""
        if self.valid_to_year is None:
            return True
        
        if year > self.valid_to_year:
            return False
        
        if year < self.valid_to_year:
            return True
        
        if self.valid_to_month is None or month is None:
            return True
        
        if month > self.valid_to_month:
            return False
        
        if month < self.valid_to_month:
            return True
        
        if self.valid_to_day is None or day is None:
            return True
        
        return day <= self.valid_to_day