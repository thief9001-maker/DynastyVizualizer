"""Command for editing an existing event."""

from commands.base_command import BaseCommand


class EditEventCommand(BaseCommand):
    """Edit details of an existing event."""

    def __init__(self, database_connection, event_id: int, **kwargs) -> None:
        """Initialize the edit event command."""
        self.db = database_connection
        self.event_id = event_id
        self.new_data = kwargs
        self.old_data: dict = {}
        # TODO: Store original event data for undo

    def run(self) -> None:
        """Update event details in database."""
        # TODO: Save current state to old_data
        # TODO: Update event record with new_data
        pass

    def undo(self) -> None:
        """Restore original event details."""
        # TODO: Restore event record from old_data
        pass
