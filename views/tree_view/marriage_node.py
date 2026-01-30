"""Visual representation of a marriage in the tree view."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsWidget, QGraphicsSceneHoverEvent
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath, QFontMetrics

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.marriage import Marriage


class MarriageNode(QGraphicsWidget):
    """Node connecting spouses in the family tree."""

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    marriage_clicked: Signal = Signal(int)
    marriage_double_clicked: Signal = Signal(int)

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    # Dimensions
    NODE_SIZE: float = 18.0
    BORDER_WIDTH: float = 2.0

    # Colors
    COLOR_FILL_ACTIVE: QColor = QColor(220, 80, 80)
    COLOR_FILL_DISSOLVED: QColor = QColor(160, 160, 160)
    COLOR_FILL_HOVER: QColor = QColor(255, 120, 80)
    COLOR_BORDER: QColor = QColor(140, 50, 50)
    COLOR_BORDER_DISSOLVED: QColor = QColor(120, 120, 120)

    # Tooltip
    COLOR_TOOLTIP_BG: QColor = QColor(50, 50, 50, 230)
    COLOR_TOOLTIP_TEXT: QColor = QColor(255, 255, 255)
    TOOLTIP_FONT_FAMILY: str = "Segoe UI"
    TOOLTIP_FONT_SIZE: int = 9
    TOOLTIP_PADDING: int = 6
    TOOLTIP_OFFSET_Y: float = -30.0

    # Z-ordering (above lines, below person boxes)
    Z_VALUE: float = 5.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(
        self,
        marriage_id: int,
        db_manager: DatabaseManager,
        marriage: Marriage | None = None
    ) -> None:
        """Initialize the marriage node."""
        super().__init__()
        self.marriage_id: int = marriage_id
        self.db_manager: DatabaseManager = db_manager
        self.marriage: Marriage | None = marriage
        self._is_hovered: bool = False

        self.setZValue(self.Z_VALUE)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsMovable, False)

        if self.marriage is None:
            self._load_marriage()

    # ------------------------------------------------------------------
    # Data Loading
    # ------------------------------------------------------------------

    def _load_marriage(self) -> None:
        """Load marriage data from database."""
        from database.marriage_repository import MarriageRepository

        repo: MarriageRepository = MarriageRepository(self.db_manager)
        self.marriage = repo.get_by_id(self.marriage_id)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_dissolved(self) -> bool:
        """Check if the marriage has ended."""
        if self.marriage is None:
            return False
        return self.marriage.dissolution_year is not None

    @property
    def _fill_color(self) -> QColor:
        """Get fill color based on state."""
        if self._is_hovered:
            return self.COLOR_FILL_HOVER
        if self.is_dissolved:
            return self.COLOR_FILL_DISSOLVED
        return self.COLOR_FILL_ACTIVE

    @property
    def _border_color(self) -> QColor:
        """Get border color based on state."""
        if self.is_dissolved:
            return self.COLOR_BORDER_DISSOLVED
        return self.COLOR_BORDER

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle of the node."""
        return QRectF(0, 0, self.NODE_SIZE, self.NODE_SIZE)

    # ------------------------------------------------------------------
    # Anchor Points (for RelationshipLine connections)
    # ------------------------------------------------------------------

    def anchor_left(self) -> QPointF:
        """Left anchor for spouse1 connection."""
        return QPointF(self.scenePos().x(), self.scenePos().y() + self.NODE_SIZE / 2)

    def anchor_right(self) -> QPointF:
        """Right anchor for spouse2 connection."""
        return QPointF(
            self.scenePos().x() + self.NODE_SIZE,
            self.scenePos().y() + self.NODE_SIZE / 2
        )

    def anchor_bottom(self) -> QPointF:
        """Bottom anchor for child connections."""
        return QPointF(
            self.scenePos().x() + self.NODE_SIZE / 2,
            self.scenePos().y() + self.NODE_SIZE
        )

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def paint(self, painter: QPainter, option, widget=None) -> None:
        """Draw the marriage node as a diamond shape."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self._draw_diamond(painter)

        if self._is_hovered:
            self._draw_tooltip(painter)

    def _draw_diamond(self, painter: QPainter) -> None:
        """Draw the diamond connector shape."""
        half: float = self.NODE_SIZE / 2
        center: QPointF = QPointF(half, half)

        path: QPainterPath = QPainterPath()
        path.moveTo(center.x(), 0)
        path.lineTo(self.NODE_SIZE, center.y())
        path.lineTo(center.x(), self.NODE_SIZE)
        path.lineTo(0, center.y())
        path.closeSubpath()

        pen: QPen = QPen(self._border_color, self.BORDER_WIDTH)
        painter.setPen(pen)
        painter.setBrush(QBrush(self._fill_color))
        painter.drawPath(path)

    def _draw_tooltip(self, painter: QPainter) -> None:
        """Draw a small tooltip showing marriage date on hover."""
        if self.marriage is None:
            return

        tooltip_text: str = self._get_tooltip_text()
        if not tooltip_text:
            return

        font: QFont = QFont(self.TOOLTIP_FONT_FAMILY, self.TOOLTIP_FONT_SIZE)
        painter.setFont(font)
        metrics: QFontMetrics = QFontMetrics(font)

        text_width: int = metrics.horizontalAdvance(tooltip_text)
        text_height: int = metrics.height()

        bg_width: float = text_width + self.TOOLTIP_PADDING * 2
        bg_height: float = text_height + self.TOOLTIP_PADDING * 2

        bg_x: float = (self.NODE_SIZE - bg_width) / 2
        bg_y: float = self.TOOLTIP_OFFSET_Y

        bg_rect: QRectF = QRectF(bg_x, bg_y, bg_width, bg_height)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.COLOR_TOOLTIP_BG))
        painter.drawRoundedRect(bg_rect, 4, 4)

        painter.setPen(QPen(self.COLOR_TOOLTIP_TEXT))
        painter.drawText(bg_rect, Qt.AlignmentFlag.AlignCenter, tooltip_text)

    def _get_tooltip_text(self) -> str:
        """Build tooltip text from marriage data."""
        if self.marriage is None:
            return ""

        parts: list[str] = []

        if self.marriage.marriage_year is not None:
            parts.append(str(self.marriage.marriage_year))

        if self.is_dissolved and self.marriage.dissolution_year is not None:
            parts.append(f"- {self.marriage.dissolution_year}")
            if self.marriage.dissolution_reason:
                parts.append(f"({self.marriage.dissolution_reason})")

        return " ".join(parts) if parts else "Marriage"

    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Handle hover enter."""
        self._is_hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Handle hover leave."""
        self._is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        """Handle click to emit signal."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.marriage_clicked.emit(self.marriage_id)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        """Handle double-click to emit signal."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.marriage_double_clicked.emit(self.marriage_id)
        super().mouseDoubleClickEvent(event)
