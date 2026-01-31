"""Visual representation of a marriage in the tree view."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QGraphicsWidget, QGraphicsSceneHoverEvent, QMenu
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics

if TYPE_CHECKING:
    from database.db_manager import DatabaseManager
    from models.marriage import Marriage


class MarriageNode(QGraphicsWidget):
    """Circular node connecting spouses in the family tree."""

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    marriage_clicked: Signal = Signal(int)
    marriage_double_clicked: Signal = Signal(int)
    end_marriage_requested: Signal = Signal(int)
    delete_marriage_requested: Signal = Signal(int)
    add_child_requested: Signal = Signal(int)

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    NODE_SIZE: float = 24.0
    BORDER_WIDTH: float = 2.0

    COLOR_FILL_ACTIVE: QColor = QColor(220, 80, 80)
    COLOR_FILL_DISSOLVED: QColor = QColor(160, 160, 160)
    COLOR_FILL_HOVER: QColor = QColor(255, 120, 80)
    COLOR_BORDER: QColor = QColor(140, 50, 50)
    COLOR_BORDER_DISSOLVED: QColor = QColor(120, 120, 120)

    COLOR_LABEL_TEXT: QColor = QColor(80, 80, 80)
    COLOR_LABEL_DATE: QColor = QColor(110, 110, 110)
    LABEL_FONT_FAMILY: str = "Segoe UI"
    LABEL_TYPE_FONT_SIZE: int = 8
    LABEL_DATE_FONT_SIZE: int = 8
    LABEL_GAP: float = 4.0

    Z_VALUE: float = 5.0
    GRID_CELL: float = 20.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(
        self,
        marriage_id: int,
        db_manager: DatabaseManager,
        marriage: Marriage | None = None,
    ) -> None:
        super().__init__()
        self.marriage_id: int = marriage_id
        self.db_manager: DatabaseManager = db_manager
        self.marriage: Marriage | None = marriage
        self._is_hovered: bool = False

        self.setZValue(self.Z_VALUE)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable, False)
        # Draggable + snap-on-release.
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        if self.marriage is None:
            self._load_marriage()

    # ------------------------------------------------------------------
    # Data Loading
    # ------------------------------------------------------------------

    def _load_marriage(self) -> None:
        from database.marriage_repository import MarriageRepository
        repo = MarriageRepository(self.db_manager)
        self.marriage = repo.get_by_id(self.marriage_id)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_dissolved(self) -> bool:
        if self.marriage is None:
            return False
        return self.marriage.dissolution_year is not None

    @property
    def _fill_color(self) -> QColor:
        if self._is_hovered:
            return self.COLOR_FILL_HOVER
        if self.is_dissolved:
            return self.COLOR_FILL_DISSOLVED
        return self.COLOR_FILL_ACTIVE

    @property
    def _border_color(self) -> QColor:
        if self.is_dissolved:
            return self.COLOR_BORDER_DISSOLVED
        return self.COLOR_BORDER

    # ------------------------------------------------------------------
    # Label text helpers (uses DateFormatter)
    # ------------------------------------------------------------------

    def _get_type_label(self) -> str:
        if self.marriage is None:
            return "Marriage"
        return self.marriage.marriage_type or "Marriage"

    def _get_date_label(self) -> str:
        """Format marriage date range using DateFormatter."""
        if self.marriage is None:
            return ""

        from utils.date_formatter import DateFormatter, DateParts, MonthStyle

        parts: list[str] = []

        if self.marriage.marriage_year is not None:
            dp = DateParts(
                year=self.marriage.marriage_year,
                month=self.marriage.marriage_month,
            )
            parts.append(
                DateFormatter.format_display(dp, separator=" ", month_style=MonthStyle.ABBREVIATED)
            )

        if self.is_dissolved and self.marriage.dissolution_year is not None:
            dp = DateParts(
                year=self.marriage.dissolution_year,
                month=self.marriage.dissolution_month,
            )
            parts.append(
                DateFormatter.format_display(dp, separator=" ", month_style=MonthStyle.ABBREVIATED)
            )
        else:
            parts.append("-")

        return " - ".join(parts) if len(parts) == 2 else (parts[0] if parts else "")

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def boundingRect(self) -> QRectF:
        # Extra space above for the label text.
        label_height = self._label_height()
        return QRectF(
            -self.NODE_SIZE,
            -(label_height + self.LABEL_GAP),
            self.NODE_SIZE * 3,
            self.NODE_SIZE + label_height + self.LABEL_GAP,
        )

    def _label_height(self) -> float:
        """Height consumed by the two label lines above the node."""
        font_type = QFont(self.LABEL_FONT_FAMILY, self.LABEL_TYPE_FONT_SIZE)
        font_date = QFont(self.LABEL_FONT_FAMILY, self.LABEL_DATE_FONT_SIZE)
        return float(QFontMetrics(font_type).height() + QFontMetrics(font_date).height() + 2)

    # ------------------------------------------------------------------
    # Anchor Points
    # ------------------------------------------------------------------

    def anchor_left(self) -> QPointF:
        return QPointF(self.scenePos().x(), self.scenePos().y() + self.NODE_SIZE / 2)

    def anchor_right(self) -> QPointF:
        return QPointF(self.scenePos().x() + self.NODE_SIZE, self.scenePos().y() + self.NODE_SIZE / 2)

    def anchor_bottom(self) -> QPointF:
        return QPointF(self.scenePos().x() + self.NODE_SIZE / 2, self.scenePos().y() + self.NODE_SIZE)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self._draw_label(painter)
        self._draw_circle(painter)

    def _draw_circle(self, painter: QPainter) -> None:
        pen = QPen(self._border_color, self.BORDER_WIDTH)
        painter.setPen(pen)
        painter.setBrush(QBrush(self._fill_color))
        painter.drawEllipse(QRectF(0, 0, self.NODE_SIZE, self.NODE_SIZE))

    def _draw_label(self, painter: QPainter) -> None:
        """Draw type and date labels centered above the circle."""
        type_text = self._get_type_label()
        date_text = self._get_date_label()

        font_type = QFont(self.LABEL_FONT_FAMILY, self.LABEL_TYPE_FONT_SIZE, QFont.Weight.Bold)
        font_date = QFont(self.LABEL_FONT_FAMILY, self.LABEL_DATE_FONT_SIZE)
        fm_type = QFontMetrics(font_type)
        fm_date = QFontMetrics(font_date)

        center_x = self.NODE_SIZE / 2

        # Type line
        painter.setFont(font_type)
        painter.setPen(QPen(self.COLOR_LABEL_TEXT))
        type_y = -(fm_date.height() + self.LABEL_GAP)
        painter.drawText(
            int(center_x - fm_type.horizontalAdvance(type_text) / 2),
            int(type_y),
            type_text,
        )

        # Date line
        painter.setFont(font_date)
        painter.setPen(QPen(self.COLOR_LABEL_DATE))
        date_y = -self.LABEL_GAP + fm_date.ascent()
        painter.drawText(
            int(center_x - fm_date.horizontalAdvance(date_text) / 2),
            int(date_y),
            date_text,
        )

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self._is_hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self._is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.marriage_clicked.emit(self.marriage_id)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.marriage_double_clicked.emit(self.marriage_id)
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Snap to grid on release."""
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.pos()
            snapped_x = round(pos.x() / self.GRID_CELL) * self.GRID_CELL
            snapped_y = round(pos.y() / self.GRID_CELL) * self.GRID_CELL
            self.setPos(snapped_x, snapped_y)

    def contextMenuEvent(self, event) -> None:
        """Right-click context menu."""
        menu = QMenu()
        end_action = menu.addAction("End Marriage")
        delete_action = menu.addAction("Delete Marriage")
        menu.addSeparator()
        add_child_action = menu.addAction("Add Child")

        chosen = menu.exec(event.screenPos())
        if chosen == end_action:
            self.end_marriage_requested.emit(self.marriage_id)
        elif chosen == delete_action:
            self.delete_marriage_requested.emit(self.marriage_id)
        elif chosen == add_child_action:
            self.add_child_requested.emit(self.marriage_id)
