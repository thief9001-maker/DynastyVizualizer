"""Main canvas for displaying the family tree."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, Signal, QRectF
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

    ZOOM_FACTOR: float = 1.15
    ZOOM_MIN: float = 0.05
    ZOOM_MAX: float = 3.0

    SCENE_MARGIN: float = 500.0
    GRID_CELL: float = 20.0

    # How many extra "person box widths" of empty space on the right.
    RIGHT_PADDING_BOXES: int = 2

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self, db_manager: DatabaseManager, parent=None) -> None:
        super().__init__(parent)
        self.db_manager: DatabaseManager = db_manager
        self._current_zoom: float = 1.0
        self._layout: LayoutResult | None = None

        self._person_boxes: dict[int, PersonBox] = {}
        self._marriage_nodes: dict[int, MarriageNode] = {}
        self._relationship_lines: list[RelationshipLine] = []
        self._generation_bands: list[GenerationBand] = []

        self._setup_scene()
        self._setup_view()
        self._time_scale: TimeScale = TimeScale(self)

    def _setup_scene(self) -> None:
        scene = QGraphicsScene(self)
        self.setScene(scene)

    def _setup_view(self) -> None:
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

        layout = TreeLayoutEngine(self.db_manager).calculate_layout()
        self._layout = layout

        if not layout.person_positions:
            return

        self._create_generation_bands(layout)
        self._create_person_boxes(layout)
        self._create_marriage_nodes(layout)
        self._create_relationship_lines(layout)

        self._update_scene_rect(layout)
        self._update_time_scale(layout)

    def _clear_scene(self) -> None:
        self.scene().clear()
        self._person_boxes.clear()
        self._marriage_nodes.clear()
        self._relationship_lines.clear()
        self._generation_bands.clear()

    # ------------------------------------------------------------------
    # Item Creation
    # ------------------------------------------------------------------

    def _create_generation_bands(self, layout: LayoutResult) -> None:
        # Determine left-most person x and place label 2 box-widths to the left.
        min_x = 0.0
        if layout.person_positions:
            min_x = min(x for x, _ in layout.person_positions.values())
        label_offset = min_x - 2 * PersonBox.BOX_MIN_WIDTH

        for gen, (band_y, band_height, label) in layout.generation_bands.items():
            band = GenerationBand(gen, band_y, band_height, label_text=label)
            band.set_label_x_offset(label_offset)
            self.scene().addItem(band)
            self._generation_bands.append(band)

    def _create_person_boxes(self, layout: LayoutResult) -> None:
        for person_id, (x, y) in layout.person_positions.items():
            box = PersonBox(person_id, self.db_manager)
            box.setPos(x, y)
            box.person_selected.connect(self._on_person_selected)
            box.person_double_clicked.connect(self._on_person_double_clicked)
            box.navigate_to_person.connect(self._navigate_to_person)
            self.scene().addItem(box)
            self._person_boxes[person_id] = box

    def _create_marriage_nodes(self, layout: LayoutResult) -> None:
        for marriage_id, (x, y) in layout.marriage_positions.items():
            node = MarriageNode(marriage_id, self.db_manager)
            node.setPos(x, y)
            node.marriage_double_clicked.connect(self._on_marriage_double_clicked)
            self.scene().addItem(node)
            self._marriage_nodes[marriage_id] = node

    def _create_relationship_lines(self, layout: LayoutResult) -> None:
        self._create_marriage_lines(layout)
        self._create_parent_child_lines(layout)

    def _create_marriage_lines(self, layout: LayoutResult) -> None:
        from database.marriage_repository import MarriageRepository

        all_marriages = MarriageRepository(self.db_manager).get_all()

        for marriage in all_marriages:
            if marriage.id is None:
                continue
            node = self._marriage_nodes.get(marriage.id)
            s1 = self._person_boxes.get(marriage.spouse1_id) if marriage.spouse1_id else None
            s2 = self._person_boxes.get(marriage.spouse2_id) if marriage.spouse2_id else None

            if s1 and node:
                line = RelationshipLine(RelationshipLine.TYPE_MARRIAGE, s1, node)
                self.scene().addItem(line)
                self._relationship_lines.append(line)
                self._register_line(line)
            if node and s2:
                line = RelationshipLine(RelationshipLine.TYPE_MARRIAGE, node, s2)
                self.scene().addItem(line)
                self._relationship_lines.append(line)
                self._register_line(line)

    def _create_parent_child_lines(self, layout: LayoutResult) -> None:
        from database.person_repository import PersonRepository
        from database.marriage_repository import MarriageRepository

        all_people = PersonRepository(self.db_manager).get_all()
        all_marriages = MarriageRepository(self.db_manager).get_all()

        marriage_by_couple: dict[tuple[int, int], int] = {}
        for m in all_marriages:
            if m.spouse1_id and m.spouse2_id and m.id:
                key = (min(m.spouse1_id, m.spouse2_id), max(m.spouse1_id, m.spouse2_id))
                marriage_by_couple[key] = m.id

        # Group children by their parent-marriage (or single-parent).
        # This lets us draw a shared horizontal sibling bar.
        from collections import defaultdict
        sibling_groups: dict[str, list[int]] = defaultdict(list)

        for person in all_people:
            if person.id is None:
                continue
            child_box = self._person_boxes.get(person.id)
            if child_box is None:
                continue

            mid = self._find_parent_marriage(person, marriage_by_couple)
            if mid is not None:
                sibling_groups[f"m:{mid}"].append(person.id)
            else:
                # Single-parent: group by whichever parent exists.
                for pid in (person.father_id, person.mother_id):
                    if pid is not None and pid in self._person_boxes:
                        sibling_groups[f"p:{pid}"].append(person.id)

        # Now draw lines for each sibling group.
        obstacle_rects = self._collect_obstacle_rects()

        for group_key, child_ids in sibling_groups.items():
            if not child_ids:
                continue

            if group_key.startswith("m:"):
                mid = int(group_key[2:])
                parent_node = self._marriage_nodes.get(mid)
                if parent_node is None:
                    continue
                self._draw_sibling_group_lines(parent_node, child_ids, obstacle_rects, from_marriage=True)
            else:
                pid = int(group_key[2:])
                parent_box = self._person_boxes.get(pid)
                if parent_box is None:
                    continue
                self._draw_sibling_group_lines(parent_box, child_ids, obstacle_rects, from_marriage=False)

    def _draw_sibling_group_lines(self, parent_item, child_ids, obstacle_rects, from_marriage: bool) -> None:
        """Draw orthogonal lines from parent_item down to children with a shared horizontal bar."""
        boxes = [self._person_boxes[cid] for cid in child_ids if cid in self._person_boxes]
        if not boxes:
            return

        if len(boxes) == 1:
            line_type = RelationshipLine.TYPE_PARENT_CHILD if from_marriage else RelationshipLine.TYPE_DIRECT_PARENT
            line = RelationshipLine(line_type, parent_item, boxes[0], obstacle_rects=obstacle_rects)
            self.scene().addItem(line)
            self._relationship_lines.append(line)
            self._register_line(line)
            return

        # Multiple children: draw a shared horizontal sibling bar.
        # Vertical line from parent down to bar Y, then horizontal across,
        # then vertical drops to each child.
        parent_rect = parent_item.boundingRect()
        parent_pos = parent_item.scenePos()
        parent_bottom_x = parent_pos.x() + parent_rect.width() / 2
        parent_bottom_y = parent_pos.y() + parent_rect.height()

        # Bar Y is halfway between parent bottom and topmost child.
        child_tops = [b.scenePos().y() for b in boxes]
        min_child_y = min(child_tops)
        bar_y = parent_bottom_y + (min_child_y - parent_bottom_y) / 2

        # Vertical drop from parent to bar.
        line_type = RelationshipLine.TYPE_PARENT_CHILD if from_marriage else RelationshipLine.TYPE_DIRECT_PARENT
        drop_line = RelationshipLine(
            line_type, parent_item, None,
            fixed_path_points=[(parent_bottom_x, parent_bottom_y), (parent_bottom_x, bar_y)],
        )
        self.scene().addItem(drop_line)
        self._relationship_lines.append(drop_line)
        self._register_line(drop_line)

        # Horizontal sibling bar.
        child_centers = sorted(b.scenePos().x() + b.boundingRect().width() / 2 for b in boxes)
        bar_line = RelationshipLine(
            RelationshipLine.TYPE_SIBLING, None, None,
            fixed_path_points=[(child_centers[0], bar_y), (child_centers[-1], bar_y)],
        )
        self.scene().addItem(bar_line)
        self._relationship_lines.append(bar_line)
        self._register_line(bar_line)

        # Connect horizontal bar junction at parent_bottom_x to the bar if needed
        # (parent may not be centered on the bar).
        # This is already handled by the drop line ending at bar_y.

        # Vertical drops from bar to each child.
        for box in boxes:
            child_pos = box.scenePos()
            child_top_x = child_pos.x() + box.boundingRect().width() / 2
            child_top_y = child_pos.y()
            child_drop = RelationshipLine(
                line_type, None, box,
                fixed_path_points=[(child_top_x, bar_y), (child_top_x, child_top_y)],
            )
            self.scene().addItem(child_drop)
            self._relationship_lines.append(child_drop)
            self._register_line(child_drop)

    def _find_parent_marriage(self, person, marriage_by_couple) -> int | None:
        if person.father_id and person.mother_id:
            key = (min(person.father_id, person.mother_id), max(person.father_id, person.mother_id))
            return marriage_by_couple.get(key)
        return None

    def _register_line(self, line: RelationshipLine) -> None:
        """Register a line on its connected items for live redraw on drag."""
        for item in (line.start_item, line.end_item):
            if item is not None and hasattr(item, '_connected_lines'):
                item._connected_lines.append(line)

    def _collect_obstacle_rects(self) -> list[QRectF]:
        """Collect bounding rectangles of all person boxes for obstacle avoidance."""
        rects: list[QRectF] = []
        for box in self._person_boxes.values():
            pos = box.scenePos()
            rect = box.boundingRect()
            margin = MarriageNode.NODE_SIZE
            rects.append(QRectF(
                pos.x() - margin, pos.y() - margin,
                rect.width() + 2 * margin, rect.height() + 2 * margin,
            ))
        return rects

    # ------------------------------------------------------------------
    # Scene Rect / Time Scale
    # ------------------------------------------------------------------

    def _update_scene_rect(self, layout: LayoutResult) -> None:
        """Size scene to content: vertical by year range, horizontal by boxes."""
        items_rect = self.scene().itemsBoundingRect()

        # Right boundary: rightmost box + 2 box widths.
        max_x = 0.0
        if layout.person_positions:
            max_x = max(x for x, _ in layout.person_positions.values())
        right_wall = max_x + PersonBox.BOX_MIN_WIDTH * (1 + self.RIGHT_PADDING_BOXES)

        expanded = QRectF(
            items_rect.left() - self.SCENE_MARGIN,
            items_rect.top() - self.SCENE_MARGIN,
            max(items_rect.width(), right_wall - items_rect.left()) + self.SCENE_MARGIN,
            items_rect.height() + 2 * self.SCENE_MARGIN,
        )
        self.scene().setSceneRect(expanded)

    def _update_time_scale(self, layout: LayoutResult) -> None:
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
        self.person_selected.emit(person_id)

    def _on_person_double_clicked(self, person_id: int) -> None:
        self.person_double_clicked.emit(person_id)

    def _on_marriage_double_clicked(self, marriage_id: int) -> None:
        self.marriage_double_clicked.emit(marriage_id)

    def _navigate_to_person(self, person_id: int) -> None:
        """Center the view on a person and open their locked tooltip."""
        box = self._person_boxes.get(person_id)
        if box is None:
            return
        # Center the view on this box.
        self.centerOn(box)
        # Trigger the tooltip by simulating a hover (call the internal method).
        if hasattr(box, '_create_enhanced_tooltip'):
            box._create_enhanced_tooltip()
            if box._tooltip_panel is not None:
                box._tooltip_panel.is_locked = True

    # ------------------------------------------------------------------
    # Scroll / Zoom  (scroll = wheel, zoom = Ctrl+wheel)
    # ------------------------------------------------------------------

    def wheelEvent(self, event) -> None:
        """Scroll wheel scrolls; Ctrl+wheel zooms."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Zoom
            if event.angleDelta().y() > 0:
                factor = self.ZOOM_FACTOR
            else:
                factor = 1.0 / self.ZOOM_FACTOR

            new_zoom = self._current_zoom * factor
            if new_zoom < self.ZOOM_MIN or new_zoom > self.ZOOM_MAX:
                return

            self._current_zoom = new_zoom
            self.scale(factor, factor)
            self._time_scale.update_geometry()
            self._time_scale.update()
        else:
            # Normal scroll
            super().wheelEvent(event)
            self._time_scale.update()

    # ------------------------------------------------------------------
    # Resize / Scroll helpers
    # ------------------------------------------------------------------

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._time_scale.update_geometry()

    def scrollContentsBy(self, dx: int, dy: int) -> None:
        super().scrollContentsBy(dx, dy)
        self._time_scale.update()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def refresh(self) -> None:
        self.rebuild_scene()

    def zoom_to_fit(self) -> None:
        self.fitInView(self.scene().itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        transform = self.transform()
        self._current_zoom = transform.m11()
        self._time_scale.update_geometry()
        self._time_scale.update()

    # ------------------------------------------------------------------
    # Snap helper (used by PersonBox / MarriageNode on drop)
    # ------------------------------------------------------------------

    @staticmethod
    def snap_to_grid(value: float, cell: float = 20.0) -> float:
        return round(value / cell) * cell
