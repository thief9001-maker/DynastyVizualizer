"""Automatic layout engine for positioning people in the tree.

Y-positions are determined by birth year (not generation).  Generations
are visual guide-bands whose year spans are computed from the people
they contain but can later be edited by the user.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.person import Person
    from models.marriage import Marriage


# ------------------------------------------------------------------
# Layout Result
# ------------------------------------------------------------------

@dataclass
class LayoutResult:
    """Complete layout output for the tree canvas."""

    person_positions: dict[int, tuple[float, float]] = field(default_factory=dict)
    marriage_positions: dict[int, tuple[float, float]] = field(default_factory=dict)
    generation_bands: dict[int, tuple[float, float, str]] = field(default_factory=dict)
    year_range: tuple[int, int] = (0, 0)
    pixels_per_year: float = 0.0


# ------------------------------------------------------------------
# Engine
# ------------------------------------------------------------------

class TreeLayoutEngine:
    """Calculate automatic positions for people in the family tree.

    Vertical placement is driven by birth year, not generation number.
    """

    # Spacing ----------------------------------------------------------
    HORIZONTAL_GAP: float = 60.0
    MARRIAGE_NODE_GAP: float = 40.0
    SIBLING_GAP: float = 20.0

    # Pixels-per-year controls how "tall" each calendar year is on-screen.
    PIXELS_PER_YEAR: float = 12.0

    # Extra buffer above earliest / below latest person (in years).
    YEAR_BUFFER: int = 5

    # Person box dimensions (must match PersonBox constants).
    BOX_WIDTH: float = 300.0
    BOX_HEIGHT: float = 130.0

    # Marriage node size (must match MarriageNode).
    MARRIAGE_NODE_SIZE: float = 24.0

    # Generation band padding above / below the extreme birth-years.
    BAND_PADDING_TOP: float = 30.0
    BAND_PADDING_BOTTOM: float = 30.0

    # Snap grid cell size (used by canvas for snap-to-grid).
    GRID_CELL: float = 20.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self, database_connection: DatabaseManager) -> None:
        self.db: DatabaseManager = database_connection

    # ------------------------------------------------------------------
    # Main Layout
    # ------------------------------------------------------------------

    def calculate_layout(self) -> LayoutResult:
        """Calculate positions for all people, marriages, and generation bands."""
        from database.person_repository import PersonRepository
        from database.marriage_repository import MarriageRepository

        person_repo = PersonRepository(self.db)
        marriage_repo = MarriageRepository(self.db)

        all_people: list[Person] = person_repo.get_all()
        all_marriages: list[Marriage] = marriage_repo.get_all()

        if not all_people:
            return LayoutResult()

        year_range = self._compute_year_range(all_people)
        earliest, latest = year_range

        # Ensure at least a 1-year span so we don't divide by zero.
        if earliest == latest:
            latest = earliest + 1

        result = LayoutResult()
        result.year_range = year_range
        result.pixels_per_year = self.PIXELS_PER_YEAR

        generations: dict[int, int] = self._compute_generations(all_people)
        marriage_lookup = self._build_marriage_lookup(all_marriages)

        self._assign_positions(all_people, generations, marriage_lookup, earliest, result)
        self._compute_marriage_positions(all_marriages, result)
        self._compute_generation_bands(all_people, generations, earliest, result)

        return result

    def calculate_positions(self) -> dict[int, tuple[float, float]]:
        """Legacy interface."""
        return self.calculate_layout().person_positions

    # ------------------------------------------------------------------
    # Year → Y mapping
    # ------------------------------------------------------------------

    def _year_to_y(self, year: int | None, earliest_year: int) -> float:
        """Convert a birth year to a scene-Y coordinate."""
        if year is None:
            return 0.0
        return (year - earliest_year + self.YEAR_BUFFER) * self.PIXELS_PER_YEAR

    # ------------------------------------------------------------------
    # Generation Computation (still used for band guides)
    # ------------------------------------------------------------------

    def _compute_generations(self, people: list[Person]) -> dict[int, int]:
        """Assign generation numbers via BFS from founders."""
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

    # ------------------------------------------------------------------
    # Marriage Lookup
    # ------------------------------------------------------------------

    def _build_marriage_lookup(self, marriages: list[Marriage]) -> dict[int, list[Marriage]]:
        lookup: dict[int, list[Marriage]] = {}
        for marriage in marriages:
            if marriage.spouse1_id is not None:
                lookup.setdefault(marriage.spouse1_id, []).append(marriage)
            if marriage.spouse2_id is not None:
                lookup.setdefault(marriage.spouse2_id, []).append(marriage)
        return lookup

    # ------------------------------------------------------------------
    # Position Assignment (birth-year Y, horizontal pairing X)
    # ------------------------------------------------------------------

    def _assign_positions(
        self,
        all_people: list[Person],
        generations: dict[int, int],
        marriage_lookup: dict[int, list[Marriage]],
        earliest_year: int,
        result: LayoutResult,
    ) -> None:
        """Assign (x, y) to every person.

        Y is determined by birth year.
        X groups spouses side-by-side, sorted within each generation to
        keep families together horizontally.
        """
        gen_groups: dict[int, list[Person]] = {}
        for person in all_people:
            if person.id is None:
                continue
            gen = generations.get(person.id, 0)
            gen_groups.setdefault(gen, []).append(person)

        for gen in gen_groups:
            gen_groups[gen].sort(key=lambda p: (p.family_id or 0, p.birth_year or 0))

        sorted_gens = sorted(gen_groups.keys())
        placed_spouses: set[int] = set()

        # Track the X cursor per generation so sibling groups sit together.
        gen_x_cursor: dict[int, float] = {g: 0.0 for g in sorted_gens}

        for gen in sorted_gens:
            people = gen_groups[gen]
            x = gen_x_cursor[gen]

            for person in people:
                if person.id is None or person.id in placed_spouses:
                    continue

                y = self._year_to_y(person.birth_year, earliest_year)

                spouse_id = self._find_same_gen_spouse(
                    person, marriage_lookup, generations, gen
                )

                if spouse_id is not None and spouse_id not in placed_spouses:
                    result.person_positions[person.id] = (self._snap(x), self._snap(y))
                    x += self.BOX_WIDTH + self.MARRIAGE_NODE_GAP

                    # Spouse Y is based on their own birth year.
                    spouse_person = next(
                        (p for p in people if p.id == spouse_id), None
                    )
                    spouse_y = self._year_to_y(
                        spouse_person.birth_year if spouse_person else person.birth_year,
                        earliest_year,
                    )
                    result.person_positions[spouse_id] = (self._snap(x), self._snap(spouse_y))
                    placed_spouses.add(spouse_id)
                    x += self.BOX_WIDTH + self.HORIZONTAL_GAP
                else:
                    result.person_positions[person.id] = (self._snap(x), self._snap(y))
                    x += self.BOX_WIDTH + self.HORIZONTAL_GAP

            gen_x_cursor[gen] = x

    def _find_same_gen_spouse(
        self,
        person: Person,
        marriage_lookup: dict[int, list[Marriage]],
        generations: dict[int, int],
        gen: int,
    ) -> int | None:
        if person.id is None:
            return None
        for marriage in marriage_lookup.get(person.id, []):
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
        self, marriages: list[Marriage], result: LayoutResult
    ) -> None:
        for marriage in marriages:
            if marriage.id is None:
                continue
            s1 = result.person_positions.get(marriage.spouse1_id) if marriage.spouse1_id else None
            s2 = result.person_positions.get(marriage.spouse2_id) if marriage.spouse2_id else None

            if s1 is not None and s2 is not None:
                mid_x = (s1[0] + self.BOX_WIDTH + s2[0]) / 2 - self.MARRIAGE_NODE_SIZE / 2
                mid_y = min(s1[1], s2[1]) + self.BOX_HEIGHT / 2 - self.MARRIAGE_NODE_SIZE / 2
                result.marriage_positions[marriage.id] = (self._snap(mid_x), self._snap(mid_y))
            elif s1 is not None:
                result.marriage_positions[marriage.id] = (
                    self._snap(s1[0] + self.BOX_WIDTH + 10),
                    self._snap(s1[1] + self.BOX_HEIGHT / 2 - self.MARRIAGE_NODE_SIZE / 2),
                )
            elif s2 is not None:
                result.marriage_positions[marriage.id] = (
                    self._snap(s2[0] - self.MARRIAGE_NODE_SIZE - 10),
                    self._snap(s2[1] + self.BOX_HEIGHT / 2 - self.MARRIAGE_NODE_SIZE / 2),
                )

    # ------------------------------------------------------------------
    # Generation Bands (visual guides)
    # ------------------------------------------------------------------

    def _compute_generation_bands(
        self,
        all_people: list[Person],
        generations: dict[int, int],
        earliest_year: int,
        result: LayoutResult,
    ) -> None:
        """Compute band y/height from birth years of people in each gen."""
        gen_years: dict[int, list[int]] = {}
        for person in all_people:
            if person.id is None:
                continue
            gen = generations.get(person.id, 0)
            if person.birth_year is not None:
                gen_years.setdefault(gen, []).append(person.birth_year)

        for gen, years in gen_years.items():
            min_year = min(years)
            max_year = max(years)
            top_y = self._year_to_y(min_year, earliest_year) - self.BAND_PADDING_TOP
            bottom_y = self._year_to_y(max_year, earliest_year) + self.BOX_HEIGHT + self.BAND_PADDING_BOTTOM
            band_height = bottom_y - top_y
            label = f"Gen {gen}"
            result.generation_bands[gen] = (top_y, band_height, label)

    # ------------------------------------------------------------------
    # Year Range
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_year_range(people: list[Person]) -> tuple[int, int]:
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

    # ------------------------------------------------------------------
    # Snap helper
    # ------------------------------------------------------------------

    def _snap(self, value: float) -> float:
        """Snap a coordinate to the nearest grid cell."""
        return round(value / self.GRID_CELL) * self.GRID_CELL
