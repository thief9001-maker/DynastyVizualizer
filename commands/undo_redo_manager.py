from __future__ import annotations
from typing import Protocol, Any


class Command(Protocol):
    def run(self) -> None:
        ...

    def undo(self) -> None:
        ...

class UndoRedoManager:
    def __init__(self):
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.run()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self) -> bool:
        if not self.undo_stack:
            return False
        cmd = self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)
        return True
    
    def redo(self) -> bool:
        if not self.redo_stack:
            return False
        cmd = self.redo_stack.pop()
        cmd.run()
        self.undo_stack.append(cmd)
        return True
    
    def can_undo(self) -> bool:
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0