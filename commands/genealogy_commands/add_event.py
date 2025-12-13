"""Command for adding an event to a person."""

from commands.base_command import BaseCommand


class AddEventCommand(BaseCommand):
    """Add a life event to a person."""

    def __init__(self, event_data: dict) -> None:
        """Initialize the add event command."""
        self.event_data = event_data
        self.event_id: int | None = None

    def run(self) -> None:
        """Insert the event into the database."""
        # TODO: Implement database INSERT
        # TODO: Store generated event_id for undo
        pass

    def undo(self) -> None:
        """Remove the event from the database."""
        # TODO: Implement database DELETE using stored event_id
        pass
