"""Base class for all undoable commands."""

from __future__ import annotations

import re


class BaseCommand:
    """Base class for all undoable commands."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    COMMAND_SUFFIX: str = "Command"
    REGEX_CAMEL_TO_SPACED: str = r'([a-z])([A-Z])'
    REGEX_REPLACEMENT: str = r'\1 \2'
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self) -> None:
        """Initialize base command."""
        self._executed: bool = False
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description for UI display."""
        class_name: str = self._get_class_name_without_suffix()
        spaced: str = self._convert_camel_case_to_spaced(class_name)
        return spaced
    
    def _get_class_name_without_suffix(self) -> str:
        """Get class name with 'Command' suffix removed."""
        class_name: str = self.__class__.__name__
        
        if class_name.endswith(self.COMMAND_SUFFIX):
            return class_name[:-len(self.COMMAND_SUFFIX)]
        
        return class_name
    
    def _convert_camel_case_to_spaced(self, text: str) -> str:
        """Convert CamelCase to spaced text."""
        return re.sub(self.REGEX_CAMEL_TO_SPACED, self.REGEX_REPLACEMENT, text)
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Execute the command."""
        raise NotImplementedError("Subclasses must implement run()")
    
    def undo(self) -> None:
        """Reverse the command's effects."""
        raise NotImplementedError("Subclasses must implement undo()")