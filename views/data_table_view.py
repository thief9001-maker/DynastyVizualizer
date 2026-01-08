"""Data table view for displaying all people."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QMenu, QMessageBox, QLineEdit, QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from utils.text_normalizer import TextNormalizer
from utils.date_formatter import DateFormatter, DateParts, MonthStyle

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from database.person_repository import PersonRepository


class DataTableView(QWidget):
    """Widget displaying all people in a sortable, filterable table."""

    # Signals
    person_edited: Signal = Signal()

    # Table Column Configuration
    COLUMN_NUMBER: int = 0
    COLUMN_NAME: int = 1
    COLUMN_GENDER: int = 2
    COLUMN_BIRTH_DATE: int = 3
    COLUMN_DEATH_DATE: int = 4
    COLUMN_COUNT: int = 5
    
    COLUMN_HEADERS: list[str] = [
        "#",
        "Name",
        "Gender",
        "Birth Date",
        "Death Date"
    ]

    # UI Configuration
    SEARCH_PLACEHOLDER: str = "Filter by name..."
    SEARCH_MAX_WIDTH: int = 300
    
    DISPLAY_NUMBER_FORMAT: str = "{:06d}"
    DISPLAY_NUMBER_START: int = 1
    
    BUTTON_TEXT_ADD: str = "+ Add Person"
    BUTTON_TEXT_REFRESH: str = "Refresh"
    LABEL_TEXT_SEARCH: str = "Search:"

    # Dialog Messages
    MSG_NO_SELECTION_TITLE: str = "No Selection"
    MSG_NO_SELECTION_EDIT: str = "Please select a person to edit."
    MSG_NO_SELECTION_DELETE: str = "Please select a person to delete."
    
    MSG_DELETE_TITLE: str = "Delete Person"
    MSG_DELETE_TEXT: str = "Delete {name}?"
    MSG_DELETE_INFO: str = "This will also delete all their marriages, events, and relationships."

    # Context Menu
    ACTION_TEXT_EDIT: str = "Edit Person"
    ACTION_TEXT_DELETE: str = "Delete Person"

    # Display Defaults
    DEFAULT_GENDER_DISPLAY: str = "Unknown"
    EMPTY_DATE_DISPLAY: str = ""

    # Date Formatting
    DATE_MONTH_STYLE: MonthStyle = MonthStyle.ABBREVIATED
    DATE_SEPARATOR: str = " "
    SORT_VALUE_UNKNOWN_MONTH: int = 0
    SORT_VALUE_UNKNOWN_DAY: int = 0

    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        """Initialize data table view with database manager."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.person_repo: PersonRepository = PersonRepository(db_manager)
        self.people: list[Person] = []
        self.person_display_numbers: dict[int, int] = {}
        
        self._setup_ui()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create the table and controls."""
        layout: QVBoxLayout = QVBoxLayout(self)
        
        toolbar: QHBoxLayout = self._create_toolbar()
        layout.addLayout(toolbar)
        
        self.table: QTableWidget = self._create_table()
        layout.addWidget(self.table)
    
    def _create_toolbar(self) -> QHBoxLayout:
        """Create toolbar with search and action buttons."""
        toolbar: QHBoxLayout = QHBoxLayout()
        
        toolbar.addWidget(QLabel(self.LABEL_TEXT_SEARCH))
        
        self.search_input: QLineEdit = QLineEdit()
        self.search_input.setPlaceholderText(self.SEARCH_PLACEHOLDER)
        self.search_input.textChanged.connect(self._filter_table)
        self.search_input.setMaximumWidth(self.SEARCH_MAX_WIDTH)
        toolbar.addWidget(self.search_input)
        
        toolbar.addStretch()
        
        add_btn: QPushButton = QPushButton(self.BUTTON_TEXT_ADD)
        add_btn.clicked.connect(self._add_person)
        toolbar.addWidget(add_btn)
        
        refresh_btn: QPushButton = QPushButton(self.BUTTON_TEXT_REFRESH)
        refresh_btn.clicked.connect(self.refresh_data)
        toolbar.addWidget(refresh_btn)
        
        return toolbar
    
    def _create_table(self) -> QTableWidget:
        """Create and configure the main data table."""
        table: QTableWidget = QTableWidget()
        table.setColumnCount(self.COLUMN_COUNT)
        table.setHorizontalHeaderLabels(self.COLUMN_HEADERS)
        
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSortingEnabled(True)
        table.setAlternatingRowColors(True)
        
        self._configure_table_columns(table)
        
        table.doubleClicked.connect(self._on_row_double_clicked)
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table.customContextMenuRequested.connect(self._show_context_menu)
        
        return table
    
    def _configure_table_columns(self, table: QTableWidget) -> None:
        """Configure column resize modes for table."""
        header: QHeaderView = table.horizontalHeader()
        header.setSectionResizeMode(self.COLUMN_NUMBER, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMN_NAME, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(self.COLUMN_GENDER, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMN_BIRTH_DATE, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMN_DEATH_DATE, QHeaderView.ResizeMode.ResizeToContents)
    
    # ------------------------------------------------------------------
    # Data Management
    # ------------------------------------------------------------------
    
    def refresh_data(self) -> None:
        """Load all people from database and assign persistent display numbers."""
        self.people = self.person_repo.get_all()
        self.people.sort(key=lambda p: p.id or 0)
        
        self._assign_display_numbers()
        self._populate_table(self.people)
    
    def _assign_display_numbers(self) -> None:
        """Assign persistent display numbers to people based on ID order."""
        self.person_display_numbers.clear()
        for index, person in enumerate(self.people, start=self.DISPLAY_NUMBER_START):
            if person.id:
                self.person_display_numbers[person.id] = index
    
    def _populate_table(self, people: list[Person]) -> None:
        """Fill table with person data."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        for person in people:
            self._add_person_row(person)
        
        self.table.setSortingEnabled(True)
    
    def _add_person_row(self, person: Person) -> None:
        """Add a single person as a row in the table."""
        row: int = self.table.rowCount()
        self.table.insertRow(row)
        
        self._set_number_cell(row, person)
        self._set_name_cell(row, person)
        self._set_gender_cell(row, person)
        self._set_birth_date_cell(row, person)
        self._set_death_date_cell(row, person)
    
    def _set_number_cell(self, row: int, person: Person) -> None:
        """Set the display number cell for a person."""
        display_num: int = self.person_display_numbers.get(person.id or 0, 0)
        display_text: str = self.DISPLAY_NUMBER_FORMAT.format(display_num)
        
        item: QTableWidgetItem = QTableWidgetItem(display_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setData(Qt.ItemDataRole.UserRole, person.id)
        item.setData(Qt.ItemDataRole.UserRole + 1, display_num)
        
        self.table.setItem(row, self.COLUMN_NUMBER, item)
    
    def _set_name_cell(self, row: int, person: Person) -> None:
        """Set the name cell for a person."""
        item: QTableWidgetItem = QTableWidgetItem(person.display_name)
        self.table.setItem(row, self.COLUMN_NAME, item)
    
    def _set_gender_cell(self, row: int, person: Person) -> None:
        """Set the gender cell for a person."""
        gender_text: str = person.gender or self.DEFAULT_GENDER_DISPLAY
        
        item: QTableWidgetItem = QTableWidgetItem(gender_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.table.setItem(row, self.COLUMN_GENDER, item)
    
    def _set_birth_date_cell(self, row: int, person: Person) -> None:
        """Set the birth date cell for a person."""
        if person.birth_year is None:
            item: QTableWidgetItem = QTableWidgetItem(self.EMPTY_DATE_DISPLAY)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, self.COLUMN_BIRTH_DATE, item)
            return
        
        date_parts: DateParts = DateParts(
            year=person.birth_year,
            month=person.birth_month,
            day=person.birth_day
        )
        
        display_text: str = DateFormatter.format_display(
            date=date_parts,
            month_style=self.DATE_MONTH_STYLE,
            separator=self.DATE_SEPARATOR
        )
        
        sort_value: int = self._calculate_date_sort_value(
            person.birth_year,
            person.birth_month,
            person.birth_day
        )
        
        item: QTableWidgetItem = QTableWidgetItem(display_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setData(Qt.ItemDataRole.UserRole, sort_value)
        
        self.table.setItem(row, self.COLUMN_BIRTH_DATE, item)
    
    def _set_death_date_cell(self, row: int, person: Person) -> None:
        """Set the death date cell for a person."""
        if person.death_year is None:
            item: QTableWidgetItem = QTableWidgetItem(self.EMPTY_DATE_DISPLAY)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, self.COLUMN_DEATH_DATE, item)
            return
        
        date_parts: DateParts = DateParts(
            year=person.death_year,
            month=person.death_month,
            day=person.death_day
        )
        
        display_text: str = DateFormatter.format_display(
            date=date_parts,
            month_style=self.DATE_MONTH_STYLE,
            separator=self.DATE_SEPARATOR
        )
        
        sort_value: int = self._calculate_date_sort_value(
            person.death_year,
            person.death_month,
            person.death_day
        )
        
        item: QTableWidgetItem = QTableWidgetItem(display_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setData(Qt.ItemDataRole.UserRole, sort_value)
        
        self.table.setItem(row, self.COLUMN_DEATH_DATE, item)
    
    def _calculate_date_sort_value(
        self,
        year: int,
        month: int | None,
        day: int | None
    ) -> int:
        """Calculate numeric sort value for date (YYYYMMDD format)."""
        year_part: int = year * 10000
        month_part: int = (month or self.SORT_VALUE_UNKNOWN_MONTH) * 100
        day_part: int = day or self.SORT_VALUE_UNKNOWN_DAY
        
        return year_part + month_part + day_part
    
    # ------------------------------------------------------------------
    # Search & Filtering
    # ------------------------------------------------------------------
    
    def _filter_table(self) -> None:
        """Filter table based on search text (accent-insensitive)."""
        search_text: str = self.search_input.text().lower()
        
        if not search_text:
            self._populate_table(self.people)
            return
        
        normalized_search: str = TextNormalizer.normalize_for_search(search_text)
        
        filtered: list[Person] = [
            person for person in self.people
            if normalized_search in TextNormalizer.normalize_for_search(person.display_name)
        ]
        
        self._populate_table(filtered)
    
    # ------------------------------------------------------------------
    # Selection & Context Menu
    # ------------------------------------------------------------------
    
    def _get_selected_person(self) -> Person | None:
        """Get the person from the selected row."""
        selected_rows: list = self.table.selectedIndexes()
        if not selected_rows:
            return None
        
        row: int = selected_rows[0].row()
        display_num_item: QTableWidgetItem | None = self.table.item(row, self.COLUMN_NUMBER)
        if not display_num_item:
            return None
        
        person_id: int = display_num_item.data(Qt.ItemDataRole.UserRole)
        return self.person_repo.get_by_id(person_id)
    
    def _on_row_double_clicked(self) -> None:
        """Handle double-click on a row."""
        self._edit_selected_person()
    
    def _show_context_menu(self, position) -> None:
        """Show right-click context menu."""
        if not self._get_selected_person():
            return
        
        menu: QMenu = QMenu(self)
        
        edit_action: QAction = QAction(self.ACTION_TEXT_EDIT, self)
        edit_action.triggered.connect(self._edit_selected_person)
        menu.addAction(edit_action)
        
        menu.addSeparator()
        
        delete_action: QAction = QAction(self.ACTION_TEXT_DELETE, self)
        delete_action.triggered.connect(self._delete_selected_person)
        menu.addAction(delete_action)
        
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    # ------------------------------------------------------------------
    # Person Actions
    # ------------------------------------------------------------------
    
    def _add_person(self) -> None:
        """Open Add Person dialog."""
        from dialogs.add_person_dialog import AddPersonDialog
        
        dialog: AddPersonDialog = AddPersonDialog(self.db_manager)
        if dialog.exec():
            self.refresh_data()
            self.person_edited.emit()
    
    def _edit_selected_person(self) -> None:
        """Open Edit Person dialog for selected row."""
        person: Person | None = self._get_selected_person()
        if not person:
            QMessageBox.warning(self, self.MSG_NO_SELECTION_TITLE, self.MSG_NO_SELECTION_EDIT)
            return
        
        from dialogs.edit_person_dialog import EditPersonDialog
        
        dialog: EditPersonDialog = EditPersonDialog(self.db_manager, person)
        if dialog.exec():
            self.refresh_data()
            self.person_edited.emit()
    
    def _delete_selected_person(self) -> None:
        """Delete the selected person after confirmation."""
        person: Person | None = self._get_selected_person()
        if not person:
            QMessageBox.warning(self, self.MSG_NO_SELECTION_TITLE, self.MSG_NO_SELECTION_DELETE)
            return
        
        if self._confirm_delete(person):
            self._execute_delete(person)
    
    def _confirm_delete(self, person: Person) -> bool:
        """Show confirmation dialog for person deletion."""
        msg: QMessageBox = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.MSG_DELETE_TITLE)
        msg.setText(self.MSG_DELETE_TEXT.format(name=person.display_name))
        msg.setInformativeText(self.MSG_DELETE_INFO)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        return msg.exec() == QMessageBox.StandardButton.Yes
    
    def _execute_delete(self, person: Person) -> None:
        """Execute the deletion of a person."""
        if person.id:
            self.person_repo.delete(person.id)
            self.refresh_data()
            self.person_edited.emit()