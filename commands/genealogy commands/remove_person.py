"""Command for removing a person from the database."""

from commands.base_command import BaseCommand


class DeletePersonCommand(BaseCommand):
    """Delete a person from the dynasty database."""

    def __init__(self, person_id: int) -> None:
        """Initialize the delete person command."""
        self.person_id = person_id
        self.person_data: dict | None = None

    def run(self) -> None:
        """Remove the person from the database."""
        # TODO: Fetch and store all person data for undo
        # TODO: Implement database DELETE
        # TODO: Handle cascade effects (orphaned children, etc.)
        pass

    def undo(self) -> None:
        """Restore the deleted person."""
        # TODO: Implement database INSERT with stored person_data
        pass
