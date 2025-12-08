"""Data model for Portrait entities."""


class Portrait:
    """Represents a portrait image for a person."""

    def __init__(
        self,
        portrait_id: int,
        person_id: int,
        image_path: str,
        valid_from_year: int | None = None,
        valid_from_month: int | None = None,
        valid_from_day: int | None = None,
        valid_to_year: int | None = None,
        valid_to_month: int | None = None,
        valid_to_day: int | None = None,
        is_primary: bool = False,
        display_order: int = 0,
    ) -> None:
        """Initialize a portrait."""
        self.id = portrait_id
        self.person_id = person_id
        self.image_path = image_path
        self.valid_from_year = valid_from_year
        self.valid_from_month = valid_from_month
        self.valid_from_day = valid_from_day
        self.valid_to_year = valid_to_year
        self.valid_to_month = valid_to_month
        self.valid_to_day = valid_to_day
        self.is_primary = is_primary
        self.display_order = display_order

    # TODO: Add valid_from_date_string property
    # TODO: Add valid_to_date_string property
    # TODO: Add is_valid_for_date method
