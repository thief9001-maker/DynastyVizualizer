"""Horizontal bar representing a person's lifespan."""

from PySide6.QtWidgets import QGraphicsWidget


class PersonBar(QGraphicsWidget):
    """Visual bar showing person's life from birth to death."""

    def __init__(self, person_id: int) -> None:
        """Initialize the person bar widget."""
        super().__init__()
        self.person_id = person_id
        # TODO: Load person data from database
        # TODO: Calculate x position from birth_year
        # TODO: Calculate width from birth_year to death_year (or current)
        # TODO: Draw horizontal bar with portrait thumbnail
        # TODO: Add name label
        # TODO: Add event markers along bar
        # TODO: Add click handler to show person details
        pass
