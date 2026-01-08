"""Handles edit menu actions (Undo, Redo, Add/Remove operations)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QAction

if TYPE_CHECKING:
    from main import MainWindow
    from models.person import Person

from dialogs.add_person_dialog import AddPersonDialog
from commands.genealogy_commands import AddPersonCommand


class EditActions:
    """Handles edit menu actions (Undo, Redo, Add/Remove operations)."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Action Text Formats
    ACTION_TEXT_UNDO_DEFAULT: str = "Undo"
    ACTION_TEXT_REDO_DEFAULT: str = "Redo"
    ACTION_TEXT_UNDO_FORMAT: str = "Undo {description}"
    ACTION_TEXT_REDO_FORMAT: str = "Redo {description}"
    
    # Dialog Results
    DIALOG_ACCEPTED: int = 1
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, parent: MainWindow) -> None:
        """Initialize edit actions handler."""
        self.parent: MainWindow = parent
        
        self.undo_action: QAction | None = None
        self.redo_action: QAction | None = None
    
    # ------------------------------------------------------------------
    # Undo/Redo Menu Updates
    # ------------------------------------------------------------------
    
    def update_undo_redo_actions(self) -> None:
        """Update Undo/Redo menu items with current action descriptions."""
        if not self._has_undo_redo_actions():
            return
        
        self._update_undo_action()
        self._update_redo_action()
    
    def _has_undo_redo_actions(self) -> bool:
        """Check if undo/redo action references are set."""
        return self.undo_action is not None and self.redo_action is not None
    
    def _update_undo_action(self) -> None:
        """Update undo action text and enabled state."""
        if self.undo_action is None:
            return
        
        undo_manager = self.parent.undo_manager
        
        if not undo_manager.can_undo():
            self.undo_action.setText(self.ACTION_TEXT_UNDO_DEFAULT)
            self.undo_action.setEnabled(False)
            return
        
        next_undo = undo_manager.peek_undo()
        if not next_undo:
            self.undo_action.setText(self.ACTION_TEXT_UNDO_DEFAULT)
            self.undo_action.setEnabled(False)
            return
        
        self.undo_action.setText(
            self.ACTION_TEXT_UNDO_FORMAT.format(description=next_undo.description())
        )
        self.undo_action.setEnabled(True)
    
    def _update_redo_action(self) -> None:
        """Update redo action text and enabled state."""
        if self.redo_action is None:
            return
        
        undo_manager = self.parent.undo_manager
        
        if not undo_manager.can_redo():
            self.redo_action.setText(self.ACTION_TEXT_REDO_DEFAULT)
            self.redo_action.setEnabled(False)
            return
        
        next_redo = undo_manager.peek_redo()
        if not next_redo:
            self.redo_action.setText(self.ACTION_TEXT_REDO_DEFAULT)
            self.redo_action.setEnabled(False)
            return
        
        self.redo_action.setText(
            self.ACTION_TEXT_REDO_FORMAT.format(description=next_redo.description())
        )
        self.redo_action.setEnabled(True)
    
    # ------------------------------------------------------------------
    # Undo/Redo Operations
    # ------------------------------------------------------------------
    
    def undo(self) -> None:
        """Undo the last action."""
        if not self.parent.undo_manager.undo():
            return
        
        self._refresh_after_undo_redo()
    
    def redo(self) -> None:
        """Redo the last undone action."""
        if not self.parent.undo_manager.redo():
            return
        
        self._refresh_after_undo_redo()
    
    def _refresh_after_undo_redo(self) -> None:
        """Refresh UI after undo or redo operation."""
        self.parent.db.mark_dirty()
        self.parent.refresh_ui()
        self.update_undo_redo_actions()
    
    # ------------------------------------------------------------------
    # Person Operations
    # ------------------------------------------------------------------
    
    def add_person(self) -> None:
        """Open dialog to add a new person to the database."""
        dialog: AddPersonDialog = AddPersonDialog(self.parent.db)
        
        if not self._dialog_accepted(dialog):
            return
        
        person: Person | None = dialog.get_person()
        if not person:
            return
        
        self._execute_add_person_command(person)
    
    def _dialog_accepted(self, dialog: QDialog) -> bool:
        """Check if dialog was accepted."""
        return dialog.exec() == self.DIALOG_ACCEPTED
    
    def _execute_add_person_command(self, person: Person) -> None:
        """Execute command to add person to database."""
        command: AddPersonCommand = AddPersonCommand(self.parent.db, person)
        self.parent.undo_manager.execute(command)
        self.parent.refresh_ui()
        self.update_undo_redo_actions()
    
    def remove_person(self) -> None:
        """Remove the selected person from the database."""
        pass
    
    # ------------------------------------------------------------------
    # Family Operations
    # ------------------------------------------------------------------
    
    def add_new_family(self) -> None:
        """Create a new family branch in the dynasty."""
        pass