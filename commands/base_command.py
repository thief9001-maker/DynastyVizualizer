import re

class BaseCommand:
    """Base class for all undoable commands."""
    
    def __init__(self):
        self._executed = False  
    
    def description(self) -> str:
        """Return human-readable description for UI display."""
        class_name = self.__class__.__name__
        if class_name.endswith("Command"):
            class_name = class_name[:-7]

        spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', class_name)
        
        return spaced
    
    def run(self) -> None:
        """Execute the command."""
        raise NotImplementedError("Subclasses must implement run()")
    
    def undo(self) -> None:
        """Reverse the command's effects."""
        raise NotImplementedError("Subclasses must implement undo()")
