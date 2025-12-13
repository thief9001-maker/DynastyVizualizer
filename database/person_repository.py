"""Database repository for Person entity operations."""

from __future__ import annotations
import sqlite3
from typing import TYPE_CHECKING

from models.person import Person

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager


class PersonRepository:
    """Handles all database operations for Person objects."""
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize repository with database manager."""
        self.db = db_manager
    
    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------
    
    def _row_to_person(self, row: sqlite3.Row) -> Person:
        """Convert database row to Person object using named column access."""
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
            dynasty_id=row['dynasty_id'] or 1,
            is_founder=bool(row['is_founder']),
            education=row['education'] or 0,
            notes=row['notes'] or ""
        )
    
    def _cursor(self):
        if self.db.conn is None:
            raise RuntimeError("DB connection not established.")
        return self.db.conn.cursor()
    
    # ------------------------------------------------------------------
    # Create Operations
    # ------------------------------------------------------------------
    
    def insert(self, person: Person) -> int:
        """Insert new person into database and return assigned ID."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        
        sql = """
            INSERT INTO Person (
                first_name, middle_name, last_name, maiden_name, nickname,
                gender, birth_year, birth_month, birth_day,
                death_year, death_month, death_day,
                arrival_year, arrival_month, arrival_day,
                moved_out_year, moved_out_month, moved_out_day,
                father_id, mother_id, family_id,
                dynasty_id, is_founder, education, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            person.first_name, person.middle_name, person.last_name,
            person.maiden_name, person.nickname,
            person.gender, person.birth_year, person.birth_month, person.birth_day,
            person.death_year, person.death_month, person.death_day,
            person.arrival_year, person.arrival_month, person.arrival_day,
            person.moved_out_year, person.moved_out_month, person.moved_out_day,
            person.father_id, person.mother_id, person.family_id,
            person.dynasty_id, 1 if person.is_founder else 0, person.education,
            person.notes
        )
        
        cursor.execute(sql, values)
        person_id = cursor.lastrowid
        
        self.db.mark_dirty()
        return person_id if person_id is not None else -1
       
    def insert_with_id(self, person: Person) -> None:
        """Insert person with specific ID (for redo operations)"""
        if self.db.conn is None:
            raise RuntimeError("Database connection not establish.")
        
        if person.id is None:
            raise ValueError("Person must have an ID for insert_with_id")
        
        cursor = self.db.conn.cursor()

        sql = """
            INSERT INTO Person (
                id, first_name, middle_name, last_name, maiden_name, nickname,
                gender, birth_year, birth_month, birth_day,
                death_year, death_month, death_day,
                arrival_year, arrival_month, arrival_day,
                moved_out_year, moved_out_month, moved_out_day,
                father_id, mother_id, family_id,
                dynasty_id, is_founder, education, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            person.id,  # Explicitly set the ID
            person.first_name, person.middle_name, person.last_name,
            person.maiden_name, person.nickname,
            person.gender, person.birth_year, person.birth_month, person.birth_day,
            person.death_year, person.death_month, person.death_day,
            person.arrival_year, person.arrival_month, person.arrival_day,
            person.moved_out_year, person.moved_out_month, person.moved_out_day,
            person.father_id, person.mother_id, person.family_id,
            person.dynasty_id, 1 if person.is_founder else 0, person.education,
            person.notes
        )
        
        cursor.execute(sql, values)
        self.db.mark_dirty()
        

    # ------------------------------------------------------------------
    # Read Operations
    # ------------------------------------------------------------------
    
    def get_by_id(self, person_id: int) -> Person | None:
        """Retrieve person by ID, return None if not found."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM Person WHERE id = ?", (person_id,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_person(row)
    
    def get_all(self) -> list[Person]:
        """Retrieve all people from database."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM Person ORDER BY last_name, first_name")
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    def get_by_name(self, first_name: str, last_name: str) -> list[Person]:
        """Find people by first and last name."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        sql = """
            SELECT * FROM Person 
            WHERE first_name = ? AND last_name = ?
            ORDER BY birth_year
        """
        cursor.execute(sql, (first_name, last_name))
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    def get_children(self, parent_id: int) -> list[Person]:
        """Retrieve all children of a given parent."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")

        cursor = self.db.conn.cursor()
        sql = """
            SELECT * FROM Person 
            WHERE father_id = ? OR mother_id = ?
            ORDER BY birth_year, birth_month, birth_day
        """
        cursor.execute(sql, (parent_id, parent_id))
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    def get_alive_in_year(self, year: int) -> list[Person]:
        """Retrieve all people alive in a given year."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")

        cursor = self.db.conn.cursor()
        sql = """
            SELECT * FROM Person
            WHERE birth_year <= ? 
            AND (death_year IS NULL OR death_year >= ?)
            ORDER BY birth_year
        """
        cursor.execute(sql, (year, year))
        rows = cursor.fetchall()
        
        return [self._row_to_person(row) for row in rows]
    
    # ------------------------------------------------------------------
    # Update Operations
    # ------------------------------------------------------------------
    
    def update(self, person: Person) -> None:
        """Update existing person in database."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        if person.id is None:
            raise ValueError("Cannot update person without ID.")
        
        cursor = self.db.conn.cursor()
        
        sql = """
            UPDATE Person SET
                first_name = ?, middle_name = ?, last_name = ?,
                maiden_name = ?, nickname = ?,
                gender = ?, birth_year = ?, birth_month = ?, birth_day = ?,
                death_year = ?, death_month = ?, death_day = ?,
                arrival_year = ?, arrival_month = ?, arrival_day = ?,
                moved_out_year = ?, moved_out_month = ?, moved_out_day = ?,
                father_id = ?, mother_id = ?, family_id = ?,
                dynasty_id = ?, is_founder = ?, education = ?, notes = ?
            WHERE id = ?
        """
        
        values = (
            person.first_name, person.middle_name, person.last_name,
            person.maiden_name, person.nickname,
            person.gender, person.birth_year, person.birth_month, person.birth_day,
            person.death_year, person.death_month, person.death_day,
            person.arrival_year, person.arrival_month, person.arrival_day,
            person.moved_out_year, person.moved_out_month, person.moved_out_day,
            person.father_id, person.mother_id, person.family_id,
            person.dynasty_id, 1 if person.is_founder else 0, person.education,
            person.notes,
            person.id
        )
        
        cursor.execute(sql, values)
        self.db.mark_dirty()
    
    # ------------------------------------------------------------------
    # Delete Operations
    # ------------------------------------------------------------------
    
    def delete(self, person_id: int) -> None:
        """Delete person from database by ID."""
        if self.db.conn is None:
            raise RuntimeError("Database connection not established.")
        
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM Person WHERE id = ?", (person_id,))
        self.db.mark_dirty()
