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
