"""Command for editing an existing marriage."""

from commands.base_command import BaseCommand


class EditMarriageCommand(BaseCommand):
    """Edit details of an existing marriage relationship."""

    def __init__(self, database_connection, marriage_id: int, **kwargs) -> None:
        """Initialize the edit marriage command."""
        self.db = database_connection
        self.marriage_id = marriage_id
        self.new_data = kwargs
        self.old_data: dict = {}
        # TODO: Store original marriage data for undo

    def run(self) -> None:
        """Update marriage details in database."""
        # TODO: Save current state to old_data
        # TODO: Update marriage record with new_data
        pass

    def undo(self) -> None:
        """Restore original marriage details."""
        # TODO: Restore marriage record from old_data
        pass
