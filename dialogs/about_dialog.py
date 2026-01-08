"""About dialog showing application information."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from main import MainWindow


class AboutDialog(QDialog):
    """Dialog displaying application information and credits."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE: str = "About Dynasty Visualizer"
    WINDOW_MIN_WIDTH: int = 400
    
    # Text Content
    APP_NAME: str = "Dynasty Visualizer"
    APP_VERSION: str = "0.2.0"
    APP_DESCRIPTION: str = "A genealogy tracking application for Ostriv settlements"
    AUTHOR: str = "Created by Alex"
    COPYRIGHT: str = "© 2025"
    GITHUB_LINK: str = "<a href='https://github.com/yourusername/dynasty-visualizer'>GitHub Repository</a>"
    
    # HTML Content
    ABOUT_TEXT_FORMAT: str = (
        "<center>"
        "<h2>{app_name}</h2>"
        "<p><b>Version:</b> {version}</p>"
        "<p>{description}</p>"
        "<p>{author}</p>"
        "<p>{copyright}</p>"
        "<p>{github}</p>"
        "</center>"
    )
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, parent: MainWindow) -> None:
        """Initialize the about dialog."""
        super().__init__(parent)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create dialog UI."""
        layout: QVBoxLayout = QVBoxLayout(self)
        
        about_text: str = self._create_about_text()
        about_label: QLabel = QLabel(about_text)
        about_label.setTextFormat(Qt.TextFormat.RichText)
        about_label.setOpenExternalLinks(True)
        about_label.setWordWrap(True)
        
        layout.addWidget(about_label)
        
        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
    
    def _create_about_text(self) -> str:
        """Create formatted about text."""
        return self.ABOUT_TEXT_FORMAT.format(
            app_name=self.APP_NAME,
            version=self.APP_VERSION,
            description=self.APP_DESCRIPTION,
            author=self.AUTHOR,
            copyright=self.COPYRIGHT,
            github=self.GITHUB_LINK
        )