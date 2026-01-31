"""Fixed time scale overlay for the tree canvas.

Pinned to the left edge of the viewport.  Shows a vertical year scale
that stays visible regardless of horizontal panning.  The year currently
being viewed is displayed centred on the scale and rolls like an
odometer as the user scrolls.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QFontMetrics, QPaintEvent

if TYPE_CHECKING:
    from PySide6.QtWidgets import QGraphicsView


class TimeScale(QWidget):
    """Fixed year-scale overlay on the left edge of the tree canvas viewport."""

    # Dimensions -------------------------------------------------------
    SCALE_WIDTH: int = 60
    TICK_LENGTH: int = 8
    MINOR_TICK_LENGTH: int = 4

    # Colors -----------------------------------------------------------
    COLOR_BG: QColor = QColor(40, 44, 52, 200)
    COLOR_BORDER: QColor = QColor(70, 75, 85)
    COLOR_TEXT: QColor = QColor(200, 210, 220)
    COLOR_TICK: QColor = QColor(140, 150, 165)
    COLOR_MINOR_TICK: QColor = QColor(90, 95, 105)
    COLOR_CENTER_LINE: QColor = QColor(255, 200, 60, 120)
    COLOR_CENTER_TEXT: QColor = QColor(255, 255, 255)

    # Fonts ------------------------------------------------------------
    FONT_FAMILY: str = "Segoe UI"
    FONT_SIZE: int = 9
    FONT_SIZE_CENTER: int = 11
    FONT_SIZE_HEADER: int = 7

    # Layout -----------------------------------------------------------
    TEXT_MARGIN_RIGHT: int = 4
    HEADER_HEIGHT: int = 20
    PADDING_TOP: int = 4

    # Tick intervals ---------------------------------------------------
    MAJOR_TICK_INTERVAL: int = 50
    MINOR_TICK_INTERVAL: int = 10

    # Month display zoom threshold (pixels-per-year at which months appear)
    MONTH_ZOOM_THRESHOLD: float = 80.0

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def __init__(self, parent_view: QGraphicsView) -> None:
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
        self._earliest_year = earliest
        self._latest_year = latest
        self.update()

    def set_scene_y_range(self, top_y: float, bottom_y: float) -> None:
        self._scene_top_y = top_y
        self._scene_bottom_y = bottom_y
        self.update()

    # ------------------------------------------------------------------
    # Coordinate Mapping
    # ------------------------------------------------------------------

    def _scene_y_to_year(self, scene_y: float) -> float:
        """Convert a scene-Y to a fractional year."""
        span_y = self._scene_bottom_y - self._scene_top_y
        if span_y == 0:
            return float(self._earliest_year)
        frac = (scene_y - self._scene_top_y) / span_y
        return self._earliest_year + frac * (self._latest_year - self._earliest_year)

    def _year_to_widget_y(self, year: float) -> float:
        """Convert a fractional year to a widget pixel Y."""
        scene_y = self._year_to_scene_y(year)
        return self._scene_y_to_widget_y(scene_y)

    def _year_to_scene_y(self, year: float) -> float:
        span = self._latest_year - self._earliest_year
        if span == 0:
            return self._scene_top_y
        frac = (year - self._earliest_year) / span
        return self._scene_top_y + frac * (self._scene_bottom_y - self._scene_top_y)

    def _scene_y_to_widget_y(self, scene_y: float) -> float:
        vp = self._view.mapFromScene(0, scene_y)
        return float(vp.y())

    def _pixels_per_year(self) -> float:
        """Current vertical pixels per calendar year in viewport space."""
        y1 = self._scene_y_to_widget_y(self._scene_top_y)
        y2 = self._scene_y_to_widget_y(self._scene_bottom_y)
        span = self._latest_year - self._earliest_year
        if span == 0:
            return 0.0
        return abs(y2 - y1) / span

    # ------------------------------------------------------------------
    # Centered-year helpers
    # ------------------------------------------------------------------

    def _center_scene_y(self) -> float:
        """Scene-Y coordinate of the viewport centre."""
        center_vp = self._view.viewport().rect().center()
        scene_pt = self._view.mapToScene(center_vp)
        return scene_pt.y()

    def _center_year(self) -> float:
        """Fractional year currently at the viewport centre."""
        return self._scene_y_to_year(self._center_scene_y())

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def paintEvent(self, event: QPaintEvent) -> None:
        if self._latest_year <= self._earliest_year:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self._draw_background(painter)
        self._draw_year_ticks(painter)
        self._draw_center_year(painter)
        self._draw_range_header(painter)

        painter.end()

    def _draw_background(self, painter: QPainter) -> None:
        painter.setPen(QPen(self.COLOR_BORDER, 1))
        painter.setBrush(QBrush(self.COLOR_BG))
        painter.drawRect(self.rect())

    def _draw_range_header(self, painter: QPainter) -> None:
        font = QFont(self.FONT_FAMILY, self.FONT_SIZE_HEADER)
        painter.setFont(font)
        painter.setPen(QPen(self.COLOR_TEXT))
        text = f"{self._earliest_year}\u2013{self._latest_year}"
        painter.drawText(QRect(0, self.PADDING_TOP, self.SCALE_WIDTH, self.HEADER_HEIGHT), Qt.AlignmentFlag.AlignCenter, text)

    def _draw_year_ticks(self, painter: QPainter) -> None:
        font = QFont(self.FONT_FAMILY, self.FONT_SIZE)
        painter.setFont(font)
        metrics = QFontMetrics(font)

        first_major = (self._earliest_year // self.MAJOR_TICK_INTERVAL) * self.MAJOR_TICK_INTERVAL
        if first_major < self._earliest_year:
            first_major += self.MAJOR_TICK_INTERVAL

        first_minor = (self._earliest_year // self.MINOR_TICK_INTERVAL) * self.MINOR_TICK_INTERVAL
        if first_minor < self._earliest_year:
            first_minor += self.MINOR_TICK_INTERVAL

        # Minor ticks
        painter.setPen(QPen(self.COLOR_MINOR_TICK, 1))
        year = first_minor
        while year <= self._latest_year:
            if year % self.MAJOR_TICK_INTERVAL != 0:
                wy = self._year_to_widget_y(float(year))
                x0 = self.SCALE_WIDTH - self.MINOR_TICK_LENGTH
                painter.drawLine(x0, int(wy), self.SCALE_WIDTH, int(wy))
            year += self.MINOR_TICK_INTERVAL

        # Major ticks
        year = first_major
        while year <= self._latest_year:
            wy = self._year_to_widget_y(float(year))
            painter.setPen(QPen(self.COLOR_TICK, 1))
            x0 = self.SCALE_WIDTH - self.TICK_LENGTH
            painter.drawLine(x0, int(wy), self.SCALE_WIDTH, int(wy))

            painter.setPen(QPen(self.COLOR_TEXT))
            label = str(year)
            tw = metrics.horizontalAdvance(label)
            tx = self.SCALE_WIDTH - self.TICK_LENGTH - tw - self.TEXT_MARGIN_RIGHT
            ty = int(wy) + metrics.ascent() // 2
            painter.drawText(tx, ty, label)
            year += self.MAJOR_TICK_INTERVAL

    # ------------------------------------------------------------------
    # Center-year indicator with odometer effect
    # ------------------------------------------------------------------

    def _draw_center_year(self, painter: QPainter) -> None:
        """Draw the centred year indicator with per-digit odometer roll."""
        center_y_px = self.height() / 2
        frac_year = self._center_year()

        # Clamp to range so we don't show impossible years.
        frac_year = max(float(self._earliest_year), min(float(self._latest_year), frac_year))

        whole_year = int(frac_year)
        fraction = frac_year - whole_year

        # Edge nudge: move the indicator toward top/bottom when close to range extremes.
        total_span = self._latest_year - self._earliest_year
        if total_span > 0:
            normalized = (frac_year - self._earliest_year) / total_span
            edge_zone = 0.08
            if normalized < edge_zone:
                center_y_px = self.height() * (0.5 - (edge_zone - normalized) / edge_zone * 0.35)
            elif normalized > 1.0 - edge_zone:
                center_y_px = self.height() * (0.5 + (normalized - (1.0 - edge_zone)) / edge_zone * 0.35)

        font = QFont(self.FONT_FAMILY, self.FONT_SIZE_CENTER, QFont.Weight.Bold)
        painter.setFont(font)
        fm = QFontMetrics(font)
        digit_h = fm.height()

        # Draw a subtle background box for the indicator.
        box_w = self.SCALE_WIDTH - 4
        box_h = digit_h + 8
        box_rect = QRectF(2, center_y_px - box_h / 2, box_w, box_h)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 200, 60, 40)))
        painter.drawRoundedRect(box_rect, 3, 3)

        # Horizontal line across full width.
        painter.setPen(QPen(self.COLOR_CENTER_LINE, 1))
        painter.drawLine(0, int(center_y_px), self.SCALE_WIDTH, int(center_y_px))

        painter.setPen(QPen(self.COLOR_CENTER_TEXT))

        ppy = self._pixels_per_year()
        show_months = ppy >= self.MONTH_ZOOM_THRESHOLD

        if show_months:
            month_index = int(fraction * 12)
            month_frac = (fraction * 12) - month_index
            month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month_str = month_names[min(month_index, 11)]
            next_month_idx = month_index + 1
            if next_month_idx >= 12:
                next_month_str = "Jan"
                next_year_str = str(whole_year + 1)
            else:
                next_month_str = month_names[next_month_idx]
                next_year_str = str(whole_year)
            # Draw year static, roll month only.
            year_str = str(whole_year)
            year_w = fm.horizontalAdvance(year_str)
            month_w = max(fm.horizontalAdvance(month_str), fm.horizontalAdvance(next_month_str))
            total_w = month_w + fm.horizontalAdvance(" ") + year_w
            tx = (self.SCALE_WIDTH - total_w) / 2
            base_y = center_y_px + fm.ascent() / 2
            roll_offset = month_frac * digit_h

            painter.save()
            painter.setClipRect(box_rect)
            # Static year part.
            painter.drawText(int(tx + month_w + fm.horizontalAdvance(" ")), int(base_y), next_year_str if next_month_idx >= 12 and month_frac > 0.5 else year_str)
            # Rolling month.
            month_clip = QRectF(tx, box_rect.top(), month_w + 2, box_rect.height())
            painter.setClipRect(month_clip)
            painter.drawText(int(tx), int(base_y - roll_offset), month_str)
            painter.drawText(int(tx), int(base_y - roll_offset + digit_h), next_month_str)
            painter.restore()
        else:
            # Per-digit odometer: only roll digits that are changing.
            current_str = str(whole_year)
            next_str = str(whole_year + 1)

            # Pad to same length.
            max_len = max(len(current_str), len(next_str))
            current_str = current_str.zfill(max_len)
            next_str = next_str.zfill(max_len)

            # Calculate total width for centering.
            total_w = sum(fm.horizontalAdvance(c) for c in current_str)
            tx = (self.SCALE_WIDTH - total_w) / 2
            base_y = center_y_px + fm.ascent() / 2

            painter.save()
            painter.setClipRect(box_rect)

            x = tx
            for i in range(max_len):
                cur_d = current_str[i]
                nxt_d = next_str[i]
                dw = fm.horizontalAdvance(cur_d)

                if cur_d == nxt_d:
                    # Static digit - no roll.
                    painter.drawText(int(x), int(base_y), cur_d)
                else:
                    # Roll this digit.
                    digit_clip = QRectF(x - 1, box_rect.top(), dw + 2, box_rect.height())
                    painter.save()
                    painter.setClipRect(digit_clip)
                    roll_offset = fraction * digit_h
                    painter.drawText(int(x), int(base_y - roll_offset), cur_d)
                    painter.drawText(int(x), int(base_y - roll_offset + digit_h), nxt_d)
                    painter.restore()
                x += dw

            painter.restore()

    # ------------------------------------------------------------------
    # Geometry Updates
    # ------------------------------------------------------------------

    def update_geometry(self) -> None:
        viewport = self._view.viewport()
        self.setGeometry(0, 0, self.SCALE_WIDTH, viewport.height())
        self.update()
