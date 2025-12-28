"""Repository for Marriage database operations."""

from database.db_manager import DatabaseManager
from models.marriage import Marriage


class MarriageRepository:
    """Handle database operations for marriages."""
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize the marriage repository."""
        self.db = db_manager
    
    def insert(self, marriage: Marriage) -> int:
        """Insert a new marriage into the database.
        
        Returns the new marriage ID, or -1 if database not open.
        """
        if not self.db.conn:
            return -1
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            INSERT INTO Marriage (
                spouse1_id, spouse2_id,
                marriage_year, marriage_month, marriage_day,
                dissolution_year, dissolution_month, dissolution_day,
                dissolution_reason, marriage_type, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            marriage.spouse1_id, marriage.spouse2_id,
            marriage.marriage_year, marriage.marriage_month, marriage.marriage_day,
            marriage.dissolution_year, marriage.dissolution_month, marriage.dissolution_day,
            marriage.dissolution_reason, marriage.marriage_type, marriage.notes
        ))
        
        self.db.conn.commit()
        return cursor.lastrowid or -1
    
    def insert_with_id(self, marriage: Marriage) -> None:
        """Insert marriage with explicit ID (for undo/redo)."""
        if not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            INSERT INTO Marriage (
                id, spouse1_id, spouse2_id,
                marriage_year, marriage_month, marriage_day,
                dissolution_year, dissolution_month, dissolution_day,
                dissolution_reason, marriage_type, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            marriage.id, marriage.spouse1_id, marriage.spouse2_id,
            marriage.marriage_year, marriage.marriage_month, marriage.marriage_day,
            marriage.dissolution_year, marriage.dissolution_month, marriage.dissolution_day,
            marriage.dissolution_reason, marriage.marriage_type, marriage.notes
        ))
        
        self.db.conn.commit()
    
    def get_by_id(self, marriage_id: int) -> Marriage | None:
        """Get a marriage by ID."""
        if not self.db.conn:
            return None
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            SELECT id, spouse1_id, spouse2_id,
                   marriage_year, marriage_month, marriage_day,
                   dissolution_year, dissolution_month, dissolution_day,
                   dissolution_reason, marriage_type, notes
            FROM Marriage
            WHERE id = ?
        """, (marriage_id,))
        
        row = cursor.fetchone()
        if row:
            return self._row_to_marriage(row)
        return None
    
    def get_by_person(self, person_id: int) -> list[Marriage]:
        """Get all marriages for a person (as either spouse)."""
        if not self.db.conn:
            return []
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            SELECT id, spouse1_id, spouse2_id,
                   marriage_year, marriage_month, marriage_day,
                   dissolution_year, dissolution_month, dissolution_day,
                   dissolution_reason, marriage_type, notes
            FROM Marriage
            WHERE spouse1_id = ? OR spouse2_id = ?
            ORDER BY marriage_year, marriage_month
        """, (person_id, person_id))
        
        return [self._row_to_marriage(row) for row in cursor.fetchall()]
    
    def get_active_marriages(self, person_id: int) -> list[Marriage]:
        """Get all active (not ended) marriages for a person."""
        if not self.db.conn:
            return []
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            SELECT id, spouse1_id, spouse2_id,
                   marriage_year, marriage_month, marriage_day,
                   dissolution_year, dissolution_month, dissolution_day,
                   dissolution_reason, marriage_type, notes
            FROM Marriage
            WHERE (spouse1_id = ? OR spouse2_id = ?)
              AND dissolution_year IS NULL
            ORDER BY marriage_year, marriage_month
        """, (person_id, person_id))
        
        return [self._row_to_marriage(row) for row in cursor.fetchall()]
    
    def get_spouse_id(self, marriage: Marriage, person_id: int) -> int | None:
        """Get the spouse ID for a given person in a marriage."""
        if marriage.spouse1_id == person_id:
            return marriage.spouse2_id
        elif marriage.spouse2_id == person_id:
            return marriage.spouse1_id
        return None
    
    def update(self, marriage: Marriage) -> None:
        """Update an existing marriage."""
        if not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
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
        """, (
            marriage.spouse1_id, marriage.spouse2_id,
            marriage.marriage_year, marriage.marriage_month, marriage.marriage_day,
            marriage.dissolution_year, marriage.dissolution_month, marriage.dissolution_day,
            marriage.dissolution_reason, marriage.marriage_type, marriage.notes,
            marriage.id
        ))
        
        self.db.conn.commit()
    
    def delete(self, marriage_id: int) -> None:
        """Delete a marriage by ID."""
        if not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        cursor.execute("DELETE FROM Marriage WHERE id = ?", (marriage_id,))
        self.db.conn.commit()
    
    def end_marriage(self, marriage_id: int, dissolution_year: int, 
                     dissolution_month: int | None = None, 
                     dissolution_day: int | None = None, 
                     reason: str = "") -> None:
        """End a marriage by setting dissolution date and reason."""
        if not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            UPDATE Marriage SET
                dissolution_year = ?,
                dissolution_month = ?,
                dissolution_day = ?,
                dissolution_reason = ?
            WHERE id = ?
        """, (dissolution_year, dissolution_month, dissolution_day, reason, marriage_id))
        
        self.db.conn.commit()
    
    def _row_to_marriage(self, row: tuple) -> Marriage:
        """Convert database row to Marriage object."""
        return Marriage(
            id=row[0],
            spouse1_id=row[1],
            spouse2_id=row[2],
            marriage_year=row[3],
            marriage_month=row[4],
            marriage_day=row[5],
            dissolution_year=row[6],
            dissolution_month=row[7],
            dissolution_day=row[8],
            dissolution_reason=row[9] or "",
            marriage_type=row[10] or "spouse",
            notes=row[11] or ""
        )