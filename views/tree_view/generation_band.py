"""Horizontal band showing a generation level in the tree."""

from __future__ import annotations

from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont


class GenerationBand(QGraphicsWidget):
    """Background band for highlighting a generation level."""

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    # Band colors (alternating)
    COLOR_EVEN: QColor = QColor(245, 248, 255, 40)
    COLOR_ODD: QColor = QColor(235, 240, 250, 40)
    COLOR_BORDER: QColor = QColor(200, 210, 230, 60)

    # Label styling
    COLOR_LABEL: QColor = QColor(140, 150, 170)
    FONT_FAMILY: str = "Segoe UI"
    FONT_SIZE: int = 11
    FONT_WEIGHT: int = 500
    LABEL_MARGIN_LEFT: float = 12.0
    LABEL_MARGIN_TOP: float = 8.0

    # Label text
    LABEL_FORMAT: str = "Gen {gen}"

    # Border
    BORDER_LINE_WIDTH: float = 0.5

    # Z-ordering (behind everything else)
    Z_VALUE: float = -100.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(
        self,
        generation: int,
        y_position: float,
        band_height: float,
        band_width: float = 10000.0
    ) -> None:
        """Initialize the generation band."""
        super().__init__()
        self.generation: int = generation
        self.band_y: float = y_position
        self.band_height: float = band_height
        self.band_width: float = band_width

        self.setPos(-self.band_width / 2, self.band_y)
        self.setZValue(self.Z_VALUE)

        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsWidget.GraphicsItemFlag.ItemIsMovable, False)
        self.setAcceptHoverEvents(False)

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle of the band."""
        return QRectF(0, 0, self.band_width, self.band_height)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def paint(self, painter: QPainter, option, widget=None) -> None:
        """Draw the generation band."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        rect: QRectF = self.boundingRect()

        self._draw_background(painter, rect)
        self._draw_top_border(painter, rect)
        self._draw_label(painter)

    def _draw_background(self, painter: QPainter, rect: QRectF) -> None:
        """Fill the band with alternating color."""
        fill_color: QColor = self.COLOR_EVEN if self.generation % 2 == 0 else self.COLOR_ODD
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(fill_color))
        painter.drawRect(rect)

    def _draw_top_border(self, painter: QPainter, rect: QRectF) -> None:
        """Draw a subtle line at the top of the band."""
        pen: QPen = QPen(self.COLOR_BORDER, self.BORDER_LINE_WIDTH)
        painter.setPen(pen)
        painter.drawLine(rect.topLeft(), rect.topRight())

    def _draw_label(self, painter: QPainter) -> None:
        """Draw the generation label in the top-left corner."""
        font: QFont = QFont(self.FONT_FAMILY, self.FONT_SIZE, self.FONT_WEIGHT)
        painter.setFont(font)
        painter.setPen(QPen(self.COLOR_LABEL))

        label_text: str = self.LABEL_FORMAT.format(gen=self.generation)
        painter.drawText(
            int(self.LABEL_MARGIN_LEFT),
            int(self.LABEL_MARGIN_TOP + self.FONT_SIZE),
            label_text
        )

    # ------------------------------------------------------------------
    # Position Updates
    # ------------------------------------------------------------------

    def update_position(self, new_y: float, new_height: float) -> None:
        """Adjust band position and height."""
        self.band_y = new_y
        self.band_height = new_height
        self.setPos(-self.band_width / 2, self.band_y)
        self.prepareGeometryChange()
        self.update()

    def update_width(self, new_width: float) -> None:
        """Adjust band width to match scene content."""
        self.band_width = new_width
        self.setPos(-self.band_width / 2, self.band_y)
        self.prepareGeometryChange()
        self.update()
