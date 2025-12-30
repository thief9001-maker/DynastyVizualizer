"""Data table view for displaying all people."""

import unicodedata

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QMenu, QMessageBox, QLineEdit, QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from database.db_manager import DatabaseManager
from database.person_repository import PersonRepository
from models.person import Person


class DataTableView(QWidget):
    """Widget displaying all people in a sortable, filterable table."""
    
    person_edited = Signal()
    
    def __init__(self, db_manager: DatabaseManager, parent=None) -> None:
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person_repo = PersonRepository(db_manager)
        self.people: list[Person] = []
        self.person_display_numbers: dict[int, int] = {}  # Maps person.id -> display number
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Create the table and controls."""
        layout = QVBoxLayout(self)
        
        toolbar = QHBoxLayout()
        
        toolbar.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter by name...")
        self.search_input.textChanged.connect(self._filter_table)
        self.search_input.setMaximumWidth(300)
        toolbar.addWidget(self.search_input)
        
        toolbar.addStretch()
        
        add_btn = QPushButton("+ Add Person")
        add_btn.clicked.connect(self._add_person)
        toolbar.addWidget(add_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_data)
        toolbar.addWidget(refresh_btn)
        
        layout.addLayout(toolbar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "#", "Name", "Gender", "Birth Year", "Death Year"
        ])
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.table.doubleClicked.connect(self._on_row_double_clicked)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        
        layout.addWidget(self.table)
    
    def refresh_data(self) -> None:
        """Load all people from database and assign persistent display numbers."""
        self.people = self.person_repo.get_all()
        
        # Sort by ID for consistent numbering
        self.people.sort(key=lambda p: p.id or 0)
        
        # Assign persistent display numbers
        self.person_display_numbers.clear()
        for index, person in enumerate(self.people, start=1):
            if person.id:
                self.person_display_numbers[person.id] = index
        
        self._populate_table(self.people)
    
    def _populate_table(self, people: list[Person]) -> None:
        """Fill table with person data."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        for person in people:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Display number (persistent, doesn't change with sorting)
            display_num = self.person_display_numbers.get(person.id or 0, 0)
            display_num_item = QTableWidgetItem(f"{display_num:06d}")
            display_num_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            display_num_item.setData(Qt.ItemDataRole.UserRole, person.id)
            # Store as integer for proper sorting
            display_num_item.setData(Qt.ItemDataRole.UserRole + 1, display_num)
            self.table.setItem(row, 0, display_num_item)
            
            # Name
            name_item = QTableWidgetItem(person.display_name)
            self.table.setItem(row, 1, name_item)
            
            # Gender
            gender_item = QTableWidgetItem(person.gender or "Unknown")
            gender_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, gender_item)
            
            # Birth Year
            birth_item = QTableWidgetItem(str(person.birth_year) if person.birth_year else "")
            birth_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, birth_item)
            
            # Death Year
            death_item = QTableWidgetItem(str(person.death_year) if person.death_year else "")
            death_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, death_item)
        
        self.table.setSortingEnabled(True)
    
    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize Unicode text for accent-insensitive comparison."""
        return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    
    def _filter_table(self) -> None:
        """Filter table based on search text (accent-insensitive)."""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self._populate_table(self.people)
            return
        
        # Normalize search text for comparison
        normalized_search = self._normalize_text(search_text)
        
        filtered = [
            p for p in self.people 
            if normalized_search in self._normalize_text(p.display_name.lower())
        ]
        self._populate_table(filtered)
    
    def _get_selected_person(self) -> Person | None:
        """Get the person from the selected row."""
        selected_rows = self.table.selectedIndexes()
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        display_num_item = self.table.item(row, 0)
        if not display_num_item:
            return None
        
        person_id = display_num_item.data(Qt.ItemDataRole.UserRole)
        return self.person_repo.get_by_id(person_id)
    
    def _on_row_double_clicked(self) -> None:
        """Handle double-click on a row."""
        self._edit_selected_person()
    
    def _show_context_menu(self, position) -> None:
        """Show right-click context menu."""
        if not self._get_selected_person():
            return
        
        menu = QMenu(self)
        
        edit_action = QAction("Edit Person", self)
        edit_action.triggered.connect(self._edit_selected_person)
        menu.addAction(edit_action)
        
        menu.addSeparator()
        
        delete_action = QAction("Delete Person", self)
        delete_action.triggered.connect(self._delete_selected_person)
        menu.addAction(delete_action)
        
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    def _add_person(self) -> None:
        """Open Add Person dialog."""
        from dialogs.add_person_dialog import AddPersonDialog
        
        dialog = AddPersonDialog(self.db_manager)
        if dialog.exec():
            self.refresh_data()
            self.person_edited.emit()
    
    def _edit_selected_person(self) -> None:
        """Open Edit Person dialog for selected row."""
        person = self._get_selected_person()
        if not person:
            QMessageBox.warning(self, "No Selection", "Please select a person to edit.")
            return
        
        from dialogs.edit_person_dialog import EditPersonDialog
        
        dialog = EditPersonDialog(self.db_manager, person)
        if dialog.exec():
            self.refresh_data()
            self.person_edited.emit()
    
    def _delete_selected_person(self) -> None:
        """Delete the selected person after confirmation."""
        person = self._get_selected_person()
        if not person:
            QMessageBox.warning(self, "No Selection", "Please select a person to delete.")
            return
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Delete Person")
        msg.setText(f"Delete {person.display_name}?")
        msg.setInformativeText("This will also delete all their marriages, events, and relationships.")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            if person.id:
                self.person_repo.delete(person.id)
                self.refresh_data()  # This reassigns numbers 1,2,3... to remaining people
                self.person_edited.emit()