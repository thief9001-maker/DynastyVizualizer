"""Data model for Marriage relationships."""

from dataclasses import dataclass


@dataclass
class Marriage:
    """Represents a marriage relationship between two people."""
    
    # Database identity
    id: int | None = None
    
    # Spouses (person IDs)
    spouse1_id: int | None = None
    spouse2_id: int | None = None
    
    # Marriage date (flexible precision)
    marriage_year: int | None = None
    marriage_month: int | None = None
    marriage_day: int | None = None
    
    # Dissolution/End date (flexible precision)
    dissolution_year: int | None = None
    dissolution_month: int | None = None
    dissolution_day: int | None = None
    
    # Dissolution details
    dissolution_reason: str = ""  # "Death", "Divorce", "Annulment", etc.
    
    # Marriage type (for different cultures/eras)
    marriage_type: str = "spouse"  # "spouse", "partner", "common-law", etc.
    
    # Notes
    notes: str = ""
    
    @property
    def is_active(self) -> bool:
        """Check if the marriage is currently active (not dissolved)."""
        return self.dissolution_year is None
    
    @property
    def marriage_date_string(self) -> str:
        """Format marriage date as readable string."""
        if not self.marriage_year:
            return "Unknown"
        
        month_names = ["", "January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        if self.marriage_month and self.marriage_day:
            # Full date: "January 15, 1675"
            return f"{month_names[self.marriage_month]} {self.marriage_day}, {self.marriage_year}"
        elif self.marriage_month:
            # Year and month: "January 1675"
            return f"{month_names[self.marriage_month]} {self.marriage_year}"
        else:
            # Year only
            return str(self.marriage_year)
    
    @property
    def dissolution_date_string(self) -> str:
        """Format dissolution date as readable string."""
        if not self.dissolution_year:
            return ""
        
        month_names = ["", "January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        if self.dissolution_month and self.dissolution_day:
            # Full date
            return f"{month_names[self.dissolution_month]} {self.dissolution_day}, {self.dissolution_year}"
        elif self.dissolution_month:
            # Year and month
            return f"{month_names[self.dissolution_month]} {self.dissolution_year}"
        else:
            # Year only
            return str(self.dissolution_year)
    
    @property
    def duration_string(self) -> str:
        """Calculate marriage duration as readable string with years, months, days."""
        if not self.marriage_year:
            return "Unknown duration"
        
        # If still active (no dissolution date), can't calculate
        if self.is_active or not self.dissolution_year:
            return "Ongoing"
        
        # Calculate duration
        start_year = self.marriage_year
        start_month = self.marriage_month or 1  # Default to January if unknown
        start_day = self.marriage_day or 1  # Default to 1st if unknown
        
        end_year = self.dissolution_year  # Now guaranteed to be int, not None
        end_month = self.dissolution_month or 1
        end_day = self.dissolution_day or 1
        
        # Calculate differences
        years = end_year - start_year
        months = end_month - start_month
        days = end_day - start_day
        
        # Adjust for negative days
        if days < 0:
            months -= 1
            # Days in previous month (approximate as 30)
            days += 30
        
        # Adjust for negative months
        if months < 0:
            years -= 1
            months += 12
        
        # Build string
        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        if days > 0 and self.marriage_day and self.dissolution_day:
            # Only show days if both dates have day precision
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        
        if not parts:
            return "Less than 1 month"
        
        return ", ".join(parts)

    @property
    def duration_years(self) -> int | None:
        """Calculate marriage duration in years only (for sorting/filtering)."""
        if not self.marriage_year or self.is_active or not self.dissolution_year:
            return None
        
        return self.dissolution_year - self.marriage_year
    
    @property
    def status_string(self) -> str:
        """Get marriage status as readable string."""
        if self.is_active:
            return "Active"
        
        if self.dissolution_reason:
            return f"Ended ({self.dissolution_reason})"
        
        return "Ended"