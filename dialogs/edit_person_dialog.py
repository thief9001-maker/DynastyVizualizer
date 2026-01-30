"""Dialog for editing a person with tabbed sections."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget,
    QStackedWidget, QDialogButtonBox, QWidget, QMessageBox
)

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person
    from models.marriage import Marriage
    from models.event import Event

from database.person_repository import PersonRepository
from database.marriage_repository import MarriageRepository
from database.event_repository import EventRepository
from dialogs.edit_person_panels.general_panel import GeneralPanel
from dialogs.edit_person_panels.relationships_panel import RelationshipsPanel
from dialogs.edit_person_panels.event_panel import EventsPanel
from commands.genealogy_commands.edit_person import EditPersonCommand


class EditPersonDialog(QDialog):
    """Tabbed dialog for comprehensive person editing."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Panel Indices
    PANEL_INDEX_GENERAL: int = 0
    PANEL_INDEX_RELATIONSHIPS: int = 1
    PANEL_INDEX_EVENTS: int = 2
    
    # Panel Names
    PANEL_NAME_GENERAL: str = "General"
    PANEL_NAME_RELATIONSHIPS: str = "Relationships"
    PANEL_NAME_EVENTS: str = "Events"
    
    # Layout
    SIDEBAR_WIDTH: int = 150
    MIN_DIALOG_WIDTH: int = 700
    MIN_DIALOG_HEIGHT: int = 500
    
    # Button Text
    BUTTON_TEXT_APPLY: str = "Apply"
    
    # Message Box Titles
    MSG_TITLE_VALIDATION_ERROR: str = "Validation Error"
    MSG_TITLE_CHANGES_SAVED: str = "Changes Saved"
    MSG_TITLE_UNSAVED_CHANGES: str = "Unsaved Changes"
    
    # Message Box Text
    MSG_TEXT_CHANGES_SAVED: str = "Your edits have been saved successfully."
    MSG_TEXT_UNSAVED_CHANGES: str = "You have unsaved changes. Discard them?"
    
    # Window Title
    WINDOW_TITLE_FORMAT: str = "Edit Person: {name}"
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent: QWidget | None = None
    ) -> None:
        """Initialize edit person dialog with database manager and person."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.person: Person = person
        self.has_unsaved_changes: bool = False
        
        self.setWindowTitle(self.WINDOW_TITLE_FORMAT.format(name=person.display_name))
        self.setMinimumSize(self.MIN_DIALOG_WIDTH, self.MIN_DIALOG_HEIGHT)
        
        self._capture_original_state()
        self._setup_ui()
        self._load_data()
    
    def _capture_original_state(self) -> None:
        """Capture original state of person and related data for undo."""
        self.original_person_data: dict = self._capture_person_state()
        self.original_marriages: list[Marriage] = self._capture_marriages_state()
        self.original_events: list[Event] = self._capture_events_state()
    
    def _capture_person_state(self) -> dict:
        """Capture current person data for undo."""
        return {
            'id': self.person.id,
            'first_name': self.person.first_name,
            'middle_name': self.person.middle_name,
            'last_name': self.person.last_name,
            'birth_year': self.person.birth_year,
            'birth_month': self.person.birth_month,
            'death_year': self.person.death_year,
            'death_month': self.person.death_month,
            'arrival_year': self.person.arrival_year,
            'arrival_month': self.person.arrival_month,
            'moved_out_year': self.person.moved_out_year,
            'moved_out_month': self.person.moved_out_month,
            'gender': self.person.gender,
            'education_level': self.person.education,
            'dynasty_id': self.person.dynasty_id,
            'father_id': self.person.father_id,
            'mother_id': self.person.mother_id,
            'notes': self.person.notes
        }
    
    def _capture_marriages_state(self) -> list[Marriage]:
        """Capture current marriages for undo."""
        if not self.person.id:
            return []
        
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriages: list[Marriage] = marriage_repo.get_by_person(self.person.id)
        
        return [self._copy_marriage(m) for m in marriages]
    
    def _copy_marriage(self, marriage: Marriage) -> Marriage:
        """Create a copy of marriage for original state."""
        from models.marriage import Marriage
        return Marriage(
            id=marriage.id,
            spouse1_id=marriage.spouse1_id,
            spouse2_id=marriage.spouse2_id,
            marriage_year=marriage.marriage_year,
            marriage_month=marriage.marriage_month,
            dissolution_year=marriage.dissolution_year,
            dissolution_month=marriage.dissolution_month,
            dissolution_day=marriage.dissolution_day,
            dissolution_reason=marriage.dissolution_reason
        )
    
    def _capture_events_state(self) -> list[Event]:
        """Capture current events for undo."""
        if not self.person.id:
            return []
        
        event_repo: EventRepository = EventRepository(self.db_manager)
        events: list[Event] = event_repo.get_by_person(self.person.id)
        
        return [self._copy_event(e) for e in events]
    
    def _copy_event(self, event: Event) -> Event:
        """Create a copy of event for original state."""
        from models.event import Event
        return Event(
            id=event.id,
            person_id=event.person_id,
            event_type=event.event_type,
            event_title=event.event_title,
            start_year=event.start_year,
            start_month=event.start_month,
            end_year=event.end_year,
            end_month=event.end_month,
            notes=event.notes
        )
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create the main dialog layout with sidebar and panels."""
        main_layout: QVBoxLayout = QVBoxLayout(self)
        
        content_layout: QHBoxLayout = self._create_content_layout()
        main_layout.addLayout(content_layout)
        
        button_box: QDialogButtonBox = self._create_button_box()
        main_layout.addWidget(button_box)
        
        self.panel_list.setCurrentRow(self.PANEL_INDEX_GENERAL)
    
    def _create_content_layout(self) -> QHBoxLayout:
        """Create layout with sidebar and panel stack."""
        content_layout: QHBoxLayout = QHBoxLayout()
        
        self.panel_list: QListWidget = self._create_panel_list()
        self.panel_stack: QStackedWidget = self._create_panel_stack()
        
        content_layout.addWidget(self.panel_list)
        content_layout.addWidget(self.panel_stack, stretch=1)
        
        return content_layout
    
    def _create_panel_list(self) -> QListWidget:
        """Create left sidebar panel list."""
        panel_list: QListWidget = QListWidget()
        panel_list.setMaximumWidth(self.SIDEBAR_WIDTH)
        panel_list.addItem(self.PANEL_NAME_GENERAL)
        panel_list.addItem(self.PANEL_NAME_RELATIONSHIPS)
        panel_list.addItem(self.PANEL_NAME_EVENTS)
        panel_list.currentRowChanged.connect(self._on_panel_changed)
        
        return panel_list
    
    def _create_panel_stack(self) -> QStackedWidget:
        """Create stacked widget with all panels."""
        panel_stack: QStackedWidget = QStackedWidget()
        
        self.general_panel: GeneralPanel = GeneralPanel(self)
        self.relationships_panel: RelationshipsPanel = RelationshipsPanel(self.db_manager, self)
        self.events_panel: EventsPanel = EventsPanel(self.db_manager, self)
        
        panel_stack.addWidget(self.general_panel)
        panel_stack.addWidget(self.relationships_panel)
        panel_stack.addWidget(self.events_panel)
        
        return panel_stack
    
    def _create_button_box(self) -> QDialogButtonBox:
        """Create dialog button box with Apply, OK, and Cancel."""
        button_box: QDialogButtonBox = QDialogButtonBox()
        
        self.apply_button = button_box.addButton(
            self.BUTTON_TEXT_APPLY,
            QDialogButtonBox.ButtonRole.ApplyRole
        )
        self.apply_button.clicked.connect(self._handle_apply)
        
        self.ok_button = button_box.addButton(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.clicked.connect(self._handle_ok)
        
        self.cancel_button = button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_button.clicked.connect(self.reject)
        
        return button_box
    
    def _on_panel_changed(self, index: int) -> None:
        """Handle panel selection change."""
        self.panel_stack.setCurrentIndex(index)
    
    # ------------------------------------------------------------------
    # Data Loading
    # ------------------------------------------------------------------
    
    def _load_data(self) -> None:
        """Load person data into all panels."""
        self.general_panel.load_person(self.person)
        self.relationships_panel.load_person(self.person)
        self.events_panel.load_person(self.person)
    
    # ------------------------------------------------------------------
    # Save Handling
    # ------------------------------------------------------------------
    
    def _handle_apply(self) -> None:
        """Save changes but keep dialog open."""
        if not self._save_changes():
            return
        
        self.has_unsaved_changes = False
        self._recapture_state_after_save()
    
    def _handle_ok(self) -> None:
        """Save changes and close dialog with confirmation."""
        if not self._save_changes():
            return
        
        self.has_unsaved_changes = False
        self._show_save_confirmation()
        self.accept()
    
    def _show_save_confirmation(self) -> None:
        """Show confirmation message that changes were saved."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(self.MSG_TITLE_CHANGES_SAVED)
        msg.setText(self.MSG_TEXT_CHANGES_SAVED)
        msg.exec()
    
    def _save_changes(self) -> bool:
        """Collect and validate data from all panels, then save via command."""
        if not self._validate_all_panels():
            return False
        
        self._update_person_from_panels()
        self._execute_edit_command()
        
        return True
    
    def _validate_all_panels(self) -> bool:
        """Validate all panels and show error if validation fails."""
        if not self._validate_general_panel():
            return False
        
        if not self._validate_relationships_panel():
            return False
        
        return True
    
    def _validate_general_panel(self) -> bool:
        """Validate general panel."""
        is_valid, error_msg = self.general_panel.validate()
        
        if not is_valid:
            self._show_validation_error(error_msg)
            return False
        
        return True
    
    def _validate_relationships_panel(self) -> bool:
        """Validate relationships panel."""
        is_valid, error_msg = self.relationships_panel.validate()
        
        if not is_valid:
            self._show_validation_error(error_msg)
            self.panel_list.setCurrentRow(self.PANEL_INDEX_RELATIONSHIPS)
            return False
        
        return True
    
    def _show_validation_error(self, error_msg: str) -> None:
        """Show validation error message."""
        QMessageBox.warning(self, self.MSG_TITLE_VALIDATION_ERROR, error_msg)
    
    def _update_person_from_panels(self) -> None:
        """Update person object from panel data."""
        person_data: dict = self.general_panel.get_person_data()
        relationship_data: dict = self.relationships_panel.get_relationship_data()
        
        self.person.first_name = person_data.get('first_name', self.person.first_name)
        self.person.middle_name = person_data.get('middle_name', self.person.middle_name)
        self.person.last_name = person_data.get('last_name', self.person.last_name)
        self.person.birth_year = person_data.get('birth_year', self.person.birth_year)
        self.person.birth_month = person_data.get('birth_month', self.person.birth_month)
        self.person.death_year = person_data.get('death_year', self.person.death_year)
        self.person.death_month = person_data.get('death_month', self.person.death_month)
        self.person.arrival_year = person_data.get('arrival_year', self.person.arrival_year)
        self.person.arrival_month = person_data.get('arrival_month', self.person.arrival_month)
        self.person.moved_out_year = person_data.get('moved_out_year', self.person.moved_out_year)
        self.person.moved_out_month = person_data.get('moved_out_month', self.person.moved_out_month)
        self.person.gender = person_data.get('gender', self.person.gender)
        self.person.education = person_data.get('education', self.person.education)
        self.person.dynasty_id = person_data.get('dynasty_id', self.person.dynasty_id)
        self.person.notes = person_data.get('notes', self.person.notes)
        
        self.person.father_id = relationship_data.get('father_id', self.person.father_id)
        self.person.mother_id = relationship_data.get('mother_id', self.person.mother_id)
    
    def _execute_edit_command(self) -> None:
        """Create and execute edit person command through undo manager."""
        command: EditPersonCommand = EditPersonCommand(
            db_manager=self.db_manager,
            person=self.person,
            original_person_data=self.original_person_data,
            new_marriages=self.relationships_panel.new_marriages,
            modified_marriages=self.relationships_panel.modified_marriages,
            deleted_marriage_ids=self.relationships_panel.deleted_marriage_ids,
            new_events=self.events_panel.new_events,
            modified_events=self.events_panel.modified_events,
            deleted_event_ids=self.events_panel.deleted_event_ids,
            original_marriages=self.original_marriages,
            original_events=self.original_events
        )
        
        self._execute_command_through_undo_manager(command)
    
    def _execute_command_through_undo_manager(self, command: EditPersonCommand) -> None:
        """Execute command and update UI state."""
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
    
    def _recapture_state_after_save(self) -> None:
        """Recapture original state after Apply (for next save)."""
        self.original_person_data = self._capture_person_state()
        self.original_marriages = self._capture_marriages_state()
        self.original_events = self._capture_events_state()
        
        self.relationships_panel.new_marriages.clear()
        self.relationships_panel.modified_marriages.clear()
        self.relationships_panel.deleted_marriage_ids.clear()
        
        self.events_panel.new_events.clear()
        self.events_panel.modified_events.clear()
        self.events_panel.deleted_event_ids.clear()
    
    # ------------------------------------------------------------------
    # Dialog Close Handling
    # ------------------------------------------------------------------
    
    def reject(self) -> None:
        """Handle Cancel button with unsaved changes warning."""
        if self.has_unsaved_changes:
            if not self._confirm_discard_changes():
                return
        
        super().reject()
    
    def _confirm_discard_changes(self) -> bool:
        """Show confirmation dialog for discarding unsaved changes."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.MSG_TITLE_UNSAVED_CHANGES)
        msg.setText(self.MSG_TEXT_UNSAVED_CHANGES)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        
        return msg.exec() == QMessageBox.StandardButton.Discard
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def mark_dirty(self) -> None:
        """Mark the dialog as having unsaved changes."""
        self.has_unsaved_changes = True