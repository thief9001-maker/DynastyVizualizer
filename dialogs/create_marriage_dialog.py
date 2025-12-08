"""Dialog for creating a new marriage between two people."""

from PySide6.QtWidgets import QDialog


class CreateMarriageDialog(QDialog):
    """Dialog for creating a marriage relationship."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the create marriage dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add PersonSelector widgets for husband/wife
        # TODO: Add DatePicker for marriage date
        # TODO: Add marriage_type dropdown (optional)
        # TODO: Add validation logic
        # TODO: Connect to CreateMarriageCommand
        pass
