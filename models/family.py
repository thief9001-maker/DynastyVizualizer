"""Data model for Family dynasties."""


class Family:
    """Represents a family dynasty grouping."""

    def __init__(
        self,
        family_id: int,
        surname: str,
        move_in_year: int | None = None,
        move_in_month: int | None = None,
        move_in_day: int | None = None,
        coat_of_arms_path: str | None = None,
        family_color: str | None = None,
        is_extinct: bool = False,
        notes: str | None = None,
    ) -> None:
        """Initialize a family dynasty."""
        self.id = family_id
        self.surname = surname
        self.move_in_year = move_in_year
        self.move_in_month = move_in_month
        self.move_in_day = move_in_day
        self.coat_of_arms_path = coat_of_arms_path
        self.family_color = family_color
        self.is_extinct = is_extinct
        self.notes = notes

    # TODO: Add move_in_date_string property
    # TODO: Add member_count property (requires database query)
    # TODO: Add founding_date property
    # TODO: Add end_date property
    # TODO: Add longest_lived_member property
