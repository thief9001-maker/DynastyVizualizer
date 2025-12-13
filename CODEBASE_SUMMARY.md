# DynastyVizualizer - Complete Codebase Snapshot

**Generated**: 2025-12-13 15:14:34
**Files**: 10 implemented / 94 total
**Lines**: ~1,146 code / ~4,058 total
**Status**: Phase 1 Complete, Phase 2 In Progress

---

## Quick Reference

# DynastyVizualizer - Codebase Reference

**Quick Reference**: Family tree/genealogy app for gaming. PySide6 + SQLite. MVC + Command pattern.

**Status**: Phase 1 ✅ Complete, Phase 2 🚧 35% (Add Person feature complete)

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

## File Structure

```
DynastyVizualizer/
├── actions/
│   ├── __init__.py 📋
│   ├── edit_actions.py 📋
│   ├── file_actions.py ✅
│   ├── help_actions.py 📋
│   ├── settings_actions.py 📋
│   ├── tools_actions.py 📋
│   └── view_actions.py 📋
├── commands/
│   ├── GUI_commands/
│   │   ├── __init__.py 📋
│   │   ├── change_skin.py 📋
│   │   ├── change_view.py 📋
│   │   ├── move_node.py 📋
│   │   ├── move_person.py 📋
│   │   ├── preference_changes.py 📋
│   │   ├── rebuild_scene.py 📋
│   │   ├── recompute_generation.py 📋
│   │   ├── recompute_generations.py 📋
│   │   └── timeline_scroll.py 📋
│   ├── ___init__.py 📋
│   ├── base_command.py 📋
│   ├── genealogy_commands/
│   │   ├── __init__.py ✅
│   │   ├── add_event.py 📋
│   │   ├── add_marriage.py 📋
│   │   ├── add_person.py 📋
│   │   ├── assign_parent.py 📋
│   │   ├── create_child.py 📋
│   │   ├── delete_event.py 📋
│   │   ├── delete_marriage.py 📋
│   │   ├── delete_person.py 📋
│   │   ├── edit_event.py 📋
│   │   ├── edit_marriage.py 📋
│   │   ├── edit_person.py 📋
│   │   ├── end_marriage.py 📋
│   │   └── unassign_parent.py 📋
│   ├── undo_redo_manager.py 📋
│   └── view_changes.py 📋
├── database/
│   ├── __init__.py 📋
│   ├── db_manager.py ✅
│   └── person_repository.py ✅
├── dialogs/
│   ├── __init__.py 📋
│   ├── about_dialog.py 📋
│   ├── add_event_dialog.py 📋
│   ├── add_person_dialog.py ✅
│   ├── create_child_dialog.py 📋
│   ├── create_marriage_dialog.py 📋
│   ├── edit_person_dialog.py 📋
│   ├── import_csv_dialog.py 📋
│   └── settings_dialog.py 📋
├── main.py ✅
├── models/
│   ├── __init__.py 📋
│   ├── event.py 📋
│   ├── family.py 📋
│   ├── major_event.py 📋
│   ├── marriage.py 📋
│   ├── person.py ✅
│   └── portrait.py 📋
├── scripts/
│   ├── create_codebase_summary.py ✅
│   └── migrate_database.py ✅
├── utils/
│   ├── __init__.py 📋
│   ├── color_manager.py 📋
│   ├── csv_importer.py 📋
│   ├── generation_calculator.py 📋
│   ├── relationship_calculator.py 📋
│   ├── settings_manager.py ✅
│   ├── skin_manager.py 📋
│   └── validators.py 📋
├── views/
│   ├── __init__.py 📋
│   ├── data_table.py 📋
│   ├── dynasty_view.py 📋
│   ├── stats_view/
│   │   ├── charts.py 📋
│   │   ├── comparison_widget.py 📋
│   │   └── family_dashboard.py 📋
│   ├── table_view/
│   │   ├── event_table.py 📋
│   │   ├── family_table.py 📋
│   │   ├── marriage_table.py 📋
│   │   └── person_table.py 📋
│   ├── timeline_view/
│   │   ├── event_marker.py 📋
│   │   ├── family_bar.py 📋
│   │   ├── major_event_marker.py 📋
│   │   ├── person_bar.py 📋
│   │   └── timeline_canvas.py 📋
│   ├── timeline_view.py 📋
│   └── tree_view/
│       ├── __init__.py 📋
│       ├── generation_band.py 📋
│       ├── layout_engine.py 📋
│       ├── marriage_node.py 📋
│       ├── person_box.py 📋
│       ├── relationship_line.py 📋
│       └── tree_canvas.py 📋
└── widgets/
    ├── __init__.py 📋
    ├── date_picker.py 📋
    ├── extended_details_panel.py 📋
    ├── person_selector.py 📋
    ├── portrait_gallery.py 📋
    └── search_bar.py 📋
```

Legend: ✅ Implemented (>20 code lines) | 📋 Scaffolded

---

## Implementation Status

**Implemented**: 10/94 files

**actions/**
- 📋 `__init__.py` (7 lines)
- 📋 `edit_actions.py` (10 lines)
- ✅ `file_actions.py` (52 lines)
- 📋 `help_actions.py` (3 lines)
- 📋 `settings_actions.py` (8 lines)
- 📋 `tools_actions.py` (6 lines)
- 📋 `view_actions.py` (6 lines)

**commands/**
- 📋 `___init__.py` (0 lines)
- 📋 `base_command.py` (2 lines)
- 📋 `undo_redo_manager.py` (18 lines)
- 📋 `view_changes.py` (0 lines)

**commands/GUI_commands/**
- 📋 `__init__.py` (0 lines)
- 📋 `change_skin.py` (3 lines)
- 📋 `change_view.py` (3 lines)
- 📋 `move_node.py` (0 lines)
- 📋 `move_person.py` (10 lines)
- 📋 `preference_changes.py` (0 lines)
- 📋 `rebuild_scene.py` (3 lines)
- 📋 `recompute_generation.py` (0 lines)
- 📋 `recompute_generations.py` (3 lines)
- 📋 `timeline_scroll.py` (0 lines)

**commands/genealogy_commands/**
- ✅ `__init__.py` (26 lines)
- 📋 `add_event.py` (3 lines)
- 📋 `add_marriage.py` (3 lines)
- 📋 `add_person.py` (8 lines)
- 📋 `assign_parent.py` (9 lines)
- 📋 `create_child.py` (11 lines)
- 📋 `delete_event.py` (3 lines)
- 📋 `delete_marriage.py` (3 lines)
- 📋 `delete_person.py` (3 lines)
- 📋 `edit_event.py` (3 lines)
- 📋 `edit_marriage.py` (3 lines)
- 📋 `edit_person.py` (3 lines)
- 📋 `end_marriage.py` (10 lines)
- 📋 `unassign_parent.py` (8 lines)

**database/**
- 📋 `__init__.py` (3 lines)
- ✅ `db_manager.py` (171 lines)
- ✅ `person_repository.py` (104 lines)

**dialogs/**
- 📋 `__init__.py` (0 lines)
- 📋 `about_dialog.py` (1 lines)
- 📋 `add_event_dialog.py` (1 lines)
- ✅ `add_person_dialog.py` (47 lines)
- 📋 `create_child_dialog.py` (1 lines)
- 📋 `create_marriage_dialog.py` (1 lines)
- 📋 `edit_person_dialog.py` (1 lines)
- 📋 `import_csv_dialog.py` (1 lines)
- 📋 `settings_dialog.py` (1 lines)

**models/**
- 📋 `__init__.py` (0 lines)
- 📋 `event.py` (15 lines)
- 📋 `family.py` (12 lines)
- 📋 `major_event.py` (15 lines)
- 📋 `marriage.py` (15 lines)
- ✅ `person.py` (50 lines)
- 📋 `portrait.py` (14 lines)

**root/**
- ✅ `main.py` (159 lines)

**scripts/**
- ✅ `create_codebase_summary.py` (102 lines)
- ✅ `migrate_database.py` (57 lines)

**utils/**
- 📋 `__init__.py` (0 lines)
- 📋 `color_manager.py` (5 lines)
- 📋 `csv_importer.py` (4 lines)
- 📋 `generation_calculator.py` (2 lines)
- 📋 `relationship_calculator.py` (3 lines)
- ✅ `settings_manager.py` (81 lines)
- 📋 `skin_manager.py` (4 lines)
- 📋 `validators.py` (5 lines)

**views/**
- 📋 `__init__.py` (0 lines)
- 📋 `data_table.py` (0 lines)
- 📋 `dynasty_view.py` (0 lines)
- 📋 `timeline_view.py` (0 lines)

**views/stats_view/**
- 📋 `charts.py` (2 lines)
- 📋 `comparison_widget.py` (2 lines)
- 📋 `family_dashboard.py` (2 lines)

**views/table_view/**
- 📋 `event_table.py` (2 lines)
- 📋 `family_table.py` (2 lines)
- 📋 `marriage_table.py` (2 lines)
- 📋 `person_table.py` (2 lines)

**views/timeline_view/**
- 📋 `event_marker.py` (1 lines)
- 📋 `family_bar.py` (1 lines)
- 📋 `major_event_marker.py` (1 lines)
- 📋 `person_bar.py` (1 lines)
- 📋 `timeline_canvas.py` (2 lines)

**views/tree_view/**
- 📋 `__init__.py` (0 lines)
- 📋 `generation_band.py` (2 lines)
- 📋 `layout_engine.py` (2 lines)
- 📋 `marriage_node.py` (1 lines)
- 📋 `person_box.py` (1 lines)
- 📋 `relationship_line.py` (7 lines)
- 📋 `tree_canvas.py` (1 lines)

**widgets/**
- 📋 `__init__.py` (0 lines)
- 📋 `date_picker.py` (1 lines)
- 📋 `extended_details_panel.py` (2 lines)
- 📋 `person_selector.py` (1 lines)
- 📋 `portrait_gallery.py` (1 lines)
- 📋 `search_bar.py` (2 lines)

---

## Complete Source Code

### Database

#### database/__init__.py (4 lines)

```python
from .db_manager import DatabaseManager
from .person_repository import PersonRepository

__all__ = ['DatabaseManager', 'PersonRepository']
```

#### database/db_manager.py (295 lines)

```python
import sqlite3
import shutil
import os


class DatabaseManager:
    """Manages SQLite-based .dyn dynasty database files."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the database manager."""
        self.parent = parent
        self.conn: sqlite3.Connection | None = None
        self.file_path: str | None = None
        self._unsaved_changes: bool = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_dirty(self) -> bool:
        """Check if there are unsaved changes."""
        return self._unsaved_changes

    @property
    def is_open(self) -> bool:
        """Check if a database is currently open."""
        return self.conn is not None

    @property
    def database_name(self) -> str | None:
        """Get the filename of the current database without path."""
        if self.file_path is None:
            return None
        return os.path.basename(self.file_path)

    @property
    def database_directory(self) -> str | None:
        """Get the directory path of the current database."""
        if self.file_path is None:
            return None
        return os.path.dirname(self.file_path)

    @property
    def has_file_path(self) -> bool:
        """Check if database has an associated file path."""
        return self.file_path is not None

    # ------------------------------------------------------------------
    # Public Methods - Database Lifecycle
    # ------------------------------------------------------------------

    def new_database(self, file_path: str) -> None:
        """Create a brand-new .dyn file with the dynasty schema."""
        if os.path.exists(file_path):
            os.remove(file_path)
        
        try:
            self.conn = sqlite3.connect(file_path)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.file_path = file_path
            self._initialize_schema()
            self._unsaved_changes = False
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create database: {e}")

    def open_database(self, file_path: str) -> None:
        """Open an existing .dyn database file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        try:
            self.conn = sqlite3.connect(file_path)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.file_path = file_path
            self._migrate_schema()
            self._unsaved_changes = False
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to open database: {e}")

    def save_database(self, path: str | None = None) -> bool:
        """
        Save the database, optionally to a new path.
        
        If path is provided, saves a copy to that location and switches to it.
        If path is None, commits changes to the current file.
        """
        if self.conn is None:
            return False
        
        # If no path provided, just commit current database
        if path is None:
            self.conn.commit()
            self._unsaved_changes = False
            return True
        
        # Save to new path (save_as behavior)
        if self.file_path is None:
            return False
        
        self.conn.commit()
        self.conn.close()
        
        # Copy database file to new location
        shutil.copy2(self.file_path, path)
        
        # Reopen connection at new path
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.file_path = path
        self._unsaved_changes = False
        return True
    
    def close(self) -> None:
        """Close the current database connection and reset state."""
        if self.conn:
            self.conn.close()
        self.conn = None
        self.file_path = None
        self._unsaved_changes = False

    # ------------------------------------------------------------------
    # Public Methods - State Management
    # ------------------------------------------------------------------

    def mark_dirty(self) -> None:
        """Mark the database as having unsaved changes."""
        if self.conn is not None:
            self._unsaved_changes = True

    def mark_clean(self) -> None:
        """Mark the database as having no unsaved changes."""
        self._unsaved_changes = False

    # ------------------------------------------------------------------
    # Private Methods
    # ------------------------------------------------------------------

    def _initialize_schema(self) -> None:
        """Create all required tables for a new dynasty database."""
        if self.conn is None:
            raise RuntimeError("Database connection is not established.")
        
        cursor = self.conn.cursor()

        schema_sql = """
        -- Person table: Core genealogical data
        -- Dates support flexible precision (year, year/month, or year/month/day)
        CREATE TABLE IF NOT EXISTS Person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            middle_name TEXT DEFAULT '',
            last_name TEXT NOT NULL,
            maiden_name TEXT,
            nickname TEXT DEFAULT '',
            gender TEXT,
            birth_year INTEGER,
            birth_month INTEGER,
            birth_day INTEGER,
            death_year INTEGER,
            death_month INTEGER,
            death_day INTEGER,
            arrival_year INTEGER,
            arrival_month INTEGER,
            arrival_day INTEGER,
            moved_out_year INTEGER,
            moved_out_month INTEGER,
            moved_out_day INTEGER,
            father_id INTEGER,
            mother_id INTEGER,
            family_id INTEGER,
            dynasty_id INTEGER DEFAULT 1,
            is_founder INTEGER DEFAULT 0,
            education INTEGER DEFAULT 0,
            notes TEXT,
            FOREIGN KEY(father_id) REFERENCES Person(id) ON DELETE SET NULL,
            FOREIGN KEY(mother_id) REFERENCES Person(id) ON DELETE SET NULL,
            FOREIGN KEY(family_id) REFERENCES Family(id) ON DELETE SET NULL
        );

        -- Event table: Life events (jobs, illnesses, moves, etc.)
        CREATE TABLE IF NOT EXISTS Event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            event_title TEXT NOT NULL,
            start_year INTEGER,
            start_month INTEGER,
            start_day INTEGER,
            end_year INTEGER,
            end_month INTEGER,
            end_day INTEGER,
            notes TEXT,
            FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
        );

        -- Marriage table: Relationships between people
        CREATE TABLE IF NOT EXISTS Marriage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spouse1_id INTEGER,
            spouse2_id INTEGER,
            marriage_year INTEGER,
            marriage_month INTEGER,
            marriage_day INTEGER,
            dissolution_year INTEGER,
            dissolution_month INTEGER,
            dissolution_day INTEGER,
            dissolution_reason TEXT,
            marriage_type TEXT DEFAULT 'spouse',
            FOREIGN KEY(spouse1_id) REFERENCES Person(id)
                ON UPDATE CASCADE ON DELETE SET NULL,
            FOREIGN KEY(spouse2_id) REFERENCES Person(id)
                ON UPDATE CASCADE ON DELETE SET NULL
        );

        -- Portrait table: Multiple images per person with date ranges
        CREATE TABLE IF NOT EXISTS Portrait (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
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

        -- Family table: Dynasty/family groupings
        CREATE TABLE IF NOT EXISTS Family (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT NOT NULL,
            move_in_year INTEGER,
            move_in_month INTEGER,
            move_in_day INTEGER,
            coat_of_arms_path TEXT,
            family_color TEXT,
            is_extinct INTEGER DEFAULT 0,
            notes TEXT
        );

        -- MajorEvent table: Historical events affecting multiple families
        CREATE TABLE IF NOT EXISTS MajorEvent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            start_year INTEGER NOT NULL,
            start_month INTEGER,
            start_day INTEGER,
            end_year INTEGER,
            end_month INTEGER,
            end_day INTEGER,
            description TEXT,
            color TEXT
        );

        -- PersonPosition table: Custom positions for draggable UI
        CREATE TABLE IF NOT EXISTS PersonPosition (
            person_id INTEGER PRIMARY KEY,
            view_type TEXT NOT NULL,
            x_position REAL NOT NULL,
            y_position REAL NOT NULL,
            FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
        );
        """
        cursor.executescript(schema_sql)
        self.conn.commit()
    
    def _migrate_schema(self) -> None:
        """Migrate existing database schema to latest version."""
        if self.conn is None:
            raise RuntimeError("Database connection is not established.")
            
        cursor = self.conn.cursor()

        cursor.execute("PRAGMA table_info(Person)")
        existing_columns = {row[1] for row in cursor.fetchall()}

        migrations = [
            # Dec/10/2025 - Person Model updates
            ("middle_name", "ALTER TABLE Person ADD COLUMN middle_name TEXT DEFAULT ''"),
            ("nickname", "ALTER TABLE Person ADD COLUMN nickname TEXT DEFAULT ''"),
            ("dynasty_id", "ALTER TABLE Person ADD COLUMN dynasty_id INTEGER DEFAULT 1"),
            ("is_founder", "ALTER TABLE Person ADD COLUMN is_founder INTEGER DEFAULT 0"),
            ("education", "ALTER TABLE Person ADD COLUMN education INTEGER DEFAULT 0"),
            ]
        for column_name, sql in migrations:
            if column_name not in existing_columns:
                cursor.execute(sql)


```

#### database/person_repository.py (272 lines)

```python
"""Database repository for Person entity operations."""

from __future__ import annotations
import sqlite3
from typing import TYPE_CHECKING

from models.person import Person

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager


class PersonRepository:
    """Handles all database operations for Person objects."""
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize repository with database manager."""
        self.db = db_manager
    
    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------
    
    def _row_to_person(self, row: sqlite3.Row) -> Person:
        """Convert database row to Person object using named column access."""
        return Person(
            id=row['id'],
            first_name=row['first_name'],
            middle_name=row['middle_name'],
            last_name=row['last_name'],
            maiden_name=row['maiden_name'],
            nickname=row['nickname'],
            gender=row['gender'],
            birth_year=row['birth_year'],
            birth_month=row['birth_month'],
            birth_day=row['birth_day'],
            death_year=row['death_year'],
            death_month=row['death_month'],
            death_day=row['death_day'],
            arrival_year=row['arrival_year'],
            arrival_month=row['arrival_month'],
            arrival_day=row['arrival_day'],
            moved_out_year=row['moved_out_year'],
            moved_out_month=row['moved_out_month'],
            moved_out_day=row['moved_out_day'],
            father_id=row['father_id'],
            mother_id=row['mother_id'],
            family_id=row['family_id'],
            dynasty_id=row['dynasty_id'] or 1,
            is_founder=bool(row['is_founder']),
            education=row['education'] or 0,
            notes=row['notes'] or ""
        )
    
    def _cursor(self):
        if self.db.conn is None:
            raise RuntimeError("DB connection not established.")
        return self.db.conn.cursor()
    
    # ------------------------------------------------------------------
    # Create Operations
    # ------------------------------------------------------------------
    
    def insert(self, person: Person) -> int:
        """Insert new person into database and return assigned ID."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        
        sql = """
            INSERT INTO Person (
                first_name, middle_name, last_name, maiden_name, nickname,
                gender, birth_year, birth_month, birth_day,
                death_year, death_month, death_day,
                arrival_year, arrival_month, arrival_day,
                moved_out_year, moved_out_month, moved_out_day,
                father_id, mother_id, family_id,
                dynasty_id, is_founder, education, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            person.first_name, person.middle_name, person.last_name,
            person.maiden_name, person.nickname,
            person.gender, person.birth_year, person.birth_month, person.birth_day,
            person.death_year, person.death_month, person.death_day,
            person.arrival_year, person.arrival_month, person.arrival_day,
            person.moved_out_year, person.moved_out_month, person.moved_out_day,
            person.father_id, person.mother_id, person.family_id,
            person.dynasty_id, 1 if person.is_founder else 0, person.education,
            person.notes
        )
        
        cursor.execute(sql, values)
        person_id = cursor.lastrowid
        
        self.db.mark_dirty()
        return person_id if person_id is not None else -1
       
    def insert_with_id(self, person: Person) -> None:
        """Insert person with specific ID (for redo operations)"""
        if self.db.conn is None:
            raise RuntimeError("Database connection not establish.")
        
        if person.id is None:
            raise ValueError("Person must have an ID for insert_with_id")
        
        cursor = self.db.conn.cursor()

        sql = """
            INSERT INTO Person (
                id, first_name, middle_name, last_name, maiden_name, nickname,
                gender, birth_year, birth_month, birth_day,
                death_year, death_month, death_day,
                arrival_year, arrival_month, arrival_day,
                moved_out_year, moved_out_month, moved_out_day,
                father_id, mother_id, family_id,
                dynasty_id, is_founder, education, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            person.id,  # Explicitly set the ID
            person.first_name, person.middle_name, person.last_name,
            person.maiden_name, person.nickname,
            person.gender, person.birth_year, person.birth_month, person.birth_day,
            person.death_year, person.death_month, person.death_day,
            person.arrival_year, person.arrival_month, person.arrival_day,
            person.moved_out_year, person.moved_out_month, person.moved_out_day,
            person.father_id, person.mother_id, person.family_id,
            person.dynasty_id, 1 if person.is_founder else 0, person.education,
            person.notes
        )
        
        cursor.execute(sql, values)
        self.db.mark_dirty()
        

    # ------------------------------------------------------------------
    # Read Operations
    # ------------------------------------------------------------------
    
    def get_by_id(self, person_id: int) -> Person | None:
        """Retrieve person by ID, return None if not found."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM Person WHERE id = ?", (person_id,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_person(row)
    
    def get_all(self) -> list[Person]:
        """Retrieve all people from database."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM Person ORDER BY last_name, first_name")
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    def get_by_name(self, first_name: str, last_name: str) -> list[Person]:
        """Find people by first and last name."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        sql = """
            SELECT * FROM Person 
            WHERE first_name = ? AND last_name = ?
            ORDER BY birth_year
        """
        cursor.execute(sql, (first_name, last_name))
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    def get_children(self, parent_id: int) -> list[Person]:
        """Retrieve all children of a given parent."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")

        cursor = self.db.conn.cursor()
        sql = """
            SELECT * FROM Person 
            WHERE father_id = ? OR mother_id = ?
            ORDER BY birth_year, birth_month, birth_day
        """
        cursor.execute(sql, (parent_id, parent_id))
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    def get_alive_in_year(self, year: int) -> list[Person]:
        """Retrieve all people alive in a given year."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")

        cursor = self.db.conn.cursor()
        sql = """
            SELECT * FROM Person
            WHERE birth_year <= ? 
            AND (death_year IS NULL OR death_year >= ?)
            ORDER BY birth_year
        """
        cursor.execute(sql, (year, year))
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    # ------------------------------------------------------------------
    # Update Operations
    # ------------------------------------------------------------------
    
    def update(self, person: Person) -> None:
        """Update existing person in database."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        if person.id is None:
            raise ValueError("Cannot update person without ID.")
        
        cursor = self.db.conn.cursor()
        
        sql = """
            UPDATE Person SET
                first_name = ?, middle_name = ?, last_name = ?,
                maiden_name = ?, nickname = ?,
                gender = ?, birth_year = ?, birth_month = ?, birth_day = ?,
                death_year = ?, death_month = ?, death_day = ?,
                arrival_year = ?, arrival_month = ?, arrival_day = ?,
                moved_out_year = ?, moved_out_month = ?, moved_out_day = ?,
                father_id = ?, mother_id = ?, family_id = ?,
                dynasty_id = ?, is_founder = ?, education = ?, notes = ?
            WHERE id = ?
        """
        
        values = (
            person.first_name, person.middle_name, person.last_name,
            person.maiden_name, person.nickname,
            person.gender, person.birth_year, person.birth_month, person.birth_day,
            person.death_year, person.death_month, person.death_day,
            person.arrival_year, person.arrival_month, person.arrival_day,
            person.moved_out_year, person.moved_out_month, person.moved_out_day,
            person.father_id, person.mother_id, person.family_id,
            person.dynasty_id, 1 if person.is_founder else 0, person.education,
            person.notes,
            person.id
        )
        
        cursor.execute(sql, values)
        self.db.mark_dirty()
    
    # ------------------------------------------------------------------
    # Delete Operations
    # ------------------------------------------------------------------
    
    def delete(self, person_id: int) -> None:
        """Delete person from database by ID."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM Person WHERE id = ?", (person_id,))
        self.db.mark_dirty()

```

### Models

#### models/__init__.py (0 lines)

```python

```

#### models/event.py (41 lines)

```python
"""Data model for Event entities."""


class Event:
    """Represents a life event for a person."""

    def __init__(
        self,
        event_id: int,
        person_id: int,
        event_type: str,
        event_title: str,
        start_year: int | None = None,
        start_month: int | None = None,
        start_day: int | None = None,
        end_year: int | None = None,
        end_month: int | None = None,
        end_day: int | None = None,
        notes: str | None = None,
    ) -> None:
        """Initialize an event."""
        self.id = event_id
        self.person_id = person_id
        self.event_type = event_type
        self.event_title = event_title
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.notes = notes

    @property
    def is_ongoing(self) -> bool:
        """Check if the event is ongoing."""
        return self.end_year is None

    # TODO: Add duration property
    # TODO: Add start_date_string property
    # TODO: Add end_date_string property

```

#### models/family.py (34 lines)

```python
"""Data model for Family dynasties."""


class Family:
    """Represents a family dynasty grouping."""

    def __init__(
        self,
        family_id: int,
        surname: str,
        move_in_year: int | None = None,
        move_in_month: int | None = None,
        move_in_day: int | None = None,
        coat_of_arms_path: str | None = None,
        family_color: str | None = None,
        is_extinct: bool = False,
        notes: str | None = None,
    ) -> None:
        """Initialize a family dynasty."""
        self.id = family_id
        self.surname = surname
        self.move_in_year = move_in_year
        self.move_in_month = move_in_month
        self.move_in_day = move_in_day
        self.coat_of_arms_path = coat_of_arms_path
        self.family_color = family_color
        self.is_extinct = is_extinct
        self.notes = notes

    # TODO: Add move_in_date_string property
    # TODO: Add member_count property (requires database query)
    # TODO: Add founding_date property
    # TODO: Add end_date property
    # TODO: Add longest_lived_member property

```

#### models/major_event.py (41 lines)

```python
"""Data model for MajorEvent entities."""


class MajorEvent:
    """Represents a major historical event affecting multiple families."""

    def __init__(
        self,
        event_id: int,
        event_name: str,
        event_type: str,
        start_year: int,
        start_month: int | None = None,
        start_day: int | None = None,
        end_year: int | None = None,
        end_month: int | None = None,
        end_day: int | None = None,
        description: str | None = None,
        color: str | None = None,
    ) -> None:
        """Initialize a major historical event."""
        self.id = event_id
        self.event_name = event_name
        self.event_type = event_type
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.description = description
        self.color = color

    @property
    def is_ongoing(self) -> bool:
        """Check if the event is ongoing."""
        return self.end_year is None

    # TODO: Add duration property
    # TODO: Add start_date_string property
    # TODO: Add end_date_string property

```

#### models/marriage.py (41 lines)

```python
"""Data model for Marriage relationships."""


class Marriage:
    """Represents a marriage relationship between two people."""

    def __init__(
        self,
        marriage_id: int,
        spouse1_id: int,
        spouse2_id: int,
        marriage_year: int | None = None,
        marriage_month: int | None = None,
        marriage_day: int | None = None,
        dissolution_year: int | None = None,
        dissolution_month: int | None = None,
        dissolution_day: int | None = None,
        dissolution_reason: str | None = None,
        marriage_type: str = "spouse",
    ) -> None:
        """Initialize a marriage relationship."""
        self.id = marriage_id
        self.spouse1_id = spouse1_id
        self.spouse2_id = spouse2_id
        self.marriage_year = marriage_year
        self.marriage_month = marriage_month
        self.marriage_day = marriage_day
        self.dissolution_year = dissolution_year
        self.dissolution_month = dissolution_month
        self.dissolution_day = dissolution_day
        self.dissolution_reason = dissolution_reason
        self.marriage_type = marriage_type

    @property
    def is_active(self) -> bool:
        """Check if the marriage is currently active."""
        return self.dissolution_year is None

    # TODO: Add duration property
    # TODO: Add marriage_date_string property
    # TODO: Add dissolution_date_string property

```

#### models/person.py (151 lines)

```python
"""Data model for Person entities."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Person:
    """Represents a person in a dynasty with flexible date precision."""
    
    # Database identity
    id: int | None = None  # None until saved to database
    dynasty_id: int = 1
    family_id: int | None = None
    
    # Name fields (full structure for flexibility)
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    maiden_name: str = ""
    nickname: str = ""
    
    # Biological information
    gender: str = "Unknown"  # "Male", "Female", "Unknown", "Other"
    
    # Birth date (year should be provided, month/day optional)
    birth_year: int | None = None
    birth_month: int | None = None
    birth_day: int | None = None
    
    # Death date (all optional - None if alive)
    death_year: int | None = None
    death_month: int | None = None
    death_day: int | None = None
    
    # Arrival/departure dates (tracking when joined/left settlement)
    arrival_year: int | None = None
    arrival_month: int | None = None
    arrival_day: int | None = None
    moved_out_year: int | None = None
    moved_out_month: int | None = None
    moved_out_day: int | None = None
    
    # Relationships (parent IDs link to database)
    father_id: int | None = None
    mother_id: int | None = None
    
    # Game-specific fields
    is_founder: bool = False
    education: int = 0  # 0-5 scale from Ostriv
    
    # User notes
    notes: str = ""
    
    # ------------------------------------------------------------------
    # Computed Properties
    # ------------------------------------------------------------------
    
    @property
    def full_name(self) -> str:
        """Get full name with optional middle name and nickname."""
        parts = [self.first_name]
        
        if self.middle_name:
            parts.append(self.middle_name)
        
        parts.append(self.last_name)

        name = " ".join(parts)
        
        if self.nickname:
            name += f' "{self.nickname}"'

        return name
    
    @property
    def display_name(self) -> str:
        """Get display name (first + last, no middle or nickname)."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_deceased(self) -> bool:
        """Check if person is deceased."""
        return self.death_year is not None
    
    def get_age(self, current_year: int) -> int | None:
        """
        Calculate age at a given year.
        
        Returns None if birth year unknown or if person died before current year.
        """
        if self.birth_year is None:
            return None
        
        # If person died, use death year as upper bound
        if self.death_year is not None and current_year > self.death_year:
            return None
        
        return current_year - self.birth_year
    
    def is_alive_in_year(self, year: int) -> bool:
        """Check if person was alive in a given year."""
        # Must have been born by that year
        if self.birth_year is None or year < self.birth_year:
            return False
        
        # If no death year, assume still alive
        if self.death_year is None:
            return True
        
        # Check if year is before death
        return year <= self.death_year
    
    def get_age_at_death(self) -> int | None:
        """Calculate age at death, or None if not deceased or birth year unknown."""
        if not self.is_deceased or self.birth_year is None or self.death_year is None:
            return None
        
        return self.death_year - self.birth_year
    
    def get_birth_date_string(self) -> str:
        """Format birth date as string with available precision (European format)."""
        if self.birth_year is None:
            return "Unknown"
        
        if self.birth_day and self.birth_month:
            return f"{self.birth_day:02d}/{self.birth_month:02d}/{self.birth_year}"
        
        if self.birth_month:
            return f"{self.birth_month:02d}/{self.birth_year}"
        
        return str(self.birth_year)
    
    def get_death_date_string(self) -> str:
        """Format death date as string with available precision (European format)."""
        if self.death_year is None:
            return "Alive"
        
        if self.death_day and self.death_month:
            return f"{self.death_day:02d}/{self.death_month:02d}/{self.death_year}"
        
        if self.death_month:
            return f"{self.death_month:02d}/{self.death_year}"
        
        return str(self.death_year)
    
    def get_lifespan_string(self) -> str:
        """Get lifespan as formatted string (e.g., '1420-1475' or '1450-')."""
        birth = str(self.birth_year) if self.birth_year else "?"
        death = str(self.death_year) if self.death_year else ""
        return f"{birth}-{death}"
```

#### models/portrait.py (36 lines)

```python
"""Data model for Portrait entities."""


class Portrait:
    """Represents a portrait image for a person."""

    def __init__(
        self,
        portrait_id: int,
        person_id: int,
        image_path: str,
        valid_from_year: int | None = None,
        valid_from_month: int | None = None,
        valid_from_day: int | None = None,
        valid_to_year: int | None = None,
        valid_to_month: int | None = None,
        valid_to_day: int | None = None,
        is_primary: bool = False,
        display_order: int = 0,
    ) -> None:
        """Initialize a portrait."""
        self.id = portrait_id
        self.person_id = person_id
        self.image_path = image_path
        self.valid_from_year = valid_from_year
        self.valid_from_month = valid_from_month
        self.valid_from_day = valid_from_day
        self.valid_to_year = valid_to_year
        self.valid_to_month = valid_to_month
        self.valid_to_day = valid_to_day
        self.is_primary = is_primary
        self.display_order = display_order

    # TODO: Add valid_from_date_string property
    # TODO: Add valid_to_date_string property
    # TODO: Add is_valid_for_date method

```

### Actions

#### actions/__init__.py (8 lines)

```python
from .file_actions import FileActions
from .edit_actions import EditActions
from .view_actions import ViewActions
from .tools_actions import ToolsActions
from .help_actions import HelpActions
from .settings_actions import SettingsActions

__all__ = ['FileActions', 'EditActions', 'ViewActions', 'ToolsActions', 'HelpActions', 'SettingsActions']
```

#### actions/edit_actions.py (44 lines)

```python
from PySide6.QtWidgets import QDialog

class EditActions:
    """Handles edit menu actions (Undo, Redo, Add/Remove operations)."""
    
    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize edit actions handler."""
        self.parent = parent
    
    def undo(self) -> None:
        """Undo the last action."""
        if self.parent.undo_manager.undo():
            self.parent.db.mark_dirty()
            self.parent.refresh_ui()
    
    def redo(self) -> None:
        """Redo the last undone action."""
        if self.parent.undo_manager.redo():
            self.parent.db.mark_dirty()
            self.parent.refresh_ui()
    
    def add_person(self) -> None:
        """Open dialog to add a new person to the database."""
        from dialogs.add_person_dialog import AddPersonDialog
        from commands.genealogy_commands import AddPersonCommand

        dialog = AddPersonDialog(self.parent)
        result = dialog.exec()

        if result == 1:  # QDialog.accepted
            person = dialog.get_person()

            if person:
                command = AddPersonCommand(self.parent.db, person)
                self.parent.undo_manager.execute(command)
                self.parent.refresh_ui()
    
    def remove_person(self) -> None:
        """Remove the selected person from the database."""
        pass  # TODO: Implement with confirmation dialog
    
    def add_new_family(self) -> None:
        """Create a new family branch in the dynasty."""
        pass  # TODO: Implement family creation
```

#### actions/file_actions.py (159 lines)

```python
from PySide6.QtWidgets import QFileDialog, QMessageBox


class FileActions:
    """Handles file menu actions (New, Open, Save, Exit)."""
    
    FILE_FILTER = "Dynasty Files (*.dyn)"
    
    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize file actions handler."""
        self.parent = parent
    
    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------
    
    def _ensure_db(self) -> bool:
        """Check if a database is currently open."""
        if not hasattr(self.parent, 'db') or not self.parent.db.is_open:
            self._show_error("Error", "No database is currently open.")
            return False
        return True
    
    def _get_save_path(self, title: str, default_name: str = "") -> str | None:
        """Show a save file dialog and return the chosen path."""
        default_path = ""
        if default_name:
            default_path = default_name
        elif self.parent.db.database_directory:
            default_path = self.parent.db.database_directory
        
        path, _ = QFileDialog.getSaveFileName(
            self.parent,
            title,
            default_path,
            self.FILE_FILTER
        )
        return path if path else None
    
    def _get_open_path(self, title: str) -> str | None:
        """Show an open file dialog and return the chosen path."""
        default_dir = ""
        if self.parent.db.is_open and self.parent.db.database_directory:
            default_dir = self.parent.db.database_directory
        
        path, _ = QFileDialog.getOpenFileName(
            self.parent,
            title,
            default_dir,
            self.FILE_FILTER
        )
        return path if path else None
    
    def _show_error(self, title: str, message: str) -> None:
        """Display an error message dialog."""
        QMessageBox.critical(self.parent, title, message)
    
    # ------------------------------------------------------------------
    # File Operations
    # ------------------------------------------------------------------
    
    def new_dynasty(self) -> None:
        """Prompt user to create a new dynasty database file."""
        path = self._get_save_path("Create New Dynasty File")
        if not path:
            return
        
        try:
            self.parent.db.new_database(path)
            self.parent.refresh_ui()
        except Exception as e:
            self._show_error(
                "Error Creating Database",
                f"Failed to create dynasty file:\n{str(e)}"
            )
    
    def open_dynasty(self) -> None:
        """Prompt user to open an existing dynasty database file."""
        path = self._get_open_path("Open Dynasty File")
        if not path:
            return
        
        try:
            self.parent.db.open_database(path)
            self.parent.refresh_ui()
        except FileNotFoundError:
            self._show_error(
                "File Not Found",
                f"The file '{path}' does not exist."
            )
        except Exception as e:
            self._show_error(
                "Error Opening Database",
                f"Failed to open dynasty file:\n{str(e)}"
            )
    
    def save(self) -> bool:
        """Save current database, falling back to save_as if no path set."""
        if not self._ensure_db():
            return False
        
        if not self.parent.db.has_file_path:
            return self.save_as()
        
        try:
            result = self.parent.db.save_database()
            if result:
                self.parent.refresh_ui()
            return result
        except Exception as e:
            self._show_error(
                "Error Saving Database",
                f"Failed to save dynasty file:\n{str(e)}"
            )
            return False
    
    def save_as(self) -> bool:
        """Prompt user to save database to a new file."""
        if not self._ensure_db():
            return False
        
        # Suggest current filename if it exists
        default_name = self.parent.db.database_name or ""
        path = self._get_save_path("Save Dynasty File As", default_name)
        if not path:
            return False
        
        try:
            self.parent.db.save_database(path)
            return True
        except Exception as e:
            self._show_error(
                "Error Saving Database",
                f"Failed to save dynasty file:\n{str(e)}"
            )
            return False
    
    def exit_app(self) -> None:
        """Prompt to save unsaved changes before closing application."""
        db = self.parent.db
        
        if db.is_open and db.is_dirty:
            msg = QMessageBox(self.parent)
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("You have unsaved changes. Do you want to save before exiting?")
            msg.setStandardButtons(
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            choice = msg.exec()
            
            if choice == QMessageBox.StandardButton.Save:
                if not self.save():
                    return
            elif choice == QMessageBox.StandardButton.Cancel:
                return
        
        self.parent.close()

```

#### actions/help_actions.py (10 lines)

```python
class HelpActions:
    """Handles help menu actions for application information."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize help actions handler."""
        self.parent = parent

    def about(self) -> None:
        """Display the about dialog with application information."""
        pass  # TODO: Implement about dialog

```

#### actions/settings_actions.py (30 lines)

```python
class SettingsActions:
    """Handles settings menu actions for various configuration options."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize settings actions handler."""
        self.parent = parent

    def settings(self) -> None:
        """Open settings dialog to modify application settings."""
        pass  # TODO: Implement settings dialog interaction

    def general(self) -> None:
        """Open general settings tab."""
        pass  # TODO: Implement general settings tab

    def shortcuts(self) -> None:
        """Open shortcuts settings tab."""
        pass  # TODO: Implement shortcuts settings tab

    def display(self) -> None:
        """Open display settings tab."""
        pass  # TODO: Implement display settings tab

    def appearance(self) -> None:
        """Open appearance settings tab."""
        pass  # TODO: Implement appearance settings tab

    def formats(self) -> None:
        """Open formats settings tab."""
        pass  # TODO: Implement formats settings tab
```

#### actions/tools_actions.py (22 lines)

```python
class ToolsActions:
    """Handles tools menu actions for validation and scene utilities."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize tools actions handler."""
        self.parent = parent

    def rebuild_scene(self) -> None:
        """Rebuild the current visualization scene from scratch."""
        pass  # TODO: Implement scene rebuild

    def recompute_generations(self) -> None:
        """Recalculate generation levels for all persons."""
        pass  # TODO: Implement generation computation

    def validate_marriages(self) -> None:
        """Check for inconsistencies in marriage records."""
        pass  # TODO: Implement marriage validation

    def validate_parentage(self) -> None:
        """Check for inconsistencies in parent-child relationships."""
        pass  # TODO: Implement parentage validation

```

#### actions/view_actions.py (22 lines)

```python
class ViewActions:
    """Handles view menu actions for switching between visualizations."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize view actions handler."""
        self.parent = parent

    def family_trees(self) -> None:
        """Switch to family trees visualization view."""
        pass  # TODO: Implement family trees view

    def timeline(self) -> None:
        """Switch to timeline visualization view."""
        pass  # TODO: Implement timeline view

    def dynasty(self) -> None:
        """Switch to dynasty visualization view."""
        pass  # TODO: Implement dynasty view

    def data_table(self) -> None:
        """Switch to data table view."""
        pass  # TODO: Implement data table view

```

### Commands

#### commands/GUI_commands/__init__.py (0 lines)

```python

```

#### commands/GUI_commands/change_skin.py (27 lines)

```python
"""Command for changing the application color scheme."""

from commands.base_command import BaseCommand


class ChangeSkinCommand(BaseCommand):
    """Switch between different UI color schemes."""

    def __init__(self, new_skin: str, old_skin: str) -> None:
        """Initialize the change skin command."""
        self.new_skin = new_skin
        self.old_skin = old_skin
        # TODO: Add reference to skin manager

    def run(self) -> None:
        """Apply the new color scheme."""
        # TODO: Load new skin from SkinManager
        # TODO: Update all UI elements
        # TODO: Save preference to Settings table
        pass

    def undo(self) -> None:
        """Restore previous color scheme."""
        # TODO: Load old skin from SkinManager
        # TODO: Update all UI elements
        # TODO: Save preference to Settings table
        pass

```

#### commands/GUI_commands/change_view.py (27 lines)

```python
"""Command for switching between different visualization views."""

from commands.base_command import BaseCommand


class ChangeViewCommand(BaseCommand):
    """Switch between tree, timeline, table, and stats views."""

    def __init__(self, new_view: str, old_view: str) -> None:
        """Initialize the change view command."""
        self.new_view = new_view  # "tree", "timeline", "table", "stats"
        self.old_view = old_view
        # TODO: Add reference to main window

    def run(self) -> None:
        """Switch to the new visualization view."""
        # TODO: Hide current view widget
        # TODO: Show new view widget
        # TODO: Update menu checkmarks
        pass

    def undo(self) -> None:
        """Switch back to the previous view."""
        # TODO: Hide current view widget
        # TODO: Show old view widget
        # TODO: Update menu checkmarks
        pass

```

#### commands/GUI_commands/move_node.py (0 lines)

```python

```

#### commands/GUI_commands/move_person.py (35 lines)

```python
"""Command for moving a person box in the tree view."""

from commands.base_command import BaseCommand


class MovePersonCommand(BaseCommand):
    """Move a person's visual position in the tree canvas."""

    def __init__(
        self,
        person_id: int,
        new_x: float,
        new_y: float,
        old_x: float,
        old_y: float,
    ) -> None:
        """Initialize the move person command."""
        self.person_id = person_id
        self.new_x = new_x
        self.new_y = new_y
        self.old_x = old_x
        self.old_y = old_y
        # TODO: Add reference to canvas/scene for visual updates

    def run(self) -> None:
        """Move person box to new position."""
        # TODO: Update PersonPosition table in database
        # TODO: Update visual position on canvas
        pass

    def undo(self) -> None:
        """Restore person box to original position."""
        # TODO: Update PersonPosition table with old coordinates
        # TODO: Update visual position on canvas
        pass

```

#### commands/GUI_commands/preference_changes.py (0 lines)

```python

```

#### commands/GUI_commands/rebuild_scene.py (25 lines)

```python
"""Command for rebuilding the entire visualization scene."""

from commands.base_command import BaseCommand


class RebuildSceneCommand(BaseCommand):
    """Rebuild the current view from database state."""

    def __init__(self, database_connection, view_type: str) -> None:
        """Initialize the rebuild scene command."""
        self.db = database_connection
        self.view_type = view_type  # "tree", "timeline", "table", "stats"
        # TODO: Store current scene state for undo

    def run(self) -> None:
        """Clear and rebuild the visualization scene."""
        # TODO: Clear current scene/view
        # TODO: Reload all data from database
        # TODO: Recreate all visual elements
        pass

    def undo(self) -> None:
        """Restore previous scene state."""
        # TODO: Restore from saved scene state
        pass

```

#### commands/GUI_commands/recompute_generation.py (0 lines)

```python

```

#### commands/GUI_commands/recompute_generations.py (26 lines)

```python
"""Command for recalculating generation levels for all people."""

from commands.base_command import BaseCommand


class RecomputeGenerationsCommand(BaseCommand):
    """Recalculate generation numbers for entire family tree."""

    def __init__(self, database_connection) -> None:
        """Initialize the recompute generations command."""
        self.db = database_connection
        self.old_generations: dict[int, int] = {}
        # TODO: Store original generation assignments for undo

    def run(self) -> None:
        """Calculate and update generation levels."""
        # TODO: Use GenerationCalculator to compute levels
        # TODO: Update Person table with new generation values
        # TODO: Update tree view layout
        pass

    def undo(self) -> None:
        """Restore original generation assignments."""
        # TODO: Restore generation values from old_generations
        # TODO: Update tree view layout
        pass

```

#### commands/GUI_commands/timeline_scroll.py (0 lines)

```python

```

#### commands/___init__.py (0 lines)

```python

```

#### commands/base_command.py (13 lines)

```python
"""Base command class for undoable operations."""


class BaseCommand:
    """Base class for all undoable commands in the application."""

    def run(self) -> None:
        """Execute the command."""
        raise NotImplementedError("Subclasses must implement run()")

    def undo(self) -> None:
        """Reverse the command's effects."""
        raise NotImplementedError("Subclasses must implement undo()")

```

#### commands/genealogy_commands/__init__.py (27 lines)

```python
from .add_event import AddEventCommand
from .add_marriage import CreateMarriageCommand
from .add_person import AddPersonCommand
from .assign_parent import AssignParentCommand
from .create_child import CreateChildCommand
from .delete_event import DeleteEventCommand
from .edit_event import EditEventCommand
from .edit_marriage import EditMarriageCommand
from .edit_person import EditPersonCommand
from .end_marriage import EndMarriageCommand
from .delete_person import DeletePersonCommand
from .unassign_parent import UnassignParentCommand

__all__ = [
    "AddEventCommand",
    "CreateMarriageCommand",
    "AddPersonCommand",
    "AssignParentCommand",
    "CreateChildCommand",
    "DeleteEventCommand",
    "EditEventCommand",
    "EditMarriageCommand",
    "EditPersonCommand",
    "EndMarriageCommand",
    "DeletePersonCommand",
    "UnassignParentCommand"
]
```

#### commands/genealogy_commands/add_event.py (23 lines)

```python
"""Command for adding an event to a person."""

from commands.base_command import BaseCommand


class AddEventCommand(BaseCommand):
    """Add a life event to a person."""

    def __init__(self, event_data: dict) -> None:
        """Initialize the add event command."""
        self.event_data = event_data
        self.event_id: int | None = None

    def run(self) -> None:
        """Insert the event into the database."""
        # TODO: Implement database INSERT
        # TODO: Store generated event_id for undo
        pass

    def undo(self) -> None:
        """Remove the event from the database."""
        # TODO: Implement database DELETE using stored event_id
        pass

```

#### commands/genealogy_commands/add_marriage.py (25 lines)

```python
"""Command for creating a marriage between two people."""

from commands.base_command import BaseCommand


class CreateMarriageCommand(BaseCommand):
    """Create a marriage relationship between two people."""

    def __init__(self, marriage_data: dict) -> None:
        """Initialize the create marriage command."""
        self.marriage_data = marriage_data
        self.marriage_id: int | None = None

    def run(self) -> None:
        """Insert the marriage into the database."""
        # TODO: Implement database INSERT
        # TODO: Store generated marriage_id for undo
        # TODO: Handle surname changes if configured
        pass

    def undo(self) -> None:
        """Remove the marriage from the database."""
        # TODO: Implement database DELETE
        # TODO: Revert surname changes if applicable
        pass

```

#### commands/genealogy_commands/add_person.py (35 lines)

```python
"""Command for adding a new person to the database."""

from __future__ import annotations
from typing import TYPE_CHECKING

from models.person import Person
from database.person_repository import PersonRepository

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager


class AddPersonCommand:
    """Add a new person to the dynasty database with undo support."""

    def __init__(self, db_manager: DatabaseManager, person: Person) -> None:
        """Initialize the add person command."""
        self.person = person
        self.person_id: int | None = None
        self.repo = PersonRepository(db_manager)

    def run(self) -> None:
        """Insert the person into the database and store the assigned ID."""
        if self.person_id is None:
            self.person_id = self.repo.insert(self.person)
            self.person.id = self.person_id

        else:
            self.person.id = self.person_id
            self.repo.insert_with_id(self.person)

    def undo(self) -> None:
        """Remove the person from the database."""
        if self.person_id is not None:
            self.repo.delete(self.person_id)
```

#### commands/genealogy_commands/assign_parent.py (33 lines)

```python
"""Command for assigning a parent to a person."""

from commands.base_command import BaseCommand


class AssignParentCommand(BaseCommand):
    """Set or change a person's father or mother."""

    def __init__(
        self,
        database_connection,
        person_id: int,
        parent_id: int,
        parent_type: str,  # "father" or "mother"
    ) -> None:
        """Initialize the assign parent command."""
        self.db = database_connection
        self.person_id = person_id
        self.parent_id = parent_id
        self.parent_type = parent_type
        self.old_parent_id: int | None = None
        # TODO: Store original parent ID for undo

    def run(self) -> None:
        """Assign the parent relationship in database."""
        # TODO: Save current parent ID to old_parent_id
        # TODO: Update father_id or mother_id based on parent_type
        pass

    def undo(self) -> None:
        """Restore original parent relationship."""
        # TODO: Restore parent ID from old_parent_id
        pass

```

#### commands/genealogy_commands/create_child.py (38 lines)

```python
"""Command for creating a child with automatic parent assignment."""

from commands.base_command import BaseCommand


class CreateChildCommand(BaseCommand):
    """Create a new person as child of specified parents."""

    def __init__(
        self,
        database_connection,
        first_name: str,
        last_name: str,
        father_id: int | None = None,
        mother_id: int | None = None,
        **kwargs,
    ) -> None:
        """Initialize the create child command."""
        self.db = database_connection
        self.first_name = first_name
        self.last_name = last_name
        self.father_id = father_id
        self.mother_id = mother_id
        self.additional_data = kwargs
        self.created_person_id: int | None = None
        # TODO: Store created person ID for undo

    def run(self) -> None:
        """Create new person with parent relationships."""
        # TODO: Insert new person into database
        # TODO: Set father_id and mother_id
        # TODO: Store created_person_id
        pass

    def undo(self) -> None:
        """Delete the created child."""
        # TODO: Delete person record using created_person_id
        pass

```

#### commands/genealogy_commands/delete_event.py (25 lines)

```python
"""Command for deleting an event from the database."""

from commands.base_command import BaseCommand


class DeleteEventCommand(BaseCommand):
    """Remove an event from the database."""

    def __init__(self, database_connection, event_id: int) -> None:
        """Initialize the delete event command."""
        self.db = database_connection
        self.event_id = event_id
        self.deleted_data: dict = {}
        # TODO: Store complete event data for undo

    def run(self) -> None:
        """Delete the event from database."""
        # TODO: Fetch and save complete event data to deleted_data
        # TODO: Delete event record from database
        pass

    def undo(self) -> None:
        """Restore the deleted event."""
        # TODO: Re-insert event record from deleted_data
        pass

```

#### commands/genealogy_commands/delete_marriage.py (25 lines)

```python
"""Command for deleting a marriage from the database."""

from commands.base_command import BaseCommand


class DeleteMarriageCommand(BaseCommand):
    """Remove a marriage relationship from the database."""

    def __init__(self, database_connection, marriage_id: int) -> None:
        """Initialize the delete marriage command."""
        self.db = database_connection
        self.marriage_id = marriage_id
        self.deleted_data: dict = {}
        # TODO: Store complete marriage data for undo

    def run(self) -> None:
        """Delete the marriage from database."""
        # TODO: Fetch and save complete marriage data to deleted_data
        # TODO: Delete marriage record from database
        pass

    def undo(self) -> None:
        """Restore the deleted marriage."""
        # TODO: Re-insert marriage record from deleted_data
        pass

```

#### commands/genealogy_commands/delete_person.py (24 lines)

```python
"""Command for removing a person from the database."""

from commands.base_command import BaseCommand


class DeletePersonCommand(BaseCommand):
    """Delete a person from the dynasty database."""

    def __init__(self, person_id: int) -> None:
        """Initialize the delete person command."""
        self.person_id = person_id
        self.person_data: dict | None = None

    def run(self) -> None:
        """Remove the person from the database."""
        # TODO: Fetch and store all person data for undo
        # TODO: Implement database DELETE
        # TODO: Handle cascade effects (orphaned children, etc.)
        pass

    def undo(self) -> None:
        """Restore the deleted person."""
        # TODO: Implement database INSERT with stored person_data
        pass

```

#### commands/genealogy_commands/edit_event.py (26 lines)

```python
"""Command for editing an existing event."""

from commands.base_command import BaseCommand


class EditEventCommand(BaseCommand):
    """Edit details of an existing event."""

    def __init__(self, database_connection, event_id: int, **kwargs) -> None:
        """Initialize the edit event command."""
        self.db = database_connection
        self.event_id = event_id
        self.new_data = kwargs
        self.old_data: dict = {}
        # TODO: Store original event data for undo

    def run(self) -> None:
        """Update event details in database."""
        # TODO: Save current state to old_data
        # TODO: Update event record with new_data
        pass

    def undo(self) -> None:
        """Restore original event details."""
        # TODO: Restore event record from old_data
        pass

```

#### commands/genealogy_commands/edit_marriage.py (26 lines)

```python
"""Command for editing an existing marriage."""

from commands.base_command import BaseCommand


class EditMarriageCommand(BaseCommand):
    """Edit details of an existing marriage relationship."""

    def __init__(self, database_connection, marriage_id: int, **kwargs) -> None:
        """Initialize the edit marriage command."""
        self.db = database_connection
        self.marriage_id = marriage_id
        self.new_data = kwargs
        self.old_data: dict = {}
        # TODO: Store original marriage data for undo

    def run(self) -> None:
        """Update marriage details in database."""
        # TODO: Save current state to old_data
        # TODO: Update marriage record with new_data
        pass

    def undo(self) -> None:
        """Restore original marriage details."""
        # TODO: Restore marriage record from old_data
        pass

```

#### commands/genealogy_commands/edit_person.py (24 lines)

```python
"""Command for editing an existing person."""

from commands.base_command import BaseCommand


class EditPersonCommand(BaseCommand):
    """Edit an existing person in the database."""

    def __init__(self, person_id: int, new_data: dict) -> None:
        """Initialize the edit person command."""
        self.person_id = person_id
        self.new_data = new_data
        self.old_data: dict | None = None

    def run(self) -> None:
        """Update the person in the database."""
        # TODO: Fetch and store old data for undo
        # TODO: Implement database UPDATE
        pass

    def undo(self) -> None:
        """Restore the person's original data."""
        # TODO: Implement database UPDATE with old_data
        pass

```

#### commands/genealogy_commands/end_marriage.py (35 lines)

```python
"""Command for ending a marriage with divorce or death."""

from commands.base_command import BaseCommand


class EndMarriageCommand(BaseCommand):
    """Mark a marriage as ended with a specific date."""

    def __init__(
        self,
        database_connection,
        marriage_id: int,
        end_year: int | None = None,
        end_month: int | None = None,
        end_day: int | None = None,
    ) -> None:
        """Initialize the end marriage command."""
        self.db = database_connection
        self.marriage_id = marriage_id
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.old_end_date: tuple[int | None, int | None, int | None] = (None, None, None)
        # TODO: Store original end date for undo

    def run(self) -> None:
        """Set the marriage end date in database."""
        # TODO: Save current end date to old_end_date
        # TODO: Update marriage end_year, end_month, end_day
        pass

    def undo(self) -> None:
        """Restore original marriage end date."""
        # TODO: Restore end date from old_end_date
        pass

```

#### commands/genealogy_commands/unassign_parent.py (31 lines)

```python
"""Command for removing a parent assignment from a person."""

from commands.base_command import BaseCommand


class UnassignParentCommand(BaseCommand):
    """Remove a person's father or mother relationship."""

    def __init__(
        self,
        database_connection,
        person_id: int,
        parent_type: str,  # "father" or "mother"
    ) -> None:
        """Initialize the unassign parent command."""
        self.db = database_connection
        self.person_id = person_id
        self.parent_type = parent_type
        self.old_parent_id: int | None = None
        # TODO: Store original parent ID for undo

    def run(self) -> None:
        """Remove the parent relationship from database."""
        # TODO: Save current parent ID to old_parent_id
        # TODO: Set father_id or mother_id to NULL based on parent_type
        pass

    def undo(self) -> None:
        """Restore the parent relationship."""
        # TODO: Restore parent ID from old_parent_id
        pass

```

#### commands/undo_redo_manager.py (55 lines)

```python
from __future__ import annotations
from typing import Protocol


class Command(Protocol):
    """Protocol defining the interface for undoable commands."""

    def run(self) -> None:
        """Execute the command."""
        ...

    def undo(self) -> None:
        """Reverse the command's effects."""
        ...


class UndoRedoManager:
    """Manages undo and redo stacks for command pattern operations."""

    def __init__(self) -> None:
        """Initialize the undo/redo manager with empty stacks."""
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        """Execute a command and add it to the undo stack."""
        command.run()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self) -> bool:
        """Undo the last executed command."""
        if not self.undo_stack:
            return False
        cmd = self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)
        return True

    def redo(self) -> bool:
        """Redo the last undone command."""
        if not self.redo_stack:
            return False
        cmd = self.redo_stack.pop()
        cmd.run()
        self.undo_stack.append(cmd)
        return True

    def can_undo(self) -> bool:
        """Check if there are commands available to undo."""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if there are commands available to redo."""
        return len(self.redo_stack) > 0

```

#### commands/view_changes.py (0 lines)

```python

```

### Dialogs

#### dialogs/__init__.py (5 lines)

```python
"""Dialog implementations for user interactions."""

from .add_person_dialog import AddPersonDialog

__all__ = ['AddPersonDialog']
```

#### dialogs/about_dialog.py (16 lines)

```python
"""About dialog showing application information."""

from PySide6.QtWidgets import QDialog


class AboutDialog(QDialog):
    """Dialog displaying application information and credits."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the about dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add application name, version, credits
        # TODO: Add license information
        # TODO: Add GitHub link
        pass

```

#### dialogs/add_event_dialog.py (20 lines)

```python
"""Dialog for adding a new event to a person."""

from PySide6.QtWidgets import QDialog


class AddEventDialog(QDialog):
    """Dialog for creating a new event entry."""

    def __init__(self, parent: 'MainWindow', person_id: int | None = None) -> None:  # type: ignore
        """Initialize the add event dialog."""
        super().__init__(parent)
        self.person_id = person_id
        # TODO: Implement dialog UI
        # TODO: Add PersonSelector widget (pre-filled if person_id provided)
        # TODO: Add event type dropdown
        # TODO: Add DatePicker for event date
        # TODO: Add description text field
        # TODO: Add validation logic
        # TODO: Connect to AddEventCommand
        pass

```

#### dialogs/add_person_dialog.py (197 lines)

```python
"""Dialog for adding a new person to the dynasty."""

from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QComboBox, QTextEdit,
    QPushButton, QDialogButtonBox, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

from models.person import Person

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class AddPersonDialog(QDialog):
    """Dialog for adding a new person with essential information."""
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the add person dialog."""
        super().__init__(parent)
        
        self.setWindowTitle("Add New Person")
        self.setMinimumWidth(400)
        
        self._person: Person | None = None
        
        self._setup_ui()
        self._connect_signals()
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_ui(self) -> None:
        """Create and arrange all dialog widgets."""
        layout = QVBoxLayout(self)
        
        # Special character toolbar
        layout.addLayout(self._create_special_char_toolbar())
        
        # Add separator line
        separator = QLabel()
        separator.setFrameShape(QLabel.Shape.HLine)
        separator.setFrameShadow(QLabel.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Form fields
        layout.addLayout(self._create_form_layout())
        
        # OK/Cancel buttons
        layout.addWidget(self._create_button_box())
    
    def _create_special_char_toolbar(self) -> QHBoxLayout:
        """Create toolbar with special character buttons."""
        toolbar = QHBoxLayout()
        
        # Label
        label = QLabel("Special Characters:")
        toolbar.addWidget(label)
        
        # Character buttons
        special_chars = ['á', 'ý', 'ó', 'é', 'í']
        
        for char in special_chars:
            btn = QPushButton(char)
            btn.setMaximumWidth(40)
            btn.setToolTip(f"Insert '{char}' at cursor")
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(lambda checked, c=char: self._insert_special_char(c))
            toolbar.addWidget(btn)
        
        # Info label
        info = QLabel("(Inserts into focused name field)")
        info.setStyleSheet("color: gray; font-size: 10px;")
        toolbar.addWidget(info)
        
        toolbar.addStretch()
        return toolbar
    
    def _create_form_layout(self) -> QFormLayout:
        """Create form with input fields."""
        form = QFormLayout()
        
        # First Name (required)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Required")
        form.addRow("First Name: *", self.first_name_input)
        
        # Last Name (required)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Required")
        form.addRow("Last Name: *", self.last_name_input)
        
        # Birth Year (required)
        self.birth_year_input = QSpinBox()
        self.birth_year_input.setRange(1000, 2100)
        self.birth_year_input.setValue(1700)
        self.birth_year_input.setSpecialValueText("Unknown")
        form.addRow("Birth Year: *", self.birth_year_input)
        
        # Gender (optional)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Unknown", "Male", "Female", "Other"])
        form.addRow("Gender:", self.gender_input)
        
        # Notes (optional)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes about this person...")
        self.notes_input.setMaximumHeight(80)
        form.addRow("Notes:", self.notes_input)
        
        return form
    
    def _create_button_box(self) -> QDialogButtonBox:
        """Create OK/Cancel button box."""
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._handle_accept)
        button_box.rejected.connect(self.reject)
        return button_box
    
    # ------------------------------------------------------------------
    # Signal Handlers
    # ------------------------------------------------------------------
    
    def _connect_signals(self) -> None:
        """Connect widget signals to handlers."""
        # Enter key in line edits should not close dialog accidentally
        self.first_name_input.returnPressed.connect(self.last_name_input.setFocus)
        self.last_name_input.returnPressed.connect(self.birth_year_input.setFocus)
    
    def _insert_special_char(self, char: str) -> None:
        """Insert special character into currently focused name field."""
        focused = self.focusWidget()
        
        # Only insert into line edit fields (name fields)
        if isinstance(focused, QLineEdit):
            focused.insert(char)
    
    def _handle_accept(self) -> None:
        """Validate inputs and create Person object before accepting."""
        if not self._validate_inputs():
            return
        
        # Create Person object from form data
        self._person = Person(
            first_name=self.first_name_input.text().strip(),
            last_name=self.last_name_input.text().strip(),
            birth_year=self.birth_year_input.value(),
            gender=self.gender_input.currentText(),
            notes=self.notes_input.toPlainText().strip()
        )
        
        self.accept()
    
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    
    def _validate_inputs(self) -> bool:
        """Validate that required fields are filled."""
        # Check first name
        if not self.first_name_input.text().strip():
            self._show_error("First name is required.")
            self.first_name_input.setFocus()
            return False
        
        # Check last name
        if not self.last_name_input.text().strip():
            self._show_error("Last name is required.")
            self.last_name_input.setFocus()
            return False
        
        # Check birth year (0 is the special "Unknown" value)
        if self.birth_year_input.value() == 0:
            self._show_error("Birth year is required.")
            self.birth_year_input.setFocus()
            return False
        
        return True
    
    def _show_error(self, message: str) -> None:
        """Display validation error message."""
        QMessageBox.warning(self, "Validation Error", message)
    
    # ------------------------------------------------------------------
    # Public Interface
    # ------------------------------------------------------------------
    
    def get_person(self) -> Person | None:
        """Return the created Person object, or None if dialog was cancelled."""
        return self._person
```

#### dialogs/create_child_dialog.py (19 lines)

```python
"""Dialog for creating a new child with parent selection."""

from PySide6.QtWidgets import QDialog


class CreateChildDialog(QDialog):
    """Dialog for creating a child of selected parents."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the create child dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add name input fields
        # TODO: Add PersonSelector widgets for father/mother
        # TODO: Add DatePicker for birth date
        # TODO: Add gender selection
        # TODO: Add validation logic
        # TODO: Connect to CreateChildCommand
        pass

```

#### dialogs/create_marriage_dialog.py (18 lines)

```python
"""Dialog for creating a new marriage between two people."""

from PySide6.QtWidgets import QDialog


class CreateMarriageDialog(QDialog):
    """Dialog for creating a marriage relationship."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the create marriage dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add PersonSelector widgets for husband/wife
        # TODO: Add DatePicker for marriage date
        # TODO: Add marriage_type dropdown (optional)
        # TODO: Add validation logic
        # TODO: Connect to CreateMarriageCommand
        pass

```

#### dialogs/edit_person_dialog.py (17 lines)

```python
"""Dialog for editing an existing person."""

from PySide6.QtWidgets import QDialog


class EditPersonDialog(QDialog):
    """Dialog for editing an existing person's data."""

    def __init__(self, parent: 'MainWindow', person_id: int) -> None:  # type: ignore
        """Initialize the edit person dialog."""
        super().__init__(parent)
        self.person_id = person_id
        # TODO: Implement dialog UI
        # TODO: Load existing person data
        # TODO: Add form fields
        # TODO: Add validation logic
        pass

```

#### dialogs/import_csv_dialog.py (19 lines)

```python
"""Dialog for importing genealogy data from CSV files."""

from PySide6.QtWidgets import QDialog


class ImportCSVDialog(QDialog):
    """Dialog for CSV import configuration and mapping."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the CSV import dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI
        # TODO: Add file picker for CSV selection
        # TODO: Add column mapping controls
        # TODO: Add preview table
        # TODO: Add import mode selection (replace/merge)
        # TODO: Add progress bar
        # TODO: Connect to CSVImporter utility
        pass

```

#### dialogs/settings_dialog.py (19 lines)

```python
"""Dialog for application preferences and settings."""

from PySide6.QtWidgets import QDialog


class PreferencesDialog(QDialog):
    """Dialog for configuring application settings."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the preferences dialog."""
        super().__init__(parent)
        # TODO: Implement dialog UI with tabs
        # TODO: Add appearance settings (skin selection)
        # TODO: Add default view selection
        # TODO: Add date format preferences
        # TODO: Add auto-save settings
        # TODO: Load current settings from database
        # TODO: Save settings on OK button
        pass

```

### Views

#### views/__init__.py (0 lines)

```python

```

#### views/data_table.py (0 lines)

```python

```

#### views/dynasty_view.py (0 lines)

```python

```

#### views/stats_view/charts.py (26 lines)

```python
"""Chart widgets for statistical visualizations."""

from PySide6.QtWidgets import QWidget


class Charts(QWidget):
    """Container for various statistical charts and graphs."""

    def __init__(self, database_connection) -> None:
        """Initialize the charts widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Add population over time chart
        # TODO: Add birth/death rate chart
        # TODO: Add age distribution histogram
        # TODO: Add family size comparison chart
        # TODO: Use matplotlib or QtCharts for rendering
        # TODO: Add export chart buttons
        pass

    def refresh_charts(self) -> None:
        """Reload data and redraw all charts."""
        # TODO: Reload statistics from database
        # TODO: Regenerate all chart data
        # TODO: Redraw all visualizations
        pass

```

#### views/stats_view/comparison_widget.py (25 lines)

```python
"""Widget for comparing statistics between families or people."""

from PySide6.QtWidgets import QWidget


class ComparisonWidget(QWidget):
    """Side-by-side comparison of selected entities."""

    def __init__(self, database_connection) -> None:
        """Initialize the comparison widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Add selectors for entities to compare
        # TODO: Display side-by-side statistics
        # TODO: Show comparison charts
        # TODO: Highlight differences
        # TODO: Support comparing families, people, or generations
        pass

    def set_comparison(self, entity1_id: int, entity2_id: int, entity_type: str) -> None:
        """Set which entities to compare."""
        # TODO: Load data for both entities
        # TODO: Calculate comparison metrics
        # TODO: Update display
        pass

```

#### views/stats_view/family_dashboard.py (27 lines)

```python
"""Dashboard widget showing dynasty statistics."""

from PySide6.QtWidgets import QWidget


class FamilyDashboard(QWidget):
    """Dashboard displaying key statistics about the dynasty."""

    def __init__(self, database_connection) -> None:
        """Initialize the family dashboard widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Calculate total people count
        # TODO: Calculate total marriages count
        # TODO: Calculate average lifespan
        # TODO: Calculate generation count
        # TODO: Display statistics in grid layout
        # TODO: Add Charts widget for visualizations
        # TODO: Add refresh button
        pass

    def refresh_stats(self) -> None:
        """Recalculate and update all statistics."""
        # TODO: Reload data from database
        # TODO: Recalculate all metrics
        # TODO: Update display widgets
        pass

```

#### views/table_view/event_table.py (27 lines)

```python
"""Table view for listing all events in the database."""

from PySide6.QtWidgets import QTableWidget


class EventTable(QTableWidget):
    """Sortable, filterable table of all events."""

    def __init__(self, database_connection) -> None:
        """Initialize the event table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Person, Event Type, Date, Description)
        # TODO: Load all events from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add clickable person names
        # TODO: Add double-click handler to show event details
        # TODO: Add right-click menu (edit/delete)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all events
        # TODO: Repopulate table
        pass

```

#### views/table_view/family_table.py (26 lines)

```python
"""Table view for listing all families in the database."""

from PySide6.QtWidgets import QTableWidget


class FamilyTable(QTableWidget):
    """Sortable, filterable table of all families."""

    def __init__(self, database_connection) -> None:
        """Initialize the family table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Family Name, Member Count, Start Year, etc.)
        # TODO: Load all families from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add double-click handler to show family details
        # TODO: Add right-click menu (edit/view members)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all families
        # TODO: Repopulate table
        pass

```

#### views/table_view/marriage_table.py (27 lines)

```python
"""Table view for listing all marriages in the database."""

from PySide6.QtWidgets import QTableWidget


class MarriageTable(QTableWidget):
    """Sortable, filterable table of all marriages."""

    def __init__(self, database_connection) -> None:
        """Initialize the marriage table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Husband, Wife, Start Date, End Date, Type)
        # TODO: Load all marriages from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add clickable person names
        # TODO: Add double-click handler to show marriage details
        # TODO: Add right-click menu (edit/end/delete)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all marriages
        # TODO: Repopulate table
        pass

```

#### views/table_view/person_table.py (27 lines)

```python
"""Table view for listing all people in the database."""

from PySide6.QtWidgets import QTableWidget


class PersonTable(QTableWidget):
    """Sortable, filterable table of all people."""

    def __init__(self, database_connection) -> None:
        """Initialize the person table widget."""
        super().__init__()
        self.db = database_connection
        # TODO: Set column headers (Name, Gender, Birth, Death, etc.)
        # TODO: Load all people from database
        # TODO: Populate table rows
        # TODO: Enable sorting by column
        # TODO: Add row selection highlighting
        # TODO: Add double-click handler to show person details
        # TODO: Add right-click menu (edit/delete)
        pass

    def refresh_data(self) -> None:
        """Reload table data from database."""
        # TODO: Clear existing rows
        # TODO: Reload all people
        # TODO: Repopulate table
        pass

```

#### views/timeline_view/event_marker.py (18 lines)

```python
"""Visual marker for person events on timeline."""

from PySide6.QtWidgets import QGraphicsWidget


class EventMarker(QGraphicsWidget):
    """Small marker showing an event on a person's timeline bar."""

    def __init__(self, event_id: int) -> None:
        """Initialize the event marker widget."""
        super().__init__()
        self.event_id = event_id
        # TODO: Load event data from database
        # TODO: Draw small icon/shape at event year
        # TODO: Use different colors for event types
        # TODO: Add tooltip showing event details
        # TODO: Add click handler for event editing
        pass

```

#### views/timeline_view/family_bar.py (19 lines)

```python
"""Horizontal bar representing a family's timespan."""

from PySide6.QtWidgets import QGraphicsWidget


class FamilyBar(QGraphicsWidget):
    """Visual bar showing family existence over time."""

    def __init__(self, family_id: int) -> None:
        """Initialize the family bar widget."""
        super().__init__()
        self.family_id = family_id
        # TODO: Calculate family start year (earliest member birth)
        # TODO: Calculate family end year (latest member death or current)
        # TODO: Draw horizontal bar spanning timespan
        # TODO: Add family name label
        # TODO: Add click handler to show family details
        # TODO: Add PersonBar widgets for each family member
        pass

```

#### views/timeline_view/major_event_marker.py (19 lines)

```python
"""Visual marker for major historical events."""

from PySide6.QtWidgets import QGraphicsWidget


class MajorEventMarker(QGraphicsWidget):
    """Vertical line showing major events across all families."""

    def __init__(self, major_event_id: int) -> None:
        """Initialize the major event marker widget."""
        super().__init__()
        self.major_event_id = major_event_id
        # TODO: Load major event data from database
        # TODO: Draw vertical line at event year
        # TODO: Add event name label
        # TODO: Use distinctive color/style
        # TODO: Add tooltip with event description
        # TODO: Add click handler for editing
        pass

```

#### views/timeline_view/person_bar.py (20 lines)

```python
"""Horizontal bar representing a person's lifespan."""

from PySide6.QtWidgets import QGraphicsWidget


class PersonBar(QGraphicsWidget):
    """Visual bar showing person's life from birth to death."""

    def __init__(self, person_id: int) -> None:
        """Initialize the person bar widget."""
        super().__init__()
        self.person_id = person_id
        # TODO: Load person data from database
        # TODO: Calculate x position from birth_year
        # TODO: Calculate width from birth_year to death_year (or current)
        # TODO: Draw horizontal bar with portrait thumbnail
        # TODO: Add name label
        # TODO: Add event markers along bar
        # TODO: Add click handler to show person details
        pass

```

#### views/timeline_view/timeline_canvas.py (25 lines)

```python
"""Main canvas for the timeline visualization view."""

from PySide6.QtWidgets import QGraphicsView


class TimelineCanvas(QGraphicsView):
    """Scrollable canvas displaying families and events over time."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the timeline canvas."""
        super().__init__(parent)
        # TODO: Create QGraphicsScene
        # TODO: Add horizontal time axis (year scale)
        # TODO: Add vertical scrolling for families
        # TODO: Implement zoom for time scale
        # TODO: Add major event markers
        # TODO: Load all families and events from database
        pass

    def refresh_timeline(self) -> None:
        """Reload and redraw entire timeline from database."""
        # TODO: Clear scene
        # TODO: Reload all data
        # TODO: Recreate all visual elements
        pass

```

#### views/timeline_view.py (0 lines)

```python

```

#### views/tree_view/__init__.py (1 lines)

```python
"""Tree view components for family tree visualization."""

```

#### views/tree_view/generation_band.py (25 lines)

```python
"""Horizontal band showing a generation level in the tree."""

from PySide6.QtWidgets import QGraphicsWidget


class GenerationBand(QGraphicsWidget):
    """Background band for highlighting a generation level."""

    def __init__(self, generation: int, y_position: float, height: float) -> None:
        """Initialize the generation band widget."""
        super().__init__()
        self.generation = generation
        self.y_position = y_position
        self.height = height
        # TODO: Draw horizontal background rectangle
        # TODO: Use alternating colors for visual separation
        # TODO: Add generation label on left side
        # TODO: Update position when tree layout changes
        pass

    def update_position(self, new_y: float, new_height: float) -> None:
        """Adjust band position and height."""
        # TODO: Update y_position and height
        # TODO: Redraw band
        pass

```

#### views/tree_view/layout_engine.py (17 lines)

```python
"""Automatic layout engine for positioning people in the tree."""


class TreeLayoutEngine:
    """Calculate automatic positions for people in the family tree."""

    def __init__(self, database_connection) -> None:
        """Initialize the layout engine."""
        self.db = database_connection

    def calculate_positions(self) -> dict[int, tuple[float, float]]:
        """Calculate x,y positions for all people."""
        # TODO: Implement generational hierarchy algorithm
        # TODO: Group siblings together
        # TODO: Consider cohort positioning (move-in dates)
        # TODO: Return dict: person_id -> (x, y)
        pass

```

#### views/tree_view/marriage_node.py (18 lines)

```python
"""Visual representation of a marriage in the tree view."""

from PySide6.QtWidgets import QGraphicsWidget


class MarriageNode(QGraphicsWidget):
    """Node connecting spouses in the family tree."""

    def __init__(self, marriage_id: int) -> None:
        """Initialize the marriage node widget."""
        super().__init__()
        self.marriage_id = marriage_id
        # TODO: Draw small connector shape (circle/diamond)
        # TODO: Display marriage date on hover
        # TODO: Connect to both spouse PersonBox widgets
        # TODO: Add click handler to show marriage details
        # TODO: Add right-click menu (edit/end/delete marriage)
        pass

```

#### views/tree_view/person_box.py (19 lines)

```python
"""Person box widget for the tree view."""

from PySide6.QtWidgets import QGraphicsWidget


class PersonBox(QGraphicsWidget):
    """Visual representation of a person in the family tree."""

    def __init__(self, person_id: int) -> None:
        """Initialize the person box widget."""
        super().__init__()
        self.person_id = person_id
        # TODO: Add portrait display
        # TODO: Add name label
        # TODO: Add dates label
        # TODO: Add gear icon button
        # TODO: Implement drag functionality
        # TODO: Implement click handlers
        pass

```

#### views/tree_view/relationship_line.py (30 lines)

```python
"""Visual line connecting related people in the tree."""

from PySide6.QtWidgets import QGraphicsWidget


class RelationshipLine(QGraphicsWidget):
    """Line connecting parent to child or spouse to spouse."""

    def __init__(
        self,
        start_person_id: int,
        end_person_id: int,
        line_type: str,  # "parent", "marriage", "sibling"
    ) -> None:
        """Initialize the relationship line widget."""
        super().__init__()
        self.start_person_id = start_person_id
        self.end_person_id = end_person_id
        self.line_type = line_type
        # TODO: Draw line between two PersonBox widgets
        # TODO: Use different styles for different line types
        # TODO: Update position when PersonBox moves
        # TODO: Add hover highlighting
        pass

    def update_endpoints(self) -> None:
        """Recalculate line position based on connected boxes."""
        # TODO: Get current positions of connected PersonBox widgets
        # TODO: Redraw line with new coordinates
        pass

```

#### views/tree_view/tree_canvas.py (16 lines)

```python
"""Main canvas for displaying the family tree."""

from PySide6.QtWidgets import QGraphicsView


class TreeCanvas(QGraphicsView):
    """Scrollable, zoomable canvas for displaying the family tree."""

    def __init__(self, parent: 'MainWindow') -> None:  # type: ignore
        """Initialize the tree canvas."""
        super().__init__(parent)
        # TODO: Create QGraphicsScene
        # TODO: Implement zoom functionality
        # TODO: Implement pan functionality
        # TODO: Add minimap (optional)
        pass

```

### Widgets

#### widgets/__init__.py (0 lines)

```python

```

#### widgets/date_picker.py (18 lines)

```python
"""Custom date picker widget supporting flexible precision."""

from PySide6.QtWidgets import QWidget


class DatePicker(QWidget):
    """Widget for entering dates with flexible precision."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the date picker widget."""
        super().__init__(parent)
        # TODO: Add year spinbox
        # TODO: Add month combobox (with None option)
        # TODO: Add day spinbox (with None option)
        # TODO: Implement date validation logic
        # TODO: Add get_date() method
        # TODO: Add set_date() method
        pass

```

#### widgets/extended_details_panel.py (27 lines)

```python
"""Panel widget for displaying detailed person information."""

from PySide6.QtWidgets import QWidget


class ExtendedDetailsPanel(QWidget):
    """Panel showing comprehensive person details and relationships."""

    def __init__(self, person_id: int | None = None) -> None:
        """Initialize the extended details panel."""
        super().__init__()
        self.person_id = person_id
        # TODO: Display full person information
        # TODO: Show all marriages with dates
        # TODO: Show all children with clickable links
        # TODO: Show all events in chronological order
        # TODO: Show portrait gallery
        # TODO: Add edit button for each section
        # TODO: Add relationship path calculator
        pass

    def set_person(self, person_id: int) -> None:
        """Update panel to show different person."""
        # TODO: Clear current display
        # TODO: Load new person data
        # TODO: Refresh all sections
        pass

```

#### widgets/person_selector.py (17 lines)

```python
"""Widget for selecting a person from the database."""

from PySide6.QtWidgets import QWidget


class PersonSelector(QWidget):
    """Searchable dropdown widget for selecting a person."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the person selector widget."""
        super().__init__(parent)
        # TODO: Add search field
        # TODO: Add dropdown list
        # TODO: Implement real-time filtering
        # TODO: Load people from database
        # TODO: Add get_selected_person() method
        pass

```

#### widgets/portrait_gallery.py (19 lines)

```python
"""Widget for displaying and managing person portraits."""

from PySide6.QtWidgets import QWidget


class PortraitGallery(QWidget):
    """Gallery widget for viewing and selecting portraits."""

    def __init__(self, person_id: int) -> None:
        """Initialize the portrait gallery widget."""
        super().__init__()
        self.person_id = person_id
        # TODO: Load portraits from Portrait table
        # TODO: Display portraits in grid layout
        # TODO: Add portrait selection highlighting
        # TODO: Add upload new portrait button
        # TODO: Add delete portrait button
        # TODO: Emit signal on portrait selection
        pass

```

#### widgets/search_bar.py (25 lines)

```python
"""Search bar widget for finding people by name."""

from PySide6.QtWidgets import QWidget


class SearchBar(QWidget):
    """Search widget with autocomplete for finding people."""

    def __init__(self) -> None:
        """Initialize the search bar widget."""
        super().__init__()
        # TODO: Add QLineEdit for search input
        # TODO: Implement autocomplete using QCompleter
        # TODO: Load all person names from database
        # TODO: Add search icon/button
        # TODO: Add clear button
        # TODO: Emit signal when person is selected
        # TODO: Support fuzzy matching (optional)
        pass

    def update_completions(self) -> None:
        """Refresh autocomplete list from database."""
        # TODO: Reload all person names
        # TODO: Update QCompleter model
        pass

```

### Utils

#### utils/__init__.py (1 lines)

```python
"""Utility modules for calculations and helpers."""

```

#### utils/color_manager.py (39 lines)

```python
"""Color utilities for UI elements."""

from PySide6.QtGui import QColor


class ColorManager:
    """Manage colors for various UI elements."""

    def __init__(self) -> None:
        """Initialize the color manager."""
        # TODO: Define color palettes
        # TODO: Define gender-specific colors
        # TODO: Define generation band colors
        # TODO: Define event type colors
        pass

    def get_person_color(self, gender: str | None) -> QColor: # type: ignore 
        """Get color for person based on gender."""
        # TODO: Return blue for male
        # TODO: Return pink for female
        # TODO: Return gray for unknown
        pass

    def get_generation_color(self, generation: int) -> QColor: # type: ignore 
        """Get alternating color for generation bands."""
        # TODO: Return alternating colors based on generation number
        pass

    def get_event_color(self, event_type: str) -> QColor: # type: ignore 
        """Get color for event type."""
        # TODO: Return different colors for different event types
        # TODO: Birth, death, marriage, arrival, etc.
        pass

    def interpolate_color(self, color1: QColor, color2: QColor, ratio: float) -> QColor: # type: ignore 
        """Blend two colors together."""
        # TODO: Calculate intermediate color
        # TODO: Return blended QColor
        pass

```

#### utils/csv_importer.py (38 lines)

```python
"""CSV import utility for bulk data loading."""

import csv


class CSVImporter:
    """Import genealogy data from CSV files."""

    def __init__(self, database_connection) -> None:
        """Initialize the CSV importer."""
        self.db = database_connection

    def import_people(self, csv_path: str, column_mapping: dict[str, str]) -> int:
        """Import people from CSV file."""
        # TODO: Open and read CSV file
        # TODO: Map CSV columns to database fields
        # TODO: Validate data
        # TODO: Insert people into database
        # TODO: Return count of imported people
        pass

    def import_marriages(self, csv_path: str, column_mapping: dict[str, str]) -> int:
        """Import marriages from CSV file."""
        # TODO: Open and read CSV file
        # TODO: Map CSV columns to database fields
        # TODO: Validate data (check person IDs exist)
        # TODO: Insert marriages into database
        # TODO: Return count of imported marriages
        pass

    def import_events(self, csv_path: str, column_mapping: dict[str, str]) -> int:
        """Import events from CSV file."""
        # TODO: Open and read CSV file
        # TODO: Map CSV columns to database fields
        # TODO: Validate data
        # TODO: Insert events into database
        # TODO: Return count of imported events
        pass

```

#### utils/generation_calculator.py (17 lines)

```python
"""Calculate generation levels for all people."""


class GenerationCalculator:
    """Compute generation levels for genealogical hierarchy."""

    def __init__(self, database_connection) -> None:
        """Initialize the generation calculator."""
        self.db = database_connection

    def recompute_all_generations(self) -> None:
        """Recalculate generation levels for all people."""
        # TODO: Find all founders (no parents)
        # TODO: Run BFS from founders
        # TODO: Assign generation numbers
        # TODO: Handle edge cases (adoptions, step-relations)
        pass

```

#### utils/relationship_calculator.py (22 lines)

```python
"""Calculate relationships between people using graph traversal."""


class RelationshipCalculator:
    """Calculate familial relationships between two people."""

    def __init__(self, database_connection) -> None:
        """Initialize the relationship calculator."""
        self.db = database_connection

    def find_relationship_path(self, person1_id: int, person2_id: int) -> list[int] | None:
        """Find the shortest relationship path between two people."""
        # TODO: Implement BFS graph traversal
        # TODO: Return list of person IDs in the path
        pass

    def describe_relationship(self, person1_id: int, person2_id: int) -> str:
        """Return a human-readable relationship description."""
        # TODO: Implement relationship naming logic
        # TODO: Handle parents, siblings, cousins, etc.
        # TODO: Handle "removed" relationships
        pass

```

#### utils/settings_manager.py (210 lines)

```python
"""User preferences and settings management."""

from __future__ import annotations
from typing import Any
from PySide6.QtCore import QSettings

class SettingsManager:
    """Manages user preferences and disk persistence."""

    DEFAULTS = {
        "shortcuts": {
            # File Menu shortcuts
            "file.new": "Ctrl+N",
            "file.open": "Ctrl+O",
            "file.save": "Ctrl+S",
            "file.save_as": "Ctrl+Shift+S",
            "file.exit": "Ctrl+Q",

            # Edit Menu shortcuts
            "edit.undo": "Ctrl+Z",
            "edit.redo": "Ctrl+Y",
            "edit.add_person": "Ctrl+P",
            "edit.remove_person": "Del",
            "edit.add_new_family": "Ctrl+F",

            # View Menu shortcuts
            "view.family_trees": "Ctrl+1",
            "view.timeline": "Ctrl+2",
            "view.dynasty": "Ctrl+3",
            "view.data_table": "Ctrl+4",

            # Tools Menu shortcuts
            "tools.rebuild_scene": "F5",
            "tools.recompute_generations": "Ctrl+R",
            "tools.validate_marriages": "Ctrl+M",
            "tools.validate_parentage": "Ctrl+Shift+P",

            # Settings Menu shortcuts
            "settings.settings": "Ctrl+,",
            "settings.general": "",
            "settings.shortcuts": "",
            "settings.display": "",
            "settings.appearance": "",
            "settings.formats": "",

            # Help Menu shortcuts
            "help.about": "F1",
        },

        "general": {
            # TODO: Define general settings defaults
            # e.g., autosave interval, default file paths, etc.
            # including different header sections as above
        },

        "display": {
            # TODO: Define display settings defaults
            # e.g., default zoom level, layout preferences, etc.
            # including different header sections as above
            # window size, position, maximized state, fonts, themes etc.
        },

        "appearance": {
            # TODO: Define appearance settings defaults
            # e.g., color schemes, node styles, edge styles, Colorblindness modes,
            # Male/Female/Unknown color preferences, generation band colors, genetic line styles, etc.
            # including different header sections as above to keep things organized
        },

        "formats": {
            # TODO: Define format settings defaults
            # e.g., date formats, name display formats, event display formats, etc.
            # Undo/Redo stack size, autosave file format, import/export preferences, etc.
            # including different header sections as above
        },
    }

    def __init__(self) -> None:
        """Initialize settings manager and load user settings."""
        
        self.qsettings = QSettings("DynastyVizualizer", "DynastyVisualizer")

        self.custom_shortcuts: dict[str, str | None] = {}
        self.custom_general: dict[str, Any] = {}
        self.custom_display: dict[str, Any] = {}
        self.custom_appearance: dict[str, Any] = {}
        self.custom_formats: dict[str, Any] = {}
    
        self._load_from_disk()

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def _get_custom_dict(self, category: str) -> dict[str, Any]:
        """Get the custom dictionary for a given category."""
        category_map = {
            "shortcuts": self.custom_shortcuts,
            "general": self.custom_general,
            "display": self.custom_display,
            "appearance": self.custom_appearance,
            "formats": self.custom_formats,
        }
        return category_map.get(category, {})

    def _load_from_disk(self) -> None:
        """Load user's saved settings from disk."""
        for category in self.DEFAULTS.keys():
            self.qsettings.beginGroup(category)
            custom_dict = self._get_custom_dict(category)
            
            for key in self.DEFAULTS[category].keys():
                if self.qsettings.contains(key):
                    value = self.qsettings.value(key)
                    custom_dict[key] = value if value else None
            
            self.qsettings.endGroup()
    def _save_to_disk(self) -> None:
        """Save user's custom settings to disk."""
        for category in self.DEFAULTS.keys():
            # Clear existing category on disk
            self.qsettings.beginGroup(category)
            self.qsettings.remove("")
            self.qsettings.endGroup()
            
            # Save only settings that exist in current DEFAULTS
            self.qsettings.beginGroup(category)
            custom_dict = self._get_custom_dict(category)
            
            for key in self.DEFAULTS[category].keys():
                if key in custom_dict:  
                    value = custom_dict[key]
                    default = self.DEFAULTS[category][key]

                    if value != default:
                        self.qsettings.setValue(key, value if value else "")
            
            self.qsettings.endGroup()
        
        self.qsettings.sync()

    # ------------------------------------------------------------------
    # Shortcut Operations (Specific, Type-Safe)
    # ------------------------------------------------------------------

    def get_shortcut(self, action_name: str) -> str:
        """Get the shortcut for a given action, falling back to default if not customized."""
        return self.get_setting("shortcuts", action_name)

    def set_shortcut(self, action_name: str, shortcut: str) -> None:
        """Set custom shortcut in memory without saving to disk."""
        self.set_setting("shortcuts", action_name, shortcut)

        if shortcut:
            for other_action in list(self.custom_shortcuts.keys()):
                if other_action != action_name:
                    if self.custom_shortcuts[other_action] == shortcut:
                        self.custom_shortcuts[other_action] = None


    # ------------------------------------------------------------------
    # Generic Settings Operations
    # ------------------------------------------------------------------

    def get_setting(self, category: str, key: str) -> Any:
        """Get setting from any category, checking custom then default."""
        # Check custom value first
        custom_dict = self._get_custom_dict(category)
        if key in custom_dict:
            value = custom_dict[key]
            return value if value is not None else ""
        
        # Fall back to default
        if category in self.DEFAULTS and key in self.DEFAULTS[category]:
            return self.DEFAULTS[category][key]
        
        return ""
    
    def set_setting(self, category: str, key: str, value: Any) -> None:
        """Set setting in any category (memory only, not saved to disk)."""
        custom_dict = self._get_custom_dict(category)
        custom_dict[key] = value if value else None

    # ------------------------------------------------------------------
    # Save/Discard/Reset Operations
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Save all custom settings to disk."""
        self._save_to_disk()

    def discard_changes(self) -> None:
        """Discard unsaved changes by reloading from disk."""
        self.custom_shortcuts.clear()
        self.custom_general.clear()
        self.custom_display.clear()
        self.custom_appearance.clear()
        self.custom_formats.clear()
        self._load_from_disk()

    def reset_category_to_defaults(self, category: str) -> None:
        """Reset one category to defaults and save to disk."""
        custom_dict = self._get_custom_dict(category)
        custom_dict.clear()
        self._save_to_disk()

    def reset_all_to_defaults(self) -> None:
        """Reset all categories to defaults and save to disk."""
        for category in self.DEFAULTS.keys():
            self.reset_category_to_defaults(category)
```

#### utils/skin_manager.py (35 lines)

```python
"""Skin/theme management for UI customization."""

from PySide6.QtWidgets import QApplication


class SkinManager:
    """Manage application color schemes and themes."""

    def __init__(self) -> None:
        """Initialize the skin manager with built-in themes."""
        self.skins: dict[str, dict[str, str]] = {}
        # TODO: Define default skin
        # TODO: Define dark mode skin
        # TODO: Define light mode skin
        # TODO: Define custom color schemes
        pass

    def load_skin(self, skin_name: str) -> None:
        """Apply a color scheme to the application."""
        # TODO: Get color definitions for skin_name
        # TODO: Generate QSS stylesheet
        # TODO: Apply to QApplication
        pass

    def get_available_skins(self) -> list[str]:
        """Get list of available skin names."""
        # TODO: Return list of skin keys
        pass

    def create_custom_skin(self, name: str, colors: dict[str, str]) -> None:
        """Create a new custom color scheme."""
        # TODO: Validate color values
        # TODO: Store in skins dictionary
        # TODO: Optionally save to Settings table
        pass

```

#### utils/validators.py (32 lines)

```python
"""Data validation tools for detecting inconsistencies."""


class MarriageValidator:
    """Validate marriage data for inconsistencies."""

    def __init__(self, database_connection) -> None:
        """Initialize the marriage validator."""
        self.db = database_connection

    def validate_all(self) -> list[dict]:
        """Check all marriages for issues."""
        # TODO: Check for overlapping marriages
        # TODO: Check for invalid dates
        # TODO: Check for self-marriages
        # TODO: Return list of issues
        pass


class ParentageValidator:
    """Validate parent-child relationships."""

    def __init__(self, database_connection) -> None:
        """Initialize the parentage validator."""
        self.db = database_connection

    def validate_all(self) -> list[dict]:
        """Check all parentage relationships for issues."""
        # TODO: Check for circular parentage
        # TODO: Check for impossible dates
        # TODO: Return list of issues
        pass

```

### Scripts

#### scripts/create_codebase_summary.py (420 lines)

```python
"""
Auto-generate CODEBASE_SUMMARY.md - Complete codebase snapshot optimized for LLMs.

This script creates a token-efficient, complete snapshot of the entire codebase
that LLMs (Claude, ChatGPT) can use to understand the full project state.

Usage:
    python scripts/create_codebase_summary.py

Output:
    CODEBASE_SUMMARY.md - Complete codebase with all source files

Features:
    - Auto-discovers all non-ignored files
    - Includes full source code for all files
    - Token-efficient format (minimal prose, maximum code)
    - LLM-optimized structure (clear sections, easy to parse)
    - Includes essential metadata and project status
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Tuple


# Configuration
OUTPUT_FILE = "CODEBASE_SUMMARY.md"
PROJECT_NAME = "DynastyVizualizer"

# Files/directories to ignore (gitignore-style)
IGNORE_PATTERNS = {
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    ".env",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".DS_Store",
    "*.egg-info",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "*.dyn",
    "*.backup",
    "node_modules",
}

# File extensions to include as source code
SOURCE_EXTENSIONS = {".py"}

# Config files to include
CONFIG_FILES = {"requirements.txt", "LICENSE"}

# Documentation files (extract minimal info only)
DOC_FILES = {"README.md", "dynasty_codebase.md"}


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored based on patterns."""
    path_str = str(path)
    name = path.name

    # Check exact matches
    if name in IGNORE_PATTERNS:
        return True

    # Check wildcard patterns
    for pattern in IGNORE_PATTERNS:
        if "*" in pattern:
            ext = pattern.replace("*", "")
            if path_str.endswith(ext):
                return True

    # Ignore the output file itself
    if name == OUTPUT_FILE:
        return True

    return False


def count_lines(filepath: Path) -> int:
    """Count total lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def count_code_lines(filepath: Path) -> int:
    """Count non-empty, non-comment lines."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            count = 0
            in_multiline_string = False

            for line in f:
                stripped = line.strip()

                # Skip empty lines
                if not stripped:
                    continue

                # Toggle multiline string state
                if '"""' in stripped or "'''" in stripped:
                    in_multiline_string = not in_multiline_string
                    continue

                # Skip if in multiline string or comment
                if in_multiline_string or stripped.startswith('#'):
                    continue

                count += 1

            return count
    except Exception:
        return 0


def discover_files(root_dir: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Discover all files in the project.

    Returns:
        (source_files, config_files, doc_files)
    """
    source_files = []
    config_files = []
    doc_files = []

    for path in sorted(root_dir.rglob("*")):
        # Skip directories and ignored files
        if path.is_dir() or should_ignore(path):
            continue

        # Categorize files
        if path.suffix in SOURCE_EXTENSIONS:
            source_files.append(path)
        elif path.name in CONFIG_FILES:
            config_files.append(path)
        elif path.name in DOC_FILES:
            doc_files.append(path)

    return source_files, config_files, doc_files


def get_relative_path(filepath: Path, root: Path) -> str:
    """Get path relative to project root."""
    try:
        return str(filepath.relative_to(root))
    except ValueError:
        return str(filepath)


def read_file_content(filepath: Path) -> str:
    """Read file content safely, trying multiple encodings."""
    # Try common encodings
    for encoding in ['utf-8', 'utf-16', 'utf-16-le', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                # Check if content looks reasonable (no null bytes everywhere)
                if '\x00' not in content or encoding.startswith('utf-16'):
                    return content
        except (UnicodeDecodeError, Exception):
            continue

    # Fallback: read as binary and decode with error handling
    try:
        with open(filepath, 'rb') as f:
            return f.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"[Error reading file: {e}]"


def extract_quick_reference(doc_files: List[Path], root: Path) -> str:
    """Extract minimal quick reference from dynasty_codebase.md."""
    dynasty_file = None
    for f in doc_files:
        if f.name == "dynasty_codebase.md":
            dynasty_file = f
            break

    if not dynasty_file:
        return "No quick reference available."

    content = read_file_content(dynasty_file)

    # Extract just the first section (up to first ---) for minimal context
    lines = content.split('\n')
    ref_lines = []
    section_count = 0

    for line in lines:
        if line.strip() == '---':
            section_count += 1
            if section_count >= 2:  # Stop after first major section
                break
        ref_lines.append(line)

    return '\n'.join(ref_lines[:40])  # Limit to ~40 lines max


def build_file_tree(source_files: List[Path], root: Path) -> str:
    """Build visual file tree."""
    # Group files by directory
    tree_dict = {}

    for filepath in source_files:
        rel_path = get_relative_path(filepath, root)
        parts = Path(rel_path).parts

        current = tree_dict
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        # Mark file as implemented (✅) if it has substantial code
        lines = count_code_lines(filepath)
        marker = " ✅" if lines > 20 else " 📋"
        current[parts[-1]] = marker

    # Build tree string
    def build_tree_recursive(d, prefix="", is_last=True):
        lines = []
        items = sorted(d.items())

        for i, (key, value) in enumerate(items):
            is_last_item = (i == len(items) - 1)
            connector = "└── " if is_last_item else "├── "

            if isinstance(value, str):  # It's a file
                lines.append(f"{prefix}{connector}{key}{value}")
            else:  # It's a directory
                lines.append(f"{prefix}{connector}{key}/")
                extension = "    " if is_last_item else "│   "
                lines.extend(build_tree_recursive(value, prefix + extension, is_last_item))

        return lines

    tree_lines = [f"{PROJECT_NAME}/"] + build_tree_recursive(tree_dict)
    return '\n'.join(tree_lines)


def generate_summary(root_dir: Path) -> None:
    """Generate the complete codebase summary."""

    print(f"🔍 Discovering files in {PROJECT_NAME}...")
    source_files, config_files, doc_files = discover_files(root_dir)

    # Calculate statistics
    total_files = len(source_files)
    implemented_files = sum(1 for f in source_files if count_code_lines(f) > 20)
    total_lines = sum(count_lines(f) for f in source_files)
    code_lines = sum(count_code_lines(f) for f in source_files)

    print(f"📊 Found {total_files} Python files ({implemented_files} implemented)")
    print(f"📏 Total: {total_lines} lines ({code_lines} code lines)")

    # Generate output
    output_path = root_dir / OUTPUT_FILE

    with open(output_path, 'w', encoding='utf-8') as out:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Header
        out.write(f"# {PROJECT_NAME} - Complete Codebase Snapshot\n\n")
        out.write(f"**Generated**: {timestamp}\n")
        out.write(f"**Files**: {implemented_files} implemented / {total_files} total\n")
        out.write(f"**Lines**: ~{code_lines:,} code / ~{total_lines:,} total\n")
        out.write(f"**Status**: Phase 1 Complete, Phase 2 In Progress\n\n")
        out.write("---\n\n")

        # Quick Reference
        out.write("## Quick Reference\n\n")
        quick_ref = extract_quick_reference(doc_files, root_dir)
        out.write(quick_ref)
        out.write("\n\n---\n\n")

        # File Tree
        out.write("## File Structure\n\n")
        out.write("```\n")
        out.write(build_file_tree(source_files, root_dir))
        out.write("\n```\n\n")
        out.write("Legend: ✅ Implemented (>20 code lines) | 📋 Scaffolded\n\n")
        out.write("---\n\n")

        # Implementation Status
        out.write("## Implementation Status\n\n")
        out.write(f"**Implemented**: {implemented_files}/{total_files} files\n\n")

        # Group by directory
        by_dir = {}
        for f in source_files:
            rel_path = get_relative_path(f, root_dir)
            dir_name = str(Path(rel_path).parent)
            if dir_name == ".":
                dir_name = "root"

            if dir_name not in by_dir:
                by_dir[dir_name] = []

            lines = count_code_lines(f)
            status = "✅" if lines > 20 else "📋"
            by_dir[dir_name].append((Path(rel_path).name, lines, status))

        for dir_name in sorted(by_dir.keys()):
            out.write(f"**{dir_name}/**\n")
            for name, lines, status in sorted(by_dir[dir_name]):
                out.write(f"- {status} `{name}` ({lines} lines)\n")
            out.write("\n")

        out.write("---\n\n")

        # Complete Source Code
        out.write("## Complete Source Code\n\n")

        # Group files by category for better organization
        categories = {
            "Core": ["main.py"],
            "Database": [],
            "Models": [],
            "Actions": [],
            "Commands": [],
            "Dialogs": [],
            "Views": [],
            "Widgets": [],
            "Utils": [],
            "Scripts": [],
        }

        for f in source_files:
            rel_path = get_relative_path(f, root_dir)
            parent = str(Path(rel_path).parent)

            if "database" in parent:
                categories["Database"].append(f)
            elif "models" in parent:
                categories["Models"].append(f)
            elif "actions" in parent:
                categories["Actions"].append(f)
            elif "commands" in parent:
                categories["Commands"].append(f)
            elif "dialogs" in parent:
                categories["Dialogs"].append(f)
            elif "views" in parent:
                categories["Views"].append(f)
            elif "widgets" in parent:
                categories["Widgets"].append(f)
            elif "utils" in parent:
                categories["Utils"].append(f)
            elif "scripts" in parent:
                categories["Scripts"].append(f)
            elif rel_path not in categories["Core"]:
                categories["Core"].append(f)

        # Output each category
        for category, files in categories.items():
            if not files or (len(files) == 1 and isinstance(files[0], str)):
                continue

            out.write(f"### {category}\n\n")

            for filepath in sorted(files):
                if isinstance(filepath, str):
                    filepath = root_dir / filepath

                rel_path = get_relative_path(filepath, root_dir)
                lines = count_lines(filepath)

                out.write(f"#### {rel_path} ({lines} lines)\n\n")
                out.write("```python\n")
                out.write(read_file_content(filepath))
                out.write("\n```\n\n")

                print(f"✅ Included {rel_path} ({lines} lines)")

        # Configuration Files
        if config_files:
            out.write("---\n\n")
            out.write("## Configuration\n\n")

            for filepath in config_files:
                rel_path = get_relative_path(filepath, root_dir)
                out.write(f"### {rel_path}\n\n")
                out.write("```\n")
                out.write(read_file_content(filepath))
                out.write("\n```\n\n")

        # Footer
        out.write("---\n\n")
        out.write(f"**End of {PROJECT_NAME} Codebase Snapshot**\n\n")
        out.write(f"- **Files**: {implemented_files} implemented / {total_files} total\n")
        out.write(f"- **Lines**: {code_lines:,} code / {total_lines:,} total\n")
        out.write(f"- **Generated**: {timestamp}\n")

    print(f"\n✅ Successfully generated {OUTPUT_FILE}")
    print(f"📊 {implemented_files}/{total_files} files, {code_lines:,} code lines")
    print(f"📄 Output: {output_path}")
    print(f"🤖 Ready for LLM consumption!\n")


if __name__ == "__main__":
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    print(f"{'='*60}")
    print(f"  {PROJECT_NAME} - Codebase Summary Generator")
    print(f"{'='*60}\n")

    generate_summary(project_root)

```

#### scripts/migrate_database.py (224 lines)

```python
"""
Migration script to upgrade existing .dyn files to the new schema.

This script safely adds:
1. Day fields to all date columns (birth, death, arrival, etc.)
2. New tables (Portrait, Family, MajorEvent, PersonPosition, Settings)
3. Additional Person fields (maiden_name, family_id, notes)
4. Marriage type field

Usage:
    python scripts/migrate_database.py <path_to_dynasty_file.dyn>

Example:
    python scripts/migrate_database.py "MyDynasty.dyn"

This migration is SAFE:
- Existing data is preserved (new columns are NULL)
- No data is deleted or modified
- Backup is created before migration
"""

import sqlite3
import shutil
import sys
from pathlib import Path


def backup_database(file_path: str) -> str:
    """Create a backup of the database before migration."""
    backup_path = f"{file_path}.backup"
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path


def get_existing_columns(cursor: sqlite3.Cursor, table_name: str) -> list[str]:
    """Get list of existing columns in a table."""
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]


def migrate_database(file_path: str) -> None:
    """Migrate an existing .dyn database to the new schema."""

    if not Path(file_path).exists():
        print(f"❌ Error: File '{file_path}' not found")
        sys.exit(1)

    print(f"Migrating database: {file_path}")
    print("=" * 60)

    # Create backup
    backup_path = backup_database(file_path)

    try:
        # Connect to database
        conn = sqlite3.connect(file_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Migrate Person table
        print("\n📝 Migrating Person table...")
        person_columns = get_existing_columns(cursor, "Person")

        person_migrations = [
            ("birth_day", "ALTER TABLE Person ADD COLUMN birth_day INTEGER"),
            ("death_day", "ALTER TABLE Person ADD COLUMN death_day INTEGER"),
            ("arrival_day", "ALTER TABLE Person ADD COLUMN arrival_day INTEGER"),
            ("moved_out_day", "ALTER TABLE Person ADD COLUMN moved_out_day INTEGER"),
            ("maiden_name", "ALTER TABLE Person ADD COLUMN maiden_name TEXT"),
            ("family_id", "ALTER TABLE Person ADD COLUMN family_id INTEGER REFERENCES Family(id) ON DELETE SET NULL"),
            ("notes", "ALTER TABLE Person ADD COLUMN notes TEXT"),
            ("middle_name", "ALTER TABLE Person ADD COLUMN middle_name TEXT DEFAULT ''"),
            ("nickname", "ALTER TABLE Person ADD COLUMN nickname TEXT DEFAULT ''"),
            ("dynasty_id", "ALTER TABLE Person ADD COLUMN dynasty_id INTEGER DEFAULT 1"),
            ("is_founder", "ALTER TABLE Person ADD COLUMN is_founder INTEGER DEFAULT 0"),
            ("education", "ALTER TABLE Person ADD COLUMN education INTEGER DEFAULT 0"),
        ]

        for col_name, sql in person_migrations:
            if col_name not in person_columns:
                cursor.execute(sql)
                print(f"  ✅ Added column: {col_name}")
            else:
                print(f"  ⏭️  Column already exists: {col_name}")

        # Migrate Event table
        print("\n📝 Migrating Event table...")
        event_columns = get_existing_columns(cursor, "Event")

        event_migrations = [
            ("start_day", "ALTER TABLE Event ADD COLUMN start_day INTEGER"),
            ("end_day", "ALTER TABLE Event ADD COLUMN end_day INTEGER"),
        ]

        for col_name, sql in event_migrations:
            if col_name not in event_columns:
                cursor.execute(sql)
                print(f"  ✅ Added column: {col_name}")
            else:
                print(f"  ⏭️  Column already exists: {col_name}")

        # Migrate Marriage table
        print("\n📝 Migrating Marriage table...")
        marriage_columns = get_existing_columns(cursor, "Marriage")

        marriage_migrations = [
            ("marriage_day", "ALTER TABLE Marriage ADD COLUMN marriage_day INTEGER"),
            ("dissolution_day", "ALTER TABLE Marriage ADD COLUMN dissolution_day INTEGER"),
            ("marriage_type", "ALTER TABLE Marriage ADD COLUMN marriage_type TEXT DEFAULT 'spouse'"),
        ]

        for col_name, sql in marriage_migrations:
            if col_name not in marriage_columns:
                cursor.execute(sql)
                print(f"  ✅ Added column: {col_name}")
            else:
                print(f"  ⏭️  Column already exists: {col_name}")

        # Create new tables
        print("\n📝 Creating new tables...")

        new_tables = {
            "Portrait": """
                CREATE TABLE IF NOT EXISTS Portrait (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id INTEGER NOT NULL,
                    image_path TEXT NOT NULL,
                    valid_from_year INTEGER,
                    valid_from_month INTEGER,
                    valid_from_day INTEGER,
                    valid_to_year INTEGER,
                    valid_to_month INTEGER,
                    valid_to_day INTEGER,
                    is_primary INTEGER DEFAULT 0,
                    display_order INTEGER DEFAULT 0,
                    FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
                )
            """,
            "Family": """
                CREATE TABLE IF NOT EXISTS Family (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    surname TEXT NOT NULL,
                    move_in_year INTEGER,
                    move_in_month INTEGER,
                    move_in_day INTEGER,
                    coat_of_arms_path TEXT,
                    family_color TEXT,
                    is_extinct INTEGER DEFAULT 0,
                    notes TEXT
                )
            """,
            "MajorEvent": """
                CREATE TABLE IF NOT EXISTS MajorEvent (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_name TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    start_year INTEGER NOT NULL,
                    start_month INTEGER,
                    start_day INTEGER,
                    end_year INTEGER,
                    end_month INTEGER,
                    end_day INTEGER,
                    description TEXT,
                    color TEXT
                )
            """,
            "PersonPosition": """
                CREATE TABLE IF NOT EXISTS PersonPosition (
                    person_id INTEGER PRIMARY KEY,
                    view_type TEXT NOT NULL,
                    x_position REAL NOT NULL,
                    y_position REAL NOT NULL,
                    FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
                )
            """,
            "Settings": """
                CREATE TABLE IF NOT EXISTS Settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """
        }

        for table_name, create_sql in new_tables.items():
            # Check if table exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            if cursor.fetchone():
                print(f"  ⏭️  Table already exists: {table_name}")
            else:
                cursor.execute(create_sql)
                print(f"  ✅ Created table: {table_name}")

        # Commit all changes
        conn.commit()
        conn.close()

        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print(f"✅ Original database backed up to: {backup_path}")
        print(f"✅ Migrated database: {file_path}")
        print("\nYour database is now ready for the full feature set!")
        print("All existing data has been preserved.")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print(f"Restoring from backup: {backup_path}")
        shutil.copy2(backup_path, file_path)
        print("✅ Database restored to original state")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/migrate_database.py <path_to_dynasty_file.dyn>")
        print("\nExample:")
        print('  python scripts/migrate_database.py "MyDynasty.dyn"')
        sys.exit(1)

    dynasty_file = sys.argv[1]
    migrate_database(dynasty_file)

```

---

## Configuration

### LICENSE

```
Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.

1. Copyright and Related Rights. A Work made available under CC0 may be
protected by copyright and related or neighboring rights ("Copyright and
Related Rights"). Copyright and Related Rights include, but are not
limited to, the following:

  i. the right to reproduce, adapt, distribute, perform, display,
     communicate, and translate a Work;
 ii. moral rights retained by the original author(s) and/or performer(s);
iii. publicity and privacy rights pertaining to a person's image or
     likeness depicted in a Work;
 iv. rights protecting against unfair competition in regards to a Work,
     subject to the limitations in paragraph 4(a), below;
  v. rights protecting the extraction, dissemination, use and reuse of data
     in a Work;
 vi. database rights (such as those arising under Directive 96/9/EC of the
     European Parliament and of the Council of 11 March 1996 on the legal
     protection of databases, and under any national implementation
     thereof, including any amended or successor version of such
     directive); and
vii. other similar, equivalent or corresponding rights throughout the
     world based on applicable law or treaty, and any national
     implementations thereof.

2. Waiver. To the greatest extent permitted by, but not in contravention
of, applicable law, Affirmer hereby overtly, fully, permanently,
irrevocably and unconditionally waives, abandons, and surrenders all of
Affirmer's Copyright and Related Rights and associated claims and causes
of action, whether now known or unknown (including existing as well as
future claims and causes of action), in the Work (i) in all territories
worldwide, (ii) for the maximum duration provided by applicable law or
treaty (including future time extensions), (iii) in any current or future
medium and for any number of copies, and (iv) for any purpose whatsoever,
including without limitation commercial, advertising or promotional
purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
member of the public at large and to the detriment of Affirmer's heirs and
successors, fully intending that such Waiver shall not be subject to
revocation, rescission, cancellation, termination, or any other legal or
equitable action to disrupt the quiet enjoyment of the Work by the public
as contemplated by Affirmer's express Statement of Purpose.

3. Public License Fallback. Should any part of the Waiver for any reason
be judged legally invalid or ineffective under applicable law, then the
Waiver shall be preserved to the maximum extent permitted taking into
account Affirmer's express Statement of Purpose. In addition, to the
extent the Waiver is so judged Affirmer hereby grants to each affected
person a royalty-free, non transferable, non sublicensable, non exclusive,
irrevocable and unconditional license to exercise Affirmer's Copyright and
Related Rights in the Work (i) in all territories worldwide, (ii) for the
maximum duration provided by applicable law or treaty (including future
time extensions), (iii) in any current or future medium and for any number
of copies, and (iv) for any purpose whatsoever, including without
limitation commercial, advertising or promotional purposes (the
"License"). The License shall be deemed effective as of the date CC0 was
applied by Affirmer to the Work. Should any part of the License for any
reason be judged legally invalid or ineffective under applicable law, such
partial invalidity or ineffectiveness shall not invalidate the remainder
of the License, and in such case Affirmer hereby affirms that he or she
will not (i) exercise any of his or her remaining Copyright and Related
Rights in the Work or (ii) assert any associated claims and causes of
action with respect to the Work, in either case contrary to Affirmer's
express Statement of Purpose.

4. Limitations and Disclaimers.

 a. No trademark or patent rights held by Affirmer are waived, abandoned,
    surrendered, licensed or otherwise affected by this document.
 b. Affirmer offers the Work as-is and makes no representations or
    warranties of any kind concerning the Work, express, implied,
    statutory or otherwise, including without limitation warranties of
    title, merchantability, fitness for a particular purpose, non
    infringement, or the absence of latent or other defects, accuracy, or
    the present or absence of errors, whether or not discoverable, all to
    the greatest extent permissible under applicable law.
 c. Affirmer disclaims responsibility for clearing rights of other persons
    that may apply to the Work or any use thereof, including without
    limitation any person's Copyright and Related Rights in the Work.
    Further, Affirmer disclaims responsibility for obtaining any necessary
    consents, permissions or other rights required for any use of the
    Work.
 d. Affirmer understands and acknowledges that Creative Commons is not a
    party to this document and has no duty or obligation with respect to
    this CC0 or use of the Work.

```

### requirements.txt

```
packaging==25.0
PySide6==6.10.1
PySide6_Addons==6.10.1
PySide6_Essentials==6.10.1
QtPy==2.4.3
shiboken6==6.10.1

```

---

**End of DynastyVizualizer Codebase Snapshot**

- **Files**: 10 implemented / 94 total
- **Lines**: 1,146 code / 4,058 total
- **Generated**: 2025-12-13 15:14:34
