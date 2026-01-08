"""Handles file menu actions (New, Open, Save, Exit)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog, QMessageBox

if TYPE_CHECKING:
    from main import MainWindow


class FileActions:
    """Handles file menu actions (New, Open, Save, Exit)."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # File Filters
    FILE_FILTER_DYNASTY: str = "Dynasty Files (*.dyn)"
    
    # Dialog Titles
    DIALOG_TITLE_OPEN: str = "Open Dynasty File"
    DIALOG_TITLE_SAVE_AS: str = "Save Dynasty File As"
    
    # Message Box Titles
    MSG_TITLE_ERROR: str = "Error"
    MSG_TITLE_UNSAVED_CHANGES: str = "Unsaved Changes"
    MSG_TITLE_FILE_NOT_FOUND: str = "File Not Found"
    MSG_TITLE_ERROR_OPENING: str = "Error Opening Database"
    MSG_TITLE_ERROR_SAVING: str = "Error Saving Database"
    
    # Message Box Text
    MSG_TEXT_NO_DATABASE: str = "No database is currently open."
    MSG_TEXT_UNSAVED_NEW: str = "You have unsaved changes. Do you want to save before creating a new dynasty?"
    MSG_TEXT_UNSAVED_EXIT: str = "You have unsaved changes. Do you want to save before exiting?"
    MSG_TEXT_FILE_NOT_FOUND: str = "The file '{path}' does not exist."
    MSG_TEXT_OPEN_ERROR: str = "Failed to open dynasty file:\n{error}"
    MSG_TEXT_SAVE_ERROR: str = "Failed to save dynasty file:\n{error}"
    
    # Default Values
    DEFAULT_PATH_EMPTY: str = ""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, parent: MainWindow) -> None:
        """Initialize file actions handler."""
        self.parent: MainWindow = parent
    
    # ------------------------------------------------------------------
    # Database Validation
    # ------------------------------------------------------------------
    
    def _ensure_db(self) -> bool:
        """Check if a database is currently open."""
        if not hasattr(self.parent, 'db'):
            self._show_error(self.MSG_TITLE_ERROR, self.MSG_TEXT_NO_DATABASE)
            return False
        
        if not self.parent.db.is_open:
            self._show_error(self.MSG_TITLE_ERROR, self.MSG_TEXT_NO_DATABASE)
            return False
        
        return True
    
    # ------------------------------------------------------------------
    # File Dialog Helpers
    # ------------------------------------------------------------------
    
    def _get_save_path(self, title: str, default_name: str = "") -> str | None:
        """Show a save file dialog and return the chosen path."""
        default_path: str = self._build_save_default_path(default_name)
        
        path, _ = QFileDialog.getSaveFileName(
            self.parent,
            title,
            default_path,
            self.FILE_FILTER_DYNASTY
        )
        
        return path if path else None
    
    def _build_save_default_path(self, default_name: str) -> str:
        """Build default path for save dialog."""
        if default_name:
            return default_name
        
        if self.parent.db.database_directory:
            return self.parent.db.database_directory
        
        return self.DEFAULT_PATH_EMPTY
    
    def _get_open_path(self, title: str) -> str | None:
        """Show an open file dialog and return the chosen path."""
        default_dir: str = self._get_default_open_directory()
        
        path, _ = QFileDialog.getOpenFileName(
            self.parent,
            title,
            default_dir,
            self.FILE_FILTER_DYNASTY
        )
        
        return path if path else None
    
    def _get_default_open_directory(self) -> str:
        """Get default directory for open dialog."""
        if not self.parent.db.is_open:
            return self.DEFAULT_PATH_EMPTY
        
        if not self.parent.db.database_directory:
            return self.DEFAULT_PATH_EMPTY
        
        return self.parent.db.database_directory
    
    # ------------------------------------------------------------------
    # UI Helpers
    # ------------------------------------------------------------------
    
    def _show_error(self, title: str, message: str) -> None:
        """Display an error message dialog."""
        QMessageBox.critical(self.parent, title, message)
    
    def _refresh_all_views(self) -> None:
        """Refresh all active views with new database data."""
        if self.parent.data_table_view:
            self.parent.data_table_view.refresh_data()
    
    # ------------------------------------------------------------------
    # Unsaved Changes Handling
    # ------------------------------------------------------------------
    
    def _prompt_save_before_new(self) -> bool:
        """Prompt to save changes before creating new database."""
        if not self.parent.db.is_dirty:
            return True
        
        reply = self._show_unsaved_changes_dialog(self.MSG_TEXT_UNSAVED_NEW)
        
        if reply == QMessageBox.StandardButton.Cancel:
            return False
        
        if reply == QMessageBox.StandardButton.Save:
            return self.save()
        
        return True
    
    def _show_unsaved_changes_dialog(self, message: str) -> QMessageBox.StandardButton:
        """Show dialog for unsaved changes with Save/Discard/Cancel options."""
        reply = QMessageBox.question(
            self.parent,
            self.MSG_TITLE_UNSAVED_CHANGES,
            message,
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        return reply
    
    # ------------------------------------------------------------------
    # Recent Files Management
    # ------------------------------------------------------------------
    
    def _add_to_recent_files(self, path: str | None) -> None:
        """Add file path to recent files list."""
        if not path:
            return
        
        self.parent.settings_manager.add_recent_file(path)
        self.parent._update_recent_files_menu()
    
    # ------------------------------------------------------------------
    # File Operations
    # ------------------------------------------------------------------
    
    def new_dynasty(self) -> None:
        """Create a new untitled dynasty database."""
        if not self._prompt_save_before_new():
            return
        
        self.parent.db.close()
        self.parent._create_untitled_database()
        self.parent.refresh_ui()
        self._refresh_all_views()
        self.parent._show_family_trees()
    
    def open_dynasty(self) -> None:
        """Prompt user to open an existing dynasty database file."""
        path: str | None = self._get_open_path(self.DIALOG_TITLE_OPEN)
        
        if not path:
            return
        
        self._attempt_open_database(path)
    
    def _attempt_open_database(self, path: str) -> None:
        """Attempt to open database file and handle errors."""
        try:
            self._open_database_success(path)
        except FileNotFoundError:
            self._show_file_not_found_error(path)
        except Exception as e:
            self._show_open_error(e)
    
    def _open_database_success(self, path: str) -> None:
        """Handle successful database open."""
        self.parent.db.open_database(path)
        self.parent.refresh_ui()
        self._refresh_all_views()
        self._add_to_recent_files(path)
    
    def _show_file_not_found_error(self, path: str) -> None:
        """Show error when file is not found."""
        self._show_error(
            self.MSG_TITLE_FILE_NOT_FOUND,
            self.MSG_TEXT_FILE_NOT_FOUND.format(path=path)
        )
    
    def _show_open_error(self, error: Exception) -> None:
        """Show error when opening database fails."""
        self._show_error(
            self.MSG_TITLE_ERROR_OPENING,
            self.MSG_TEXT_OPEN_ERROR.format(error=str(error))
        )
    
    def save(self) -> bool:
        """Save current database, falling back to save_as if no path set."""
        if not self._ensure_db():
            return False
        
        if not self.parent.db.has_file_path:
            return self.save_as()
        
        return self._attempt_save_database()
    
    def _attempt_save_database(self, path: str | None = None) -> bool:
        """Attempt to save database and handle errors."""
        try:
            return self._save_database_success(path)
        except Exception as e:
            self._show_save_error(e)
            return False
    
    def _save_database_success(self, path: str | None = None) -> bool:
        """Handle successful database save."""
        result: bool = self.parent.db.save_database(path) 
        
        if not result:
            return False
        
        self.parent.refresh_ui()
        self._add_to_recent_files(self.parent.db.file_path)
        
        return True
    
    def _show_save_error(self, error: Exception) -> None:
        """Show error when saving database fails."""
        self._show_error(
            self.MSG_TITLE_ERROR_SAVING,
            self.MSG_TEXT_SAVE_ERROR.format(error=str(error))
        )
    
    def save_as(self) -> bool:
        """Prompt user to save database to a new file."""
        if not self._ensure_db():
            return False
        
        default_name: str = self.parent.db.database_name or self.DEFAULT_PATH_EMPTY
        path: str | None = self._get_save_path(self.DIALOG_TITLE_SAVE_AS, default_name)
        
        if not path:
            return False
        
        return self._attempt_save_database(path)
    
    def exit_app(self) -> None:
        """Prompt to save unsaved changes before closing application."""
        if not self._check_exit_conditions():
            return
        
        self.parent.close()
    
    def _check_exit_conditions(self) -> bool:
        """Check if application can exit, prompting for save if needed."""
        if not self._has_unsaved_changes():
            return True
        
        return self._prompt_save_before_exit()
    
    def _has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes."""
        db = self.parent.db
        return db.is_open and db.is_dirty
    
    def _prompt_save_before_exit(self) -> bool:
        """Prompt to save changes before exiting."""
        choice = self._show_unsaved_changes_dialog(self.MSG_TEXT_UNSAVED_EXIT)
        
        if choice == QMessageBox.StandardButton.Cancel:
            return False
        
        if choice == QMessageBox.StandardButton.Save:
            return self.save()
        
        return True