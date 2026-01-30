"""Test script to verify TreeCanvas and all Phase 3 components work correctly.

Creates a temporary database with sample family data and launches the tree view.
"""

import os
import sys
import tempfile

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt


def create_test_database():
    """Create a temporary .dyn database with sample family data."""
    import sqlite3

    fd, path = tempfile.mkstemp(suffix=".dyn")
    os.close(fd)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create schema (minimal tables needed)
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Family (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_name TEXT NOT NULL DEFAULT '',
            notes TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS Person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL DEFAULT '',
            middle_name TEXT DEFAULT '',
            last_name TEXT NOT NULL DEFAULT '',
            maiden_name TEXT DEFAULT '',
            nickname TEXT DEFAULT '',
            gender TEXT DEFAULT 'Unknown',
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
            family_id INTEGER DEFAULT 1,
            dynasty_id INTEGER DEFAULT 1,
            is_founder INTEGER DEFAULT 0,
            education INTEGER DEFAULT 0,
            is_favorite INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            FOREIGN KEY (father_id) REFERENCES Person(id),
            FOREIGN KEY (mother_id) REFERENCES Person(id),
            FOREIGN KEY (family_id) REFERENCES Family(id)
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
            dissolution_reason TEXT DEFAULT '',
            marriage_type TEXT DEFAULT 'Marriage',
            notes TEXT DEFAULT '',
            FOREIGN KEY (spouse1_id) REFERENCES Person(id),
            FOREIGN KEY (spouse2_id) REFERENCES Person(id)
        );

        CREATE TABLE IF NOT EXISTS Portrait (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            image_path TEXT DEFAULT '',
            is_primary INTEGER DEFAULT 0,
            display_order INTEGER DEFAULT 0,
            FOREIGN KEY (person_id) REFERENCES Person(id)
        );

        CREATE TABLE IF NOT EXISTS Event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            event_type TEXT DEFAULT '',
            event_name TEXT DEFAULT '',
            start_year INTEGER,
            start_month INTEGER,
            start_day INTEGER,
            end_year INTEGER,
            end_month INTEGER,
            end_day INTEGER,
            description TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES Person(id)
        );

        CREATE TABLE IF NOT EXISTS MajorEvent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT DEFAULT '',
            event_year INTEGER,
            event_month INTEGER,
            event_day INTEGER,
            description TEXT DEFAULT '',
            dynasty_id INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS Dynasty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dynasty_name TEXT NOT NULL DEFAULT '',
            notes TEXT DEFAULT ''
        );

        INSERT INTO Dynasty (dynasty_name) VALUES ('Test Dynasty');
        INSERT INTO Family (family_name) VALUES ('Test Family');
    """)

    # --- Sample People ---
    # Generation 0 (founders)
    cursor.execute(
        "INSERT INTO Person (first_name, last_name, gender, birth_year, death_year, is_founder, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("John", "Smith", "Male", 1920, 1995, 1, 1),
    )
    john_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO Person (first_name, last_name, maiden_name, gender, birth_year, death_year, is_founder, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("Mary", "Smith", "Jones", "Female", 1922, 1998, 1, 1),
    )
    mary_id = cursor.lastrowid

    # Generation 1 (children of John & Mary)
    cursor.execute(
        "INSERT INTO Person (first_name, last_name, gender, birth_year, father_id, mother_id, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Robert", "Smith", "Male", 1945, john_id, mary_id, 1),
    )
    robert_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO Person (first_name, last_name, maiden_name, gender, birth_year, father_id, mother_id, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("Susan", "Smith", "Smith", "Female", 1948, john_id, mary_id, 1),
    )
    susan_id = cursor.lastrowid

    # Spouse for Robert (married in)
    cursor.execute(
        "INSERT INTO Person (first_name, last_name, maiden_name, gender, birth_year, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        ("Linda", "Smith", "Brown", "Female", 1947, 1),
    )
    linda_id = cursor.lastrowid

    # Generation 2 (children of Robert & Linda)
    cursor.execute(
        "INSERT INTO Person (first_name, last_name, gender, birth_year, father_id, mother_id, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("David", "Smith", "Male", 1970, robert_id, linda_id, 1),
    )
    david_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO Person (first_name, last_name, gender, birth_year, father_id, mother_id, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Emily", "Smith", "Female", 1973, robert_id, linda_id, 1),
    )
    emily_id = cursor.lastrowid

    # Single parent edge case: Susan has a child but no recorded spouse
    cursor.execute(
        "INSERT INTO Person (first_name, last_name, gender, birth_year, mother_id, family_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        ("James", "Wilson", "Male", 1975, susan_id, 1),
    )
    james_id = cursor.lastrowid

    # --- Marriages ---
    cursor.execute(
        "INSERT INTO Marriage (spouse1_id, spouse2_id, marriage_year) VALUES (?, ?, ?)",
        (john_id, mary_id, 1940),
    )

    cursor.execute(
        "INSERT INTO Marriage (spouse1_id, spouse2_id, marriage_year) VALUES (?, ?, ?)",
        (robert_id, linda_id, 1968),
    )

    conn.commit()

    print(f"Created test database: {path}")
    print(f"  People: John({john_id}), Mary({mary_id}), Robert({robert_id}), "
          f"Susan({susan_id}), Linda({linda_id}), David({david_id}), "
          f"Emily({emily_id}), James({james_id})")
    print(f"  Marriages: John+Mary, Robert+Linda")
    print(f"  Single parent: Susan -> James (no marriage node)")

    return path, conn


def main():
    app = QApplication(sys.argv)

    db_path, conn = create_test_database()

    # Create a minimal DatabaseManager-like object
    from database.db_manager import DatabaseManager

    class FakeMainWindow:
        """Minimal stand-in for MainWindow so DatabaseManager can init."""
        pass

    db = DatabaseManager(FakeMainWindow())  # type: ignore[arg-type]
    db.conn = conn
    db.conn.row_factory = __import__("sqlite3").Row
    db.file_path = db_path

    # Build the test window
    from views.tree_view.tree_canvas import TreeCanvas

    window = QMainWindow()
    window.setWindowTitle("TreeCanvas Test")
    window.resize(1200, 800)

    central = QWidget()
    layout = QVBoxLayout(central)
    layout.setContentsMargins(0, 0, 0, 0)

    # Toolbar
    toolbar = QHBoxLayout()
    btn_rebuild = QPushButton("Rebuild Scene")
    btn_fit = QPushButton("Zoom to Fit")
    toolbar.addWidget(btn_rebuild)
    toolbar.addWidget(btn_fit)
    toolbar.addStretch()
    layout.addLayout(toolbar)

    # Canvas
    canvas = TreeCanvas(db, central)
    layout.addWidget(canvas)

    btn_rebuild.clicked.connect(canvas.rebuild_scene)
    btn_fit.clicked.connect(canvas.zoom_to_fit)

    canvas.person_selected.connect(lambda pid: print(f"Selected person: {pid}"))
    canvas.person_double_clicked.connect(lambda pid: print(f"Double-clicked person: {pid}"))
    canvas.marriage_double_clicked.connect(lambda mid: print(f"Double-clicked marriage: {mid}"))

    window.setCentralWidget(central)

    # Build the scene
    print("\nBuilding tree scene...")
    canvas.rebuild_scene()
    print("Scene built successfully!")
    print(f"  Person boxes: {len(canvas._person_boxes)}")
    print(f"  Marriage nodes: {len(canvas._marriage_nodes)}")
    print(f"  Relationship lines: {len(canvas._relationship_lines)}")
    print(f"  Generation bands: {len(canvas._generation_bands)}")

    window.show()
    canvas.zoom_to_fit()

    print("\nTree canvas is displayed. Close the window to exit.")
    print("  - Scroll wheel to zoom")
    print("  - Click and drag to pan")
    print("  - Double-click a person box to emit signal")

    exit_code = app.exec()

    # Cleanup
    conn.close()
    os.remove(db_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
