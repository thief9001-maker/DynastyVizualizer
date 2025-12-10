# DynastyVizualizer Codebase Summary

## Project Overview

**DynastyVizualizer** is a comprehensive family tree visualization and genealogy management application designed for games with multi-generational families, starting with [Ostriv](https://store.steampowered.com/app/773790/Ostriv/). It provides tools to create, manage, and visualize complex family dynasties with support for marriages, events, portraits, and genealogical relationships across multiple views and perspectives.

### Technology Stack
- **GUI Framework**: PySide6 (Qt for Python)
- **Database**: SQLite with custom `.dyn` file format
- **Language**: Python 3.10+
- **Patterns**: MVC architecture with Command pattern for undo/redo

### Vision
A beautiful, feature-rich genealogy application that combines the depth of professional genealogy software with the accessibility of modern UI design. Support for draggable person nodes, multiple visualization modes (tree, timeline, statistics), relationship tracing, portrait galleries, and historical event tracking.

---

## Codebase Statistics

- **Total Python Files**: 104 (12 implemented, 92 scaffolded)
- **Lines of Code**: ~1,400 (excluding comments and blank lines)
- **Total Lines**: ~2,900 (including docstrings and comments)
- **Implementation Status**: ~12% complete (Phase 1 nearing completion)
- **Estimated Final Size**: 10,000-15,000 lines of code

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

The application uses **Model-View-Controller (MVC)** architecture combined with the **Command Pattern** for undo/redo functionality. This architecture successfully scales to support complex features like draggable UI, multiple views, and relationship tracing.

#### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   MainWindow (main.py)                      │
│                   - Central Controller                      │
│                   - Menu bar and toolbar                    │
│                   - View switching and lifecycle            │
└──────────┬──────────────────────────────────┬───────────────┘
           │                                  │
           │ delegates to                     │ displays
           ▼                                  ▼
    ┌──────────────┐                  ┌──────────────────┐
    │   Actions    │                  │      Views       │
    │   Handlers   │                  │  (Presentation)  │
    │ (Controllers)│                  │                  │
    └──────┬───────┘                  │  • TreeView      │
           │                          │  • TimelineView  │
           │ creates/executes         │  • TableView     │
           ▼                          │  • StatsView     │
    ┌──────────────┐                  └────────┬─────────┘
    │   Commands   │                           │
    │  (Business   │                           │ reads from
    │   Logic)     │                           │
    └──────┬───────┘                           │
           │                                   │
           │ modifies                          │
           ▼                                   ▼
    ┌──────────────────────────────────────────────────────┐
    │              DatabaseManager (Model)                  │
    │              - SQLite .dyn files                      │
    │              - CRUD operations                        │
    │              - Data validation                        │
    └───────────────────────────────────────────────────────┘
```

#### Component Responsibilities

**Model (Data Layer)**
- `database/db_manager.py` - SQLite database operations
- `models/` - Data classes (Person, Marriage, Event, Family, Portrait, MajorEvent)
- Responsibilities:
  - Store and retrieve data
  - Enforce data integrity
  - Provide clean API for data access
  - Track dirty state (unsaved changes)

**View (Presentation Layer)**
- `views/tree_view/` - Family tree visualization
- `views/timeline_view/` - Chronological timeline
- `views/table_view/` - Spreadsheet-style tables
- `views/stats_view/` - Statistics dashboard
- `dialogs/` - Modal dialogs for data entry
- `widgets/` - Reusable UI components
- Responsibilities:
  - Display data to user
  - Capture user input
  - Emit signals on user actions
  - Update when data changes

**Controller (Logic Layer)**
- `main.py` - Central controller and view manager
- `actions/` - Action handlers for menu operations
- `commands/` - Business logic encapsulated as commands
- Responsibilities:
  - Respond to user actions
  - Create and execute commands
  - Coordinate between model and view
  - Manage application state

#### Command Pattern Integration

Every data modification goes through the command pattern for undo/redo support:

```
User Action Flow:
┌──────────┐      ┌──────────┐      ┌──────────────┐      ┌──────────┐
│   User   │─────▶│   View   │─────▶│   Action     │─────▶│ Command  │
│  (Click) │      │ (Signal) │      │   Handler    │      │ (Created)│
└──────────┘      └──────────┘      └──────────────┘      └────┬─────┘
                                                                │
                                                                ▼
                                                    ┌───────────────────┐
                                                    │  UndoRedoManager  │
                                                    │  execute(command) │
                                                    └─────────┬─────────┘
                                                              │
                                                              ▼
                                            ┌─────────────────────────────┐
                                            │  1. command.run()           │
                                            │  2. Modify database         │
                                            │  3. Push to undo stack      │
                                            │  4. Clear redo stack        │
                                            │  5. Emit signals to update  │
                                            └─────────────────────────────┘
```

#### Interaction Example: Adding a Person

Let's trace what happens when a user adds a new person:

**Step 1: User Initiates Action**
```
User clicks: Edit → Add Person
  ↓
main.py menu action triggered
  ↓
Calls: self.edit_actions.add_person()
```

**Step 2: Controller Creates Dialog**
```
actions/edit_actions.py:
  ↓
Opens: AddPersonDialog(self.parent)
  ↓
User fills form: Name, Gender, Birth Date, etc.
  ↓
User clicks: OK button
```

**Step 3: Dialog Creates Command**
```
dialogs/add_person_dialog.py:
  ↓
Creates: AddPersonCommand(db=self.db, first_name="John", last_name="Smith", ...)
  ↓
Passes to: self.parent.undo_manager.execute(command)
```

**Step 4: Command Executes**
```
commands/undo_redo_manager.py:
  execute(command):
    1. command.run()  ─────────────┐
       ↓                           │
    2. Add to undo stack           │
       self.undo_stack.append(cmd) │
       ↓                           │
    3. Clear redo stack            │
       self.redo_stack.clear()     │
                                   │
                                   ▼
commands/genealogy_commands/add_person.py:
  run():
    1. INSERT INTO Person (...) VALUES (...)
       ↓
    2. Store self.person_id = cursor.lastrowid
       ↓
    3. db.mark_dirty()
       ↓
    4. Emit signal: person_added(self.person_id)
```

**Step 5: Views Update**
```
Views listening to signals:
  ↓
TreeView.on_person_added(person_id)
  - Creates new PersonBox widget
  - Adds to scene
  - Runs layout engine
  ↓
TableView.on_person_added(person_id)
  - Adds new row to person table
  - Sorts if necessary
  ↓
MainWindow updates:
  - Sets title to show unsaved changes (*)
  - Enables Undo menu item
```

**Step 6: User Can Undo**
```
User presses: Ctrl+Z or Edit → Undo
  ↓
undo_manager.undo():
  1. Pop command from undo stack
  2. command.undo()  ────────────┐
  3. Push to redo stack          │
                                 │
                                 ▼
AddPersonCommand.undo():
  1. DELETE FROM Person WHERE id = self.person_id
  2. Emit signal: person_removed(self.person_id)
     ↓
Views update:
  - TreeView removes PersonBox
  - TableView removes row
  - MainWindow enables Redo
```

#### Interaction Example: Dragging a Person Box

Demonstrates how GUI operations are also commands:

**Step 1: User Drags Person Box**
```
User action: Click and drag PersonBox in TreeView
  ↓
views/tree_view/person_box.py:
  mousePressEvent()  - Record start position
  mouseMoveEvent()   - Update position in real-time
  mouseReleaseEvent() - Finalize position
```

**Step 2: Create Move Command**
```
views/tree_view/person_box.py:
  mouseReleaseEvent():
    old_pos = self.start_position
    new_pos = self.pos()
    ↓
Creates: MovePersonCommand(
           person_id=self.person_id,
           old_x=old_pos.x(), old_y=old_pos.y(),
           new_x=new_pos.x(), new_y=new_pos.y()
         )
    ↓
Executes via: undo_manager.execute(command)
```

**Step 3: Command Persists Position**
```
commands/gui_commands/move_person.py:
  run():
    1. UPDATE PersonPosition
       SET x_position=new_x, y_position=new_y
       WHERE person_id=self.person_id
    2. db.mark_dirty()
    3. (Visual position already updated during drag)
```

**Step 4: Undo Restores Position**
```
User presses: Ctrl+Z
  ↓
MovePersonCommand.undo():
  1. UPDATE PersonPosition
     SET x_position=old_x, y_position=old_y
  2. Emit signal: person_position_changed(person_id)
     ↓
TreeView.on_person_position_changed():
  - Animates PersonBox back to original position
```

#### Data Flow Patterns

**Read Operations (No Commands Needed)**
```
View needs data:
  1. View calls: db_manager.query(...)
  2. Database returns: list[Person] or Person object
  3. View creates widgets to display data
  4. No undo/redo needed (read-only)
```

**Write Operations (Via Commands)**
```
Modification needed:
  1. Create command object
  2. Execute via undo_manager.execute(command)
  3. Command.run() modifies database
  4. Command pushed to undo stack
  5. Views notified via signals
  6. All commands are undoable
```

**Multi-View Synchronization**
```
Data changes in one view:
  1. Command modifies database
  2. Command emits Qt signal
  3. All views listening to that signal update
  4. Example signals:
     - person_added(person_id)
     - person_modified(person_id)
     - person_deleted(person_id)
     - marriage_created(marriage_id)
     - etc.
```

#### Why This Pattern Works

**Separation of Concerns**
- Model knows nothing about views
- Views know nothing about business logic
- Commands encapsulate all business logic
- Easy to test each layer independently

**Undo/Redo Everything**
- UI changes (drag person box) → MovePersonCommand
- Data changes (add person) → AddPersonCommand
- Bulk operations (CSV import) → ImportCSVCommand
- Settings changes → ChangeSettingCommand
- All operations are undoable by design

**Multiple Views Without Coupling**
- TreeView, TimelineView, TableView, StatsView all observe the same data
- Any view can trigger commands
- All views automatically update via signals
- Views never directly call each other

**Scalability**
- New operation? Create new command class
- New view? Create new widget and connect signals
- New feature? Add to appropriate layer
- No changes to existing code structure

**Qt Integration**
- Signals/slots provide automatic observer pattern
- QGraphicsView provides scene/view separation
- QAbstractTableModel for table views
- Qt's undo framework could be integrated later

---

## Database Schema

### Complete Schema (All Phases)

All tables are created from the start to ensure consistency. Dates support flexible precision: year only, year/month, or full year/month/day. Any component can be NULL.

**Migration**: Existing `.dyn` files can be safely upgraded using `scripts/migrate_database.py`

---

#### Person Table
```sql
CREATE TABLE Person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    maiden_name TEXT,
    gender TEXT,
    -- Birth date (flexible: year, year/month, or year/month/day)
    birth_year INTEGER,
    birth_month INTEGER,
    birth_day INTEGER,
    -- Death date (flexible precision)
    death_year INTEGER,
    death_month INTEGER,
    death_day INTEGER,
    -- Arrival date (when moved into town/game)
    arrival_year INTEGER,
    arrival_month INTEGER,
    arrival_day INTEGER,
    -- Move-out date (when left town/game)
    moved_out_year INTEGER,
    moved_out_month INTEGER,
    moved_out_day INTEGER,
    -- Relationships
    father_id INTEGER,
    mother_id INTEGER,
    family_id INTEGER,
    notes TEXT,
    FOREIGN KEY(father_id) REFERENCES Person(id) ON DELETE SET NULL,
    FOREIGN KEY(mother_id) REFERENCES Person(id) ON DELETE SET NULL,
    FOREIGN KEY(family_id) REFERENCES Family(id) ON DELETE SET NULL
);
```

**Features**:
- Flexible date precision (all day fields can be NULL for Ostriv, populated for real-world genealogy)
- Maiden name tracking for married individuals
- Family dynasty grouping via `family_id`
- General notes field for additional context

---

#### Event Table
```sql
CREATE TABLE Event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_title TEXT NOT NULL,
    -- Start date (flexible precision)
    start_year INTEGER,
    start_month INTEGER,
    start_day INTEGER,
    -- End date (for ongoing events like jobs)
    end_year INTEGER,
    end_month INTEGER,
    end_day INTEGER,
    notes TEXT,
    FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
);
```

**Event Types**: `job`, `illness`, `injury`, `residence`, `education`, `military`, `custom`

**Features**:
- Support for both point-in-time events (marriage, birth) and duration events (job, illness)
- Flexible date precision for all historical contexts

---

#### Marriage Table
```sql
CREATE TABLE Marriage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spouse1_id INTEGER,
    spouse2_id INTEGER,
    -- Marriage date (flexible precision)
    marriage_year INTEGER,
    marriage_month INTEGER,
    marriage_day INTEGER,
    -- Dissolution date (divorce/death)
    dissolution_year INTEGER,
    dissolution_month INTEGER,
    dissolution_day INTEGER,
    dissolution_reason TEXT,
    marriage_type TEXT DEFAULT 'spouse',  -- 'spouse', 'concubine', 'affair'
    FOREIGN KEY(spouse1_id) REFERENCES Person(id)
        ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY(spouse2_id) REFERENCES Person(id)
        ON UPDATE CASCADE ON DELETE SET NULL
);
```

**Features**:
- Support for multiple marriage types (spouse, concubine, affair for games like Crusader Kings)
- Track dissolution reason (death, divorce, annulment)
- Flexible date precision
- Cascade updates for person ID changes
- Preserve marriage records even if persons are deleted (SET NULL)

---

#### Portrait Table
```sql
CREATE TABLE Portrait (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    -- Date range when this portrait is valid (flexible precision)
    valid_from_year INTEGER,
    valid_from_month INTEGER,
    valid_from_day INTEGER,
    valid_to_year INTEGER,
    valid_to_month INTEGER,
    valid_to_day INTEGER,
    is_primary INTEGER DEFAULT 0,
    display_order INTEGER DEFAULT 0,
    FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
);
```

**Features**:
- Multiple portraits per person
- Date-based portrait switching (e.g., "looked like this from 1705-1720")
- Cycle through portraits automatically or manually
- Primary portrait designation
- Display order for galleries

---

#### Family Table
```sql
CREATE TABLE Family (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname TEXT NOT NULL,
    -- Move-in date (when family arrived)
    move_in_year INTEGER,
    move_in_month INTEGER,
    move_in_day INTEGER,
    coat_of_arms_path TEXT,
    family_color TEXT,  -- RGB hex code for visualization
    is_extinct INTEGER DEFAULT 0,
    notes TEXT
);
```

**Purpose**: Group people by family dynasty (not just surname), track move-in dates, extinction status

**Note**: Multiple families can share the same surname if they moved in separately

**Features**:
- Coat of arms/family image support
- Color-coding for visual identification
- Extinction tracking

---

#### MajorEvent Table
```sql
CREATE TABLE MajorEvent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    event_type TEXT NOT NULL,  -- 'war', 'disaster', 'plague', 'festival', etc.
    -- Start date (year required, month/day optional)
    start_year INTEGER NOT NULL,
    start_month INTEGER,
    start_day INTEGER,
    -- End date (for ongoing events like wars)
    end_year INTEGER,
    end_month INTEGER,
    end_day INTEGER,
    description TEXT,
    color TEXT  -- For timeline visualization
);
```

**Purpose**: Historical context markers displayed across all families in timeline view

**Examples**: World War 1, Great Plague of 1665, Town Fire of 1720

**Features**:
- Flexible date precision
- Support for both point events and duration events
- Color-coding for visual distinction in timeline

---

#### PersonPosition Table
```sql
CREATE TABLE PersonPosition (
    person_id INTEGER PRIMARY KEY,
    view_type TEXT NOT NULL,  -- 'tree', 'custom'
    x_position REAL NOT NULL,
    y_position REAL NOT NULL,
    FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
);
```

**Purpose**: Store custom positions when user drags person boxes in tree view

**Features**:
- Per-person custom positioning
- Automatic layout as fallback if no custom position
- View-type support for future multiple tree layouts

---

#### Settings Table
```sql
CREATE TABLE Settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

**Purpose**: Store user preferences and application settings

**Example Settings**:
- `date_format` → "YYYY-MM-DD", "DD/MM/YYYY", etc.
- `auto_surname_change` → "true", "false"
- `surname_inheritance` → "paternal", "maternal", "choice"
- `default_skin` → "default", "parchment", "blueprint"
- `auto_save_interval` → "300" (seconds)

---

### Date Flexibility Design

All date fields follow the pattern: `year`, `month`, `day`

**Ostriv Usage** (no day precision):
- `birth_year = 1705, birth_month = 3, birth_day = NULL`
- Display: "March 1705"

**Real-World Genealogy** (full precision):
- `birth_year = 1705, birth_month = 3, birth_day = 15`
- Display: "March 15, 1705" or "15/03/1705"

**Unknown Month** (year only):
- `birth_year = 1705, birth_month = NULL, birth_day = NULL`
- Display: "1705"

This design supports seamless transitions between game contexts and real-world use.

---

## Directory Structure

Complete file structure with implementation status:

```
DynastyVizualizer/
├── main.py                              # Application entry point (280 lines) ✅
│
├── database/                            # Data layer (Model)
│   ├── __init__.py
│   └── db_manager.py                   # SQLite CRUD operations (268 lines) ✅
│
├── models/                              # Data model classes
│   ├── __init__.py
│   ├── person.py                       # Person dataclass model (170 lines) ✅
│   ├── marriage.py                     # Marriage relationship (41 lines) 📋
│   ├── event.py                        # Life events (41 lines) 📋
│   ├── portrait.py                     # Portrait metadata (30 lines) 📋
│   ├── family.py                       # Family dynasty (35 lines) 📋
│   └── major_event.py                  # Historical events (30 lines) 📋
│
├── actions/                             # Menu action handlers (Controllers)
│   ├── __init__.py                     # (6 lines) ✅
│   ├── file_actions.py                 # New/Open/Save/Exit (159 lines) ✅
│   ├── edit_actions.py                 # Undo/Redo/Add/Remove (29 lines) ✅
│   ├── view_actions.py                 # View switching (22 lines) ✅
│   ├── tools_actions.py                # Validation tools (22 lines) ✅
│   ├── settings_actions.py             # Settings configuration (27 lines) ✅
│   └── help_actions.py                 # About dialog (10 lines) ✅
│
├── commands/                            # Command pattern for undo/redo
│   ├── __init__.py
│   ├── undo_redo_manager.py            # Command manager (55 lines) ✅
│   ├── base_command.py                 # Base command class (13 lines) 📋
│   │
│   ├── genealogy commands/             # Genealogy operations [PHASE 2-3]
│   │   ├── __init__.py
│   │   ├── add_person.py               # Create new person (23 lines) 📋
│   │   ├── edit_person.py              # Modify person data (24 lines) 📋
│   │   ├── remove_person.py            # Delete person (24 lines) 📋
│   │   ├── add_marriage.py             # Create marriage (25 lines) 📋
│   │   ├── edit_marriage.py            # Modify marriage (25 lines) 📋
│   │   ├── end_marriage.py             # End marriage (30 lines) 📋
│   │   ├── delete_marriage.py          # Delete marriage (24 lines) 📋
│   │   ├── create_child.py             # Create with parents (30 lines) 📋
│   │   ├── add_event.py                # Add life event (23 lines) 📋
│   │   ├── edit_event.py               # Modify event (24 lines) 📋
│   │   ├── delete_event.py             # Delete event (24 lines) 📋
│   │   ├── assign_parent.py            # Set parent link (33 lines) 📋
│   │   └── unassign_parent.py          # Remove parent link (31 lines) 📋
│   │
│   └── GUI commands/                   # GUI operations [PHASE 3-5]
│       ├── __init__.py
│       ├── move_person.py              # Drag-and-drop (28 lines) 📋
│       ├── rebuild_scene.py            # Rebuild view (25 lines) 📋
│       ├── recompute_generations.py    # Recalc generations (26 lines) 📋
│       ├── change_skin.py              # Switch theme (26 lines) 📋
│       └── change_view.py              # Switch view mode (27 lines) 📋
│
├── views/                               # Visualization layer (Views)
│   ├── __init__.py
│   ├── data_table.py                   # (placeholder)
│   ├── dynasty_view.py                 # (placeholder)
│   ├── timeline_view.py                # (placeholder)
│   │
│   ├── tree_view/                      # Family tree visualization [PHASE 3]
│   │   ├── __init__.py                 # 📋
│   │   ├── tree_canvas.py              # Main canvas (25 lines) 📋
│   │   ├── person_box.py               # Person widget (38 lines) 📋
│   │   ├── marriage_node.py            # Marriage connector (20 lines) 📋
│   │   ├── relationship_line.py        # Parent-child lines (27 lines) 📋
│   │   ├── layout_engine.py            # Auto-positioning (20 lines) 📋
│   │   └── generation_band.py          # Gen markers (25 lines) 📋
│   │
│   ├── timeline_view/                  # Timeline visualization [PHASE 5]
│   │   ├── timeline_canvas.py          # Timeline canvas (25 lines) 📋
│   │   ├── family_bar.py               # Family lifespan (24 lines) 📋
│   │   ├── person_bar.py               # Person lifespan (27 lines) 📋
│   │   ├── event_marker.py             # Event icons (20 lines) 📋
│   │   └── major_event_marker.py       # Historical events (20 lines) 📋
│   │
│   ├── table_view/                     # Database tables [PHASE 6]
│   │   ├── person_table.py             # People table (28 lines) 📋
│   │   ├── marriage_table.py           # Marriages table (28 lines) 📋
│   │   ├── event_table.py              # Events table (28 lines) 📋
│   │   └── family_table.py             # Families table (26 lines) 📋
│   │
│   └── stats_view/                     # Statistics [PHASE 7]
│       ├── family_dashboard.py         # Stats dashboard (25 lines) 📋
│       ├── comparison_widget.py        # Compare entities (25 lines) 📋
│       └── charts.py                   # Visual charts (24 lines) 📋
│
├── widgets/                             # Reusable UI components
│   ├── __init__.py
│   ├── date_picker.py                  # Date input widget (20 lines) 📋
│   ├── person_selector.py              # Person dropdown (20 lines) 📋
│   ├── portrait_gallery.py             # Portrait display (24 lines) 📋
│   ├── extended_details_panel.py       # Detail panel (30 lines) 📋
│   └── search_bar.py                   # Search widget (26 lines) 📋
│
├── dialogs/                             # Modal dialogs
│   ├── __init__.py                     # 📋
│   ├── add_person_dialog.py            # Add person form (18 lines) 📋
│   ├── edit_person_dialog.py           # Edit person form (18 lines) 📋
│   ├── create_marriage_dialog.py       # Marriage form (19 lines) 📋
│   ├── create_child_dialog.py          # Child form (20 lines) 📋
│   ├── add_event_dialog.py             # Event form (21 lines) 📋
│   ├── settings_dialog.py              # Settings configuration (15 lines) 📋
│   ├── import_csv_dialog.py            # CSV import (22 lines) 📋
│   └── about_dialog.py                 # About dialog (13 lines) 📋
│
├── utils/                               # Utility modules
│   ├── __init__.py                     # 📋
│   ├── settings_manager.py             # Settings/shortcuts mgr (180 lines) ✅
│   ├── relationship_calculator.py      # Relationship logic (20 lines) 📋
│   ├── generation_calculator.py        # Generation levels (16 lines) 📋
│   ├── validators.py                   # Data validation (28 lines) 📋
│   ├── csv_importer.py                 # CSV import (36 lines) 📋
│   ├── skin_manager.py                 # Theme management (32 lines) 📋
│   └── color_manager.py                # Color utilities (33 lines) 📋
│
├── resources/                           # Assets [PHASE 8]
│   ├── skins/                          # UI themes
│   ├── icons/                          # App icons
│   └── default_portraits/              # Portrait placeholders
│
├── scripts/                             # Development tools
│   ├── create_codebase_summary.py      # Code snapshot tool ✅
│   └── migrate_database.py             # Database migration ✅
│
├── CODEBASE_SUMMARY.md                 # This file ✅
├── README.md                           # User documentation ✅
├── requirements.txt                    # Python dependencies ✅
└── LICENSE                             # MIT License ✅

Legend:
  ✅ = Fully implemented
  📋 = Scaffolded (class structure, docstrings, TODOs)
  [PHASE X] = Target implementation phase
```

### File Count Summary

**By Status:**
- ✅ Implemented: 12 files (main.py, database, actions, models/person.py, utils/settings_manager.py, undo_redo_manager)
- 📋 Scaffolded: 92 files (models, commands, views, widgets, dialogs, utils)
- Total Python files: 104

**By Category:**
- Core: 1 (main.py)
- Database: 1 (db_manager.py)
- Models: 6 (person ✅, marriage, event, portrait, family, major_event)
- Actions: 6 (file, edit, view, tools, settings ✅, help)
- Commands: 20 (base + 13 genealogy + 5 GUI + undo_redo_manager)
- Views: 22 (tree: 6, timeline: 5, table: 4, stats: 3, other: 4)
- Widgets: 5 (date_picker, person_selector, portrait_gallery, extended_details, search_bar)
- Dialogs: 9 (add_person, edit_person, create_marriage, create_child, add_event, settings 📋, import_csv, about)
- Utils: 7 (settings_manager ✅, relationship_calculator, generation_calculator, validators, csv_importer, skin_manager, color_manager)
- Scripts: 2 (create_codebase_summary, migrate_database)
- Documentation: 3 (CODEBASE_SUMMARY, README, LICENSE)

### Implementation Checklist

Use this checklist to track development progress:

**Phase 1: Foundation** (~80% complete)
- [x] Main window and menu structure
- [x] Database schema and management
- [x] File operations (New/Open/Save)
- [x] Undo/redo infrastructure
- [x] Settings management system
- [x] Keyboard shortcut handling
- [x] Settings menu with configuration options
- [ ] Basic dialogs (Add Person, About)
- [ ] Error handling and user feedback

**Phase 2: Models & CRUD** (~8% complete)
- [x] Implement Person model with dataclass
- [ ] Implement Marriage model (4 properties)
- [ ] Implement Event model (5 properties)
- [ ] Implement Portrait model (4 properties)
- [ ] Implement Family model (4 properties)
- [ ] Implement MajorEvent model (5 properties)
- [ ] Implement AddPersonCommand
- [ ] Implement EditPersonCommand
- [ ] Implement RemovePersonCommand
- [ ] Implement AddMarriageCommand
- [ ] Implement AddPersonDialog (13 fields)
- [ ] Implement EditPersonDialog
- [ ] Implement DatePicker widget
- [ ] Implement PersonSelector widget

**Phase 3: Tree Visualization** (0% complete)
- [ ] Implement PersonBox widget
- [ ] Implement MarriageNode widget
- [ ] Implement RelationshipLine widget
- [ ] Implement TreeLayoutEngine
- [ ] Implement TreeCanvas
- [ ] Implement GenerationBand
- [ ] Implement MovePersonCommand
- [ ] Implement ExtendedDetailsPanel

**Phases 4-9:** See roadmap section for detailed breakdown

---

## Development Roadmap

### 🚧 **Phase 1: Foundation** (CURRENT - Weeks 1-2)
**Status**: ~80% Complete
**Lines**: ~1,150

Core infrastructure for database management, undo/redo, settings, and application framework.

**Completed:**
- [x] Main application window and menu structure with Settings menu
- [x] Comprehensive database schema (all 8 tables with flexible dates)
- [x] SQLite database management (`.dyn` format with automatic migration support)
- [x] File operations (New, Open, Save, Save As, Exit) - fully functional
- [x] Undo/redo infrastructure (Command pattern framework)
- [x] Action handler framework (file, edit, view, tools, settings, help)
- [x] Settings management system with disk persistence (QSettings)
- [x] **Keyboard shortcut system** - All menu actions have customizable shortcuts:
  - File: Ctrl+N (New), Ctrl+O (Open), Ctrl+S (Save), Ctrl+Shift+S (Save As), Ctrl+Q (Exit)
  - Edit: Ctrl+Z (Undo), Ctrl+Y (Redo), Ctrl+P (Add Person), Del (Remove Person)
  - View: Ctrl+1-4 (Switch views)
  - Tools: F5 (Rebuild Scene), Ctrl+R (Recompute Generations)
  - Settings: Ctrl+, (Settings)
  - Help: F1 (About)
- [x] Project scaffolding (all 104 files created)

**In Progress:**
- [ ] Edit menu functionality (Add Person, Remove Person dialogs)
- [ ] Settings dialog implementation (currently scaffolded placeholders)
- [ ] Help menu functionality (About dialog)
- [ ] Basic error dialogs and user feedback
- [ ] Application icon and branding

**Key Files**: `main.py`, `database/db_manager.py`, `actions/`, `utils/settings_manager.py`, `commands/undo_redo_manager.py`

**Next Steps**: Implement Add Person dialog and command, implement Settings dialog UI

---

### 📋 **Phase 2: Data Models & Basic CRUD** (Weeks 2-5)
**Status**: Started (~8% complete)
**Estimated Lines**: +1,200

Build data models and basic create/read/update/delete operations with dialogs.

**Completed:**
- [x] **Person model with dataclass** - Full implementation with 20+ properties:
  - Name fields: first_name, middle_name, last_name, maiden_name, nickname
  - Flexible date support: birth/death/arrival/moved_out (year/month/day)
  - Relationships: father_id, mother_id, family_id
  - Game fields: is_founder, education, dynasty_id
  - Computed properties: full_name, display_name, is_deceased
  - Utility methods: get_age(year), is_alive_in_year(year), get_age_at_death()
  - Date formatting: get_birth_date_string(), get_death_date_string(), get_lifespan_string()

**Goals:**
- [ ] Implement `Marriage`, `Event` model classes
- [ ] Create `AddPersonCommand`, `EditPersonCommand`, `DeletePersonCommand`
- [ ] Create `AddPersonDialog`, `EditPersonDialog` with full validation
- [ ] Build `CreateMarriageCommand`, `CreateChildCommand`
- [ ] Build `CreateMarriageDialog`
- [ ] Implement flexible date handling widget (year/month/day with nulls)
- [ ] Add portrait support (`Portrait` model + upload functionality)
- [ ] Create `DatePicker` widget (supports partial dates)
- [ ] Create `PersonSelector` widget (searchable dropdown)
- [ ] Implement basic list view to display people

**Deliverable**: Can add, edit, and delete people and marriages through functional dialogs

**Key Files**: `models/person.py` ✅, `commands/genealogy_commands/`, `dialogs/`, `widgets/date_picker.py`

**Next Steps**: Implement AddPersonDialog and AddPersonCommand, create PersonRepository

---

### 📋 **Phase 3: Tree Visualization** (Weeks 6-10)
**Status**: Not Started
**Estimated Lines**: +2,500

Build the interactive family tree view with QGraphicsView and custom widgets.

**Goals:**
- [ ] Create `PersonBox` custom QGraphicsWidget (portrait + name + dates + gear icon)
- [ ] Create `MarriageNode` widget (connection point + dates)
- [ ] Create `RelationshipLine` widget (parent-child connectors using QPainterPath)
- [ ] Implement `TreeLayoutEngine` (automatic generational positioning algorithm)
- [ ] Build `TreeCanvas` (QGraphicsView with scrollable, zoomable scene)
- [ ] Implement generation bands with labels
- [ ] Add drag-and-drop for creating marriages (drop person on person)
- [ ] Add drag-and-drop for repositioning person boxes
- [ ] Implement `MovePersonCommand` (undoable position changes)
- [ ] Add in-place editing (click name/date to edit)
- [ ] Implement gear icon → extended details panel
- [ ] Build `ExtendedDetailsPanel` (tabbed: Info, Events, Relationships, Portraits)
- [ ] Add right-click context menus

**Deliverable**: Fully interactive family tree with draggable people, marriages, and visual hierarchy

**Key Files**: `views/tree_view/`, `widgets/extended_details_panel.py`, `commands/gui_commands/move_person.py`

---

### 🚧 **Phase 4: Relationship Analysis** (Week 11-13)
**Status**: Not Started
**Estimated Lines**: +800

Implement relationship tracing and highlighting.

**Goals:**
- [ ] Create `RelationshipCalculator` utility (graph traversal)
- [ ] Single-click selection highlights immediate family (parents, spouses, children)
- [ ] Double-click sets person as "primary" and labels all relationships
  - Brother, Sister, Father, Mother, Spouse, Ex-Spouse
  - Grandfather, Grandmother, Uncle, Aunt, Cousin
  - Step-parent, Step-sibling, Half-sibling
  - "1st removed", "2nd removed" for distant relatives
- [ ] Ctrl+Click two people to find relationship path
  - Highlight path with gradient (green → yellow → red by distance)
  - Show relationship description in popup
  - Dim unrelated people
- [ ] Implement search bar with real-time pruning
  - Type name → filter tree to matching people + connections
  - Highlight matches
  - Auto-scroll to first match

**Deliverable**: Visual relationship exploration and tracing

**Key Files**: `utils/relationship_calculator.py`, `views/tree_view/tree_canvas.py`, `widgets/search_bar.py`

---

### 🚧 **Phase 5: Timeline View** (Week 14-17)
**Status**: Not Started
**Estimated Lines**: +1,800

Build chronological timeline visualization with family lifespans.

**Goals:**
- [ ] Create `TimelineCanvas` (horizontal scrolling timeline)
- [ ] Create `FamilyBar` widget (collapsible family lifespan)
  - Show family move-in → extinction dates
  - Chevron to expand/collapse members
  - Sticky header while scrolling through family
- [ ] Create `PersonBar` widget (individual lifespan bar)
  - Birth → death (or current date)
  - Portrait thumbnail
  - Event markers on bar (marriage, children, job changes, etc.)
- [ ] Create `EventMarker` widget (clickable icons on person bars)
- [ ] Create `MajorEventMarker` widget (vertical line across all families)
- [ ] Implement `Family` model and database table
- [ ] Implement `MajorEvent` model and database table
- [ ] Add "Add Major Event" dialog
- [ ] Implement sticky header logic (pin family bar, bump on scroll past)

**Deliverable**: Timeline view showing family lifespans and events

**Key Files**: `views/timeline_view/`, `models/family.py`, `models/major_event.py`

---

### 🚧 **Phase 6: Table View & Data Management** (Week 18-20)
**Status**: Not Started
**Estimated Lines**: +900

Build database table views for spreadsheet-style editing.

**Goals:**
- [ ] Create `PersonTableWidget` (sortable, filterable, editable)
- [ ] Create `MarriageTableWidget`
- [ ] Create `EventTableWidget`
- [ ] Create `FamilyTableWidget` (with computed statistics)
- [ ] Add warning dialog on first open ("editing raw data")
- [ ] Implement `EditCellCommand` (undoable table edits)
- [ ] Add computed fields to Family table:
  - Member count (living/total)
  - Longest lived member
  - Most children (father/mother separately)
- [ ] Build CSV import functionality
  - Flexible date format detection (YYYY-MM-DD, MM-DD-YYYY, etc.)
  - Column mapping dialog
  - Validation and error preview
  - Bulk `ImportPersonsCommand`

**Deliverable**: Spreadsheet-style data editing and CSV import

**Key Files**: `views/table_view/`, `dialogs/import_csv_dialog.py`, `utils/csv_importer.py`

---

### 🚧 **Phase 7: Statistics & Analytics** (Week 21-23)
**Status**: Not Started
**Estimated Lines**: +1,100

Build family statistics dashboard and comparison tools.

**Goals:**
- [ ] Create `FamilyDashboard` widget with cards showing:
  - Total families, living persons, deceased persons
  - Average lifespan
  - Largest family, most marriages, most children
  - Current generation count
- [ ] Add charts (using matplotlib or Qt Charts):
  - Population over time (line chart)
  - Deaths per year (bar chart)
  - Family size distribution (pie chart)
- [ ] Build family comparison tool (Ctrl+Click families)
  - Side-by-side statistics
  - Intermarriage count (connections between families)
  - Shared ancestors
- [ ] Implement data validation tools:
  - `MarriageValidator` (overlapping marriages, invalid dates)
  - `ParentageValidator` (circular parentage, impossible dates)
  - Validation report with clickable issues
- [ ] Implement `GenerationCalculator` utility
  - Recompute generations from founders (BFS algorithm)
  - Handle edge cases (adoptions, remarriages)

**Deliverable**: Statistics dashboard and data validation tools

**Key Files**: `views/stats_view/`, `utils/validators.py`, `utils/generation_calculator.py`

---

### 🚧 **Phase 8: Visual Customization** (Week 24-26)
**Status**: Not Started
**Estimated Lines**: +1,200

Implement UI skins, portrait management, and family color coding.

**Goals:**
- [ ] Create `SkinManager` class (load skins from JSON)
- [ ] Build built-in skins:
  - Default (clean, modern)
  - Parchment (aged paper aesthetic)
  - Blueprint (technical drawing style)
  - Medieval (illuminated manuscript)
- [ ] Add skin selector to preferences
- [ ] Support user custom skins (import skin folder)
- [ ] Implement `PortraitGallery` widget
  - Display multiple portraits per person
  - Add/edit/delete portraits
  - Set date ranges for portraits (valid from → valid to)
  - Auto-cycle or manual selection
- [ ] Build portrait import workflow
  - Copy images to `/portraits/` subdirectory
  - Support PNG, JPG, GIF formats
  - Thumbnail generation
- [ ] Implement family color coding (optional feature)
  - **Option A**: Mixed colors (genetic blending)
  - **Option B**: Striped patterns (proportional stripes)
  - **Option C**: Relationship gradient (green=close, red=distant)
  - Toggle in preferences (default: off)

**Deliverable**: Themeable UI and comprehensive portrait management

**Key Files**: `utils/skin_manager.py`, `utils/color_manager.py`, `widgets/portrait_gallery.py`, `resources/skins/`

---

### 🚧 **Phase 9: Polish & Advanced Features** (Week 27-30)
**Status**: Partially Started (~15% complete)
**Estimated Lines**: +800

Final polish, preferences, keyboard shortcuts, and quality-of-life features.

**Completed:**
- [x] **Keyboard shortcuts** - Full implementation with customizable shortcuts via SettingsManager:
  - Ctrl+N/O/S (File operations)
  - Ctrl+Z/Y (Undo/Redo)
  - Ctrl+P (Add Person), Del (Delete)
  - Ctrl+1/2/3/4 (Switch views)
  - F5 (Rebuild Scene), Ctrl+R (Recompute Generations)
- [x] Settings management infrastructure with disk persistence

**Goals:**
- [ ] Build `SettingsDialog` with tabs:
  - General (date format, auto-save interval, confirmations)
  - Shortcuts (customize all keyboard shortcuts)
  - Display (skin, font size, color scheme)
  - Appearance (colors, node styles)
  - Formats (date/name display formats)
- [ ] Add comprehensive right-click context menus
- [ ] Build `AboutDialog` with credits and version info
- [ ] Implement export functionality:
  - Export tree view as PNG/JPG
  - Export entire tree (not just viewport)
  - Resolution multiplier (1x, 2x, 4x)
  - Optional: PDF export (multi-page)
- [ ] Create first-run tutorial/welcome dialog
- [ ] Add sample dynasty database (pre-populated example)
- [ ] Implement auto-save with configurable interval
- [ ] Add keyboard shortcut reference (Help menu)

**Deliverable**: Polished, production-ready application

**Key Files**: `dialogs/preferences_dialog.py`, `dialogs/about_dialog.py`, `utils/export_manager.py`

---

### 📋 **Phase 10: Future Enhancements** (Post-Release)

**Potential Features:**
- [ ] Multi-dynasty support (tabs for multiple open files)
- [ ] Cloud sync and sharing
- [ ] Collaboration features (concurrent editing)
- [ ] Game-specific integrations:
  - Ostriv save file import
  - Crusader Kings 3 save file import
  - Support for titles, claims, traits (CK3)
- [ ] Mobile version (touch-optimized)
- [ ] Advanced genealogy features:
  - DNA inheritance simulation
  - Genetic trait tracking
  - Ancestry composition
- [ ] Research log and citations
- [ ] Media attachments (documents, certificates)

---

## Current Implementation Details

### Implemented Components (Phase 1 Complete)

#### 1. **main.py** (222 lines) ✅
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

#### 2. **database/db_manager.py** (193 lines) ✅
**Responsibilities**:
- Manage SQLite connections to `.dyn` files
- Create new databases with schema initialization
- Open existing dynasty files
- Save/commit changes to disk
- Track dirty state (unsaved changes)

**Key Methods**:
- `new_database(file_path: str)` - Create fresh `.dyn` file
- `open_database(file_path: str)` - Open existing file
- `save_database(path: str | None)` - Save or "Save As"
- `mark_dirty()` / `mark_clean()` - Track unsaved changes

**Properties**:
- `is_open` - Check if database is loaded
- `is_dirty` - Check if there are unsaved changes
- `database_name` - Get filename without path
- `database_directory` - Get directory path

#### 3. **actions/file_actions.py** (159 lines) ✅
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

#### 4. **actions/edit_actions.py** (29 lines) ⚠️ Partial
**Implemented**:
- `undo()` - Undo last action
- `redo()` - Redo last undone action

**Scaffolded** (Phase 2):
- `add_person()` - TODO: Implement with dialog
- `remove_person()` - TODO: Implement with confirmation
- `add_new_family()` - TODO: Implement family creation

#### 5. **commands/undo_redo_manager.py** (55 lines) ✅
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
- `execute(command: Command)` - Run command and add to undo stack
- `undo()` - Undo last command
- `redo()` - Redo last undone command
- `can_undo()` / `can_redo()` - Check stack availability

---

## Architecture Validation

### Is MVC + Command Still Appropriate?

**YES** - The architecture scales excellently for all planned features:

✅ **Draggable UI**: `MovePersonCommand` makes position changes undoable
✅ **Multiple Views**: Each view is a separate widget, no coupling
✅ **Relationship Tracing**: Pure data operations in `RelationshipCalculator`
✅ **Complex Operations**: Marriage creation, child creation = discrete commands
✅ **Data Import**: `ImportCSVCommand` wraps bulk operations
✅ **Preferences**: Settings changes = commands (undoable theme switches, etc.)

### Pattern Benefits for This Project

1. **Undo/Redo Everything**: UI changes, data changes, imports - all undoable
2. **View Independence**: Tree, Timeline, Table, Stats views all observe same models
3. **Testability**: Commands are isolated, testable units
4. **Extensibility**: Adding new operations = adding new command classes
5. **Qt Integration**: Signals/slots naturally fit observer pattern

---

## Development Best Practices

### When Adding New Features

1. **Model First**: Create data model class with properties
2. **Database Schema**: Add/update database tables
3. **Commands**: Create undoable command classes
4. **UI**: Build widgets/dialogs
5. **Integration**: Wire to menus/actions
6. **Test**: Verify undo/redo works

### File Reference Guide

Use these files as implementation templates:

- **Data Models**: (Phase 2 - to be created)
- **Commands**: `commands/undo_redo_manager.py` (protocol usage)
- **Action Handlers**: `actions/file_actions.py` (error handling, dialogs)
- **Database**: `database/db_manager.py` (property patterns, encapsulation)
- **Main Window**: `main.py` (action connections, UI updates)

---

## Dependencies

From `requirements.txt`:
- `PySide6==6.10.1` - Qt framework for Python
- `PySide6-Addons==6.10.1` - Additional Qt modules
- `PySide6-Essentials==6.10.1` - Core Qt functionality
- `QtPy==2.4.3` - Qt abstraction layer
- `shiboken6==6.10.1` - Python/C++ bindings

**Future Dependencies** (Phase 7-9):
- `matplotlib` or `pyqtgraph` - For statistics charts
- `Pillow` - For image processing (thumbnails, portraits)

---

## Quick Reference: Context Bundles

### For Architecture Discussion
Share:
1. This document (`CODEBASE_SUMMARY.md`)
2. `main.py` (first 100 lines for structure)
3. Database schema sections

### For Code Review
Share these implementation files:
1. `main.py` - Application structure
2. `database/db_manager.py` - Data layer
3. `actions/file_actions.py` - Example action handler
4. `commands/undo_redo_manager.py` - Command pattern

### For Standards Review
Share examples from each category:
1. `main.py` (lines 10-45)
2. `database/db_manager.py` (lines 6-48)
3. `commands/undo_redo_manager.py` (full file)

---

**Last Updated**: 2025-12-10
**Codebase Version**: 0.1.0-dev (Phase 1: ~80% Complete)
**Next Milestone**: Implement AddPersonDialog, AddPersonCommand, and PersonRepository (Phase 2 start)
