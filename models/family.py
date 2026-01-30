"""Data model for Family dynasties."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from utils.date_formatter import DateFormatter, DateParts, MonthStyle


@dataclass
class Family:
    """Represents a family dynasty grouping."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    DATE_UNKNOWN: ClassVar[str] = "Unknown"
    DEFAULT_FAMILY_NAME: ClassVar[str] = "Unknown Family"
    FAMILY_NAME_SUFFIX: ClassVar[str] = " Family"
    
    # Database Identity
    id: int | None = None

    # Family Identification
    surname: str = ""

    # Move-In Date 
    move_in_year: int | None = None
    move_in_month: int | None = None
    move_in_day: int | None = None
    
    # Visual Representation
    coat_of_arms_path: str = ""
    family_color: str = ""

    # Status
    is_extinct: bool = False
    
    # Notes
    notes: str = ""
    
    # ------------------------------------------------------------------
    # Computed Properties - Dates
    # ------------------------------------------------------------------
    
    @property
    def move_in_date_string(self) -> str:
        """Format move-in date as readable string."""
        if self.move_in_year is None:
            return self.DATE_UNKNOWN
        
        date_parts: DateParts = DateParts(
            year=self.move_in_year,
            month=self.move_in_month,
            day=self.move_in_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            month_style=MonthStyle.FULL_NAME,
            separator=" "
        )
    
    # ------------------------------------------------------------------
    # Computed Properties - Display
    # ------------------------------------------------------------------
    
    @property
    def display_name(self) -> str:
        """Get family display name."""
        return f"{self.surname}{self.FAMILY_NAME_SUFFIX}" if self.surname else self.DEFAULT_FAMILY_NAME