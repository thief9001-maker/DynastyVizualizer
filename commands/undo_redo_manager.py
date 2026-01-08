"""Manages undo and redo stacks for command pattern operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from commands.base_command import BaseCommand


class UndoRedoManager:
    """Manages undo and redo stacks for command pattern operations."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    STACK_EMPTY_INDEX: int = 0
    STACK_LAST_INDEX: int = -1
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self) -> None:
        """Initialize the undo/redo manager with empty stacks."""
        self.undo_stack: list[BaseCommand] = []
        self.redo_stack: list[BaseCommand] = []
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def execute(self, command: BaseCommand) -> None:
        """Execute a command and add it to the undo stack."""
        command.run()
        self.undo_stack.append(command)
        self.redo_stack.clear()
    
    # ------------------------------------------------------------------
    # Undo/Redo Operations
    # ------------------------------------------------------------------
    
    def undo(self) -> bool:
        """Undo the last executed command."""
        if not self.can_undo():
            return False
        
        cmd: BaseCommand = self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)
        
        return True
    
    def redo(self) -> bool:
        """Redo the last undone command."""
        if not self.can_redo():
            return False
        
        cmd: BaseCommand = self.redo_stack.pop()
        cmd.run()
        self.undo_stack.append(cmd)
        
        return True
    
    # ------------------------------------------------------------------
    # Stack State Queries
    # ------------------------------------------------------------------
    
    def can_undo(self) -> bool:
        """Check if there are commands available to undo."""
        return len(self.undo_stack) > self.STACK_EMPTY_INDEX
    
    def can_redo(self) -> bool:
        """Check if there are commands available to redo."""
        return len(self.redo_stack) > self.STACK_EMPTY_INDEX
    
    def peek_undo(self) -> BaseCommand | None:
        """Get the next command that would be undone without executing it."""
        if not self.can_undo():
            return None
        
        return self.undo_stack[self.STACK_LAST_INDEX]
    
    def peek_redo(self) -> BaseCommand | None:
        """Get the next command that would be redone without executing it."""
        if not self.can_redo():
            return None
        
        return self.redo_stack[self.STACK_LAST_INDEX]
    
    # ------------------------------------------------------------------
    # Stack Management
    # ------------------------------------------------------------------
    
    def clear(self) -> None:
        """Clear both undo and redo stacks."""
        self.undo_stack.clear()
        self.redo_stack.clear()
    
    def clear_undo_stack(self) -> None:
        """Clear only the undo stack."""
        self.undo_stack.clear()
    
    def clear_redo_stack(self) -> None:
        """Clear only the redo stack."""
        self.redo_stack.clear()