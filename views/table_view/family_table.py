"""Table view for listing all families in the database."""

from PySide6.QtWidgets import QTableWidget


class FamilyTable(QTableWidget):
    """Sortable, filterable table of all families."""

    def __init__(self, database_connection) -> None:
        """Initialize the family table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Family Name, Member Count, Start Year, etc.)
        # TODO: Load all families from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add double-click handler to show family details
        # TODO: Add right-click menu (edit/view members)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all families
        # TODO: Repopulate table
        pass
