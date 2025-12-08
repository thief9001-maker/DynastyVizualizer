"""Widget for displaying and managing person portraits."""

from PySide6.QtWidgets import QWidget


class PortraitGallery(QWidget):
    """Gallery widget for viewing and selecting portraits."""

    def __init__(self, person_id: int) -> None:
        """Initialize the portrait gallery widget."""
        super().__init__()
        self.person_id = person_id
        # TODO: Load portraits from Portrait table
        # TODO: Display portraits in grid layout
        # TODO: Add portrait selection highlighting
        # TODO: Add upload new portrait button
        # TODO: Add delete portrait button
        # TODO: Emit signal on portrait selection
        pass
