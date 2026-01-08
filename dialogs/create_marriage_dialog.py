"""Dialog for creating a new marriage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QDialogButtonBox, QWidget, QMessageBox
)

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from widgets.person_selector import PersonSelector
from widgets.date_picker import DatePicker


class CreateMarriageDialog(QDialog):
    """Dialog for creating a new marriage relationship."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE: str = "Create Marriage"
    WINDOW_MIN_WIDTH: int = 450
    
    # Labels
    LABEL_PERSON_1: str = "Person 1:"
    LABEL_PERSON_2: str = "Person 2:"
    LABEL_MARRIAGE_DATE: str = "Marriage Date:"
    
    # Checkboxes
    CHECKBOX_DATE_UNKNOWN: str = "Date Unknown"
    
    # Message Box Titles
    MSG_TITLE_VALIDATION_ERROR: str = "Validation Error"
    
    # Message Box Text
    MSG_TEXT_SELECT_SPOUSE: str = "Please select a spouse."
    MSG_TEXT_SELF_MARRIAGE: str = "A person cannot marry themselves."
    
    # Layout
    SPACING_ALIGNMENT: int = 85
    
    # Default Values
    DEFAULT_YEAR: int = 1721
    DEFAULT_MONTH: int = 1
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent: QWidget | None = None
    ) -> None:
        """Initialize create marriage dialog."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.person: Person = person
        self.spouse_id: int | None = None
        self.marriage_year: int | None = None
        self.marriage_month: int | None = None
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout: QVBoxLayout = QVBoxLayout(self)
        
        self._create_person_1_row(layout)
        self._create_person_2_row(layout)
        self._create_date_unknown_checkbox(layout)
        self._create_marriage_date_row(layout)
        
        layout.addStretch()
        
        self._create_button_box(layout)
        
        self._update_date_visibility()
    
    def _create_person_1_row(self, layout: QVBoxLayout) -> None:
        """Create person 1 display row."""
        person1_layout: QHBoxLayout = QHBoxLayout()
        person1_layout.addWidget(QLabel(self.LABEL_PERSON_1))
        
        person1_label: QLabel = QLabel(f"<b>{self.person.display_name}</b>")
        person1_layout.addWidget(person1_label)
        person1_layout.addStretch()
        
        layout.addLayout(person1_layout)
    
    def _create_person_2_row(self, layout: QVBoxLayout) -> None:
        """Create person 2 selector row."""
        person2_layout: QHBoxLayout = QHBoxLayout()
        person2_layout.addWidget(QLabel(self.LABEL_PERSON_2))
        
        self.spouse_selector: PersonSelector = PersonSelector(self.db_manager)
        person2_layout.addWidget(self.spouse_selector)
        
        layout.addLayout(person2_layout)
    
    def _create_date_unknown_checkbox(self, layout: QVBoxLayout) -> None:
        """Create date unknown checkbox."""
        date_unknown_layout: QHBoxLayout = QHBoxLayout()
        date_unknown_layout.addSpacing(self.SPACING_ALIGNMENT)
        
        self.date_unknown_check: QCheckBox = QCheckBox(self.CHECKBOX_DATE_UNKNOWN)
        self.date_unknown_check.setChecked(True)
        self.date_unknown_check.stateChanged.connect(self._on_date_unknown_toggled)
        date_unknown_layout.addWidget(self.date_unknown_check)
        date_unknown_layout.addStretch()
        
        layout.addLayout(date_unknown_layout)
    
    def _create_marriage_date_row(self, layout: QVBoxLayout) -> None:
        """Create marriage date picker row."""
        marriage_date_layout: QHBoxLayout = QHBoxLayout()
        
        self.marriage_date_label: QLabel = QLabel(self.LABEL_MARRIAGE_DATE)
        marriage_date_layout.addWidget(self.marriage_date_label)
        
        self.marriage_date: DatePicker = DatePicker()
        self.marriage_date.set_date(self.DEFAULT_YEAR, self.DEFAULT_MONTH)
        self.marriage_date.unknown_check.setVisible(False)
        marriage_date_layout.addWidget(self.marriage_date)
        marriage_date_layout.addStretch()
        
        layout.addLayout(marriage_date_layout)
    
    def _create_button_box(self, layout: QVBoxLayout) -> None:
        """Create dialog button box."""
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------
    
    def _on_date_unknown_toggled(self) -> None:
        """Handle date unknown checkbox toggle."""
        self._update_date_visibility()
    
    def _update_date_visibility(self) -> None:
        """Show/hide marriage date based on checkbox."""
        date_known: bool = not self.date_unknown_check.isChecked()
        self.marriage_date_label.setVisible(date_known)
        self.marriage_date.setVisible(date_known)
    
    def _handle_accept(self) -> None:
        """Validate and accept."""
        if not self._validate_inputs():
            return
        
        self._collect_marriage_data()
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate all input fields."""
        spouse_id: int | None = self.spouse_selector.get_person_id()
        
        if not spouse_id:
            QMessageBox.warning(
                self,
                self.MSG_TITLE_VALIDATION_ERROR,
                self.MSG_TEXT_SELECT_SPOUSE
            )
            return False
        
        if spouse_id == self.person.id:
            QMessageBox.warning(
                self,
                self.MSG_TITLE_VALIDATION_ERROR,
                self.MSG_TEXT_SELF_MARRIAGE
            )
            return False
        
        return True
    
    # ------------------------------------------------------------------
    # Data Collection
    # ------------------------------------------------------------------
    
    def _collect_marriage_data(self) -> None:
        """Collect marriage data from input fields."""
        self.spouse_id = self.spouse_selector.get_person_id()
        
        if self.date_unknown_check.isChecked():
            self.marriage_year = None
            self.marriage_month = None
        else:
            year, month = self.marriage_date.get_date()
            self.marriage_year = year
            self.marriage_month = month
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_marriage_data(self) -> tuple[int | None, int | None, int | None]:
        """Returns (spouse_id, year, month)."""
        return (self.spouse_id, self.marriage_year, self.marriage_month)