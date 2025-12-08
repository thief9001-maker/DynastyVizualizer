"""Command for creating a marriage between two people."""

from commands.base_command import BaseCommand


class CreateMarriageCommand(BaseCommand):
    """Create a marriage relationship between two people."""

    def __init__(self, marriage_data: dict) -> None:
        """Initialize the create marriage command."""
        self.marriage_data = marriage_data
        self.marriage_id: int | None = None

    def run(self) -> None:
        """Insert the marriage into the database."""
        # TODO: Implement database INSERT
        # TODO: Store generated marriage_id for undo
        # TODO: Handle surname changes if configured
        pass

    def undo(self) -> None:
        """Remove the marriage from the database."""
        # TODO: Implement database DELETE
        # TODO: Revert surname changes if applicable
        pass
