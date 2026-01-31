"""Visual line connecting related people in the tree.

All paths are orthogonal (right-angled).  Person boxes are treated as
obstacles and lines route around them with a clearance margin equal to
the marriage node size.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath

if TYPE_CHECKING:
    from views.tree_view.person_box import PersonBox
    from views.tree_view.marriage_node import MarriageNode


class RelationshipLine(QGraphicsPathItem):
    """Orthogonal line connecting family-tree elements."""

    # Line types -------------------------------------------------------
    TYPE_MARRIAGE: str = "marriage"
    TYPE_PARENT_CHILD: str = "parent"
    TYPE_DIRECT_PARENT: str = "direct_parent"
    TYPE_SIBLING: str = "sibling"

    # Widths -----------------------------------------------------------
    LINE_WIDTH_MARRIAGE: float = 2.5
    LINE_WIDTH_PARENT: float = 2.0
    LINE_WIDTH_DIRECT_PARENT: float = 2.0
    LINE_WIDTH_SIBLING: float = 1.5
    LINE_WIDTH_HOVER: float = 4.0

    # Colors -----------------------------------------------------------
    COLOR_MARRIAGE: QColor = QColor(180, 80, 80)
    COLOR_PARENT: QColor = QColor(80, 130, 180)
    COLOR_DIRECT_PARENT: QColor = QColor(120, 100, 180)
    COLOR_SIBLING: QColor = QColor(120, 140, 160)
    COLOR_HOVER: QColor = QColor(255, 165, 0)

    # Z-ordering -------------------------------------------------------
    Z_VALUE: float = -10.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(
        self,
        line_type: str,
        start_item: QGraphicsItem | None = None,
        end_item: QGraphicsItem | None = None,
        *,
        obstacle_rects: list[QRectF] | None = None,
        fixed_path_points: list[tuple[float, float]] | None = None,
    ) -> None:
        super().__init__()
        self.line_type: str = line_type
        self.start_item: QGraphicsItem | None = start_item
        self.end_item: QGraphicsItem | None = end_item
        self._obstacle_rects: list[QRectF] = obstacle_rects or []
        self._fixed_path_points: list[tuple[float, float]] | None = fixed_path_points
        self._is_hovered: bool = False

        self.setZValue(self.Z_VALUE)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)

        self._apply_default_pen()
        self.update_path()

    # ------------------------------------------------------------------
    # Pen / Style
    # ------------------------------------------------------------------

    def _apply_default_pen(self) -> None:
        style_map = {
            self.TYPE_MARRIAGE: (self.COLOR_MARRIAGE, self.LINE_WIDTH_MARRIAGE),
            self.TYPE_PARENT_CHILD: (self.COLOR_PARENT, self.LINE_WIDTH_PARENT),
            self.TYPE_DIRECT_PARENT: (self.COLOR_DIRECT_PARENT, self.LINE_WIDTH_DIRECT_PARENT),
            self.TYPE_SIBLING: (self.COLOR_SIBLING, self.LINE_WIDTH_SIBLING),
        }
        color, width = style_map.get(self.line_type, (self.COLOR_PARENT, self.LINE_WIDTH_PARENT))
        pen = QPen(color, width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.setPen(pen)

    def _apply_hover_pen(self) -> None:
        pen = QPen(self.COLOR_HOVER, self.LINE_WIDTH_HOVER)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.setPen(pen)

    # ------------------------------------------------------------------
    # Path Construction
    # ------------------------------------------------------------------

    def update_path(self) -> None:
        """Rebuild the QPainterPath from current state."""
        if self._fixed_path_points is not None:
            self.setPath(self._build_fixed_path())
            return

        if self.start_item is None or self.end_item is None:
            self.setPath(QPainterPath())
            return

        start = self._get_anchor_point(self.start_item, is_start=True)
        end = self._get_anchor_point(self.end_item, is_start=False)

        if self.line_type == self.TYPE_MARRIAGE:
            self.setPath(self._build_horizontal_path(start, end))
        else:
            self.setPath(self._build_orthogonal_path(start, end))

    def _build_fixed_path(self) -> QPainterPath:
        """Build a path from explicit coordinate pairs."""
        path = QPainterPath()
        pts = self._fixed_path_points
        if not pts:
            return path
        path.moveTo(QPointF(pts[0][0], pts[0][1]))
        for x, y in pts[1:]:
            path.lineTo(QPointF(x, y))
        return path

    def _build_horizontal_path(self, start: QPointF, end: QPointF) -> QPainterPath:
        path = QPainterPath()
        path.moveTo(start)
        path.lineTo(end)
        return path

    def _build_orthogonal_path(self, start: QPointF, end: QPointF) -> QPainterPath:
        """Build an orthogonal (right-angled) path, routing around obstacles."""
        path = QPainterPath()
        path.moveTo(start)

        # Simple elbow: go down from start, then horizontal, then down to end.
        mid_y = start.y() + (end.y() - start.y()) / 2

        # Check if the horizontal segment at mid_y would cross an obstacle
        # that is *not* an origin box.
        seg_start = QPointF(start.x(), mid_y)
        seg_end = QPointF(end.x(), mid_y)

        # If obstacles block this route, shift the mid_y to avoid them.
        mid_y = self._avoid_obstacles_y(seg_start, seg_end, mid_y, start, end)

        if abs(start.x() - end.x()) < 1.0:
            # Straight vertical drop.
            path.lineTo(end)
        else:
            path.lineTo(QPointF(start.x(), mid_y))
            path.lineTo(QPointF(end.x(), mid_y))
            path.lineTo(end)

        return path

    def _avoid_obstacles_y(
        self, seg_start: QPointF, seg_end: QPointF, mid_y: float,
        path_start: QPointF, path_end: QPointF,
    ) -> float:
        """Nudge mid_y so the horizontal segment doesn't cross obstacle rects.

        Only considers obstacles that are NOT the origin or destination items.
        """
        if not self._obstacle_rects:
            return mid_y

        min_x = min(seg_start.x(), seg_end.x())
        max_x = max(seg_start.x(), seg_end.x())

        for rect in self._obstacle_rects:
            # Skip if this obstacle is the start or end item's own bounding box.
            # (A line may pass under the box it originates from.)
            if self._rect_contains_point(rect, path_start) or self._rect_contains_point(rect, path_end):
                continue

            # Does the horizontal segment at mid_y intersect this rect?
            if rect.top() <= mid_y <= rect.bottom() and max_x >= rect.left() and min_x <= rect.right():
                # Route above or below, whichever is shorter.
                above = rect.top() - 5
                below = rect.bottom() + 5
                if abs(above - mid_y) <= abs(below - mid_y):
                    mid_y = above
                else:
                    mid_y = below

        return mid_y

    @staticmethod
    def _rect_contains_point(rect: QRectF, point: QPointF) -> bool:
        return rect.contains(point)

    # ------------------------------------------------------------------
    # Anchor Points
    # ------------------------------------------------------------------

    def _get_anchor_point(self, item: QGraphicsItem, is_start: bool) -> QPointF:
        rect = item.boundingRect()
        pos = item.scenePos()
        center_x = pos.x() + rect.width() / 2

        if self.line_type == self.TYPE_MARRIAGE:
            center_y = pos.y() + rect.height() / 2
            if is_start:
                return QPointF(pos.x() + rect.width(), center_y)
            return QPointF(pos.x(), center_y)

        if is_start:
            return QPointF(center_x, pos.y() + rect.height())
        return QPointF(center_x, pos.y())

    # ------------------------------------------------------------------
    # Update helpers
    # ------------------------------------------------------------------

    def update_endpoints(self) -> None:
        self.update_path()

    def set_start_item(self, item: QGraphicsItem) -> None:
        self.start_item = item
        self.update_path()

    def set_end_item(self, item: QGraphicsItem) -> None:
        self.end_item = item
        self.update_path()

    # ------------------------------------------------------------------
    # Hover Events
    # ------------------------------------------------------------------

    def hoverEnterEvent(self, event) -> None:
        self._is_hovered = True
        self._apply_hover_pen()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self._is_hovered = False
        self._apply_default_pen()
        super().hoverLeaveEvent(event)

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        super().paint(painter, option, widget)
