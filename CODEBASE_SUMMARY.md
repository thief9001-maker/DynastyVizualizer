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

- **Total Python Files**: 37 (9 implemented, 28 scaffolded)
- **Lines of Code**: ~532 (excluding comments and blank lines)
- **Total Lines**: 718 (including docstrings and comments)
- **Implementation Status**: ~5% complete (foundation infrastructure)
- **Estimated Final Size**: 8,000-12,000 lines of code

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

The architecture successfully scales to support complex features like draggable UI, multiple views, and relationship tracing:

```
┌─────────────────────────────────────────────────┐
│         MainWindow (main.py)                    │
│         - Qt GUI setup and view management      │
│         - Menu bar and toolbar                  │
│         - View switching (Tree/Timeline/Table)  │
└────────────┬────────────────────────────────────┘
             │
        ┌────┴─────────────────────┐
        │                          │
   ┌────▼──────┐          ┌───────▼────────┐
   │  Actions  │          │   Database     │
   │  Handlers │          │   Manager      │
   │           │          │                │
   │  • File   │          │  SQLite .dyn   │
   │  • Edit   │◄─────────┤  • Person      │
   │  • View   │ interact │  • Marriage    │
   │  • Tools  │          │  • Event       │
   │  • Help   │          │  • Portrait    │
   └─────┬─────┘          │  • Family      │
         │                │  • MajorEvent  │
         │ execute()      └────────────────┘
         ▼
   ┌────────────────┐
   │  UndoRedo      │          ┌─────────────────┐
   │  Manager       │          │  Views          │
   │                │          │                 │
   │  Commands:     │          │  • TreeView     │
   │  • Genealogy   │          │  • TimelineView │
   │  • GUI Ops     │          │  • TableView    │
   └────────────────┘          │  • StatsView    │
                               └─────────────────┘
```

**Why This Pattern Works:**
- **MVC**: Separates data (models), presentation (views), and logic (controllers/actions)
- **Command Pattern**: Every operation is undoable/redoable, including UI changes like dragging nodes
- **Observer Pattern**: Qt signals/slots automatically update UI when data changes
- **Scalability**: New views are just new widgets; new operations are just new commands

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

```
DynastyVizualizer/
├── main.py                          # Application entry point (222 lines)
├── database/
│   ├── __init__.py
│   └── db_manager.py               # SQLite CRUD operations (193 lines) ✅
├── models/                          # Data models [PHASE 2]
│   ├── __init__.py
│   ├── person.py                   # Person class with computed properties
│   ├── marriage.py                 # Marriage relationship class
│   ├── event.py                    # Event/life history class
│   ├── portrait.py                 # Portrait metadata class
│   ├── family.py                   # Family dynasty class
│   └── major_event.py              # Historical event class
├── actions/                         # Menu action handlers ✅
│   ├── __init__.py                 # (6 lines)
│   ├── file_actions.py             # New/Open/Save/Exit (159 lines)
│   ├── edit_actions.py             # Undo/Redo (29 lines)
│   ├── view_actions.py             # View switching (22 lines)
│   ├── tools_actions.py            # Validation tools (22 lines)
│   └── help_actions.py             # About dialog (10 lines)
├── commands/
│   ├── __init__.py
│   ├── undo_redo_manager.py        # Command pattern manager (55 lines) ✅
│   ├── base_command.py             # Base command class [PHASE 2]
│   ├── genealogy_commands/         # Person/marriage/event operations [PHASE 2-3]
│   │   ├── add_person.py
│   │   ├── edit_person.py
│   │   ├── delete_person.py
│   │   ├── create_marriage.py
│   │   ├── edit_marriage.py
│   │   ├── end_marriage.py
│   │   ├── delete_marriage.py
│   │   ├── create_child.py
│   │   ├── add_event.py
│   │   ├── edit_event.py
│   │   └── delete_event.py
│   └── gui_commands/               # View/scene commands [PHASE 5]
│       ├── move_person.py          # Drag-and-drop command
│       ├── rebuild_scene.py
│       ├── recompute_generations.py
│       ├── change_skin.py
│       └── change_view.py
├── views/                           # Visualization widgets [PHASE 3-4]
│   ├── __init__.py
│   ├── tree_view/                  # Family tree visualization
│   │   ├── tree_canvas.py          # Main scrollable canvas
│   │   ├── person_box.py           # Person widget
│   │   ├── marriage_node.py        # Marriage connection widget
│   │   ├── relationship_line.py    # Parent-child lines
│   │   ├── layout_engine.py        # Automatic positioning
│   │   └── generation_band.py      # Generation markers
│   ├── timeline_view/              # Timeline visualization
│   │   ├── timeline_canvas.py
│   │   ├── family_bar.py           # Family lifespan bar
│   │   ├── person_bar.py           # Individual lifespan bar
│   │   ├── event_marker.py         # Life event markers
│   │   └── major_event_marker.py   # Historical event overlay
│   ├── table_view/                 # Database table views
│   │   ├── person_table.py
│   │   ├── marriage_table.py
│   │   ├── event_table.py
│   │   └── family_table.py
│   └── stats_view/                 # Statistics dashboard [PHASE 7]
│       ├── family_dashboard.py
│       ├── comparison_widget.py
│       └── charts.py
├── widgets/                         # Reusable custom widgets [PHASE 2-3]
│   ├── __init__.py
│   ├── date_picker.py              # Flexible date input (year/month/day)
│   ├── person_selector.py          # Searchable person dropdown
│   ├── portrait_gallery.py         # Multi-portrait display
│   ├── extended_details_panel.py   # Person deep-dive panel
│   └── search_bar.py               # Real-time search with pruning
├── dialogs/                         # Modal dialogs [PHASE 2-3]
│   ├── __init__.py
│   ├── add_person_dialog.py
│   ├── edit_person_dialog.py
│   ├── create_marriage_dialog.py
│   ├── create_child_dialog.py
│   ├── add_event_dialog.py
│   ├── preferences_dialog.py
│   ├── import_csv_dialog.py
│   └── about_dialog.py
├── utils/                           # Utility modules [PHASE 4-7]
│   ├── __init__.py
│   ├── relationship_calculator.py  # Calculate relationships between people
│   ├── generation_calculator.py    # Compute generation levels
│   ├── validators.py               # Data validation tools
│   ├── csv_importer.py             # CSV import logic
│   ├── skin_manager.py             # UI skin/theme management
│   └── color_manager.py            # Family color coding logic
├── resources/                       # Assets and resources [PHASE 6]
│   ├── skins/                      # UI skins (default, parchment, etc.)
│   ├── icons/                      # Application icons
│   └── default_portraits/          # Blank portrait placeholder
├── scripts/                         # Development utilities
│   └── create_codebase_summary.py  # Code sharing script ✅
├── CODEBASE_SUMMARY.md             # This file ✅
├── README.md                       # User documentation ✅
├── requirements.txt                # Dependencies ✅
└── LICENSE                         # MIT License ✅
```

---

## Development Roadmap

### ✅ **Phase 1: Foundation** (CURRENT - Week 1-2)
**Status**: 100% Complete
**Lines**: ~720

Core infrastructure for database management and undo/redo.

**Completed:**
- [x] Main application window and menu structure
- [x] SQLite database management (`.dyn` format)
- [x] File operations (New, Open, Save, Save As, Exit)
- [x] Undo/redo infrastructure (Command pattern)
- [x] Action handler framework
- [x] Project scaffolding

**Key Files**: `main.py`, `database/db_manager.py`, `actions/`, `commands/undo_redo_manager.py`

---

### 🚧 **Phase 2: Data Models & Basic CRUD** (Week 3-5)
**Status**: Not Started
**Estimated Lines**: +1,200

Build data models and basic create/read/update/delete operations.

**Goals:**
- [ ] Implement `Person`, `Marriage`, `Event` model classes
- [ ] Create `AddPersonCommand`, `EditPersonCommand`, `DeletePersonCommand`
- [ ] Create `AddPersonDialog`, `EditPersonDialog`
- [ ] Build `CreateMarriageCommand`, `CreateChildCommand`
- [ ] Build `CreateMarriageDialog`
- [ ] Implement flexible date handling (year/month/day with nulls)
- [ ] Add portrait support (`Portrait` model + database table)
- [ ] Create `DatePicker` widget (supports partial dates)
- [ ] Create `PersonSelector` widget (searchable dropdown)

**Deliverable**: Can add, edit, and delete people and marriages through dialogs

**Key Files**: `models/`, `commands/genealogy_commands/`, `dialogs/`, `widgets/date_picker.py`

---

### 🚧 **Phase 3: Tree Visualization** (Week 6-10)
**Status**: Not Started
**Estimated Lines**: +2,500

Build the interactive family tree view with draggable person boxes.

**Goals:**
- [ ] Create `PersonBox` custom widget (portrait + name + dates + gear icon)
- [ ] Create `MarriageNode` widget (connection point + dates)
- [ ] Create `RelationshipLine` widget (parent-child connectors)
- [ ] Implement `TreeLayoutEngine` (automatic generational positioning)
- [ ] Build `TreeCanvas` (scrollable, zoomable QGraphicsView)
- [ ] Implement generation bands with labels
- [ ] Add drag-and-drop for creating marriages
- [ ] Add drag-and-drop for repositioning person boxes
- [ ] Implement `MovePersonCommand` (undoable position changes)
- [ ] Add in-place editing (click name to edit)
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
**Status**: Not Started
**Estimated Lines**: +800

Final polish, preferences, keyboard shortcuts, and quality-of-life features.

**Goals:**
- [ ] Build `PreferencesDialog` with tabs:
  - General (date format, auto-save interval, confirmations)
  - Display (skin, font size, color scheme)
  - Behavior (surname change rules, portrait auto-cycle)
  - Advanced (validation strictness, close relative marriages)
- [ ] Implement keyboard shortcuts:
  - Ctrl+N/O/S (File operations)
  - Ctrl+Z/Y (Undo/Redo)
  - Ctrl+F (Search), Ctrl+P (Add Person), Del (Delete)
  - Ctrl+1/2/3/4 (Switch views)
  - Ctrl+Plus/Minus/0 (Zoom)
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

**Last Updated**: 2025-12-08
**Codebase Version**: 0.1.0-dev (Phase 1 Complete)
**Next Milestone**: Phase 2 - Data Models & Basic CRUD
