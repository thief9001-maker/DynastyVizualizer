"""Command for adding a new person to the database."""

from commands.base_command import BaseCommand


class AddPersonCommand(BaseCommand):
    """Add a new person to the dynasty database."""

    def __init__(self, person_data: dict) -> None:
        """Initialize the add person command."""
        self.person_data = person_data
        self.person_id: int | None = None

    def run(self) -> None:
        """Insert the person into the database."""
        # TODO: Implement database INSERT
        # TODO: Store generated person_id for undo
        pass

    def undo(self) -> None:
        """Remove the person from the database."""
        # TODO: Implement database DELETE using stored person_id
        pass
