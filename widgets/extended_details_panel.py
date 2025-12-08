"""Panel widget for displaying detailed person information."""

from PySide6.QtWidgets import QWidget


class ExtendedDetailsPanel(QWidget):
    """Panel showing comprehensive person details and relationships."""

    def __init__(self, person_id: int | None = None) -> None:
        """Initialize the extended details panel."""
        super().__init__()
        self.person_id = person_id
        # TODO: Display full person information
        # TODO: Show all marriages with dates
        # TODO: Show all children with clickable links
        # TODO: Show all events in chronological order
        # TODO: Show portrait gallery
        # TODO: Add edit button for each section
        # TODO: Add relationship path calculator
        pass

    def set_person(self, person_id: int) -> None:
        """Update panel to show different person."""
        # TODO: Clear current display
        # TODO: Load new person data
        # TODO: Refresh all sections
        pass
