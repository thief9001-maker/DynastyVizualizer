from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QAction

from dialogs.add_person_dialog import AddPersonDialog
from commands.genealogy_commands import AddPersonCommand
        

class EditActions:
    """Handles edit menu actions (Undo, Redo, Add/Remove operations)."""
    
    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize edit actions handler."""
        self.parent = parent
        
        # Store references to the menu actions so we can update their text
        # These will be set by MainWindow after it creates the menu
        self.undo_action: QAction | None = None
        self.redo_action: QAction | None = None
    
    def update_undo_redo_actions(self) -> None:
        """Update Undo/Redo menu items with current action descriptions."""
        if self.undo_action is None or self.redo_action is None:
            return 
        
        undo_manager = self.parent.undo_manager
        
        # Update Undo action
        if undo_manager.can_undo():
            next_undo = undo_manager.peek_undo()
            if next_undo:
                self.undo_action.setText(f"Undo {next_undo.description()}")
                self.undo_action.setEnabled(True)
        else:
            self.undo_action.setText("Undo")
            self.undo_action.setEnabled(False)
        
        # Update Redo action
        if undo_manager.can_redo():
            next_redo = undo_manager.peek_redo()
            if next_redo:
                self.redo_action.setText(f"Redo {next_redo.description()}")
                self.redo_action.setEnabled(True)
        else:
            self.redo_action.setText("Redo")
            self.redo_action.setEnabled(False)
    
    def undo(self) -> None:
        """Undo the last action."""
        if self.parent.undo_manager.undo():
            self.parent.db.mark_dirty()
            self.parent.refresh_ui()
            self.update_undo_redo_actions()  # Update menu after undo
    
    def redo(self) -> None:
        """Redo the last undone action."""
        if self.parent.undo_manager.redo():
            self.parent.db.mark_dirty()
            self.parent.refresh_ui()
            self.update_undo_redo_actions()  # Update menu after redo
    
    def add_person(self) -> None:
        """Open dialog to add a new person to the database."""

        dialog = AddPersonDialog(self.parent)
        result = dialog.exec()
        
        if result == 1:  # QDialog.accepted
            person = dialog.get_person()
            if person:
                command = AddPersonCommand(self.parent.db, person)
                self.parent.undo_manager.execute(command)
                self.parent.refresh_ui()
                self.update_undo_redo_actions()  # Update menu after adding person
    
    def remove_person(self) -> None:
        """Remove the selected person from the database."""
        pass  # TODO: Implement with confirmation dialog
    
    def add_new_family(self) -> None:
        """Create a new family branch in the dynasty."""
        pass  # TODO: Implement family creation