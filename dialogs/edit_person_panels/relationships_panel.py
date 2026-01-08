"""Relationships panel for Edit Person dialog."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, 
    QLabel, QScrollArea, QCheckBox,
    QGroupBox, QPushButton, QHBoxLayout, 
    QFrame, QMessageBox, QComboBox,
    QDialog
)
from PySide6.QtCore import QSignalBlocker

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from database.person_repository import PersonRepository
from database.marriage_repository import MarriageRepository
from widgets.person_selector import PersonSelector
from widgets.date_picker import DatePicker
from dialogs.create_marriage_dialog import CreateMarriageDialog
from dialogs.end_marriage_dialog import EndMarriageDialog
from models.marriage import Marriage


class RelationshipsPanel(QWidget):
    """Panel for editing person relationships."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Section Labels
    LABEL_PARENTS: str = "Parents"
    LABEL_FATHER: str = "Father:"
    LABEL_MOTHER: str = "Mother:"
    LABEL_SIBLINGS: str = "<b>Siblings:</b>"
    LABEL_MARRIAGES: str = "Marriages"
    LABEL_CHILDREN: str = "Children"
    LABEL_SPOUSE: str = "Spouse:"
    LABEL_MARRIED: str = "Married:"
    LABEL_ENDED: str = "Ended:"
    LABEL_REASON: str = "Reason:"
    LABEL_EMPTY: str = ""
    
    # Button Text
    BUTTON_TEXT_VIEW_PERSON: str = "View Person"
    BUTTON_TEXT_ADD_MARRIAGE: str = "+ Add New Marriage"
    BUTTON_TEXT_ADD_CHILD: str = "+ Add Child"
    BUTTON_TEXT_END_MARRIAGE: str = "End Marriage"
    BUTTON_TEXT_REACTIVATE: str = "Reactivate"
    BUTTON_TEXT_DELETE: str = "Delete"
    BUTTON_TEXT_REMOVE: str = "Remove"
    
    # Checkbox Text
    CHECKBOX_DATE_UNKNOWN: str = "Date Unknown"
    
    # Status Indicators
    STATUS_ACTIVE: str = "✓ Active"
    STATUS_ENDED: str = "○ Ended"
    
    # Placeholder Text
    PLACEHOLDER_NO_SIBLINGS: str = "No siblings found"
    PLACEHOLDER_NO_MARRIAGES: str = "No marriages recorded"
    PLACEHOLDER_NO_CHILDREN: str = "No children recorded"
    
    # Message Box Titles
    MSG_TITLE_SAVE_CHANGES: str = "Save Changes?"
    MSG_TITLE_ACTIVE_MARRIAGE: str = "Active Marriage"
    MSG_TITLE_END_CURRENT_MARRIAGE: str = "End Current Marriage?"
    MSG_TITLE_INCOMPLETE_MARRIAGE: str = "Incomplete Marriage"
    MSG_TITLE_INVALID_DATE: str = "Invalid Date"
    MSG_TITLE_REACTIVATE_MARRIAGE: str = "Reactivate Marriage?"
    MSG_TITLE_DELETE_MARRIAGE: str = "Delete Marriage"
    MSG_TITLE_REMOVE_CHILD: str = "Remove Child"
    
    # Message Box Text
    MSG_TEXT_SAVE_BEFORE_JUMP: str = "Save changes before jumping to another person?"
    MSG_TEXT_ACTIVE_MARRIAGE_PROMPT: str = "This person has an active marriage. End it before creating a new one?"
    MSG_TEXT_END_BEFORE_NEW: str = "This person has an active marriage. End it before creating a new one?"
    MSG_TEXT_INCOMPLETE_MARRIAGE: str = "Please select a spouse for the current marriage before adding a new one."
    MSG_TEXT_INVALID_END_DATE: str = "Marriage cannot end before it started."
    MSG_TEXT_REACTIVATE_MARRIAGE: str = "Remove the end date and reactivate this marriage? This will remove any empty active marriages."
    MSG_TEXT_DELETE_MARRIAGE: str = "Are you sure you want to delete this marriage?"
    MSG_TEXT_REMOVE_CHILD_FORMAT: str = "Remove {child_name} as a child of {parent_name}?"
    MSG_TEXT_REMOVE_CHILD_INFO: str = "This will clear the parent relationship but not delete the person."
    
    # Birth Info Format
    BIRTH_INFO_FORMAT: str = "b. {year}"
    BIRTH_INFO_UNKNOWN: str = "birth unknown"
    
    # Person Display Format
    PERSON_DISPLAY_FORMAT: str = "{name} ({birth})"
    
    # Dissolution Reasons
    REASON_DEATH: str = "Death"
    REASON_DIVORCE: str = "Divorce"
    REASON_ANNULMENT: str = "Annulment"
    REASON_OTHER: str = "Other"
    REASON_UNKNOWN: str = "Unknown"
    
    # Styles
    STYLE_PLACEHOLDER: str = "color: gray; font-style: italic; padding: 10px;"
    STYLE_ACTIVE_STATUS: str = "font-weight: bold; color: green"
    STYLE_ENDED_STATUS: str = "font-weight: bold; color: gray"
    
    # Sorting
    SORT_YEAR_UNKNOWN: int = 9999
    SORT_MONTH_UNKNOWN: int = 12
    
    # Layout
    INDENT_SPACING: int = 60
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        """Initialize relationships panel with database manager."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.person_repo: PersonRepository = PersonRepository(db_manager)
        self.marriage_repo: MarriageRepository = MarriageRepository(db_manager)
        self.current_person: Person | None = None
        
        self.marriage_widgets: list[tuple[Marriage, QFrame]] = []
        self.new_marriages: list[Marriage] = []
        self.deleted_marriage_ids: list[int] = []
        self.modified_marriages: dict[int, Marriage] = {}
        
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create all relationship sections."""
        scroll: QScrollArea = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        container: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout(container)
        
        layout.addWidget(self._create_parents_section())
        layout.addWidget(self._create_marriages_section())
        layout.addWidget(self._create_children_section())
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout: QVBoxLayout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def _create_parents_section(self) -> QGroupBox:
        """Create parents section with father/mother selectors."""
        group: QGroupBox = QGroupBox(self.LABEL_PARENTS)
        layout: QVBoxLayout = QVBoxLayout(group)
        form: QFormLayout = QFormLayout()
        
        self._create_father_row(form)
        self._create_mother_row(form)
        
        layout.addLayout(form)
        
        siblings_label: QLabel = QLabel(self.LABEL_SIBLINGS)
        layout.addWidget(siblings_label)
        
        self.siblings_container: QVBoxLayout = QVBoxLayout()
        layout.addLayout(self.siblings_container)
        
        return group
    
    def _create_father_row(self, form: QFormLayout) -> None:
        """Create father selector row."""
        self.father_selector: PersonSelector = PersonSelector(self.db_manager)
        self.father_selector.set_filter(gender="Male")
        self.father_selector.personSelected.connect(self._mark_dirty)
        self.father_selector.selectionCleared.connect(self._mark_dirty)
        self.father_selector.personSelected.connect(lambda: self._load_siblings())
        
        father_row: QHBoxLayout = QHBoxLayout()
        father_row.addWidget(self.father_selector)
        
        self.father_jump_btn: QPushButton = QPushButton(self.BUTTON_TEXT_VIEW_PERSON)
        self.father_jump_btn.clicked.connect(
            lambda: self._jump_to_person(self.father_selector.get_person_id())
        )
        father_row.addWidget(self.father_jump_btn)
        
        form.addRow(self.LABEL_FATHER, father_row)
    
    def _create_mother_row(self, form: QFormLayout) -> None:
        """Create mother selector row."""
        self.mother_selector: PersonSelector = PersonSelector(self.db_manager)
        self.mother_selector.set_filter(gender="Female")
        self.mother_selector.personSelected.connect(self._mark_dirty)
        self.mother_selector.selectionCleared.connect(self._mark_dirty)
        self.mother_selector.personSelected.connect(lambda: self._load_siblings())
        
        mother_row: QHBoxLayout = QHBoxLayout()
        mother_row.addWidget(self.mother_selector)
        
        self.mother_jump_btn: QPushButton = QPushButton(self.BUTTON_TEXT_VIEW_PERSON)
        self.mother_jump_btn.clicked.connect(
            lambda: self._jump_to_person(self.mother_selector.get_person_id())
        )
        mother_row.addWidget(self.mother_jump_btn)
        
        form.addRow(self.LABEL_MOTHER, mother_row)
    
    def _create_marriages_section(self) -> QGroupBox:
        """Create marriages section with inline editing."""
        group: QGroupBox = QGroupBox(self.LABEL_MARRIAGES)
        layout: QVBoxLayout = QVBoxLayout(group)
        
        self.marriages_container: QVBoxLayout = QVBoxLayout()
        layout.addLayout(self.marriages_container)
        
        add_btn: QPushButton = QPushButton(self.BUTTON_TEXT_ADD_MARRIAGE)
        add_btn.clicked.connect(self._add_marriage)
        layout.addWidget(add_btn)
        
        return group
    
    def _create_children_section(self) -> QGroupBox:
        """Create children section."""
        group: QGroupBox = QGroupBox(self.LABEL_CHILDREN)
        layout: QVBoxLayout = QVBoxLayout(group)
        
        self.children_container: QVBoxLayout = QVBoxLayout()
        layout.addLayout(self.children_container)
        
        add_btn: QPushButton = QPushButton(self.BUTTON_TEXT_ADD_CHILD)
        add_btn.clicked.connect(self._add_child)
        layout.addWidget(add_btn)
        
        return group
    
    # ------------------------------------------------------------------
    # Marriage Widget Creation
    # ------------------------------------------------------------------
    
    def _create_marriage_widget(self, marriage: Marriage) -> QFrame:
        """Create inline editable widget for a marriage."""
        frame: QFrame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        main_layout: QVBoxLayout = QVBoxLayout(frame)
        
        header_layout: QHBoxLayout = self._create_marriage_header(marriage)
        main_layout.addLayout(header_layout)
        
        spouse_layout: QHBoxLayout = self._create_spouse_row(marriage, frame)
        main_layout.addLayout(spouse_layout)
        
        date_unknown_layout: QHBoxLayout = self._create_date_unknown_row(marriage, frame)
        main_layout.addLayout(date_unknown_layout)
        
        marriage_date_layout: QHBoxLayout = self._create_marriage_date_row(marriage, frame)
        main_layout.addLayout(marriage_date_layout)
        
        if not marriage.is_active:
            self._add_dissolution_rows(marriage, frame, main_layout)
        
        button_layout: QHBoxLayout = self._create_marriage_buttons(marriage)
        main_layout.addLayout(button_layout)
        
        return frame
    
    def _create_marriage_header(self, marriage: Marriage) -> QHBoxLayout:
        """Create marriage status header."""
        header_layout: QHBoxLayout = QHBoxLayout()
        
        status_text: str = self.STATUS_ACTIVE if marriage.is_active else self.STATUS_ENDED
        status_style: str = self.STYLE_ACTIVE_STATUS if marriage.is_active else self.STYLE_ENDED_STATUS
        
        status_indicator: QLabel = QLabel(status_text)
        status_indicator.setStyleSheet(status_style)
        header_layout.addWidget(status_indicator)
        header_layout.addStretch()
        
        return header_layout
    
    def _create_spouse_row(self, marriage: Marriage, frame: QFrame) -> QHBoxLayout:
        """Create spouse selector row."""
        spouse_layout: QHBoxLayout = QHBoxLayout()
        spouse_layout.addWidget(QLabel(self.LABEL_SPOUSE))
        
        spouse_selector: PersonSelector = PersonSelector(self.db_manager)
        
        with QSignalBlocker(spouse_selector):
            spouse_id: int | None = self._get_spouse_id_for_marriage(marriage)
            if spouse_id:
                spouse_selector.set_person(spouse_id)
        
        spouse_selector.personSelected.connect(self._mark_dirty)
        spouse_layout.addWidget(spouse_selector)
        
        spouse_jump_btn: QPushButton = QPushButton(self.BUTTON_TEXT_VIEW_PERSON)
        spouse_jump_btn.setEnabled(spouse_id is not None)
        spouse_jump_btn.clicked.connect(lambda: self._jump_to_person(spouse_selector.get_person_id()))
        spouse_selector.personSelected.connect(lambda: spouse_jump_btn.setEnabled(True))
        spouse_selector.selectionCleared.connect(lambda: spouse_jump_btn.setEnabled(False))
        spouse_layout.addWidget(spouse_jump_btn)
        
        frame.spouse_selector = spouse_selector  # type: ignore[attr-defined]
        
        return spouse_layout
    
    def _get_spouse_id_for_marriage(self, marriage: Marriage) -> int | None:
        """Get spouse ID for current person in marriage."""
        if not self.current_person or not self.current_person.id:
            return None
        
        return self.marriage_repo.get_spouse_id(marriage, self.current_person.id)
    
    def _create_date_unknown_row(self, marriage: Marriage, frame: QFrame) -> QHBoxLayout:
        """Create date unknown checkbox row."""
        date_unknown_layout: QHBoxLayout = QHBoxLayout()
        date_unknown_layout.addSpacing(self.INDENT_SPACING)
        
        date_unknown_check: QCheckBox = QCheckBox(self.CHECKBOX_DATE_UNKNOWN)
        date_unknown_check.setChecked(marriage.marriage_year is None)
        date_unknown_layout.addWidget(date_unknown_check)
        date_unknown_layout.addStretch()
        
        frame.date_unknown_check = date_unknown_check  # type: ignore[attr-defined]
        
        return date_unknown_layout
    
    def _create_marriage_date_row(self, marriage: Marriage, frame: QFrame) -> QHBoxLayout:
        """Create marriage date picker row."""
        marriage_date_layout: QHBoxLayout = QHBoxLayout()
        
        marriage_date_label: QLabel = QLabel(self.LABEL_MARRIED)
        marriage_date_layout.addWidget(marriage_date_label)
        
        marriage_date: DatePicker = DatePicker()
        with QSignalBlocker(marriage_date):
            if marriage.marriage_year:
                marriage_date.set_date(marriage.marriage_year, marriage.marriage_month or 1)
            else:
                marriage_date.set_date(1721, 1)
        
        marriage_date.unknown_check.setVisible(False)
        marriage_date.dateChanged.connect(self._mark_dirty)
        marriage_date_layout.addWidget(marriage_date)
        marriage_date_layout.addStretch()
        
        date_known: bool = marriage.marriage_year is not None
        marriage_date_label.setVisible(date_known)
        marriage_date.setVisible(date_known)
        
        date_unknown_check: QCheckBox = frame.date_unknown_check  # type: ignore[attr-defined]
        date_unknown_check.stateChanged.connect(
            lambda: self._toggle_marriage_date_visibility(
                date_unknown_check,
                marriage_date_label,
                marriage_date
            )
        )
        
        frame.marriage_date = marriage_date  # type: ignore[attr-defined]
        
        return marriage_date_layout
    
    def _toggle_marriage_date_visibility(
        self,
        checkbox: QCheckBox,
        label: QLabel,
        picker: DatePicker
    ) -> None:
        """Toggle marriage date visibility based on checkbox."""
        date_is_known: bool = not checkbox.isChecked()
        label.setVisible(date_is_known)
        picker.setVisible(date_is_known)
        self._mark_dirty()
    
    def _add_dissolution_rows(self, marriage: Marriage, frame: QFrame, layout: QVBoxLayout) -> None:
        """Add dissolution date and reason rows for ended marriages."""
        end_date_layout: QHBoxLayout = self._create_end_date_row(marriage, frame)
        layout.addLayout(end_date_layout)
        
        reason_layout: QHBoxLayout = self._create_reason_row(marriage, frame)
        layout.addLayout(reason_layout)
    
    def _create_end_date_row(self, marriage: Marriage, frame: QFrame) -> QHBoxLayout:
        """Create end date picker row."""
        end_date_layout: QHBoxLayout = QHBoxLayout()
        end_date_layout.addWidget(QLabel(self.LABEL_ENDED))
        
        end_date: DatePicker = DatePicker()
        with QSignalBlocker(end_date):
            if marriage.dissolution_year:
                end_date.set_date(marriage.dissolution_year, marriage.dissolution_month)
        
        end_date.dateChanged.connect(self._mark_dirty)
        end_date_layout.addWidget(end_date)
        end_date_layout.addStretch()
        
        frame.end_date = end_date  # type: ignore[attr-defined]
        
        return end_date_layout
    
    def _create_reason_row(self, marriage: Marriage, frame: QFrame) -> QHBoxLayout:
        """Create dissolution reason combo box row."""
        reason_layout: QHBoxLayout = QHBoxLayout()
        reason_layout.addWidget(QLabel(self.LABEL_REASON))
        
        reason_combo: QComboBox = QComboBox()
        with QSignalBlocker(reason_combo):
            reason_combo.addItems([
                self.REASON_DEATH,
                self.REASON_DIVORCE,
                self.REASON_ANNULMENT,
                self.REASON_OTHER,
                self.REASON_UNKNOWN
            ])
            if marriage.dissolution_reason:
                index: int = reason_combo.findText(marriage.dissolution_reason)
                if index >= 0:
                    reason_combo.setCurrentIndex(index)
        
        reason_combo.currentIndexChanged.connect(self._mark_dirty)
        reason_layout.addWidget(reason_combo)
        reason_layout.addStretch()
        
        frame.reason_combo = reason_combo  # type: ignore[attr-defined]
        
        return reason_layout
    
    def _create_marriage_buttons(self, marriage: Marriage) -> QHBoxLayout:
        """Create action buttons for marriage."""
        button_layout: QHBoxLayout = QHBoxLayout()
        button_layout.addStretch()
        
        if marriage.is_active:
            end_btn: QPushButton = QPushButton(self.BUTTON_TEXT_END_MARRIAGE)
            end_btn.clicked.connect(lambda: self._end_marriage(marriage))
            button_layout.addWidget(end_btn)
        else:
            reactivate_btn: QPushButton = QPushButton(self.BUTTON_TEXT_REACTIVATE)
            reactivate_btn.clicked.connect(lambda: self._reactivate_marriage(marriage))
            button_layout.addWidget(reactivate_btn)
        
        delete_btn: QPushButton = QPushButton(self.BUTTON_TEXT_DELETE)
        delete_btn.clicked.connect(lambda: self._delete_marriage(marriage))
        button_layout.addWidget(delete_btn)
        
        return button_layout
    
    # ------------------------------------------------------------------
    # Person Widget Creation
    # ------------------------------------------------------------------
    
    def _create_person_widget(self, person: Person, show_remove: bool = False) -> QFrame:
        """Create widget displaying a person with jump button."""
        frame: QFrame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout: QHBoxLayout = QHBoxLayout(frame)
        
        birth_info: str = self._format_birth_info(person)
        info_text: str = self.PERSON_DISPLAY_FORMAT.format(
            name=person.display_name,
            birth=birth_info
        )
        info_label: QLabel = QLabel(info_text)
        layout.addWidget(info_label)
        layout.addStretch()
        
        jump_btn: QPushButton = QPushButton(self.BUTTON_TEXT_VIEW_PERSON)
        jump_btn.clicked.connect(lambda: self._jump_to_person(person.id))
        layout.addWidget(jump_btn)
        
        if show_remove:
            remove_btn: QPushButton = QPushButton(self.BUTTON_TEXT_REMOVE)
            remove_btn.clicked.connect(lambda: self._remove_child(person))
            layout.addWidget(remove_btn)
        
        return frame
    
    def _format_birth_info(self, person: Person) -> str:
        """Format birth information for person display."""
        if person.birth_year:
            return self.BIRTH_INFO_FORMAT.format(year=person.birth_year)
        return self.BIRTH_INFO_UNKNOWN
    
    # ------------------------------------------------------------------
    # Parent Dialog Communication
    # ------------------------------------------------------------------
    
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
    
    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    
    def _jump_to_person(self, person_id: int | None) -> None:
        """Jump to editing a different person."""
        if person_id is None:
            return
        
        dialog = self._find_parent_dialog()
        if not dialog:
            return
        
        person: Person | None = self.person_repo.get_by_id(person_id)
        if not person:
            return
        
        if dialog.has_unsaved_changes:
            if not self._confirm_save_before_jump(dialog):
                return
        
        self._switch_to_person(dialog, person)
    
    def _confirm_save_before_jump(self, dialog) -> bool:
        """Confirm whether to save changes before jumping to another person."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(self.MSG_TITLE_SAVE_CHANGES)
        msg.setText(self.MSG_TEXT_SAVE_BEFORE_JUMP)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        
        result = msg.exec()
        
        if result == QMessageBox.StandardButton.Cancel:
            return False
        
        if result == QMessageBox.StandardButton.Save:
            return dialog._save_changes()
        
        return True
    
    def _switch_to_person(self, dialog, person: Person) -> None:
        """Switch dialog to display different person."""
        dialog.person = person
        dialog.setWindowTitle(f"Edit Person: {person.display_name}")
        dialog._load_data()
        dialog.has_unsaved_changes = False
        dialog.panel_list.setCurrentRow(1)
    
    # ------------------------------------------------------------------
    # Marriage Management
    # ------------------------------------------------------------------

    def _add_marriage(self) -> None:
        """Add a new marriage using dialog."""
        if not self.current_person or not self.current_person.id:
            return
        
        if not self._validate_existing_marriages():
            return
        
        active_marriages: list[Marriage] = self._get_active_marriages()
        
        if not active_marriages:
            self._open_create_marriage_dialog()
            return
        
        result: bool | None = self._handle_active_marriage_before_new(active_marriages[0])
        
        if result is None:
            return
        
        self._open_create_marriage_dialog()

    def _get_active_marriages(self) -> list[Marriage]:
        """Get list of currently active marriages."""
        return [m for m, _ in self.marriage_widgets if m.is_active]

    def _validate_existing_marriages(self) -> bool:
        """Validate that all active marriages have spouses selected."""
        for marriage, widget in self.marriage_widgets:
            if not marriage.is_active:
                continue
            
            if not self._has_spouse_selected(widget):
                self._show_incomplete_marriage_error()
                return False
        
        return True

    def _has_spouse_selected(self, widget: QFrame) -> bool:
        """Check if marriage widget has a spouse selected."""
        spouse_selector: PersonSelector = widget.spouse_selector  # type: ignore[attr-defined]
        return spouse_selector.get_person_id() is not None

    def _show_incomplete_marriage_error(self) -> None:
        """Show error message for incomplete marriage."""
        QMessageBox.warning(
            self,
            self.MSG_TITLE_INCOMPLETE_MARRIAGE,
            self.MSG_TEXT_INCOMPLETE_MARRIAGE
        )

    def _handle_active_marriage_before_new(self, active_marriage: Marriage) -> bool | None:
        """
        Handle existing active marriage before creating new one.
        
        Returns:
            True: User ended the marriage, proceed with new marriage
            False: User wants to create new marriage anyway (keep current active)
            None: User cancelled, don't create new marriage
        """
        reply: QMessageBox.StandardButton = self._show_active_marriage_prompt()
        
        if reply == QMessageBox.StandardButton.Cancel:
            return None
        
        if reply == QMessageBox.StandardButton.No:
            return False
        
        return self._end_marriage_with_dialog(active_marriage)

    def _show_active_marriage_prompt(self) -> QMessageBox.StandardButton:
        """Show prompt asking user how to handle active marriage."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(self.MSG_TITLE_END_CURRENT_MARRIAGE)
        msg.setText(self.MSG_TEXT_END_BEFORE_NEW)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No |
            QMessageBox.StandardButton.Cancel
        )
        
        result: int = msg.exec()
        return QMessageBox.StandardButton(result)

    def _end_marriage_with_dialog(self, active_marriage: Marriage) -> bool | None:
        """Open end marriage dialog and process result."""
        end_dialog: EndMarriageDialog = EndMarriageDialog(active_marriage, self)
        
        if end_dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        
        self._apply_marriage_dissolution(active_marriage, end_dialog)
        return True

    def _apply_marriage_dissolution(self, marriage: Marriage, dialog: EndMarriageDialog) -> None:
        """Apply dissolution data from dialog to marriage."""
        year, month, reason = dialog.get_dissolution_data()
        
        marriage.dissolution_year = year
        marriage.dissolution_month = month
        marriage.dissolution_reason = reason
        
        if marriage.id:
            self.modified_marriages[marriage.id] = marriage
        
        self._load_marriages()
        self._mark_dirty()

    def _open_create_marriage_dialog(self) -> None:
        """Open dialog to create new marriage."""
        from dialogs.create_marriage_dialog import CreateMarriageDialog
        
        if not self.current_person:
            return
        
        dialog: CreateMarriageDialog = CreateMarriageDialog(
            self.db_manager,
            self.current_person,
            self
        )
        
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        self._create_marriage_from_dialog(dialog)

    def _create_marriage_from_dialog(self, dialog: CreateMarriageDialog) -> None:
        """Create marriage object from dialog data."""
        spouse_id, year, month = dialog.get_marriage_data()
        
        new_marriage: Marriage = Marriage(
            spouse1_id=self.current_person.id,  # type: ignore[union-attr]
            spouse2_id=spouse_id,
            marriage_year=year,
            marriage_month=month
        )
        
        self.new_marriages.append(new_marriage)
        self._load_marriages()
        self._mark_dirty()

    def _end_marriage(self, marriage: Marriage) -> None:
        """End a marriage with dialog."""
        dialog: EndMarriageDialog = EndMarriageDialog(marriage, self)
        
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        year, month, reason = dialog.get_dissolution_data()
        
        if not self._validate_end_date(marriage, year, month):
            return
        
        self._update_marriage_dissolution(marriage, year, month, reason)

    def _update_marriage_dissolution(
        self,
        marriage: Marriage,
        year: int | None,
        month: int | None,
        reason: str
    ) -> None:
        """Update marriage with dissolution data."""
        marriage.dissolution_year = year
        marriage.dissolution_month = month
        marriage.dissolution_reason = reason
        
        if marriage.id:
            self.modified_marriages[marriage.id] = marriage
        
        self._load_marriages()
        self._mark_dirty()

    def _validate_end_date(
        self,
        marriage: Marriage,
        end_year: int | None,
        end_month: int | None
    ) -> bool:
        """Validate that end date is after marriage date."""
        if not marriage.marriage_year or not end_year:
            return True
        
        if self._is_end_before_start(marriage, end_year, end_month):
            self._show_invalid_end_date_error()
            return False
        
        return True

    def _is_end_before_start(
        self,
        marriage: Marriage,
        end_year: int,
        end_month: int | None
    ) -> bool:
        """Check if end date is before marriage start date."""
        if end_year < marriage.marriage_year:  # type: ignore[operator]
            return True
        
        if end_year == marriage.marriage_year:
            if marriage.marriage_month and end_month:
                if end_month < marriage.marriage_month:
                    return True
        
        return False

    def _show_invalid_end_date_error(self) -> None:
        """Show error for invalid end date."""
        QMessageBox.warning(
            self,
            self.MSG_TITLE_INVALID_DATE,
            self.MSG_TEXT_INVALID_END_DATE
        )

    def _reactivate_marriage(self, marriage: Marriage) -> None:
        """Reactivate an ended marriage."""
        if not self._confirm_reactivate_marriage():
            return
        
        self._delete_empty_active_marriages()
        self._clear_marriage_dissolution(marriage)
        self._load_marriages()
        self._mark_dirty()

    def _clear_marriage_dissolution(self, marriage: Marriage) -> None:
        """Clear dissolution data from marriage."""
        marriage.dissolution_year = None
        marriage.dissolution_month = None
        marriage.dissolution_day = None
        marriage.dissolution_reason = ""
        
        if marriage.id:
            self.modified_marriages[marriage.id] = marriage

    def _confirm_reactivate_marriage(self) -> bool:
        """Confirm reactivation of ended marriage."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(self.MSG_TITLE_REACTIVATE_MARRIAGE)
        msg.setText(self.MSG_TEXT_REACTIVATE_MARRIAGE)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        return msg.exec() == QMessageBox.StandardButton.Yes

    def _delete_empty_active_marriages(self) -> None:
        """Delete any active marriages that have no spouse selected."""
        for m, widget in list(self.marriage_widgets):
            if not m.is_active:
                continue
            
            if self._has_spouse_selected(widget):
                continue
            
            self._mark_marriage_for_deletion(m)

    def _mark_marriage_for_deletion(self, marriage: Marriage) -> None:
        """Mark marriage for deletion."""
        if marriage.id:
            self.deleted_marriage_ids.append(marriage.id)
        
        if marriage in self.new_marriages:
            self.new_marriages.remove(marriage)

    def _delete_marriage(self, marriage: Marriage) -> None:
        """Delete a marriage after confirmation."""
        if not self._confirm_delete_marriage():
            return
        
        self._mark_marriage_for_deletion(marriage)
        self._remove_marriage_widget(marriage)
        self._load_marriages()
        self._mark_dirty()

    def _remove_marriage_widget(self, marriage: Marriage) -> None:
        """Remove marriage from widget list."""
        self.marriage_widgets = [
            (m, w) for m, w in self.marriage_widgets if m != marriage
        ]

    def _confirm_delete_marriage(self) -> bool:
        """Confirm deletion of marriage."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.MSG_TITLE_DELETE_MARRIAGE)
        msg.setText(self.MSG_TEXT_DELETE_MARRIAGE)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        return msg.exec() == QMessageBox.StandardButton.Yes

    # ------------------------------------------------------------------
    # Child Management
    # ------------------------------------------------------------------
    
    def _add_child(self) -> None:
        """Open dialog to create a new child."""
        if not self.current_person or not self.current_person.id:
            return
        
        parent2_id: int | None = self._find_oldest_active_marriage_spouse()
        
        self._open_create_child_dialog(parent2_id)
    
    def _find_oldest_active_marriage_spouse(self) -> int | None:
        """Find spouse from oldest active marriage."""
        active_marriages: list[Marriage] = self.marriage_repo.get_active_marriages(
            self.current_person.id  # type: ignore[arg-type]
        )
        
        if not active_marriages:
            return None
        
        active_marriages.sort(key=self._get_marriage_sort_key)
        oldest_marriage: Marriage = active_marriages[0]
        
        return self.marriage_repo.get_spouse_id(
            oldest_marriage,
            self.current_person.id  # type: ignore[arg-type]
        )
    
    def _get_marriage_sort_key(self, marriage: Marriage) -> tuple[int, int]:
        """Get sort key for marriage based on date."""
        if marriage.marriage_year is None:
            return (self.SORT_YEAR_UNKNOWN, self.SORT_MONTH_UNKNOWN)
        
        return (marriage.marriage_year, marriage.marriage_month or 0)
    
    def _open_create_child_dialog(self, parent2_id: int | None) -> None:
        """Open dialog to create child."""
        from dialogs.create_child_dialog import CreateChildDialog
        
        if not self.current_person:
            return
        
        dialog: CreateChildDialog = CreateChildDialog(
            self.db_manager,
            self.current_person,
            parent2_id,
            self
        )
        
        if not dialog.exec():
            return
        
        created_person: Person | None = dialog.get_created_person()
        if created_person:
            self._load_children()
            self._mark_dirty()
    
    def _remove_child(self, child: Person) -> None:
        """Remove parent-child relationship."""
        if not self.current_person:
            return
        
        if not self._confirm_remove_child(child):
            return
        
        self._clear_parent_relationship(child)
        self.person_repo.update(child)
        
        self._load_children()
        self._mark_dirty()
    
    def _confirm_remove_child(self, child: Person) -> bool:
        """Confirm removal of child relationship."""
        if not self.current_person:
            return False
        
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.MSG_TITLE_REMOVE_CHILD)
        msg.setText(self.MSG_TEXT_REMOVE_CHILD_FORMAT.format(
            child_name=child.display_name,
            parent_name=self.current_person.display_name
        ))
        msg.setInformativeText(self.MSG_TEXT_REMOVE_CHILD_INFO)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        return msg.exec() == QMessageBox.StandardButton.Yes
    
    def _clear_parent_relationship(self, child: Person) -> None:
        """Clear parent IDs from child."""
        if not self.current_person:
            return
        
        if child.father_id == self.current_person.id:
            child.father_id = None
        
        if child.mother_id == self.current_person.id:
            child.mother_id = None
    
    # ------------------------------------------------------------------
    # Data Loading
    # ------------------------------------------------------------------
    
    def load_person(self, person: Person) -> None:
        """Load person relationship data."""
        self.current_person = person
        
        self.new_marriages.clear()
        self.deleted_marriage_ids.clear()
        self.modified_marriages.clear()
        
        blockers: list[QSignalBlocker] = [
            QSignalBlocker(self.father_selector),
            QSignalBlocker(self.mother_selector),
        ]
        
        self._load_parent_selectors(person)
        self._load_siblings()
        self._load_marriages()
        self._load_children()
    
    def _load_parent_selectors(self, person: Person) -> None:
        """Load father and mother selectors."""
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
    
    def _load_siblings(self) -> None:
        """Load and display siblings."""
        self._clear_container(self.siblings_container)
        
        if not self.current_person:
            return
        
        siblings: list[Person] = self._get_siblings()
        
        if siblings:
            self._display_siblings(siblings)
        else:
            self._show_placeholder(self.siblings_container, self.PLACEHOLDER_NO_SIBLINGS)
    
    def _get_siblings(self) -> list[Person]:
        """Get list of siblings from both parents."""
        if not self.current_person or not self.current_person.id:
            return []
        
        siblings: list[Person] = []
        
        self._add_siblings_from_parent(self.father_selector.get_person_id(), siblings)
        self._add_siblings_from_parent(self.mother_selector.get_person_id(), siblings)
        
        return siblings

    def _add_siblings_from_parent(self, parent_id: int | None, siblings: list[Person]) -> None:
        """Add siblings from a specific parent to the siblings list."""
        if not parent_id or not self.current_person:
            return
        
        children: list[Person] = self.person_repo.get_children(parent_id)
        
        for child in children:
            if self._is_valid_sibling(child, siblings):
                siblings.append(child)

    def _is_valid_sibling(self, child: Person, existing_siblings: list[Person]) -> bool:
        """Check if child is a valid sibling (not self, not already in list)."""
        if not self.current_person:
            return False
        
        if child.id == self.current_person.id:
            return False
        
        if child in existing_siblings:
            return False
        
        return True
    
    def _display_siblings(self, siblings: list[Person]) -> None:
        """Display siblings in container."""
        for sibling in siblings:
            sibling_widget: QFrame = self._create_person_widget(sibling)
            self.siblings_container.addWidget(sibling_widget)
    
    def _load_marriages(self) -> None:
        """Load and display marriages."""
        self._clear_container(self.marriages_container)
        self.marriage_widgets.clear()
        
        if not self.current_person or not self.current_person.id:
            self._show_placeholder(self.marriages_container, self.PLACEHOLDER_NO_MARRIAGES)
            return
        
        all_marriages: list[Marriage] = self._get_all_marriages()
        
        if all_marriages:
            self._display_marriages(all_marriages)
        else:
            self._show_placeholder(self.marriages_container, self.PLACEHOLDER_NO_MARRIAGES)
    
    def _get_all_marriages(self) -> list[Marriage]:
        """Get all marriages (database + new - deleted), sorted by date."""
        if not self.current_person or self.current_person.id is None:
            return []
        
        marriages: list[Marriage] = self.marriage_repo.get_by_person(self.current_person.id)
        marriages = [m for m in marriages if m.id not in self.deleted_marriage_ids]
        
        marriages = self._apply_marriage_modifications(marriages)
        
        all_marriages: list[Marriage] = marriages + self.new_marriages
        all_marriages.sort(key=self._get_marriage_sort_key)
        
        return all_marriages
    
    def _apply_marriage_modifications(self, marriages: list[Marriage]) -> list[Marriage]:
        """Apply any modified marriage data."""
        return [
            self.modified_marriages[m.id] if m.id and m.id in self.modified_marriages else m
            for m in marriages
        ]
    
    def _display_marriages(self, marriages: list[Marriage]) -> None:
        """Display marriages in container."""
        for marriage in marriages:
            widget: QFrame = self._create_marriage_widget(marriage)
            self.marriages_container.addWidget(widget)
            self.marriage_widgets.append((marriage, widget))
    
    def _load_children(self) -> None:
        """Load and display children."""
        self._clear_container(self.children_container)
        
        if not self.current_person or not self.current_person.id:
            return
        
        children: list[Person] = self.person_repo.get_children(self.current_person.id)
        
        if children:
            self._display_children(children)
        else:
            self._show_placeholder(self.children_container, self.PLACEHOLDER_NO_CHILDREN)
    
    def _display_children(self, children: list[Person]) -> None:
        """Display children in container."""
        for child in children:
            child_widget: QFrame = self._create_person_widget(child, show_remove=True)
            self.children_container.addWidget(child_widget)
    
    def _clear_container(self, container: QVBoxLayout) -> None:
        """Clear all widgets from a container."""
        while container.count():
            item = container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def _show_placeholder(self, container: QVBoxLayout, text: str) -> None:
        """Show placeholder text in container."""
        placeholder: QLabel = QLabel(text)
        placeholder.setStyleSheet(self.STYLE_PLACEHOLDER)
        container.addWidget(placeholder)
    
    # ------------------------------------------------------------------
    # Data Extraction
    # ------------------------------------------------------------------
    
    def get_relationship_data(self) -> dict:
        """Extract relationship data."""
        return {
            'father_id': self.father_selector.get_person_id(),
            'mother_id': self.mother_selector.get_person_id(),
        }
    
    # ------------------------------------------------------------------
    # Data Persistence
    # ------------------------------------------------------------------
    
    def save_marriages(self) -> None:
        """Save all marriage changes to database."""
        for marriage_id in self.deleted_marriage_ids:
            self.marriage_repo.delete(marriage_id)
        
        for marriage in self.new_marriages:
            self._update_marriage_from_widget(marriage)
            self.marriage_repo.insert(marriage)
        
        for marriage, widget in self.marriage_widgets:
            if marriage in self.new_marriages:
                continue
            
            if marriage.id:
                self._update_marriage_from_widget(marriage, widget)
                self.marriage_repo.update(marriage)
        
        self.new_marriages.clear()
        self.deleted_marriage_ids.clear()
        self.modified_marriages.clear()
    
    def _update_marriage_from_widget(self, marriage: Marriage, widget: QFrame | None = None) -> None:
        """Update marriage object from widget values."""
        if widget is None:
            widget = self._find_widget_for_marriage(marriage)
        
        if widget is None:
            return
        
        self._update_marriage_spouse(marriage, widget)
        self._update_marriage_date(marriage, widget)
    
    def _find_widget_for_marriage(self, marriage: Marriage) -> QFrame | None:
        """Find widget associated with marriage."""
        for m, w in self.marriage_widgets:
            if m == marriage:
                return w
        return None
    
    def _update_marriage_spouse(self, marriage: Marriage, widget: QFrame) -> None:
        """Update marriage spouse IDs from widget."""
        spouse_selector: PersonSelector = widget.spouse_selector  # type: ignore[attr-defined]
        spouse_id: int | None = spouse_selector.get_person_id()
        
        if not self.current_person or not self.current_person.id:
            return
        
        if marriage.spouse1_id == self.current_person.id:
            marriage.spouse2_id = spouse_id
        else:
            marriage.spouse1_id = spouse_id
    
    def _update_marriage_date(self, marriage: Marriage, widget: QFrame) -> None:
        """Update marriage date from widget."""
        date_unknown_check: QCheckBox = widget.date_unknown_check  # type: ignore[attr-defined]
        
        if date_unknown_check.isChecked():
            marriage.marriage_year = None
            marriage.marriage_month = None
        else:
            marriage_date_picker: DatePicker = widget.marriage_date  # type: ignore[attr-defined]
            year, month = marriage_date_picker.get_date()
            marriage.marriage_year = year
            marriage.marriage_month = month
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def validate(self) -> tuple[bool, str]:
        """Validate relationship data."""
        if not self.current_person:
            return (True, "")
        
        if self.father_selector.get_person_id() == self.current_person.id:
            return (False, "A person cannot be their own father.")
        
        if self.mother_selector.get_person_id() == self.current_person.id:
            return (False, "A person cannot be their own mother.")
        
        for marriage, widget in self.marriage_widgets:
            is_valid, error_msg = self._validate_marriage_dates(marriage, widget)
            if not is_valid:
                return (False, error_msg)
        
        return (True, "")
    
    def _validate_marriage_dates(self, marriage: Marriage, widget: QFrame) -> tuple[bool, str]:
        """Validate marriage date ranges."""
        marriage_date_picker: DatePicker = widget.marriage_date  # type: ignore[attr-defined]
        marriage_year, marriage_month = marriage_date_picker.get_date()
        
        if marriage.is_active:
            return (True, "")
        
        if not marriage.dissolution_year or not marriage_year:
            return (True, "")
        
        if marriage.dissolution_year < marriage_year:
            return (False, "Marriage end date cannot be before start date.")
        
        if marriage.dissolution_year == marriage_year:
            if marriage.dissolution_month and marriage_month:
                if marriage.dissolution_month < marriage_month:
                    return (False, "Marriage end date cannot be before start date.")
        
        return (True, "")