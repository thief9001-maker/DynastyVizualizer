"""Visual marker for major historical events."""

from PySide6.QtWidgets import QGraphicsWidget


class MajorEventMarker(QGraphicsWidget):
    """Vertical line showing major events across all families."""

    def __init__(self, major_event_id: int) -> None:
        """Initialize the major event marker widget."""
        super().__init__()
        self.major_event_id = major_event_id
        # TODO: Load major event data from database
        # TODO: Draw vertical line at event year
        # TODO: Add event name label
        # TODO: Use distinctive color/style
        # TODO: Add tooltip with event description
        # TODO: Add click handler for editing
        pass
