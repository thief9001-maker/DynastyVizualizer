"""Test script to visualize PersonBox widgets."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtGui import QBrush, QColor, QPainter


class TestWindow(QMainWindow):
    """Simple test window to display PersonBox widgets."""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("PersonBox Test")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setBackgroundBrush(QBrush(QColor(240, 240, 240)))
        
        layout.addWidget(self.view)
        
        self._add_test_person_boxes()
    
    def _add_test_person_boxes(self):
        """Add a few PersonBox widgets to test the display."""
        if not self.db or not self.db.conn:
            print("No database connection!")
            return
        
        # Import here to avoid issues
        from views.tree_view.person_box import PersonBox
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM Person LIMIT 6")
        people = cursor.fetchall()
        
        x = 50
        y = 50
        spacing_x = 320
        spacing_y = 150
        
        for i, person_row in enumerate(people):
            person_id = person_row['id']
            
            person_box = PersonBox(person_id, self.db)
            
            # Connect signals
            person_box.person_double_clicked.connect(self.on_person_double_clicked)
            person_box.person_selected.connect(self.on_person_selected)
            
            col = i % 3
            row = i // 3
            person_box.setPos(x + col * spacing_x, y + row * spacing_y)
            
            self.scene.addItem(person_box)
        
        self.scene.setSceneRect(0, 0, 1100, 600)
    
    def on_person_double_clicked(self, person_id: int):
        """Handle person double-click."""
        print(f"Double-clicked person ID: {person_id}")
    
    def on_person_selected(self, person_id: int):
        """Handle person selection."""
        print(f"Selected person ID: {person_id}")


if __name__ == "__main__":
    print("PersonBox Test")
    print("-" * 50)
    
    db_file = r"D:\Programs\DynastyVizualizer\Struggberg Family Tree 1.dyn"
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager(None)
    db.open_database(db_file)
    
    app = QApplication(sys.argv)
    window = TestWindow(db)
    window.show()
    sys.exit(app.exec())
    
    from database.db_manager import DatabaseManager
    
    db = DatabaseManager(None)
    db.open_database(db_file)
    
    app = QApplication(sys.argv)
    window = TestWindow(db)
    window.show()
    sys.exit(app.exec())