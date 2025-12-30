# DynastyVizualizer - Codebase Reference

**Quick Reference**: Family tree/genealogy app for gaming. PySide6 + SQLite. MVC + Command pattern.

**Status**: Phase 1 ✅ Complete, Phase 2 ✅ ~90% Complete (Nearly all CRUD operations complete)

---

## Architecture

**Pattern**: MVC + Command for undo/redo

```
User Action → Dialog → Command → Repository → Database
                ↓
         UndoManager (stores command)
                ↓
         Views update via signals
```

---

## Completed Features

### Phase 1: Foundation ✅
- Database: SQLite `.dyn` files, 8 tables, flexible dates (year/month/day)
- File ops: New, Open, Save, Save As with unsaved changes tracking
- Undo/redo: Command pattern infrastructure
- Settings: QSettings persistence, keyboard shortcuts
- Migration: Automatic schema upgrades

### Phase 2: Data Management ✅ ~90%

**Person Management:**
- **Person Model** (25 fields with computed properties)
- **PersonRepository** (272 lines) - Full CRUD + search
- **AddPersonDialog** (252 lines) - Special characters, validation
- **EditPersonDialog** (166 lines + 3 panels):
  - General Panel (310 lines): Names, dates, gender, education
  - Relationships Panel (777 lines): Parents, marriages, children
  - Events Panel (252 lines): Personal event timeline
- **DeletePersonCommand** - With confirmation dialog

**Marriage Management:**
- **Marriage Model** - Full lifecycle (dates, types, dissolution)
- **MarriageRepository** (207 lines) - CRUD + get_by_spouse
- **CreateMarriageDialog** - Marry two people with validation
- **EndMarriageDialog** - Divorce/dissolution with reasons
- **EditMarriageCommand** - Modify existing marriages

**Event System:**
- **Event Model** - Flexible date ranges
- **EventRepository** - Full CRUD operations
- **CreateEventDialog** / **EditEventDialog** (183/219 lines)
- **Event Types**: Birth, Marriage, Death, Job, Move, Illness, etc.
- Timeline display in Edit Person dialog

**Child Creation:**
- **CreateChildDialog** (250 lines) - Automatic parent assignment
- **AssignParentCommand** / **UnassignParentCommand**
- Parent validation

**Reusable Widgets:**
- **DatePicker** (183 lines) - Flexible year/month/day
- **PersonSelector** (162 lines) - Searchable dropdown
- **Search Bar** - Real-time filtering

**Data Views:**
- **Data Table View** (237 lines) - Sortable, filterable, searchable
- Double-click to edit, right-click context menus

**Commands:**
- 14 Genealogy Commands (all ✅)
- 8 GUI Commands (all ✅)

---

## Database Schema (Essential)

**Person Table** (25 fields):
```sql
CREATE TABLE Person (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    maiden_name TEXT,
    nickname TEXT,
    gender TEXT,
    birth_year INTEGER, birth_month INTEGER, birth_day INTEGER,
    death_year INTEGER, death_month INTEGER, death_day INTEGER,
    arrival_year INTEGER, arrival_month INTEGER, arrival_day INTEGER,
    moved_out_year INTEGER, moved_out_month INTEGER, moved_out_day INTEGER,
    father_id INTEGER, mother_id INTEGER, family_id INTEGER,
    dynasty_id INTEGER DEFAULT 1,
    is_founder INTEGER DEFAULT 0,
    education INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY(father_id) REFERENCES Person(id) ON DELETE SET NULL,
    FOREIGN KEY(mother_id) REFERENCES Person(id) ON DELETE SET NULL,
    FOREIGN KEY(family_id) REFERENCES Family(id) ON DELETE SET NULL
);
```

**Other Tables**: Marriage, Event, Portrait, Family, MajorEvent, PersonPosition, Settings

**Flexible Dates**: All dates support year-only, year/month, or full year/month/day precision

---

## File Structure (Implemented Only)

```
DynastyVizualizer/
├── main.py                              # Entry point, menus, shortcuts
├── database/
│   ├── db_manager.py                   # SQLite connection, schema, migration
│   └── person_repository.py            # Person CRUD operations
├── models/
│   └── person.py                       # Person dataclass (25 fields)
├── actions/                             # Menu handlers (all 6 files)
│   ├── file_actions.py                 # New/Open/Save/Exit
│   ├── edit_actions.py                 # Undo/Redo/Add Person
│   ├── view_actions.py, tools_actions.py, settings_actions.py, help_actions.py
├── commands/
│   ├── undo_redo_manager.py            # Command pattern manager
│   └── genealogy_commands/
│       └── add_person.py               # AddPersonCommand (undo/redo)
├── dialogs/
│   └── add_person_dialog.py            # Add person UI (special chars)
├── utils/
│   └── settings_manager.py             # QSettings, keyboard shortcuts
└── scripts/
    ├── migrate_database.py             # Schema migration tool
    └── create_codebase_summary.py      # Doc generator
```

**Scaffolded** (88 files): Other models, commands, views, widgets, dialogs

---

## Code Patterns

### Command Pattern Example
```python
class AddPersonCommand:
    def __init__(self, db_manager: DatabaseManager, person: Person):
        self.person = person
        self.person_id: int | None = None
        self.repo = PersonRepository(db_manager)

    def run(self) -> None:
        if self.person_id is None:
            self.person_id = self.repo.insert(self.person)
        else:
            self.person.id = self.person_id
            self.repo.insert_with_id(self.person)  # Redo with same ID

    def undo(self) -> None:
        if self.person_id is not None:
            self.repo.delete(self.person_id)
```

### Repository Pattern Example
```python
class PersonRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def insert(self, person: Person) -> int:
        # Returns new person_id

    def insert_with_id(self, person: Person) -> None:
        # For redo: uses person.id explicitly

    def get_by_id(self, person_id: int) -> Person | None:
        # Fetch by ID

    def get_children(self, parent_id: int) -> list[Person]:
        # Search by father_id or mother_id
```

### Dialog Pattern Example
```python
class AddPersonDialog(QDialog):
    def _create_special_char_toolbar(self) -> QHBoxLayout:
        # Buttons for á, ý, ó, é, í

    def _validate_inputs(self) -> bool:
        # Check required fields

    def get_person(self) -> Person | None:
        # Returns created Person or None
```

---

## Coding Standards

**Type Hints** (Python 3.10+):
```python
def save_database(self, path: str | None = None) -> bool:
    """Save database."""

self.conn: sqlite3.Connection | None = None
self.undo_stack: list[Command] = []
```

**Docstrings** (concise, imperative):
```python
def new_database(self, file_path: str) -> None:
    """Create a brand-new .dyn file with the dynasty schema."""
```

**Rules**:
- Use `X | None` not `Optional[X]`
- Use `list[T]`, `dict[K,V]` (lowercase)
- Single-line docstrings (5-15 words)
- Forward refs with quotes: `'MainWindow'`

---

## Migration System

**Usage**:
```bash
python scripts/migrate_database.py "MyDynasty.dyn"
```

**Features**:
- Adds new columns (middle_name, nickname, dynasty_id, etc.)
- Creates new tables (Portrait, Family, MajorEvent, etc.)
- Backup before migration
- Preserves all existing data
- Safe, idempotent (can run multiple times)

---

## Next Steps (Phase 2 → Phase 3)

- [ ] Settings dialog completion (all tabs)
- [ ] About dialog (Help menu)
- [ ] Portrait gallery UI (model exists)
- [ ] Family Tree visualization (Phase 3)
- [ ] Timeline view integration (Phase 5)

---

## Quick Stats

- **Files**: 95+ files implemented
- **Lines**: ~7,700 / ~15,000-20,000 estimated
- **Phase 1**: ✅ 100% complete
- **Phase 2**: ✅ ~90% complete
- **Overall Progress**: ~25-30%
- **Updated**: 2025-12-30

---

## Key Achievements

✅ Complete database foundation with migration
✅ Full undo/redo infrastructure (22 commands)
✅ Keyboard shortcuts system
✅ **Complete Person Management** (Add, Edit with 3 panels, Delete)
✅ **Complete Marriage Management** (Create, Edit, End)
✅ **Complete Event System** (Create, Edit, Delete, Timeline display)
✅ **Child Creation** with automatic parent assignment
✅ **Data Table View** with sorting, filtering, search
✅ **Recent Files** management
✅ DatePicker and PersonSelector reusable widgets
✅ ID preservation across undo/redo
✅ Professional validation and error handling

**Why It Works**:
- Command pattern = everything undoable
- Repository pattern = clean data access
- Qt signals = views auto-sync
- Flexible dates = supports games + real genealogy
