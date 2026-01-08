"""Command for adding a new person to the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from commands.base_command import BaseCommand
from database.person_repository import PersonRepository


class AddPersonCommand(BaseCommand):
    """Add a new person to the dynasty database with undo support."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, person: Person) -> None:
        """Initialize the add person command."""
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.person: Person = person
        self.person_id: int | None = None
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Insert the person into the database and store the assigned ID."""
        repo: PersonRepository = PersonRepository(self.db_manager)
        
        if self.person_id is None:
            self._insert_new_person(repo)
        else:
            self._reinsert_person_with_id(repo)
    
    def _insert_new_person(self, repo: PersonRepository) -> None:
        """Insert person as new record and store generated ID."""
        self.person_id = repo.insert(self.person)
        self.person.id = self.person_id
    
    def _reinsert_person_with_id(self, repo: PersonRepository) -> None:
        """Reinsert person with previously assigned ID (for redo)."""
        self.person.id = self.person_id
        repo.insert_with_id(self.person)
    
    def undo(self) -> None:
        """Remove the person from the database."""
        if self.person_id is None:
            return
        
        repo: PersonRepository = PersonRepository(self.db_manager)
        repo.delete(self.person_id)