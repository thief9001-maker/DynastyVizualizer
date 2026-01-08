"""Data model for Person entities."""

from __future__ import annotations

from dataclasses import dataclass

from utils.date_formatter import DateFormatter, DateParts, MonthStyle, DateOrder


@dataclass
class Person:
    """Represents a person in a dynasty with flexible date precision."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    DEFAULT_GENDER: str = "Unknown"
    DEFAULT_DYNASTY_ID: int = 1
    DEFAULT_EDUCATION: int = 0
    
    GENDER_MALE: str = "Male"
    GENDER_FEMALE: str = "Female"
    GENDER_UNKNOWN: str = "Unknown"
    GENDER_OTHER: str = "Other"
    
    DATE_UNKNOWN: str = "Unknown"
    DATE_ALIVE: str = "Alive"
    DATE_SEPARATOR: str = "-"
    DATE_PLACEHOLDER: str = "?"
    
    # Database Identity
    id: int | None = None
    dynasty_id: int = DEFAULT_DYNASTY_ID
    family_id: int | None = None
    
    # Name Fields
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    maiden_name: str = ""
    nickname: str = ""
    
    # Biological Information
    gender: str = DEFAULT_GENDER
    
    # Birth Date
    birth_year: int | None = None
    birth_month: int | None = None
    birth_day: int | None = None
    
    # Death Date
    death_year: int | None = None
    death_month: int | None = None
    death_day: int | None = None
    
    # Arrival/Departure Dates
    arrival_year: int | None = None
    arrival_month: int | None = None
    arrival_day: int | None = None
    moved_out_year: int | None = None
    moved_out_month: int | None = None
    moved_out_day: int | None = None
    
    # Relationships
    father_id: int | None = None
    mother_id: int | None = None
    
    # Game-Specific Fields
    is_founder: bool = False
    education: int = DEFAULT_EDUCATION
    
    # User Notes
    notes: str = ""
    
    # ------------------------------------------------------------------
    # Computed Properties - Names
    # ------------------------------------------------------------------
    
    @property
    def full_name(self) -> str:
        """Get full name with optional middle name and nickname."""
        parts: list[str] = [self.first_name]
        
        if self.middle_name:
            parts.append(self.middle_name)
        
        parts.append(self.last_name)
        name: str = " ".join(parts)
        
        if self.nickname:
            name += f' "{self.nickname}"'
        
        return name
    
    @property
    def display_name(self) -> str:
        """Get display name (first + last, no middle or nickname)."""
        return f"{self.first_name} {self.last_name}"
    
    # ------------------------------------------------------------------
    # Computed Properties - Life Status
    # ------------------------------------------------------------------
    
    @property
    def is_deceased(self) -> bool:
        """Check if person is deceased."""
        return self.death_year is not None
    
    def is_alive_in_year(self, year: int) -> bool:
        """Check if person was alive in a given year."""
        if self.birth_year is None or year < self.birth_year:
            return False
        
        if self.death_year is None:
            return True
        
        return year <= self.death_year
    
    # ------------------------------------------------------------------
    # Computed Properties - Age Calculations
    # ------------------------------------------------------------------
    
    def get_age(self, current_year: int) -> int | None:
        """Calculate age at a given year."""
        if self.birth_year is None:
            return None
        
        if self.death_year is not None and current_year > self.death_year:
            return None
        
        return current_year - self.birth_year
    
    def get_age_at_death(self) -> int | None:
        """Calculate age at death, or None if not deceased or birth year unknown."""
        if not self.is_deceased or self.birth_year is None or self.death_year is None:
            return None
        
        return self.death_year - self.birth_year
    
    # ------------------------------------------------------------------
    # Computed Properties - Date Formatting
    # ------------------------------------------------------------------
    
    @property
    def birth_date_string(self) -> str:
        """Format birth date as readable string."""
        if self.birth_year is None:
            return self.DATE_UNKNOWN
        
        date_parts: DateParts = DateParts(
            year=self.birth_year,
            month=self.birth_month,
            day=self.birth_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            order=DateOrder.DMY,
            month_style=MonthStyle.NUMERIC_PADDED,
            separator="/",
            pad_day=True
        )
    
    @property
    def death_date_string(self) -> str:
        """Format death date as readable string."""
        if self.death_year is None:
            return self.DATE_ALIVE
        
        date_parts: DateParts = DateParts(
            year=self.death_year,
            month=self.death_month,
            day=self.death_day
        )
        
        return DateFormatter.format_display(
            date=date_parts,
            order=DateOrder.DMY,
            month_style=MonthStyle.NUMERIC_PADDED,
            separator="/",
            pad_day=True
        )
    
    @property
    def lifespan_string(self) -> str:
        """Get lifespan as formatted string (e.g., '1420-1475' or '1450-')."""
        birth: str = str(self.birth_year) if self.birth_year else self.DATE_PLACEHOLDER
        death: str = str(self.death_year) if self.death_year else ""
        return f"{birth}{self.DATE_SEPARATOR}{death}"