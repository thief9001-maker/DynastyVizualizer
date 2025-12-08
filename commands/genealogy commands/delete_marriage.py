"""Command for deleting a marriage from the database."""

from commands.base_command import BaseCommand


class DeleteMarriageCommand(BaseCommand):
    """Remove a marriage relationship from the database."""

    def __init__(self, database_connection, marriage_id: int) -> None:
        """Initialize the delete marriage command."""
        self.db = database_connection
        self.marriage_id = marriage_id
        self.deleted_data: dict = {}
        # TODO: Store complete marriage data for undo

    def run(self) -> None:
        """Delete the marriage from database."""
        # TODO: Fetch and save complete marriage data to deleted_data
        # TODO: Delete marriage record from database
        pass

    def undo(self) -> None:
        """Restore the deleted marriage."""
        # TODO: Re-insert marriage record from deleted_data
        pass
