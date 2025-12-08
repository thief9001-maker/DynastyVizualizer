"""Table view for listing all marriages in the database."""

from PySide6.QtWidgets import QTableWidget


class MarriageTable(QTableWidget):
    """Sortable, filterable table of all marriages."""

    def __init__(self, database_connection) -> None:
        """Initialize the marriage table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Husband, Wife, Start Date, End Date, Type)
        # TODO: Load all marriages from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add clickable person names
        # TODO: Add double-click handler to show marriage details
        # TODO: Add right-click menu (edit/end/delete)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all marriages
        # TODO: Repopulate table
        pass
