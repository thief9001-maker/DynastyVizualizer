"""Widget for comparing statistics between families or people."""

from PySide6.QtWidgets import QWidget


class ComparisonWidget(QWidget):
    """Side-by-side comparison of selected entities."""

    def __init__(self, database_connection) -> None:
        """Initialize the comparison widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Add selectors for entities to compare
        # TODO: Display side-by-side statistics
        # TODO: Show comparison charts
        # TODO: Highlight differences
        # TODO: Support comparing families, people, or generations
        pass

    def set_comparison(self, entity1_id: int, entity2_id: int, entity_type: str) -> None:
        """Set which entities to compare."""
        # TODO: Load data for both entities
        # TODO: Calculate comparison metrics
        # TODO: Update display
        pass
