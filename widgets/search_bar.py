"""Search bar widget for finding people by name."""

from PySide6.QtWidgets import QWidget


class SearchBar(QWidget):
    """Search widget with autocomplete for finding people."""

    def __init__(self) -> None:
        """Initialize the search bar widget."""
        super().__init__()
        # TODO: Add QLineEdit for search input
        # TODO: Implement autocomplete using QCompleter
        # TODO: Load all person names from database
        # TODO: Add search icon/button
        # TODO: Add clear button
        # TODO: Emit signal when person is selected
        # TODO: Support fuzzy matching (optional)
        pass

    def update_completions(self) -> None:
        """Refresh autocomplete list from database."""
        # TODO: Reload all person names
        # TODO: Update QCompleter model
        pass
