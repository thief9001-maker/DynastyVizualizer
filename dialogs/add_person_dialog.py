"""Dialog for adding a new person to the database."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QTextEdit,
    QPushButton, QLabel, QDialogButtonBox, QCheckBox, QWidget
)
from PySide6.QtCore import Qt

from database.db_manager import DatabaseManager
from database.person_repository import PersonRepository
from models.person import Person
from widgets.date_picker import DatePicker


class AddPersonDialog(QDialog):
    """Dialog for adding a new person with essential information."""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person_repo = PersonRepository(db_manager)
        
        self.setWindowTitle("Add New Person")
        self.setMinimumWidth(500)
        
        self._person: Person | None = None
        
        self._setup_ui()
        self._connect_signals()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create and arrange all dialog widgets."""
        self.main_layout = QVBoxLayout(self)  # Store as instance variable
        
        # Special character toolbar
        self.main_layout.addLayout(self._create_special_char_toolbar())
        
        # Add separator line
        separator = QLabel()
        separator.setFrameShape(QLabel.Shape.HLine)
        separator.setFrameShadow(QLabel.Shadow.Sunken)
        self.main_layout.addWidget(separator)
        
        # Form fields
        self.main_layout.addLayout(self._create_form_layout())
        
        # OK/Cancel buttons
        self.main_layout.addWidget(self._create_button_box())
    
    def _create_special_char_toolbar(self) -> QHBoxLayout:
        """Create toolbar with special character buttons."""
        toolbar = QHBoxLayout()
        
        # Label
        label = QLabel("Special Characters:")
        toolbar.addWidget(label)
        
        # Character buttons
        special_chars = ['á', 'ý', 'ó', 'é', 'í']
        
        for char in special_chars:
            btn = QPushButton(char)
            btn.setMaximumWidth(40)
            btn.setToolTip(f"Insert '{char}' at cursor")
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(lambda checked, c=char: self._insert_special_char(c))
            toolbar.addWidget(btn)
        
        toolbar.addStretch()
        
        return toolbar
    
    def _create_form_layout(self) -> QFormLayout:
        """Create the main form with input fields."""
        form = QFormLayout()
        
        # First Name (required)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Required")
        form.addRow("First Name: *", self.first_name_input)
        
        # Middle Name (optional)
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Optional")
        form.addRow("Middle Name:", self.middle_name_input)
        
        # Last Name (required)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Required")
        form.addRow("Last Name: *", self.last_name_input)
        
        # Gender (optional)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Unknown", "Male", "Female", "Other"])
        form.addRow("Gender:", self.gender_input)
        
        # --- Date Section ---
        
        # Born in Town checkbox
        self.born_in_town_check = QCheckBox("Born in Town")
        self.born_in_town_check.setChecked(False)  # Default: arrived from elsewhere
        form.addRow("", self.born_in_town_check)
        
        # Birth Date picker FIRST (stays visible always)
        self.birth_date_picker = DatePicker()
        form.addRow("Birth Date: *", self.birth_date_picker)
        
        # Arrival Date picker SECOND (disappears when born in town)
        self.arrival_date_label = QLabel("Arrival Date:")
        self.arrival_date_picker = DatePicker()
        form.addRow(self.arrival_date_label, self.arrival_date_picker)
        
        # Notes (optional)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes about this person...")
        self.notes_input.setMaximumHeight(80)
        form.addRow("Notes:", self.notes_input)
        
        return form
    
    def _create_button_box(self) -> QDialogButtonBox:
        """Create OK and Cancel buttons."""
        button_box = QDialogButtonBox(
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
        # When "Born in Town" changes, show/hide arrival date
        self.born_in_town_check.stateChanged.connect(self._update_date_visibility)
        
        # Set initial visibility
        self._update_date_visibility()
    
    def _update_date_visibility(self) -> None:
        """Show or hide arrival date based on 'Born in Town' checkbox."""
        is_born_in_town = self.born_in_town_check.isChecked()
        
        # Hide/show arrival date row
        self.arrival_date_label.setVisible(not is_born_in_town)
        self.arrival_date_picker.setVisible(not is_born_in_town)
        
        # Adjust birth date precision hint
        if is_born_in_town:
            # Born in town: we know the precise month
            self.birth_date_picker.unknown_check.setChecked(False)
        else:
            # Arrived: might only know birth year
            self.birth_date_picker.unknown_check.setChecked(True)
        
        # Force layout to recalculate and resize dialog
        self.main_layout.invalidate()  # Use stored reference
        self.main_layout.activate()
        
        # Resize dialog to fit new content
        self.resize(self.minimumSizeHint())

    def _insert_special_char(self, char: str) -> None:
        """Insert a special character at the cursor position."""
        focused = self.focusWidget()
        
        if isinstance(focused, QLineEdit):
            focused.insert(char)
            focused.setFocus()
    
    def _handle_accept(self) -> None:
        """Validate inputs and create Person object before accepting."""
        if not self._validate_inputs():
            return
        
        birth_year, birth_month = self.birth_date_picker.get_date()
        
        arrival_year = None
        arrival_month = None
        if not self.born_in_town_check.isChecked():
            arrival_year, arrival_month = self.arrival_date_picker.get_date()
        
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
        
        # Save to database
        person_id = self.person_repo.insert(self._person)
        self._person.id = person_id
        
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate required fields and show error if invalid."""
        # First name required
        if not self.first_name_input.text().strip():
            self._show_error("First name is required.")
            self.first_name_input.setFocus()
            return False
        
        # Last name required
        if not self.last_name_input.text().strip():
            self._show_error("Last name is required.")
            self.last_name_input.setFocus()
            return False
        
        # Birth year required (always has a value from DatePicker)
        birth_year, _ = self.birth_date_picker.get_date()
        if birth_year < 1500 or birth_year > 2000:
            self._show_error("Birth year must be between 1500 and 2000.")
            return False
        
        return True
    
    def _show_error(self, message: str) -> None:
        """Display an error message to the user."""
        from PySide6.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Validation Error")
        msg.setText(message)
        msg.exec()
    
    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------
    
    def get_person(self) -> Person | None:
        """Return the created Person object."""
        return self._person