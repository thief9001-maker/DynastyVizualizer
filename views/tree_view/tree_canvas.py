"""Main canvas for displaying the family tree."""

from PySide6.QtWidgets import QGraphicsView


class TreeCanvas(QGraphicsView):
    """Scrollable, zoomable canvas for displaying the family tree."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the tree canvas."""
        super().__init__(parent)
        # TODO: Create QGraphicsScene
        # TODO: Implement zoom functionality
        # TODO: Implement pan functionality
        # TODO: Add minimap (optional)
        pass
