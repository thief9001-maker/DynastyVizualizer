"""Command for recalculating generation levels for all people."""

from commands.base_command import BaseCommand


class RecomputeGenerationsCommand(BaseCommand):
    """Recalculate generation numbers for entire family tree."""

    def __init__(self, database_connection) -> None:
        """Initialize the recompute generations command."""
        super().__init__()
        self.db = database_connection
        self.old_generations: dict[int, int] = {}
        # TODO: Store original generation assignments for undo

    def run(self) -> None:
        """Calculate and update generation levels."""
        # TODO: Use GenerationCalculator to compute levels
        # TODO: Update Person table with new generation values
        # TODO: Update tree view layout
        pass

    def undo(self) -> None:
        """Restore original generation assignments."""
        # TODO: Restore generation values from old_generations
        # TODO: Update tree view layout
        pass
