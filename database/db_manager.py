"""Manages SQLite-based .dyn dynasty database files."""

from __future__ import annotations

import sqlite3
import shutil
import os
from typing import TYPE_CHECKING

from utils.date_formatter import DateFormatter

if TYPE_CHECKING:
    from main import MainWindow


class DatabaseManager:
    """Manages SQLite-based .dyn dynasty database files."""

    def __init__(self, parent: MainWindow) -> None:
        """Initialize database manager with parent window reference."""
        self.parent: MainWindow = parent
        self.conn: sqlite3.Connection | None = None
        self.file_path: str | None = None
        self._temp_file_path: str | None = None
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
        return os.path.basename(self.file_path) if self.file_path else None

    @property
    def database_directory(self) -> str | None:
        """Get the directory path of the current database."""
        return os.path.dirname(self.file_path) if self.file_path else None

    @property
    def has_file_path(self) -> bool:
        """Check if database has an associated file path."""
        return self.file_path is not None

    # ------------------------------------------------------------------
    # Database Lifecycle
    # ------------------------------------------------------------------

    def new_database(self, file_path: str) -> None:
        """Create a brand-new .dyn file with the dynasty schema."""
        if os.path.exists(file_path):
            os.remove(file_path)
        
        self._connect_to_database(file_path)
        self._initialize_schema()
        self._unsaved_changes = False

    def open_database(self, file_path: str) -> None:
        """Open an existing .dyn database file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Database file not found: {file_path}")
        
        self._connect_to_database(file_path)
        self._migrate_schema()
        self._unsaved_changes = False

    def save_database(self, path: str | None = None) -> bool:
        """Save database, optionally to a new path."""
        if self.conn is None:
            raise RuntimeError("Cannot save: no database connection")
        
        if path is None:
            self.conn.commit()
            self._unsaved_changes = False
            return True
        
        self._save_to_new_path(path)
        return True

    def close(self) -> None:
        """Close the current database connection and reset state."""
        if self.conn:
            self.conn.close()
        self.conn = None
        self.file_path = None
        self._unsaved_changes = False

    # ------------------------------------------------------------------
    # State Management
    # ------------------------------------------------------------------

    def mark_dirty(self) -> None:
        """Mark the database as having unsaved changes."""
        if self.conn is not None:
            self._unsaved_changes = True

    def mark_clean(self) -> None:
        """Mark the database as having no unsaved changes."""
        self._unsaved_changes = False

    # ------------------------------------------------------------------
    # Connection Management
    # ------------------------------------------------------------------

    def _connect_to_database(self, file_path: str) -> None:
        """Establish connection to database file with proper configuration."""
        try:
            self.conn = sqlite3.connect(file_path)
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to connect to database: {e}") from e
        
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.file_path = file_path

    def _save_to_new_path(self, new_path: str) -> None:
        """Save database to a new file path."""
        if self.conn is None:
            raise RuntimeError("Cannot save: no database connection")
        
        self.conn.commit()
        current_path: str | None = self.file_path or self._temp_file_path
        
        if not current_path or not os.path.exists(current_path):
            raise RuntimeError("Cannot save: no source database file")
        
        self.conn.close()
        shutil.copy2(current_path, new_path)
        
        self._connect_to_database(new_path)
        self._unsaved_changes = False

    # ------------------------------------------------------------------
    # Schema Initialization
    # ------------------------------------------------------------------

    def _initialize_schema(self) -> None:
        """Create all required tables for a new dynasty database."""
        if self.conn is None:
            raise RuntimeError("Cannot initialize schema: no database connection")
        
        cursor: sqlite3.Cursor = self.conn.cursor()
        cursor.executescript(self._get_schema_sql())
        self.conn.commit()

    @staticmethod
    def _get_schema_sql() -> str:
        """Get the complete database schema as SQL."""
        return """
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
            is_favorite INTEGER DEFAULT 0,
            notes TEXT,
            FOREIGN KEY(father_id) REFERENCES Person(id) ON DELETE SET NULL,
            FOREIGN KEY(mother_id) REFERENCES Person(id) ON DELETE SET NULL,
            FOREIGN KEY(family_id) REFERENCES Family(id) ON DELETE SET NULL
        );

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
            notes TEXT,
            FOREIGN KEY(spouse1_id) REFERENCES Person(id)
                ON UPDATE CASCADE ON DELETE SET NULL,
            FOREIGN KEY(spouse2_id) REFERENCES Person(id)
                ON UPDATE CASCADE ON DELETE SET NULL
        );

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

        CREATE TABLE IF NOT EXISTS PersonPosition (
            person_id INTEGER PRIMARY KEY,
            view_type TEXT NOT NULL,
            x_position REAL NOT NULL,
            y_position REAL NOT NULL,
            FOREIGN KEY(person_id) REFERENCES Person(id) ON DELETE CASCADE
        );
        """
    
    # ------------------------------------------------------------------
    # Schema Migration
    # ------------------------------------------------------------------
    
    def _migrate_schema(self) -> None:
        """Migrate existing database schema to latest version."""
        if self.conn is None:
            raise RuntimeError("Cannot migrate schema: no database connection")
        
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        self._migrate_person_table(cursor)
        self._migrate_marriage_table(cursor)
        self._migrate_event_table_data(cursor)
        self._migrate_person_table_data(cursor)
        self._migrate_marriage_table_data(cursor)

        self.conn.commit()
    
    def _migrate_person_table(self, cursor: sqlite3.Cursor) -> None:
        """Apply Person table schema migrations."""
        existing_columns: set[str] = self._get_table_columns(cursor, "Person")
        
        migrations: list[tuple[str, str]] = [
            ("middle_name", "ALTER TABLE Person ADD COLUMN middle_name TEXT DEFAULT ''"),
            ("nickname", "ALTER TABLE Person ADD COLUMN nickname TEXT DEFAULT ''"),
            ("dynasty_id", "ALTER TABLE Person ADD COLUMN dynasty_id INTEGER DEFAULT 1"),
            ("is_founder", "ALTER TABLE Person ADD COLUMN is_founder INTEGER DEFAULT 0"),
            ("education", "ALTER TABLE Person ADD COLUMN education INTEGER DEFAULT 0"),
            ("is_favorite", "ALTER TABLE Person ADD COLUMN is_favorite INTEGER DEFAULT 0"),
        ]
        
        self._apply_column_migrations(cursor, existing_columns, migrations)
    
    def _migrate_marriage_table(self, cursor: sqlite3.Cursor) -> None:
        """Apply Marriage table schema migrations."""
        existing_columns: set[str] = self._get_table_columns(cursor, "Marriage")
        
        migrations: list[tuple[str, str]] = [
            ("notes", "ALTER TABLE Marriage ADD COLUMN notes TEXT"),
        ]
        
        self._apply_column_migrations(cursor, existing_columns, migrations)

    def _migrate_event_table_data(self, cursor: sqlite3.Cursor) -> None:
        """Normalize Event table month data."""
        self._normalize_month_columns(
            cursor,
            table="Event",
            id_column="id",
            month_columns=["start_month", "end_month"],
        )
    
    def _migrate_person_table_data(self, cursor: sqlite3.Cursor) -> None:
        """Normalize Person table month data."""
        self._normalize_month_columns(
            cursor,
            table="Person",
            id_column="id",
            month_columns=["birth_month", "death_month", "arrival_month", "moved_out_month"],
        )

    def _migrate_marriage_table_data(self, cursor: sqlite3.Cursor) -> None:
        """Normalize Marriage table month data."""
        self._normalize_month_columns(
            cursor,
            table="Marriage",
            id_column="id",
            month_columns=["marriage_month", "dissolution_month"],
        )
    
    # ------------------------------------------------------------------
    # Migration Utilities
    # ------------------------------------------------------------------

    def _normalize_month_columns(
        self,
        cursor: sqlite3.Cursor,
        *,
        table: str,
        id_column: str,
        month_columns: list[str],
    ) -> None:
        """Normalize month columns to integer values for a table."""
        columns_list: list[str] = [id_column] + month_columns
        columns_str: str = ", ".join(columns_list)
        where_clause: str = " OR ".join(f"{col} IS NOT NULL" for col in month_columns)

        cursor.execute(f"SELECT {columns_str} FROM {table} WHERE {where_clause}")

        for row in cursor.fetchall():
            row_id: int = row[id_column]
            updates: dict[str, int | None] = {
                col: DateFormatter.normalize_month(row[col]) for col in month_columns
            }

            set_clause: str = ", ".join(f"{col} = ?" for col in updates)
            values: list[int | None] = list(updates.values()) + [row_id]

            cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)
    
    @staticmethod
    def _get_table_columns(cursor: sqlite3.Cursor, table_name: str) -> set[str]:
        """Get set of column names for a table."""
        cursor.execute(f"PRAGMA table_info({table_name})")
        return {row[1] for row in cursor.fetchall()}
    
    @staticmethod
    def _apply_column_migrations(
        cursor: sqlite3.Cursor,
        existing_columns: set[str],
        migrations: list[tuple[str, str]],
    ) -> None:
        """Apply column addition migrations if columns don't exist."""
        for column_name, sql in migrations:
            if column_name not in existing_columns:
                cursor.execute(sql)