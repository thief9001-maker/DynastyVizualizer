"""Command for changing the application color scheme."""

from commands.base_command import BaseCommand


class ChangeSkinCommand(BaseCommand):
    """Switch between different UI color schemes."""

    def __init__(self, new_skin: str, old_skin: str) -> None:
        """Initialize the change skin command."""
        self.new_skin = new_skin
        self.old_skin = old_skin
        # TODO: Add reference to skin manager

    def run(self) -> None:
        """Apply the new color scheme."""
        # TODO: Load new skin from SkinManager
        # TODO: Update all UI elements
        # TODO: Save preference to Settings table
        pass

    def undo(self) -> None:
        """Restore previous color scheme."""
        # TODO: Load old skin from SkinManager
        # TODO: Update all UI elements
        # TODO: Save preference to Settings table
        pass
