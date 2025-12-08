"""Command for removing a parent assignment from a person."""

from commands.base_command import BaseCommand


class UnassignParentCommand(BaseCommand):
    """Remove a person's father or mother relationship."""

    def __init__(
        self,
        database_connection,
        person_id: int,
        parent_type: str,  # "father" or "mother"
    ) -> None:
        """Initialize the unassign parent command."""
        self.db = database_connection
        self.person_id = person_id
        self.parent_type = parent_type
        self.old_parent_id: int | None = None
        # TODO: Store original parent ID for undo

    def run(self) -> None:
        """Remove the parent relationship from database."""
        # TODO: Save current parent ID to old_parent_id
        # TODO: Set father_id or mother_id to NULL based on parent_type
        pass

    def undo(self) -> None:
        """Restore the parent relationship."""
        # TODO: Restore parent ID from old_parent_id
        pass
