"""Dialog for editing a person with tabbed sections."""

from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget,
    QStackedWidget, QDialogButtonBox, QWidget, QLabel,
    QMessageBox
)
from PySide6.QtCore import Qt

from database.db_manager import DatabaseManager
from models.person import Person
from dialogs.edit_person_panels.general_panel import GeneralPanel

class EditPersonDialog(QDialog):
    """Tabbed dialog for comprehensive person editing."""
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent: QWidget | None = None
    ) -> None:
        """Initialize the edit person dialog."""
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person = person
        
        # Track if user has made changes
        self.has_unsaved_changes = False
        
        # Edited person data (will be filled by panels)
        self.edited_person: Person | None = None
        
        self.setWindowTitle(f"Edit Person: {person.display_name}")
        self.setMinimumSize(700, 500)
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self) -> None:
        """Create the main dialog layout with sidebar and panels."""
        main_layout = QVBoxLayout(self)
        
        # Horizontal split: sidebar | content
        content_layout = QHBoxLayout()
        
        # Left sidebar - panel selector
        self.panel_list = QListWidget()
        self.panel_list.setMaximumWidth(150)
        self.panel_list.addItem("General")
        self.panel_list.addItem("Relationships")
        self.panel_list.addItem("Events")
        self.panel_list.currentRowChanged.connect(self._on_panel_changed)
        
        # Right side - stacked panels
        self.panel_stack = QStackedWidget()
        
        # Create placeholder panels (we'll build these next)
        self.general_panel = self._create_general_panel()
        self.relationships_panel = self._create_relationships_panel()
        self.events_panel = self._create_events_panel()
        
        self.panel_stack.addWidget(self.general_panel)
        self.panel_stack.addWidget(self.relationships_panel)
        self.panel_stack.addWidget(self.events_panel)
        
        # Add to content layout
        content_layout.addWidget(self.panel_list)
        content_layout.addWidget(self.panel_stack, stretch=1)
        
        main_layout.addLayout(content_layout)
        
        # Bottom buttons - three button layout
        button_box = QDialogButtonBox()
        
        # Apply button - saves without closing
        self.apply_button = button_box.addButton(
            "Apply",
            QDialogButtonBox.ButtonRole.ApplyRole
        )
        self.apply_button.clicked.connect(self._handle_apply)
        
        # OK button - saves and closes
        self.ok_button = button_box.addButton(
            QDialogButtonBox.StandardButton.Ok
        )
        self.ok_button.clicked.connect(self._handle_ok)
        
        # Cancel button - closes without saving
        self.cancel_button = button_box.addButton(
            QDialogButtonBox.StandardButton.Cancel
        )
        self.cancel_button.clicked.connect(self.reject)
        
        main_layout.addWidget(button_box)
        
        # Select first panel
        self.panel_list.setCurrentRow(0)
    
    def _create_general_panel(self) -> QWidget:
        """Create the General information panel."""
        self.general_panel_widget = GeneralPanel(self)
        return self.general_panel_widget
    
    def _create_relationships_panel(self) -> QWidget:
        """Create the Relationships panel (parents, marriages, children)."""
        from dialogs.edit_person_panels.relationships_panel import RelationshipsPanel
        self.relationships_panel_widget = RelationshipsPanel(self.db_manager, self)
        return self.relationships_panel_widget
        
    def _create_events_panel(self) -> QWidget:
        """Create the Events panel (timeline of life events)."""
        # Placeholder
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        placeholder = QLabel("Events Panel - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        return panel
    
    def _on_panel_changed(self, index: int) -> None:
        """Handle panel selection change."""
        self.panel_stack.setCurrentIndex(index)
    
    def _load_data(self) -> None:
        """Load person data into all panels."""
        self.general_panel_widget.load_person(self.person)
        self.relationships_panel_widget.load_person(self.person)  # This line must be here!
            
    def _handle_apply(self) -> None:
        """Save changes but keep dialog open (Apply button)."""
        if self._save_changes():
            self.has_unsaved_changes = False
    
    def _handle_ok(self) -> None:
        """Save changes and close dialog with confirmation (OK button)."""
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
        # Validate General panel
        is_valid, error_msg = self.general_panel_widget.validate()
        if not is_valid:
            QMessageBox.warning(self, "Validation Error", error_msg)
            return False
        
        # Validate Relationships panel
        is_valid, error_msg = self.relationships_panel_widget.validate()
        if not is_valid:
            QMessageBox.warning(self, "Validation Error", error_msg)
            self.panel_list.setCurrentRow(1)  # Switch to Relationships tab
            return False
        
        # Get data from panels
        person_data = self.general_panel_widget.get_person_data()
        relationship_data = self.relationships_panel_widget.get_relationship_data()
        
        # Merge relationship data into person data
        person_data.update(relationship_data)
        
        # Create edited person
        from dataclasses import replace
        self.edited_person = replace(self.person, **person_data)
        
        # Save marriages
        self.relationships_panel_widget.save_marriages()
        
        # TODO: Save person to database via command
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
            
            result = msg.exec()
            if result == QMessageBox.StandardButton.Discard:
                super().reject()  # Close without saving
            # Otherwise, do nothing (stay open)
        else:
            super().reject()  # No changes, just close
    
    def mark_dirty(self) -> None:
        """Mark the dialog as having unsaved changes.
        
        Call this from panels when user edits anything.
        """
        self.has_unsaved_changes = True
    
    def get_edited_person(self) -> Person | None:
        """Get the edited person data after dialog is accepted."""
        return self.edited_person