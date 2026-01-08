"""Command for editing an existing marriage."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.marriage import Marriage

from commands.base_command import BaseCommand
from database.marriage_repository import MarriageRepository


class EditMarriageCommand(BaseCommand):
    """Edit details of an existing marriage relationship."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        marriage: Marriage,
        original_marriage_data: dict
    ) -> None:
        """
        Initialize edit marriage command.
        
        Args:
            db_manager: Database manager instance
            marriage: Modified marriage object
            original_marriage_data: Original marriage data for undo
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.marriage: Marriage = marriage
        self.original_marriage_data: dict = original_marriage_data
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Update marriage details in database."""
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriage_repo.update(self.marriage)
    
    def undo(self) -> None:
        """Restore original marriage details."""
        from models.marriage import Marriage
        
        original_marriage: Marriage = Marriage(**self.original_marriage_data)
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriage_repo.update(original_marriage)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return "Edit Marriage"