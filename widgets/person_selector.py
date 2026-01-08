"""Widget for selecting a person from the database with autocomplete."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QCompleter
from PySide6.QtCore import Signal, Qt, QStringListModel, QSortFilterProxyModel, QModelIndex, QPersistentModelIndex

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from database.person_repository import PersonRepository
from utils.text_normalizer import TextNormalizer


class AccentInsensitiveProxyModel(QSortFilterProxyModel):
    """Proxy model that performs accent-insensitive filtering."""
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the proxy model."""
        super().__init__(parent)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex | QPersistentModelIndex) -> bool:
        """Check if row matches filter using accent-insensitive comparison."""
        source_model = self.sourceModel()
        if not source_model:
            return False
        
        index: QModelIndex = source_model.index(source_row, 0, source_parent)
        data: str = source_model.data(index, Qt.ItemDataRole.DisplayRole)
        
        if not data:
            return False
        
        filter_text: str = self.filterRegularExpression().pattern()
        if not filter_text:
            return True
        
        normalized_data: str = TextNormalizer.normalize_for_search(data)
        normalized_filter: str = TextNormalizer.normalize_for_search(filter_text)
        
        return normalized_filter in normalized_data


class PersonSelector(QWidget):
    """Autocomplete text field for selecting a person from the database."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # UI Text
    PLACEHOLDER_TEXT: str = "Type to search for a person..."
    
    # Date Display Formats
    DATE_FORMAT_LIFESPAN: str = "{birth}-{death}"
    DATE_FORMAT_BIRTH_ONLY: str = "b. {year}"
    DATE_FORMAT_UNKNOWN: str = "dates unknown"
    DATE_PLACEHOLDER_UNKNOWN: str = "?"
    
    # Person Display Format
    PERSON_DISPLAY_FORMAT: str = "{name} ({dates})"
    
    # Gender Filter Values
    GENDER_UNKNOWN: str = "Unknown"
    
    # Completer Settings
    COMPLETER_MAX_VISIBLE: int = 10
    
    # Layout
    LAYOUT_MARGIN: int = 0
    
    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------
    
    personSelected: Signal = Signal(int)
    selectionCleared: Signal = Signal()
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget | None = None) -> None:
        """Initialize the person selector widget."""
        super().__init__(parent)
        
        self.db_manager: DatabaseManager = db_manager
        self.person_repo: PersonRepository = PersonRepository(db_manager)
        
        self.gender_filter: str | None = None
        self._name_to_id: dict[str, int] = {}
        self._selected_person_id: int | None = None
        
        self._setup_ui()
        self._load_people()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create the autocomplete text field."""
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(
            self.LAYOUT_MARGIN,
            self.LAYOUT_MARGIN,
            self.LAYOUT_MARGIN,
            self.LAYOUT_MARGIN
        )
        
        self.text_field: QLineEdit = self._create_text_field()
        self.completer: QCompleter = self._create_completer()
        
        self.text_field.setCompleter(self.completer)
        
        self._connect_signals()
        
        layout.addWidget(self.text_field)
    
    def _create_text_field(self) -> QLineEdit:
        """Create the text input field."""
        text_field: QLineEdit = QLineEdit(self)
        text_field.setPlaceholderText(self.PLACEHOLDER_TEXT)
        text_field.setClearButtonEnabled(True)
        return text_field
    
    def _create_completer(self) -> QCompleter:
        """Create the autocomplete completer with accent-insensitive filtering."""
        completer: QCompleter = QCompleter(self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setMaxVisibleItems(self.COMPLETER_MAX_VISIBLE)
        
        self.proxy_model: AccentInsensitiveProxyModel = AccentInsensitiveProxyModel(self)
        completer.setModel(self.proxy_model)
        
        return completer
    
    def _connect_signals(self) -> None:
        """Connect widget signals to handlers."""
        self.completer.activated.connect(self._on_person_selected)
        self.text_field.textChanged.connect(self._on_text_changed)
    
    # ------------------------------------------------------------------
    # Data Loading
    # ------------------------------------------------------------------
    
    def _load_people(self) -> None:
        """Load all people from database and populate completer."""
        if not self.db_manager.is_open:
            return
        
        all_people: list[Person] = self.person_repo.get_all()
        filtered_people: list[Person] = self._apply_gender_filter(all_people)
        
        self._name_to_id.clear()
        display_names: list[str] = self._build_display_names(filtered_people)
        display_names.sort()
        
        self._update_completer_model(display_names)
    
    def _apply_gender_filter(self, people: list[Person]) -> list[Person]:
        """Filter people by gender if filter is set."""
        if not self.gender_filter:
            return people
        
        return [
            p for p in people
            if p.gender in (self.gender_filter, self.GENDER_UNKNOWN)
        ]
    
    def _build_display_names(self, people: list[Person]) -> list[str]:
        """Build list of display names for people."""
        display_names: list[str] = []
        
        for person in people:
            if person.id is None:
                continue
            
            display_name: str = self._format_person_display(person)
            display_names.append(display_name)
            self._name_to_id[display_name] = person.id
        
        return display_names
    
    def _update_completer_model(self, display_names: list[str]) -> None:
        """Update the completer's data model with proxy for accent-insensitive search."""
        source_model: QStringListModel = QStringListModel(display_names)
        self.proxy_model.setSourceModel(source_model)
    
    # ------------------------------------------------------------------
    # Display Formatting
    # ------------------------------------------------------------------
    
    def _format_person_display(self, person: Person) -> str:
        """Format a person's info for display in the dropdown."""
        name: str = person.display_name
        date_str: str = self._format_date_info(person)
        
        return self.PERSON_DISPLAY_FORMAT.format(name=name, dates=date_str)
    
    def _format_date_info(self, person: Person) -> str:
        """Format date information for person display."""
        if person.death_year:
            return self._format_lifespan(person)
        
        if person.birth_year:
            return self.DATE_FORMAT_BIRTH_ONLY.format(year=person.birth_year)
        
        return self.DATE_FORMAT_UNKNOWN
    
    def _format_lifespan(self, person: Person) -> str:
        """Format lifespan string for deceased person."""
        birth: str = str(person.birth_year) if person.birth_year else self.DATE_PLACEHOLDER_UNKNOWN
        death: str = str(person.death_year)
        
        return self.DATE_FORMAT_LIFESPAN.format(birth=birth, death=death)
    
    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------
    
    def _on_person_selected(self, display_name: str) -> None:
        """Handle person selection from dropdown."""
        person_id: int | None = self._name_to_id.get(display_name)
        
        if person_id is None:
            return
        
        self._selected_person_id = person_id
        self.personSelected.emit(person_id)
    
    def _on_text_changed(self, text: str) -> None:
        """Handle text field changes."""
        if not text.strip():
            self._clear_selection()
    
    def _clear_selection(self) -> None:
        """Clear the current selection."""
        self._selected_person_id = None
        self.selectionCleared.emit()
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_person_id(self) -> int | None:
        """Get the currently selected person's ID."""
        return self._selected_person_id
    
    def set_person(self, person_id: int | None) -> None:
        """Set the selected person by ID."""
        if person_id is None:
            self.clear()
            return
        
        display_name: str | None = self._find_display_name_for_id(person_id)
        
        if display_name:
            self.text_field.setText(display_name)
            self._selected_person_id = person_id
        else:
            self.clear()
    
    def _find_display_name_for_id(self, person_id: int) -> str | None:
        """Find display name for a given person ID."""
        for display_name, pid in self._name_to_id.items():
            if pid == person_id:
                return display_name
        return None
    
    def clear(self) -> None:
        """Clear the selection."""
        self.text_field.clear()
        self._selected_person_id = None
        self.selectionCleared.emit()
    
    def refresh(self) -> None:
        """Reload people from database (call after adding/editing people)."""
        current_id: int | None = self._selected_person_id
        self._load_people()
        
        if current_id is not None:
            self.set_person(current_id)
    
    def set_filter(self, gender: str | None = None) -> None:
        """Filter the displayed people by gender."""
        self.gender_filter = gender
        self._load_people()