"""Command for creating a child with automatic parent assignment."""

from commands.base_command import BaseCommand


class CreateChildCommand(BaseCommand):
    """Create a new person as child of specified parents."""

    def __init__(
        self,
        database_connection,
        first_name: str,
        last_name: str,
        father_id: int | None = None,
        mother_id: int | None = None,
        **kwargs,
    ) -> None:
        """Initialize the create child command."""
        self.db = database_connection
        self.first_name = first_name
        self.last_name = last_name
        self.father_id = father_id
        self.mother_id = mother_id
        self.additional_data = kwargs
        self.created_person_id: int | None = None
        # TODO: Store created person ID for undo

    def run(self) -> None:
        """Create new person with parent relationships."""
        # TODO: Insert new person into database
        # TODO: Set father_id and mother_id
        # TODO: Store created_person_id
        pass

    def undo(self) -> None:
        """Delete the created child."""
        # TODO: Delete person record using created_person_id
        pass
