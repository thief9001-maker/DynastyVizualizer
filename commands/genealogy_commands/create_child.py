"""Command for creating a child with automatic parent assignment."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from commands.base_command import BaseCommand
from database.person_repository import PersonRepository


class CreateChildCommand(BaseCommand):
    """Create a new person as child of specified parents."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, child: Person) -> None:
        """
        Initialize create child command.
        
        Args:
            db_manager: Database manager instance
            child: Child person object with parent relationships
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.child: Person = child
        self.created_person_id: int | None = None
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Create new person with parent relationships in database."""
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        
        if self.created_person_id is None:
            self.created_person_id = person_repo.insert(self.child)
            self.child.id = self.created_person_id
        else:
            self.child.id = self.created_person_id
            person_repo.insert_with_id(self.child)
    
    def undo(self) -> None:
        """Delete the created child."""
        if self.created_person_id is None:
            return
        
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        person_repo.delete(self.created_person_id)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return f"Create Child: {self.child.first_name} {self.child.last_name}"