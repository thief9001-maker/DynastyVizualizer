"""Command for deleting an event from the database."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.event import Event

from commands.base_command import BaseCommand
from database.event_repository import EventRepository


class DeleteEventCommand(BaseCommand):
    """Remove an event from the database."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, event: Event) -> None:
        """
        Initialize delete event command.
        
        Args:
            db_manager: Database manager instance
            event: Event to delete
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.event: Event = event
        self.deleted_event_data: dict = self._capture_event_data()
    
    def _capture_event_data(self) -> dict:
        """Capture complete event data for undo."""
        return {
            'id': self.event.id,
            'person_id': self.event.person_id,
            'event_type': self.event.event_type,
            'event_title': self.event.event_title,
            'start_year': self.event.start_year,
            'start_month': self.event.start_month,
            'start_day': self.event.start_day,
            'end_year': self.event.end_year,
            'end_month': self.event.end_month,
            'end_day': self.event.end_day,
            'notes': self.event.notes
        }
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Delete the event from database."""
        if self.event.id is None:
            return
        
        event_repo: EventRepository = EventRepository(self.db_manager)
        event_repo.delete(self.event.id)
    
    def undo(self) -> None:
        """Restore the deleted event."""
        from models.event import Event
        
        restored_event: Event = Event(**self.deleted_event_data)
        event_repo: EventRepository = EventRepository(self.db_manager)
        event_repo.insert_with_id(restored_event)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return f"Delete Event: {self.event.event_title}"