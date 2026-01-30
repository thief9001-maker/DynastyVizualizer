"""Visual line connecting related people in the tree."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath

if TYPE_CHECKING:
    from views.tree_view.person_box import PersonBox
    from views.tree_view.marriage_node import MarriageNode


class RelationshipLine(QGraphicsPathItem):
    """Line connecting parent to child, spouse to spouse, or direct parent link."""

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    # Line types
    TYPE_MARRIAGE: str = "marriage"
    TYPE_PARENT_CHILD: str = "parent"
    TYPE_DIRECT_PARENT: str = "direct_parent"
    TYPE_SIBLING: str = "sibling"

    # Line styles by type
    LINE_WIDTH_MARRIAGE: float = 2.5
    LINE_WIDTH_PARENT: float = 2.0
    LINE_WIDTH_DIRECT_PARENT: float = 2.0
    LINE_WIDTH_SIBLING: float = 1.0
    LINE_WIDTH_HOVER: float = 4.0

    # Colors
    COLOR_MARRIAGE: QColor = QColor(180, 80, 80)
    COLOR_PARENT: QColor = QColor(80, 130, 180)
    COLOR_DIRECT_PARENT: QColor = QColor(120, 100, 180)
    COLOR_SIBLING: QColor = QColor(160, 160, 160)
    COLOR_HOVER: QColor = QColor(255, 165, 0)
    COLOR_SELECTED: QColor = QColor(33, 150, 243)

    # Elbow line spacing
    ELBOW_DROP: float = 20.0

    # Z-ordering (above bands, below boxes)
    Z_VALUE: float = -10.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(
        self,
        line_type: str,
        start_item: QGraphicsItem | None = None,
        end_item: QGraphicsItem | None = None
    ) -> None:
        """Initialize the relationship line."""
        super().__init__()
        self.line_type: str = line_type
        self.start_item: QGraphicsItem | None = start_item
        self.end_item: QGraphicsItem | None = end_item
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
        """Set the pen based on line type."""
        color: QColor
        width: float

        if self.line_type == self.TYPE_MARRIAGE:
            color = self.COLOR_MARRIAGE
            width = self.LINE_WIDTH_MARRIAGE
        elif self.line_type == self.TYPE_PARENT_CHILD:
            color = self.COLOR_PARENT
            width = self.LINE_WIDTH_PARENT
        elif self.line_type == self.TYPE_DIRECT_PARENT:
            color = self.COLOR_DIRECT_PARENT
            width = self.LINE_WIDTH_DIRECT_PARENT
        elif self.line_type == self.TYPE_SIBLING:
            color = self.COLOR_SIBLING
            width = self.LINE_WIDTH_SIBLING
        else:
            color = self.COLOR_PARENT
            width = self.LINE_WIDTH_PARENT

        pen: QPen = QPen(color, width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.setPen(pen)

    def _apply_hover_pen(self) -> None:
        """Set the hover highlight pen."""
        pen: QPen = QPen(self.COLOR_HOVER, self.LINE_WIDTH_HOVER)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.setPen(pen)

    # ------------------------------------------------------------------
    # Path Construction
    # ------------------------------------------------------------------

    def update_path(self) -> None:
        """Rebuild the path based on current endpoint positions."""
        if self.start_item is None or self.end_item is None:
            self.setPath(QPainterPath())
            return

        start_pos: QPointF = self._get_anchor_point(self.start_item, is_start=True)
        end_pos: QPointF = self._get_anchor_point(self.end_item, is_start=False)

        path: QPainterPath = QPainterPath()

        if self.line_type == self.TYPE_MARRIAGE:
            path = self._build_horizontal_path(start_pos, end_pos)
        elif self.line_type in (self.TYPE_PARENT_CHILD, self.TYPE_DIRECT_PARENT):
            path = self._build_elbow_path(start_pos, end_pos)
        elif self.line_type == self.TYPE_SIBLING:
            path = self._build_horizontal_path(start_pos, end_pos)
        else:
            path.moveTo(start_pos)
            path.lineTo(end_pos)

        self.setPath(path)

    def _build_horizontal_path(self, start: QPointF, end: QPointF) -> QPainterPath:
        """Build a straight horizontal line between two points."""
        path: QPainterPath = QPainterPath()
        path.moveTo(start)
        path.lineTo(end)
        return path

    def _build_elbow_path(self, start: QPointF, end: QPointF) -> QPainterPath:
        """Build an elbow (right-angle) path from parent down to child."""
        path: QPainterPath = QPainterPath()
        path.moveTo(start)

        mid_y: float = start.y() + self.ELBOW_DROP

        if abs(start.x() - end.x()) < 1.0:
            path.lineTo(end)
        else:
            path.lineTo(QPointF(start.x(), mid_y))
            path.lineTo(QPointF(end.x(), mid_y))
            path.lineTo(end)

        return path

    # ------------------------------------------------------------------
    # Anchor Points
    # ------------------------------------------------------------------

    def _get_anchor_point(self, item: QGraphicsItem, is_start: bool) -> QPointF:
        """Get the connection point on an item."""
        rect: QRectF = item.boundingRect()
        scene_pos: QPointF = item.scenePos()

        center_x: float = scene_pos.x() + rect.width() / 2

        if self.line_type == self.TYPE_MARRIAGE:
            center_y: float = scene_pos.y() + rect.height() / 2
            if is_start:
                return QPointF(scene_pos.x() + rect.width(), center_y)
            return QPointF(scene_pos.x(), center_y)

        if is_start:
            return QPointF(center_x, scene_pos.y() + rect.height())

        return QPointF(center_x, scene_pos.y())

    # ------------------------------------------------------------------
    # Update from endpoint movement
    # ------------------------------------------------------------------

    def update_endpoints(self) -> None:
        """Recalculate line position based on connected items."""
        self.update_path()

    def set_start_item(self, item: QGraphicsItem) -> None:
        """Set or replace the start item."""
        self.start_item = item
        self.update_path()

    def set_end_item(self, item: QGraphicsItem) -> None:
        """Set or replace the end item."""
        self.end_item = item
        self.update_path()

    # ------------------------------------------------------------------
    # Hover Events
    # ------------------------------------------------------------------

    def hoverEnterEvent(self, event) -> None:
        """Highlight line on hover."""
        self._is_hovered = True
        self._apply_hover_pen()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        """Remove highlight on hover exit."""
        self._is_hovered = False
        self._apply_default_pen()
        super().hoverLeaveEvent(event)

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------

    def paint(self, painter: QPainter, option, widget=None) -> None:
        """Draw the relationship line with antialiasing."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        super().paint(painter, option, widget)
