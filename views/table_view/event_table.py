"""Table view for listing all events in the database."""

from PySide6.QtWidgets import QTableWidget


class EventTable(QTableWidget):
    """Sortable, filterable table of all events."""

    def __init__(self, database_connection) -> None:
        """Initialize the event table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Person, Event Type, Date, Description)
        # TODO: Load all events from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add clickable person names
        # TODO: Add double-click handler to show event details
        # TODO: Add right-click menu (edit/delete)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all events
        # TODO: Repopulate table
        pass
