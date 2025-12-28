"""Data model for Family dynasties."""

from dataclasses import dataclass


@dataclass
class Family:
    """Represents a family dynasty grouping."""
    
    # Database identity
    id: int | None = None
    
    # Family identification
    surname: str = ""
    
    # Move-in date (when family arrived in settlement)
    move_in_year: int | None = None
    move_in_month: int | None = None
    move_in_day: int | None = None
    
    # Visual representation
    coat_of_arms_path: str = ""  # Path to coat of arms image
    family_color: str = ""  # Hex color for UI display
    
    # Status
    is_extinct: bool = False  # True if no living members
    
    # Notes
    notes: str = ""
    
    @property
    def move_in_date_string(self) -> str:
        """Format move-in date as readable string."""
        if not self.move_in_year:
            return "Unknown"
        
        month_names = ["", "January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        if self.move_in_month and self.move_in_day:
            # Full date
            return f"{month_names[self.move_in_month]} {self.move_in_day}, {self.move_in_year}"
        elif self.move_in_month:
            # Year and month
            return f"{month_names[self.move_in_month]} {self.move_in_year}"
        else:
            # Year only
            return str(self.move_in_year)
    
    @property
    def display_name(self) -> str:
        """Get family display name."""
        return f"{self.surname} Family" if self.surname else "Unknown Family"
    
    # Note: member_count, founding_date, end_date, longest_lived_member
    # require database queries, so they'll be methods in FamilyRepository