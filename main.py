"""Main application window for Dynasty Visualizer."""

from __future__ import annotations

import sys
import os
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMessageBox,
    QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

if TYPE_CHECKING:
    pass

from database.db_manager import DatabaseManager
from actions import FileActions, EditActions, ToolsActions, HelpActions, SettingsActions
from commands.undo_redo_manager import UndoRedoManager
from utils.settings_manager import SettingsManager


class MainWindow(QMainWindow):
    """Main application window for Dynasty Visualizer."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    # Window
    WINDOW_TITLE: str = "Dynasty Visualizer"
    WINDOW_TITLE_UNTITLED: str = "Dynasty Visualizer - Untitled *"
    WINDOW_TITLE_FORMAT: str = "Dynasty Visualizer - {name}{dirty}"
    WINDOW_WIDTH_DEFAULT: int = 1000
    WINDOW_HEIGHT_DEFAULT: int = 700
    
    # Temp Database
    TEMP_DB_NAME: str = "dynasty_untitled.dyn"
    
    # Menu Names
    MENU_FILE: str = "File"
    MENU_EDIT: str = "Edit"
    MENU_VIEW: str = "View"
    MENU_TOOLS: str = "Tools"
    MENU_SETTINGS: str = "Settings"
    MENU_HELP: str = "Help"
    
    # File Menu Actions
    ACTION_TEXT_NEW_DYNASTY: str = "New Dynasty"
    ACTION_TEXT_OPEN_DYNASTY: str = "Open Dynasty"
    ACTION_TEXT_SAVE: str = "Save"
    ACTION_TEXT_SAVE_AS: str = "Save As"
    ACTION_TEXT_EXIT: str = "Exit"
    ACTION_TEXT_RECENT_FILES: str = "Recent Files"
    ACTION_TEXT_CLEAR_RECENT: str = "Clear Recent Files"
    ACTION_TEXT_NO_RECENT: str = "(No Recent Files)"
    
    # Edit Menu Actions
    ACTION_TEXT_UNDO: str = "Undo"
    ACTION_TEXT_REDO: str = "Redo"
    ACTION_TEXT_ADD_PERSON: str = "Add Person"
    ACTION_TEXT_EDIT_PERSON: str = "Edit Person"
    ACTION_TEXT_REMOVE_PERSON: str = "Remove Person"
    ACTION_TEXT_ADD_FAMILY: str = "Add New Family"
    
    # View Menu Actions
    ACTION_TEXT_FAMILY_TREES: str = "Family Trees"
    ACTION_TEXT_TIMELINE: str = "Timeline"
    ACTION_TEXT_DYNASTY: str = "Dynasty"
    ACTION_TEXT_DATA_TABLE: str = "Data Table"
    
    # Tools Menu Actions
    ACTION_TEXT_REBUILD_SCENE: str = "Rebuild Scene"
    ACTION_TEXT_RECOMPUTE_GENERATIONS: str = "Recompute Generations"
    ACTION_TEXT_VALIDATE_MARRIAGES: str = "Validate Marriages"
    ACTION_TEXT_VALIDATE_PARENTAGE: str = "Validate Parentage"
    
    # Settings Menu Actions
    ACTION_TEXT_SETTINGS: str = "Settings"
    ACTION_TEXT_GENERAL: str = "General"
    ACTION_TEXT_SHORTCUTS: str = "Shortcuts"
    ACTION_TEXT_DISPLAY: str = "Display"
    ACTION_TEXT_APPEARANCE: str = "Appearance"
    ACTION_TEXT_FORMATS: str = "Formats"
    
    # Help Menu Actions
    ACTION_TEXT_ABOUT: str = "About"
    
    # Action Object Names
    ACTION_NAME_FILE_NEW: str = "file.new"
    ACTION_NAME_FILE_OPEN: str = "file.open"
    ACTION_NAME_FILE_SAVE: str = "file.save"
    ACTION_NAME_FILE_SAVE_AS: str = "file.save_as"
    ACTION_NAME_FILE_EXIT: str = "file.exit"
    ACTION_NAME_EDIT_UNDO: str = "edit.undo"
    ACTION_NAME_EDIT_REDO: str = "edit.redo"
    ACTION_NAME_EDIT_ADD_PERSON: str = "edit.add_person"
    ACTION_NAME_EDIT_EDIT_PERSON: str = "edit.edit_person"
    ACTION_NAME_EDIT_REMOVE_PERSON: str = "edit.remove_person"
    ACTION_NAME_EDIT_ADD_FAMILY: str = "edit.add_new_family"
    ACTION_NAME_VIEW_FAMILY_TREES: str = "view.family_trees"
    ACTION_NAME_VIEW_TIMELINE: str = "view.timeline"
    ACTION_NAME_VIEW_DYNASTY: str = "view.dynasty"
    ACTION_NAME_VIEW_DATA_TABLE: str = "view.data_table"
    ACTION_NAME_TOOLS_REBUILD: str = "tools.rebuild_scene"
    ACTION_NAME_TOOLS_RECOMPUTE: str = "tools.recompute_generations"
    ACTION_NAME_TOOLS_VALIDATE_MARRIAGES: str = "tools.validate_marriages"
    ACTION_NAME_TOOLS_VALIDATE_PARENTAGE: str = "tools.validate_parentage"
    ACTION_NAME_SETTINGS_SETTINGS: str = "settings.settings"
    ACTION_NAME_SETTINGS_GENERAL: str = "settings.general"
    ACTION_NAME_SETTINGS_SHORTCUTS: str = "settings.shortcuts"
    ACTION_NAME_SETTINGS_DISPLAY: str = "settings.display"
    ACTION_NAME_SETTINGS_APPEARANCE: str = "settings.appearance"
    ACTION_NAME_SETTINGS_FORMATS: str = "settings.formats"
    ACTION_NAME_HELP_ABOUT: str = "help.about"
    
    # Shortcuts (Temporary - will move to settings)
    SHORTCUT_EDIT_PERSON: str = "Ctrl+E"
    
    # Message Box Titles
    MSG_TITLE_FILE_NOT_FOUND: str = "File Not Found"
    MSG_TITLE_ERROR: str = "Error"
    MSG_TITLE_EDIT_PERSON: str = "Edit Person"
    MSG_TITLE_UNSAVED_CHANGES: str = "Unsaved Changes"
    
    # Message Box Text
    MSG_TEXT_FILE_NOT_FOUND: str = "The file '{path}' no longer exists."
    MSG_TEXT_OPEN_ERROR: str = "Failed to open file:\n{error}"
    MSG_TEXT_SELECT_PERSON: str = "Please select a person to edit."
    MSG_TEXT_UNSAVED_CHANGES: str = "You have unsaved changes. Do you want to save before exiting?"
    
    # Placeholder View Text
    PLACEHOLDER_GENEALOGY: str = "Genealogy View\n(Coming Soon!)"
    PLACEHOLDER_TIMELINE: str = "Timeline View\n(Coming Soon!)"
    PLACEHOLDER_DYNASTY: str = "Dynasty View\n(Coming Soon!)"
    
    # Styles
    STYLE_PLACEHOLDER: str = "font-size: 24px; color: gray;"
    
    # Dirty Marker
    DIRTY_MARKER: str = " *"
    DIRTY_MARKER_EMPTY: str = ""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()
        
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(self.WINDOW_WIDTH_DEFAULT, self.WINDOW_HEIGHT_DEFAULT)
        
        self.db: DatabaseManager = DatabaseManager(self)
        self.undo_manager: UndoRedoManager = UndoRedoManager()
        self.settings_manager: SettingsManager = SettingsManager()
        
        self.file_actions: FileActions = FileActions(self)
        self.edit_actions: EditActions = EditActions(self)
        self.tools_actions: ToolsActions = ToolsActions(self)
        self.settings_actions: SettingsActions = SettingsActions(self)
        self.help_actions: HelpActions = HelpActions(self)
        
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
        
        temp_dir: str = tempfile.gettempdir()
        temp_file: str = os.path.join(temp_dir, self.TEMP_DB_NAME)
        
        if os.path.exists(temp_file):
            self._remove_temp_file(temp_file)
        
        self.db.new_database(temp_file)
        self.db._temp_file_path = temp_file
        self.db.file_path = None
        
        self.refresh_ui()
    
    def _remove_temp_file(self, temp_file: str) -> None:
        """Remove temporary file if it exists."""
        try:
            os.remove(temp_file)
        except Exception:
            pass
    
    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------
    
    def _setup_central_widget(self) -> None:
        """Setup the central widget with stacked views."""
        self.view_stack: QStackedWidget = QStackedWidget()
        self.setCentralWidget(self.view_stack)
        
        self.genealogy_view = None
        self.timeline_view = None
        self.dynasty_view = None
        self.data_table_view = None
    
    def _create_menus(self) -> None:
        """Create all menu bars and menu items."""
        menubar: QMenuBar = self.menuBar()
        
        self._create_file_menu(menubar)
        self._create_edit_menu(menubar)
        self._create_view_menu(menubar)
        self._create_tools_menu(menubar)
        self._create_settings_menu(menubar)
        self._create_help_menu(menubar)
    
    def _create_file_menu(self, menubar: QMenuBar) -> None:
        """Create the File menu."""
        file_menu = menubar.addMenu(self.MENU_FILE)
        
        self.action_new_dynasty: QAction = self._create_action(
            self.ACTION_TEXT_NEW_DYNASTY,
            self.ACTION_NAME_FILE_NEW
        )
        
        self.action_open_dynasty: QAction = self._create_action(
            self.ACTION_TEXT_OPEN_DYNASTY,
            self.ACTION_NAME_FILE_OPEN
        )
        
        file_menu.addAction(self.action_new_dynasty)
        file_menu.addAction(self.action_open_dynasty)
        
        self.recent_files_menu = file_menu.addMenu(self.ACTION_TEXT_RECENT_FILES)
        self._update_recent_files_menu()
        
        file_menu.addSeparator()
        
        self.action_save: QAction = self._create_action(
            self.ACTION_TEXT_SAVE,
            self.ACTION_NAME_FILE_SAVE
        )
        
        self.action_save_as: QAction = self._create_action(
            self.ACTION_TEXT_SAVE_AS,
            self.ACTION_NAME_FILE_SAVE_AS
        )
        
        file_menu.addAction(self.action_save)
        file_menu.addAction(self.action_save_as)
        file_menu.addSeparator()
        
        self.action_exit: QAction = self._create_action(
            self.ACTION_TEXT_EXIT,
            self.ACTION_NAME_FILE_EXIT
        )
        
        file_menu.addAction(self.action_exit)
    
    def _create_edit_menu(self, menubar: QMenuBar) -> None:
        """Create the Edit menu."""
        edit_menu = menubar.addMenu(self.MENU_EDIT)
        
        self.action_undo: QAction = self._create_action(
            self.ACTION_TEXT_UNDO,
            self.ACTION_NAME_EDIT_UNDO
        )
        
        self.action_redo: QAction = self._create_action(
            self.ACTION_TEXT_REDO,
            self.ACTION_NAME_EDIT_REDO
        )
        
        self.action_add_person: QAction = self._create_action(
            self.ACTION_TEXT_ADD_PERSON,
            self.ACTION_NAME_EDIT_ADD_PERSON
        )
        
        self.action_edit_person: QAction = QAction(self.ACTION_TEXT_EDIT_PERSON, self)
        self.action_edit_person.setObjectName(self.ACTION_NAME_EDIT_EDIT_PERSON)
        self.action_edit_person.setShortcut(self.SHORTCUT_EDIT_PERSON)
        
        self.action_remove_person: QAction = self._create_action(
            self.ACTION_TEXT_REMOVE_PERSON,
            self.ACTION_NAME_EDIT_REMOVE_PERSON
        )
        
        self.action_add_new_family: QAction = self._create_action(
            self.ACTION_TEXT_ADD_FAMILY,
            self.ACTION_NAME_EDIT_ADD_FAMILY
        )
        self.action_add_new_family.setEnabled(False)
        
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
        view_menu = menubar.addMenu(self.MENU_VIEW)
        
        self.action_view_family_trees: QAction = self._create_action(
            self.ACTION_TEXT_FAMILY_TREES,
            self.ACTION_NAME_VIEW_FAMILY_TREES
        )
        
        self.action_view_timeline: QAction = self._create_action(
            self.ACTION_TEXT_TIMELINE,
            self.ACTION_NAME_VIEW_TIMELINE
        )
        
        self.action_view_dynasty: QAction = self._create_action(
            self.ACTION_TEXT_DYNASTY,
            self.ACTION_NAME_VIEW_DYNASTY
        )
        
        self.action_view_data_table: QAction = self._create_action(
            self.ACTION_TEXT_DATA_TABLE,
            self.ACTION_NAME_VIEW_DATA_TABLE
        )
        
        view_menu.addAction(self.action_view_family_trees)
        view_menu.addAction(self.action_view_timeline)
        view_menu.addAction(self.action_view_dynasty)
        view_menu.addAction(self.action_view_data_table)
    
    def _create_tools_menu(self, menubar: QMenuBar) -> None:
        """Create the Tools menu."""
        tools_menu = menubar.addMenu(self.MENU_TOOLS)
        
        self.action_rebuild_scene: QAction = self._create_action(
            self.ACTION_TEXT_REBUILD_SCENE,
            self.ACTION_NAME_TOOLS_REBUILD
        )
        
        self.action_recompute_generations: QAction = self._create_action(
            self.ACTION_TEXT_RECOMPUTE_GENERATIONS,
            self.ACTION_NAME_TOOLS_RECOMPUTE
        )
        
        self.action_validate_marriages: QAction = self._create_action(
            self.ACTION_TEXT_VALIDATE_MARRIAGES,
            self.ACTION_NAME_TOOLS_VALIDATE_MARRIAGES
        )
        
        self.action_validate_parentage: QAction = self._create_action(
            self.ACTION_TEXT_VALIDATE_PARENTAGE,
            self.ACTION_NAME_TOOLS_VALIDATE_PARENTAGE
        )
        
        tools_menu.addAction(self.action_rebuild_scene)
        tools_menu.addAction(self.action_recompute_generations)
        tools_menu.addAction(self.action_validate_marriages)
        tools_menu.addAction(self.action_validate_parentage)
    
    def _create_settings_menu(self, menubar: QMenuBar) -> None:
        """Create the Settings menu."""
        settings_menu = menubar.addMenu(self.MENU_SETTINGS)
        
        self.action_settings: QAction = self._create_action(
            self.ACTION_TEXT_SETTINGS,
            self.ACTION_NAME_SETTINGS_SETTINGS
        )
        
        self.action_general: QAction = self._create_action(
            self.ACTION_TEXT_GENERAL,
            self.ACTION_NAME_SETTINGS_GENERAL
        )
        
        self.action_shortcuts: QAction = self._create_action(
            self.ACTION_TEXT_SHORTCUTS,
            self.ACTION_NAME_SETTINGS_SHORTCUTS
        )
        
        self.action_display: QAction = self._create_action(
            self.ACTION_TEXT_DISPLAY,
            self.ACTION_NAME_SETTINGS_DISPLAY
        )
        
        self.action_appearance: QAction = self._create_action(
            self.ACTION_TEXT_APPEARANCE,
            self.ACTION_NAME_SETTINGS_APPEARANCE
        )
        
        self.action_formats: QAction = self._create_action(
            self.ACTION_TEXT_FORMATS,
            self.ACTION_NAME_SETTINGS_FORMATS
        )
        
        settings_menu.addAction(self.action_settings)
        settings_menu.addSeparator()
        settings_menu.addAction(self.action_general)
        settings_menu.addAction(self.action_shortcuts)
        settings_menu.addAction(self.action_display)
        settings_menu.addAction(self.action_appearance)
        settings_menu.addAction(self.action_formats)
    
    def _create_help_menu(self, menubar: QMenuBar) -> None:
        """Create the Help menu."""
        help_menu = menubar.addMenu(self.MENU_HELP)
        
        self.action_about: QAction = self._create_action(
            self.ACTION_TEXT_ABOUT,
            self.ACTION_NAME_HELP_ABOUT
        )
        
        help_menu.addAction(self.action_about)
    
    def _create_action(self, text: str, object_name: str) -> QAction:
        """Create a QAction with text, object name, and shortcut from settings."""
        action: QAction = QAction(text, self)
        action.setObjectName(object_name)
        shortcut: str = self.settings_manager.get_shortcut(object_name)
        if shortcut:
            action.setShortcut(shortcut)
        return action
    
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
        
        recent: list[str] = self.settings_manager.get_recent_files()
        
        if recent:
            self._populate_recent_files(recent)
        else:
            self._show_no_recent_files()
    
    def _populate_recent_files(self, recent: list[str]) -> None:
        """Populate recent files menu with file actions."""
        for path in recent:
            filename: str = os.path.basename(path)
            action: QAction = QAction(filename, self)
            action.setData(path)
            action.triggered.connect(lambda checked, p=path: self._open_recent_file(p))
            self.recent_files_menu.addAction(action)
        
        self.recent_files_menu.addSeparator()
        
        clear_action: QAction = QAction(self.ACTION_TEXT_CLEAR_RECENT, self)
        clear_action.triggered.connect(self._clear_recent_files)
        self.recent_files_menu.addAction(clear_action)
    
    def _show_no_recent_files(self) -> None:
        """Show placeholder when no recent files exist."""
        no_recent: QAction = QAction(self.ACTION_TEXT_NO_RECENT, self)
        no_recent.setEnabled(False)
        self.recent_files_menu.addAction(no_recent)
    
    def _open_recent_file(self, path: str) -> None:
        """Open a file from recent files list."""
        if not os.path.exists(path):
            self._show_file_not_found_error(path)
            return
        
        self._attempt_open_file(path)
    
    def _show_file_not_found_error(self, path: str) -> None:
        """Show error message when file is not found."""
        QMessageBox.warning(
            self,
            self.MSG_TITLE_FILE_NOT_FOUND,
            self.MSG_TEXT_FILE_NOT_FOUND.format(path=path)
        )
        self._remove_from_recent_files(path)
    
    def _attempt_open_file(self, path: str) -> None:
        """Attempt to open file and handle errors."""
        try:
            self.db.open_database(path)
            self.refresh_ui()
            self.file_actions._refresh_all_views()
            self.settings_manager.add_recent_file(path)
            self._update_recent_files_menu()
        except Exception as e:
            self._show_open_error(e)
    
    def _show_open_error(self, error: Exception) -> None:
        """Show error message when file fails to open."""
        QMessageBox.critical(
            self,
            self.MSG_TITLE_ERROR,
            self.MSG_TEXT_OPEN_ERROR.format(error=str(error))
        )
    
    def _remove_from_recent_files(self, path: str) -> None:
        """Remove a file from recent files list."""
        recent: list[str] = self.settings_manager.get_recent_files()
        
        if path not in recent:
            return
        
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
            from views.tree_view.tree_canvas import TreeCanvas
            self.genealogy_view = TreeCanvas(self.db, self)
            self.genealogy_view.person_double_clicked.connect(self._on_tree_person_double_clicked)
            self.view_stack.addWidget(self.genealogy_view)

        self.genealogy_view.rebuild_scene()
        self.view_stack.setCurrentWidget(self.genealogy_view)

    def _on_tree_person_double_clicked(self, person_id: int) -> None:
        """Handle double-click on a person in the tree canvas."""
        from dialogs.edit_person_dialog import EditPersonDialog
        dialog: EditPersonDialog = EditPersonDialog(person_id, self.db, self)
        if dialog.exec():
            self.refresh_ui()
    
    def _show_timeline(self) -> None:
        """Switch to timeline view."""
        if self.timeline_view is None:
            self.timeline_view = self._create_placeholder_view(self.PLACEHOLDER_TIMELINE)
            self.view_stack.addWidget(self.timeline_view)
        
        self.view_stack.setCurrentWidget(self.timeline_view)
    
    def _show_dynasty(self) -> None:
        """Switch to dynasty view."""
        if self.dynasty_view is None:
            self.dynasty_view = self._create_placeholder_view(self.PLACEHOLDER_DYNASTY)
            self.view_stack.addWidget(self.dynasty_view)
        
        self.view_stack.setCurrentWidget(self.dynasty_view)
    
    def _create_placeholder_view(self, text: str) -> QLabel:
        """Create a placeholder view with text."""
        placeholder: QLabel = QLabel(text)
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(self.STYLE_PLACEHOLDER)
        return placeholder
    
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
        if self._is_data_table_active():
            self.data_table_view._edit_selected_person()  # type: ignore[union-attr]
        else:
            self._show_select_person_message()
    
    def _is_data_table_active(self) -> bool:
        """Check if data table view is currently active."""
        return (
            self.data_table_view is not None and 
            self.view_stack.currentWidget() == self.data_table_view
        )
    
    def _show_select_person_message(self) -> None:
        """Show message to select a person."""
        QMessageBox.information(
            self,
            self.MSG_TITLE_EDIT_PERSON,
            self.MSG_TEXT_SELECT_PERSON
        )
    
    # ------------------------------------------------------------------
    # UI Update Methods
    # ------------------------------------------------------------------
    
    def _update_window_title(self) -> None:
        """Update the window title to reflect current database state."""
        if not self.db.is_open:
            self.setWindowTitle(self.WINDOW_TITLE)
            return
        
        if self.db.file_path is None:
            self.setWindowTitle(self.WINDOW_TITLE_UNTITLED)
            return
        
        dirty_marker: str = self.DIRTY_MARKER if self.db.is_dirty else self.DIRTY_MARKER_EMPTY
        title: str = self.WINDOW_TITLE_FORMAT.format(
            name=self.db.database_name,
            dirty=dirty_marker
        )
        self.setWindowTitle(title)
    
    def _update_menu_states(self) -> None:
        """Enable or disable menu items based on current state."""
        has_db: bool = self.db.is_open
        
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
        """Refresh window title, menu states, and undo/redo labels."""
        self._update_window_title()
        self._update_menu_states()
        self.edit_actions.update_undo_redo_actions()
        if self.genealogy_view is not None and self.view_stack.currentWidget() is self.genealogy_view:
            self.genealogy_view.rebuild_scene()
    
    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------
    
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if not self._has_unsaved_changes():
            event.accept()
            return
        
        choice = self._prompt_save_before_close()
        
        if choice == QMessageBox.StandardButton.Save:
            if self.file_actions.save():
                event.accept()
            else:
                event.ignore()
        elif choice == QMessageBox.StandardButton.Discard:
            event.accept()
        else:
            event.ignore()
    
    def _has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes."""
        return self.db.is_open and self.db.is_dirty
    
    def _prompt_save_before_close(self) -> QMessageBox.StandardButton:
        """Prompt user to save changes before closing."""
        msg: QMessageBox = QMessageBox(self)
        msg.setWindowTitle(self.MSG_TITLE_UNSAVED_CHANGES)
        msg.setText(self.MSG_TEXT_UNSAVED_CHANGES)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        result: int = msg.exec()
        return QMessageBox.StandardButton(result)


# ------------------------------------------------------------------
# Application Entry Point
# ------------------------------------------------------------------

def main() -> None:
    """Application entry point."""
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()