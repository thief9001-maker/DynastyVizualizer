"""Command for assigning a parent to a person."""

from commands.base_command import BaseCommand


class AssignParentCommand(BaseCommand):
    """Set or change a person's father or mother."""

    def __init__(
        self,
        database_connection,
        person_id: int,
        parent_id: int,
        parent_type: str,  # "father" or "mother"
    ) -> None:
        """Initialize the assign parent command."""
        self.db = database_connection
        self.person_id = person_id
        self.parent_id = parent_id
        self.parent_type = parent_type
        self.old_parent_id: int | None = None
        # TODO: Store original parent ID for undo

    def run(self) -> None:
        """Assign the parent relationship in database."""
        # TODO: Save current parent ID to old_parent_id
        # TODO: Update father_id or mother_id based on parent_type
        pass

    def undo(self) -> None:
        """Restore original parent relationship."""
        # TODO: Restore parent ID from old_parent_id
        pass
