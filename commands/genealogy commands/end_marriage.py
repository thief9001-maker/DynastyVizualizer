"""Command for ending a marriage with divorce or death."""

from commands.base_command import BaseCommand


class EndMarriageCommand(BaseCommand):
    """Mark a marriage as ended with a specific date."""

    def __init__(
        self,
        database_connection,
        marriage_id: int,
        end_year: int | None = None,
        end_month: int | None = None,
        end_day: int | None = None,
    ) -> None:
        """Initialize the end marriage command."""
        self.db = database_connection
        self.marriage_id = marriage_id
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.old_end_date: tuple[int | None, int | None, int | None] = (None, None, None)
        # TODO: Store original end date for undo

    def run(self) -> None:
        """Set the marriage end date in database."""
        # TODO: Save current end date to old_end_date
        # TODO: Update marriage end_year, end_month, end_day
        pass

    def undo(self) -> None:
        """Restore original marriage end date."""
        # TODO: Restore end date from old_end_date
        pass
