"""Person box widget for the tree view."""

from PySide6.QtWidgets import QGraphicsWidget


class PersonBox(QGraphicsWidget):
    """Visual representation of a person in the family tree."""

    def __init__(self, person_id: int) -> None:
        """Initialize the person box widget."""
        super().__init__()
        self.person_id = person_id
        # TODO: Add portrait display
        # TODO: Add name label
        # TODO: Add dates label
        # TODO: Add gear icon button
        # TODO: Implement drag functionality
        # TODO: Implement click handlers
        pass
