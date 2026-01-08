"""Command for ending a marriage with divorce or death."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.marriage import Marriage

from commands.base_command import BaseCommand
from database.marriage_repository import MarriageRepository


class EndMarriageCommand(BaseCommand):
    """Mark a marriage as ended with a specific date."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        marriage: Marriage,
        end_year: int | None,
        end_month: int | None,
        end_reason: str
    ) -> None:
        """
        Initialize end marriage command.
        
        Args:
            db_manager: Database manager instance
            marriage: Marriage to end
            end_year: Dissolution year
            end_month: Dissolution month
            end_reason: Reason for dissolution
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.marriage: Marriage = marriage
        self.end_year: int | None = end_year
        self.end_month: int | None = end_month
        self.end_reason: str = end_reason
        
        self.old_end_year: int | None = marriage.dissolution_year
        self.old_end_month: int | None = marriage.dissolution_month
        self.old_end_reason: str = marriage.dissolution_reason or ""
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Set the marriage end date in database."""
        self.marriage.dissolution_year = self.end_year
        self.marriage.dissolution_month = self.end_month
        self.marriage.dissolution_reason = self.end_reason
        
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriage_repo.update(self.marriage)
    
    def undo(self) -> None:
        """Restore original marriage end date."""
        self.marriage.dissolution_year = self.old_end_year
        self.marriage.dissolution_month = self.old_end_month
        self.marriage.dissolution_reason = self.old_end_reason
        
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        marriage_repo.update(self.marriage)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return "End Marriage"