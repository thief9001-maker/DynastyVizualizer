"""General information panel for Edit Person dialog."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QTextEdit, QLabel, QScrollArea, QCheckBox
)
from PySide6.QtCore import QSignalBlocker

from models.person import Person
from widgets.date_picker import DatePicker


class GeneralPanel(QWidget):
    """Panel for editing general person information."""
    
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create all form fields."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container = QWidget()
        form = QFormLayout(container)
        
        # Name fields
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Required")
        self.first_name_input.textChanged.connect(self._on_field_changed)
        form.addRow("First Name: *", self.first_name_input)
        
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setPlaceholderText("Optional")
        self.middle_name_input.textChanged.connect(self._on_field_changed)
        form.addRow("Middle Name:", self.middle_name_input)
        
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Required")
        self.last_name_input.textChanged.connect(self._on_field_changed)
        form.addRow("Last Name: *", self.last_name_input)
        
        self.maiden_name_input = QLineEdit()
        self.maiden_name_input.setPlaceholderText("Optional")
        self.maiden_name_input.textChanged.connect(self._on_field_changed)
        form.addRow("Maiden Name:", self.maiden_name_input)
        
        self.nickname_input = QLineEdit()
        self.nickname_input.setPlaceholderText("Optional")
        self.nickname_input.textChanged.connect(self._on_field_changed)
        form.addRow("Nickname:", self.nickname_input)
        
        # Gender
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Unknown", "Male", "Female", "Other"])
        self.gender_input.currentIndexChanged.connect(self._on_field_changed)
        form.addRow("Gender:", self.gender_input)
        
        # Birth Date
        self.birth_date_picker = DatePicker()
        self.birth_date_picker.dateChanged.connect(self._on_field_changed)
        form.addRow("Birth Date:", self.birth_date_picker)
        
        # Death Date with checkbox BELOW
        self.death_date_label = QLabel("Death Date:")
        self.death_date_picker = DatePicker()
        self.death_date_picker.dateChanged.connect(self._on_field_changed)
        form.addRow(self.death_date_label, self.death_date_picker)
        
        self.died_check = QCheckBox("Died?")
        self.died_check.setChecked(False)
        self.died_check.stateChanged.connect(self._on_died_toggled)
        self.died_check.stateChanged.connect(self._on_field_changed)
        form.addRow("", self.died_check)
        
        # Arrival Date with checkbox BELOW
        self.arrival_date_label = QLabel("Arrival Date:")
        self.arrival_date_picker = DatePicker()
        self.arrival_date_picker.dateChanged.connect(self._on_field_changed)
        form.addRow(self.arrival_date_label, self.arrival_date_picker)
        
        self.immigrant_check = QCheckBox("Immigrant?")
        self.immigrant_check.setChecked(False)
        self.immigrant_check.stateChanged.connect(self._on_immigrant_toggled)
        self.immigrant_check.stateChanged.connect(self._on_field_changed)
        form.addRow("", self.immigrant_check)
        
        # Moved Out Date with checkbox BELOW
        self.moved_out_date_label = QLabel("Moved Out Date:")
        self.moved_out_date_picker = DatePicker()
        self.moved_out_date_picker.dateChanged.connect(self._on_field_changed)
        form.addRow(self.moved_out_date_label, self.moved_out_date_picker)
        
        self.moved_out_check = QCheckBox("Moved Out?")
        self.moved_out_check.setChecked(False)
        self.moved_out_check.stateChanged.connect(self._on_moved_out_toggled)
        self.moved_out_check.stateChanged.connect(self._on_field_changed)
        form.addRow("", self.moved_out_check)
        
        # Game-specific fields
        self.dynasty_id_input = QLineEdit()
        self.dynasty_id_input.setText("1")
        self.dynasty_id_input.textChanged.connect(self._on_field_changed)
        form.addRow("Dynasty ID:", self.dynasty_id_input)
        
        self.is_founder_check = QCheckBox("Is Dynasty Founder")
        self.is_founder_check.stateChanged.connect(self._on_field_changed)
        form.addRow("", self.is_founder_check)
        
        self.education_input = QComboBox()
        self.education_input.addItems([
            "0 - Uneducated", "1 - Basic", "2 - Elementary",
            "3 - Advanced", "4 - Expert", "5 - Master"
        ])
        self.education_input.currentIndexChanged.connect(self._on_field_changed)
        form.addRow("Education:", self.education_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes about this person...")
        self.notes_input.setMaximumHeight(120)
        self.notes_input.textChanged.connect(self._on_field_changed)
        form.addRow("Notes:", self.notes_input)
        
        scroll.setWidget(container)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
        
        self._update_died_visibility()
        self._update_immigrant_visibility()
        self._update_moved_out_visibility()

    def _on_immigrant_toggled(self) -> None:
        """Handle immigrant checkbox toggle."""
        self._update_immigrant_visibility()

    def _update_immigrant_visibility(self) -> None:
        """Show/hide arrival date based on checkbox."""
        is_immigrant = self.immigrant_check.isChecked()
        self.arrival_date_label.setVisible(is_immigrant)
        self.arrival_date_picker.setVisible(is_immigrant)

    def _on_died_toggled(self) -> None:
        """Handle died checkbox toggle."""
        self._update_died_visibility()

    def _update_died_visibility(self) -> None:
        """Show/hide death date based on checkbox."""
        has_died = self.died_check.isChecked()
        self.death_date_label.setVisible(has_died)
        self.death_date_picker.setVisible(has_died)

    def _on_moved_out_toggled(self) -> None:
        """Handle moved out checkbox toggle."""
        self._update_moved_out_visibility()
    
    def _update_moved_out_visibility(self) -> None:
        """Show/hide moved out date based on checkbox."""
        is_moved_out = self.moved_out_check.isChecked()
        self.moved_out_date_label.setVisible(is_moved_out)
        self.moved_out_date_picker.setVisible(is_moved_out)
    
    def _on_field_changed(self) -> None:
        """Mark dialog as dirty when any field changes."""
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
    
    def load_person(self, person: Person) -> None:
        """Load person data into form fields."""
        blockers = [
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
        
        # Names
        self.first_name_input.setText(person.first_name or "")
        self.middle_name_input.setText(person.middle_name or "")
        self.last_name_input.setText(person.last_name or "")
        self.maiden_name_input.setText(person.maiden_name or "")
        self.nickname_input.setText(person.nickname or "")
        
        # Gender
        if person.gender:
            index = self.gender_input.findText(person.gender)
            if index >= 0:
                self.gender_input.setCurrentIndex(index)
        
        # Dates
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
        else:
            self.immigrant_check.setChecked(False)
        
        if person.moved_out_year:
            self.moved_out_check.setChecked(True)
            self.moved_out_date_picker.set_date(person.moved_out_year, person.moved_out_month)
        else:
            self.moved_out_check.setChecked(False)
        
        self._update_died_visibility()
        self._update_immigrant_visibility()
        self._update_moved_out_visibility()
        
        # Game fields
        self.dynasty_id_input.setText(str(person.dynasty_id))
        self.is_founder_check.setChecked(person.is_founder)
        self.education_input.setCurrentIndex(person.education)
        
        # Notes
        self.notes_input.setPlainText(person.notes or "")
    
    def get_person_data(self) -> dict:
        """Extract form data as dictionary."""
        birth_year, birth_month = self.birth_date_picker.get_date()
        
        if self.died_check.isChecked():
            death_year, death_month = self.death_date_picker.get_date()
        else:
            death_year, death_month = None, None
        
        if self.immigrant_check.isChecked():
            arrival_year, arrival_month = self.arrival_date_picker.get_date()
        else:
            arrival_year, arrival_month = None, None
        
        if self.moved_out_check.isChecked():
            moved_out_year, moved_out_month = self.moved_out_date_picker.get_date()
        else:
            moved_out_year, moved_out_month = None, None
        
        education_text = self.education_input.currentText()
        education_level = int(education_text.split(" ")[0])
        
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
            'dynasty_id': int(self.dynasty_id_input.text() or "1"),
            'is_founder': self.is_founder_check.isChecked(),
            'education': education_level,
            'notes': self.notes_input.toPlainText().strip()
        }

    def validate(self) -> tuple[bool, str]:
        """Validate form data."""
        if not self.first_name_input.text().strip():
            return (False, "First name is required.")
        
        if not self.last_name_input.text().strip():
            return (False, "Last name is required.")
        
        try:
            dynasty_id = int(self.dynasty_id_input.text())
            if dynasty_id < 1:
                return (False, "Dynasty ID must be a positive number.")
        except ValueError:
            return (False, "Dynasty ID must be a valid number.")
        
        return (True, "")