"""Widget for selecting a person from the database with autocomplete."""

import unicodedata
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QCompleter
from PySide6.QtCore import Signal, Qt, QStringListModel

from database.db_manager import DatabaseManager
from database.person_repository import PersonRepository


class PersonSelector(QWidget):
    """Autocomplete text field for selecting a person from the database."""
    
    # Signal emitted when a person is selected (emits person_id)
    personSelected = Signal(int)
    # Signal emitted when selection is cleared
    selectionCleared = Signal()
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        """Initialize the person selector widget."""
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.person_repo = PersonRepository(db_manager)

        self.gender_filter: str | None = None

        self._name_to_id: dict[str, int] = {}

        self._selected_person_id: int | None = None
        
        self._setup_ui()
        self._load_people()
    
    def _setup_ui(self) -> None:
        """Create the autocomplete text field."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create text field
        self.text_field = QLineEdit(self)
        self.text_field.setPlaceholderText("Type to search for a person...")
        self.text_field.setClearButtonEnabled(True)
        
        # Create completer
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setMaxVisibleItems(10)
        
        # Attach completer to text field
        self.text_field.setCompleter(self.completer)
        
        # Connect signals
        self.completer.activated.connect(self._on_person_selected)
        self.text_field.textChanged.connect(self._on_text_changed)
        
        layout.addWidget(self.text_field)
    
    def _load_people(self) -> None:
        """Load all people from database and populate completer."""
        if not self.db_manager.is_open:
            return

        all_people = self.person_repo.get_all()

        if hasattr(self, 'gender_filter') and self.gender_filter:
            all_people = [p for p in all_people if p.gender in (self.gender_filter, "Unknown")]

        self._name_to_id.clear()

        display_names = []
        
        for person in all_people:
            if person.id is None:
                continue
            
            display_name = self._format_person_display(person)
            display_names.append(display_name)
            self._name_to_id[display_name] = person.id

        display_names.sort()

        from PySide6.QtCore import QStringListModel
        model = QStringListModel(display_names)
        self.completer.setModel(model)
    
    def _format_person_display(self, person) -> str:
        """Format a person's info for display in the dropdown."""
        name = person.display_name

        if person.death_year:
            date_str = f"{person.birth_year or '?'}-{person.death_year}"
        elif person.birth_year:
            date_str = f"b. {person.birth_year}"
        else:
            date_str = "dates unknown"
        
        return f"{name} ({date_str})"
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for searching (handle special characters)."""
        text = text.lower()
        
        # Unicode normalization: á → a, ý → y, etc.
        normalized = unicodedata.normalize('NFD', text)
        ascii_text = ''.join(
            char for char in normalized 
            if unicodedata.category(char) != 'Mn'
        )
        
        return ascii_text
    
    def _on_person_selected(self, display_name: str) -> None:
        """Handle person selection from dropdown."""
        person_id = self._name_to_id.get(display_name)
        
        if person_id is not None:
            self._selected_person_id = person_id
            self.personSelected.emit(person_id)
    
    def _on_text_changed(self, text: str) -> None:
        """Handle text field changes."""
        if not text.strip():
            self._selected_person_id = None
            self.selectionCleared.emit()
    
    def get_person_id(self) -> int | None:
        """Get the currently selected person's ID."""
        return self._selected_person_id
    
    def set_person(self, person_id: int | None) -> None:
        """Set the selected person by ID."""
        if person_id is None:
            self.clear()
            return

        for display_name, pid in self._name_to_id.items():
            if pid == person_id:
                self.text_field.setText(display_name)
                self._selected_person_id = person_id
                return

        self.clear()
    
    def clear(self) -> None:
        """Clear the selection."""
        self.text_field.clear()
        self._selected_person_id = None
        self.selectionCleared.emit()
    
    def refresh(self) -> None:
        """Reload people from database (call after adding/editing people)."""
        current_id = self._selected_person_id
        self._load_people()

        if current_id is not None:
            self.set_person(current_id)
    
    def set_filter(self, gender: str | None = None) -> None:
        """Filter the displayed people by gender."""
        self.gender_filter = gender
        self._load_people()