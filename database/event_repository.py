"""Repository for Event database operations."""

from __future__ import annotations

import sqlite3

from database.base_repository import BaseRepository
from models.event import Event


class EventRepository(BaseRepository[Event]):
    """Handle database operations for events."""
    
    # ------------------------------------------------------------------
    # SQL Query Templates
    # ------------------------------------------------------------------
    
    SQL_INSERT: str = """
        INSERT INTO Event (
            person_id, event_type, event_title,
            start_year, start_month, start_day,
            end_year, end_month, end_day, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    SQL_INSERT_WITH_ID: str = """
        INSERT INTO Event (
            id, person_id, event_type, event_title,
            start_year, start_month, start_day,
            end_year, end_month, end_day, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    SQL_SELECT_BY_ID: str = """
        SELECT * FROM Event WHERE id = ?
    """
    
    SQL_SELECT_BY_PERSON: str = """
        SELECT * FROM Event
        WHERE person_id = ?
        ORDER BY start_year, start_month, start_day
    """
    
    SQL_UPDATE: str = """
        UPDATE Event SET
            person_id = ?,
            event_type = ?,
            event_title = ?,
            start_year = ?,
            start_month = ?,
            start_day = ?,
            end_year = ?,
            end_month = ?,
            end_day = ?,
            notes = ?
        WHERE id = ?
    """
    
    SQL_DELETE: str = "DELETE FROM Event WHERE id = ?"
    
    # ------------------------------------------------------------------
    # Default Values
    # ------------------------------------------------------------------
    
    DEFAULT_EVENT_TYPE: str = ""
    DEFAULT_EVENT_TITLE: str = ""
    DEFAULT_NOTES: str = ""
    
    # ------------------------------------------------------------------
    # Abstract Method Implementations (Required by BaseRepository)
    # ------------------------------------------------------------------
    
    def _row_to_entity(self, row: sqlite3.Row) -> Event:
        """Convert database row to Event object."""
        return Event(
            id=row['id'],
            person_id=row['person_id'],
            event_type=row['event_type'] or self.DEFAULT_EVENT_TYPE,
            event_title=row['event_title'] or self.DEFAULT_EVENT_TITLE,
            start_year=self._to_int(row['start_year']),
            start_month=self._to_int(row['start_month']),
            start_day=self._to_int(row['start_day']),
            end_year=self._to_int(row['end_year']),
            end_month=self._to_int(row['end_month']),
            end_day=self._to_int(row['end_day']),
            notes=row['notes'] or self.DEFAULT_NOTES
        )
    
    def _entity_to_values_without_id(self, entity: Event) -> tuple:
        """Extract event data as tuple for INSERT (without ID)."""
        return (
            entity.person_id, entity.event_type, entity.event_title,
            entity.start_year, entity.start_month, entity.start_day,
            entity.end_year, entity.end_month, entity.end_day, entity.notes
        )
    
    def _entity_to_values_with_id(self, entity: Event) -> tuple:
        """Extract event data as tuple for INSERT with explicit ID."""
        return (
            entity.id,
            entity.person_id, entity.event_type, entity.event_title,
            entity.start_year, entity.start_month, entity.start_day,
            entity.end_year, entity.end_month, entity.end_day, entity.notes
        )
    
    def _entity_to_values_for_update(self, entity: Event) -> tuple:
        """Extract event data as tuple for UPDATE (ID at end)."""
        return (
            entity.person_id, entity.event_type, entity.event_title,
            entity.start_year, entity.start_month, entity.start_day,
            entity.end_year, entity.end_month, entity.end_day, entity.notes,
            entity.id
        )
    
    def _get_insert_sql(self) -> str:
        """Get SQL for INSERT operation."""
        return self.SQL_INSERT
    
    def _get_insert_with_id_sql(self) -> str:
        """Get SQL for INSERT with explicit ID."""
        return self.SQL_INSERT_WITH_ID
    
    def _get_select_by_id_sql(self) -> str:
        """Get SQL for SELECT by ID."""
        return self.SQL_SELECT_BY_ID
    
    def _get_update_sql(self) -> str:
        """Get SQL for UPDATE operation."""
        return self.SQL_UPDATE
    
    def _get_delete_sql(self) -> str:
        """Get SQL for DELETE operation."""
        return self.SQL_DELETE
    
    def _get_entity_name(self) -> str:
        """Get entity name for error messages."""
        return "Event"
    
    # ------------------------------------------------------------------
    # Event-Specific Query Operations
    # ------------------------------------------------------------------
    
    def get_by_person(self, person_id: int) -> list[Event]:
        """Get all events for a person, sorted chronologically."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_BY_PERSON, (person_id,))
        rows: list[sqlite3.Row] = cursor.fetchall()
        
        return [self._row_to_entity(row) for row in rows]
    
    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------
    
    @staticmethod
    def _to_int(value: int | None) -> int | None:
        """Convert database value to int or None."""
        return int(value) if value is not None else None