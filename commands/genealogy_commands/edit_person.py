"""Command for editing an existing person and related data."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person
    from models.marriage import Marriage
    from models.event import Event

from commands.base_command import BaseCommand
from database.person_repository import PersonRepository
from database.marriage_repository import MarriageRepository
from database.event_repository import EventRepository


class EditPersonCommand(BaseCommand):
    """
    Composite command for editing person and all related changes.
    
    Bundles:
    - Person data changes (name, dates, etc.)
    - Marriage changes (new, modified, deleted)
    - Event changes (new, modified, deleted)
    - Parent relationship changes
    """
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        person: Person,
        original_person_data: dict,
        new_marriages: list[Marriage],
        modified_marriages: dict[int, Marriage],
        deleted_marriage_ids: list[int],
        new_events: list[Event],
        modified_events: dict[int, Event],
        deleted_event_ids: list[int],
        original_marriages: list[Marriage],
        original_events: list[Event]
    ) -> None:
        """
        Initialize edit person command with all changes.
        
        Args:
            db_manager: Database manager instance
            person: Modified person object
            original_person_data: Original person data for undo
            new_marriages: New marriages to insert
            modified_marriages: Existing marriages that were modified
            deleted_marriage_ids: Marriage IDs to delete
            new_events: New events to insert
            modified_events: Existing events that were modified
            deleted_event_ids: Event IDs to delete
            original_marriages: Original marriage data for undo
            original_events: Original event data for undo
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.person: Person = person
        self.original_person_data: dict = original_person_data
        
        self.new_marriages: list[Marriage] = new_marriages
        self.modified_marriages: dict[int, Marriage] = modified_marriages
        self.deleted_marriage_ids: list[int] = deleted_marriage_ids
        
        self.new_events: list[Event] = new_events
        self.modified_events: dict[int, Event] = modified_events
        self.deleted_event_ids: list[int] = deleted_event_ids
        
        self.original_marriages: list[Marriage] = original_marriages
        self.original_events: list[Event] = original_events
        
        self.inserted_marriage_ids: list[int] = []
        self.inserted_event_ids: list[int] = []
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Execute all changes to person and related data."""
        self.inserted_marriage_ids.clear()
        self.inserted_event_ids.clear()
        self._update_person()
        self._apply_marriage_changes()
        self._apply_event_changes()
    
    def _update_person(self) -> None:
        """Update person data in database."""
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        person_repo.update(self.person)
    
    def _apply_marriage_changes(self) -> None:
        """Apply all marriage changes."""
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        
        for marriage_id in self.deleted_marriage_ids:
            marriage_repo.delete(marriage_id)
        
        for marriage in self.new_marriages:
            marriage_id: int = marriage_repo.insert(marriage)
            self.inserted_marriage_ids.append(marriage_id)
        
        for marriage_id, marriage in self.modified_marriages.items():
            marriage_repo.update(marriage)
    
    def _apply_event_changes(self) -> None:
        """Apply all event changes."""
        event_repo: EventRepository = EventRepository(self.db_manager)
        
        for event_id in self.deleted_event_ids:
            event_repo.delete(event_id)
        
        for event in self.new_events:
            event_id: int = event_repo.insert(event)
            self.inserted_event_ids.append(event_id)
        
        for event_id, event in self.modified_events.items():
            event_repo.update(event)
    
    # ------------------------------------------------------------------
    # Command Undo
    # ------------------------------------------------------------------
    
    def undo(self) -> None:
        """Undo all changes and restore original state."""
        self._restore_person()
        self._restore_marriages()
        self._restore_events()
    
    def _restore_person(self) -> None:
        """Restore original person data."""
        person_repo: PersonRepository = PersonRepository(self.db_manager)
        
        from models.person import Person
        original_person: Person = Person(**self.original_person_data)
        person_repo.update(original_person)
    
    def _restore_marriages(self) -> None:
        """Restore original marriages."""
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        
        for marriage_id in self.inserted_marriage_ids:
            marriage_repo.delete(marriage_id)
        
        for marriage in self.original_marriages:
            if marriage.id in self.deleted_marriage_ids:
                marriage_repo.insert_with_id(marriage)
            elif marriage.id in self.modified_marriages:
                marriage_repo.update(marriage)
    
    def _restore_events(self) -> None:
        """Restore original events."""
        event_repo: EventRepository = EventRepository(self.db_manager)
        
        for event_id in self.inserted_event_ids:
            event_repo.delete(event_id)
        
        for event in self.original_events:
            if event.id in self.deleted_event_ids:
                event_repo.insert_with_id(event)
            elif event.id in self.modified_events:
                event_repo.update(event)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return f"Edit {self.person.first_name} {self.person.last_name}"