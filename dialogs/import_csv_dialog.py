"""Dialog for importing genealogy data from CSV files."""

from PySide6.QtWidgets import QDialog


class ImportCSVDialog(QDialog):
    """Dialog for CSV import configuration and mapping."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the CSV import dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add file picker for CSV selection
        # TODO: Add column mapping controls
        # TODO: Add preview table
        # TODO: Add import mode selection (replace/merge)
        # TODO: Add progress bar
        # TODO: Connect to CSVImporter utility
        pass
