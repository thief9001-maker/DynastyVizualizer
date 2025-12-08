"""Data model for Marriage relationships."""


class Marriage:
    """Represents a marriage relationship between two people."""

    def __init__(
        self,
        marriage_id: int,
        spouse1_id: int,
        spouse2_id: int,
        marriage_year: int | None = None,
        marriage_month: int | None = None,
        marriage_day: int | None = None,
        dissolution_year: int | None = None,
        dissolution_month: int | None = None,
        dissolution_day: int | None = None,
        dissolution_reason: str | None = None,
        marriage_type: str = "spouse",
    ) -> None:
        """Initialize a marriage relationship."""
        self.id = marriage_id
        self.spouse1_id = spouse1_id
        self.spouse2_id = spouse2_id
        self.marriage_year = marriage_year
        self.marriage_month = marriage_month
        self.marriage_day = marriage_day
        self.dissolution_year = dissolution_year
        self.dissolution_month = dissolution_month
        self.dissolution_day = dissolution_day
        self.dissolution_reason = dissolution_reason
        self.marriage_type = marriage_type

    @property
    def is_active(self) -> bool:
        """Check if the marriage is currently active."""
        return self.dissolution_year is None

    # TODO: Add duration property
    # TODO: Add marriage_date_string property
    # TODO: Add dissolution_date_string property
