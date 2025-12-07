from PySide6.QtWidgets import QFileDialog, QMessageBox


class FileActions:
    """Handles file menu actions (New, Open, Save, Exit)."""
    
    FILE_FILTER = "Dynasty Files (*.dyn)"
    
    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize file actions handler."""
        self.parent = parent
    
    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------
    
    def _ensure_db(self) -> bool:
        """Check if a database is currently open."""
        if not hasattr(self.parent, 'db') or not self.parent.db.is_open:
            self._show_error("Error", "No database is currently open.")
            return False
        return True
    
    def _get_save_path(self, title: str, default_name: str = "") -> str | None:
        """Show a save file dialog and return the chosen path."""
        default_path = ""
        if default_name:
            default_path = default_name
        elif self.parent.db.database_directory:
            default_path = self.parent.db.database_directory
        
        path, _ = QFileDialog.getSaveFileName(
            self.parent,
            title,
            default_path,
            self.FILE_FILTER
        )
        return path if path else None
    
    def _get_open_path(self, title: str) -> str | None:
        """Show an open file dialog and return the chosen path."""
        default_dir = ""
        if self.parent.db.is_open and self.parent.db.database_directory:
            default_dir = self.parent.db.database_directory
        
        path, _ = QFileDialog.getOpenFileName(
            self.parent,
            title,
            default_dir,
            self.FILE_FILTER
        )
        return path if path else None
    
    def _show_error(self, title: str, message: str) -> None:
        """Display an error message dialog."""
        QMessageBox.critical(self.parent, title, message)
    
    # ------------------------------------------------------------------
    # File Operations
    # ------------------------------------------------------------------
    
    def new_dynasty(self) -> None:
        """Prompt user to create a new dynasty database file."""
        path = self._get_save_path("Create New Dynasty File")
        if not path:
            return
        
        try:
            self.parent.db.new_database(path)
            self.parent.refresh_ui()
        except Exception as e:
            self._show_error(
                "Error Creating Database",
                f"Failed to create dynasty file:\n{str(e)}"
            )
    
    def open_dynasty(self) -> None:
        """Prompt user to open an existing dynasty database file."""
        path = self._get_open_path("Open Dynasty File")
        if not path:
            return
        
        try:
            self.parent.db.open_database(path)
            self.parent.refresh_ui()
        except FileNotFoundError:
            self._show_error(
                "File Not Found",
                f"The file '{path}' does not exist."
            )
        except Exception as e:
            self._show_error(
                "Error Opening Database",
                f"Failed to open dynasty file:\n{str(e)}"
            )
    
    def save(self) -> bool:
        """Save current database, falling back to save_as if no path set."""
        if not self._ensure_db():
            return False
        
        if not self.parent.db.has_file_path:
            return self.save_as()
        
        try:
            result = self.parent.db.save_database()
            if result:
                self.parent.refresh_ui()
            return result
        except Exception as e:
            self._show_error(
                "Error Saving Database",
                f"Failed to save dynasty file:\n{str(e)}"
            )
            return False
    
    def save_as(self) -> bool:
        """Prompt user to save database to a new file."""
        if not self._ensure_db():
            return False
        
        # Suggest current filename if it exists
        default_name = self.parent.db.database_name or ""
        path = self._get_save_path("Save Dynasty File As", default_name)
        if not path:
            return False
        
        try:
            self.parent.db.save_database(path)
            return True
        except Exception as e:
            self._show_error(
                "Error Saving Database",
                f"Failed to save dynasty file:\n{str(e)}"
            )
            return False
    
    def exit_app(self) -> None:
        """Prompt to save unsaved changes before closing application."""
        db = self.parent.db
        
        if db.is_open and db.is_dirty:
            msg = QMessageBox(self.parent)
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("You have unsaved changes. Do you want to save before exiting?")
            msg.setStandardButtons(
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            choice = msg.exec()
            
            if choice == QMessageBox.StandardButton.Save:
                if not self.save():
                    return
            elif choice == QMessageBox.StandardButton.Cancel:
                return
        
        self.parent.close()
