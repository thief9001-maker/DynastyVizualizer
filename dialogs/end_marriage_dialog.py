"""Dialog for ending a marriage."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QDialogButtonBox, QWidget, QMessageBox
)

from widgets.date_picker import DatePicker
from models.marriage import Marriage


class EndMarriageDialog(QDialog):
    """Dialog for ending a marriage with date and reason."""
    
    def __init__(self, marriage: Marriage, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.marriage = marriage
        self.dissolution_year: int | None = None
        self.dissolution_month: int | None = None
        self.dissolution_reason: str = ""
        
        self.setWindowTitle("End Marriage")
        self.setMinimumWidth(400)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # End date
        self.end_date = DatePicker()
        
        # Set minimum date to marriage start date
        if self.marriage.marriage_year:
            self.end_date.set_min_date(self.marriage.marriage_year, self.marriage.marriage_month)
            self.end_date.set_date(self.marriage.marriage_year, self.marriage.marriage_month)
        else:
            self.end_date.set_date(1721, None)
        
        form.addRow("End Date:", self.end_date)
        
        # Reason
        self.reason_combo = QComboBox()
        self.reason_combo.addItems(["Death", "Divorce", "Annulment", "Other", "Unknown"])
        form.addRow("Reason:", self.reason_combo)
        
        layout.addLayout(form)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def _handle_accept(self) -> None:
        """Validate and accept."""
        year, month = self.end_date.get_date()
        
        if not year:
            QMessageBox.warning(self, "Validation Error", "End date year is required.")
            return
        
        # Validate against marriage start date
        if self.marriage.marriage_year:
            if year < self.marriage.marriage_year:
                QMessageBox.warning(
                    self,
                    "Invalid Date",
                    "Marriage cannot end before it started."
                )
                return
            elif year == self.marriage.marriage_year and self.marriage.marriage_month and month:
                if month < self.marriage.marriage_month:
                    QMessageBox.warning(
                        self,
                        "Invalid Date",
                        "Marriage cannot end before it started."
                    )
                    return
        
        self.dissolution_year = year
        self.dissolution_month = month
        self.dissolution_reason = self.reason_combo.currentText()
        
        self.accept()
    
    def get_dissolution_data(self) -> tuple[int | None, int | None, str]:
        """Returns (year, month, reason)."""
        return (self.dissolution_year, self.dissolution_month, self.dissolution_reason)