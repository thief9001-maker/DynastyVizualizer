"""Repository for Event database operations."""

from database.db_manager import DatabaseManager
from models.event import Event


class EventRepository:
    """Handle database operations for events."""
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        self.db = db_manager
    
    def insert(self, event: Event) -> int:
        """Insert a new event into the database."""
        if not self.db.conn:
            return -1
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            INSERT INTO Event (
                person_id, event_type, event_title,
                start_year, start_month, start_day,
                end_year, end_month, end_day, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.person_id, event.event_type, event.event_title,
            event.start_year, event.start_month, event.start_day,
            event.end_year, event.end_month, event.end_day, event.notes
        ))
        
        self.db.conn.commit()
        return cursor.lastrowid or -1
    
    def get_by_id(self, event_id: int) -> Event | None:
        """Get an event by ID."""
        if not self.db.conn:
            return None
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            SELECT id, person_id, event_type, event_title,
                   start_year, start_month, start_day,
                   end_year, end_month, end_day, notes
            FROM Event
            WHERE id = ?
        """, (event_id,))
        
        row = cursor.fetchone()
        return self._row_to_event(row) if row else None
    
    def get_by_person(self, person_id: int) -> list[Event]:
        """Get all events for a person, sorted chronologically."""
        if not self.db.conn:
            return []
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            SELECT id, person_id, event_type, event_title,
                   start_year, start_month, start_day,
                   end_year, end_month, end_day, notes
            FROM Event
            WHERE person_id = ?
            ORDER BY start_year, start_month, start_day
        """, (person_id,))
        
        return [self._row_to_event(row) for row in cursor.fetchall()]
    
    def update(self, event: Event) -> None:
        """Update an existing event."""
        if not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
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
        """, (
            event.person_id, event.event_type, event.event_title,
            event.start_year, event.start_month, event.start_day,
            event.end_year, event.end_month, event.end_day, event.notes,
            event.id
        ))
        
        self.db.conn.commit()
    
    def delete(self, event_id: int) -> None:
        """Delete an event by ID."""
        if not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM Event WHERE id = ?", (event_id,))
        self.db.conn.commit()
    
    @staticmethod
    def _to_int(value) -> int | None:
        """Convert database value to int or None."""
        return int(value) if value is not None else None
    
    def _row_to_event(self, row: tuple) -> Event:
        """Convert database row to Event object."""
        return Event(
            id=row[0],
            person_id=row[1],
            event_type=row[2] or "",
            event_title=row[3] or "",
            start_year=self._to_int(row[4]),
            start_month=self._to_int(row[5]),
            start_day=self._to_int(row[6]),
            end_year=self._to_int(row[7]),
            end_month=self._to_int(row[8]),
            end_day=self._to_int(row[9]),
            notes=row[10] or ""
        )