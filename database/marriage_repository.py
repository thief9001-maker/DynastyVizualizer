"""Repository for Marriage database operations."""

from __future__ import annotations

import sqlite3

from database.base_repository import BaseRepository
from models.marriage import Marriage


class MarriageRepository(BaseRepository[Marriage]):
    """Handle database operations for marriages."""
    
    # ------------------------------------------------------------------
    # SQL Query Templates
    # ------------------------------------------------------------------
    
    SQL_INSERT: str = """
        INSERT INTO Marriage (
            spouse1_id, spouse2_id,
            marriage_year, marriage_month, marriage_day,
            dissolution_year, dissolution_month, dissolution_day,
            dissolution_reason, marriage_type, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    SQL_INSERT_WITH_ID: str = """
        INSERT INTO Marriage (
            id, spouse1_id, spouse2_id,
            marriage_year, marriage_month, marriage_day,
            dissolution_year, dissolution_month, dissolution_day,
            dissolution_reason, marriage_type, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    SQL_SELECT_BY_ID: str = """
        SELECT * FROM Marriage WHERE id = ?
    """
    
    SQL_SELECT_BY_PERSON: str = """
        SELECT * FROM Marriage
        WHERE spouse1_id = ? OR spouse2_id = ?
        ORDER BY marriage_year, marriage_month
    """

    SQL_SELECT_ALL: str = """
        SELECT * FROM Marriage
        ORDER BY marriage_year, marriage_month
    """
    
    SQL_SELECT_ACTIVE_BY_PERSON: str = """
        SELECT * FROM Marriage
        WHERE (spouse1_id = ? OR spouse2_id = ?)
          AND dissolution_year IS NULL
        ORDER BY marriage_year, marriage_month
    """
    
    SQL_UPDATE: str = """
        UPDATE Marriage SET
            spouse1_id = ?,
            spouse2_id = ?,
            marriage_year = ?,
            marriage_month = ?,
            marriage_day = ?,
            dissolution_year = ?,
            dissolution_month = ?,
            dissolution_day = ?,
            dissolution_reason = ?,
            marriage_type = ?,
            notes = ?
        WHERE id = ?
    """
    
    SQL_DELETE: str = "DELETE FROM Marriage WHERE id = ?"
    
    SQL_END_MARRIAGE: str = """
        UPDATE Marriage SET
            dissolution_year = ?,
            dissolution_month = ?,
            dissolution_day = ?,
            dissolution_reason = ?
        WHERE id = ?
    """
    
    # ------------------------------------------------------------------
    # Default Values
    # ------------------------------------------------------------------
    
    DEFAULT_MARRIAGE_TYPE: str = "spouse"
    DEFAULT_NOTES: str = ""
    DEFAULT_DISSOLUTION_REASON: str = ""
    
    # ------------------------------------------------------------------
    # Abstract Method Implementations (Required by BaseRepository)
    # ------------------------------------------------------------------
    
    def _row_to_entity(self, row: sqlite3.Row) -> Marriage:
        """Convert database row to Marriage object."""
        return Marriage(
            id=row['id'],
            spouse1_id=row['spouse1_id'],
            spouse2_id=row['spouse2_id'],
            marriage_year=row['marriage_year'],
            marriage_month=row['marriage_month'],
            marriage_day=row['marriage_day'],
            dissolution_year=row['dissolution_year'],
            dissolution_month=row['dissolution_month'],
            dissolution_day=row['dissolution_day'],
            dissolution_reason=row['dissolution_reason'] or self.DEFAULT_DISSOLUTION_REASON,
            marriage_type=row['marriage_type'] or self.DEFAULT_MARRIAGE_TYPE,
            notes=row['notes'] or self.DEFAULT_NOTES
        )
    
    def _entity_to_values_without_id(self, entity: Marriage) -> tuple:
        """Extract marriage data as tuple for INSERT (without ID)."""
        return (
            entity.spouse1_id, entity.spouse2_id,
            entity.marriage_year, entity.marriage_month, entity.marriage_day,
            entity.dissolution_year, entity.dissolution_month, entity.dissolution_day,
            entity.dissolution_reason, entity.marriage_type, entity.notes
        )
    
    def _entity_to_values_with_id(self, entity: Marriage) -> tuple:
        """Extract marriage data as tuple for INSERT with explicit ID."""
        return (
            entity.id,
            entity.spouse1_id, entity.spouse2_id,
            entity.marriage_year, entity.marriage_month, entity.marriage_day,
            entity.dissolution_year, entity.dissolution_month, entity.dissolution_day,
            entity.dissolution_reason, entity.marriage_type, entity.notes
        )
    
    def _entity_to_values_for_update(self, entity: Marriage) -> tuple:
        """Extract marriage data as tuple for UPDATE (ID at end)."""
        return (
            entity.spouse1_id, entity.spouse2_id,
            entity.marriage_year, entity.marriage_month, entity.marriage_day,
            entity.dissolution_year, entity.dissolution_month, entity.dissolution_day,
            entity.dissolution_reason, entity.marriage_type, entity.notes,
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
        return "Marriage"
    
    # ------------------------------------------------------------------
    # Marriage-Specific Query Operations
    # ------------------------------------------------------------------
    
    def get_all(self) -> list[Marriage]:
        """Retrieve all marriages from database."""
        self._ensure_connection()

        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_ALL)
        rows: list[sqlite3.Row] = cursor.fetchall()

        return [self._row_to_entity(row) for row in rows]

    def get_by_person(self, person_id: int) -> list[Marriage]:
        """Get all marriages for a person (as either spouse)."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_BY_PERSON, (person_id, person_id))
        rows: list[sqlite3.Row] = cursor.fetchall()
        
        return [self._row_to_entity(row) for row in rows]
    
    def get_active_marriages(self, person_id: int) -> list[Marriage]:
        """Get all active (not ended) marriages for a person."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_ACTIVE_BY_PERSON, (person_id, person_id))
        rows: list[sqlite3.Row] = cursor.fetchall()
        
        return [self._row_to_entity(row) for row in rows]
    
    def end_marriage(
        self,
        marriage_id: int,
        dissolution_year: int,
        dissolution_month: int | None = None,
        dissolution_day: int | None = None,
        reason: str = ""
    ) -> None:
        """End a marriage by setting dissolution date and reason."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(
            self.SQL_END_MARRIAGE,
            (dissolution_year, dissolution_month, dissolution_day, reason, marriage_id)
        )
        self.db.mark_dirty()
    
    @staticmethod
    def get_spouse_id(marriage: Marriage, person_id: int) -> int | None:
        """Get the spouse ID for a given person in a marriage."""
        if marriage.spouse1_id == person_id:
            return marriage.spouse2_id
        elif marriage.spouse2_id == person_id:
            return marriage.spouse1_id
        return None