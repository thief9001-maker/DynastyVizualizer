"""Calculate generation levels for all people."""


class GenerationCalculator:
    """Compute generation levels for genealogical hierarchy."""

    def __init__(self, database_connection) -> None:
        """Initialize the generation calculator."""
        self.db = database_connection

    def recompute_all_generations(self) -> None:
        """Recalculate generation levels for all people."""
        # TODO: Find all founders (no parents)
        # TODO: Run BFS from founders
        # TODO: Assign generation numbers
        # TODO: Handle edge cases (adoptions, step-relations)
        pass
