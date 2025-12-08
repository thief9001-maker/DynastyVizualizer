"""Data model for Person entities."""


class Person:
    """Represents a person in the dynasty database."""

    def __init__(
        self,
        person_id: int,
        first_name: str,
        last_name: str,
        maiden_name: str | None = None,
        gender: str | None = None,
        birth_year: int | None = None,
        birth_month: int | None = None,
        birth_day: int | None = None,
        death_year: int | None = None,
        death_month: int | None = None,
        death_day: int | None = None,
        arrival_year: int | None = None,
        arrival_month: int | None = None,
        arrival_day: int | None = None,
        moved_out_year: int | None = None,
        moved_out_month: int | None = None,
        moved_out_day: int | None = None,
        father_id: int | None = None,
        mother_id: int | None = None,
        family_id: int | None = None,
        notes: str | None = None,
    ) -> None:
        """Initialize a person with genealogical data."""
        self.id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.maiden_name = maiden_name
        self.gender = gender
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.death_year = death_year
        self.death_month = death_month
        self.death_day = death_day
        self.arrival_year = arrival_year
        self.arrival_month = arrival_month
        self.arrival_day = arrival_day
        self.moved_out_year = moved_out_year
        self.moved_out_month = moved_out_month
        self.moved_out_day = moved_out_day
        self.father_id = father_id
        self.mother_id = mother_id
        self.family_id = family_id
        self.notes = notes

    @property
    def full_name(self) -> str:
        """Get the full name of the person."""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_deceased(self) -> bool:
        """Check if the person is deceased."""
        return self.death_year is not None

    # TODO: Add age_at_death property
    # TODO: Add current_age property
    # TODO: Add lifespan property
    # TODO: Add birth_date_string property
    # TODO: Add death_date_string property
