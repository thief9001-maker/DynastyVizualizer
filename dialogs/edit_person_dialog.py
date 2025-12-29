"""Dialog for editing a person with tabbed sections."""

from dataclasses import replace

from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget,
    QStackedWidget, QDialogButtonBox, QWidget, QMessageBox
)

from database.db_manager import DatabaseManager
from database.person_repository import PersonRepository
from models.person import Person
from dialogs.edit_person_panels.general_panel import GeneralPanel
from dialogs.edit_person_panels.relationships_panel import RelationshipsPanel
from dialogs.edit_person_panels.event_panel import EventsPanel


class EditPersonDialog(QDialog):
    """Tabbed dialog for comprehensive person editing."""
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person = person
        self.has_unsaved_changes = False
        self.edited_person: Person | None = None
        
        self.setWindowTitle(f"Edit Person: {person.display_name}")
        self.setMinimumSize(700, 500)
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self) -> None:
        """Create the main dialog layout with sidebar and panels."""
        main_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        
        # Left sidebar
        self.panel_list = QListWidget()
        self.panel_list.setMaximumWidth(150)
        self.panel_list.addItem("General")
        self.panel_list.addItem("Relationships")
        self.panel_list.addItem("Events")
        self.panel_list.currentRowChanged.connect(self._on_panel_changed)
        
        # Right side - stacked panels
        self.panel_stack = QStackedWidget()
        
        self.general_panel_widget = GeneralPanel(self)
        self.relationships_panel_widget = RelationshipsPanel(self.db_manager, self)
        self.events_panel_widget = EventsPanel(self.db_manager, self)
        
        self.panel_stack.addWidget(self.general_panel_widget)
        self.panel_stack.addWidget(self.relationships_panel_widget)
        self.panel_stack.addWidget(self.events_panel_widget)
        
        content_layout.addWidget(self.panel_list)
        content_layout.addWidget(self.panel_stack, stretch=1)
        main_layout.addLayout(content_layout)
        
        # Bottom buttons
        button_box = QDialogButtonBox()
        
        self.apply_button = button_box.addButton(
            "Apply",
            QDialogButtonBox.ButtonRole.ApplyRole
        )
        self.apply_button.clicked.connect(self._handle_apply)
        
        self.ok_button = button_box.addButton(QDialogButtonBox.StandardButton.Ok)
        self.ok_button.clicked.connect(self._handle_ok)
        
        self.cancel_button = button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        self.cancel_button.clicked.connect(self.reject)
        
        main_layout.addWidget(button_box)
        
        self.panel_list.setCurrentRow(0)
    
    def _on_panel_changed(self, index: int) -> None:
        """Handle panel selection change."""
        self.panel_stack.setCurrentIndex(index)
    
    def _load_data(self) -> None:
        """Load person data into all panels."""
        self.general_panel_widget.load_person(self.person)
        self.relationships_panel_widget.load_person(self.person)
        self.events_panel_widget.load_person(self.person)
    
    def _handle_apply(self) -> None:
        """Save changes but keep dialog open."""
        if self._save_changes():
            self.has_unsaved_changes = False
    
    def _handle_ok(self) -> None:
        """Save changes and close dialog with confirmation."""
        if self._save_changes():
            self.has_unsaved_changes = False
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Changes Saved")
            msg.setText("Your edits have been saved successfully.")
            msg.exec()
            
            self.accept()
    
    def _save_changes(self) -> bool:
        """Collect and validate data from all panels, then save."""
        is_valid, error_msg = self.general_panel_widget.validate()
        if not is_valid:
            QMessageBox.warning(self, "Validation Error", error_msg)
            return False
        
        is_valid, error_msg = self.relationships_panel_widget.validate()
        if not is_valid:
            QMessageBox.warning(self, "Validation Error", error_msg)
            self.panel_list.setCurrentRow(1)
            return False
        
        person_data = self.general_panel_widget.get_person_data()
        relationship_data = self.relationships_panel_widget.get_relationship_data()
        person_data.update(relationship_data)
        
        self.edited_person = replace(self.person, **person_data)
        
        person_repo = PersonRepository(self.db_manager)
        person_repo.update(self.edited_person)
        
        self.relationships_panel_widget.save_marriages()
        self.events_panel_widget.save_events()
        
        self.person = self.edited_person
        
        return True
    
    def reject(self) -> None:
        """Handle Cancel button - warn if unsaved changes."""
        if self.has_unsaved_changes:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("You have unsaved changes. Discard them?")
            msg.setStandardButtons(
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )
            
            if msg.exec() == QMessageBox.StandardButton.Discard:
                super().reject()
        else:
            super().reject()
    
    def mark_dirty(self) -> None:
        """Mark the dialog as having unsaved changes."""
        self.has_unsaved_changes = True
    
    def get_edited_person(self) -> Person | None:
        """Get the edited person data after dialog is accepted."""
        return self.edited_person