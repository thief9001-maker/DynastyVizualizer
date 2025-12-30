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

    # ------------------------------------------------------------------
    # Recent Files Operations
    # ------------------------------------------------------------------

    def get_recent_files(self) -> list[str]:
        """Get list of recent file paths."""
        self.qsettings.beginGroup("recent_files")
        size = self.qsettings.beginReadArray("files")
        recent = []
        for i in range(size):
            self.qsettings.setArrayIndex(i)
            path = self.qsettings.value("path")
            if path:
                recent.append(path)
        self.qsettings.endArray()
        self.qsettings.endGroup()
        return recent

    def add_recent_file(self, file_path: str) -> None:
        """Add file to recent files list (most recent first)."""
        recent = self.get_recent_files()

        if file_path in recent:
            recent.remove(file_path)
        
        recent.insert(0, file_path)

        recent = recent[:10]

        self.qsettings.beginGroup("recent_files")
        self.qsettings.beginWriteArray("files")
        for i, path in enumerate(recent):
            self.qsettings.setArrayIndex(i)
            self.qsettings.setValue("path", path)
        self.qsettings.endArray()
        self.qsettings.endGroup()
        self.qsettings.sync()

    def clear_recent_files(self) -> None:
        """Clear all recent files."""
        self.qsettings.beginGroup("recent_files")
        self.qsettings.remove("")
        self.qsettings.endGroup()
        self.qsettings.sync()