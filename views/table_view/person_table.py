"""Table view for listing all people in the database."""

from PySide6.QtWidgets import QTableWidget


class PersonTable(QTableWidget):
    """Sortable, filterable table of all people."""

    def __init__(self, database_connection) -> None:
        """Initialize the person table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Name, Gender, Birth, Death, etc.)
        # TODO: Load all people from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add row selection highlighting
        # TODO: Add double-click handler to show person details
        # TODO: Add right-click menu (edit/delete)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all people
        # TODO: Repopulate table
        pass
