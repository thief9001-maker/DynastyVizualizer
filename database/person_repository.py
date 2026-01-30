"""Database repository for Person entity operations."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

from database.base_repository import BaseRepository
from models.person import Person

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager


class PersonRepository(BaseRepository[Person]):
    """Handles all database operations for Person objects."""
    
    # ------------------------------------------------------------------
    # SQL Query Templates
    # ------------------------------------------------------------------
    
    SQL_INSERT: str = """
        INSERT INTO Person (
            first_name, middle_name, last_name, maiden_name, nickname,
            gender, birth_year, birth_month, birth_day,
            death_year, death_month, death_day,
            arrival_year, arrival_month, arrival_day,
            moved_out_year, moved_out_month, moved_out_day,
            father_id, mother_id, family_id,
            dynasty_id, is_founder, education, is_favorite, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    SQL_INSERT_WITH_ID: str = """
        INSERT INTO Person (
            id, first_name, middle_name, last_name, maiden_name, nickname,
            gender, birth_year, birth_month, birth_day,
            death_year, death_month, death_day,
            arrival_year, arrival_month, arrival_day,
            moved_out_year, moved_out_month, moved_out_day,
            father_id, mother_id, family_id,
            dynasty_id, is_founder, education, is_favorite, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    SQL_SELECT_BY_ID: str = "SELECT * FROM Person WHERE id = ?"
    
    SQL_SELECT_ALL: str = "SELECT * FROM Person ORDER BY last_name, first_name"
    
    SQL_SELECT_BY_NAME: str = """
        SELECT * FROM Person 
        WHERE first_name = ? AND last_name = ?
        ORDER BY birth_year
    """
    
    SQL_SELECT_CHILDREN: str = """
        SELECT * FROM Person 
        WHERE father_id = ? OR mother_id = ?
        ORDER BY birth_year, birth_month, birth_day
    """
    
    SQL_SELECT_ALIVE_IN_YEAR: str = """
        SELECT * FROM Person
        WHERE birth_year <= ? 
        AND (death_year IS NULL OR death_year >= ?)
        ORDER BY birth_year
    """
    
    SQL_UPDATE: str = """
        UPDATE Person SET
            first_name = ?, middle_name = ?, last_name = ?,
            maiden_name = ?, nickname = ?,
            gender = ?, birth_year = ?, birth_month = ?, birth_day = ?,
            death_year = ?, death_month = ?, death_day = ?,
            arrival_year = ?, arrival_month = ?, arrival_day = ?,
            moved_out_year = ?, moved_out_month = ?, moved_out_day = ?,
            father_id = ?, mother_id = ?, family_id = ?,
            dynasty_id = ?, is_founder = ?, education = ?, is_favorite = ?, notes = ?
        WHERE id = ?
    """
    
    SQL_DELETE: str = "DELETE FROM Person WHERE id = ?"
    
    # ------------------------------------------------------------------
    # Default Values
    # ------------------------------------------------------------------
    
    DEFAULT_DYNASTY_ID: int = 1
    FOUNDER_FLAG_TRUE: int = 1
    FOUNDER_FLAG_FALSE: int = 0
    DEFAULT_EDUCATION: int = 0
    DEFAULT_NOTES: str = ""
    
    # ------------------------------------------------------------------
    # Abstract Method Implementations (Required by BaseRepository)
    # ------------------------------------------------------------------
    
    def _row_to_entity(self, row: sqlite3.Row) -> Person:
        """Convert database row to Person object."""
        return Person(
            id=row['id'],
            first_name=row['first_name'],
            middle_name=row['middle_name'],
            last_name=row['last_name'],
            maiden_name=row['maiden_name'],
            nickname=row['nickname'],
            gender=row['gender'],
            birth_year=row['birth_year'],
            birth_month=row['birth_month'],
            birth_day=row['birth_day'],
            death_year=row['death_year'],
            death_month=row['death_month'],
            death_day=row['death_day'],
            arrival_year=row['arrival_year'],
            arrival_month=row['arrival_month'],
            arrival_day=row['arrival_day'],
            moved_out_year=row['moved_out_year'],
            moved_out_month=row['moved_out_month'],
            moved_out_day=row['moved_out_day'],
            father_id=row['father_id'],
            mother_id=row['mother_id'],
            family_id=row['family_id'],
            dynasty_id=row['dynasty_id'] or self.DEFAULT_DYNASTY_ID,
            is_founder=bool(row['is_founder']),
            education=row['education'] or self.DEFAULT_EDUCATION,
            is_favorite=bool(row['is_favorite']),
            notes=row['notes'] or self.DEFAULT_NOTES
        )
    
    def _entity_to_values_without_id(self, entity: Person) -> tuple:
        """Extract person data as tuple for INSERT (without ID)."""
        return (
            entity.first_name, entity.middle_name, entity.last_name,
            entity.maiden_name, entity.nickname,
            entity.gender, entity.birth_year, entity.birth_month, entity.birth_day,
            entity.death_year, entity.death_month, entity.death_day,
            entity.arrival_year, entity.arrival_month, entity.arrival_day,
            entity.moved_out_year, entity.moved_out_month, entity.moved_out_day,
            entity.father_id, entity.mother_id, entity.family_id,
            entity.dynasty_id,
            self.FOUNDER_FLAG_TRUE if entity.is_founder else self.FOUNDER_FLAG_FALSE,
            entity.education,
            self.FOUNDER_FLAG_TRUE if entity.is_favorite else self.FOUNDER_FLAG_FALSE,
            entity.notes
        )

    def _entity_to_values_with_id(self, entity: Person) -> tuple:
        """Extract person data as tuple for INSERT with explicit ID."""
        return (
            entity.id,
            entity.first_name, entity.middle_name, entity.last_name,
            entity.maiden_name, entity.nickname,
            entity.gender, entity.birth_year, entity.birth_month, entity.birth_day,
            entity.death_year, entity.death_month, entity.death_day,
            entity.arrival_year, entity.arrival_month, entity.arrival_day,
            entity.moved_out_year, entity.moved_out_month, entity.moved_out_day,
            entity.father_id, entity.mother_id, entity.family_id,
            entity.dynasty_id,
            self.FOUNDER_FLAG_TRUE if entity.is_founder else self.FOUNDER_FLAG_FALSE,
            entity.education,
            self.FOUNDER_FLAG_TRUE if entity.is_favorite else self.FOUNDER_FLAG_FALSE,
            entity.notes
        )

    def _entity_to_values_for_update(self, entity: Person) -> tuple:
        """Extract person data as tuple for UPDATE (ID at end)."""
        return (
            entity.first_name, entity.middle_name, entity.last_name,
            entity.maiden_name, entity.nickname,
            entity.gender, entity.birth_year, entity.birth_month, entity.birth_day,
            entity.death_year, entity.death_month, entity.death_day,
            entity.arrival_year, entity.arrival_month, entity.arrival_day,
            entity.moved_out_year, entity.moved_out_month, entity.moved_out_day,
            entity.father_id, entity.mother_id, entity.family_id,
            entity.dynasty_id,
            self.FOUNDER_FLAG_TRUE if entity.is_founder else self.FOUNDER_FLAG_FALSE,
            entity.education,
            self.FOUNDER_FLAG_TRUE if entity.is_favorite else self.FOUNDER_FLAG_FALSE,
            entity.notes,
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
        return "Person"
    
    # ------------------------------------------------------------------
    # Person-Specific Query Operations
    # ------------------------------------------------------------------
    
    def get_all(self) -> list[Person]:
        """Retrieve all people from database."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_ALL)
        rows: list[sqlite3.Row] = cursor.fetchall()
        
        return [self._row_to_entity(row) for row in rows]
    
    def get_by_name(self, first_name: str, last_name: str) -> list[Person]:
        """Find people by first and last name."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_BY_NAME, (first_name, last_name))
        rows: list[sqlite3.Row] = cursor.fetchall()
        
        return [self._row_to_entity(row) for row in rows]
    
    def get_children(self, parent_id: int) -> list[Person]:
        """Retrieve all children of a given parent."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_CHILDREN, (parent_id, parent_id))
        rows: list[sqlite3.Row] = cursor.fetchall()
        
        return [self._row_to_entity(row) for row in rows]
    
    def get_alive_in_year(self, year: int) -> list[Person]:
        """Retrieve all people alive in a given year."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self.SQL_SELECT_ALIVE_IN_YEAR, (year, year))
        rows: list[sqlite3.Row] = cursor.fetchall()
        
        return [self._row_to_entity(row) for row in rows]