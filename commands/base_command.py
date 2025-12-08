"""Base command class for undoable operations."""


class BaseCommand:
    """Base class for all undoable commands in the application."""

    def run(self) -> None:
        """Execute the command."""
        raise NotImplementedError("Subclasses must implement run()")

    def undo(self) -> None:
        """Reverse the command's effects."""
        raise NotImplementedError("Subclasses must implement undo()")
