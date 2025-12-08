"""Widget for selecting a person from the database."""

from PySide6.QtWidgets import QWidget


class PersonSelector(QWidget):
    """Searchable dropdown widget for selecting a person."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the person selector widget."""
        super().__init__(parent)
        # TODO: Add search field
        # TODO: Add dropdown list
        # TODO: Implement real-time filtering
        # TODO: Load people from database
        # TODO: Add get_selected_person() method
        pass
