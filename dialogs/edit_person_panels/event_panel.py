"""Events panel for Edit Person dialog."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QGroupBox,
    QPushButton, QLabel, QFrame, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import QSignalBlocker

from database.db_manager import DatabaseManager
from database.event_repository import EventRepository
from models.person import Person
from models.event import Event


class EventsPanel(QWidget):
    """Panel for viewing and managing person's life events."""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.event_repo = EventRepository(db_manager)
        self.current_person: Person | None = None
        
        self.event_widgets: list[tuple[Event, QFrame]] = []
        self.new_events: list[Event] = []
        self.deleted_event_ids: list[int] = []
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create the events timeline layout."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Events timeline section
        events_group = QGroupBox("Life Events Timeline")
        events_layout = QVBoxLayout(events_group)
        
        self.events_container = QVBoxLayout()
        events_layout.addLayout(self.events_container)
        
        # Add event button
        add_btn = QPushButton("+ Add Event")
        add_btn.clicked.connect(self._add_event)
        events_layout.addWidget(add_btn)
        
        layout.addWidget(events_group)
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def _create_event_widget(self, event: Event) -> QFrame:
        """Create a widget displaying an event in timeline format."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        main_layout = QVBoxLayout(frame)
        
        # Header: event type and title
        header_layout = QHBoxLayout()
        
        # Event type badge
        type_label = QLabel(f"[{event.event_type}]")
        type_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        header_layout.addWidget(type_label)
        
        # Event title
        title_label = QLabel(event.event_title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Ongoing badge
        if event.is_ongoing:
            ongoing_label = QLabel("● Ongoing")
            ongoing_label.setStyleSheet("color: green; font-weight: bold;")
            header_layout.addWidget(ongoing_label)
        
        main_layout.addLayout(header_layout)
        
        # Date range
        date_label = QLabel(event.date_range_string)
        date_label.setStyleSheet("color: gray; font-style: italic;")
        main_layout.addWidget(date_label)
        
        # Notes (if present)
        if event.notes:
            notes_label = QLabel(event.notes)
            notes_label.setWordWrap(True)
            notes_label.setStyleSheet("margin-top: 5px; padding: 5px; background-color: #f5f5f5;")
            main_layout.addWidget(notes_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(lambda: self._edit_event(event))
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self._delete_event(event))
        button_layout.addWidget(delete_btn)
        
        main_layout.addLayout(button_layout)
        
        return frame
    
    def _add_event(self) -> None:
        """Open dialog to add a new event."""
        if not self.current_person:
            return
        
        from dialogs.create_event_dialog import CreateEventDialog
        dialog = CreateEventDialog(self.db_manager, self.current_person, self)
        
        if dialog.exec():
            created_event = dialog.get_created_event()
            if created_event:
                self.new_events.append(created_event)
                self._load_events()
                self._on_field_changed()
    
    def _edit_event(self, event: Event) -> None:
        """Open dialog to edit an event."""
        from dialogs.edit_event_dialog import EditEventDialog
        dialog = EditEventDialog(self.db_manager, event, self)
        
        if dialog.exec():
            edited_event = dialog.get_edited_event()
            if edited_event:
                # Update the event in place
                event.event_type = edited_event.event_type
                event.event_title = edited_event.event_title
                event.start_year = edited_event.start_year
                event.start_month = edited_event.start_month
                event.end_year = edited_event.end_year
                event.end_month = edited_event.end_month
                event.notes = edited_event.notes
                
                self._load_events()
                self._on_field_changed()

    def _delete_event(self, event: Event) -> None:
        """Delete an event after confirmation."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Delete Event")
        msg.setText(f"Are you sure you want to delete this event?\n\n{event.event_title}")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            if event.id:
                self.deleted_event_ids.append(event.id)
            if event in self.new_events:
                self.new_events.remove(event)
            
            self.event_widgets = [(e, w) for e, w in self.event_widgets if e != event]
            self._load_events()
            self._on_field_changed()
    
    def load_person(self, person: Person) -> None:
        """Load person's events."""
        self.current_person = person
        
        self.new_events.clear()
        self.deleted_event_ids.clear()
        
        self._load_events()
    
    def _load_events(self) -> None:
        """Load and display events in timeline order."""
        while self.events_container.count():
            item = self.events_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.event_widgets.clear()
        
        if not self.current_person or not self.current_person.id:
            placeholder = QLabel("No events recorded")
            placeholder.setStyleSheet("color: gray; font-style: italic; padding: 10px;")
            self.events_container.addWidget(placeholder)
            return
        
        # Get events from database
        events = self.event_repo.get_by_person(self.current_person.id)
        
        # Filter out deleted ones
        events = [e for e in events if e.id not in self.deleted_event_ids]
        
        # Add new events
        all_events = events + self.new_events
        
        # Sort chronologically
        all_events.sort(key=lambda e: (
            (9999, 12, 31) if e.start_year is None else 
            (e.start_year, e.start_month or 0, e.start_day or 0)
        ))
        
        if all_events:
            for event in all_events:
                widget = self._create_event_widget(event)
                self.events_container.addWidget(widget)
                self.event_widgets.append((event, widget))
        else:
            placeholder = QLabel("No events recorded")
            placeholder.setStyleSheet("color: gray; font-style: italic; padding: 10px;")
            self.events_container.addWidget(placeholder)
    
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