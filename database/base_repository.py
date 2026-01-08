"""Base repository with shared database operations."""
from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING, TypeVar, Generic, Protocol
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager

class HasID(Protocol):
    """Protocol for entities that have an ID attribute."""
    id: int | None

T = TypeVar('T', bound=HasID)

class BaseRepository(ABC, Generic[T]):
    """Base class for all repository classes with common operations."""

    # Constants - Error Messages
    ERROR_NO_CONNECTION: str = "Database connection not established."
    ERROR_NO_ID_FOR_UPDATE: str = "Cannot update {entity} without ID."
    ERROR_NO_ID_FOR_INSERT: str = "{entity} must have an ID for insert_with_id."

    # Constants - Default Values
    DEFAULT_ID_ON_ERROR: int = -1
    
    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initialize repository with database manager."""
        self.db: DatabaseManager = db_manager
    
    # ------------------------------------------------------------------
    # Abstract Methods - Must Be Implemented by Child Classes
    # ------------------------------------------------------------------
    
    @abstractmethod
    def _row_to_entity(self, row: sqlite3.Row) -> T:
        """Convert database row to entity object."""
        pass
    
    @abstractmethod
    def _entity_to_values_without_id(self, entity: T) -> tuple:
        """Extract entity data as tuple for INSERT (without ID)."""
        pass
    
    @abstractmethod
    def _entity_to_values_with_id(self, entity: T) -> tuple:
        """Extract entity data as tuple for INSERT with explicit ID."""
        pass
    
    @abstractmethod
    def _entity_to_values_for_update(self, entity: T) -> tuple:
        """Extract entity data as tuple for UPDATE (ID at end)."""
        pass
    
    @abstractmethod
    def _get_insert_sql(self) -> str:
        """Get SQL for INSERT operation."""
        pass
    
    @abstractmethod
    def _get_insert_with_id_sql(self) -> str:
        """Get SQL for INSERT with explicit ID."""
        pass
    
    @abstractmethod
    def _get_select_by_id_sql(self) -> str:
        """Get SQL for SELECT by ID."""
        pass
    
    @abstractmethod
    def _get_update_sql(self) -> str:
        """Get SQL for UPDATE operation."""
        pass
    
    @abstractmethod
    def _get_delete_sql(self) -> str:
        """Get SQL for DELETE operation."""
        pass
    
    @abstractmethod
    def _get_entity_name(self) -> str:
        """Get entity name for error messages."""
        pass
    
    # ------------------------------------------------------------------
    # Helper Methods - Database Access
    # ------------------------------------------------------------------
    
    def _get_cursor(self) -> sqlite3.Cursor:
        """Get database cursor or raise if connection unavailable."""
        if self.db.conn is None:
            raise RuntimeError(self.ERROR_NO_CONNECTION)
        return self.db.conn.cursor()
    
    def _ensure_connection(self) -> None:
        """Ensure database connection exists or raise."""
        if self.db.conn is None:
            raise RuntimeError(self.ERROR_NO_CONNECTION)
    
    # ------------------------------------------------------------------
    # Common CRUD Operations
    # ------------------------------------------------------------------
    
    def insert(self, entity: T) -> int:
        """Insert new entity into database and return assigned ID."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        values: tuple = self._entity_to_values_without_id(entity)
        
        cursor.execute(self._get_insert_sql(), values)
        entity_id: int | None = cursor.lastrowid
        
        self.db.mark_dirty()
        return entity_id if entity_id is not None else self.DEFAULT_ID_ON_ERROR
    
    def insert_with_id(self, entity: T) -> None:
        """Insert entity with specific ID (for redo operations)."""
        self._ensure_connection()

        if not hasattr(entity, 'id') or entity.id is None:
            entity_name = self._get_entity_name()
            raise ValueError(self.ERROR_NO_ID_FOR_INSERT.format(entity=entity_name))
        
        cursor: sqlite3.Cursor = self._get_cursor()
        values: tuple = self._entity_to_values_with_id(entity)
        
        cursor.execute(self._get_insert_with_id_sql(), values)
        self.db.mark_dirty()
    
    def get_by_id(self, entity_id: int) -> T | None:
        """Retrieve entity by ID, return None if not found."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self._get_select_by_id_sql(), (entity_id,))
        row: sqlite3.Row | None = cursor.fetchone()
        
        if row is None:
            return None
        
        return self._row_to_entity(row)
    
    def update(self, entity: T) -> None:
        """Update existing entity in database."""
        self._ensure_connection()

        if not hasattr(entity, 'id') or entity.id is None:
            entity_name = self._get_entity_name()
            raise ValueError(self.ERROR_NO_ID_FOR_UPDATE.format(entity=entity_name))
        
        cursor: sqlite3.Cursor = self._get_cursor()
        values: tuple = self._entity_to_values_for_update(entity)
        
        cursor.execute(self._get_update_sql(), values)
        self.db.mark_dirty()
    
    def delete(self, entity_id: int) -> None:
        """Delete entity from database by ID."""
        self._ensure_connection()
        
        cursor: sqlite3.Cursor = self._get_cursor()
        cursor.execute(self._get_delete_sql(), (entity_id,))
        self.db.mark_dirty()