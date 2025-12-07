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
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.file_path = file_path
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
        CREATE TABLE IF NOT EXISTS Person (
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
        
        CREATE TABLE IF NOT EXISTS Event (
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

        CREATE TABLE IF NOT EXISTS Marriage (
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
        """

        cursor.executescript(schema_sql)
        self.conn.commit()
