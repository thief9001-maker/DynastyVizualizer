"""Dialog for adding a new person to the dynasty."""

from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QComboBox, QTextEdit,
    QPushButton, QDialogButtonBox, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

from models.person import Person

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class AddPersonDialog(QDialog):
    """Dialog for adding a new person with essential information."""
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the add person dialog."""
        super().__init__(parent)
        
        self.setWindowTitle("Add New Person")
        self.setMinimumWidth(400)
        
        self._person: Person | None = None
        
        self._setup_ui()
        self._connect_signals()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create and arrange all dialog widgets."""
        layout = QVBoxLayout(self)
        
        # Special character toolbar
        layout.addLayout(self._create_special_char_toolbar())
        
        # Add separator line
        separator = QLabel()
        separator.setFrameShape(QLabel.Shape.HLine)
        separator.setFrameShadow(QLabel.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Form fields
        layout.addLayout(self._create_form_layout())
        
        # OK/Cancel buttons
        layout.addWidget(self._create_button_box())
    
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
        
        # Info label
        info = QLabel("(Inserts into focused name field)")
        info.setStyleSheet("color: gray; font-size: 10px;")
        toolbar.addWidget(info)
        
        toolbar.addStretch()
        return toolbar
    
    def _create_form_layout(self) -> QFormLayout:
        """Create form with input fields."""
        form = QFormLayout()
        
        # First Name (required)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Required")
        form.addRow("First Name: *", self.first_name_input)
        
        # Last Name (required)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Required")
        form.addRow("Last Name: *", self.last_name_input)
        
        # Birth Year (required)
        self.birth_year_input = QSpinBox()
        self.birth_year_input.setRange(1000, 2100)
        self.birth_year_input.setValue(1700)
        self.birth_year_input.setSpecialValueText("Unknown")
        form.addRow("Birth Year: *", self.birth_year_input)
        
        # Gender (optional)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Unknown", "Male", "Female", "Other"])
        form.addRow("Gender:", self.gender_input)
        
        # Notes (optional)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes about this person...")
        self.notes_input.setMaximumHeight(80)
        form.addRow("Notes:", self.notes_input)
        
        return form
    
    def _create_button_box(self) -> QDialogButtonBox:
        """Create OK/Cancel button box."""
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
        # Enter key in line edits should not close dialog accidentally
        self.first_name_input.returnPressed.connect(self.last_name_input.setFocus)
        self.last_name_input.returnPressed.connect(self.birth_year_input.setFocus)
    
    def _insert_special_char(self, char: str) -> None:
        """Insert special character into currently focused name field."""
        focused = self.focusWidget()
        
        # Only insert into line edit fields (name fields)
        if isinstance(focused, QLineEdit):
            focused.insert(char)
    
    def _handle_accept(self) -> None:
        """Validate inputs and create Person object before accepting."""
        if not self._validate_inputs():
            return
        
        # Create Person object from form data
        self._person = Person(
            first_name=self.first_name_input.text().strip(),
            last_name=self.last_name_input.text().strip(),
            birth_year=self.birth_year_input.value(),
            gender=self.gender_input.currentText(),
            notes=self.notes_input.toPlainText().strip()
        )
        
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate that required fields are filled."""
        # Check first name
        if not self.first_name_input.text().strip():
            self._show_error("First name is required.")
            self.first_name_input.setFocus()
            return False
        
        # Check last name
        if not self.last_name_input.text().strip():
            self._show_error("Last name is required.")
            self.last_name_input.setFocus()
            return False
        
        # Check birth year (0 is the special "Unknown" value)
        if self.birth_year_input.value() == 0:
            self._show_error("Birth year is required.")
            self.birth_year_input.setFocus()
            return False
        
        return True
    
    def _show_error(self, message: str) -> None:
        """Display validation error message."""
        QMessageBox.warning(self, "Validation Error", message)
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_person(self) -> Person | None:
        """Return the created Person object, or None if dialog was cancelled."""
        return self._person