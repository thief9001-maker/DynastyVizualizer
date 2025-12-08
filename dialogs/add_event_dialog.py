"""Dialog for adding a new event to a person."""

from PySide6.QtWidgets import QDialog


class AddEventDialog(QDialog):
    """Dialog for creating a new event entry."""

    def __init__(self, parent: 'MainWindow', person_id: int | None = None) -> None:  # type: ignore
        """Initialize the add event dialog."""
        super().__init__(parent)
        self.person_id = person_id
        # TODO: Implement dialog UI
        # TODO: Add PersonSelector widget (pre-filled if person_id provided)
        # TODO: Add event type dropdown
        # TODO: Add DatePicker for event date
        # TODO: Add description text field
        # TODO: Add validation logic
        # TODO: Connect to AddEventCommand
        pass
