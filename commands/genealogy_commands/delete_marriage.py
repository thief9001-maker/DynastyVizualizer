"""Command for deleting a marriage from the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.marriage import Marriage

from commands.base_command import BaseCommand
from database.marriage_repository import MarriageRepository


class DeleteMarriageCommand(BaseCommand):
    """Remove a marriage relationship from the database."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, marriage: Marriage) -> None:
        """
        Initialize delete marriage command.
        
        Args:
            db_manager: Database manager instance
            marriage: Marriage to delete
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.marriage: Marriage = marriage
        self.deleted_marriage_data: dict = self._capture_marriage_data()
    
    def _capture_marriage_data(self) -> dict:
        """Capture complete marriage data for undo."""
        return {
            'id': self.marriage.id,
            'spouse1_id': self.marriage.spouse1_id,
            'spouse2_id': self.marriage.spouse2_id,
            'marriage_year': self.marriage.marriage_year,
            'marriage_month': self.marriage.marriage_month,
            'dissolution_year': self.marriage.dissolution_year,
            'dissolution_month': self.marriage.dissolution_month,
            'dissolution_day': self.marriage.dissolution_day,
            'dissolution_reason': self.marriage.dissolution_reason
        }
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Delete the marriage from database."""
        if self.marriage.id is None:
            return
        
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriage_repo.delete(self.marriage.id)
    
    def undo(self) -> None:
        """Restore the deleted marriage."""
        from models.marriage import Marriage
        
        restored_marriage: Marriage = Marriage(**self.deleted_marriage_data)
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriage_repo.insert_with_id(restored_marriage)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return "Delete Marriage"