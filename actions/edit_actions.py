from PySide6.QtWidgets import QDialog

class EditActions:
    """Handles edit menu actions (Undo, Redo, Add/Remove operations)."""
    
    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize edit actions handler."""
        self.parent = parent
    
    def undo(self) -> None:
        """Undo the last action."""
        if self.parent.undo_manager.undo():
            self.parent.db.mark_dirty()
            self.parent.refresh_ui()
    
    def redo(self) -> None:
        """Redo the last undone action."""
        if self.parent.undo_manager.redo():
            self.parent.db.mark_dirty()
            self.parent.refresh_ui()
    
    def add_person(self) -> None:
        """Open dialog to add a new person to the database."""
        from dialogs.add_person_dialog import AddPersonDialog
        from commands.genealogy_commands import AddPersonCommand

        dialog = AddPersonDialog(self.parent)
        result = dialog.exec()

        if result == 1:  # QDialog.accepted
            person = dialog.get_person()

            if person:
                command = AddPersonCommand(self.parent.db, person)
                self.parent.undo_manager.execute(command)
                self.parent.refresh_ui()
    
    def remove_person(self) -> None:
        """Remove the selected person from the database."""
        pass  # TODO: Implement with confirmation dialog
    
    def add_new_family(self) -> None:
        """Create a new family branch in the dynasty."""
        pass  # TODO: Implement family creation