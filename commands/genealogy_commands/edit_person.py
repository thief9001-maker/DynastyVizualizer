"""Command for editing an existing person."""

from commands.base_command import BaseCommand


class EditPersonCommand(BaseCommand):
    """Edit an existing person in the database."""

    def __init__(self, person_id: int, new_data: dict) -> None:
        """Initialize the edit person command."""
        self.person_id = person_id
        self.new_data = new_data
        self.old_data: dict | None = None

    def run(self) -> None:
        """Update the person in the database."""
        # TODO: Fetch and store old data for undo
        # TODO: Implement database UPDATE
        pass

    def undo(self) -> None:
        """Restore the person's original data."""
        # TODO: Implement database UPDATE with old_data
        pass
