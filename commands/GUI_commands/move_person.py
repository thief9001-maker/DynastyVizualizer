"""Command for moving a person box in the tree view."""

from commands.base_command import BaseCommand


class MovePersonCommand(BaseCommand):
    """Move a person's visual position in the tree canvas."""

    def __init__(
        self,
        person_id: int,
        new_x: float,
        new_y: float,
        old_x: float,
        old_y: float,
    ) -> None:
        """Initialize the move person command."""
        super().__init__()
        self.person_id = person_id
        self.new_x = new_x
        self.new_y = new_y
        self.old_x = old_x
        self.old_y = old_y
        # TODO: Add reference to canvas/scene for visual updates

    def run(self) -> None:
        """Move person box to new position."""
        # TODO: Update PersonPosition table in database
        # TODO: Update visual position on canvas
        pass

    def undo(self) -> None:
        """Restore person box to original position."""
        # TODO: Update PersonPosition table with old coordinates
        # TODO: Update visual position on canvas
        pass
