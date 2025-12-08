"""Data validation tools for detecting inconsistencies."""


class MarriageValidator:
    """Validate marriage data for inconsistencies."""

    def __init__(self, database_connection) -> None:
        """Initialize the marriage validator."""
        self.db = database_connection

    def validate_all(self) -> list[dict]:
        """Check all marriages for issues."""
        # TODO: Check for overlapping marriages
        # TODO: Check for invalid dates
        # TODO: Check for self-marriages
        # TODO: Return list of issues
        pass


class ParentageValidator:
    """Validate parent-child relationships."""

    def __init__(self, database_connection) -> None:
        """Initialize the parentage validator."""
        self.db = database_connection

    def validate_all(self) -> list[dict]:
        """Check all parentage relationships for issues."""
        # TODO: Check for circular parentage
        # TODO: Check for impossible dates
        # TODO: Return list of issues
        pass
