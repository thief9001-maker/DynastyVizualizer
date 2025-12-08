"""Data model for MajorEvent entities."""


class MajorEvent:
    """Represents a major historical event affecting multiple families."""

    def __init__(
        self,
        event_id: int,
        event_name: str,
        event_type: str,
        start_year: int,
        start_month: int | None = None,
        start_day: int | None = None,
        end_year: int | None = None,
        end_month: int | None = None,
        end_day: int | None = None,
        description: str | None = None,
        color: str | None = None,
    ) -> None:
        """Initialize a major historical event."""
        self.id = event_id
        self.event_name = event_name
        self.event_type = event_type
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.description = description
        self.color = color

    @property
    def is_ongoing(self) -> bool:
        """Check if the event is ongoing."""
        return self.end_year is None

    # TODO: Add duration property
    # TODO: Add start_date_string property
    # TODO: Add end_date_string property
