"""Horizontal bar representing a family's timespan."""

from PySide6.QtWidgets import QGraphicsWidget


class FamilyBar(QGraphicsWidget):
    """Visual bar showing family existence over time."""

    def __init__(self, family_id: int) -> None:
        """Initialize the family bar widget."""
        super().__init__()
        self.family_id = family_id
        # TODO: Calculate family start year (earliest member birth)
        # TODO: Calculate family end year (latest member death or current)
        # TODO: Draw horizontal bar spanning timespan
        # TODO: Add family name label
        # TODO: Add click handler to show family details
        # TODO: Add PersonBar widgets for each family member
        pass
