"""Dialog for editing an existing event."""

from dataclasses import replace

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QLabel, QDialogButtonBox, QWidget, QMessageBox, QTextEdit, QCheckBox
)
from PySide6.QtCore import QSignalBlocker

from database.db_manager import DatabaseManager
from models.event import Event
from widgets.date_picker import DatePicker


class EditEventDialog(QDialog):
    """Dialog for editing an existing life event."""
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        life_event: Event,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.life_event = life_event
        self.edited_event: Event | None = None
        
        self.setWindowTitle(f"Edit Event: {life_event.event_title}")
        self.setMinimumWidth(550)
        
        self._setup_ui()
        self._load_event()
    
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
        start_date_layout.addWidget(self.start_date_picker)
        start_date_layout.addStretch()
        layout.addLayout(start_date_layout)
        
        # Ongoing checkbox
        ongoing_layout = QHBoxLayout()
        ongoing_layout.addSpacing(LABEL_WIDTH + 10)
        
        self.ongoing_check = QCheckBox("Ongoing Event")
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
    
    def _load_event(self) -> None:
        """Load event data into form fields."""
        blockers = [
            QSignalBlocker(self.event_type_input),
            QSignalBlocker(self.event_title_input),
            QSignalBlocker(self.start_date_picker),
            QSignalBlocker(self.ongoing_check),
            QSignalBlocker(self.end_date_picker),
            QSignalBlocker(self.notes_input),
        ]
        
        # Event Type
        index = self.event_type_input.findText(self.life_event.event_type)
        if index >= 0:
            self.event_type_input.setCurrentIndex(index)
        else:
            self.event_type_input.setCurrentText(self.life_event.event_type)
        
        # Event Title
        self.event_title_input.setText(self.life_event.event_title)
        
        # Start Date
        if self.life_event.start_year:
            self.start_date_picker.set_date(self.life_event.start_year, self.life_event.start_month)
        
        # Ongoing / End Date
        if self.life_event.is_ongoing:
            self.ongoing_check.setChecked(True)
        else:
            self.ongoing_check.setChecked(False)
            if self.life_event.end_year:
                self.end_date_picker.set_date(self.life_event.end_year, self.life_event.end_month)
        
        # Notes
        self.notes_input.setPlainText(self.life_event.notes)
        
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
        """Validate and save event."""
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
        
        # Create edited event
        self.edited_event = replace(
            self.life_event,
            event_type=event_type,
            event_title=event_title,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
            notes=notes
        )
        
        self.accept()
    
    def get_edited_event(self) -> Event | None:
        """Returns the edited event."""
        return self.edited_event