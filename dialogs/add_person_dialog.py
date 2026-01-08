"""Dialog for adding a new person to the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QTextEdit,
    QPushButton, QLabel, QDialogButtonBox, QCheckBox, QWidget, QMessageBox
)
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from database.person_repository import PersonRepository
from widgets.date_picker import DatePicker


class AddPersonDialog(QDialog):
    """Dialog for adding a new person with essential information."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE: str = "Add New Person"
    WINDOW_MIN_WIDTH: int = 500
    
    # Labels
    LABEL_SPECIAL_CHARS: str = "Special Characters:"
    LABEL_FIRST_NAME: str = "First Name: *"
    LABEL_MIDDLE_NAME: str = "Middle Name:"
    LABEL_LAST_NAME: str = "Last Name: *"
    LABEL_GENDER: str = "Gender:"
    LABEL_BIRTH_DATE: str = "Birth Date: *"
    LABEL_ARRIVAL_DATE: str = "Arrival Date:"
    LABEL_NOTES: str = "Notes:"
    LABEL_EMPTY: str = ""
    
    # Checkboxes
    CHECKBOX_BORN_IN_TOWN: str = "Born in Town"
    
    # Placeholders
    PLACEHOLDER_REQUIRED: str = "Required"
    PLACEHOLDER_OPTIONAL: str = "Optional"
    PLACEHOLDER_NOTES: str = "Optional notes about this person..."
    
    # Special Characters
    SPECIAL_CHARS: list[str] = ['á', 'ý', 'ó', 'é', 'í']
    CHAR_BUTTON_MAX_WIDTH: int = 40
    CHAR_BUTTON_TOOLTIP_FORMAT: str = "Insert '{char}' at cursor"
    
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
    MSG_TEXT_BIRTH_YEAR_RANGE: str = "Birth year must be between {min} and {max}."
    
    # Layout
    NOTES_MAX_HEIGHT: int = 80
    
    # Date Validation
    BIRTH_YEAR_MIN: int = 1500
    BIRTH_YEAR_MAX: int = 2000
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        """Initialize add person dialog."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.person_repo: PersonRepository = PersonRepository(db_manager)
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        
        self._person: Person | None = None
        
        self._setup_ui()
        self._connect_signals()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create and arrange all dialog widgets."""
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        
        self.main_layout.addLayout(self._create_special_char_toolbar())
        self.main_layout.addWidget(self._create_separator())
        self.main_layout.addLayout(self._create_form_layout())
        self.main_layout.addWidget(self._create_button_box())
    
    def _create_special_char_toolbar(self) -> QHBoxLayout:
        """Create toolbar with special character buttons."""
        toolbar: QHBoxLayout = QHBoxLayout()
        
        label: QLabel = QLabel(self.LABEL_SPECIAL_CHARS)
        toolbar.addWidget(label)
        
        for char in self.SPECIAL_CHARS:
            btn: QPushButton = self._create_special_char_button(char)
            toolbar.addWidget(btn)
        
        toolbar.addStretch()
        
        return toolbar
    
    def _create_special_char_button(self, char: str) -> QPushButton:
        """Create a button for inserting a special character."""
        btn: QPushButton = QPushButton(char)
        btn.setMaximumWidth(self.CHAR_BUTTON_MAX_WIDTH)
        btn.setToolTip(self.CHAR_BUTTON_TOOLTIP_FORMAT.format(char=char))
        btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        btn.clicked.connect(lambda checked, c=char: self._insert_special_char(c))
        return btn
    
    def _create_separator(self) -> QLabel:
        """Create horizontal separator line."""
        separator: QLabel = QLabel()
        separator.setFrameShape(QLabel.Shape.HLine)
        separator.setFrameShadow(QLabel.Shadow.Sunken)
        return separator
    
    def _create_form_layout(self) -> QFormLayout:
        """Create the main form with input fields."""
        form: QFormLayout = QFormLayout()
        
        self._create_name_fields(form)
        self._create_gender_field(form)
        self._create_born_in_town_checkbox(form)
        self._create_date_fields(form)
        self._create_notes_field(form)
        
        return form
    
    def _create_name_fields(self, form: QFormLayout) -> None:
        """Create name input fields."""
        self.first_name_input: QLineEdit = QLineEdit()
        self.first_name_input.setPlaceholderText(self.PLACEHOLDER_REQUIRED)
        form.addRow(self.LABEL_FIRST_NAME, self.first_name_input)
        
        self.middle_name_input: QLineEdit = QLineEdit()
        self.middle_name_input.setPlaceholderText(self.PLACEHOLDER_OPTIONAL)
        form.addRow(self.LABEL_MIDDLE_NAME, self.middle_name_input)
        
        self.last_name_input: QLineEdit = QLineEdit()
        self.last_name_input.setPlaceholderText(self.PLACEHOLDER_REQUIRED)
        form.addRow(self.LABEL_LAST_NAME, self.last_name_input)
    
    def _create_gender_field(self, form: QFormLayout) -> None:
        """Create gender selection field."""
        self.gender_input: QComboBox = QComboBox()
        self.gender_input.addItems([
            self.GENDER_UNKNOWN,
            self.GENDER_MALE,
            self.GENDER_FEMALE,
            self.GENDER_OTHER
        ])
        form.addRow(self.LABEL_GENDER, self.gender_input)
    
    def _create_born_in_town_checkbox(self, form: QFormLayout) -> None:
        """Create born in town checkbox."""
        self.born_in_town_check: QCheckBox = QCheckBox(self.CHECKBOX_BORN_IN_TOWN)
        self.born_in_town_check.setChecked(False)
        form.addRow(self.LABEL_EMPTY, self.born_in_town_check)
    
    def _create_date_fields(self, form: QFormLayout) -> None:
        """Create date input fields."""
        self.birth_date_picker: DatePicker = DatePicker()
        form.addRow(self.LABEL_BIRTH_DATE, self.birth_date_picker)
        
        self.arrival_date_label: QLabel = QLabel(self.LABEL_ARRIVAL_DATE)
        self.arrival_date_picker: DatePicker = DatePicker()
        form.addRow(self.arrival_date_label, self.arrival_date_picker)
    
    def _create_notes_field(self, form: QFormLayout) -> None:
        """Create notes text field."""
        self.notes_input: QTextEdit = QTextEdit()
        self.notes_input.setPlaceholderText(self.PLACEHOLDER_NOTES)
        self.notes_input.setMaximumHeight(self.NOTES_MAX_HEIGHT)
        form.addRow(self.LABEL_NOTES, self.notes_input)
    
    def _create_button_box(self) -> QDialogButtonBox:
        """Create OK and Cancel buttons."""
        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        
        return button_box
    
    # ------------------------------------------------------------------
    # Signal Handlers
    # ------------------------------------------------------------------
    
    def _connect_signals(self) -> None:
        """Connect widget signals to handlers."""
        self.born_in_town_check.stateChanged.connect(self._update_date_visibility)
        self._update_date_visibility()
    
    def _update_date_visibility(self) -> None:
        """Show or hide arrival date based on 'Born in Town' checkbox."""
        is_born_in_town: bool = self.born_in_town_check.isChecked()
        
        self.arrival_date_label.setVisible(not is_born_in_town)
        self.arrival_date_picker.setVisible(not is_born_in_town)
        
        self._update_birth_date_precision(is_born_in_town)
        self._resize_dialog()
    
    def _update_birth_date_precision(self, is_born_in_town: bool) -> None:
        """Update birth date precision hint based on birth location."""
        if is_born_in_town:
            self.birth_date_picker.unknown_check.setChecked(False)
        else:
            self.birth_date_picker.unknown_check.setChecked(True)
    
    def _resize_dialog(self) -> None:
        """Resize dialog to fit content."""
        self.main_layout.invalidate()
        self.main_layout.activate()
        self.resize(self.minimumSizeHint())
    
    def _insert_special_char(self, char: str) -> None:
        """Insert a special character at the cursor position."""
        focused = self.focusWidget()
        
        if not isinstance(focused, QLineEdit):
            return
        
        focused.insert(char)
        focused.setFocus()
    
    def _handle_accept(self) -> None:
        """Validate inputs and create Person object before accepting."""
        if not self._validate_inputs():
            return
        
        self._create_person()
        self._save_person_to_database()
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate required fields and show error if invalid."""
        if not self._validate_first_name():
            return False
        
        if not self._validate_last_name():
            return False
        
        if not self._validate_birth_year():
            return False
        
        return True
    
    def _validate_first_name(self) -> bool:
        """Validate first name is not empty."""
        if not self.first_name_input.text().strip():
            self._show_error(self.MSG_TEXT_FIRST_NAME_REQUIRED)
            self.first_name_input.setFocus()
            return False
        
        return True
    
    def _validate_last_name(self) -> bool:
        """Validate last name is not empty."""
        if not self.last_name_input.text().strip():
            self._show_error(self.MSG_TEXT_LAST_NAME_REQUIRED)
            self.last_name_input.setFocus()
            return False
        
        return True
    
    def _validate_birth_year(self) -> bool:
        """Validate birth year is within acceptable range."""
        birth_year, _ = self.birth_date_picker.get_date()
        
        if birth_year < self.BIRTH_YEAR_MIN or birth_year > self.BIRTH_YEAR_MAX:
            self._show_error(
                self.MSG_TEXT_BIRTH_YEAR_RANGE.format(
                    min=self.BIRTH_YEAR_MIN,
                    max=self.BIRTH_YEAR_MAX
                )
            )
            return False
        
        return True
    
    def _show_error(self, message: str) -> None:
        """Display an error message to the user."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.MSG_TITLE_VALIDATION_ERROR)
        msg.setText(message)
        msg.exec()
    
    # ------------------------------------------------------------------
    # Person Creation
    # ------------------------------------------------------------------
    
    def _create_person(self) -> None:
        """Create person object from input fields."""
        from models.person import Person
        
        birth_year, birth_month = self.birth_date_picker.get_date()
        arrival_year, arrival_month = self._get_arrival_date()
        
        self._person = Person(
            first_name=self.first_name_input.text().strip(),
            middle_name=self.middle_name_input.text().strip(),
            last_name=self.last_name_input.text().strip(),
            birth_year=birth_year,
            birth_month=birth_month,
            arrival_year=arrival_year,
            arrival_month=arrival_month,
            gender=self.gender_input.currentText(),
            notes=self.notes_input.toPlainText().strip()
        )
    
    def _get_arrival_date(self) -> tuple[int | None, int | None]:
        """Get arrival date or None if born in town."""
        if self.born_in_town_check.isChecked():
            return None, None
        
        return self.arrival_date_picker.get_date()
    
    def _save_person_to_database(self) -> None:
        """Save the created person to database."""
        if self._person is None:
            return
        
        person_id: int = self.person_repo.insert(self._person)
        self._person.id = person_id
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_person(self) -> Person | None:
        """Return the created Person object."""
        return self._person