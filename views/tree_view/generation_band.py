"""Horizontal band showing a generation level in the tree."""

from __future__ import annotations

from PySide6.QtWidgets import QGraphicsWidget, QMenu
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics


class GenerationBand(QGraphicsWidget):
    """Background band for highlighting a generation level.

    Generation bands are visual guides.  Their label can be edited and
    their year-span can be redefined by the user.
    """

    # ------------------------------------------------------------------
    # Signals
    # ------------------------------------------------------------------

    label_edit_requested: Signal = Signal(int)  # generation number

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    COLOR_EVEN: QColor = QColor(245, 248, 255, 40)
    COLOR_ODD: QColor = QColor(235, 240, 250, 40)
    COLOR_BORDER: QColor = QColor(200, 210, 230, 60)

    COLOR_LABEL: QColor = QColor(140, 150, 170)
    COLOR_LABEL_BG: QColor = QColor(255, 255, 255, 50)
    COLOR_LABEL_BORDER: QColor = QColor(180, 190, 210, 80)
    FONT_FAMILY: str = "Segoe UI"
    FONT_SIZE: int = 11
    FONT_WEIGHT: int = 500
    LABEL_MARGIN_TOP: float = 8.0
    LABEL_PADDING: float = 6.0

    BORDER_LINE_WIDTH: float = 0.5
    Z_VALUE: float = -100.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(
        self,
        generation: int,
        y_position: float,
        band_height: float,
        band_width: float = 10000.0,
        label_text: str | None = None,
    ) -> None:
        super().__init__()
        self.generation: int = generation
        self.band_y: float = y_position
        self.band_height: float = band_height
        self.band_width: float = band_width
        self.label_text: str = label_text or f"Gen {generation}"
        self._label_x_offset: float = 0.0

        self.setPos(-self.band_width / 2, self.band_y)
        self.setZValue(self.Z_VALUE)

        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsMovable, False)
        self.setAcceptHoverEvents(True)

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def set_label_x_offset(self, scene_x: float) -> None:
        """Set the scene-X position for the label box."""
        self._label_x_offset = scene_x

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.band_width, self.band_height)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        rect = self.boundingRect()
        self._draw_background(painter, rect)
        self._draw_top_border(painter, rect)
        self._draw_label(painter)

    def _draw_background(self, painter: QPainter, rect: QRectF) -> None:
        fill = self.COLOR_EVEN if self.generation % 2 == 0 else self.COLOR_ODD
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(fill))
        painter.drawRect(rect)

    def _draw_top_border(self, painter: QPainter, rect: QRectF) -> None:
        painter.setPen(QPen(self.COLOR_BORDER, self.BORDER_LINE_WIDTH))
        painter.drawLine(rect.topLeft(), rect.topRight())

    def _draw_label(self, painter: QPainter) -> None:
        """Draw the generation label inside a small rounded box."""
        font = QFont(self.FONT_FAMILY, self.FONT_SIZE, self.FONT_WEIGHT)
        painter.setFont(font)
        fm = QFontMetrics(font)

        text_w = fm.horizontalAdvance(self.label_text)
        text_h = fm.height()

        # Convert scene-X to local coords.  The band is placed at
        # x = -band_width/2, so local_x = scene_x - (-band_width/2).
        local_x = self._label_x_offset + self.band_width / 2
        local_y = self.LABEL_MARGIN_TOP

        box_rect = QRectF(
            local_x - self.LABEL_PADDING,
            local_y - self.LABEL_PADDING / 2,
            text_w + self.LABEL_PADDING * 2,
            text_h + self.LABEL_PADDING,
        )

        # Background box.
        painter.setPen(QPen(self.COLOR_LABEL_BORDER, 1))
        painter.setBrush(QBrush(self.COLOR_LABEL_BG))
        painter.drawRoundedRect(box_rect, 4, 4)

        # Text.
        painter.setPen(QPen(self.COLOR_LABEL))
        painter.drawText(int(local_x), int(local_y + fm.ascent()), self.label_text)

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.label_edit_requested.emit(self.generation)
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu()
        rename_action = menu.addAction("Rename Generation")
        redefine_action = menu.addAction("Redefine Year Span")
        chosen = menu.exec(event.screenPos())
        if chosen == rename_action:
            self.label_edit_requested.emit(self.generation)
        elif chosen == redefine_action:
            self.label_edit_requested.emit(self.generation)

    # ------------------------------------------------------------------
    # Position Updates
    # ------------------------------------------------------------------

    def update_position(self, new_y: float, new_height: float) -> None:
        self.band_y = new_y
        self.band_height = new_height
        self.setPos(-self.band_width / 2, self.band_y)
        self.prepareGeometryChange()
        self.update()

    def update_width(self, new_width: float) -> None:
        self.band_width = new_width
        self.setPos(-self.band_width / 2, self.band_y)
        self.prepareGeometryChange()
        self.update()
