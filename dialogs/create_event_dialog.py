"""Dialog for creating a new event."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QLabel, QDialogButtonBox, QWidget, QMessageBox, QTextEdit, QCheckBox
)
from PySide6.QtCore import QSignalBlocker

from database.db_manager import DatabaseManager
from models.person import Person
from models.event import Event
from widgets.date_picker import DatePicker


class CreateEventDialog(QDialog):
    """Dialog for creating a new life event."""
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person = person
        self.created_event: Event | None = None
        
        self.setWindowTitle(f"Create Event for {person.display_name}")
        self.setMinimumWidth(550)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout = QVBoxLayout(self)
        
        LABEL_WIDTH = 100
        
        # Event Type
        type_layout = QHBoxLayout()
        type_label = QLabel("Event Type: *")
        type_label.setMinimumWidth(LABEL_WIDTH)
        type_layout.addWidget(type_label)
        
        self.event_type_input = QComboBox()
        self.event_type_input.addItems([
            "Birth", "Death", "Marriage", "Divorce",
            "Job", "Education", "Move", "Military",
            "Immigration", "Other"
        ])
        self.event_type_input.setEditable(True)
        type_layout.addWidget(self.event_type_input)
        layout.addLayout(type_layout)
        
        # Event Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Event Title: *")
        title_label.setMinimumWidth(LABEL_WIDTH)
        title_layout.addWidget(title_label)
        
        self.event_title_input = QLineEdit()
        self.event_title_input.setPlaceholderText("E.g., 'Became Blacksmith', 'Moved to Town'")
        title_layout.addWidget(self.event_title_input)
        layout.addLayout(title_layout)
        
        # Start Date
        start_date_layout = QHBoxLayout()
        start_date_label = QLabel("Start Date:")
        start_date_label.setMinimumWidth(LABEL_WIDTH)
        start_date_layout.addWidget(start_date_label)
        
        self.start_date_picker = DatePicker()
        self.start_date_picker.set_date(1721, 1)
        start_date_layout.addWidget(self.start_date_picker)
        start_date_layout.addStretch()
        layout.addLayout(start_date_layout)
        
        # Ongoing checkbox
        ongoing_layout = QHBoxLayout()
        ongoing_layout.addSpacing(LABEL_WIDTH + 10)
        
        self.ongoing_check = QCheckBox("Ongoing Event")
        self.ongoing_check.setChecked(False)
        self.ongoing_check.stateChanged.connect(self._on_ongoing_toggled)
        ongoing_layout.addWidget(self.ongoing_check)
        ongoing_layout.addStretch()
        layout.addLayout(ongoing_layout)
        
        # End Date
        end_date_layout = QHBoxLayout()
        self.end_date_label = QLabel("End Date:")
        self.end_date_label.setMinimumWidth(LABEL_WIDTH)
        end_date_layout.addWidget(self.end_date_label)
        
        self.end_date_picker = DatePicker()
        self.end_date_picker.set_date(1721, 1)
        end_date_layout.addWidget(self.end_date_picker)
        end_date_layout.addStretch()
        layout.addLayout(end_date_layout)
        
        # Notes
        notes_layout = QVBoxLayout()
        notes_label = QLabel("Notes:")
        notes_layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes about this event...")
        self.notes_input.setMaximumHeight(100)
        notes_layout.addWidget(self.notes_input)
        layout.addLayout(notes_layout)
        
        layout.addStretch()
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self._update_ongoing_state()
    
    def _on_ongoing_toggled(self) -> None:
        """Handle ongoing checkbox toggle."""
        self._update_ongoing_state()
    
    def _update_ongoing_state(self) -> None:
        """Show/hide end date based on ongoing status."""
        is_ongoing = self.ongoing_check.isChecked()
        self.end_date_label.setVisible(not is_ongoing)
        self.end_date_picker.setVisible(not is_ongoing)
    
    def _handle_accept(self) -> None:
        """Validate and create event."""
        event_type = self.event_type_input.currentText().strip()
        event_title = self.event_title_input.text().strip()
        
        if not event_type:
            QMessageBox.warning(self, "Validation Error", "Event type is required.")
            return
        
        if not event_title:
            QMessageBox.warning(self, "Validation Error", "Event title is required.")
            return
        
        start_year, start_month = self.start_date_picker.get_date()
        
        if self.ongoing_check.isChecked():
            end_year, end_month = None, None
        else:
            end_year, end_month = self.end_date_picker.get_date()
            
            # Validate end date after start date
            if start_year and end_year:
                if end_year < start_year:
                    QMessageBox.warning(self, "Invalid Date", "End date cannot be before start date.")
                    return
                elif end_year == start_year and start_month and end_month:
                    if end_month < start_month:
                        QMessageBox.warning(self, "Invalid Date", "End date cannot be before start date.")
                        return
        
        notes = self.notes_input.toPlainText().strip()
        
        self.created_event = Event(
            person_id=self.person.id,
            event_type=event_type,
            event_title=event_title,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
            notes=notes
        )
        
        self.accept()
    
    def get_created_event(self) -> Event | None:
        """Returns the created event."""
        return self.created_event