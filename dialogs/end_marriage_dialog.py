"""Dialog for ending a marriage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QDialogButtonBox, QWidget, QMessageBox
)

if TYPE_CHECKING:
    from models.marriage import Marriage

from widgets.date_picker import DatePicker


class EndMarriageDialog(QDialog):
    """Dialog for ending a marriage with date and reason."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE: str = "End Marriage"
    WINDOW_MIN_WIDTH: int = 400
    
    # Labels
    LABEL_END_DATE: str = "End Date:"
    LABEL_REASON: str = "Reason:"
    
    # Dissolution Reasons
    REASON_DEATH: str = "Death"
    REASON_DIVORCE: str = "Divorce"
    REASON_ANNULMENT: str = "Annulment"
    REASON_OTHER: str = "Other"
    REASON_UNKNOWN: str = "Unknown"
    
    # Message Box Titles
    MSG_TITLE_VALIDATION_ERROR: str = "Validation Error"
    MSG_TITLE_INVALID_DATE: str = "Invalid Date"
    
    # Message Box Text
    MSG_TEXT_YEAR_REQUIRED: str = "End date year is required."
    MSG_TEXT_END_BEFORE_START: str = "Marriage cannot end before it started."
    
    # Default Values
    DEFAULT_YEAR: int = 1721
    DEFAULT_MONTH: int | None = None
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, marriage: Marriage, parent: QWidget | None = None) -> None:
        """Initialize end marriage dialog."""
        super().__init__(parent)
        
        self.marriage: Marriage = marriage
        self.dissolution_year: int | None = None
        self.dissolution_month: int | None = None
        self.dissolution_reason: str = ""
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout: QVBoxLayout = QVBoxLayout(self)
        
        form: QFormLayout = self._create_form_layout()
        layout.addLayout(form)
        
        button_box: QDialogButtonBox = self._create_button_box()
        layout.addWidget(button_box)
    
    def _create_form_layout(self) -> QFormLayout:
        """Create form with end date and reason fields."""
        form: QFormLayout = QFormLayout()
        
        self._create_end_date_field(form)
        self._create_reason_field(form)
        
        return form
    
    def _create_end_date_field(self, form: QFormLayout) -> None:
        """Create end date picker field."""
        self.end_date: DatePicker = DatePicker()
        
        if self.marriage.marriage_year:
            self._set_date_constraints_from_marriage()
        else:
            self.end_date.set_date(self.DEFAULT_YEAR, self.DEFAULT_MONTH)
        
        self.end_date.unknown_check.setChecked(False)
        
        form.addRow(self.LABEL_END_DATE, self.end_date)

    def _set_date_constraints_from_marriage(self) -> None:
        """Set date picker constraints based on marriage start date."""
        self.end_date.set_min_date(
            self.marriage.marriage_year,  # type: ignore[arg-type]
            self.marriage.marriage_month
        )
        self.end_date.set_date(
            self.marriage.marriage_year,  # type: ignore[arg-type]
            self.marriage.marriage_month
        )
        
    def _create_reason_field(self, form: QFormLayout) -> None:
        """Create dissolution reason dropdown."""
        self.reason_combo: QComboBox = QComboBox()
        self.reason_combo.addItems([
            self.REASON_DEATH,
            self.REASON_DIVORCE,
            self.REASON_ANNULMENT,
            self.REASON_OTHER,
            self.REASON_UNKNOWN
        ])
        form.addRow(self.LABEL_REASON, self.reason_combo)
    
    def _create_button_box(self) -> QDialogButtonBox:
        """Create dialog button box."""
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        return button_box
    
    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------
    
    def _handle_accept(self) -> None:
        """Validate and accept."""
        if not self._validate_inputs():
            return
        
        self._collect_dissolution_data()
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate all input fields."""
        year, month = self.end_date.get_date()
        
        if not self._validate_year_exists(year):
            return False
        
        if not self._validate_end_after_start(year, month):
            return False
        
        return True
    
    def _validate_year_exists(self, year: int | None) -> bool:
        """Validate that year is provided."""
        if not year:
            QMessageBox.warning(
                self,
                self.MSG_TITLE_VALIDATION_ERROR,
                self.MSG_TEXT_YEAR_REQUIRED
            )
            return False
        
        return True
    
    def _validate_end_after_start(self, year: int, month: int | None) -> bool:
        """Validate end date is after marriage start date."""
        if not self.marriage.marriage_year:
            return True
        
        if year < self.marriage.marriage_year:
            self._show_invalid_date_error()
            return False
        
        if self._is_same_year_but_earlier_month(year, month):
            self._show_invalid_date_error()
            return False
        
        return True
    
    def _is_same_year_but_earlier_month(self, year: int, month: int | None) -> bool:
        """Check if end date is same year but earlier month than start."""
        if year != self.marriage.marriage_year:
            return False
        
        if not self.marriage.marriage_month or not month:
            return False
        
        return month < self.marriage.marriage_month
    
    def _show_invalid_date_error(self) -> None:
        """Show error for invalid date range."""
        QMessageBox.warning(
            self,
            self.MSG_TITLE_INVALID_DATE,
            self.MSG_TEXT_END_BEFORE_START
        )
    
    # ------------------------------------------------------------------
    # Data Collection
    # ------------------------------------------------------------------
    
    def _collect_dissolution_data(self) -> None:
        """Collect dissolution data from input fields."""
        year, month = self.end_date.get_date()
        
        self.dissolution_year = year
        self.dissolution_month = month
        self.dissolution_reason = self.reason_combo.currentText()
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_dissolution_data(self) -> tuple[int | None, int | None, str]:
        """Returns (year, month, reason)."""
        return (self.dissolution_year, self.dissolution_month, self.dissolution_reason)