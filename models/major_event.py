"""Data model for MajorEvent entities."""

from __future__ import annotations

from dataclasses import dataclass

from utils.date_formatter import DateFormatter, DateParts, MonthStyle


@dataclass
class MajorEvent:
    """Represents a major historical event affecting multiple families."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    EVENT_TYPE_WAR: str = "War"
    EVENT_TYPE_PLAGUE: str = "Plague"
    EVENT_TYPE_FAMINE: str = "Famine"
    EVENT_TYPE_DISASTER: str = "Disaster"
    EVENT_TYPE_CELEBRATION: str = "Celebration"
    EVENT_TYPE_POLITICAL: str = "Political"
    EVENT_TYPE_OTHER: str = "Other"
    
    DATE_UNKNOWN: str = "Unknown"
    DATE_ONGOING: str = "Ongoing"
    DATE_PRESENT: str = "Present"
    
    # ------------------------------------------------------------------
    # Database Identity
    # ------------------------------------------------------------------
    
    id: int | None = None
    
    # ------------------------------------------------------------------
    # Event Details
    # ------------------------------------------------------------------
    
    event_name: str = ""
    event_type: str = ""
    description: str = ""
    
    # ------------------------------------------------------------------
    # Start Date
    # ------------------------------------------------------------------
    
    start_year: int | None = None
    start_month: int | None = None
    start_day: int | None = None
    
    # ------------------------------------------------------------------
    # End Date
    # ------------------------------------------------------------------
    
    end_year: int | None = None
    end_month: int | None = None
    end_day: int | None = None
    
    # ------------------------------------------------------------------
    # Visual Representation
    # ------------------------------------------------------------------
    
    color: str = ""
    
    # ------------------------------------------------------------------
    # Computed Properties - Status
    # ------------------------------------------------------------------
    
    @property
    def is_ongoing(self) -> bool:
        """Check if the event is currently ongoing."""
        return self.end_year is None
    
    # ------------------------------------------------------------------
    # Computed Properties - Date Formatting
    # ------------------------------------------------------------------
    
    @property
    def start_date_string(self) -> str:
        """Format start date as readable string."""
        if self.start_year is None:
            return self.DATE_UNKNOWN
        
        date_parts: DateParts = DateParts(
            year=self.start_year,
            month=self.start_month,
            day=self.start_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            month_style=MonthStyle.FULL_NAME,
            separator=" "
        )
    
    @property
    def end_date_string(self) -> str:
        """Format end date as readable string."""
        if self.end_year is None:
            return self.DATE_ONGOING
        
        date_parts: DateParts = DateParts(
            year=self.end_year,
            month=self.end_month,
            day=self.end_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            month_style=MonthStyle.FULL_NAME,
            separator=" "
        )
    
    @property
    def date_range_string(self) -> str:
        """Get formatted date range for display."""
        if self.is_ongoing:
            return f"{self.start_date_string} - {self.DATE_PRESENT}"
        elif self.end_year:
            return f"{self.start_date_string} - {self.end_date_string}"
        else:
            return self.start_date_string
    
    # ------------------------------------------------------------------
    # Computed Properties - Duration
    # ------------------------------------------------------------------
    
    @property
    def duration_years(self) -> int | None:
        """Calculate event duration in years (None if ongoing or no dates)."""
        if self.start_year is None:
            return None
        
        if self.end_year:
            return self.end_year - self.start_year
        
        return None
    
    @property
    def duration_string(self) -> str:
        """Get human-readable duration."""
        duration: int | None = self.duration_years
        
        if duration is None:
            if self.is_ongoing:
                return self.DATE_ONGOING
            return self.DATE_UNKNOWN
        
        if duration == 0:
            return "Less than 1 year"
        
        return f"{duration} year{'s' if duration != 1 else ''}"