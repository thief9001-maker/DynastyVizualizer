"""Command for editing an existing event."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.event import Event

from commands.base_command import BaseCommand
from database.event_repository import EventRepository


class EditEventCommand(BaseCommand):
    """Edit details of an existing event with undo support."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        event: Event,
        original_event_data: dict
    ) -> None:
        """
        Initialize edit event command.
        
        Args:
            db_manager: Database manager instance
            event: Modified event object
            original_event_data: Original event data for undo
        """
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.event: Event = event
        self.original_event_data: dict = original_event_data
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Update event in database."""
        event_repo: EventRepository = EventRepository(self.db_manager)
        event_repo.update(self.event)
    
    def undo(self) -> None:
        """Restore original event data."""
        from models.event import Event
        
        original_event: Event = Event(**self.original_event_data)
        event_repo: EventRepository = EventRepository(self.db_manager)
        event_repo.update(original_event)
    
    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------
    
    def description(self) -> str:
        """Return human-readable description."""
        return f"Edit Event: {self.event.event_title}"