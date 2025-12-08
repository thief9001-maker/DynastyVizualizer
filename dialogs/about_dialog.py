"""About dialog showing application information."""

from PySide6.QtWidgets import QDialog


class AboutDialog(QDialog):
    """Dialog displaying application information and credits."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the about dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add application name, version, credits
        # TODO: Add license information
        # TODO: Add GitHub link
        pass
