"""Dialog for adding a new person."""

from PySide6.QtWidgets import QDialog


class AddPersonDialog(QDialog):
    """Dialog for creating a new person in the database."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the add person dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add form fields (name, gender, dates)
        # TODO: Add DatePicker widgets
        # TODO: Add validation logic
        pass
