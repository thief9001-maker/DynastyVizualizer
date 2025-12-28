"""Data model for Event entities."""

from dataclasses import dataclass


@dataclass
class Event:
    """Represents a life event for a person."""
    
    # Database identity
    id: int | None = None
    
    # Associated person
    person_id: int | None = None
    
    # Event details
    event_type: str = ""  # "Birth", "Marriage", "Death", "Job", "Move", etc.
    event_title: str = ""  # "Became Blacksmith", "Moved to Town", etc.
    
    # Start date (flexible precision)
    start_year: int | None = None
    start_month: int | None = None
    start_day: int | None = None
    
    # End date (for ongoing events like jobs)
    end_year: int | None = None
    end_month: int | None = None
    end_day: int | None = None
    
    # Notes
    notes: str = ""
    
    @property
    def is_ongoing(self) -> bool:
        """Check if the event is currently ongoing (no end date)."""
        return self.end_year is None
    
    @property
    def start_date_string(self) -> str:
        """Format start date as readable string."""
        if not self.start_year:
            return "Unknown"
        
        month_names = ["", "January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        if self.start_month and self.start_day:
            # Full date
            return f"{month_names[self.start_month]} {self.start_day}, {self.start_year}"
        elif self.start_month:
            # Year and month
            return f"{month_names[self.start_month]} {self.start_year}"
        else:
            # Year only
            return str(self.start_year)
    
    @property
    def end_date_string(self) -> str:
        """Format end date as readable string."""
        if not self.end_year:
            return "Ongoing" if self.start_year else ""
        
        month_names = ["", "January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        if self.end_month and self.end_day:
            # Full date
            return f"{month_names[self.end_month]} {self.end_day}, {self.end_year}"
        elif self.end_month:
            # Year and month
            return f"{month_names[self.end_month]} {self.end_year}"
        else:
            # Year only
            return str(self.end_year)
    
    @property
    def duration_years(self) -> int | None:
        """Calculate event duration in years (None if ongoing or no dates)."""
        if not self.start_year:
            return None
        
        if self.end_year:
            return self.end_year - self.start_year
        
        return None  # Ongoing, no duration yet
    
    @property
    def date_range_string(self) -> str:
        """Get formatted date range for display."""
        if self.is_ongoing:
            return f"{self.start_date_string} - Present"
        elif self.end_year:
            return f"{self.start_date_string} - {self.end_date_string}"
        else:
            return self.start_date_string