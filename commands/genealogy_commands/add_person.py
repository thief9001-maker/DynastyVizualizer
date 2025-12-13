"""Command for adding a new person to the database."""

from __future__ import annotations
from typing import TYPE_CHECKING

from models.person import Person
from database.person_repository import PersonRepository

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager


class AddPersonCommand:
    """Add a new person to the dynasty database with undo support."""

    def __init__(self, db_manager: DatabaseManager, person: Person) -> None:
        """Initialize the add person command."""
        self.person = person
        self.person_id: int | None = None
        self.repo = PersonRepository(db_manager)

    def run(self) -> None:
        """Insert the person into the database and store the assigned ID."""
        if self.person_id is None:
            self.person_id = self.repo.insert(self.person)
            self.person.id = self.person_id

        else:
            self.person.id = self.person_id
            self.repo.insert_with_id(self.person)

    def undo(self) -> None:
        """Remove the person from the database."""
        if self.person_id is not None:
            self.repo.delete(self.person_id)