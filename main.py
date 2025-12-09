import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PySide6.QtGui import QAction

from database.db_manager import DatabaseManager
from actions import FileActions, EditActions, ViewActions, ToolsActions, HelpActions, SettingsActions
from commands.undo_redo_manager import UndoRedoManager
from utils.settings_manager import SettingsManager

class MainWindow(QMainWindow):
    """Main application window for Dynasty Visualizer."""

    def __init__(self) -> None:
        """Initialize the main window and all UI components."""
        super().__init__()

        self.setWindowTitle("Dynasty Visualizer")
        self.resize(1000, 700)

        # Initialize database manager
        self.db = DatabaseManager(self)

        # Initialize undo/redo manager
        self.undo_manager = UndoRedoManager()

        # Initialize settings manager
        self.settings_manager = SettingsManager()

        # Create UI elements
        self._create_menus()

        # Initialize action handlers
        self.file_actions = FileActions(self)
        self.edit_actions = EditActions(self)
        self.view_actions = ViewActions(self)
        self.tools_actions = ToolsActions(self)
        self.settings_actions = SettingsActions(self)
        self.help_actions = HelpActions(self)

        # Connect menu actions to handlers
        self._connect_actions()

        # Update window title and menu states
        self._update_window_title()
        self._update_menu_states()

    # ------------------------------------------------------------------
    # UI Creation
    # ------------------------------------------------------------------

    def _create_menus(self) -> None:
        """Create all menu bars and menu items."""
        menubar = self.menuBar()

        self._create_file_menu(menubar)
        self._create_edit_menu(menubar)
        self._create_view_menu(menubar)
        self._create_tools_menu(menubar)
        self._create_settings_menu(menubar)
        self._create_help_menu(menubar)

    def _create_file_menu(self, menubar: QMenuBar) -> None:
        """Create the File menu with all file operations."""
        file_menu = menubar.addMenu("File")

        self.action_new_dynasty = QAction("New Dynasty", self)
        self.action_new_dynasty.setObjectName("file.new")
        self.action_new_dynasty.setShortcut(self.settings_manager.get_shortcut("file.new"))

        self.action_open_dynasty = QAction("Open Dynasty", self)
        self.action_open_dynasty.setObjectName("file.open")
        self.action_open_dynasty.setShortcut(self.settings_manager.get_shortcut("file.open"))

        self.action_save = QAction("Save", self)
        self.action_save.setObjectName("file.save")
        self.action_save.setShortcut(self.settings_manager.get_shortcut("file.save"))
        
        self.action_save_as = QAction("Save As", self)
        self.action_save_as.setObjectName("file.save_as")
        self.action_save_as.setShortcut(self.settings_manager.get_shortcut("file.save_as"))

        self.action_exit = QAction("Exit", self)
        self.action_exit.setObjectName("file.exit")
        self.action_exit.setShortcut(self.settings_manager.get_shortcut("file.exit"))

        file_menu.addAction(self.action_new_dynasty)
        file_menu.addAction(self.action_open_dynasty)
        file_menu.addSeparator()
        file_menu.addAction(self.action_save)
        file_menu.addAction(self.action_save_as)
        file_menu.addSeparator()
        file_menu.addAction(self.action_exit)

    def _create_edit_menu(self, menubar: QMenuBar) -> None:
        """Create the Edit menu with editing operations."""
        edit_menu = menubar.addMenu("Edit")

        self.action_undo = QAction("Undo", self)
        self.action_undo.setObjectName("edit.undo")
        self.action_undo.setShortcut(self.settings_manager.get_shortcut("edit.undo"))

        self.action_redo = QAction("Redo", self)
        self.action_redo.setObjectName("edit.redo")
        self.action_redo.setShortcut(self.settings_manager.get_shortcut("edit.redo"))
        
        self.action_add_person = QAction("Add Person", self)
        self.action_add_person.setObjectName("edit.add_person")
        self.action_add_person.setShortcut(self.settings_manager.get_shortcut("edit.add_person"))

        self.action_remove_person = QAction("Remove Person", self)
        self.action_remove_person.setObjectName("edit.remove_person")
        self.action_remove_person.setShortcut(self.settings_manager.get_shortcut("edit.remove_person"))

        self.action_add_new_family = QAction("Add New Family", self)
        self.action_add_new_family.setObjectName("edit.add_new_family")
        self.action_add_new_family.setShortcut(self.settings_manager.get_shortcut("edit.add_new_family"))

        edit_menu.addAction(self.action_undo)
        edit_menu.addAction(self.action_redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.action_add_person)
        edit_menu.addAction(self.action_remove_person)
        edit_menu.addAction(self.action_add_new_family)

    def _create_view_menu(self, menubar: QMenuBar) -> None:
        """Create the View menu with different visualization options."""
        view_menu = menubar.addMenu("View")

        self.action_view_family_trees = QAction("Family Trees", self)
        self.action_view_family_trees.setObjectName("view.family_trees")
        self.action_view_family_trees.setShortcut(self.settings_manager.get_shortcut("view.family_trees"))

        self.action_view_timeline = QAction("Timeline", self)
        self.action_view_timeline.setObjectName("view.timeline")
        self.action_view_timeline.setShortcut(self.settings_manager.get_shortcut("view.timeline"))
        
        self.action_view_dynasty = QAction("Dynasty", self)
        self.action_view_dynasty.setObjectName("view.dynasty")
        self.action_view_dynasty.setShortcut(self.settings_manager.get_shortcut("view.dynasty"))

        self.action_view_data_table = QAction("Data Table", self)
        self.action_view_data_table.setObjectName("view.data_table")
        self.action_view_data_table.setShortcut(self.settings_manager.get_shortcut("view.data_table"))

        view_menu.addAction(self.action_view_family_trees)
        view_menu.addAction(self.action_view_timeline)
        view_menu.addAction(self.action_view_dynasty)
        view_menu.addAction(self.action_view_data_table)

    def _create_tools_menu(self, menubar: QMenuBar) -> None:
        """Create the Tools menu with utility operations."""
        tools_menu = menubar.addMenu("Tools")

        self.action_rebuild_scene = QAction("Rebuild Scene", self)
        self.action_rebuild_scene.setObjectName("tools.rebuild_scene")
        self.action_rebuild_scene.setShortcut(self.settings_manager.get_shortcut("tools.rebuild_scene"))

        self.action_recompute_generations = QAction("Recompute Generations", self)
        self.action_recompute_generations.setObjectName("tools.recompute_generations")
        self.action_recompute_generations.setShortcut(self.settings_manager.get_shortcut("tools.recompute_generations"))
        
        self.action_validate_marriages = QAction("Validate Marriages", self)
        self.action_validate_marriages.setObjectName("tools.validate_marriages")
        self.action_validate_marriages.setShortcut(self.settings_manager.get_shortcut("tools.validate_marriages"))

        self.action_validate_parentage = QAction("Validate Parentage", self)
        self.action_validate_parentage.setObjectName("tools.validate_parentage")
        self.action_validate_parentage.setShortcut(self.settings_manager.get_shortcut("tools.validate_parentage"))

        tools_menu.addAction(self.action_rebuild_scene)
        tools_menu.addAction(self.action_recompute_generations)
        tools_menu.addAction(self.action_validate_marriages)
        tools_menu.addAction(self.action_validate_parentage)

    def _create_settings_menu(self, menubar: QMenuBar) -> None:
        """Create the settings menu with application options."""
        settings_menu = menubar.addMenu("Settings")

        self.action_settings = QAction("Settings", self)
        self.action_settings.setObjectName("settings.settings")
        self.action_settings.setShortcut(self.settings_manager.get_shortcut("settings.settings"))

        self.action_general = QAction("General", self)
        self.action_general.setObjectName("settings.general")
        self.action_general.setShortcut(self.settings_manager.get_shortcut("settings.general"))

        self.action_shortcuts = QAction("Shortcuts", self)
        self.action_shortcuts.setObjectName("settings.shortcuts")
        self.action_shortcuts.setShortcut(self.settings_manager.get_shortcut("settings.shortcuts"))

        self.action_display = QAction("Display", self)
        self.action_display.setObjectName("settings.display")
        self.action_display.setShortcut(self.settings_manager.get_shortcut("settings.display"))

        self.action_appearance = QAction("Appearance", self)
        self.action_appearance.setObjectName("settings.appearance")
        self.action_appearance.setShortcut(self.settings_manager.get_shortcut("settings.appearance"))

        self.action_formats = QAction("Formats", self)
        self.action_formats.setObjectName("settings.formats")
        self.action_formats.setShortcut(self.settings_manager.get_shortcut("settings.formats"))

        settings_menu.addAction(self.action_settings)
        settings_menu.addSeparator()
        settings_menu.addAction(self.action_general)
        settings_menu.addAction(self.action_shortcuts)
        settings_menu.addAction(self.action_display)
        settings_menu.addAction(self.action_appearance)
        settings_menu.addAction(self.action_formats)


    def _create_help_menu(self, menubar: QMenuBar) -> None:
        """Create the Help menu with application information."""
        help_menu = menubar.addMenu("Help")

        self.action_about = QAction("About", self)
        self.action_about.setObjectName("help.about")
        self.action_about.setShortcut(self.settings_manager.get_shortcut("help.about"))
        help_menu.addAction(self.action_about)

    # ------------------------------------------------------------------
    # Action Connections
    # ------------------------------------------------------------------

    def _connect_actions(self) -> None:
        """Connect all menu actions to their handler methods."""
        # File menu connections
        self.action_new_dynasty.triggered.connect(self.file_actions.new_dynasty)
        self.action_open_dynasty.triggered.connect(self.file_actions.open_dynasty)
        self.action_save.triggered.connect(self.file_actions.save)
        self.action_save_as.triggered.connect(self.file_actions.save_as)
        self.action_exit.triggered.connect(self.file_actions.exit_app)

        # Edit menu connections
        self.action_undo.triggered.connect(self.edit_actions.undo)
        self.action_redo.triggered.connect(self.edit_actions.redo)
        self.action_add_person.triggered.connect(self.edit_actions.add_person)
        self.action_remove_person.triggered.connect(self.edit_actions.remove_person)
        self.action_add_new_family.triggered.connect(self.edit_actions.add_new_family)

        # View menu connections
        self.action_view_family_trees.triggered.connect(self.view_actions.family_trees)
        self.action_view_timeline.triggered.connect(self.view_actions.timeline)
        self.action_view_dynasty.triggered.connect(self.view_actions.dynasty)
        self.action_view_data_table.triggered.connect(self.view_actions.data_table)

        # Tools menu connections
        self.action_rebuild_scene.triggered.connect(self.tools_actions.rebuild_scene)
        self.action_recompute_generations.triggered.connect(self.tools_actions.recompute_generations)
        self.action_validate_marriages.triggered.connect(self.tools_actions.validate_marriages)
        self.action_validate_parentage.triggered.connect(self.tools_actions.validate_parentage)

        # Settings menu connections
        self.action_settings.triggered.connect(self.settings_actions.settings)
        self.action_general.triggered.connect(self.settings_actions.general)
        self.action_shortcuts.triggered.connect(self.settings_actions.shortcuts)
        self.action_display.triggered.connect(self.settings_actions.display)
        self.action_appearance.triggered.connect(self.settings_actions.appearance)
        self.action_formats.triggered.connect(self.settings_actions.formats)

        # Help menu connections
        self.action_about.triggered.connect(self.help_actions.about)

    # ------------------------------------------------------------------
    # UI Update Methods
    # ------------------------------------------------------------------

    def _update_window_title(self) -> None:
        """Update the window title to reflect current database state."""
        if self.db.is_open:
            dirty_marker = " *" if self.db.is_dirty else ""
            self.setWindowTitle(f"Dynasty Visualizer - {self.db.database_name}{dirty_marker}")
        else:
            self.setWindowTitle("Dynasty Visualizer")

    def _update_menu_states(self) -> None:
        """Enable or disable menu items based on current state."""
        has_db = self.db.is_open

        # File menu states
        self.action_save.setEnabled(has_db and self.db.is_dirty)
        self.action_save_as.setEnabled(has_db)

        # Edit menu states (disable if no database open)
        self.action_undo.setEnabled(self.undo_manager.can_undo())
        self.action_redo.setEnabled(self.undo_manager.can_redo())
        self.action_add_person.setEnabled(has_db)
        self.action_remove_person.setEnabled(has_db)
        self.action_add_new_family.setEnabled(has_db)

        # View menu states
        self.action_view_family_trees.setEnabled(has_db)
        self.action_view_timeline.setEnabled(has_db)
        self.action_view_dynasty.setEnabled(has_db)
        self.action_view_data_table.setEnabled(has_db)

        # Tools menu states
        self.action_rebuild_scene.setEnabled(has_db)
        self.action_recompute_generations.setEnabled(has_db)
        self.action_validate_marriages.setEnabled(has_db)
        self.action_validate_parentage.setEnabled(has_db)

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def refresh_ui(self) -> None:
        """Refresh window title and menu states after database changes."""
        self._update_window_title()
        self._update_menu_states()


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()