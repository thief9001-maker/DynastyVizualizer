"""Command for adding an event to a person."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.event import Event

from commands.base_command import BaseCommand
from database.event_repository import EventRepository


class AddEventCommand(BaseCommand):
    """Add a life event to a person."""
    
    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------
    
    def __init__(self, db_manager: DatabaseManager, event: Event) -> None:
        """Initialize the add event command."""
        super().__init__()
        self.db_manager: DatabaseManager = db_manager
        self.event: Event = event
        self.event_id: int | None = None
    
    # ------------------------------------------------------------------
    # Command Execution
    # ------------------------------------------------------------------
    
    def run(self) -> None:
        """Insert the event into the database."""
        event_repo: EventRepository = EventRepository(self.db_manager)
        self.event_id = event_repo.insert(self.event)
    
    def undo(self) -> None:
        """Remove the event from the database."""
        if self.event_id is None:
            return
        
        event_repo: EventRepository = EventRepository(self.db_manager)
        event_repo.delete(self.event_id)