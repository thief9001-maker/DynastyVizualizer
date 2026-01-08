"""General information panel for Edit Person dialog."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QTextEdit, QLabel, QScrollArea, QCheckBox
)
from PySide6.QtCore import QSignalBlocker

if TYPE_CHECKING:
    from models.person import Person

from widgets.date_picker import DatePicker


class GeneralPanel(QWidget):
    """Panel for editing general person information."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Labels
    LABEL_FIRST_NAME: str = "First Name: *"
    LABEL_MIDDLE_NAME: str = "Middle Name:"
    LABEL_LAST_NAME: str = "Last Name: *"
    LABEL_MAIDEN_NAME: str = "Maiden Name:"
    LABEL_NICKNAME: str = "Nickname:"
    LABEL_GENDER: str = "Gender:"
    LABEL_BIRTH_DATE: str = "Birth Date:"
    LABEL_DEATH_DATE: str = "Death Date:"
    LABEL_ARRIVAL_DATE: str = "Arrival Date:"
    LABEL_MOVED_OUT_DATE: str = "Moved Out Date:"
    LABEL_DYNASTY_ID: str = "Dynasty ID:"
    LABEL_EDUCATION: str = "Education:"
    LABEL_NOTES: str = "Notes:"
    LABEL_EMPTY: str = ""
    
    # Placeholders
    PLACEHOLDER_REQUIRED: str = "Required"
    PLACEHOLDER_OPTIONAL: str = "Optional"
    PLACEHOLDER_NOTES: str = "Optional notes about this person..."
    
    # Checkboxes
    CHECKBOX_DIED: str = "Died?"
    CHECKBOX_IMMIGRANT: str = "Immigrant?"
    CHECKBOX_MOVED_OUT: str = "Moved Out?"
    CHECKBOX_IS_FOUNDER: str = "Is Dynasty Founder"
    
    # Gender Options
    GENDER_UNKNOWN: str = "Unknown"
    GENDER_MALE: str = "Male"
    GENDER_FEMALE: str = "Female"
    GENDER_OTHER: str = "Other"
    
    # Education Levels
    EDUCATION_LEVEL_0: str = "0 - Uneducated"
    EDUCATION_LEVEL_1: str = "1 - Basic"
    EDUCATION_LEVEL_2: str = "2 - Elementary"
    EDUCATION_LEVEL_3: str = "3 - Advanced"
    EDUCATION_LEVEL_4: str = "4 - Expert"
    EDUCATION_LEVEL_5: str = "5 - Master"
    
    # Default Values
    DEFAULT_DYNASTY_ID: str = "1"
    NOTES_MAX_HEIGHT: int = 120
    
    # Validation Messages
    VALIDATION_ERROR_FIRST_NAME: str = "First name is required."
    VALIDATION_ERROR_LAST_NAME: str = "Last name is required."
    VALIDATION_ERROR_DYNASTY_ID_POSITIVE: str = "Dynasty ID must be a positive number."
    VALIDATION_ERROR_DYNASTY_ID_INVALID: str = "Dynasty ID must be a valid number."
    
    # Parsing Constants
    EDUCATION_TEXT_SEPARATOR: str = " "
    EDUCATION_LEVEL_INDEX: int = 0
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize general panel."""
        super().__init__(parent)
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create all form fields."""
        scroll: QScrollArea = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container: QWidget = QWidget()
        form: QFormLayout = QFormLayout(container)
        
        self._create_name_fields(form)
        self._create_gender_field(form)
        self._create_date_fields(form)
        self._create_game_fields(form)
        self._create_notes_field(form)
        
        scroll.setWidget(container)
        
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        
        self._update_died_visibility()
        self._update_immigrant_visibility()
        self._update_moved_out_visibility()
        self._update_birth_month_visibility()
    
    def _create_name_fields(self, form: QFormLayout) -> None:
        """Create name input fields."""
        self.first_name_input: QLineEdit = QLineEdit()
        self.first_name_input.setPlaceholderText(self.PLACEHOLDER_REQUIRED)
        self.first_name_input.textChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_FIRST_NAME, self.first_name_input)
        
        self.middle_name_input: QLineEdit = QLineEdit()
        self.middle_name_input.setPlaceholderText(self.PLACEHOLDER_OPTIONAL)
        self.middle_name_input.textChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_MIDDLE_NAME, self.middle_name_input)
        
        self.last_name_input: QLineEdit = QLineEdit()
        self.last_name_input.setPlaceholderText(self.PLACEHOLDER_REQUIRED)
        self.last_name_input.textChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_LAST_NAME, self.last_name_input)
        
        self.maiden_name_input: QLineEdit = QLineEdit()
        self.maiden_name_input.setPlaceholderText(self.PLACEHOLDER_OPTIONAL)
        self.maiden_name_input.textChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_MAIDEN_NAME, self.maiden_name_input)
        
        self.nickname_input: QLineEdit = QLineEdit()
        self.nickname_input.setPlaceholderText(self.PLACEHOLDER_OPTIONAL)
        self.nickname_input.textChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_NICKNAME, self.nickname_input)
    
    def _create_gender_field(self, form: QFormLayout) -> None:
        """Create gender selection field."""
        self.gender_input: QComboBox = QComboBox()
        self.gender_input.addItems([
            self.GENDER_UNKNOWN,
            self.GENDER_MALE,
            self.GENDER_FEMALE,
            self.GENDER_OTHER
        ])
        self.gender_input.currentIndexChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_GENDER, self.gender_input)
    
    def _create_date_fields(self, form: QFormLayout) -> None:
        """Create date input fields with checkboxes."""
        self.birth_date_picker: DatePicker = DatePicker()
        self.birth_date_picker.dateChanged.connect(self._mark_dirty)
        self.birth_date_picker.unknown_check.setVisible(False)
        form.addRow(self.LABEL_BIRTH_DATE, self.birth_date_picker)
        
        self._create_death_date_field(form)
        self._create_arrival_date_field(form)
        self._create_moved_out_date_field(form)
    
    def _create_death_date_field(self, form: QFormLayout) -> None:
        """Create death date field with checkbox."""
        self.death_date_label: QLabel = QLabel(self.LABEL_DEATH_DATE)
        self.death_date_picker: DatePicker = DatePicker()
        self.death_date_picker.dateChanged.connect(self._mark_dirty)
        form.addRow(self.death_date_label, self.death_date_picker)
        
        self.died_check: QCheckBox = QCheckBox(self.CHECKBOX_DIED)
        self.died_check.setChecked(False)
        self.died_check.stateChanged.connect(self._on_died_toggled)
        self.died_check.stateChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_EMPTY, self.died_check)
    
    def _create_arrival_date_field(self, form: QFormLayout) -> None:
        """Create arrival date field with checkbox."""
        self.arrival_date_label: QLabel = QLabel(self.LABEL_ARRIVAL_DATE)
        self.arrival_date_picker: DatePicker = DatePicker()
        self.arrival_date_picker.dateChanged.connect(self._mark_dirty)
        form.addRow(self.arrival_date_label, self.arrival_date_picker)
        
        self.immigrant_check: QCheckBox = QCheckBox(self.CHECKBOX_IMMIGRANT)
        self.immigrant_check.setChecked(False)
        self.immigrant_check.stateChanged.connect(self._on_immigrant_toggled)
        self.immigrant_check.stateChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_EMPTY, self.immigrant_check)
    
    def _create_moved_out_date_field(self, form: QFormLayout) -> None:
        """Create moved out date field with checkbox."""
        self.moved_out_date_label: QLabel = QLabel(self.LABEL_MOVED_OUT_DATE)
        self.moved_out_date_picker: DatePicker = DatePicker()
        self.moved_out_date_picker.dateChanged.connect(self._mark_dirty)
        form.addRow(self.moved_out_date_label, self.moved_out_date_picker)
        
        self.moved_out_check: QCheckBox = QCheckBox(self.CHECKBOX_MOVED_OUT)
        self.moved_out_check.setChecked(False)
        self.moved_out_check.stateChanged.connect(self._on_moved_out_toggled)
        self.moved_out_check.stateChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_EMPTY, self.moved_out_check)
    
    def _create_game_fields(self, form: QFormLayout) -> None:
        """Create game-specific fields."""
        self.dynasty_id_input: QLineEdit = QLineEdit()
        self.dynasty_id_input.setText(self.DEFAULT_DYNASTY_ID)
        self.dynasty_id_input.textChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_DYNASTY_ID, self.dynasty_id_input)
        
        self.is_founder_check: QCheckBox = QCheckBox(self.CHECKBOX_IS_FOUNDER)
        self.is_founder_check.stateChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_EMPTY, self.is_founder_check)
        
        self.education_input: QComboBox = QComboBox()
        self.education_input.addItems([
            self.EDUCATION_LEVEL_0,
            self.EDUCATION_LEVEL_1,
            self.EDUCATION_LEVEL_2,
            self.EDUCATION_LEVEL_3,
            self.EDUCATION_LEVEL_4,
            self.EDUCATION_LEVEL_5
        ])
        self.education_input.currentIndexChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_EDUCATION, self.education_input)
    
    def _create_notes_field(self, form: QFormLayout) -> None:
        """Create notes text field."""
        self.notes_input: QTextEdit = QTextEdit()
        self.notes_input.setPlaceholderText(self.PLACEHOLDER_NOTES)
        self.notes_input.setMaximumHeight(self.NOTES_MAX_HEIGHT)
        self.notes_input.textChanged.connect(self._mark_dirty)
        form.addRow(self.LABEL_NOTES, self.notes_input)
    
    # ------------------------------------------------------------------
    # Visibility Control
    # ------------------------------------------------------------------
    
    def _on_immigrant_toggled(self) -> None:
        """Handle immigrant checkbox toggle."""
        self._update_immigrant_visibility()
        self._update_birth_month_visibility()
    
    def _update_immigrant_visibility(self) -> None:
        """Show or hide arrival date based on checkbox."""
        is_immigrant: bool = self.immigrant_check.isChecked()
        self.arrival_date_label.setVisible(is_immigrant)
        self.arrival_date_picker.setVisible(is_immigrant)

    def _update_birth_month_visibility(self) -> None:
        """Enable or disable birth month based on immigrant status."""
        is_immigrant: bool = self.immigrant_check.isChecked()
        
        if is_immigrant:
            self.birth_date_picker.month_spin.setEnabled(False)
            self.birth_date_picker.month_spin.setValue(1)
            self.birth_date_picker.unknown_check.setChecked(True)
        else:
            self.birth_date_picker.month_spin.setEnabled(True)
            self.birth_date_picker.unknown_check.setChecked(False)
    
    def _on_died_toggled(self) -> None:
        """Handle died checkbox toggle."""
        self._update_died_visibility()
    
    def _update_died_visibility(self) -> None:
        """Show or hide death date based on checkbox."""
        has_died: bool = self.died_check.isChecked()
        self.death_date_label.setVisible(has_died)
        self.death_date_picker.setVisible(has_died)
    
    def _on_moved_out_toggled(self) -> None:
        """Handle moved out checkbox toggle."""
        self._update_moved_out_visibility()
    
    def _update_moved_out_visibility(self) -> None:
        """Show or hide moved out date based on checkbox."""
        is_moved_out: bool = self.moved_out_check.isChecked()
        self.moved_out_date_label.setVisible(is_moved_out)
        self.moved_out_date_picker.setVisible(is_moved_out)
    
    # ------------------------------------------------------------------
    # Parent Dialog Communication
    # ------------------------------------------------------------------
    
    def _mark_dirty(self) -> None:
        """Mark parent dialog as having unsaved changes."""
        dialog = self._find_parent_dialog()
        if dialog:
            dialog.mark_dirty()
    
    def _find_parent_dialog(self):
        """Find the parent EditPersonDialog."""
        parent = self.parent()
        while parent:
            from dialogs.edit_person_dialog import EditPersonDialog
            if isinstance(parent, EditPersonDialog):
                return parent
            parent = parent.parent()
        return None
    
    # ------------------------------------------------------------------
    # Data Loading
    # ------------------------------------------------------------------
    
    def load_person(self, person: Person) -> None:
        """Load person data into form fields."""
        blockers: list[QSignalBlocker] = self._create_signal_blockers()
        
        self._load_name_fields(person)
        self._load_gender_field(person)
        self._load_date_fields(person)
        self._load_game_fields(person)
        self._load_notes_field(person)
        
        self._update_died_visibility()
        self._update_immigrant_visibility()
        self._update_moved_out_visibility()
        self._update_birth_month_visibility()
    
    def _create_signal_blockers(self) -> list[QSignalBlocker]:
        """Create signal blockers for all input widgets."""
        return [
            QSignalBlocker(self.first_name_input),
            QSignalBlocker(self.middle_name_input),
            QSignalBlocker(self.last_name_input),
            QSignalBlocker(self.maiden_name_input),
            QSignalBlocker(self.nickname_input),
            QSignalBlocker(self.gender_input),
            QSignalBlocker(self.birth_date_picker),
            QSignalBlocker(self.died_check),
            QSignalBlocker(self.death_date_picker),
            QSignalBlocker(self.immigrant_check),
            QSignalBlocker(self.arrival_date_picker),
            QSignalBlocker(self.moved_out_check),
            QSignalBlocker(self.moved_out_date_picker),
            QSignalBlocker(self.dynasty_id_input),
            QSignalBlocker(self.is_founder_check),
            QSignalBlocker(self.education_input),
            QSignalBlocker(self.notes_input),
        ]
    
    def _load_name_fields(self, person: Person) -> None:
        """Load name field values from person."""
        self.first_name_input.setText(person.first_name or "")
        self.middle_name_input.setText(person.middle_name or "")
        self.last_name_input.setText(person.last_name or "")
        self.maiden_name_input.setText(person.maiden_name or "")
        self.nickname_input.setText(person.nickname or "")
    
    def _load_gender_field(self, person: Person) -> None:
        """Load gender field value from person."""
        if not person.gender:
            return
        
        index: int = self.gender_input.findText(person.gender)
        if index >= 0:
            self.gender_input.setCurrentIndex(index)
    
    def _load_date_fields(self, person: Person) -> None:
        """Load date field values from person."""
        if person.birth_year:
            self.birth_date_picker.set_date(person.birth_year, person.birth_month)
        
        if person.death_year:
            self.died_check.setChecked(True)
            self.death_date_picker.set_date(person.death_year, person.death_month)
        else:
            self.died_check.setChecked(False)
        
        if person.arrival_year:
            self.immigrant_check.setChecked(True)
            self.arrival_date_picker.set_date(person.arrival_year, person.arrival_month)
            self.arrival_date_picker.unknown_check.setVisible(False)
        else:
            self.immigrant_check.setChecked(False)
        
        if person.moved_out_year:
            self.moved_out_check.setChecked(True)
            self.moved_out_date_picker.set_date(person.moved_out_year, person.moved_out_month)
        else:
            self.moved_out_check.setChecked(False)
    
    def _load_game_fields(self, person: Person) -> None:
        """Load game-specific field values from person."""
        self.dynasty_id_input.setText(str(person.dynasty_id))
        self.is_founder_check.setChecked(person.is_founder)
        self.education_input.setCurrentIndex(person.education)
    
    def _load_notes_field(self, person: Person) -> None:
        """Load notes field value from person."""
        self.notes_input.setPlainText(person.notes or "")
    
    # ------------------------------------------------------------------
    # Data Extraction
    # ------------------------------------------------------------------
    
    def get_person_data(self) -> dict:
        """Extract form data as dictionary."""
        birth_year, birth_month = self.birth_date_picker.get_date()
        
        death_year, death_month = self._get_death_date()
        arrival_year, arrival_month = self._get_arrival_date()
        moved_out_year, moved_out_month = self._get_moved_out_date()
        
        education_level: int = self._parse_education_level()
        
        return {
            'first_name': self.first_name_input.text().strip(),
            'middle_name': self.middle_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'maiden_name': self.maiden_name_input.text().strip(),
            'nickname': self.nickname_input.text().strip(),
            'gender': self.gender_input.currentText(),
            'birth_year': birth_year,
            'birth_month': birth_month,
            'death_year': death_year,
            'death_month': death_month,
            'arrival_year': arrival_year,
            'arrival_month': arrival_month,
            'moved_out_year': moved_out_year,
            'moved_out_month': moved_out_month,
            'dynasty_id': int(self.dynasty_id_input.text() or self.DEFAULT_DYNASTY_ID),
            'is_founder': self.is_founder_check.isChecked(),
            'education': education_level,
            'notes': self.notes_input.toPlainText().strip()
        }
    
    def _get_death_date(self) -> tuple[int | None, int | None]:
        """Get death date from picker if died checkbox is checked."""
        if self.died_check.isChecked():
            return self.death_date_picker.get_date()
        return None, None
    
    def _get_arrival_date(self) -> tuple[int | None, int | None]:
        """Get arrival date from picker if immigrant checkbox is checked."""
        if self.immigrant_check.isChecked():
            return self.arrival_date_picker.get_date()
        return None, None
    
    def _get_moved_out_date(self) -> tuple[int | None, int | None]:
        """Get moved out date from picker if moved out checkbox is checked."""
        if self.moved_out_check.isChecked():
            return self.moved_out_date_picker.get_date()
        return None, None
    
    def _parse_education_level(self) -> int:
        """Parse education level from combo box text."""
        education_text: str = self.education_input.currentText()
        return int(education_text.split(self.EDUCATION_TEXT_SEPARATOR)[self.EDUCATION_LEVEL_INDEX])
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def validate(self) -> tuple[bool, str]:
        """Validate form data."""
        if not self.first_name_input.text().strip():
            return (False, self.VALIDATION_ERROR_FIRST_NAME)
        
        if not self.last_name_input.text().strip():
            return (False, self.VALIDATION_ERROR_LAST_NAME)
        
        dynasty_id_valid, dynasty_error = self._validate_dynasty_id()
        if not dynasty_id_valid:
            return (False, dynasty_error)
        
        return (True, "")
    
    def _validate_dynasty_id(self) -> tuple[bool, str]:
        """Validate dynasty ID is a positive integer."""
        try:
            dynasty_id: int = int(self.dynasty_id_input.text())
            if dynasty_id < 1:
                return (False, self.VALIDATION_ERROR_DYNASTY_ID_POSITIVE)
        except ValueError:
            return (False, self.VALIDATION_ERROR_DYNASTY_ID_INVALID)
        
        return (True, "")