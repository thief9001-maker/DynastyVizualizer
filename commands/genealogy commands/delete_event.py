"""Command for deleting an event from the database."""

from commands.base_command import BaseCommand


class DeleteEventCommand(BaseCommand):
    """Remove an event from the database."""

    def __init__(self, database_connection, event_id: int) -> None:
        """Initialize the delete event command."""
        self.db = database_connection
        self.event_id = event_id
        self.deleted_data: dict = {}
        # TODO: Store complete event data for undo

    def run(self) -> None:
        """Delete the event from database."""
        # TODO: Fetch and save complete event data to deleted_data
        # TODO: Delete event record from database
        pass

    def undo(self) -> None:
        """Restore the deleted event."""
        # TODO: Re-insert event record from deleted_data
        pass
