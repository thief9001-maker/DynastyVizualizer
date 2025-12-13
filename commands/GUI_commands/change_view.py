"""Command for switching between different visualization views."""

from commands.base_command import BaseCommand


class ChangeViewCommand(BaseCommand):
    """Switch between tree, timeline, table, and stats views."""

    def __init__(self, new_view: str, old_view: str) -> None:
        """Initialize the change view command."""
        self.new_view = new_view  # "tree", "timeline", "table", "stats"
        self.old_view = old_view
        # TODO: Add reference to main window

    def run(self) -> None:
        """Switch to the new visualization view."""
        # TODO: Hide current view widget
        # TODO: Show new view widget
        # TODO: Update menu checkmarks
        pass

    def undo(self) -> None:
        """Switch back to the previous view."""
        # TODO: Hide current view widget
        # TODO: Show old view widget
        # TODO: Update menu checkmarks
        pass
