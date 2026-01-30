"""Command for creating a marriage between two people."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.marriage import Marriage

from commands.base_command import BaseCommand
from database.marriage_repository import MarriageRepository


class AddMarriageCommand(BaseCommand):
    """Create a marriage relationship between two people."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, marriage: Marriage) -> None:
        """Initialize the create marriage command."""
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.marriage: Marriage = marriage
        self.marriage_id: int | None = None
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Insert the marriage into the database."""
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)

        if self.marriage_id is None:
            self.marriage_id = marriage_repo.insert(self.marriage)
            self.marriage.id = self.marriage_id
        else:
            self.marriage.id = self.marriage_id
            marriage_repo.insert_with_id(self.marriage)
    
    def undo(self) -> None:
        """Remove the marriage from the database."""
        if self.marriage_id is None:
            return
        
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriage_repo.delete(self.marriage_id)