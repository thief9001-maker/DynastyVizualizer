"""Command for rebuilding the entire visualization scene."""

from commands.base_command import BaseCommand


class RebuildSceneCommand(BaseCommand):
    """Rebuild the current view from database state."""

    def __init__(self, database_connection, view_type: str) -> None:
        """Initialize the rebuild scene command."""
        super().__init__()
        self.db = database_connection
        self.view_type = view_type  # "tree", "timeline", "table", "stats"
        # TODO: Store current scene state for undo

    def run(self) -> None:
        """Clear and rebuild the visualization scene."""
        # TODO: Clear current scene/view
        # TODO: Reload all data from database
        # TODO: Recreate all visual elements
        pass

    def undo(self) -> None:
        """Restore previous scene state."""
        # TODO: Restore from saved scene state
        pass
