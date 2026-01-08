"""Dialog for creating a new event."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QLabel, QDialogButtonBox, QWidget, QMessageBox, QTextEdit, QCheckBox
)

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person
    from models.event import Event

from widgets.date_picker import DatePicker


class CreateEventDialog(QDialog):
    """Dialog for creating a new life event."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE_FORMAT: str = "Create Event for {name}"
    WINDOW_MIN_WIDTH: int = 550
    
    # Labels
    LABEL_EVENT_TYPE: str = "Event Type: *"
    LABEL_EVENT_TITLE: str = "Event Title: *"
    LABEL_START_DATE: str = "Start Date:"
    LABEL_END_DATE: str = "End Date:"
    LABEL_NOTES: str = "Notes:"
    LABEL_WIDTH: int = 100
    
    # Checkboxes
    CHECKBOX_ONGOING: str = "Ongoing Event"
    
    # Placeholders
    PLACEHOLDER_TITLE: str = "E.g., 'Became Blacksmith', 'Moved to Town'"
    PLACEHOLDER_NOTES: str = "Optional notes about this event..."
    
    # Event Types
    EVENT_TYPE_BIRTH: str = "Birth"
    EVENT_TYPE_DEATH: str = "Death"
    EVENT_TYPE_MARRIAGE: str = "Marriage"
    EVENT_TYPE_DIVORCE: str = "Divorce"
    EVENT_TYPE_JOB: str = "Job"
    EVENT_TYPE_EDUCATION: str = "Education"
    EVENT_TYPE_MOVE: str = "Move"
    EVENT_TYPE_MILITARY: str = "Military"
    EVENT_TYPE_IMMIGRATION: str = "Immigration"
    EVENT_TYPE_OTHER: str = "Other"
    
    # Message Box Titles
    MSG_TITLE_VALIDATION_ERROR: str = "Validation Error"
    MSG_TITLE_INVALID_DATE: str = "Invalid Date"
    
    # Message Box Text
    MSG_TEXT_TYPE_REQUIRED: str = "Event type is required."
    MSG_TEXT_TITLE_REQUIRED: str = "Event title is required."
    MSG_TEXT_END_BEFORE_START: str = "End date cannot be before start date."
    
    # Layout
    SPACING_INDENT: int = 10
    NOTES_MAX_HEIGHT: int = 100
    
    # Default Values
    DEFAULT_YEAR: int = 1721
    DEFAULT_MONTH: int = 1
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent: QWidget | None = None
    ) -> None:
        """Initialize create event dialog."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.person: Person = person
        self.created_event: Event | None = None
        
        self.setWindowTitle(self.WINDOW_TITLE_FORMAT.format(name=person.display_name))
        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create dialog widgets."""
        layout: QVBoxLayout = QVBoxLayout(self)
        
        self._create_event_type_row(layout)
        self._create_event_title_row(layout)
        self._create_start_date_row(layout)
        self._create_ongoing_checkbox(layout)
        self._create_end_date_row(layout)
        self._create_notes_section(layout)
        
        layout.addStretch()
        
        self._create_button_box(layout)
        
        self._update_ongoing_state()
    
    def _create_event_type_row(self, layout: QVBoxLayout) -> None:
        """Create event type selection row."""
        type_layout: QHBoxLayout = QHBoxLayout()
        
        type_label: QLabel = QLabel(self.LABEL_EVENT_TYPE)
        type_label.setMinimumWidth(self.LABEL_WIDTH)
        type_layout.addWidget(type_label)
        
        self.event_type_input: QComboBox = QComboBox()
        self.event_type_input.addItems([
            self.EVENT_TYPE_BIRTH,
            self.EVENT_TYPE_DEATH,
            self.EVENT_TYPE_MARRIAGE,
            self.EVENT_TYPE_DIVORCE,
            self.EVENT_TYPE_JOB,
            self.EVENT_TYPE_EDUCATION,
            self.EVENT_TYPE_MOVE,
            self.EVENT_TYPE_MILITARY,
            self.EVENT_TYPE_IMMIGRATION,
            self.EVENT_TYPE_OTHER
        ])
        self.event_type_input.setEditable(True)
        type_layout.addWidget(self.event_type_input)
        
        layout.addLayout(type_layout)
    
    def _create_event_title_row(self, layout: QVBoxLayout) -> None:
        """Create event title input row."""
        title_layout: QHBoxLayout = QHBoxLayout()
        
        title_label: QLabel = QLabel(self.LABEL_EVENT_TITLE)
        title_label.setMinimumWidth(self.LABEL_WIDTH)
        title_layout.addWidget(title_label)
        
        self.event_title_input: QLineEdit = QLineEdit()
        self.event_title_input.setPlaceholderText(self.PLACEHOLDER_TITLE)
        title_layout.addWidget(self.event_title_input)
        
        layout.addLayout(title_layout)
    
    def _create_start_date_row(self, layout: QVBoxLayout) -> None:
        """Create start date picker row."""
        start_date_layout: QHBoxLayout = QHBoxLayout()
        
        start_date_label: QLabel = QLabel(self.LABEL_START_DATE)
        start_date_label.setMinimumWidth(self.LABEL_WIDTH)
        start_date_layout.addWidget(start_date_label)
        
        self.start_date_picker: DatePicker = DatePicker()
        self.start_date_picker.set_date(self.DEFAULT_YEAR, self.DEFAULT_MONTH)
        start_date_layout.addWidget(self.start_date_picker)
        start_date_layout.addStretch()
        
        layout.addLayout(start_date_layout)
    
    def _create_ongoing_checkbox(self, layout: QVBoxLayout) -> None:
        """Create ongoing event checkbox."""
        ongoing_layout: QHBoxLayout = QHBoxLayout()
        ongoing_layout.addSpacing(self.LABEL_WIDTH + self.SPACING_INDENT)
        
        self.ongoing_check: QCheckBox = QCheckBox(self.CHECKBOX_ONGOING)
        self.ongoing_check.setChecked(False)
        self.ongoing_check.stateChanged.connect(self._on_ongoing_toggled)
        ongoing_layout.addWidget(self.ongoing_check)
        ongoing_layout.addStretch()
        
        layout.addLayout(ongoing_layout)
    
    def _create_end_date_row(self, layout: QVBoxLayout) -> None:
        """Create end date picker row."""
        end_date_layout: QHBoxLayout = QHBoxLayout()
        
        self.end_date_label: QLabel = QLabel(self.LABEL_END_DATE)
        self.end_date_label.setMinimumWidth(self.LABEL_WIDTH)
        end_date_layout.addWidget(self.end_date_label)
        
        self.end_date_picker: DatePicker = DatePicker()
        self.end_date_picker.set_date(self.DEFAULT_YEAR, self.DEFAULT_MONTH)
        end_date_layout.addWidget(self.end_date_picker)
        end_date_layout.addStretch()
        
        layout.addLayout(end_date_layout)
    
    def _create_notes_section(self, layout: QVBoxLayout) -> None:
        """Create notes text area."""
        notes_layout: QVBoxLayout = QVBoxLayout()
        
        notes_label: QLabel = QLabel(self.LABEL_NOTES)
        notes_layout.addWidget(notes_label)
        
        self.notes_input: QTextEdit = QTextEdit()
        self.notes_input.setPlaceholderText(self.PLACEHOLDER_NOTES)
        self.notes_input.setMaximumHeight(self.NOTES_MAX_HEIGHT)
        notes_layout.addWidget(self.notes_input)
        
        layout.addLayout(notes_layout)
    
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
    
    def _on_ongoing_toggled(self) -> None:
        """Handle ongoing checkbox toggle."""
        self._update_ongoing_state()
    
    def _update_ongoing_state(self) -> None:
        """Show/hide end date based on ongoing status."""
        is_ongoing: bool = self.ongoing_check.isChecked()
        self.end_date_label.setVisible(not is_ongoing)
        self.end_date_picker.setVisible(not is_ongoing)
    
    def _handle_accept(self) -> None:
        """Validate and create event."""
        if not self._validate_inputs():
            return
        
        self._create_event()
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate all input fields."""
        if not self._validate_event_type():
            return False
        
        if not self._validate_event_title():
            return False
        
        if not self._validate_date_range():
            return False
        
        return True
    
    def _validate_event_type(self) -> bool:
        """Validate event type is not empty."""
        event_type: str = self.event_type_input.currentText().strip()
        
        if not event_type:
            QMessageBox.warning(
                self,
                self.MSG_TITLE_VALIDATION_ERROR,
                self.MSG_TEXT_TYPE_REQUIRED
            )
            return False
        
        return True
    
    def _validate_event_title(self) -> bool:
        """Validate event title is not empty."""
        event_title: str = self.event_title_input.text().strip()
        
        if not event_title:
            QMessageBox.warning(
                self,
                self.MSG_TITLE_VALIDATION_ERROR,
                self.MSG_TEXT_TITLE_REQUIRED
            )
            return False
        
        return True
    
    def _validate_date_range(self) -> bool:
        """Validate end date is after start date."""
        if self.ongoing_check.isChecked():
            return True
        
        start_year, start_month = self.start_date_picker.get_date()
        end_year, end_month = self.end_date_picker.get_date()
        
        if not start_year or not end_year:
            return True
        
        if end_year < start_year:
            self._show_invalid_date_error()
            return False
        
        if end_year == start_year and start_month and end_month:
            if end_month < start_month:
                self._show_invalid_date_error()
                return False
        
        return True
    
    def _show_invalid_date_error(self) -> None:
        """Show error for invalid date range."""
        QMessageBox.warning(
            self,
            self.MSG_TITLE_INVALID_DATE,
            self.MSG_TEXT_END_BEFORE_START
        )
    
    # ------------------------------------------------------------------
    # Event Creation
    # ------------------------------------------------------------------
    
    def _create_event(self) -> None:
        """Create event from input fields."""
        from models.event import Event
        
        event_type: str = self.event_type_input.currentText().strip()
        event_title: str = self.event_title_input.text().strip()
        start_year, start_month = self.start_date_picker.get_date()
        end_year, end_month = self._get_end_date()
        notes: str = self.notes_input.toPlainText().strip()
        
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
    
    def _get_end_date(self) -> tuple[int | None, int | None]:
        """Get end date or None if ongoing."""
        if self.ongoing_check.isChecked():
            return None, None
        
        return self.end_date_picker.get_date()
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_created_event(self) -> Event | None:
        """Returns the created event."""
        return self.created_event