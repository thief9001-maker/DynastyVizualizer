"""Data model for Person entities."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Person:
    """Represents a person in a dynasty with flexible date precision."""
    
    # Database identity
    id: int | None = None  # None until saved to database
    dynasty_id: int = 1
    family_id: int | None = None
    
    # Name fields (full structure for flexibility)
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    maiden_name: str = ""
    nickname: str = ""
    
    # Biological information
    sex: str = "Unknown"  # "Male", "Female", "Unknown", "Other"
    
    # Birth date (year should be provided, month/day optional)
    birth_year: int | None = None
    birth_month: int | None = None
    birth_day: int | None = None
    
    # Death date (all optional - None if alive)
    death_year: int | None = None
    death_month: int | None = None
    death_day: int | None = None
    
    # Arrival/departure dates (tracking when joined/left settlement)
    arrival_year: int | None = None
    arrival_month: int | None = None
    arrival_day: int | None = None
    moved_out_year: int | None = None
    moved_out_month: int | None = None
    moved_out_day: int | None = None
    
    # Relationships (parent IDs link to database)
    father_id: int | None = None
    mother_id: int | None = None
    
    # Game-specific fields
    is_founder: bool = False
    education: int = 0  # 0-5 scale from Ostriv
    
    # User notes
    notes: str = ""
    
    # ------------------------------------------------------------------
    # Computed Properties
    # ------------------------------------------------------------------
    
    @property
    def full_name(self) -> str:
        """Get full name with optional middle name and nickname."""
        parts = [self.first_name]
        
        if self.middle_name:
            parts.append(self.middle_name)
        
        parts.append(self.last_name)

        name = " ".join(parts)
        
        if self.nickname:
            name += f' "{self.nickname}"'

        return name
    
    @property
    def display_name(self) -> str:
        """Get display name (first + last, no middle or nickname)."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_deceased(self) -> bool:
        """Check if person is deceased."""
        return self.death_year is not None
    
    def get_age(self, current_year: int) -> int | None:
        """
        Calculate age at a given year.
        
        Returns None if birth year unknown or if person died before current year.
        """
        if self.birth_year is None:
            return None
        
        # If person died, use death year as upper bound
        if self.death_year is not None and current_year > self.death_year:
            return None
        
        return current_year - self.birth_year
    
    def is_alive_in_year(self, year: int) -> bool:
        """Check if person was alive in a given year."""
        # Must have been born by that year
        if self.birth_year is None or year < self.birth_year:
            return False
        
        # If no death year, assume still alive
        if self.death_year is None:
            return True
        
        # Check if year is before death
        return year <= self.death_year
    
    def get_age_at_death(self) -> int | None:
        """Calculate age at death, or None if not deceased or birth year unknown."""
        if not self.is_deceased or self.birth_year is None or self.death_year is None:
            return None
        
        return self.death_year - self.birth_year
    
    def get_birth_date_string(self) -> str:
        """Format birth date as string with available precision (European format)."""
        if self.birth_year is None:
            return "Unknown"
        
        if self.birth_day and self.birth_month:
            return f"{self.birth_day:02d}/{self.birth_month:02d}/{self.birth_year}"
        
        if self.birth_month:
            return f"{self.birth_month:02d}/{self.birth_year}"
        
        return str(self.birth_year)
    
    def get_death_date_string(self) -> str:
        """Format death date as string with available precision (European format)."""
        if self.death_year is None:
            return "Alive"
        
        if self.death_day and self.death_month:
            return f"{self.death_day:02d}/{self.death_month:02d}/{self.death_year}"
        
        if self.death_month:
            return f"{self.death_month:02d}/{self.death_year}"
        
        return str(self.death_year)
    
    def get_lifespan_string(self) -> str:
        """Get lifespan as formatted string (e.g., '1420-1475' or '1450-')."""
        birth = str(self.birth_year) if self.birth_year else "?"
        death = str(self.death_year) if self.death_year else ""
        return f"{birth}-{death}"