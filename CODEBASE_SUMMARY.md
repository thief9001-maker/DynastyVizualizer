# DynastyVizualizer Codebase Summary

## Project Overview

**DynastyVizualizer** is a family tree visualization GUI application designed for the game [Ostriv](https://store.steampowered.com/app/773790/Ostriv/). It provides tools to create, manage, and visualize multi-generational family dynasties with support for marriages, events, and genealogical relationships.

### Technology Stack
- **GUI Framework**: PySide6 (Qt for Python)
- **Database**: SQLite with custom `.dyn` file format
- **Language**: Python 3.10+
- **Patterns**: MVC architecture with Command pattern for undo/redo

---

## Codebase Statistics

- **Total Python Files**: 37 (9 implemented, 28 scaffolded)
- **Lines of Code**: ~532 (excluding comments and blank lines)
- **Total Lines**: 718 (including docstrings and comments)
- **Implementation Status**: ~15% complete (core infrastructure done)

---

## Coding Standards & Conventions

### Type Hints
We use modern Python 3.10+ type hint syntax throughout the codebase:

```python
# Union types with pipe operator (not Optional[...])
def save_database(self, path: str | None = None) -> bool:
    """Save the database, optionally to a new path."""

# Instance variables with type annotations
self.conn: sqlite3.Connection | None = None
self.file_path: str | None = None

# Modern collection types (lowercase, not typing.List/Dict)
self.undo_stack: list[Command] = []
self.data: dict[str, int] = {}

# Forward references for circular imports
def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
```

**Rules**:
- ✅ Always specify return types (`-> Type`)
- ✅ Use `X | None` instead of `Optional[X]` or `Union[X, None]`
- ✅ Use lowercase `list[T]`, `dict[K, V]` (PEP 585 style)
- ✅ Use forward references with quotes for circular imports
- ✅ Add `# type: ignore` when necessary for Qt compatibility

### Docstrings
We maintain concise, single-line docstrings for clarity and consistency:

```python
def new_database(self, file_path: str) -> None:
    """Create a brand-new .dyn file with the dynasty schema."""

class DatabaseManager:
    """Manages SQLite-based .dyn dynasty database files."""
```

**Rules**:
- ✅ Single-line triple quotes for most methods/classes
- ✅ Imperative/action verbs ("Create...", "Check...", "Initialize...")
- ✅ Keep to 5-15 words typically
- ✅ No parameter documentation or return value docs
- ✅ Only use multi-line when genuinely needed for context
- ❌ Avoid complex/advanced docstring formats (Google, NumPy, Sphinx style)

### Code Style
- **Formatting**: PEP 8 compliant
- **Section markers**: Use `# -----` comment blocks to organize code sections
- **Naming**: Descriptive names, `snake_case` for functions/variables
- **Properties**: Use `@property` decorators for encapsulation
- **Error handling**: Specific exception types, informative error messages

---

## Architecture

### Design Pattern: MVC + Command

```
┌─────────────────────────────────────────────────┐
│         MainWindow (main.py)                    │
│         - Qt GUI setup                          │
│         - Menu bar management                   │
│         - Coordinate actions and database       │
└────────────┬────────────────────────────────────┘
             │
        ┌────┴─────────────────────┐
        │                          │
   ┌────▼──────┐          ┌───────▼────────┐
   │  Actions  │          │   Database     │
   │  Handler  │          │   Manager      │
   │           │          │                │
   │  • File   │          │  SQLite .dyn   │
   │  • Edit   │◄─────────┤  • Person      │
   │  • View   │ interact │  • Marriage    │
   │  • Tools  │          │  • Event       │
   │  • Help   │          │                │
   └─────┬─────┘          └────────────────┘
         │
         │ execute()
         ▼
   ┌────────────────┐
   │  UndoRedo      │
   │  Manager       │
   │                │
   │  Command       │
   │  Pattern       │
   └────────────────┘
```

### Directory Structure

```
DynastyVizualizer/
├── main.py                          # Application entry point (222 lines)
├── database/
│   ├── __init__.py
│   └── db_manager.py               # SQLite CRUD operations (193 lines)
├── actions/                         # Menu action handlers (222 lines total)
│   ├── __init__.py                 # Exports all action classes (6 lines)
│   ├── file_actions.py             # New/Open/Save/Exit (159 lines)
│   ├── edit_actions.py             # Undo/Redo operations (29 lines)
│   ├── view_actions.py             # View switching (22 lines)
│   ├── tools_actions.py            # Validation tools (22 lines)
│   └── help_actions.py             # About dialog (10 lines)
├── commands/
│   ├── undo_redo_manager.py        # Command pattern manager (55 lines)
│   ├── base_command.py             # Base command class [SCAFFOLDED]
│   ├── genealogy commands/         # Person/marriage/event commands [SCAFFOLDED]
│   │   ├── add_person.py
│   │   ├── edit_person.py
│   │   ├── remove_person.py
│   │   ├── add_marriage.py
│   │   ├── end_marraige.py
│   │   ├── add_event.py
│   │   ├── modify_event.py
│   │   ├── remove_event.py
│   │   ├── assign_parent.py
│   │   └── unassign_parent.py
│   └── GUI commands/               # View/scene commands [SCAFFOLDED]
│       ├── move_node.py
│       ├── rebuild_scene.py
│       ├── recompute_generation.py
│       ├── preference_changes.py
│       └── timeline_scroll.py
├── models/                          # Data models [SCAFFOLDED]
│   ├── person.py
│   ├── marriage.py
│   └── event.py
├── views/                           # Visualization widgets [SCAFFOLDED]
│   ├── dynasty_view.py
│   ├── timeline_view.py
│   └── data_table.py
├── widgets/                         # Custom widgets [SCAFFOLDED]
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## Implemented Components

### 1. Main Window (`main.py`)
**Status**: ✅ Complete
**Lines**: 222

**Responsibilities**:
- Initialize PySide6 QMainWindow
- Create menu bar (File, Edit, View, Tools, Help)
- Manage database and undo/redo managers
- Connect menu actions to handlers
- Update UI state based on database/undo stack status

**Key Methods**:
- `_create_menus()` - Builds all menu structures
- `_connect_actions()` - Links menu items to action handlers
- `_update_menu_states()` - Enable/disable menus based on app state
- `refresh_ui()` - Public method to refresh title and menu states

### 2. Database Manager (`database/db_manager.py`)
**Status**: ✅ Complete
**Lines**: 193

**Responsibilities**:
- Manage SQLite connections to `.dyn` files
- Create new databases with schema initialization
- Open existing dynasty files
- Save/commit changes to disk
- Track dirty state (unsaved changes)

**Key Methods**:
- `new_database(file_path)` - Create fresh `.dyn` file
- `open_database(file_path)` - Open existing file
- `save_database(path=None)` - Save or "Save As"
- `mark_dirty()` / `mark_clean()` - Track unsaved changes

**Properties**:
- `is_open` - Check if database is loaded
- `is_dirty` - Check if there are unsaved changes
- `database_name` - Get filename without path
- `database_directory` - Get directory path

**Schema** (see `_initialize_schema()` at line 138):
- **Person** table: Names, dates (birth/death/arrival), parent references
- **Marriage** table: Spouse references, dates, dissolution info
- **Event** table: Person events with types, dates, notes

### 3. File Actions (`actions/file_actions.py`)
**Status**: ✅ Complete
**Lines**: 159

**Responsibilities**:
- Handle File menu operations
- Show file dialogs (open/save)
- Error handling for file operations
- Prompt for unsaved changes on exit

**Key Methods**:
- `new_dynasty()` - Create new dynasty file
- `open_dynasty()` - Open existing file
- `save()` - Save current database
- `save_as()` - Save to new path
- `exit_app()` - Close application with unsaved check

### 4. Edit Actions (`actions/edit_actions.py`)
**Status**: ⚠️ Partially Complete
**Lines**: 29

**Implemented**:
- `undo()` - Undo last action
- `redo()` - Redo last undone action

**Scaffolded**:
- `add_person()` - TODO: Implement with dialog
- `remove_person()` - TODO: Implement with confirmation
- `add_new_family()` - TODO: Implement family creation

### 5. View Actions (`actions/view_actions.py`)
**Status**: 📝 Scaffolded
**Lines**: 22

All methods are placeholders awaiting view implementation:
- `family_trees()` - Switch to family trees view
- `timeline()` - Switch to timeline view
- `dynasty()` - Switch to dynasty overview
- `data_table()` - Switch to data table view

### 6. Tools Actions (`actions/tools_actions.py`)
**Status**: 📝 Scaffolded
**Lines**: 22

Utility operations for data validation:
- `rebuild_scene()` - Rebuild visualization from scratch
- `recompute_generations()` - Recalculate generation levels
- `validate_marriages()` - Check marriage data consistency
- `validate_parentage()` - Check parent-child relationship validity

### 7. Help Actions (`actions/help_actions.py`)
**Status**: 📝 Scaffolded
**Lines**: 10

- `about()` - TODO: Show about dialog

### 8. Undo/Redo Manager (`commands/undo_redo_manager.py`)
**Status**: ✅ Complete
**Lines**: 55

**Responsibilities**:
- Implement Command pattern for undo/redo
- Maintain undo and redo stacks
- Execute commands and manage stack state

**Command Protocol**:
```python
class Command(Protocol):
    def run(self) -> None: ...
    def undo(self) -> None: ...
```

**Key Methods**:
- `execute(command)` - Run command and add to undo stack
- `undo()` - Undo last command
- `redo()` - Redo last undone command
- `can_undo()` / `can_redo()` - Check stack availability

---

## Scaffolded Components (Future Work)

### Models
Data classes to represent domain objects:
- **Person**: Genealogical person record
- **Marriage**: Marriage relationship between two persons
- **Event**: Life events (occupation, residence, etc.)

### Views
PySide6 widgets for visualization:
- **DynastyView**: Full dynasty tree visualization
- **TimelineView**: Chronological timeline of events
- **DataTable**: Spreadsheet-like data editing

### Commands - Genealogy Operations
Undoable commands for data modification:
- Add/Edit/Remove Person
- Add Marriage / End Marriage
- Add/Modify/Remove Event
- Assign/Unassign Parent relationships

### Commands - GUI Operations
Undoable view/scene operations:
- Move Node (drag-and-drop in tree view)
- Rebuild Scene (refresh visualization)
- Recompute Generations (recalculate levels)
- Timeline Scroll (navigate timeline)
- Preference Changes (settings/options)

---

## Database Schema

### Person Table
```sql
CREATE TABLE Person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    birth_month INTEGER,
    birth_year INTEGER,
    death_month INTEGER,
    death_year INTEGER,
    arrival_month INTEGER,
    arrival_year INTEGER,
    father_id INTEGER,
    mother_id INTEGER,
    moved_out_month INTEGER,
    moved_out_year INTEGER
);
```

### Event Table
```sql
CREATE TABLE Event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_title TEXT NOT NULL,
    start_month INTEGER,
    start_year INTEGER,
    end_month INTEGER,
    end_year INTEGER,
    notes TEXT,
    FOREIGN KEY(person_id) REFERENCES Person(id)
);
```

### Marriage Table
```sql
CREATE TABLE Marriage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spouse1_id INTEGER,
    spouse2_id INTEGER,
    marriage_month INTEGER,
    marriage_year INTEGER,
    dissolution_month INTEGER,
    dissolution_year INTEGER,
    dissolution_reason TEXT,
    FOREIGN KEY(spouse1_id) REFERENCES Person(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY(spouse2_id) REFERENCES Person(id)
        ON UPDATE CASCADE ON DELETE SET NULL
);
```

**Features**:
- Foreign key constraints enabled
- Cascade updates for person references
- NULL on delete (preserve marriage records)

---

## Development Workflow

### Adding New Features
1. **Create scaffolded files** if not already present
2. **Follow coding standards** (type hints, docstrings)
3. **Implement Command classes** for undoable operations
4. **Update UI** to call new commands
5. **Test** with sample dynasty files

### File Reference Guide
When extending the project, use these files as templates:

- **Class structure**: `database/db_manager.py` (property patterns, encapsulation)
- **Action handlers**: `actions/file_actions.py` (error handling, dialogs)
- **Menu integration**: `main.py` (action connections, UI updates)
- **Command pattern**: `commands/undo_redo_manager.py` (protocol usage)

---

## Dependencies

From `requirements.txt`:
- `PySide6==6.10.1` - Qt framework for Python
- `PySide6-Addons==6.10.1`
- `PySide6-Essentials==6.10.1`
- `QtPy==2.4.3` - Qt abstraction layer
- `shiboken6==6.10.1` - Python/C++ bindings

---

## Quick Reference: Sharing Code

### For Code Review
Share these core implementation files:
1. `main.py` - Application structure
2. `database/db_manager.py` - Data layer
3. `actions/file_actions.py` - File operations example
4. `commands/undo_redo_manager.py` - Command pattern

### For Architecture Discussion
Share:
1. This document (`CODEBASE_SUMMARY.md`)
2. `main.py` (first 50 lines for structure)
3. Database schema section from `db_manager.py`

### For Standards Review
Share examples from each category:
1. `main.py` (lines 10-45)
2. `db_manager.py` (lines 6-48)
3. `undo_redo_manager.py` (full file)

---

## Project Status

### ✅ Completed (Phase 1: Core Infrastructure)
- [x] Main application window and menu system
- [x] SQLite database management with `.dyn` format
- [x] File operations (New, Open, Save, Save As, Exit)
- [x] Undo/redo infrastructure with Command pattern
- [x] Project scaffolding for future components

### 🚧 In Progress (Phase 2: Data Models)
- [ ] Person model implementation
- [ ] Marriage model implementation
- [ ] Event model implementation

### 📋 Planned (Phase 3: Views & Visualization)
- [ ] Dynasty tree view widget
- [ ] Timeline view widget
- [ ] Data table view widget

### 📋 Planned (Phase 4: Commands & Operations)
- [ ] Genealogy commands (add/edit/remove)
- [ ] GUI commands (scene manipulation)
- [ ] Validation tools implementation

---

**Last Updated**: 2025-12-07
**Codebase Version**: 0.1.0 (Early Development)
