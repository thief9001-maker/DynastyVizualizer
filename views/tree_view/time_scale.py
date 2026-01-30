"""Fixed time scale overlay for the tree canvas."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics, QPaintEvent

if TYPE_CHECKING:
    from PySide6.QtWidgets import QGraphicsView


class TimeScale(QWidget):
    """Fixed year-scale overlay pinned to the left side of the tree canvas.

    Shows a vertical bar mapping scene Y-coordinates to calendar years.
    Stays fixed in place while the user pans and zooms the main canvas.
    When fully zoomed out, displays the complete dynasty timespan from
    earliest recorded year (top) to latest recorded year (bottom).
    """

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    # Dimensions
    SCALE_WIDTH: int = 50
    TICK_LENGTH: int = 8
    MINOR_TICK_LENGTH: int = 4

    # Colors
    COLOR_BG: QColor = QColor(40, 44, 52, 200)
    COLOR_BORDER: QColor = QColor(70, 75, 85)
    COLOR_TEXT: QColor = QColor(200, 210, 220)
    COLOR_TICK: QColor = QColor(140, 150, 165)
    COLOR_MINOR_TICK: QColor = QColor(90, 95, 105)
    COLOR_CURRENT_LINE: QColor = QColor(255, 200, 60, 120)

    # Font
    FONT_FAMILY: str = "Segoe UI"
    FONT_SIZE: int = 9
    FONT_SIZE_HEADER: int = 7

    # Layout
    TEXT_MARGIN_LEFT: int = 6
    TEXT_MARGIN_RIGHT: int = 4
    HEADER_HEIGHT: int = 20
    FOOTER_HEIGHT: int = 20
    PADDING_TOP: int = 4
    PADDING_BOTTOM: int = 4

    # Tick intervals
    MAJOR_TICK_INTERVAL: int = 50
    MINOR_TICK_INTERVAL: int = 10

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self, parent_view: QGraphicsView) -> None:
        """Initialize the time scale overlay."""
        super().__init__(parent_view.viewport())
        self._view: QGraphicsView = parent_view
        self._earliest_year: int = 0
        self._latest_year: int = 0
        self._scene_top_y: float = 0.0
        self._scene_bottom_y: float = 1000.0

        self.setFixedWidth(self.SCALE_WIDTH)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.raise_()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def set_year_range(self, earliest: int, latest: int) -> None:
        """Set the year range for the scale."""
        self._earliest_year = earliest
        self._latest_year = latest
        self.update()

    def set_scene_y_range(self, top_y: float, bottom_y: float) -> None:
        """Set the scene Y-coordinate range that maps to the year range."""
        self._scene_top_y = top_y
        self._scene_bottom_y = bottom_y
        self.update()

    # ------------------------------------------------------------------
    # Coordinate Mapping
    # ------------------------------------------------------------------

    def _year_to_widget_y(self, year: int) -> float:
        """Convert a calendar year to a widget Y pixel position."""
        if self._latest_year <= self._earliest_year:
            return self.HEADER_HEIGHT

        scene_y: float = self._year_to_scene_y(year)
        return self._scene_y_to_widget_y(scene_y)

    def _year_to_scene_y(self, year: int) -> float:
        """Convert a calendar year to a scene Y coordinate."""
        if self._latest_year <= self._earliest_year:
            return self._scene_top_y

        year_fraction: float = (year - self._earliest_year) / (self._latest_year - self._earliest_year)
        return self._scene_top_y + year_fraction * (self._scene_bottom_y - self._scene_top_y)

    def _scene_y_to_widget_y(self, scene_y: float) -> float:
        """Convert a scene Y coordinate to a widget pixel position."""
        viewport_point = self._view.mapFromScene(0, scene_y)
        return float(viewport_point.y())

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def paintEvent(self, event: QPaintEvent) -> None:
        """Draw the time scale overlay."""
        if self._latest_year <= self._earliest_year:
            return

        painter: QPainter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self._draw_background(painter)
        self._draw_year_ticks(painter)
        self._draw_range_header(painter)

        painter.end()

    def _draw_background(self, painter: QPainter) -> None:
        """Draw the semi-transparent background panel."""
        rect: QRect = self.rect()

        painter.setPen(QPen(self.COLOR_BORDER, 1))
        painter.setBrush(QBrush(self.COLOR_BG))
        painter.drawRect(rect)

    def _draw_range_header(self, painter: QPainter) -> None:
        """Draw the year range summary at top."""
        font: QFont = QFont(self.FONT_FAMILY, self.FONT_SIZE_HEADER)
        painter.setFont(font)
        painter.setPen(QPen(self.COLOR_TEXT))

        header_text: str = f"{self._earliest_year}-{self._latest_year}"
        header_rect: QRect = QRect(0, self.PADDING_TOP, self.SCALE_WIDTH, self.HEADER_HEIGHT)
        painter.drawText(header_rect, Qt.AlignmentFlag.AlignCenter, header_text)

    def _draw_year_ticks(self, painter: QPainter) -> None:
        """Draw year markers along the scale."""
        font: QFont = QFont(self.FONT_FAMILY, self.FONT_SIZE)
        painter.setFont(font)
        metrics: QFontMetrics = QFontMetrics(font)

        first_major: int = (self._earliest_year // self.MAJOR_TICK_INTERVAL) * self.MAJOR_TICK_INTERVAL
        if first_major < self._earliest_year:
            first_major += self.MAJOR_TICK_INTERVAL

        first_minor: int = (self._earliest_year // self.MINOR_TICK_INTERVAL) * self.MINOR_TICK_INTERVAL
        if first_minor < self._earliest_year:
            first_minor += self.MINOR_TICK_INTERVAL

        self._draw_minor_ticks(painter, first_minor)
        self._draw_major_ticks(painter, first_major, metrics)

    def _draw_minor_ticks(self, painter: QPainter, first_minor: int) -> None:
        """Draw minor tick marks."""
        painter.setPen(QPen(self.COLOR_MINOR_TICK, 1))

        year: int = first_minor
        while year <= self._latest_year:
            if year % self.MAJOR_TICK_INTERVAL != 0:
                widget_y: float = self._year_to_widget_y(year)
                x_start: int = self.SCALE_WIDTH - self.MINOR_TICK_LENGTH
                painter.drawLine(x_start, int(widget_y), self.SCALE_WIDTH, int(widget_y))
            year += self.MINOR_TICK_INTERVAL

    def _draw_major_ticks(self, painter: QPainter, first_major: int, metrics: QFontMetrics) -> None:
        """Draw major tick marks with year labels."""
        year: int = first_major
        while year <= self._latest_year:
            widget_y: float = self._year_to_widget_y(year)

            painter.setPen(QPen(self.COLOR_TICK, 1))
            x_start: int = self.SCALE_WIDTH - self.TICK_LENGTH
            painter.drawLine(x_start, int(widget_y), self.SCALE_WIDTH, int(widget_y))

            painter.setPen(QPen(self.COLOR_TEXT))
            label: str = str(year)
            text_width: int = metrics.horizontalAdvance(label)
            text_x: int = self.SCALE_WIDTH - self.TICK_LENGTH - text_width - self.TEXT_MARGIN_RIGHT
            text_y: int = int(widget_y) + metrics.ascent() // 2
            painter.drawText(text_x, text_y, label)

            year += self.MAJOR_TICK_INTERVAL

    # ------------------------------------------------------------------
    # Geometry Updates
    # ------------------------------------------------------------------

    def update_geometry(self) -> None:
        """Resize and reposition to match the parent viewport."""
        viewport = self._view.viewport()
        self.setGeometry(0, 0, self.SCALE_WIDTH, viewport.height())
        self.update()
