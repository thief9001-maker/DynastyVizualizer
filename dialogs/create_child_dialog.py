"""Dialog for creating a new child with parent selection."""

from PySide6.QtWidgets import QDialog


class CreateChildDialog(QDialog):
    """Dialog for creating a child of selected parents."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the create child dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add name input fields
        # TODO: Add PersonSelector widgets for father/mother
        # TODO: Add DatePicker for birth date
        # TODO: Add gender selection
        # TODO: Add validation logic
        # TODO: Connect to CreateChildCommand
        pass
