"""Dialog for creating a new marriage."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel,
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
        
        form = QFormLayout()
        
        # Person 1 (current person - read-only display)
        person1_label = QLabel(f"<b>{self.person.display_name}</b>")
        form.addRow("Person 1:", person1_label)
        
        # Person 2 (spouse - searchable)
        self.spouse_selector = PersonSelector(self.db_manager)
        form.addRow("Person 2:", self.spouse_selector)
        
        # Marriage date
        self.marriage_date = DatePicker()
        self.marriage_date.set_date(1721, None)
        form.addRow("Marriage Date:", self.marriage_date)
        
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
        spouse_id = self.spouse_selector.get_person_id()
        
        if not spouse_id:
            QMessageBox.warning(self, "Validation Error", "Please select a spouse.")
            return
        
        if spouse_id == self.person.id:
            QMessageBox.warning(self, "Validation Error", "A person cannot marry themselves.")
            return
        
        year, month = self.marriage_date.get_date()
        
        self.spouse_id = spouse_id
        self.marriage_year = year
        self.marriage_month = month
        
        self.accept()
    
    def get_marriage_data(self) -> tuple[int | None, int | None, int | None]:
        """Returns (spouse_id, year, month)."""
        return (self.spouse_id, self.marriage_year, self.marriage_month)