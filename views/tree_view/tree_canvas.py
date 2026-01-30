"""Main canvas for displaying the family tree."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager

from views.tree_view.person_box import PersonBox
from views.tree_view.marriage_node import MarriageNode
from views.tree_view.relationship_line import RelationshipLine
from views.tree_view.generation_band import GenerationBand
from views.tree_view.layout_engine import TreeLayoutEngine, LayoutResult
from views.tree_view.time_scale import TimeScale


class TreeCanvas(QGraphicsView):
    """Scrollable, zoomable canvas for displaying the family tree."""

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    person_selected: Signal = Signal(int)
    person_double_clicked: Signal = Signal(int)
    marriage_double_clicked: Signal = Signal(int)

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    # Zoom
    ZOOM_FACTOR: float = 1.15
    ZOOM_MIN: float = 0.05
    ZOOM_MAX: float = 3.0

    # Scene
    SCENE_MARGIN: float = 500.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self, db_manager: DatabaseManager, parent=None) -> None:
        """Initialize the tree canvas."""
        super().__init__(parent)
        self.db_manager: DatabaseManager = db_manager
        self._current_zoom: float = 1.0

        self._person_boxes: dict[int, PersonBox] = {}
        self._marriage_nodes: dict[int, MarriageNode] = {}
        self._relationship_lines: list[RelationshipLine] = []
        self._generation_bands: list[GenerationBand] = []

        self._setup_scene()
        self._setup_view()
        self._time_scale: TimeScale = TimeScale(self)

    def _setup_scene(self) -> None:
        """Create and configure the graphics scene."""
        scene: QGraphicsScene = QGraphicsScene(self)
        self.setScene(scene)

    def _setup_view(self) -> None:
        """Configure view rendering and interaction."""
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    # ------------------------------------------------------------------
    # Scene Building
    # ------------------------------------------------------------------

    def rebuild_scene(self) -> None:
        """Clear and rebuild the entire scene from database."""
        self._clear_scene()

        layout: LayoutResult = TreeLayoutEngine(self.db_manager).calculate_layout()

        if not layout.person_positions:
            return

        self._create_generation_bands(layout)
        self._create_person_boxes(layout)
        self._create_marriage_nodes(layout)
        self._create_relationship_lines(layout)

        self._update_scene_rect()
        self._update_time_scale(layout)

    def _clear_scene(self) -> None:
        """Remove all items from the scene."""
        self.scene().clear()
        self._person_boxes.clear()
        self._marriage_nodes.clear()
        self._relationship_lines.clear()
        self._generation_bands.clear()

    # ------------------------------------------------------------------
    # Item Creation
    # ------------------------------------------------------------------

    def _create_generation_bands(self, layout: LayoutResult) -> None:
        """Create generation band backgrounds."""
        for gen, (band_y, band_height) in layout.generation_bands.items():
            band: GenerationBand = GenerationBand(gen, band_y, band_height)
            self.scene().addItem(band)
            self._generation_bands.append(band)

    def _create_person_boxes(self, layout: LayoutResult) -> None:
        """Create person box widgets and position them."""
        for person_id, (x, y) in layout.person_positions.items():
            box: PersonBox = PersonBox(person_id, self.db_manager)
            box.setPos(x, y)
            box.person_selected.connect(self._on_person_selected)
            box.person_double_clicked.connect(self._on_person_double_clicked)
            self.scene().addItem(box)
            self._person_boxes[person_id] = box

    def _create_marriage_nodes(self, layout: LayoutResult) -> None:
        """Create marriage node connectors."""
        for marriage_id, (x, y) in layout.marriage_positions.items():
            node: MarriageNode = MarriageNode(marriage_id, self.db_manager)
            node.setPos(x, y)
            node.marriage_double_clicked.connect(self._on_marriage_double_clicked)
            self.scene().addItem(node)
            self._marriage_nodes[marriage_id] = node

    def _create_relationship_lines(self, layout: LayoutResult) -> None:
        """Create all relationship lines between items."""
        self._create_marriage_lines(layout)
        self._create_parent_child_lines(layout)

    def _create_marriage_lines(self, layout: LayoutResult) -> None:
        """Create horizontal lines connecting spouses through marriage nodes."""
        from database.marriage_repository import MarriageRepository

        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)
        all_marriages = marriage_repo.get_all()

        for marriage in all_marriages:
            if marriage.id is None:
                continue

            node = self._marriage_nodes.get(marriage.id)
            spouse1_box = self._person_boxes.get(marriage.spouse1_id) if marriage.spouse1_id else None
            spouse2_box = self._person_boxes.get(marriage.spouse2_id) if marriage.spouse2_id else None

            if spouse1_box and node:
                line: RelationshipLine = RelationshipLine(
                    RelationshipLine.TYPE_MARRIAGE, spouse1_box, node
                )
                self.scene().addItem(line)
                self._relationship_lines.append(line)

            if node and spouse2_box:
                line = RelationshipLine(
                    RelationshipLine.TYPE_MARRIAGE, node, spouse2_box
                )
                self.scene().addItem(line)
                self._relationship_lines.append(line)

    def _create_parent_child_lines(self, layout: LayoutResult) -> None:
        """Create lines from parents/marriage nodes down to children."""
        from database.person_repository import PersonRepository
        from database.marriage_repository import MarriageRepository

        person_repo: PersonRepository = PersonRepository(self.db_manager)
        marriage_repo: MarriageRepository = MarriageRepository(self.db_manager)

        all_people = person_repo.get_all()
        all_marriages = marriage_repo.get_all()

        marriage_by_couple: dict[tuple[int, int], int] = {}
        for marriage in all_marriages:
            if marriage.spouse1_id and marriage.spouse2_id and marriage.id:
                key = (min(marriage.spouse1_id, marriage.spouse2_id),
                       max(marriage.spouse1_id, marriage.spouse2_id))
                marriage_by_couple[key] = marriage.id

        for person in all_people:
            if person.id is None:
                continue

            child_box = self._person_boxes.get(person.id)
            if child_box is None:
                continue

            parent_marriage_id: int | None = self._find_parent_marriage(
                person, marriage_by_couple
            )

            if parent_marriage_id is not None:
                parent_node = self._marriage_nodes.get(parent_marriage_id)
                if parent_node:
                    line: RelationshipLine = RelationshipLine(
                        RelationshipLine.TYPE_PARENT_CHILD, parent_node, child_box
                    )
                    self.scene().addItem(line)
                    self._relationship_lines.append(line)
            else:
                self._create_direct_parent_line(person, child_box)

    def _find_parent_marriage(self, person, marriage_by_couple) -> int | None:
        """Find a marriage between the person's parents."""
        if person.father_id and person.mother_id:
            key = (min(person.father_id, person.mother_id),
                   max(person.father_id, person.mother_id))
            return marriage_by_couple.get(key)
        return None

    def _create_direct_parent_line(self, person, child_box) -> None:
        """Create a direct parent-to-child line when no marriage node exists."""
        for parent_id in (person.father_id, person.mother_id):
            if parent_id is None:
                continue

            parent_box = self._person_boxes.get(parent_id)
            if parent_box is None:
                continue

            line: RelationshipLine = RelationshipLine(
                RelationshipLine.TYPE_DIRECT_PARENT, parent_box, child_box
            )
            self.scene().addItem(line)
            self._relationship_lines.append(line)

    # ------------------------------------------------------------------
    # Scene Rect / Time Scale
    # ------------------------------------------------------------------

    def _update_scene_rect(self) -> None:
        """Expand scene rect to include all items plus margin."""
        items_rect = self.scene().itemsBoundingRect()
        expanded = items_rect.adjusted(
            -self.SCENE_MARGIN, -self.SCENE_MARGIN,
            self.SCENE_MARGIN, self.SCENE_MARGIN
        )
        self.scene().setSceneRect(expanded)

    def _update_time_scale(self, layout: LayoutResult) -> None:
        """Configure the time scale overlay from layout data."""
        earliest, latest = layout.year_range
        if earliest == 0 and latest == 0:
            return

        self._time_scale.set_year_range(earliest, latest)

        bands = layout.generation_bands
        if bands:
            sorted_gens = sorted(bands.keys())
            top_y = bands[sorted_gens[0]][0]
            last_band = bands[sorted_gens[-1]]
            bottom_y = last_band[0] + last_band[1]
            self._time_scale.set_scene_y_range(top_y, bottom_y)

        self._time_scale.update_geometry()

    # ------------------------------------------------------------------
    # Signal Handlers
    # ------------------------------------------------------------------

    def _on_person_selected(self, person_id: int) -> None:
        """Forward person selection signal."""
        self.person_selected.emit(person_id)

    def _on_person_double_clicked(self, person_id: int) -> None:
        """Forward person double-click signal."""
        self.person_double_clicked.emit(person_id)

    def _on_marriage_double_clicked(self, marriage_id: int) -> None:
        """Forward marriage double-click signal."""
        self.marriage_double_clicked.emit(marriage_id)

    # ------------------------------------------------------------------
    # Zoom
    # ------------------------------------------------------------------

    def wheelEvent(self, event) -> None:
        """Zoom in/out with scroll wheel."""
        if event.angleDelta().y() > 0:
            factor: float = self.ZOOM_FACTOR
        else:
            factor = 1.0 / self.ZOOM_FACTOR

        new_zoom: float = self._current_zoom * factor

        if new_zoom < self.ZOOM_MIN or new_zoom > self.ZOOM_MAX:
            return

        self._current_zoom = new_zoom
        self.scale(factor, factor)
        self._time_scale.update_geometry()
        self._time_scale.update()

    # ------------------------------------------------------------------
    # Resize
    # ------------------------------------------------------------------

    def resizeEvent(self, event) -> None:
        """Update time scale geometry on resize."""
        super().resizeEvent(event)
        self._time_scale.update_geometry()

    # ------------------------------------------------------------------
    # Scroll Updates
    # ------------------------------------------------------------------

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        """Update time scale when the view scrolls."""
        super().scrollContentsBy(dx, dy)
        self._time_scale.update()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def refresh(self) -> None:
        """Rebuild the scene from current database state."""
        self.rebuild_scene()

    def zoom_to_fit(self) -> None:
        """Fit the entire tree in the viewport."""
        self.fitInView(self.scene().itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        transform = self.transform()
        self._current_zoom = transform.m11()
        self._time_scale.update_geometry()
        self._time_scale.update()
