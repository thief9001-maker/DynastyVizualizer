"""Relationships panel for Edit Person dialog."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QScrollArea,
    QGroupBox, QPushButton, QHBoxLayout, QFrame, QMessageBox, QComboBox
)
from PySide6.QtCore import QSignalBlocker

from database.db_manager import DatabaseManager
from database.person_repository import PersonRepository
from database.marriage_repository import MarriageRepository
from models.person import Person
from models.marriage import Marriage
from widgets.person_selector import PersonSelector
from widgets.date_picker import DatePicker
from dialogs.end_marriage_dialog import EndMarriageDialog


class RelationshipsPanel(QWidget):
    """Panel for editing person relationships."""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person_repo = PersonRepository(db_manager)
        self.marriage_repo = MarriageRepository(db_manager)
        self.current_person: Person | None = None
        
        self.marriage_widgets: list[tuple[Marriage, QFrame]] = []
        self.new_marriages: list[Marriage] = []
        self.deleted_marriage_ids: list[int] = []
        self.modified_marriages: dict[int, Marriage] = {}
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create all relationship sections."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        
        layout.addWidget(self._create_parents_section())
        layout.addWidget(self._create_marriages_section())
        layout.addWidget(self._create_children_section())
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def _create_parents_section(self) -> QGroupBox:
        """Create parents section with father/mother selectors."""
        group = QGroupBox("Parents")
        layout = QVBoxLayout(group)
        form = QFormLayout()
        
        # Father selector
        self.father_selector = PersonSelector(self.db_manager)
        self.father_selector.set_filter(gender="Male")
        self.father_selector.personSelected.connect(self._on_field_changed)
        self.father_selector.selectionCleared.connect(self._on_field_changed)
        self.father_selector.personSelected.connect(lambda: self._load_siblings())
        
        father_row = QHBoxLayout()
        father_row.addWidget(self.father_selector)
        self.father_jump_btn = QPushButton("View Person")
        self.father_jump_btn.clicked.connect(
            lambda: self._jump_to_person(self.father_selector.get_person_id())
        )
        father_row.addWidget(self.father_jump_btn)
        form.addRow("Father:", father_row)
        
        # Mother selector
        self.mother_selector = PersonSelector(self.db_manager)
        self.mother_selector.set_filter(gender="Female")
        self.mother_selector.personSelected.connect(self._on_field_changed)
        self.mother_selector.selectionCleared.connect(self._on_field_changed)
        self.mother_selector.personSelected.connect(lambda: self._load_siblings())
        
        mother_row = QHBoxLayout()
        mother_row.addWidget(self.mother_selector)
        self.mother_jump_btn = QPushButton("View Person")
        self.mother_jump_btn.clicked.connect(
            lambda: self._jump_to_person(self.mother_selector.get_person_id())
        )
        mother_row.addWidget(self.mother_jump_btn)
        form.addRow("Mother:", mother_row)
        
        layout.addLayout(form)
        
        layout.addWidget(QLabel("<b>Siblings:</b>"))
        self.siblings_container = QVBoxLayout()
        layout.addLayout(self.siblings_container)
        
        return group
    
    def _create_marriages_section(self) -> QGroupBox:
        """Create marriages section with inline editing."""
        group = QGroupBox("Marriages")
        layout = QVBoxLayout(group)
        
        self.marriages_container = QVBoxLayout()
        layout.addLayout(self.marriages_container)
        
        add_btn = QPushButton("+ Add New Marriage")
        add_btn.clicked.connect(self._add_marriage)
        layout.addWidget(add_btn)
        
        return group
    
    def _create_children_section(self) -> QGroupBox:
        """Create children section."""
        group = QGroupBox("Children")
        layout = QVBoxLayout(group)
        
        self.children_container = QVBoxLayout()
        layout.addLayout(self.children_container)
        
        add_btn = QPushButton("+ Add Child")
        add_btn.clicked.connect(self._add_child)
        layout.addWidget(add_btn)
        
        return group
    
    def _create_marriage_widget(self, marriage: Marriage) -> QFrame:
        """Create inline editable widget for a marriage."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        layout = QVBoxLayout(frame)
        
        # Status header
        header_layout = QHBoxLayout()
        status_indicator = QLabel("✓ Active" if marriage.is_active else "○ Ended")
        status_indicator.setStyleSheet(
            f"font-weight: bold; color: {'green' if marriage.is_active else 'gray'}"
        )
        header_layout.addWidget(status_indicator)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        form = QFormLayout()
        
        # Spouse selector
        spouse_selector = PersonSelector(self.db_manager)
        
        with QSignalBlocker(spouse_selector):
            if self.current_person and self.current_person.id:
                spouse_id = self.marriage_repo.get_spouse_id(marriage, self.current_person.id)
            else:
                spouse_id = None
            
            if spouse_id:
                spouse_selector.set_person(spouse_id)
        
        spouse_selector.personSelected.connect(self._on_field_changed)
        
        spouse_row = QHBoxLayout()
        spouse_row.addWidget(spouse_selector)
        
        spouse_jump_btn = QPushButton("View Person")
        spouse_jump_btn.setEnabled(spouse_id is not None)
        spouse_jump_btn.clicked.connect(lambda: self._jump_to_person(spouse_selector.get_person_id()))
        spouse_selector.personSelected.connect(lambda: spouse_jump_btn.setEnabled(True))
        spouse_selector.selectionCleared.connect(lambda: spouse_jump_btn.setEnabled(False))
        spouse_row.addWidget(spouse_jump_btn)
        
        form.addRow("Spouse:", spouse_row)
        
        # Marriage date
        marriage_date = DatePicker()
        with QSignalBlocker(marriage_date):
            if marriage.marriage_year:
                marriage_date.set_date(marriage.marriage_year, marriage.marriage_month)
        
        marriage_date.dateChanged.connect(self._on_field_changed)
        form.addRow("Married:", marriage_date)
        
        # End date and reason (if ended)
        if not marriage.is_active:
            end_date = DatePicker()
            with QSignalBlocker(end_date):
                if marriage.dissolution_year:
                    end_date.set_date(marriage.dissolution_year, marriage.dissolution_month)
            
            end_date.dateChanged.connect(self._on_field_changed)
            form.addRow("Ended:", end_date)
            
            reason_combo = QComboBox()
            with QSignalBlocker(reason_combo):
                reason_combo.addItems(["Death", "Divorce", "Annulment", "Other", "Unknown"])
                if marriage.dissolution_reason:
                    index = reason_combo.findText(marriage.dissolution_reason)
                    if index >= 0:
                        reason_combo.setCurrentIndex(index)
            
            reason_combo.currentIndexChanged.connect(self._on_field_changed)
            form.addRow("Reason:", reason_combo)
        
        layout.addLayout(form)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        if marriage.is_active:
            end_btn = QPushButton("End Marriage")
            end_btn.clicked.connect(lambda: self._end_marriage(marriage))
            button_layout.addWidget(end_btn)
        else:
            reactivate_btn = QPushButton("Reactivate")
            reactivate_btn.clicked.connect(lambda: self._reactivate_marriage(marriage))
            button_layout.addWidget(reactivate_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self._delete_marriage(marriage))
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
        # Store widget references for data collection
        frame.spouse_selector = spouse_selector  # type: ignore[attr-defined]
        frame.marriage_date = marriage_date  # type: ignore[attr-defined]
        if not marriage.is_active:
            frame.end_date = end_date  # type: ignore[attr-defined]
            frame.reason_combo = reason_combo  # type: ignore[attr-defined]
        
        return frame
    
    def _create_person_widget(self, person: Person) -> QFrame:
        """Create widget displaying a person with jump button."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(frame)
        
        birth_info = f"b. {person.birth_year}" if person.birth_year else "birth unknown"
        info_label = QLabel(f"{person.display_name} ({birth_info})")
        layout.addWidget(info_label)
        layout.addStretch()
        
        jump_btn = QPushButton("View Person")
        jump_btn.clicked.connect(lambda: self._jump_to_person(person.id))
        layout.addWidget(jump_btn)
        
        return frame
    
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
    
    def _jump_to_person(self, person_id: int | None) -> None:
        """Jump to editing a different person."""
        if person_id is None:
            return
        
        dialog = self._find_parent_dialog()
        if not dialog:
            return
        
        person = self.person_repo.get_by_id(person_id)
        if not person:
            return
        
        if dialog.has_unsaved_changes:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("Save Changes?")
            msg.setText("Save changes before jumping to another person?")
            msg.setStandardButtons(
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel
            )
            
            result = msg.exec()
            if result == QMessageBox.StandardButton.Cancel:
                return
            elif result == QMessageBox.StandardButton.Save:
                if not dialog._save_changes():
                    return
        
        dialog.person = person
        dialog.setWindowTitle(f"Edit Person: {person.display_name}")
        dialog._load_data()
        dialog.has_unsaved_changes = False
        dialog.panel_list.setCurrentRow(1)
    
    def _add_marriage(self) -> None:
        """Add a new marriage using dialog."""
        if not self.current_person or not self.current_person.id:
            return
        
        active_marriages = [m for m, _ in self.marriage_widgets if m.is_active]
        
        # Validate active marriages have spouses
        for marriage, widget in self.marriage_widgets:
            if marriage.is_active:
                spouse_selector = widget.spouse_selector  # type: ignore[attr-defined]
                if not spouse_selector.get_person_id():
                    QMessageBox.warning(
                        self,
                        "Incomplete Marriage",
                        "Please select a spouse for the current marriage before adding a new one."
                    )
                    return
        
        if active_marriages:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("End Current Marriage?")
            msg.setText("This person has an active marriage. End it before creating a new one?")
            msg.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if msg.exec() == QMessageBox.StandardButton.Yes:
                marriage = active_marriages[0]
                from dialogs.end_marriage_dialog import EndMarriageDialog
                end_dialog = EndMarriageDialog(marriage, self)
                
                if end_dialog.exec():
                    year, month, reason = end_dialog.get_dissolution_data()
                    marriage.dissolution_year = year
                    marriage.dissolution_month = month
                    marriage.dissolution_reason = reason
                    
                    if marriage.id:
                        self.modified_marriages[marriage.id] = marriage
                    
                    self._on_field_changed()
                else:
                    return
        
        # Open create marriage dialog
        from dialogs.create_marriage_dialog import CreateMarriageDialog
        dialog = CreateMarriageDialog(self.db_manager, self.current_person, self)
        
        if dialog.exec():
            spouse_id, year, month = dialog.get_marriage_data()
            
            # Create new marriage with data from dialog
            new_marriage = Marriage(
                spouse1_id=self.current_person.id,
                spouse2_id=spouse_id,
                marriage_year=year,
                marriage_month=month
            )
            
            self.new_marriages.append(new_marriage)
            self._load_marriages()
            self._on_field_changed()

    def _end_marriage(self, marriage: Marriage) -> None:
        """End a marriage with dialog."""
        dialog = EndMarriageDialog(marriage, self)
        
        if dialog.exec():
            year, month, reason = dialog.get_dissolution_data()
            
            # Validate end date after marriage date
            if marriage.marriage_year:
                if year and year < marriage.marriage_year:
                    QMessageBox.warning(self, "Invalid Date", "Marriage cannot end before it started.")
                    return
                elif year == marriage.marriage_year and marriage.marriage_month and month:
                    if month < marriage.marriage_month:
                        QMessageBox.warning(self, "Invalid Date", "Marriage cannot end before it started.")
                        return
            
            marriage.dissolution_year = year
            marriage.dissolution_month = month
            marriage.dissolution_reason = reason
            
            if marriage.id:
                self.modified_marriages[marriage.id] = marriage
            
            self._load_marriages()
            self._on_field_changed()
    
    def _reactivate_marriage(self, marriage: Marriage) -> None:
        """Reactivate an ended marriage."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Reactivate Marriage?")
        msg.setText("Remove the end date and reactivate this marriage? This will remove any empty active marriages.")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            # Delete empty active marriages
            for m, widget in list(self.marriage_widgets):
                if m != marriage and m.is_active:
                    spouse_selector = widget.spouse_selector  # type: ignore[attr-defined]
                    spouse_id = spouse_selector.get_person_id()
                    
                    if not spouse_id:
                        if m.id:
                            self.deleted_marriage_ids.append(m.id)
                        if m in self.new_marriages:
                            self.new_marriages.remove(m)
            
            marriage.dissolution_year = None
            marriage.dissolution_month = None
            marriage.dissolution_day = None
            marriage.dissolution_reason = ""
            
            if marriage.id:
                self.modified_marriages[marriage.id] = marriage
            
            self._load_marriages()
            self._on_field_changed()
    
    def _delete_marriage(self, marriage: Marriage) -> None:
        """Delete a marriage after confirmation."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Delete Marriage")
        msg.setText("Are you sure you want to delete this marriage?")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            if marriage.id:
                self.deleted_marriage_ids.append(marriage.id)
            if marriage in self.new_marriages:
                self.new_marriages.remove(marriage)
            
            self.marriage_widgets = [(m, w) for m, w in self.marriage_widgets if m != marriage]
            self._load_marriages()
            self._on_field_changed()
    
    def _add_child(self) -> None:
        """Open dialog to add a new child."""
        QMessageBox.information(self, "Not Implemented", "Add Child coming soon!")
    
    def load_person(self, person: Person) -> None:
        """Load person relationship data."""
        self.current_person = person
        
        self.new_marriages.clear()
        self.deleted_marriage_ids.clear()
        self.modified_marriages.clear()
        
        blockers = [
            QSignalBlocker(self.father_selector),
            QSignalBlocker(self.mother_selector),
        ]
        
        if person.father_id:
            self.father_selector.set_person(person.father_id)
            self.father_jump_btn.setEnabled(True)
        else:
            self.father_selector.clear()
            self.father_jump_btn.setEnabled(False)
        
        if person.mother_id:
            self.mother_selector.set_person(person.mother_id)
            self.mother_jump_btn.setEnabled(True)
        else:
            self.mother_selector.clear()
            self.mother_jump_btn.setEnabled(False)
        
        self._load_siblings()
        self._load_marriages()
        self._load_children()
    
    def _load_siblings(self) -> None:
        """Load and display siblings."""
        while self.siblings_container.count():
            item = self.siblings_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        if not self.current_person:
            return
        
        siblings = []
        
        father_id = self.father_selector.get_person_id()
        if father_id:
            father_children = self.person_repo.get_children(father_id)
            siblings.extend([p for p in father_children if p.id != self.current_person.id])
        
        mother_id = self.mother_selector.get_person_id()
        if mother_id:
            mother_children = self.person_repo.get_children(mother_id)
            for child in mother_children:
                if child.id != self.current_person.id and child not in siblings:
                    siblings.append(child)
        
        if siblings:
            for sibling in siblings:
                sibling_widget = self._create_person_widget(sibling)
                self.siblings_container.addWidget(sibling_widget)
        else:
            placeholder = QLabel("No siblings found")
            placeholder.setStyleSheet("color: gray; font-style: italic;")
            self.siblings_container.addWidget(placeholder)
    
    def _load_marriages(self) -> None:
        """Load and display marriages."""
        while self.marriages_container.count():
            item = self.marriages_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.marriage_widgets.clear()
        
        if not self.current_person or not self.current_person.id:
            placeholder = QLabel("No marriages recorded")
            placeholder.setStyleSheet("color: gray; font-style: italic; padding: 10px;")
            self.marriages_container.addWidget(placeholder)
            return
        
        marriages = self.marriage_repo.get_by_person(self.current_person.id)
        marriages = [m for m in marriages if m.id not in self.deleted_marriage_ids]
        
        # Apply modifications
        for i, m in enumerate(marriages):
            if m.id and m.id in self.modified_marriages:
                marriages[i] = self.modified_marriages[m.id]
        
        all_marriages = marriages + self.new_marriages
        
        # Sort by date (oldest first)
        all_marriages.sort(key=lambda m: (
            (9999, 12) if m.marriage_year is None else (m.marriage_year, m.marriage_month or 0)
        ))
        
        if all_marriages:
            for marriage in all_marriages:
                widget = self._create_marriage_widget(marriage)
                self.marriages_container.addWidget(widget)
                self.marriage_widgets.append((marriage, widget))
        else:
            placeholder = QLabel("No marriages recorded")
            placeholder.setStyleSheet("color: gray; font-style: italic; padding: 10px;")
            self.marriages_container.addWidget(placeholder)
    
    def _load_children(self) -> None:
        """Load and display children."""
        while self.children_container.count():
            item = self.children_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        if not self.current_person or not self.current_person.id:
            return
        
        children = self.person_repo.get_children(self.current_person.id)
        
        if children:
            for child in children:
                child_widget = self._create_person_widget(child)
                self.children_container.addWidget(child_widget)
        else:
            placeholder = QLabel("No children recorded")
            placeholder.setStyleSheet("color: gray; font-style: italic; padding: 10px;")
            self.children_container.addWidget(placeholder)
    
    def get_relationship_data(self) -> dict:
        """Extract relationship data."""
        return {
            'father_id': self.father_selector.get_person_id(),
            'mother_id': self.mother_selector.get_person_id(),
        }
    
    def save_marriages(self) -> None:
        """Save all marriage changes to database."""
        for marriage_id in self.deleted_marriage_ids:
            self.marriage_repo.delete(marriage_id)
        
        for marriage in self.new_marriages:
            for m, widget in self.marriage_widgets:
                if m == marriage:
                    spouse_selector = widget.spouse_selector  # type: ignore[attr-defined]
                    spouse_id = spouse_selector.get_person_id()
                    if spouse_id:
                        marriage.spouse2_id = spouse_id
                    
                    marriage_date_picker = widget.marriage_date  # type: ignore[attr-defined]
                    year, month = marriage_date_picker.get_date()
                    marriage.marriage_year = year
                    marriage.marriage_month = month
                    break
            
            self.marriage_repo.insert(marriage)
        
        for marriage_id, marriage in self.modified_marriages.items():
            for m, widget in self.marriage_widgets:
                if m.id == marriage_id:
                    spouse_selector = widget.spouse_selector  # type: ignore[attr-defined]
                    spouse_id = spouse_selector.get_person_id()
                    
                    if self.current_person and self.current_person.id:
                        if marriage.spouse1_id == self.current_person.id:
                            marriage.spouse2_id = spouse_id
                        else:
                            marriage.spouse1_id = spouse_id
                    
                    marriage_date_picker = widget.marriage_date  # type: ignore[attr-defined]
                    year, month = marriage_date_picker.get_date()
                    marriage.marriage_year = year
                    marriage.marriage_month = month
                    break
            
            self.marriage_repo.update(marriage)
        
        self.new_marriages.clear()
        self.deleted_marriage_ids.clear()
        self.modified_marriages.clear()
    
    def validate(self) -> tuple[bool, str]:
        """Validate relationship data."""
        if not self.current_person:
            return (True, "")
        
        if self.father_selector.get_person_id() == self.current_person.id:
            return (False, "A person cannot be their own father.")
        if self.mother_selector.get_person_id() == self.current_person.id:
            return (False, "A person cannot be their own mother.")
        
        for marriage, widget in self.marriage_widgets:
            marriage_date_picker = widget.marriage_date  # type: ignore[attr-defined]
            marriage_year, marriage_month = marriage_date_picker.get_date()
            
            if not marriage.is_active:
                if marriage.dissolution_year and marriage_year:
                    if marriage.dissolution_year < marriage_year:
                        return (False, "Marriage end date cannot be before start date.")
                    elif marriage.dissolution_year == marriage_year and marriage.dissolution_month and marriage_month:
                        if marriage.dissolution_month < marriage_month:
                            return (False, "Marriage end date cannot be before start date.")
        
        return (True, "")