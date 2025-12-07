from __future__ import annotations
from typing import Protocol


class Command(Protocol):
    """Protocol defining the interface for undoable commands."""

    def run(self) -> None:
        """Execute the command."""
        ...

    def undo(self) -> None:
        """Reverse the command's effects."""
        ...


class UndoRedoManager:
    """Manages undo and redo stacks for command pattern operations."""

    def __init__(self) -> None:
        """Initialize the undo/redo manager with empty stacks."""
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        """Execute a command and add it to the undo stack."""
        command.run()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self) -> bool:
        """Undo the last executed command."""
        if not self.undo_stack:
            return False
        cmd = self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)
        return True

    def redo(self) -> bool:
        """Redo the last undone command."""
        if not self.redo_stack:
            return False
        cmd = self.redo_stack.pop()
        cmd.run()
        self.undo_stack.append(cmd)
        return True

    def can_undo(self) -> bool:
        """Check if there are commands available to undo."""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if there are commands available to redo."""
        return len(self.redo_stack) > 0
