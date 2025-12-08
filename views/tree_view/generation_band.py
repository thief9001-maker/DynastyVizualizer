"""Horizontal band showing a generation level in the tree."""

from PySide6.QtWidgets import QGraphicsWidget


class GenerationBand(QGraphicsWidget):
    """Background band for highlighting a generation level."""

    def __init__(self, generation: int, y_position: float, height: float) -> None:
        """Initialize the generation band widget."""
        super().__init__()
        self.generation = generation
        self.y_position = y_position
        self.height = height
        # TODO: Draw horizontal background rectangle
        # TODO: Use alternating colors for visual separation
        # TODO: Add generation label on left side
        # TODO: Update position when tree layout changes
        pass

    def update_position(self, new_y: float, new_height: float) -> None:
        """Adjust band position and height."""
        # TODO: Update y_position and height
        # TODO: Redraw band
        pass
