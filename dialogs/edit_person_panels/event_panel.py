"""Events panel for Edit Person dialog."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGroupBox,
    QPushButton, QLabel, QFrame, QHBoxLayout, QMessageBox
)

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person
    from models.event import Event

from database.event_repository import EventRepository


class EventsPanel(QWidget):
    """Panel for viewing and managing person's life events."""
    
    LABEL_SECTION_TITLE: str = "Life Events Timeline"
    LABEL_NO_EVENTS: str = "No events recorded"
    LABEL_ONGOING_BADGE: str = "● Ongoing"
    
    BUTTON_TEXT_ADD_EVENT: str = "+ Add Event"
    BUTTON_TEXT_EDIT: str = "Edit"
    BUTTON_TEXT_DELETE: str = "Delete"
    
    MSG_TITLE_DELETE_EVENT: str = "Delete Event"
    MSG_TEXT_DELETE_EVENT: str = "Are you sure you want to delete this event?\n\n{title}"
    
    STYLE_TYPE_BADGE: str = "font-weight: bold; color: #2196F3;"
    STYLE_TITLE: str = "font-size: 14px; font-weight: bold;"
    STYLE_ONGOING_BADGE: str = "color: green; font-weight: bold;"
    STYLE_DATE: str = "color: gray; font-style: italic;"
    STYLE_NOTES: str = "margin-top: 5px; padding: 5px; background-color: #f5f5f5;"
    STYLE_PLACEHOLDER: str = "color: gray; font-style: italic; padding: 10px;"
    
    EVENT_TYPE_BADGE_FORMAT: str = "[{type}]"
    
    SORT_YEAR_UNKNOWN: int = 9999
    SORT_MONTH_UNKNOWN: int = 12
    SORT_DAY_UNKNOWN: int = 31
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        """Initialize events panel with database manager."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.event_repo: EventRepository = EventRepository(db_manager)
        self.current_person: Person | None = None
        
        self.event_widgets: list[tuple[Event, QFrame]] = []
        self.new_events: list[Event] = []
        self.deleted_event_ids: list[int] = []
        self.modified_events: dict[int, Event] = {}
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create the events timeline layout."""
        scroll: QScrollArea = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout(container)
        
        events_group: QGroupBox = self._create_events_section()
        layout.addWidget(events_group)
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout: QVBoxLayout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def _create_events_section(self) -> QGroupBox:
        """Create events timeline section with add button."""
        events_group: QGroupBox = QGroupBox(self.LABEL_SECTION_TITLE)
        events_layout: QVBoxLayout = QVBoxLayout(events_group)
        
        self.events_container: QVBoxLayout = QVBoxLayout()
        events_layout.addLayout(self.events_container)
        
        add_btn: QPushButton = QPushButton(self.BUTTON_TEXT_ADD_EVENT)
        add_btn.clicked.connect(self._add_event)
        events_layout.addWidget(add_btn)
        
        return events_group
    
    def _create_event_widget(self, event: Event) -> QFrame:
        """Create a widget displaying an event in timeline format."""
        frame: QFrame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        main_layout: QVBoxLayout = QVBoxLayout(frame)
        
        header_layout: QHBoxLayout = self._create_event_header(event)
        main_layout.addLayout(header_layout)
        
        date_label: QLabel = self._create_date_label(event)
        main_layout.addWidget(date_label)
        
        if event.notes:
            notes_label: QLabel = self._create_notes_label(event)
            main_layout.addWidget(notes_label)
        
        button_layout: QHBoxLayout = self._create_event_buttons(event)
        main_layout.addLayout(button_layout)
        
        return frame
    
    def _create_event_header(self, event: Event) -> QHBoxLayout:
        """Create event header with type badge, title, and ongoing indicator."""
        header_layout: QHBoxLayout = QHBoxLayout()
        
        type_label: QLabel = QLabel(self.EVENT_TYPE_BADGE_FORMAT.format(type=event.event_type))
        type_label.setStyleSheet(self.STYLE_TYPE_BADGE)
        header_layout.addWidget(type_label)
        
        title_label: QLabel = QLabel(event.event_title)
        title_label.setStyleSheet(self.STYLE_TITLE)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        if event.is_ongoing:
            ongoing_label: QLabel = QLabel(self.LABEL_ONGOING_BADGE)
            ongoing_label.setStyleSheet(self.STYLE_ONGOING_BADGE)
            header_layout.addWidget(ongoing_label)
        
        return header_layout
    
    def _create_date_label(self, event: Event) -> QLabel:
        """Create date range label for event."""
        date_label: QLabel = QLabel(event.date_range_string)
        date_label.setStyleSheet(self.STYLE_DATE)
        return date_label
    
    def _create_notes_label(self, event: Event) -> QLabel:
        """Create notes label for event."""
        notes_label: QLabel = QLabel(event.notes)
        notes_label.setWordWrap(True)
        notes_label.setStyleSheet(self.STYLE_NOTES)
        return notes_label
    
    def _create_event_buttons(self, event: Event) -> QHBoxLayout:
        """Create action buttons for event."""
        button_layout: QHBoxLayout = QHBoxLayout()
        button_layout.addStretch()
        
        edit_btn: QPushButton = QPushButton(self.BUTTON_TEXT_EDIT)
        edit_btn.clicked.connect(lambda: self._edit_event(event))
        button_layout.addWidget(edit_btn)
        
        delete_btn: QPushButton = QPushButton(self.BUTTON_TEXT_DELETE)
        delete_btn.clicked.connect(lambda: self._delete_event(event))
        button_layout.addWidget(delete_btn)
        
        return button_layout
    
    def _add_event(self) -> None:
        """Open dialog to add a new event."""
        if not self.current_person:
            return
        
        from dialogs.create_event_dialog import CreateEventDialog
        
        dialog: CreateEventDialog = CreateEventDialog(self.db_manager, self.current_person, self)
        
        if not dialog.exec():
            return
        
        created_event: Event | None = dialog.get_created_event()
        if not created_event:
            return
        
        self.new_events.append(created_event)
        self._load_events()
        self._mark_dirty()

    def _edit_event(self, event: Event) -> None:
        """Open dialog to edit an event."""
        from dialogs.edit_event_dialog import EditEventDialog

        dialog: EditEventDialog = EditEventDialog(self.db_manager, event, self)

        if not dialog.exec():
            return

        self._load_events()
        self._mark_dirty()
    
    def _update_event_in_place(self, event: Event, edited_event: Event) -> None:
        """Update event attributes from edited event."""
        event.event_type = edited_event.event_type
        event.event_title = edited_event.event_title
        event.start_year = edited_event.start_year
        event.start_month = edited_event.start_month
        event.start_day = edited_event.start_day
        event.end_year = edited_event.end_year
        event.end_month = edited_event.end_month
        event.end_day = edited_event.end_day
        event.notes = edited_event.notes
    
    def _delete_event(self, event: Event) -> None:
        """Delete an event after confirmation."""
        if not self._confirm_delete_event(event):
            return
        
        if event.id:
            self.deleted_event_ids.append(event.id)
        
        if event in self.new_events:
            self.new_events.remove(event)
        
        self.event_widgets = [(e, w) for e, w in self.event_widgets if e != event]
        self._load_events()
        self._mark_dirty()
    
    def _confirm_delete_event(self, event: Event) -> bool:
        """Show confirmation dialog for deleting event."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.MSG_TITLE_DELETE_EVENT)
        msg.setText(self.MSG_TEXT_DELETE_EVENT.format(title=event.event_title))
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        return msg.exec() == QMessageBox.StandardButton.Yes
    
    def load_person(self, person: Person) -> None:
        """Load person's events."""
        self.current_person = person
        
        self.new_events.clear()
        self.deleted_event_ids.clear()
        
        self._load_events()
    
    def _load_events(self) -> None:
        """Load and display events in timeline order."""
        self._clear_events_container()
        self.event_widgets.clear()
        
        if not self._has_valid_person():
            self._show_placeholder()
            return
        
        all_events: list[Event] = self._get_all_events()
        
        if all_events:
            self._display_events(all_events)
        else:
            self._show_placeholder()
    
    def _clear_events_container(self) -> None:
        """Clear all widgets from events container."""
        while self.events_container.count():
            item = self.events_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def _has_valid_person(self) -> bool:
        """Check if current person is valid and has an ID."""
        return self.current_person is not None and self.current_person.id is not None
    
    def _show_placeholder(self) -> None:
        """Show placeholder text when no events exist."""
        placeholder: QLabel = QLabel(self.LABEL_NO_EVENTS)
        placeholder.setStyleSheet(self.STYLE_PLACEHOLDER)
        self.events_container.addWidget(placeholder)
    
    def _get_all_events(self) -> list[Event]:
        """Get all events (database + new - deleted), sorted chronologically."""
        if not self.current_person or self.current_person.id is None:
            return []
        
        events: list[Event] = self.event_repo.get_by_person(self.current_person.id)
        events = [e for e in events if e.id not in self.deleted_event_ids]
        
        all_events: list[Event] = events + self.new_events
        all_events.sort(key=self._get_event_sort_key)
        
        return all_events
    
    def _get_event_sort_key(self, event: Event) -> tuple[int, int, int]:
        """Get sort key for event based on start date."""
        if event.start_year is None:
            return (self.SORT_YEAR_UNKNOWN, self.SORT_MONTH_UNKNOWN, self.SORT_DAY_UNKNOWN)
        
        return (
            event.start_year,
            event.start_month or 0,
            event.start_day or 0
        )
    
    def _display_events(self, events: list[Event]) -> None:
        """Display all events in the container."""
        for event in events:
            widget: QFrame = self._create_event_widget(event)
            self.events_container.addWidget(widget)
            self.event_widgets.append((event, widget))
    
    def save_events(self) -> None:
        """Save all event changes to database."""
        for event_id in self.deleted_event_ids:
            self.event_repo.delete(event_id)
        
        for event in self.new_events:
            self.event_repo.insert(event)
        
        self.new_events.clear()
        self.deleted_event_ids.clear()
    
    def validate(self) -> tuple[bool, str]:
        """Validate event data."""
        return (True, "")
    
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