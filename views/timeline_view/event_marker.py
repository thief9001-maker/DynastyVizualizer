"""Visual marker for person events on timeline."""

from PySide6.QtWidgets import QGraphicsWidget


class EventMarker(QGraphicsWidget):
    """Small marker showing an event on a person's timeline bar."""

    def __init__(self, event_id: int) -> None:
        """Initialize the event marker widget."""
        super().__init__()
        self.event_id = event_id
        # TODO: Load event data from database
        # TODO: Draw small icon/shape at event year
        # TODO: Use different colors for event types
        # TODO: Add tooltip showing event details
        # TODO: Add click handler for event editing
        pass
