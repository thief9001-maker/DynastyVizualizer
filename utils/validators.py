"""Data validation tools for detecting inconsistencies."""

from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from database.person_repository import PersonRepository
    from models.person import Person
    from models.marriage import Marriage


@dataclass
class ValidationIssue:
    """Represents a data validation issue."""
    
    issue_type: str
    category: str
    message: str
    entity_type: str

    TYPE_ERROR: str = "error"
    TYPE_WARNING: str = "warning"
    TYPE_INFO: str = "info"
    
    entity_id: int | None = None
    details: dict | None = None


class MarriageValidator:
    """Validate marriage data for inconsistencies."""
    
    CATEGORY_OVERLAPPING: str = "overlapping_marriages"
    CATEGORY_INVALID_DATE: str = "invalid_date"
    CATEGORY_SELF_MARRIAGE: str = "self_marriage"
    CATEGORY_IMPOSSIBLE_AGE: str = "impossible_age"
    CATEGORY_DEATH_CONFLICT: str = "death_conflict"
    
    MIN_MARRIAGE_AGE: int = 12
    MAX_REASONABLE_AGE_GAP: int = 50
    
    def __init__(self, database_connection: DatabaseManager) -> None:
        """Initialize the marriage validator."""
        self.db: DatabaseManager = database_connection
    
    def validate_all(self) -> list[ValidationIssue]:
        """Check all marriages for issues."""
        from database.marriage_repository import MarriageRepository
        
        marriage_repo: MarriageRepository = MarriageRepository(self.db)
        issues: list[ValidationIssue] = []
        
        marriages: list[Marriage] = self._get_all_marriages(marriage_repo)
        
        for marriage in marriages:
            issues.extend(self._validate_marriage(marriage))
        
        issues.extend(self._check_overlapping_marriages(marriages))
        
        return issues
    
    def _get_all_marriages(self, marriage_repo) -> list[Marriage]:
        """Get all marriages from repository."""
        return []
    
    def _validate_marriage(self, marriage: Marriage) -> list[ValidationIssue]:
        """Validate a single marriage."""
        issues: list[ValidationIssue] = []
        
        self_marriage_issue: ValidationIssue | None = self._check_self_marriage(marriage)
        if self_marriage_issue:
            issues.append(self_marriage_issue)
        
        date_issue: ValidationIssue | None = self._check_marriage_dates(marriage)
        if date_issue:
            issues.append(date_issue)
        
        age_issues: list[ValidationIssue] = self._check_spouse_ages(marriage)
        issues.extend(age_issues)
        
        death_issue: ValidationIssue | None = self._check_death_conflicts(marriage)
        if death_issue:
            issues.append(death_issue)
        
        return issues
    
    def _check_self_marriage(self, marriage: Marriage) -> ValidationIssue | None:
        """Check if person is married to themselves."""
        if marriage.spouse1_id == marriage.spouse2_id:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_ERROR,
                category=self.CATEGORY_SELF_MARRIAGE,
                message="Person cannot be married to themselves",
                entity_type="Marriage",
                entity_id=marriage.id,
                details={"spouse_id": marriage.spouse1_id}
            )
        return None
    
    def _check_marriage_dates(self, marriage: Marriage) -> ValidationIssue | None:
        """Check if marriage dates are valid."""
        if marriage.marriage_year is None:
            return None
        
        if not marriage.dissolution_year:
            return None
        
        if marriage.dissolution_year < marriage.marriage_year:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_ERROR,
                category=self.CATEGORY_INVALID_DATE,
                message="Marriage ended before it started",
                entity_type="Marriage",
                entity_id=marriage.id,
                details={
                    "marriage_year": marriage.marriage_year,
                    "dissolution_year": marriage.dissolution_year
                }
            )

        if marriage.dissolution_year != marriage.marriage_year:
            return None
        
        if not (marriage.marriage_month and marriage.dissolution_month):
            return None
        
        if marriage.dissolution_month < marriage.marriage_month:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_ERROR,
                category=self.CATEGORY_INVALID_DATE,
                message="Marriage ended before it started (same year, earlier month)",
                entity_type="Marriage",
                entity_id=marriage.id
            )
        
        return None
    
    def _check_spouse_ages(self, marriage: Marriage) -> list[ValidationIssue]:
        """Check if spouses were reasonable age at marriage."""
        from database.person_repository import PersonRepository
        
        issues: list[ValidationIssue] = []
        
        if marriage.marriage_year is None:
            return issues
        
        person_repo: PersonRepository = PersonRepository(self.db)
        
        if marriage.spouse1_id:
            spouse1: Person | None = person_repo.get_by_id(marriage.spouse1_id)
            if spouse1:
                spouse1_issue: ValidationIssue | None = self._check_single_spouse_age(
                    marriage, spouse1, "spouse1"
                )
                if spouse1_issue:
                    issues.append(spouse1_issue)
        
        if marriage.spouse2_id:
            spouse2: Person | None = person_repo.get_by_id(marriage.spouse2_id)
            if spouse2:
                spouse2_issue: ValidationIssue | None = self._check_single_spouse_age(
                    marriage, spouse2, "spouse2"
                )
                if spouse2_issue:
                    issues.append(spouse2_issue)
        
        return issues
    
    def _check_single_spouse_age(
        self,
        marriage: Marriage,
        spouse: Person,
        spouse_label: str
    ) -> ValidationIssue | None:
        """Check if a single spouse was reasonable age at marriage."""
        if spouse.birth_year is None or marriage.marriage_year is None:
            return None
        
        age_at_marriage: int = marriage.marriage_year - spouse.birth_year
        
        if age_at_marriage < 0:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_ERROR,
                category=self.CATEGORY_IMPOSSIBLE_AGE,
                message="Person married before they were born",
                entity_type="Marriage",
                entity_id=marriage.id,
                details={
                    "person_id": spouse.id,
                    "person_name": spouse.display_name,
                    "spouse": spouse_label
                }
            )
        
        if age_at_marriage < self.MIN_MARRIAGE_AGE:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_WARNING,
                category=self.CATEGORY_IMPOSSIBLE_AGE,
                message=f"Person was very young at marriage (age {age_at_marriage})",
                entity_type="Marriage",
                entity_id=marriage.id,
                details={
                    "person_id": spouse.id,
                    "person_name": spouse.display_name,
                    "age_at_marriage": age_at_marriage,
                    "spouse": spouse_label
                }
            )
        
        return None
    
    def _check_death_conflicts(self, marriage: Marriage) -> ValidationIssue | None:
        """Check if marriage occurred after death of spouse."""
        from database.person_repository import PersonRepository
        
        if marriage.marriage_year is None:
            return None
        
        person_repo: PersonRepository = PersonRepository(self.db)
        
        for spouse_id, spouse_label in [(marriage.spouse1_id, "spouse1"), (marriage.spouse2_id, "spouse2")]:
            if not spouse_id:
                continue
            
            spouse: Person | None = person_repo.get_by_id(spouse_id)
            if not spouse or spouse.death_year is None:
                continue
            
            if marriage.marriage_year > spouse.death_year:
                return ValidationIssue(
                    issue_type=ValidationIssue.TYPE_ERROR,
                    category=self.CATEGORY_DEATH_CONFLICT,
                    message="Marriage occurred after death of spouse",
                    entity_type="Marriage",
                    entity_id=marriage.id,
                    details={
                        "person_id": spouse.id,
                        "person_name": spouse.display_name,
                        "death_year": spouse.death_year,
                        "marriage_year": marriage.marriage_year
                    }
                )
        
        return None
    
    def _check_overlapping_marriages(self, marriages: list[Marriage]) -> list[ValidationIssue]:
        """Check for overlapping marriages for each person."""
        from database.person_repository import PersonRepository
        
        issues: list[ValidationIssue] = []
        person_repo: PersonRepository = PersonRepository(self.db)
        
        person_ids: set[int] = set()
        for marriage in marriages:
            if marriage.spouse1_id:
                person_ids.add(marriage.spouse1_id)
            if marriage.spouse2_id:
                person_ids.add(marriage.spouse2_id)
        
        for person_id in person_ids:
            person_marriages: list[Marriage] = self._get_marriages_for_person(marriages, person_id)
            overlap_issues: list[ValidationIssue] = self._find_overlapping_marriages(
                person_marriages, person_id, person_repo
            )
            issues.extend(overlap_issues)
        
        return issues
    
    @staticmethod
    def _get_marriages_for_person(marriages: list[Marriage], person_id: int) -> list[Marriage]:
        """Get all marriages for a specific person."""
        return [
            m for m in marriages
            if m.spouse1_id == person_id or m.spouse2_id == person_id
        ]
    
    def _find_overlapping_marriages(
        self,
        marriages: list[Marriage],
        person_id: int,
        person_repo: PersonRepository
    ) -> list[ValidationIssue]:
        """Find overlapping marriages for a person."""
        issues: list[ValidationIssue] = []
        
        sorted_marriages: list[Marriage] = sorted(
            marriages,
            key=lambda m: m.marriage_year if m.marriage_year else 0
        )
        
        for i, marriage1 in enumerate(sorted_marriages):
            for marriage2 in sorted_marriages[i + 1:]:
                overlap_issue: ValidationIssue | None = self._check_marriage_overlap(
                    marriage1, marriage2, person_id, person_repo
                )
                if overlap_issue:
                    issues.append(overlap_issue)
        
        return issues
    
    def _check_marriage_overlap(
        self,
        marriage1: Marriage,
        marriage2: Marriage,
        person_id: int,
        person_repo: PersonRepository
    ) -> ValidationIssue | None:
        """Check if two marriages overlap in time."""
        if marriage1.marriage_year is None or marriage2.marriage_year is None:
            return None
        
        if marriage1.dissolution_year is None:
            return self._create_overlap_issue(marriage1, marriage2, person_id, person_repo)
        
        if marriage1.dissolution_year >= marriage2.marriage_year:
            return self._create_overlap_issue(marriage1, marriage2, person_id, person_repo)
        
        return None
    
    def _create_overlap_issue(
        self,
        marriage1: Marriage,
        marriage2: Marriage,
        person_id: int,
        person_repo: PersonRepository
    ) -> ValidationIssue:
        """Create a validation issue for overlapping marriages."""
        person: Person | None = person_repo.get_by_id(person_id)
        person_name: str = person.display_name if person else f"Person {person_id}"
        
        return ValidationIssue(
            issue_type=ValidationIssue.TYPE_WARNING,
            category=self.CATEGORY_OVERLAPPING,
            message=f"Overlapping marriages detected for {person_name}",
            entity_type="Marriage",
            entity_id=marriage1.id,
            details={
                "person_id": person_id,
                "person_name": person_name,
                "marriage1_id": marriage1.id,
                "marriage2_id": marriage2.id,
                "marriage1_year": marriage1.marriage_year,
                "marriage2_year": marriage2.marriage_year
            }
        )


class ParentageValidator:
    """Validate parent-child relationships."""
    
    CATEGORY_CIRCULAR: str = "circular_parentage"
    CATEGORY_IMPOSSIBLE_AGE: str = "impossible_age"
    CATEGORY_GENDER_MISMATCH: str = "gender_mismatch"
    CATEGORY_DEATH_CONFLICT: str = "death_conflict"
    
    MIN_PARENT_AGE: int = 12
    MAX_REASONABLE_PARENT_AGE: int = 60
    MIN_REASONABLE_PARENT_AGE: int = 15
    
    def __init__(self, database_connection: DatabaseManager) -> None:
        """Initialize the parentage validator."""
        self.db: DatabaseManager = database_connection
    
    def validate_all(self) -> list[ValidationIssue]:
        """Check all parentage relationships for issues."""
        from database.person_repository import PersonRepository
        
        person_repo: PersonRepository = PersonRepository(self.db)
        issues: list[ValidationIssue] = []
        
        all_people: list[Person] = person_repo.get_all()
        
        for person in all_people:
            issues.extend(self._validate_person_parentage(person, person_repo))
        
        return issues
    
    def _validate_person_parentage(
        self,
        person: Person,
        person_repo: PersonRepository
    ) -> list[ValidationIssue]:
        """Validate parentage for a single person."""
        issues: list[ValidationIssue] = []
        
        circular_issue: ValidationIssue | None = self._check_circular_parentage(person, person_repo)
        if circular_issue:
            issues.append(circular_issue)
        
        if person.father_id:
            father_issues: list[ValidationIssue] = self._validate_parent(
                person, person.father_id, "father", person_repo
            )
            issues.extend(father_issues)
        
        if person.mother_id:
            mother_issues: list[ValidationIssue] = self._validate_parent(
                person, person.mother_id, "mother", person_repo
            )
            issues.extend(mother_issues)
        
        return issues
    
    def _check_circular_parentage(
        self,
        person: Person,
        person_repo: PersonRepository
    ) -> ValidationIssue | None:
        """Check for circular parent-child relationships."""
        if person.id is None:
            return None
        
        visited: set[int] = set()
        current_id: int | None = person.id
        
        while current_id is not None:
            if current_id in visited:
                return ValidationIssue(
                    issue_type=ValidationIssue.TYPE_ERROR,
                    category=self.CATEGORY_CIRCULAR,
                    message="Circular parentage detected in family tree",
                    entity_type="Person",
                    entity_id=person.id,
                    details={"circular_person_id": current_id}
                )
            
            visited.add(current_id)
            current_person: Person | None = person_repo.get_by_id(current_id)
            
            if not current_person:
                break
            
            current_id = current_person.father_id
        
        return None
    
    def _validate_parent(
        self,
        child: Person,
        parent_id: int,
        parent_type: str,
        person_repo: PersonRepository
    ) -> list[ValidationIssue]:
        """Validate a parent-child relationship."""
        issues: list[ValidationIssue] = []
        
        parent: Person | None = person_repo.get_by_id(parent_id)
        if not parent:
            return issues
        
        gender_issue: ValidationIssue | None = self._check_parent_gender(child, parent, parent_type)
        if gender_issue:
            issues.append(gender_issue)
        
        age_issue: ValidationIssue | None = self._check_parent_age(child, parent, parent_type)
        if age_issue:
            issues.append(age_issue)
        
        death_issue: ValidationIssue | None = self._check_parent_alive_at_birth(
            child, parent, parent_type
        )
        if death_issue:
            issues.append(death_issue)
        
        return issues
    
    def _check_parent_gender(
        self,
        child: Person,
        parent: Person,
        parent_type: str
    ) -> ValidationIssue | None:
        """Check if parent's gender matches their role."""
        expected_gender: str = Person.GENDER_MALE if parent_type == "father" else Person.GENDER_FEMALE
        
        if parent.gender != expected_gender and parent.gender != Person.GENDER_UNKNOWN:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_WARNING,
                category=self.CATEGORY_GENDER_MISMATCH,
                message=f"{parent_type.capitalize()} has unexpected gender",
                entity_type="Person",
                entity_id=child.id,
                details={
                    "child_name": child.display_name,
                    "parent_id": parent.id,
                    "parent_name": parent.display_name,
                    "parent_type": parent_type,
                    "expected_gender": expected_gender,
                    "actual_gender": parent.gender
                }
            )
        
        return None
    
    def _check_parent_age(
        self,
        child: Person,
        parent: Person,
        parent_type: str
    ) -> ValidationIssue | None:
        """Check if parent was reasonable age at child's birth."""
        if child.birth_year is None or parent.birth_year is None:
            return None
        
        parent_age_at_birth: int = child.birth_year - parent.birth_year
        
        if parent_age_at_birth < 0:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_ERROR,
                category=self.CATEGORY_IMPOSSIBLE_AGE,
                message=f"{parent_type.capitalize()} was born after child",
                entity_type="Person",
                entity_id=child.id,
                details={
                    "child_name": child.display_name,
                    "parent_id": parent.id,
                    "parent_name": parent.display_name,
                    "parent_type": parent_type,
                    "parent_age": parent_age_at_birth
                }
            )
        
        if parent_age_at_birth < self.MIN_PARENT_AGE:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_ERROR,
                category=self.CATEGORY_IMPOSSIBLE_AGE,
                message=f"{parent_type.capitalize()} was very young at child's birth (age {parent_age_at_birth})",
                entity_type="Person",
                entity_id=child.id,
                details={
                    "child_name": child.display_name,
                    "parent_id": parent.id,
                    "parent_name": parent.display_name,
                    "parent_type": parent_type,
                    "parent_age": parent_age_at_birth
                }
            )
        
        if parent_age_at_birth < self.MIN_REASONABLE_PARENT_AGE:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_WARNING,
                category=self.CATEGORY_IMPOSSIBLE_AGE,
                message=f"{parent_type.capitalize()} was unusually young at child's birth (age {parent_age_at_birth})",
                entity_type="Person",
                entity_id=child.id,
                details={
                    "child_name": child.display_name,
                    "parent_id": parent.id,
                    "parent_name": parent.display_name,
                    "parent_type": parent_type,
                    "parent_age": parent_age_at_birth
                }
            )
        
        if parent_age_at_birth > self.MAX_REASONABLE_PARENT_AGE:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_WARNING,
                category=self.CATEGORY_IMPOSSIBLE_AGE,
                message=f"{parent_type.capitalize()} was unusually old at child's birth (age {parent_age_at_birth})",
                entity_type="Person",
                entity_id=child.id,
                details={
                    "child_name": child.display_name,
                    "parent_id": parent.id,
                    "parent_name": parent.display_name,
                    "parent_type": parent_type,
                    "parent_age": parent_age_at_birth
                }
            )
        
        return None
    
    def _check_parent_alive_at_birth(
        self,
        child: Person,
        parent: Person,
        parent_type: str
    ) -> ValidationIssue | None:
        """Check if parent was alive when child was born."""
        if child.birth_year is None or parent.death_year is None:
            return None
        
        if parent.death_year < child.birth_year:
            return ValidationIssue(
                issue_type=ValidationIssue.TYPE_ERROR,
                category=self.CATEGORY_DEATH_CONFLICT,
                message=f"{parent_type.capitalize()} died before child was born",
                entity_type="Person",
                entity_id=child.id,
                details={
                    "child_name": child.display_name,
                    "child_birth_year": child.birth_year,
                    "parent_id": parent.id,
                    "parent_name": parent.display_name,
                    "parent_type": parent_type,
                    "parent_death_year": parent.death_year
                }
            )
        
        return None