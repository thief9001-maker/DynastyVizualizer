"""Person box widget for the tree view."""

from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtCore import Qt, QRectF, QPointF, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPixmap, QPainterPath, QFontMetrics
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.person import Person
    from database.db_manager import DatabaseManager
    from views.tree_view.enhanced_tooltip_panel import EnhancedTooltipPanel


class PersonBox(QGraphicsWidget):
    """Visual representation of a person in the family tree."""
    
    person_double_clicked: Signal = Signal(int)
    person_selected: Signal = Signal(int)
    favorite_toggled: Signal = Signal(int, bool)
    
    BOX_MIN_WIDTH: int = 300
    BOX_MAX_WIDTH: int = 300
    BOX_HEIGHT: int = 130
    PHOTO_SIZE: int = 110
    BORDER_WIDTH: int = 3
    CORNER_RADIUS: int = 8
    TEXT_PADDING: int = 10
    
    TOOLTIP_WIDTH: int = 300
    TOOLTIP_HEIGHT: int = 600
    TOOLTIP_OFFSET_X: int = 10
    TOOLTIP_DELAY: int = 1000
    
    FAVORITE_STAR_SIZE: int = 20
    
    COLOR_LIVING: QColor = QColor(76, 175, 80)
    COLOR_DECEASED: QColor = QColor(158, 158, 158)
    COLOR_BG: QColor = QColor(255, 255, 255)
    COLOR_TEXT: QColor = QColor(33, 33, 33)
    COLOR_TEXT_LIGHT: QColor = QColor(120, 120, 120)
    COLOR_SEPARATOR: QColor = QColor(200, 200, 200)
    COLOR_FAVORITE_STAR: QColor = QColor(255, 215, 0)
    COLOR_FAVORITE_HOVER: QColor = QColor(200, 200, 200)
    
    def __init__(
        self, 
        person_id: int, 
        db_manager: 'DatabaseManager',
        current_year: int | None = None
    ) -> None:
        super().__init__()
        
        self.person_id: int = person_id
        self.db: 'DatabaseManager' = db_manager
        self.current_year: int = current_year if current_year is not None else datetime.now().year
        
        self.person: 'Person | None' = None
        self.portrait_pixmap: QPixmap | None = None
        self.is_favorite: bool = False
        
        self._font_name_bold: QFont = QFont("Segoe UI", 11, QFont.Weight.Bold)
        self._font_normal: QFont = QFont("Segoe UI", 9)
        self._font_icon: QFont = QFont("Segoe UI Emoji", 12)

        self._load_person_data()
        self._load_portrait()
        self._load_favorite_status()
        
        self.box_width: float = self._calculate_box_width()
        _, name_line2 = self._get_display_name_lines()
        self.box_height: float = self.BOX_HEIGHT + (18 if name_line2 else 0)
        
        self.setFlags(
            QGraphicsWidget.GraphicsItemFlag.ItemIsMovable |
            QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setMinimumSize(self.box_width, self.box_height)
        self.setMaximumSize(self.box_width, self.box_height)
        
        self._is_dragging: bool = False
        self._drag_start_pos: QPointF | None = None
        
        self._tooltip_delay_timer: QTimer = QTimer()
        self._tooltip_delay_timer.setSingleShot(True)
        self._tooltip_delay_timer.timeout.connect(self._show_enhanced_tooltip)
        
        self._is_hovered: bool = False
        self._is_name_hovered: bool = False
        self._is_star_hovered: bool = False
        self._tooltip_manually_positioned: bool = False
        self._tooltip_panel: 'EnhancedTooltipPanel | None' = None
    
    def _query_one(self, sql: str, params: tuple = ()) -> dict | None:
        """Execute query and return first row as dict."""
        if not self.db or not self.db.conn:
            return None
        cursor = self.db.conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def _load_person_data(self) -> None:
        """Load person data from database."""
        row: dict | None = self._query_one("SELECT * FROM Person WHERE id = ?", (self.person_id,))
        if not row:
            return
        
        from models.person import Person
        
        self.person = Person(
            id=row.get('id'),
            first_name=row.get('first_name', ''),
            middle_name=row.get('middle_name', ''),
            last_name=row.get('last_name', ''),
            maiden_name=row.get('maiden_name') or '',
            nickname=row.get('nickname', ''),
            gender=row.get('gender', 'Unknown'),
            birth_year=row.get('birth_year'),
            birth_month=row.get('birth_month'),
            birth_day=row.get('birth_day'),
            death_year=row.get('death_year'),
            death_month=row.get('death_month'),
            death_day=row.get('death_day'),
            arrival_year=row.get('arrival_year'),
            arrival_month=row.get('arrival_month'),
            arrival_day=row.get('arrival_day'),
            moved_out_year=row.get('moved_out_year'),
            moved_out_month=row.get('moved_out_month'),
            moved_out_day=row.get('moved_out_day'),
            father_id=row.get('father_id'),
            mother_id=row.get('mother_id'),
            family_id=row.get('family_id'),
            dynasty_id=row.get('dynasty_id', 1),
            is_founder=bool(row.get('is_founder', 0)),
            education=row.get('education', 0),
            notes=row.get('notes', '')
        )
    
    def _load_portrait(self) -> None:
        """Load portrait image from database if exists."""
        row: dict | None = self._query_one(
            "SELECT image_path FROM Portrait WHERE person_id = ? AND is_primary = 1 ORDER BY display_order LIMIT 1",
            (self.person_id,)
        )
        
        if row and row['image_path']:
            pixmap: QPixmap = QPixmap(row['image_path'])
            if not pixmap.isNull():
                self.portrait_pixmap = pixmap.scaled(
                    self.PHOTO_SIZE, 
                    self.PHOTO_SIZE, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
    
    def _load_favorite_status(self) -> None:
        """Load favorite status from database."""
        row: dict | None = self._query_one("SELECT is_favorite FROM Person WHERE id = ?", (self.person_id,))
        if row:
            self.is_favorite = bool(row['is_favorite'])
    
    # ========================================
    # Helper Methods
    # ========================================
    
    def _calculate_box_width(self) -> float:
        """Return fixed box width."""
        return self.BOX_MIN_WIDTH

    def _get_display_name_lines(self) -> tuple[str, str | None]:
        """Get name text, split across two lines if exceeds 32 characters."""
        if not self.person:
            return ("", None)
        
        full_name: str = f"{self.person.first_name} {self.person.last_name}"
        
        if len(full_name) <= 32:
            return (full_name, None)
        
        metrics: QFontMetrics = QFontMetrics(self._font_name_bold)
        gear_space: int = 30
        available_width: float = self.BOX_MIN_WIDTH - (self.PHOTO_SIZE + 15 + self.TEXT_PADDING) - gear_space
        
        first_name: str = self.person.first_name
        last_name: str = self.person.last_name
        
        if metrics.horizontalAdvance(first_name) <= available_width:
            return (first_name, last_name)
        
        for i in range(len(first_name), 0, -1):
            truncated: str = first_name[:i] + "..."
            if metrics.horizontalAdvance(truncated) <= available_width:
                return (truncated, last_name)
        
        return (first_name[:10] + "...", last_name)
    
    def _get_birth_display_text(self) -> str:
        """Get birth date display text with month if available."""
        if not self.person:
            return "?"
        return self.person.get_birth_date_string()
    
    def _get_death_display_text(self) -> str:
        """Get death date display text with month if available."""
        if not self.person:
            return ""
        
        if not self.person.is_deceased:
            return ""
        
        return self.person.get_death_date_string()

    def _is_sick(self) -> bool:
        """Check if person has any active illness events."""
        if not self.db or not self.db.conn:
            return False
        
        cursor = self.db.conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) as count FROM Event WHERE person_id = ? AND event_type = 'Illness' AND (end_year IS NULL OR end_year >= ?)",
            (self.person_id, self.current_year)
        )
        row = cursor.fetchone()
        return row['count'] > 0 if row else False
    
    def _is_immigrant(self) -> bool:
        """Check if person immigrated."""
        if not self.person:
            return False
        has_arrival_date: bool = self.person.arrival_year is not None
        is_not_founder: bool = not self.person.is_founder
        return has_arrival_date and is_not_founder
    
    def _get_gender_symbol(self) -> str:
        """Get the gender symbol for display."""
        if not self.person:
            return "⚲"
        return {"Male": "♂", "Female": "♀"}.get(self.person.gender, "⚲")
    
    def _get_age_text(self) -> str:
        """Generate age text like 'd. 64 (now 108)' or 'Age: 45'."""
        if not self.person or not self.person.birth_year:
            return ""
        
        is_deceased: bool = self.person.is_deceased
        has_death_year: bool = self.person.death_year is not None
        
        if is_deceased and has_death_year:
            age_at_death: int | None = self.person.get_age_at_death()
            if age_at_death is None:
                return "d. ?"
            would_be_age: int = self.current_year - self.person.birth_year
            return f"d. {age_at_death} (now {would_be_age})"
        
        current_age: int | None = self.person.get_age(self.current_year)
        return f"Age: {current_age}" if current_age else ""
    
    def _get_star_rect(self) -> QRectF:
        """Get clickable area for favorite star."""
        star_x: float = self.box_width - 55
        star_y: float = 10
        return QRectF(star_x, star_y, self.FAVORITE_STAR_SIZE, self.FAVORITE_STAR_SIZE)
    
    def _get_name_rect(self) -> QRectF:
        """Get hoverable area for tooltip trigger."""
        return QRectF(0, 0, self.box_width, self.box_height)
    
    def _is_mouse_near_tooltip(self, mouse_pos: QPointF) -> bool:
        """Check if mouse is in grace area between box and tooltip."""
        if not self._tooltip_panel:
            return False
        
        grace_width: int = 30
        grace_rect: QRectF = QRectF(
            self.box_width - grace_width,
            0,
            self.TOOLTIP_OFFSET_X + grace_width * 2,
            self.box_height
        )
        return grace_rect.contains(mouse_pos)
    
    def _stop_tooltip_timer(self) -> None:
        """Stop tooltip delay timer."""
        self._tooltip_delay_timer.stop()

    def _format_date_for_box(self, year: int | None, month: int | None) -> str:
        """Format date for PersonBox display with full month name."""
        if year is None:
            return "?"
        
        month_names: dict[int, str] = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        
        if month:
            month_name: str = month_names.get(month, '')
            return f"{month_name} {year}"
        else:
            return str(year)
    
    # ========================================
    # Painting
    # ========================================
    
    def paint(self, painter: QPainter, option, widget=None) -> None:
        """Draw the person box with all visual elements."""
        if not self.person:
            return
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        border_color: QColor = self.COLOR_DECEASED if self.person.is_deceased else self.COLOR_LIVING
        painter.setPen(QPen(border_color, self.BORDER_WIDTH))
        painter.setBrush(QBrush(self.COLOR_BG))
        painter.drawRoundedRect(
            QRectF(0, 0, self.box_width, self.box_height), 
            self.CORNER_RADIUS, 
            self.CORNER_RADIUS
        )
        
        photo_rect: QRectF = QRectF(
            self.BORDER_WIDTH, 
            self.BORDER_WIDTH, 
            self.PHOTO_SIZE + 10, 
            self.box_height - 2 * self.BORDER_WIDTH
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(245, 245, 245)))
        
        path: QPainterPath = QPainterPath()
        path.addRoundedRect(photo_rect, self.CORNER_RADIUS, self.CORNER_RADIUS)
        painter.setClipPath(path)
        painter.drawRect(photo_rect)
        painter.setClipping(False)
        
        if self.portrait_pixmap:
            x_offset: float = (self.PHOTO_SIZE + 10 - self.portrait_pixmap.width()) / 2 + self.BORDER_WIDTH
            y_offset: float = (self.box_height - self.portrait_pixmap.height()) / 2
            painter.drawPixmap(int(x_offset), int(y_offset), self.portrait_pixmap)
        else:
            self._draw_placeholder_portrait(painter, photo_rect)
        
        separator_x: float = self.PHOTO_SIZE + 15
        painter.setPen(QPen(self.COLOR_SEPARATOR, 1))
        painter.drawLine(
            int(separator_x), 
            int(self.BORDER_WIDTH + 5), 
            int(separator_x), 
            int(self.box_height - self.BORDER_WIDTH - 5)
        )
        
        self._draw_text_content(painter, separator_x + self.TEXT_PADDING)
        
        should_draw_star: bool = self._is_hovered or self.is_favorite
        if should_draw_star:
            self._draw_favorite_star(painter)
    
    def _draw_placeholder_portrait(self, painter: QPainter, photo_rect: QRectF) -> None:
        """Draw silhouette placeholder when no portrait exists."""
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        
        center_x: float = photo_rect.center().x()
        center_y: float = photo_rect.top() + 30
        painter.drawEllipse(QPointF(center_x, center_y), 15, 15)
        
        body_width: float = 30
        body_height: float = 35
        body_x: float = center_x - body_width / 2
        body_y: float = center_y + 18
        painter.drawRoundedRect(QRectF(body_x, body_y, body_width, body_height), 5, 5)
        
        painter.setFont(QFont("Segoe UI", 7))
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        text_rect: QRectF = QRectF(photo_rect.left() + 5, photo_rect.top() + 85, photo_rect.width() - 10, 25)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "Click to add\nportrait")
    
    def _draw_text_content(self, painter: QPainter, start_x: float) -> None:
        """Draw all text content on right side of box."""
        if not self.person:
            return
        
        icon_y: float = 25
        icon_x: float = start_x
        
        painter.setFont(self._font_icon)
        painter.setPen(QPen(self.COLOR_TEXT))
        
        icon_conditions: list[tuple[bool, str]] = [
            (self.person.is_founder, "🍃"),
            (self._is_immigrant(), "↓"),
            (self.person.is_deceased, "💀"),
            (self._is_sick(), "🤒")
        ]
        
        for condition, icon in icon_conditions:
            if condition:
                painter.drawText(int(icon_x), int(icon_y), icon)
                icon_x += 20
        
        painter.drawText(int(self.box_width - 30), int(icon_y), "⚙")
        
        name_line1, name_line2 = self._get_display_name_lines()
        name_y: float = 50
        
        painter.setFont(self._font_name_bold)
        painter.drawText(int(start_x), int(name_y), name_line1)
        
        if name_line2:
            name_y += 18
            painter.drawText(int(start_x), int(name_y), name_line2)
        
        painter.setFont(self._font_normal)
        painter.setPen(QPen(QColor(100, 100, 100)))
        
        gender_y: float = name_y + 18
        gender_text: str = f"{self._get_gender_symbol()} {self.person.gender}"
        painter.drawText(int(start_x), int(gender_y), gender_text)
        
        current_y: float = gender_y + 16
        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QPen(self.COLOR_TEXT))
        
        has_arrival: bool = self.person.arrival_year is not None
        
        if has_arrival:
            arrival_text: str = self._format_date_for_box(
                self.person.arrival_year,
                self.person.arrival_month
            )
            
            has_departure: bool = self.person.moved_out_year is not None
            
            if has_departure:
                departure_text: str = self._format_date_for_box(
                    self.person.moved_out_year,
                    self.person.moved_out_month
                )
                painter.drawText(int(start_x), int(current_y), f"A: {arrival_text} | D: {departure_text}")
            else:
                painter.drawText(int(start_x), int(current_y), f"A: {arrival_text}")
            
            current_y += 14

        birth_text: str = self._format_date_for_box(
            self.person.birth_year,
            self.person.birth_month
        )

        if self.person.is_deceased:
            death_text: str = self._format_date_for_box(
                self.person.death_year,
                self.person.death_month
            )
            life_dates: str = f"b. {birth_text} - d. {death_text}"
        else:
            life_dates: str = f"b. {birth_text} -"

        painter.drawText(int(start_x), int(current_y), life_dates)
        current_y += 14

        painter.setPen(QPen(QColor(100, 100, 100)))

        if self.person.is_deceased:
            age_at_death: int | None = self.person.get_age_at_death()
            if age_at_death is not None:
                painter.drawText(int(start_x), int(current_y), f"Died at {age_at_death} years old")
                current_y += 14
            
            if self.person.birth_year:
                years_since_birth: int = self.current_year - self.person.birth_year
                painter.drawText(int(start_x), int(current_y), f"Age: {years_since_birth}")
        else:
            current_age: int | None = self.person.get_age(self.current_year)
            if current_age is not None:
                painter.drawText(int(start_x), int(current_y), f"Age: {current_age}")
            
    def _draw_favorite_star(self, painter: QPainter) -> None:
        """Draw favorite star (filled if favorite, hollow if hovering)."""
        painter.setFont(QFont("Segoe UI Emoji", 16))
        
        star_x: float = self.box_width - 55
        star_y: float = 10
        
        if self.is_favorite:
            painter.setPen(QPen(self.COLOR_FAVORITE_STAR))
            painter.drawText(int(star_x), int(star_y + 15), "★")
        elif self._is_star_hovered or self._is_hovered:
            painter.setPen(QPen(self.COLOR_FAVORITE_HOVER))
            painter.drawText(int(star_x), int(star_y + 15), "☆")
    
    # ========================================
    # Tooltip Management
    # ========================================
    
    def _show_enhanced_tooltip(self) -> None:
        """Show enhanced tooltip panel next to person box."""
        tooltip_already_exists: bool = self._tooltip_panel is not None
        no_scene_available: bool = not self.scene()
        
        if tooltip_already_exists or no_scene_available:
            return
        
        from views.tree_view.enhanced_tooltip_panel import EnhancedTooltipPanel
        
        self._tooltip_panel = EnhancedTooltipPanel(self.person_id, self.db, self.current_year)
        
        if not self._tooltip_panel:
            return
        
        self._tooltip_panel.parent_person_box = self
        self._tooltip_panel.manually_moved.connect(self._on_tooltip_manually_moved)
        self._tooltip_panel.closed.connect(self._on_tooltip_closed)
        
        tooltip_x: float = self.pos().x() + self.box_width + self.TOOLTIP_OFFSET_X
        tooltip_y: float = self.pos().y()
        self._tooltip_panel.setPos(tooltip_x, tooltip_y)
        
        self.scene().addItem(self._tooltip_panel)

    def _on_tooltip_manually_moved(self) -> None:
        """Handle tooltip being manually repositioned by user."""
        self._tooltip_manually_positioned = True
    
    def _on_tooltip_closed(self) -> None:
        """Handle tooltip being closed."""
        self._tooltip_panel = None
    
    def _hide_enhanced_tooltip(self) -> None:
        """Remove enhanced tooltip from scene."""
        if self._tooltip_panel and self.scene():
            self.scene().removeItem(self._tooltip_panel)
            self._tooltip_panel = None

    def _check_hide_tooltip(self) -> None:
        """Check if tooltip should be hidden after leaving person box."""
        if not self._tooltip_panel:
            return
        
        tooltip_is_hovered: bool = self._tooltip_panel.is_hovered
        tooltip_is_locked: bool = self._tooltip_panel.is_locked
        
        should_keep_tooltip: bool = tooltip_is_hovered or tooltip_is_locked
        
        if not should_keep_tooltip:
            self._hide_enhanced_tooltip()
    
    # ========================================
    # Qt Event Handlers
    # ========================================
    
    def boundingRect(self) -> QRectF:
        """Define widget bounds for Qt rendering system."""
        return QRectF(0, 0, self.box_width, self.box_height)
    
    def hoverEnterEvent(self, event) -> None:
        """Start tooltip delay timer when mouse enters box."""
        self._is_hovered = True
        self._tooltip_delay_timer.start(self.TOOLTIP_DELAY)
        self.update()
        super().hoverEnterEvent(event)
    
    def hoverMoveEvent(self, event) -> None:
        """Track hover state for name and star areas."""
        mouse_position: QPointF = event.pos()
        
        self._is_name_hovered = self._get_name_rect().contains(mouse_position)
        self._is_star_hovered = self._get_star_rect().contains(mouse_position)
        
        mouse_left_box: bool = not self._is_name_hovered
        tooltip_exists: bool = self._tooltip_panel is not None
        tooltip_unlocked: bool = not (self._tooltip_panel.is_locked if self._tooltip_panel else False)
        mouse_not_near_tooltip: bool = not self._is_mouse_near_tooltip(mouse_position)
        
        should_hide_tooltip: bool = (
            mouse_left_box and 
            tooltip_exists and 
            tooltip_unlocked and 
            mouse_not_near_tooltip
        )
        
        if should_hide_tooltip:
            self._hide_enhanced_tooltip()
        
        self.update()
        super().hoverMoveEvent(event)
    
    def hoverLeaveEvent(self, event) -> None:
        """Stop timers and potentially hide tooltip when mouse leaves."""
        self._is_hovered = False
        self._is_name_hovered = False
        self._is_star_hovered = False
        self._stop_tooltip_timer()
        
        tooltip_exists: bool = self._tooltip_panel is not None
        tooltip_is_unlocked: bool = not (self._tooltip_panel.is_locked if self._tooltip_panel else True)
        
        if tooltip_exists and tooltip_is_unlocked:
            QTimer.singleShot(200, self._check_hide_tooltip)
        
        self.update()
        super().hoverLeaveEvent(event)
    
    def mousePressEvent(self, event) -> None:
        """Handle clicks on star (favorite toggle) or box (drag start)."""
        is_left_click: bool = event.button() == Qt.MouseButton.LeftButton
        
        if not is_left_click:
            super().mousePressEvent(event)
            return
        
        click_position: QPointF = event.pos()
        clicked_on_star: bool = self._get_star_rect().contains(click_position)
        
        if clicked_on_star:
            self.is_favorite = not self.is_favorite
            self.favorite_toggled.emit(self.person_id, self.is_favorite)
            self._save_favorite_status()
            self.update()
            return
        
        self._is_dragging = True
        self._drag_start_pos = click_position
        self.person_selected.emit(self.person_id)
        self._stop_tooltip_timer()
        
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """Handle dragging - move box and tooltip together if not manually positioned."""
        if not self._is_dragging:
            super().mouseMoveEvent(event)
            return
        
        self._stop_tooltip_timer()
        
        tooltip_exists: bool = self._tooltip_panel is not None

        if tooltip_exists and self._tooltip_panel:
            expected_x: float = self.pos().x() + self.box_width + self.TOOLTIP_OFFSET_X
            expected_y: float = self.pos().y()
            
            actual_x: float = self._tooltip_panel.pos().x()
            actual_y: float = self._tooltip_panel.pos().y()
            
            position_tolerance: int = 10
            x_difference: float = abs(actual_x - expected_x)
            y_difference: float = abs(actual_y - expected_y)
            
            is_in_default_position: bool = x_difference <= position_tolerance and y_difference <= position_tolerance
            should_move_tooltip: bool = is_in_default_position or not self._tooltip_manually_positioned
            
            if should_move_tooltip:
                self._tooltip_panel.setPos(expected_x, expected_y)
        
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event) -> None:
        """End drag operation."""
        is_left_click: bool = event.button() == Qt.MouseButton.LeftButton
        if is_left_click:
            self._is_dragging = False
        super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event) -> None:
        """Emit signal on double-click."""
        is_left_click: bool = event.button() == Qt.MouseButton.LeftButton
        if is_left_click:
            self.person_double_clicked.emit(self.person_id)
        super().mouseDoubleClickEvent(event)
    
    def _save_favorite_status(self) -> None:
        """Persist favorite status to database."""
        if not self.db or not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        favorite_value: int = 1 if self.is_favorite else 0
        cursor.execute(
            "UPDATE Person SET is_favorite = ? WHERE id = ?",
            (favorite_value, self.person_id)
        )
        self.db.conn.commit()