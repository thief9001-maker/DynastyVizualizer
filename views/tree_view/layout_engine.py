"""Automatic layout engine for positioning people in the tree."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person
    from models.marriage import Marriage


@dataclass
class LayoutResult:
    """Complete layout output for the tree canvas."""

    person_positions: dict[int, tuple[float, float]] = field(default_factory=dict)
    marriage_positions: dict[int, tuple[float, float]] = field(default_factory=dict)
    generation_bands: dict[int, tuple[float, float]] = field(default_factory=dict)
    year_range: tuple[int, int] = (0, 0)


class TreeLayoutEngine:
    """Calculate automatic positions for people in the family tree."""

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    # Spacing
    HORIZONTAL_GAP: float = 60.0
    VERTICAL_GAP: float = 200.0
    MARRIAGE_NODE_GAP: float = 40.0
    SIBLING_GAP: float = 20.0

    # Person box dimensions (must match PersonBox constants)
    BOX_WIDTH: float = 300.0
    BOX_HEIGHT: float = 130.0

    # Marriage node size (must match MarriageNode)
    MARRIAGE_NODE_SIZE: float = 18.0

    # Generation band padding
    BAND_PADDING_TOP: float = 30.0
    BAND_PADDING_BOTTOM: float = 30.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self, database_connection: DatabaseManager) -> None:
        """Initialize the layout engine."""
        self.db: DatabaseManager = database_connection

    # ------------------------------------------------------------------
    # Main Layout
    # ------------------------------------------------------------------

    def calculate_layout(self) -> LayoutResult:
        """Calculate positions for all people, marriages, and generation bands."""
        from database.person_repository import PersonRepository
        from database.marriage_repository import MarriageRepository

        person_repo: PersonRepository = PersonRepository(self.db)
        marriage_repo: MarriageRepository = MarriageRepository(self.db)

        all_people: list[Person] = person_repo.get_all()
        all_marriages: list[Marriage] = marriage_repo.get_all()

        if not all_people:
            return LayoutResult()

        generations: dict[int, int] = self._compute_generations(all_people)
        gen_groups: dict[int, list[Person]] = self._group_by_generation(all_people, generations)
        marriage_lookup: dict[int, list[Marriage]] = self._build_marriage_lookup(all_marriages)

        result: LayoutResult = LayoutResult()

        self._assign_positions(gen_groups, marriage_lookup, generations, result)
        self._compute_generation_bands(gen_groups, result)
        self._compute_marriage_positions(all_marriages, result)
        result.year_range = self._compute_year_range(all_people)

        return result

    def calculate_positions(self) -> dict[int, tuple[float, float]]:
        """Calculate x,y positions for all people (legacy interface)."""
        return self.calculate_layout().person_positions

    # ------------------------------------------------------------------
    # Generation Computation
    # ------------------------------------------------------------------

    def _compute_generations(self, people: list[Person]) -> dict[int, int]:
        """Assign generation numbers to all people via BFS from founders."""
        person_map: dict[int, Person] = {}
        children_of: dict[int, list[int]] = {}
        generations: dict[int, int] = {}
        founders: list[int] = []

        for person in people:
            if person.id is None:
                continue
            person_map[person.id] = person

            if person.father_id is None and person.mother_id is None:
                founders.append(person.id)

            for parent_id in (person.father_id, person.mother_id):
                if parent_id is not None:
                    children_of.setdefault(parent_id, []).append(person.id)

        if not founders:
            for person in people:
                if person.id is not None:
                    founders.append(person.id)
                    break

        queue: list[tuple[int, int]] = [(pid, 0) for pid in founders]

        while queue:
            person_id, gen = queue.pop(0)

            if person_id in generations:
                continue

            generations[person_id] = gen

            for child_id in children_of.get(person_id, []):
                if child_id not in generations:
                    queue.append((child_id, gen + 1))

        for person in people:
            if person.id is not None and person.id not in generations:
                generations[person.id] = 0

        return generations

    def _group_by_generation(
        self,
        people: list[Person],
        generations: dict[int, int]
    ) -> dict[int, list[Person]]:
        """Group people by their generation number."""
        groups: dict[int, list[Person]] = {}

        for person in people:
            if person.id is None:
                continue
            gen: int = generations.get(person.id, 0)
            groups.setdefault(gen, []).append(person)

        for gen in groups:
            groups[gen].sort(key=lambda p: (p.family_id or 0, p.birth_year or 0))

        return groups

    # ------------------------------------------------------------------
    # Marriage Lookup
    # ------------------------------------------------------------------

    def _build_marriage_lookup(self, marriages: list[Marriage]) -> dict[int, list[Marriage]]:
        """Build person_id -> marriages mapping."""
        lookup: dict[int, list[Marriage]] = {}

        for marriage in marriages:
            if marriage.spouse1_id is not None:
                lookup.setdefault(marriage.spouse1_id, []).append(marriage)
            if marriage.spouse2_id is not None:
                lookup.setdefault(marriage.spouse2_id, []).append(marriage)

        return lookup

    # ------------------------------------------------------------------
    # Position Assignment
    # ------------------------------------------------------------------

    def _assign_positions(
        self,
        gen_groups: dict[int, list[Person]],
        marriage_lookup: dict[int, list[Marriage]],
        generations: dict[int, int],
        result: LayoutResult
    ) -> None:
        """Assign x,y positions to all people, grouping spouses together."""
        sorted_gens: list[int] = sorted(gen_groups.keys())
        placed_spouses: set[int] = set()

        for gen in sorted_gens:
            y: float = gen * (self.BOX_HEIGHT + self.VERTICAL_GAP)
            x: float = 0.0
            people: list[Person] = gen_groups[gen]

            for person in people:
                if person.id is None or person.id in placed_spouses:
                    continue

                spouse_id: int | None = self._find_same_gen_spouse(
                    person, marriage_lookup, generations, gen
                )

                if spouse_id is not None and spouse_id not in placed_spouses:
                    result.person_positions[person.id] = (x, y)
                    x += self.BOX_WIDTH + self.MARRIAGE_NODE_GAP

                    result.person_positions[spouse_id] = (x, y)
                    placed_spouses.add(spouse_id)

                    x += self.BOX_WIDTH + self.HORIZONTAL_GAP
                else:
                    result.person_positions[person.id] = (x, y)
                    x += self.BOX_WIDTH + self.HORIZONTAL_GAP

    def _find_same_gen_spouse(
        self,
        person: Person,
        marriage_lookup: dict[int, list[Marriage]],
        generations: dict[int, int],
        gen: int
    ) -> int | None:
        """Find a spouse of person who is in the same generation."""
        if person.id is None:
            return None

        marriages: list[Marriage] = marriage_lookup.get(person.id, [])

        for marriage in marriages:
            spouse_id: int | None = None

            if marriage.spouse1_id == person.id:
                spouse_id = marriage.spouse2_id
            elif marriage.spouse2_id == person.id:
                spouse_id = marriage.spouse1_id

            if spouse_id is not None and generations.get(spouse_id) == gen:
                return spouse_id

        return None

    # ------------------------------------------------------------------
    # Marriage Node Positions
    # ------------------------------------------------------------------

    def _compute_marriage_positions(
        self,
        marriages: list[Marriage],
        result: LayoutResult
    ) -> None:
        """Position marriage nodes between their spouses."""
        for marriage in marriages:
            if marriage.id is None:
                continue

            s1_pos = result.person_positions.get(marriage.spouse1_id) if marriage.spouse1_id else None
            s2_pos = result.person_positions.get(marriage.spouse2_id) if marriage.spouse2_id else None

            if s1_pos is not None and s2_pos is not None:
                mid_x: float = (s1_pos[0] + self.BOX_WIDTH + s2_pos[0]) / 2 - self.MARRIAGE_NODE_SIZE / 2
                mid_y: float = s1_pos[1] + self.BOX_HEIGHT / 2 - self.MARRIAGE_NODE_SIZE / 2
                result.marriage_positions[marriage.id] = (mid_x, mid_y)
            elif s1_pos is not None:
                result.marriage_positions[marriage.id] = (
                    s1_pos[0] + self.BOX_WIDTH + 10,
                    s1_pos[1] + self.BOX_HEIGHT / 2 - self.MARRIAGE_NODE_SIZE / 2
                )
            elif s2_pos is not None:
                result.marriage_positions[marriage.id] = (
                    s2_pos[0] - self.MARRIAGE_NODE_SIZE - 10,
                    s2_pos[1] + self.BOX_HEIGHT / 2 - self.MARRIAGE_NODE_SIZE / 2
                )

    # ------------------------------------------------------------------
    # Generation Bands
    # ------------------------------------------------------------------

    def _compute_generation_bands(
        self,
        gen_groups: dict[int, list[Person]],
        result: LayoutResult
    ) -> None:
        """Compute y-position and height for each generation band."""
        sorted_gens: list[int] = sorted(gen_groups.keys())

        for gen in sorted_gens:
            band_y: float = gen * (self.BOX_HEIGHT + self.VERTICAL_GAP) - self.BAND_PADDING_TOP
            band_height: float = self.BOX_HEIGHT + self.BAND_PADDING_TOP + self.BAND_PADDING_BOTTOM
            result.generation_bands[gen] = (band_y, band_height)

    # ------------------------------------------------------------------
    # Year Range
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_year_range(people: list[Person]) -> tuple[int, int]:
        """Find the earliest and latest years across all people."""
        years: list[int] = []

        for person in people:
            if person.birth_year is not None:
                years.append(person.birth_year)
            if person.death_year is not None:
                years.append(person.death_year)
            if person.arrival_year is not None:
                years.append(person.arrival_year)

        if not years:
            return (0, 0)

        return (min(years), max(years))
