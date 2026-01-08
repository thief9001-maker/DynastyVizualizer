"""Handles settings menu actions for various configuration options."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from main import MainWindow


class SettingsActions:
    """Handles settings menu actions for various configuration options."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Message Box Titles
    MSG_TITLE_NOT_IMPLEMENTED: str = "Not Yet Implemented"
    
    # Message Box Text
    MSG_TEXT_SETTINGS: str = "Settings dialog coming soon!"
    MSG_TEXT_GENERAL: str = "General settings coming soon!"
    MSG_TEXT_SHORTCUTS: str = "Shortcuts configuration coming soon!"
    MSG_TEXT_DISPLAY: str = "Display settings coming soon!"
    MSG_TEXT_APPEARANCE: str = "Appearance settings coming soon!"
    MSG_TEXT_FORMATS: str = "Format settings coming soon!"
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, parent: MainWindow) -> None:
        """Initialize settings actions handler."""
        self.parent: MainWindow = parent
    
    # ------------------------------------------------------------------
    # Settings Actions
    # ------------------------------------------------------------------
    
    def settings(self) -> None:
        """Open settings dialog to modify application settings."""
        self._show_not_implemented(self.MSG_TEXT_SETTINGS)
    
    def general(self) -> None:
        """Open general settings tab."""
        self._show_not_implemented(self.MSG_TEXT_GENERAL)
    
    def shortcuts(self) -> None:
        """Open shortcuts settings tab."""
        self._show_not_implemented(self.MSG_TEXT_SHORTCUTS)
    
    def display(self) -> None:
        """Open display settings tab."""
        self._show_not_implemented(self.MSG_TEXT_DISPLAY)
    
    def appearance(self) -> None:
        """Open appearance settings tab."""
        self._show_not_implemented(self.MSG_TEXT_APPEARANCE)
    
    def formats(self) -> None:
        """Open formats settings tab."""
        self._show_not_implemented(self.MSG_TEXT_FORMATS)
    
    # ------------------------------------------------------------------
    # UI Helpers
    # ------------------------------------------------------------------
    
    def _show_not_implemented(self, message: str) -> None:
        """Show a 'not yet implemented' message dialog."""
        QMessageBox.information(
            self.parent,
            self.MSG_TITLE_NOT_IMPLEMENTED,
            message
        )