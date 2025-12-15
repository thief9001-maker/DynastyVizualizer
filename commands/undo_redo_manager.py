from __future__ import annotations

from commands.base_command import BaseCommand


class UndoRedoManager:
    """Manages undo and redo stacks for command pattern operations."""
    
    def __init__(self) -> None:
        """Initialize the undo/redo manager with empty stacks."""
        self.undo_stack: list[BaseCommand] = []
        self.redo_stack: list[BaseCommand] = []
    
    def execute(self, command: BaseCommand) -> None:  
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
    
    def peek_undo(self) -> BaseCommand | None:
        """Get the next command that would be undone without executing it."""
        if self.can_undo():
            return self.undo_stack[-1]
        return None
    
    def peek_redo(self) -> BaseCommand | None:
        """Get the next command that would be redone without executing it."""
        if self.can_redo():
            return self.redo_stack[-1]
        return None