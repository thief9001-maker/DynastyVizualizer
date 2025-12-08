"""Visual representation of a marriage in the tree view."""

from PySide6.QtWidgets import QGraphicsWidget


class MarriageNode(QGraphicsWidget):
    """Node connecting spouses in the family tree."""

    def __init__(self, marriage_id: int) -> None:
        """Initialize the marriage node widget."""
        super().__init__()
        self.marriage_id = marriage_id
        # TODO: Draw small connector shape (circle/diamond)
        # TODO: Display marriage date on hover
        # TODO: Connect to both spouse PersonBox widgets
        # TODO: Add click handler to show marriage details
        # TODO: Add right-click menu (edit/end/delete marriage)
        pass
