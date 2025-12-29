"""Dialog for creating a new marriage."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QDialogButtonBox, QWidget, QMessageBox
)

from database.db_manager import DatabaseManager
from models.person import Person
from widgets.person_selector import PersonSelector
from widgets.date_picker import DatePicker


class CreateMarriageDialog(QDialog):
    """Dialog for creating a new marriage relationship."""
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person = person
        self.spouse_id: int | None = None
        self.marriage_year: int | None = None
        self.marriage_month: int | None = None
        
        self.setWindowTitle("Create Marriage")
        self.setMinimumWidth(450)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        # Person 1
        person1_layout = QHBoxLayout()
        person1_layout.addWidget(QLabel("Person 1:"))
        person1_label = QLabel(f"<b>{self.person.display_name}</b>")
        person1_layout.addWidget(person1_label)
        person1_layout.addStretch()
        layout.addLayout(person1_layout)
        
        # Person 2
        person2_layout = QHBoxLayout()
        person2_layout.addWidget(QLabel("Person 2:"))
        self.spouse_selector = PersonSelector(self.db_manager)
        person2_layout.addWidget(self.spouse_selector)
        layout.addLayout(person2_layout)
        
        # Date Unknown checkbox
        date_unknown_layout = QHBoxLayout()
        date_unknown_layout.addSpacing(85)  # Align with fields above
        self.date_unknown_check = QCheckBox("Date Unknown")
        self.date_unknown_check.setChecked(True)
        self.date_unknown_check.stateChanged.connect(self._on_date_unknown_toggled)
        date_unknown_layout.addWidget(self.date_unknown_check)
        date_unknown_layout.addStretch()
        layout.addLayout(date_unknown_layout)
        
        # Marriage date
        marriage_date_layout = QHBoxLayout()
        self.marriage_date_label = QLabel("Marriage Date:")
        marriage_date_layout.addWidget(self.marriage_date_label)
        self.marriage_date = DatePicker()
        self.marriage_date.set_date(1721, 1)
        self.marriage_date.unknown_check.setVisible(False)
        marriage_date_layout.addWidget(self.marriage_date)
        marriage_date_layout.addStretch()
        layout.addLayout(marriage_date_layout)
        
        layout.addStretch()
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self._update_date_visibility()
    
    def _on_date_unknown_toggled(self) -> None:
        """Handle date unknown checkbox toggle."""
        self._update_date_visibility()
    
    def _update_date_visibility(self) -> None:
        """Show/hide marriage date based on checkbox."""
        date_known = not self.date_unknown_check.isChecked()
        self.marriage_date_label.setVisible(date_known)
        self.marriage_date.setVisible(date_known)
    
    def _handle_accept(self) -> None:
        """Validate and accept."""
        spouse_id = self.spouse_selector.get_person_id()
        
        if not spouse_id:
            QMessageBox.warning(self, "Validation Error", "Please select a spouse.")
            return
        
        if spouse_id == self.person.id:
            QMessageBox.warning(self, "Validation Error", "A person cannot marry themselves.")
            return
        
        # Only get date if Date Unknown is NOT checked
        if self.date_unknown_check.isChecked():
            # Explicitly set to None - date is unknown
            self.spouse_id = spouse_id
            self.marriage_year = None
            self.marriage_month = None
        else:
            # Get date from picker
            year, month = self.marriage_date.get_date()
            self.spouse_id = spouse_id
            self.marriage_year = year
            self.marriage_month = month
        
        self.accept()
    
    def get_marriage_data(self) -> tuple[int | None, int | None, int | None]:
        """Returns (spouse_id, year, month)."""
        return (self.spouse_id, self.marriage_year, self.marriage_month)