"""Dialog for editing an existing event."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QLabel, QDialogButtonBox, QWidget, QMessageBox, QTextEdit, QCheckBox
)
from PySide6.QtCore import QSignalBlocker

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.event import Event

from widgets.date_picker import DatePicker


class EditEventDialog(QDialog):
    """Dialog for editing an existing life event."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE_FORMAT: str = "Edit Event: {title}"
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
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        life_event: Event,
        parent: QWidget | None = None
    ) -> None:
        """Initialize edit event dialog."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.life_event: Event = life_event
        self.original_event_data: dict = self._capture_event_state()
        
        self.setWindowTitle(self.WINDOW_TITLE_FORMAT.format(title=life_event.event_title))
        self.setMinimumWidth(self.WINDOW_MIN_WIDTH)
        
        self._setup_ui()
        self._load_event()
    
    def _capture_event_state(self) -> dict:
        """Capture current event data for undo."""
        return {
            'id': self.life_event.id,
            'person_id': self.life_event.person_id,
            'event_type': self.life_event.event_type,
            'event_title': self.life_event.event_title,
            'start_year': self.life_event.start_year,
            'start_month': self.life_event.start_month,
            'end_year': self.life_event.end_year,
            'end_month': self.life_event.end_month,
            'notes': self.life_event.notes
        }
    
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
        start_date_layout.addWidget(self.start_date_picker)
        start_date_layout.addStretch()
        
        layout.addLayout(start_date_layout)
    
    def _create_ongoing_checkbox(self, layout: QVBoxLayout) -> None:
        """Create ongoing event checkbox."""
        ongoing_layout: QHBoxLayout = QHBoxLayout()
        ongoing_layout.addSpacing(self.LABEL_WIDTH + self.SPACING_INDENT)
        
        self.ongoing_check: QCheckBox = QCheckBox(self.CHECKBOX_ONGOING)
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
    # Data Loading
    # ------------------------------------------------------------------
    
    def _load_event(self) -> None:
        """Load event data into form fields."""
        blockers: list[QSignalBlocker] = [
            QSignalBlocker(self.event_type_input),
            QSignalBlocker(self.event_title_input),
            QSignalBlocker(self.start_date_picker),
            QSignalBlocker(self.ongoing_check),
            QSignalBlocker(self.end_date_picker),
            QSignalBlocker(self.notes_input),
        ]
        
        self._load_event_type()
        self._load_event_title()
        self._load_start_date()
        self._load_end_date()
        self._load_notes()
        
        self._update_ongoing_state()
    
    def _load_event_type(self) -> None:
        """Load event type into combo box."""
        index: int = self.event_type_input.findText(self.life_event.event_type)
        
        if index >= 0:
            self.event_type_input.setCurrentIndex(index)
        else:
            self.event_type_input.setCurrentText(self.life_event.event_type)
    
    def _load_event_title(self) -> None:
        """Load event title into input field."""
        self.event_title_input.setText(self.life_event.event_title)
    
    def _load_start_date(self) -> None:
        """Load start date into picker."""
        if self.life_event.start_year:
            self.start_date_picker.set_date(
                self.life_event.start_year,
                self.life_event.start_month
            )
    
    def _load_end_date(self) -> None:
        """Load end date or mark as ongoing."""
        if self.life_event.is_ongoing:
            self.ongoing_check.setChecked(True)
        else:
            self.ongoing_check.setChecked(False)
            if self.life_event.end_year:
                self.end_date_picker.set_date(
                    self.life_event.end_year,
                    self.life_event.end_month
                )
    
    def _load_notes(self) -> None:
        """Load notes into text area."""
        self.notes_input.setPlainText(self.life_event.notes)
    
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
        """Validate and save event."""
        if not self._validate_inputs():
            return
        
        self._update_event_from_inputs()
        self._execute_edit_command()
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
        
        if self._is_end_before_start(start_year, start_month, end_year, end_month):
            self._show_invalid_date_error()
            return False
        
        return True
    
    def _is_end_before_start(
        self,
        start_year: int,
        start_month: int | None,
        end_year: int,
        end_month: int | None
    ) -> bool:
        """Check if end date is before start date."""
        if end_year < start_year:
            return True
        
        if end_year == start_year and start_month and end_month:
            if end_month < start_month:
                return True
        
        return False
    
    def _show_invalid_date_error(self) -> None:
        """Show error for invalid date range."""
        QMessageBox.warning(
            self,
            self.MSG_TITLE_INVALID_DATE,
            self.MSG_TEXT_END_BEFORE_START
        )
    
    # ------------------------------------------------------------------
    # Event Update
    # ------------------------------------------------------------------
    
    def _update_event_from_inputs(self) -> None:
        """Update event object from input fields."""
        self.life_event.event_type = self.event_type_input.currentText().strip()
        self.life_event.event_title = self.event_title_input.text().strip()
        
        start_year, start_month = self.start_date_picker.get_date()
        self.life_event.start_year = start_year
        self.life_event.start_month = start_month
        
        end_year, end_month = self._get_end_date()
        self.life_event.end_year = end_year
        self.life_event.end_month = end_month
        
        self.life_event.notes = self.notes_input.toPlainText().strip()
    
    def _get_end_date(self) -> tuple[int | None, int | None]:
        """Get end date or None if ongoing."""
        if self.ongoing_check.isChecked():
            return None, None
        
        return self.end_date_picker.get_date()
    
    def _execute_edit_command(self) -> None:
        """Create and execute edit event command through undo manager."""
        from commands.genealogy_commands.edit_event import EditEventCommand
        
        command: EditEventCommand = EditEventCommand(
            db_manager=self.db_manager,
            event=self.life_event,
            original_event_data=self.original_event_data
        )
        
        main_window = self._find_main_window()
        
        if not main_window:
            return
        
        main_window.undo_manager.execute(command)
        main_window.db.mark_dirty()
        main_window.refresh_ui()
        main_window.edit_actions.update_undo_redo_actions()
    
    def _find_main_window(self):
        """Find the main window for accessing undo manager."""
        parent = self.parent()
        
        while parent:
            from main import MainWindow
            if isinstance(parent, MainWindow):
                return parent
            parent = parent.parent()
        
        return None