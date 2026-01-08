"""Dialog for creating a new child."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QComboBox, QLabel, QDialogButtonBox, QWidget, QMessageBox, 
    QCheckBox, QFrame
)
from PySide6.QtCore import QSignalBlocker, Qt

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from database.person_repository import PersonRepository
from widgets.person_selector import PersonSelector
from widgets.date_picker import DatePicker


class CreateChildDialog(QDialog):
    """Dialog for creating a new child with pre-filled parents."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE: str = "Create Child"
    WINDOW_MIN_WIDTH: int = 550
    
    # Labels
    LABEL_PARENTS: str = "<b>Parents:</b>"
    LABEL_PARENT_1: str = "Parent 1:"
    LABEL_PARENT_2: str = "Parent 2:"
    LABEL_CHILD_INFO: str = "<b>Child Information:</b>"
    LABEL_FIRST_NAME: str = "First Name: *"
    LABEL_LAST_NAME: str = "Last Name: *"
    LABEL_GENDER: str = "Gender:"
    LABEL_BIRTH_DATE: str = "Birth Date:"
    LABEL_ARRIVAL_DATE: str = "Arrival Date:"
    LABEL_WIDTH: int = 85
    
    # Checkboxes
    CHECKBOX_IMMIGRANT: str = "Immigrant"
    
    # Placeholders
    PLACEHOLDER_REQUIRED: str = "Required"
    
    # Gender Options
    GENDER_UNKNOWN: str = "Unknown"
    GENDER_MALE: str = "Male"
    GENDER_FEMALE: str = "Female"
    GENDER_OTHER: str = "Other"
    
    # Message Box Titles
    MSG_TITLE_VALIDATION_ERROR: str = "Validation Error"
    
    # Message Box Text
    MSG_TEXT_FIRST_NAME_REQUIRED: str = "First name is required."
    MSG_TEXT_LAST_NAME_REQUIRED: str = "Last name is required."
    
    # Layout
    SPACING_INDENT: int = 20
    GENDER_COMBO_MIN_WIDTH: int = 120
    
    # Default Values
    DEFAULT_YEAR: int = 1721
    DEFAULT_MONTH: int = 1
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        parent1: Person,
        parent2_id: int | None = None,
        parent_widget: QWidget | None = None
    ) -> None:
        """Initialize create child dialog."""
        super().__init__(parent_widget)
        
        self.db_manager: DatabaseManager = db_manager
        self.person_repo: PersonRepository = PersonRepository(db_manager)
        self.parent1: Person = parent1
        self.parent2_id: int | None = parent2_id
        
        self.created_person: Person | None = None
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout: QVBoxLayout = QVBoxLayout(self)
        
        self._create_parents_section(layout)
        self._create_divider(layout)
        self._create_child_info_section(layout)
        
        layout.addStretch()
        
        self._create_button_box(layout)
        
        self._update_immigrant_state()
    
    def _create_parents_section(self, layout: QVBoxLayout) -> None:
        """Create parents section."""
        parents_header: QLabel = QLabel(self.LABEL_PARENTS)
        layout.addWidget(parents_header)
        
        self._create_parent1_row(layout)
        self._create_parent2_row(layout)
    
    def _create_parent1_row(self, layout: QVBoxLayout) -> None:
        """Create parent 1 display row."""
        parent1_layout: QHBoxLayout = QHBoxLayout()
        parent1_layout.addSpacing(self.SPACING_INDENT)
        
        parent1_label_text: QLabel = QLabel(self.LABEL_PARENT_1)
        parent1_label_text.setMinimumWidth(self.LABEL_WIDTH)
        parent1_layout.addWidget(parent1_label_text)
        
        parent1_name: QLabel = QLabel(f"<b>{self.parent1.display_name}</b>")
        parent1_layout.addWidget(parent1_name)
        parent1_layout.addStretch()
        
        layout.addLayout(parent1_layout)
    
    def _create_parent2_row(self, layout: QVBoxLayout) -> None:
        """Create parent 2 selector row."""
        parent2_layout: QHBoxLayout = QHBoxLayout()
        parent2_layout.addSpacing(self.SPACING_INDENT)
        
        parent2_label_text: QLabel = QLabel(self.LABEL_PARENT_2)
        parent2_label_text.setMinimumWidth(self.LABEL_WIDTH)
        parent2_layout.addWidget(parent2_label_text)
        
        self.parent2_selector: PersonSelector = PersonSelector(self.db_manager)
        if self.parent2_id:
            with QSignalBlocker(self.parent2_selector):
                self.parent2_selector.set_person(self.parent2_id)
        parent2_layout.addWidget(self.parent2_selector)
        
        layout.addLayout(parent2_layout)
    
    def _create_divider(self, layout: QVBoxLayout) -> None:
        """Create horizontal divider line."""
        line: QFrame = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
    
    def _create_child_info_section(self, layout: QVBoxLayout) -> None:
        """Create child information section."""
        child_header: QLabel = QLabel(self.LABEL_CHILD_INFO)
        layout.addWidget(child_header)
        
        self._create_first_name_row(layout)
        self._create_last_name_row(layout)
        self._create_gender_row(layout)
        self._create_birth_date_row(layout)
        self._create_immigrant_checkbox(layout)
        self._create_arrival_date_row(layout)
    
    def _create_first_name_row(self, layout: QVBoxLayout) -> None:
        """Create first name input row."""
        first_name_layout: QHBoxLayout = QHBoxLayout()
        first_name_layout.addSpacing(self.SPACING_INDENT)
        
        first_name_label: QLabel = QLabel(self.LABEL_FIRST_NAME)
        first_name_label.setMinimumWidth(self.LABEL_WIDTH)
        first_name_layout.addWidget(first_name_label)
        
        self.first_name_input: QLineEdit = QLineEdit()
        self.first_name_input.setPlaceholderText(self.PLACEHOLDER_REQUIRED)
        first_name_layout.addWidget(self.first_name_input)
        
        layout.addLayout(first_name_layout)
    
    def _create_last_name_row(self, layout: QVBoxLayout) -> None:
        """Create last name input row."""
        last_name_layout: QHBoxLayout = QHBoxLayout()
        last_name_layout.addSpacing(self.SPACING_INDENT)
        
        last_name_label: QLabel = QLabel(self.LABEL_LAST_NAME)
        last_name_label.setMinimumWidth(self.LABEL_WIDTH)
        last_name_layout.addWidget(last_name_label)
        
        self.last_name_input: QLineEdit = QLineEdit()
        self.last_name_input.setPlaceholderText(self.PLACEHOLDER_REQUIRED)
        self.last_name_input.setText(self.parent1.last_name)
        last_name_layout.addWidget(self.last_name_input)
        
        layout.addLayout(last_name_layout)
    
    def _create_gender_row(self, layout: QVBoxLayout) -> None:
        """Create gender selection row."""
        gender_layout: QHBoxLayout = QHBoxLayout()
        gender_layout.addSpacing(self.SPACING_INDENT)
        
        gender_label: QLabel = QLabel(self.LABEL_GENDER)
        gender_label.setMinimumWidth(self.LABEL_WIDTH)
        gender_layout.addWidget(gender_label)
        
        self.gender_input: QComboBox = QComboBox()
        self.gender_input.addItems([
            self.GENDER_UNKNOWN,
            self.GENDER_MALE,
            self.GENDER_FEMALE,
            self.GENDER_OTHER
        ])
        self.gender_input.setMinimumWidth(self.GENDER_COMBO_MIN_WIDTH)
        gender_layout.addWidget(self.gender_input)
        gender_layout.addStretch()
        
        layout.addLayout(gender_layout)
    
    def _create_birth_date_row(self, layout: QVBoxLayout) -> None:
        """Create birth date picker row."""
        birth_date_layout: QHBoxLayout = QHBoxLayout()
        birth_date_layout.addSpacing(self.SPACING_INDENT)
        
        birth_date_label: QLabel = QLabel(self.LABEL_BIRTH_DATE)
        birth_date_label.setMinimumWidth(self.LABEL_WIDTH)
        birth_date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        birth_date_layout.addWidget(birth_date_label)
        
        self.birth_date_picker: DatePicker = DatePicker()
        self.birth_date_picker.set_date(self.DEFAULT_YEAR, self.DEFAULT_MONTH)
        birth_date_layout.addWidget(self.birth_date_picker)
        birth_date_layout.addStretch()
        
        layout.addLayout(birth_date_layout)
    
    def _create_immigrant_checkbox(self, layout: QVBoxLayout) -> None:
        """Create immigrant checkbox."""
        immigrant_layout: QHBoxLayout = QHBoxLayout()
        immigrant_layout.addSpacing(self.SPACING_INDENT)
        
        self.immigrant_check: QCheckBox = QCheckBox(self.CHECKBOX_IMMIGRANT)
        self.immigrant_check.setChecked(False)
        self.immigrant_check.stateChanged.connect(self._on_immigrant_toggled)
        immigrant_layout.addWidget(self.immigrant_check)
        immigrant_layout.addStretch()
        
        layout.addLayout(immigrant_layout)
    
    def _create_arrival_date_row(self, layout: QVBoxLayout) -> None:
        """Create arrival date picker row."""
        arrival_date_layout: QHBoxLayout = QHBoxLayout()
        arrival_date_layout.addSpacing(self.SPACING_INDENT)
        
        self.arrival_date_label: QLabel = QLabel(self.LABEL_ARRIVAL_DATE)
        self.arrival_date_label.setMinimumWidth(self.LABEL_WIDTH)
        self.arrival_date_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        arrival_date_layout.addWidget(self.arrival_date_label)
        
        self.arrival_date_picker: DatePicker = DatePicker()
        self.arrival_date_picker.set_date(self.DEFAULT_YEAR, self.DEFAULT_MONTH)
        arrival_date_layout.addWidget(self.arrival_date_picker)
        arrival_date_layout.addStretch()
        
        layout.addLayout(arrival_date_layout)
    
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
    
    def _on_immigrant_toggled(self) -> None:
        """Handle immigrant checkbox toggle."""
        self._update_immigrant_state()
    
    def _update_immigrant_state(self) -> None:
        """Update visibility based on immigrant status."""
        is_immigrant: bool = self.immigrant_check.isChecked()
        
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
        if not self._validate_inputs():
            return
        
        self._create_child()
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate all input fields."""
        if not self._validate_first_name():
            return False
        
        if not self._validate_last_name():
            return False
        
        return True
    
    def _validate_first_name(self) -> bool:
        """Validate first name is not empty."""
        first_name: str = self.first_name_input.text().strip()
        
        if not first_name:
            QMessageBox.warning(
                self,
                self.MSG_TITLE_VALIDATION_ERROR,
                self.MSG_TEXT_FIRST_NAME_REQUIRED
            )
            return False
        
        return True
    
    def _validate_last_name(self) -> bool:
        """Validate last name is not empty."""
        last_name: str = self.last_name_input.text().strip()
        
        if not last_name:
            QMessageBox.warning(
                self,
                self.MSG_TITLE_VALIDATION_ERROR,
                self.MSG_TEXT_LAST_NAME_REQUIRED
            )
            return False
        
        return True
    
    # ------------------------------------------------------------------
    # Child Creation
    # ------------------------------------------------------------------
    
    def _create_child(self) -> None:
        """Create child person object."""
        from models.person import Person
        
        first_name: str = self.first_name_input.text().strip()
        last_name: str = self.last_name_input.text().strip()
        gender: str = self.gender_input.currentText()
        
        birth_year, birth_month = self._get_birth_date()
        arrival_year, arrival_month = self._get_arrival_date()
        father_id, mother_id = self._determine_parent_ids()
        
        new_person: Person = Person(
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
        
        person_id: int = self.person_repo.insert(new_person)
        new_person.id = person_id
        
        self.created_person = new_person
    
    def _get_birth_date(self) -> tuple[int | None, int | None]:
        """Get birth date based on immigrant status."""
        if self.immigrant_check.isChecked():
            birth_year, _ = self.birth_date_picker.get_date()
            return birth_year, None
        
        return self.birth_date_picker.get_date()
    
    def _get_arrival_date(self) -> tuple[int | None, int | None]:
        """Get arrival date if immigrant."""
        if self.immigrant_check.isChecked():
            return self.arrival_date_picker.get_date()
        
        return None, None
    
    def _determine_parent_ids(self) -> tuple[int | None, int | None]:
        """Determine father and mother IDs based on parent genders."""
        parent2_id: int | None = self.parent2_selector.get_person_id()
        
        if self.parent1.gender == self.GENDER_MALE:
            return self.parent1.id, parent2_id
        
        if self.parent1.gender == self.GENDER_FEMALE:
            return parent2_id, self.parent1.id
        
        return self.parent1.id, parent2_id
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_created_person(self) -> Person | None:
        """Returns the created child Person."""
        return self.created_person