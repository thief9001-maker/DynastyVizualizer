"""Command for removing a person from the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person

from commands.base_command import BaseCommand
from database.person_repository import PersonRepository


class DeletePersonCommand(BaseCommand):
    """Delete a person from the dynasty database."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, person: Person) -> None:
        """
        Initialize delete person command.
        
        Args:
            db_manager: Database manager instance
            person: Person to delete
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.person: Person = person
        self.deleted_person_data: dict = self._capture_person_data()
    
    def _capture_person_data(self) -> dict:
        """Capture complete person data for undo."""
        return {
            'id': self.person.id,
            'first_name': self.person.first_name,
            'middle_name': self.person.middle_name,
            'last_name': self.person.last_name,
            'maiden_name': self.person.maiden_name,
            'nickname': self.person.nickname,
            'gender': self.person.gender,
            'birth_year': self.person.birth_year,
            'birth_month': self.person.birth_month,
            'birth_day': self.person.birth_day,
            'death_year': self.person.death_year,
            'death_month': self.person.death_month,
            'death_day': self.person.death_day,
            'arrival_year': self.person.arrival_year,
            'arrival_month': self.person.arrival_month,
            'arrival_day': self.person.arrival_day,
            'moved_out_year': self.person.moved_out_year,
            'moved_out_month': self.person.moved_out_month,
            'moved_out_day': self.person.moved_out_day,
            'father_id': self.person.father_id,
            'mother_id': self.person.mother_id,
            'family_id': self.person.family_id,
            'dynasty_id': self.person.dynasty_id,
            'is_founder': self.person.is_founder,
            'education': self.person.education,
            'notes': self.person.notes
        }
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Remove the person from the database."""
        if self.person.id is None:
            return
        
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        person_repo.delete(self.person.id)
    
    def undo(self) -> None:
        """Restore the deleted person."""
        from models.person import Person
        
        restored_person: Person = Person(**self.deleted_person_data)
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        person_repo.insert_with_id(restored_person)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return f"Delete Person: {self.person.first_name} {self.person.last_name}"