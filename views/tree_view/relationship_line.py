"""Visual line connecting related people in the tree."""

from PySide6.QtWidgets import QGraphicsWidget


class RelationshipLine(QGraphicsWidget):
    """Line connecting parent to child or spouse to spouse."""

    def __init__(
        self,
        start_person_id: int,
        end_person_id: int,
        line_type: str,  # "parent", "marriage", "sibling"
    ) -> None:
        """Initialize the relationship line widget."""
        super().__init__()
        self.start_person_id = start_person_id
        self.end_person_id = end_person_id
        self.line_type = line_type
        # TODO: Draw line between two PersonBox widgets
        # TODO: Use different styles for different line types
        # TODO: Update position when PersonBox moves
        # TODO: Add hover highlighting
        pass

    def update_endpoints(self) -> None:
        """Recalculate line position based on connected boxes."""
        # TODO: Get current positions of connected PersonBox widgets
        # TODO: Redraw line with new coordinates
        pass
