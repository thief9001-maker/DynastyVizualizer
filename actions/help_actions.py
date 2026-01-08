"""Handles help menu actions for application information."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from main import MainWindow


class HelpActions:
    """Handles help menu actions for application information."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Dialog Titles
    DIALOG_TITLE_ABOUT: str = "About Dynasty Visualizer"
    
    # Dialog Text
    DIALOG_TEXT_ABOUT: str = (
        "<h2>Dynasty Visualizer</h2>"
        "<p>Version 0.2.0</p>"
        "<p>A genealogy tracking application for Ostriv settlements.</p>"
        "<p>Created by Alex</p>"
        "<p>© 2025</p>"
    )
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, parent: MainWindow) -> None:
        """Initialize help actions handler."""
        self.parent: MainWindow = parent
    
    # ------------------------------------------------------------------
    # Help Actions
    # ------------------------------------------------------------------
    
    def about(self) -> None:
        """Display the about dialog with application information."""
        QMessageBox.about(
            self.parent,
            self.DIALOG_TITLE_ABOUT,
            self.DIALOG_TEXT_ABOUT
        )