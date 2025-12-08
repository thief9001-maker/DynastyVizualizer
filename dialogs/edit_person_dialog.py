"""Dialog for editing an existing person."""

from PySide6.QtWidgets import QDialog


class EditPersonDialog(QDialog):
    """Dialog for editing an existing person's data."""

    def __init__(self, parent: 'MainWindow', person_id: int) -> None:  # type: ignore
        """Initialize the edit person dialog."""
        super().__init__(parent)
        self.person_id = person_id
        # TODO: Implement dialog UI
        # TODO: Load existing person data
        # TODO: Add form fields
        # TODO: Add validation logic
        pass
