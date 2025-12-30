"""Main application window for Dynasty Visualizer."""

import sys, os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMessageBox,
    QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from database.db_manager import DatabaseManager
from actions import FileActions, EditActions, ViewActions, ToolsActions, HelpActions, SettingsActions
from commands.undo_redo_manager import UndoRedoManager
from utils.settings_manager import SettingsManager


class MainWindow(QMainWindow):
    """Main application window for Dynasty Visualizer."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Dynasty Visualizer")
        self.resize(1000, 700)

        self.db = DatabaseManager(self)
        self.undo_manager = UndoRedoManager()
        self.settings_manager = SettingsManager()

        self.file_actions = FileActions(self)
        self.edit_actions = EditActions(self)
        self.view_actions = ViewActions(self)
        self.tools_actions = ToolsActions(self)
        self.settings_actions = SettingsActions(self)
        self.help_actions = HelpActions(self)

        self._setup_central_widget()
        self._create_menus()
        self._connect_actions()
        
        self._create_untitled_database()

        self._show_family_trees()
        
        self._update_window_title()
        self._update_menu_states()

    def _create_untitled_database(self) -> None:
        """Create a temporary database for new sessions."""
        import tempfile
        
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "dynasty_untitled.dyn")
        
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        
        self.db.new_database(temp_file)

        self.db._temp_file_path = temp_file
        self.db.file_path = None
        
        self.refresh_ui()

    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------

    def _setup_central_widget(self) -> None:
        """Setup the central widget with stacked views."""
        self.view_stack = QStackedWidget()
        self.setCentralWidget(self.view_stack)
        
        self.genealogy_view = None
        self.timeline_view = None
        self.dynasty_view = None
        self.data_table_view = None

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
        """Create the File menu."""
        file_menu = menubar.addMenu("File")

        self.action_new_dynasty = QAction("New Dynasty", self)
        self.action_new_dynasty.setObjectName("file.new")
        self.action_new_dynasty.setShortcut(self.settings_manager.get_shortcut("file.new"))

        self.action_open_dynasty = QAction("Open Dynasty", self)
        self.action_open_dynasty.setObjectName("file.open")
        self.action_open_dynasty.setShortcut(self.settings_manager.get_shortcut("file.open"))

        file_menu.addAction(self.action_new_dynasty)
        file_menu.addAction(self.action_open_dynasty)

        self.recent_files_menu = file_menu.addMenu("Recent Files")
        self._update_recent_files_menu()
        
        file_menu.addSeparator()

        self.action_save = QAction("Save", self)
        self.action_save.setObjectName("file.save")
        self.action_save.setShortcut(self.settings_manager.get_shortcut("file.save"))
        
        self.action_save_as = QAction("Save As", self)
        self.action_save_as.setObjectName("file.save_as")
        self.action_save_as.setShortcut(self.settings_manager.get_shortcut("file.save_as"))

        file_menu.addAction(self.action_save)
        file_menu.addAction(self.action_save_as)
        file_menu.addSeparator()

        self.action_exit = QAction("Exit", self)
        self.action_exit.setObjectName("file.exit")
        self.action_exit.setShortcut(self.settings_manager.get_shortcut("file.exit"))
        
        file_menu.addAction(self.action_exit)

    def _create_edit_menu(self, menubar: QMenuBar) -> None:
        """Create the Edit menu."""
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

        self.action_edit_person = QAction("Edit Person", self)
        self.action_edit_person.setObjectName("edit.edit_person")
        self.action_edit_person.setShortcut("Ctrl+E")  # Add to settings_manager later

        self.action_remove_person = QAction("Remove Person", self)
        self.action_remove_person.setObjectName("edit.remove_person")
        self.action_remove_person.setShortcut(self.settings_manager.get_shortcut("edit.remove_person"))

        self.action_add_new_family = QAction("Add New Family", self)
        self.action_add_new_family.setObjectName("edit.add_new_family")
        self.action_add_new_family.setShortcut(self.settings_manager.get_shortcut("edit.add_new_family"))
        self.action_add_new_family.setEnabled(False)  # Disabled for now

        edit_menu.addAction(self.action_undo)
        edit_menu.addAction(self.action_redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.action_add_person)
        edit_menu.addAction(self.action_edit_person)
        edit_menu.addAction(self.action_remove_person)
        edit_menu.addSeparator()
        edit_menu.addAction(self.action_add_new_family)

        self.edit_actions.undo_action = self.action_undo
        self.edit_actions.redo_action = self.action_redo
        self.edit_actions.update_undo_redo_actions()

    def _create_view_menu(self, menubar: QMenuBar) -> None:
        """Create the View menu."""
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
        """Create the Tools menu."""
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
        """Create the Settings menu."""
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
        """Create the Help menu."""
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
        self.action_new_dynasty.triggered.connect(self.file_actions.new_dynasty)
        self.action_open_dynasty.triggered.connect(self.file_actions.open_dynasty)
        self.action_save.triggered.connect(self.file_actions.save)
        self.action_save_as.triggered.connect(self.file_actions.save_as)
        self.action_exit.triggered.connect(self.file_actions.exit_app)

        self.action_undo.triggered.connect(self.edit_actions.undo)
        self.action_redo.triggered.connect(self.edit_actions.redo)
        self.action_add_person.triggered.connect(self.edit_actions.add_person)
        self.action_edit_person.triggered.connect(self._edit_selected_person)
        self.action_remove_person.triggered.connect(self.edit_actions.remove_person)
        self.action_add_new_family.triggered.connect(self.edit_actions.add_new_family)

        self.action_view_family_trees.triggered.connect(self._show_family_trees)
        self.action_view_timeline.triggered.connect(self._show_timeline)
        self.action_view_dynasty.triggered.connect(self._show_dynasty)
        self.action_view_data_table.triggered.connect(self._show_data_table)

        self.action_rebuild_scene.triggered.connect(self.tools_actions.rebuild_scene)
        self.action_recompute_generations.triggered.connect(self.tools_actions.recompute_generations)
        self.action_validate_marriages.triggered.connect(self.tools_actions.validate_marriages)
        self.action_validate_parentage.triggered.connect(self.tools_actions.validate_parentage)

        self.action_settings.triggered.connect(self.settings_actions.settings)
        self.action_general.triggered.connect(self.settings_actions.general)
        self.action_shortcuts.triggered.connect(self.settings_actions.shortcuts)
        self.action_display.triggered.connect(self.settings_actions.display)
        self.action_appearance.triggered.connect(self.settings_actions.appearance)
        self.action_formats.triggered.connect(self.settings_actions.formats)

        self.action_about.triggered.connect(self.help_actions.about)

    # ------------------------------------------------------------------
    # Recent Files Management
    # ------------------------------------------------------------------

    def _update_recent_files_menu(self) -> None:
        """Update the Recent Files submenu with current list."""
        self.recent_files_menu.clear()
        
        recent = self.settings_manager.get_recent_files()
        
        if recent:
            for path in recent:
                filename = os.path.basename(path)
                action = QAction(filename, self)
                action.setData(path)
                action.triggered.connect(lambda checked, p=path: self._open_recent_file(p))
                self.recent_files_menu.addAction(action)
            
            self.recent_files_menu.addSeparator()
            
            clear_action = QAction("Clear Recent Files", self)
            clear_action.triggered.connect(self._clear_recent_files)
            self.recent_files_menu.addAction(clear_action)
        else:
            no_recent = QAction("(No Recent Files)", self)
            no_recent.setEnabled(False)
            self.recent_files_menu.addAction(no_recent)

    def _open_recent_file(self, path: str) -> None:
        """Open a file from recent files list."""
        if not os.path.exists(path):
            QMessageBox.warning(
                self,
                "File Not Found",
                f"The file '{path}' no longer exists."
            )
            self._remove_from_recent_files(path)
            return
        
        try:
            self.db.open_database(path)
            self.refresh_ui()
            self.file_actions._refresh_all_views()
            self.settings_manager.add_recent_file(path)
            self._update_recent_files_menu()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{str(e)}")

    def _remove_from_recent_files(self, path: str) -> None:
        """Remove a file from recent files list."""
        recent = self.settings_manager.get_recent_files()
        if path in recent:
            recent.remove(path)
            self.settings_manager.clear_recent_files()
            for p in recent:
                self.settings_manager.add_recent_file(p)
        self._update_recent_files_menu()

    def _clear_recent_files(self) -> None:
        """Clear the recent files list."""
        self.settings_manager.clear_recent_files()
        self._update_recent_files_menu()

    # ------------------------------------------------------------------
    # View Management
    # ------------------------------------------------------------------

    def _show_family_trees(self) -> None:
        """Switch to family trees view."""
        if self.genealogy_view is None:
            genealogy_placeholder = QLabel("Genealogy View\n(Coming Soon!)")
            genealogy_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            genealogy_placeholder.setStyleSheet("font-size: 24px; color: gray;")
            self.genealogy_view = genealogy_placeholder
            self.view_stack.addWidget(self.genealogy_view)
        
        self.view_stack.setCurrentWidget(self.genealogy_view)

    def _show_timeline(self) -> None:
        """Switch to timeline view."""
        if self.timeline_view is None:
            timeline_placeholder = QLabel("Timeline View\n(Coming Soon!)")
            timeline_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            timeline_placeholder.setStyleSheet("font-size: 24px; color: gray;")
            self.timeline_view = timeline_placeholder
            self.view_stack.addWidget(self.timeline_view)
        
        self.view_stack.setCurrentWidget(self.timeline_view)

    def _show_dynasty(self) -> None:
        """Switch to dynasty view."""
        if self.dynasty_view is None:
            dynasty_placeholder = QLabel("Dynasty View\n(Coming Soon!)")
            dynasty_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dynasty_placeholder.setStyleSheet("font-size: 24px; color: gray;")
            self.dynasty_view = dynasty_placeholder
            self.view_stack.addWidget(self.dynasty_view)
        
        self.view_stack.setCurrentWidget(self.dynasty_view)

    def _show_data_table(self) -> None:
        """Switch to data table view."""
        if self.data_table_view is None:
            from views.data_table_view import DataTableView
            self.data_table_view = DataTableView(self.db, self)
            self.view_stack.addWidget(self.data_table_view)
        
        self.data_table_view.refresh_data()
        self.view_stack.setCurrentWidget(self.data_table_view)

    def _edit_selected_person(self) -> None:
        """Edit the currently selected person in the active view."""
        if self.data_table_view and self.view_stack.currentWidget() == self.data_table_view:
            self.data_table_view._edit_selected_person()
        else:
            QMessageBox.information(
                self,
                "Edit Person",
                "Please select a person to edit."
            )

    # ------------------------------------------------------------------
    # UI Update Methods
    # ------------------------------------------------------------------

    def _update_window_title(self) -> None:
        """Update the window title to reflect current database state."""
        if self.db.is_open:
            if self.db.file_path is None:
                title = "Dynasty Visualizer - Untitled *"
            else:
                dirty_marker = " *" if self.db.is_dirty else ""
                title = f"Dynasty Visualizer - {self.db.database_name}{dirty_marker}"
            self.setWindowTitle(title)
        else:
            self.setWindowTitle("Dynasty Visualizer")

    def _update_menu_states(self) -> None:
        """Enable or disable menu items based on current state."""
        has_db = self.db.is_open

        # Always allow Save/Save As even for untitled
        self.action_save.setEnabled(has_db)
        self.action_save_as.setEnabled(has_db)

        self.action_undo.setEnabled(self.undo_manager.can_undo())
        self.action_redo.setEnabled(self.undo_manager.can_redo())
        self.action_add_person.setEnabled(has_db)
        self.action_edit_person.setEnabled(has_db)
        self.action_remove_person.setEnabled(has_db)

        self.action_view_family_trees.setEnabled(has_db)
        self.action_view_timeline.setEnabled(has_db)
        self.action_view_dynasty.setEnabled(has_db)
        self.action_view_data_table.setEnabled(has_db)

        self.action_rebuild_scene.setEnabled(has_db)
        self.action_recompute_generations.setEnabled(has_db)
        self.action_validate_marriages.setEnabled(has_db)
        self.action_validate_parentage.setEnabled(has_db)

    def refresh_ui(self) -> None:
        """Refresh window title and menu states after database changes."""
        self._update_window_title()
        self._update_menu_states()

    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if self.db.is_open and self.db.is_dirty:
            msg = QMessageBox(self)
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("You have unsaved changes. Do you want to save before exiting?")
            msg.setStandardButtons(
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            choice = msg.exec()
            
            if choice == QMessageBox.StandardButton.Save:
                if self.file_actions.save():
                    event.accept()
                else:
                    event.ignore()
            elif choice == QMessageBox.StandardButton.Discard:
                event.accept()
            else: 
                event.ignore()
        else:
            event.accept()


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()