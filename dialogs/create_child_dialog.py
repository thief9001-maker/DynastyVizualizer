"""Dialog for creating a new child."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QComboBox, QLabel, QDialogButtonBox, QWidget, QMessageBox, 
    QCheckBox, QFrame
)
from PySide6.QtCore import QSignalBlocker, Qt

from database.db_manager import DatabaseManager
from database.person_repository import PersonRepository
from models.person import Person
from widgets.person_selector import PersonSelector
from widgets.date_picker import DatePicker


class CreateChildDialog(QDialog):
    """Dialog for creating a new child with pre-filled parents."""
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        parent1: Person,
        parent2_id: int | None = None,
        parent_widget: QWidget | None = None
    ) -> None:
        super().__init__(parent_widget)
        
        self.db_manager = db_manager
        self.person_repo = PersonRepository(db_manager)
        self.parent1 = parent1
        self.parent2_id = parent2_id
        
        self.created_person: Person | None = None
        
        self.setWindowTitle("Create Child")
        self.setMinimumWidth(550)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        LABEL_WIDTH = 85  # Consistent label width for alignment
        
        # Parents header
        parents_header = QLabel("<b>Parents:</b>")
        layout.addWidget(parents_header)
        
        # Parent 1 (indented)
        parent1_layout = QHBoxLayout()
        parent1_layout.addSpacing(20)
        parent1_label_text = QLabel("Parent 1:")
        parent1_label_text.setMinimumWidth(LABEL_WIDTH)
        parent1_layout.addWidget(parent1_label_text)
        parent1_name = QLabel(f"<b>{self.parent1.display_name}</b>")
        parent1_layout.addWidget(parent1_name)
        parent1_layout.addStretch()
        layout.addLayout(parent1_layout)
        
        # Parent 2 (indented)
        parent2_layout = QHBoxLayout()
        parent2_layout.addSpacing(20)
        parent2_label_text = QLabel("Parent 2:")
        parent2_label_text.setMinimumWidth(LABEL_WIDTH)
        parent2_layout.addWidget(parent2_label_text)
        self.parent2_selector = PersonSelector(self.db_manager)
        if self.parent2_id:
            with QSignalBlocker(self.parent2_selector):
                self.parent2_selector.set_person(self.parent2_id)
        parent2_layout.addWidget(self.parent2_selector)
        layout.addLayout(parent2_layout)
        
        # Divider line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        # Child Information header
        child_header = QLabel("<b>Child Information:</b>")
        layout.addWidget(child_header)
        
        # First Name (indented)
        first_name_layout = QHBoxLayout()
        first_name_layout.addSpacing(20)
        first_name_label = QLabel("First Name: *")
        first_name_label.setMinimumWidth(LABEL_WIDTH)
        first_name_layout.addWidget(first_name_label)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Required")
        first_name_layout.addWidget(self.first_name_input)
        layout.addLayout(first_name_layout)
        
        # Last Name (indented)
        last_name_layout = QHBoxLayout()
        last_name_layout.addSpacing(20)
        last_name_label = QLabel("Last Name: *")
        last_name_label.setMinimumWidth(LABEL_WIDTH)
        last_name_layout.addWidget(last_name_label)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Required")
        self.last_name_input.setText(self.parent1.last_name)
        last_name_layout.addWidget(self.last_name_input)
        layout.addLayout(last_name_layout)
        
        # Gender (indented)
        gender_layout = QHBoxLayout()
        gender_layout.addSpacing(20)
        gender_label = QLabel("Gender:")
        gender_label.setMinimumWidth(LABEL_WIDTH)
        gender_layout.addWidget(gender_label)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Unknown", "Male", "Female", "Other"])
        self.gender_input.setMinimumWidth(120)
        gender_layout.addWidget(self.gender_input)
        gender_layout.addStretch()
        layout.addLayout(gender_layout)
        
        # Birth Date (indented)
        birth_date_layout = QHBoxLayout()
        birth_date_layout.addSpacing(20)
        birth_date_label = QLabel("Birth Date:")
        birth_date_label.setMinimumWidth(LABEL_WIDTH)
        birth_date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        birth_date_layout.addWidget(birth_date_label)
        self.birth_date_picker = DatePicker()
        self.birth_date_picker.set_date(1721, 1)
        birth_date_layout.addWidget(self.birth_date_picker)
        birth_date_layout.addStretch()
        layout.addLayout(birth_date_layout)
        
        # Immigrant checkbox (indented to align with field labels)
        immigrant_layout = QHBoxLayout()
        immigrant_layout.addSpacing(20)
        self.immigrant_check = QCheckBox("Immigrant")
        self.immigrant_check.setChecked(False)
        self.immigrant_check.stateChanged.connect(self._on_immigrant_toggled)
        immigrant_layout.addWidget(self.immigrant_check)
        immigrant_layout.addStretch()
        layout.addLayout(immigrant_layout)
        
        # Arrival Date (indented)
        arrival_date_layout = QHBoxLayout()
        arrival_date_layout.addSpacing(20)
        self.arrival_date_label = QLabel("Arrival Date:")
        self.arrival_date_label.setMinimumWidth(LABEL_WIDTH)
        self.arrival_date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        arrival_date_layout.addWidget(self.arrival_date_label)
        self.arrival_date_picker = DatePicker()
        self.arrival_date_picker.set_date(1721, 1)
        arrival_date_layout.addWidget(self.arrival_date_picker)
        arrival_date_layout.addStretch()
        layout.addLayout(arrival_date_layout)
        
        layout.addStretch()
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self._update_immigrant_state()
    
    def _on_immigrant_toggled(self) -> None:
        """Handle immigrant checkbox toggle."""
        self._update_immigrant_state()
    
    def _update_immigrant_state(self) -> None:
        """Update visibility based on immigrant status."""
        is_immigrant = self.immigrant_check.isChecked()
        
        self.birth_date_picker.unknown_check.setVisible(False)
        self.birth_date_picker.month_spin.setEnabled(not is_immigrant)
        
        if is_immigrant:
            self.birth_date_picker.unknown_check.setChecked(True)
        else:
            self.birth_date_picker.unknown_check.setChecked(False)
        
        self.arrival_date_label.setVisible(is_immigrant)
        self.arrival_date_picker.setVisible(is_immigrant)
        self.arrival_date_picker.unknown_check.setVisible(False)
    
    def _handle_accept(self) -> None:
        """Validate and create child."""
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        
        if not first_name:
            QMessageBox.warning(self, "Validation Error", "First name is required.")
            return
        
        if not last_name:
            QMessageBox.warning(self, "Validation Error", "Last name is required.")
            return
        
        gender = self.gender_input.currentText()
        
        if self.immigrant_check.isChecked():
            birth_year, _ = self.birth_date_picker.get_date()
            birth_month = None
            arrival_year, arrival_month = self.arrival_date_picker.get_date()
        else:
            birth_year, birth_month = self.birth_date_picker.get_date()
            arrival_year, arrival_month = None, None
        
        father_id = None
        mother_id = None
        parent2_id = self.parent2_selector.get_person_id()
        
        if self.parent1.gender == "Male":
            father_id = self.parent1.id
            if parent2_id:
                mother_id = parent2_id
        elif self.parent1.gender == "Female":
            mother_id = self.parent1.id
            if parent2_id:
                father_id = parent2_id
        else:
            father_id = self.parent1.id
            mother_id = parent2_id
        
        new_person = Person(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_year=birth_year,
            birth_month=birth_month,
            arrival_year=arrival_year,
            arrival_month=arrival_month,
            father_id=father_id,
            mother_id=mother_id,
            dynasty_id=self.parent1.dynasty_id
        )
        
        person_id = self.person_repo.insert(new_person)
        new_person.id = person_id
        
        self.created_person = new_person
        
        self.accept()
    
    def get_created_person(self) -> Person | None:
        """Returns the created child Person."""
        return self.created_person