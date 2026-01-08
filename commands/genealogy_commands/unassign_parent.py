"""Command for removing a parent assignment from a person."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from commands.base_command import BaseCommand
from database.person_repository import PersonRepository


class UnassignParentCommand(BaseCommand):
    """Remove a person's father or mother relationship."""
    
    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------
    
    PARENT_TYPE_FATHER: str = "father"
    PARENT_TYPE_MOTHER: str = "mother"
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        parent_type: str
    ) -> None:
        """
        Initialize unassign parent command.
        
        Args:
            db_manager: Database manager instance
            person: Person to remove parent from
            parent_type: "father" or "mother"
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.person: Person = person
        self.parent_type: str = parent_type
        self.old_parent_id: int | None = self._get_current_parent_id()
    
    def _get_current_parent_id(self) -> int | None:
        """Get current parent ID before unassignment."""
        if self.parent_type == self.PARENT_TYPE_FATHER:
            return self.person.father_id
        return self.person.mother_id
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Remove the parent relationship from database."""
        if self.parent_type == self.PARENT_TYPE_FATHER:
            self.person.father_id = None
        else:
            self.person.mother_id = None
        
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        person_repo.update(self.person)
    
    def undo(self) -> None:
        """Restore the parent relationship."""
        if self.parent_type == self.PARENT_TYPE_FATHER:
            self.person.father_id = self.old_parent_id
        else:
            self.person.mother_id = self.old_parent_id
        
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        person_repo.update(self.person)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        parent_label: str = "Father" if self.parent_type == self.PARENT_TYPE_FATHER else "Mother"
        return f"Remove {parent_label}"