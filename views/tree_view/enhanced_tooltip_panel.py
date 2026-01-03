"""Enhanced tooltip panel for person details."""

from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtCore import Qt, QRectF, Signal, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QCursor
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from models.person import Person
    from database.db_manager import DatabaseManager
    from views.tree_view.person_box import PersonBox


class EnhancedTooltipPanel(QGraphicsWidget):
    """Enhanced tooltip showing detailed person information."""
    
    closed: Signal = Signal()
    manually_moved: Signal = Signal()
    
    PANEL_WIDTH: int = 300
    PANEL_HEIGHT: int = 600
    PADDING: int = 15
    CORNER_RADIUS: int = 8
    
    LOCK_ICON_SIZE: int = 10
    LOCK_INDICATOR_SIZE: int = 20
    LOCK_START_DELAY: int = 1000
    HOVER_LOCK_DURATION: int = 3000
    
    SECTION_HEADER_SPACING: int = 20
    SECTION_BOTTOM_SPACING: int = 10
    SEPARATOR_BOTTOM_SPACING: int = 15
    LINE_SPACING: int = 16
    LINE_SPACING_SMALL: int = 14
    LINE_SPACING_TINY: int = 4
    
    INDENT_LEVEL_0: int = 0
    INDENT_LEVEL_1: int = 10
    INDENT_LEVEL_2: int = 20
    INDENT_LEVEL_3: int = 30
    
    LOCK_ICON_OFFSET_X: float = 6.5
    LOCK_ICON_OFFSET_Y: float = 4
    LOCK_INDICATOR_X_OFFSET: int = 63
    LOCK_INDICATOR_Y_OFFSET: int = 15
    LOCK_ICON_CLICKABLE_SIZE: int = 25

    
    CLOSE_BUTTON_X_OFFSET: int = 30
    CLOSE_BUTTON_Y_OFFSET: int = 10
    CLOSE_BUTTON_SIZE: int = 20
    CLOSE_BUTTON_LINE_LENGTH: int = 15
    
    HEADER_HEIGHT: int = 50
    HEADER_PARTIAL_HEIGHT: int = 25
    HEADER_TEXT_Y_OFFSET: int = 10
    HEADER_TEXT_HEIGHT: int = 30
    HEADER_RIGHT_MARGIN: int = 70
    
    INITIAL_CONTENT_Y: int = 70
    DESCENDANTS_MAX_Y_OFFSET: int = 150
    EVENTS_MAX_Y_OFFSET: int = 20
    
    GENERATION_HEADER_Y_OFFSET: int = 14
    GENERATION_HEADER_HEIGHT: int = 16
    GENERATION_GROUP_SPACING: int = 18
    
    PERSON_ENTRY_NAME_OFFSET: int = 14
    PERSON_ENTRY_DATE_OFFSET: int = 16
    PERSON_ENTRY_DATE_INDENT: int = 10
    PERSON_ENTRY_ARRIVAL_OFFSET: int = 12
    
    SIBLING_DISPLAY_COUNT: int = 3
    SIBLING_OVERFLOW_INDENT: int = 10
    
    EVENT_TYPE_INDENT: int = 10
    
    PIE_START_ANGLE: int = 90 * 16
    PIE_FULL_CIRCLE: int = 360 * 16
    
    HOVER_HIDE_DELAY: int = 100
    
    COLOR_BG: QColor = QColor(255, 255, 255)
    COLOR_BORDER: QColor = QColor(100, 100, 255)
    COLOR_HEADER_BG: QColor = QColor(240, 240, 255)
    COLOR_TEXT: QColor = QColor(33, 33, 33)
    COLOR_TEXT_LIGHT: QColor = QColor(100, 100, 100)
    COLOR_CLOSE_BUTTON: QColor = QColor(200, 0, 0)
    COLOR_CLOSE_BUTTON_IDLE: QColor = QColor(150, 150, 150)
    COLOR_SEPARATOR: QColor = QColor(220, 220, 220)
    COLOR_LOCK_FILL: QColor = QColor(100, 100, 255)
    COLOR_LOCK_INDICATOR: QColor = QColor(100, 100, 255, 100)
    COLOR_LOCK_ICON_INACTIVE: QColor = QColor(80, 80, 80)
    
    def __init__(
        self,
        person_id: int,
        db_manager: 'DatabaseManager',
        current_year: int
    ) -> None:
        super().__init__()
        
        self.person_id: int = person_id
        self.db: 'DatabaseManager' = db_manager
        self.current_year: int = current_year
        
        self.person: 'Person | None' = None
        self.events: list = []
        self.relationships: dict = {}
        
        self._load_person_data()
        self._load_events()
        self.relationships = self._load_relationships()
        
        self.setMinimumSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)
        self.setMaximumSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)
        
        self._close_button_hovered: bool = False
        self._is_being_dragged: bool = False
        self._drag_start_pos: QPoint | None = None
        self.is_hovered: bool = False
        self.is_locked: bool = False
        self.parent_person_box: 'PersonBox | None' = None
        
        self._collapsed_generations: dict[str, bool] = {
            'descendants': False,
            'children': True,
            'grandchildren': True,
            'great_grandchildren': True,
            'great_great_grandchildren': True
        }
        self._generation_click_rects: dict[str, QRectF] = {}
        
        self._font_icon_small: QFont = QFont("Segoe UI Emoji", self.LOCK_ICON_SIZE)
        
        self._lock_delay_timer: QTimer = QTimer()
        self._lock_delay_timer.setSingleShot(True)
        self._lock_delay_timer.timeout.connect(self._start_lock_timer)
        
        self._hover_timer: QTimer = QTimer()
        self._hover_timer.setSingleShot(True)
        self._hover_timer.timeout.connect(self._on_hover_lock)
        
        self._animation_timer: QTimer = QTimer()
        self._animation_timer.setInterval(50)
        self._animation_timer.timeout.connect(self.update)
        
        self.setAcceptHoverEvents(True)
        self.setFlags(
            QGraphicsWidget.GraphicsItemFlag.ItemIsMovable |
            QGraphicsWidget.GraphicsItemFlag.ItemIsSelectable
        )
    
    # ========================================
    # Data Loading
    # ========================================
    
    def _load_person_data(self) -> None:
        """Load person data from database."""
        if not self.db or not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM Person WHERE id = ?", (self.person_id,))
        row = cursor.fetchone()
        
        if not row:
            return
        
        person_dict: dict = dict(row)
        
        from models.person import Person
        
        self.person = Person(
            id=person_dict.get('id'),
            first_name=person_dict.get('first_name', ''),
            middle_name=person_dict.get('middle_name', ''),
            last_name=person_dict.get('last_name', ''),
            maiden_name=person_dict.get('maiden_name') or '',
            nickname=person_dict.get('nickname', ''),
            gender=person_dict.get('gender', 'Unknown'),
            birth_year=person_dict.get('birth_year'),
            birth_month=person_dict.get('birth_month'),
            birth_day=person_dict.get('birth_day'),
            death_year=person_dict.get('death_year'),
            death_month=person_dict.get('death_month'),
            death_day=person_dict.get('death_day'),
            arrival_year=person_dict.get('arrival_year'),
            arrival_month=person_dict.get('arrival_month'),
            arrival_day=person_dict.get('arrival_day'),
            moved_out_year=person_dict.get('moved_out_year'),
            moved_out_month=person_dict.get('moved_out_month'),
            moved_out_day=person_dict.get('moved_out_day'),
            father_id=person_dict.get('father_id'),
            mother_id=person_dict.get('mother_id'),
            family_id=person_dict.get('family_id'),
            dynasty_id=person_dict.get('dynasty_id', 1),
            is_founder=bool(person_dict.get('is_founder', 0)),
            education=person_dict.get('education', 0),
            notes=person_dict.get('notes', '')
        )
    
    def _load_events(self) -> None:
        """Load events for this person."""
        if not self.db or not self.db.conn:
            return
        
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT * FROM Event 
            WHERE person_id = ?
            ORDER BY start_year, start_month, start_day
        """, (self.person_id,))
        
        self.events = cursor.fetchall()
    
    def _load_relationships(self) -> dict:
        """Load family relationships including full and half siblings."""
        if not self.db or not self.db.conn or not self.person:
            return {}
        
        cursor = self.db.conn.cursor()

        siblings: dict[str, list[str]] = {
            'brothers': [], 
            'sisters': [], 
            'other': [],
            'half_brothers': [],
            'half_sisters': [],
            'half_other': []
        }
        
        has_parents: bool = self.person.father_id is not None or self.person.mother_id is not None
        
        if has_parents:
            cursor.execute("""
                SELECT id, first_name, last_name, gender, father_id, mother_id
                FROM Person 
                WHERE (father_id = ? OR mother_id = ?)
                AND id != ?
            """, (self.person.father_id, self.person.mother_id, self.person_id))
            
            for row in cursor.fetchall():
                sibling: dict = dict(row)
                sibling_name: str = f"{sibling['first_name']} {sibling['last_name']}"
                
                shares_father: bool = sibling['father_id'] == self.person.father_id and self.person.father_id is not None
                shares_mother: bool = sibling['mother_id'] == self.person.mother_id and self.person.mother_id is not None
                is_full_sibling: bool = shares_father and shares_mother
                
                sibling_gender: str = sibling['gender']
                category_suffix: str = '' if is_full_sibling else 'half_'
                
                if sibling_gender == 'Male':
                    siblings[f'{category_suffix}brothers'].append(sibling_name)
                elif sibling_gender == 'Female':
                    siblings[f'{category_suffix}sisters'].append(sibling_name)
                else:
                    siblings[f'{category_suffix}other'].append(sibling_name)

        descendants: dict = self._load_all_descendants()
        
        return {
            'siblings': siblings,
            'descendants': descendants
        }

    def _load_all_descendants(self) -> dict[str, list[dict] | dict]:
        """Load all descendants with full details for collapsible list."""
        if not self.db or not self.db.conn:
            return {'all': [], 'by_generation': {}}
        
        cursor = self.db.conn.cursor()
        
        cursor.execute("""
            SELECT id, first_name, last_name, birth_year, death_year, gender, arrival_year, moved_out_year
            FROM Person 
            WHERE father_id = ? OR mother_id = ?
            ORDER BY birth_year
        """, (self.person_id, self.person_id))
        
        children: list[dict] = [dict(row) for row in cursor.fetchall()]
        all_descendants: list[dict] = []
        descendants_by_generation: dict[str, list[dict]] = {'children': children}
        
        for child in children:
            all_descendants.append(self._create_descendant_dict(child, 'child'))
        
        current_generation_ids: list[int] = [c['id'] for c in children]
        generation_names: list[str] = ['grandchildren', 'great_grandchildren', 'great_great_grandchildren']
        
        for generation_name in generation_names:
            if not current_generation_ids:
                break
            
            next_generation: list[dict] = self._fetch_generation(cursor, current_generation_ids)
            
            if next_generation:
                descendants_by_generation[generation_name] = next_generation
                
                for person in next_generation:
                    generation_label: str = generation_name.replace('_', ' ')
                    all_descendants.append(self._create_descendant_dict(person, generation_label))
                
                current_generation_ids = [p['id'] for p in next_generation]
            else:
                break
        
        return {
            'all': all_descendants,
            'by_generation': descendants_by_generation
        }

    def _fetch_generation(self, cursor, parent_ids: list[int]) -> list[dict]:
        """Fetch a generation of descendants given parent IDs."""
        placeholders: str = ','.join('?' * len(parent_ids))
        cursor.execute(f"""
            SELECT id, first_name, last_name, birth_year, death_year, gender, arrival_year, moved_out_year
            FROM Person 
            WHERE father_id IN ({placeholders}) OR mother_id IN ({placeholders})
            ORDER BY birth_year
        """, parent_ids + parent_ids)
        
        return [dict(row) for row in cursor.fetchall()]

    def _create_descendant_dict(self, person: dict, generation: str) -> dict:
        """Create standardized descendant dictionary."""
        return {
            'id': person['id'],
            'first_name': person['first_name'],
            'last_name': person['last_name'],
            'name': f"{person['first_name']} {person['last_name']}",
            'generation': generation,
            'gender': person.get('gender', 'Unknown'),
            'birth_year': person['birth_year'],
            'death_year': person['death_year'],
            'arrival_year': person.get('arrival_year'),
            'moved_out_year': person.get('moved_out_year')
        }
    
    # ========================================
    # Helper Methods
    # ========================================
    
    def _get_close_button_rect(self) -> QRectF:
        """Get close button clickable area."""
        close_x: float = self.PANEL_WIDTH - self.CLOSE_BUTTON_X_OFFSET
        close_y: float = self.CLOSE_BUTTON_Y_OFFSET
        return QRectF(close_x, close_y, self.CLOSE_BUTTON_SIZE, self.CLOSE_BUTTON_SIZE)
    
    def _get_lock_icon_rect(self) -> QRectF:
        """Get clickable area for lock icon."""
        indicator_x: float = self.PANEL_WIDTH - self.LOCK_INDICATOR_X_OFFSET
        indicator_y: float = self.LOCK_ICON_OFFSET_Y
        return QRectF(indicator_x - 5, indicator_y, self.LOCK_ICON_CLICKABLE_SIZE, 20)
    
    def _get_generation_header_rect(self, y: float, generation_key: str) -> QRectF:
        """Get clickable rectangle for generation header."""
        if generation_key == 'descendants':
            rect: QRectF = QRectF(
                self.PADDING + self.INDENT_LEVEL_1, 
                y - self.GENERATION_HEADER_Y_OFFSET, 
                self.PANEL_WIDTH - self.PADDING - self.INDENT_LEVEL_2, 
                self.GENERATION_HEADER_HEIGHT
        )
        else:
            rect: QRectF = QRectF(
                self.PADDING + self.INDENT_LEVEL_1, 
                y - self.GENERATION_HEADER_Y_OFFSET, 
                self.PANEL_WIDTH - self.PADDING - self.INDENT_LEVEL_2, 
                self.GENERATION_HEADER_HEIGHT
        )
        self._generation_click_rects[generation_key] = rect
        return rect
    
    def _get_generation_display_name(self, generation_key: str) -> str:
        """Get display name for generation with proper formatting."""
        generation_names: dict[str, str] = {
            'children': 'Children',
            'grandchildren': 'Grandchildren',
            'great_grandchildren': 'Great Grandchildren',
            'great_great_grandchildren': 'G² Grandchildren'
        }
        
        if generation_key.startswith('great_'):
            great_count: int = generation_key.count('great_')
            if great_count > 2:
                return f"G^{great_count} Grandchildren"
        
        return generation_names.get(generation_key, generation_key.replace('_', ' ').title())
    
    def _get_gender_symbol(self, gender: str) -> str:
        """Get gender symbol for display."""
        return {"Male": "♂", "Female": "♀"}.get(gender, "⚲")
    
    def _toggle_generation(self, generation_key: str) -> None:
        """Toggle collapse state for a generation and repaint."""
        current_state: bool = self._collapsed_generations.get(generation_key, True)
        self._collapsed_generations[generation_key] = not current_state
        self.update()
    
    def _start_lock_timer(self) -> None:
        """Start the hover lock timer."""
        if not self.is_locked:
            self._hover_timer.start(self.HOVER_LOCK_DURATION)
            self._animation_timer.start()
    
    def _on_hover_lock(self) -> None:
        """Called when lock timer completes."""
        self.is_locked = True
        self._animation_timer.stop()
        self.update()
    
    def _check_self_hide(self) -> None:
        """Hide tooltip if mouse isn't back in it and not locked."""
        mouse_not_in_tooltip: bool = not self.is_hovered
        tooltip_not_locked: bool = not self.is_locked
        
        should_hide: bool = mouse_not_in_tooltip and tooltip_not_locked
        
        if should_hide and self.scene():
            self.scene().removeItem(self)
            self.closed.emit()
    
    def _format_single_date(self, year: int | None, month: int | None, day: int | None) -> str:
        """Format a single date with month abbreviation."""
        if year is None:
            return "?"
        
        month_names: dict[int, str] = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        
        if day and month:
            month_abbr: str = month_names.get(month, '')
            return f"{day} {month_abbr} {year}"
        elif month:
            month_abbr: str = month_names.get(month, '')
            return f"{month_abbr} {year}"
        else:
            return str(year)

    def _format_years(self, birth_year: int | None, death_year: int | None) -> str:
        """Format birth and death years for display."""
        birth_text: str = f"b. {birth_year}" if birth_year else "b. ?"
        
        if death_year:
            return f"({birth_text} - d. {death_year})"
        
        return f"({birth_text})"
    
    def _format_person_dates(self, person: dict) -> str:
        """Format all important dates for a person."""
        dates_parts: list[str] = []
        
        arrival_year: int | None = person.get('arrival_year')
        arrival_month: int | None = person.get('arrival_month')
        moved_out_year: int | None = person.get('moved_out_year')
        moved_out_month: int | None = person.get('moved_out_month')
        birth_year: int | None = person.get('birth_year')
        birth_month: int | None = person.get('birth_month')
        death_year: int | None = person.get('death_year')
        death_month: int | None = person.get('death_month')
        
        arrival_text: str = f"Arrival {arrival_month} {arrival_year}"
        if arrival_year and moved_out_year:
            dates_parts.append(f"{arrival_text} - Departure {moved_out_month} {moved_out_year}")
        elif arrival_year:
            dates_parts.append(f"{arrival_text}")

        birth_text: str = f"b. {birth_month} {birth_year}" if birth_month and birth_year else "b. ?"
        if death_year:
            dates_parts.append(f"{birth_text} - d. {death_month} {death_year}")
        else:
            dates_parts.append(birth_text)
        
        return " | ".join(dates_parts) if dates_parts else ""
    
    def _draw_section_header(self, painter: QPainter, y: float, section_font: QFont, text: str) -> float:
        """Draw a section header and return updated y position."""
        painter.setFont(section_font)
        painter.setPen(QPen(self.COLOR_TEXT))
        painter.drawText(self.PADDING, int(y), text)
        return y + self.SECTION_HEADER_SPACING
    
    def _draw_separator_line(self, painter: QPainter, y: float) -> float:
        """Draw horizontal separator line and return updated y position."""
        painter.setPen(QPen(self.COLOR_SEPARATOR, 1))
        painter.drawLine(self.PADDING, int(y), self.PANEL_WIDTH - self.PADDING, int(y))
        return y + self.SEPARATOR_BOTTOM_SPACING
    
    # ========================================
    # Painting
    # ========================================
    
    def paint(self, painter: QPainter, option, widget=None) -> None:
        """Draw the tooltip panel."""
        if not self.person:
            return
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setPen(QPen(self.COLOR_BORDER, 2))
        painter.setBrush(QBrush(self.COLOR_BG))
        painter.drawRoundedRect(
            QRectF(0, 0, self.PANEL_WIDTH, self.PANEL_HEIGHT),
            self.CORNER_RADIUS,
            self.CORNER_RADIUS
        )
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.COLOR_HEADER_BG))
        painter.drawRoundedRect(
            QRectF(0, 0, self.PANEL_WIDTH, self.HEADER_HEIGHT),
            self.CORNER_RADIUS,
            self.CORNER_RADIUS
        )
        painter.drawRect(QRectF(0, self.HEADER_PARTIAL_HEIGHT, self.PANEL_WIDTH, self.HEADER_PARTIAL_HEIGHT))
        
        self._draw_lock_indicator(painter)
        self._draw_close_button(painter)
        self._draw_header(painter)
        self._draw_content(painter)
    
    def _draw_lock_indicator(self, painter: QPainter) -> None:
        """Draw lock indicator with countdown animation and clickable icon."""
        indicator_x: float = self.PANEL_WIDTH - self.LOCK_INDICATOR_X_OFFSET
        indicator_y: float = self.LOCK_INDICATOR_Y_OFFSET
        center_x: float = indicator_x + self.LOCK_INDICATOR_SIZE / 2
        center_y: float = indicator_y + self.LOCK_INDICATOR_SIZE / 2
        
        is_timer_active: bool = self._hover_timer.isActive()
        
        if is_timer_active:
            elapsed: int = self._hover_timer.interval() - self._hover_timer.remainingTime()
            fill_percent: float = min(1.0, elapsed / self.HOVER_LOCK_DURATION)
            
            painter.setPen(QPen(self.COLOR_LOCK_INDICATOR, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(
                int(indicator_x), 
                int(indicator_y), 
                self.LOCK_INDICATOR_SIZE, 
                self.LOCK_INDICATOR_SIZE
            )
            
            if fill_percent > 0:
                painter.setBrush(QBrush(self.COLOR_LOCK_FILL))
                span_angle: int = int(-self.PIE_FULL_CIRCLE * fill_percent)
                painter.drawPie(
                    int(indicator_x), 
                    int(indicator_y), 
                    self.LOCK_INDICATOR_SIZE, 
                    self.LOCK_INDICATOR_SIZE,
                    self.PIE_START_ANGLE,
                    span_angle
                )
        
        painter.setFont(self._font_icon_small)
        
        if self.is_locked:
            painter.setPen(QPen(self.COLOR_LOCK_FILL))
            painter.drawText(
                int(center_x - self.LOCK_ICON_OFFSET_X), 
                int(center_y + self.LOCK_ICON_OFFSET_Y), 
                "🔒"
            )
        else:
            painter.setPen(QPen(self.COLOR_LOCK_ICON_INACTIVE))
            painter.drawText(
                int(center_x - self.LOCK_ICON_OFFSET_X), 
                int(center_y + self.LOCK_ICON_OFFSET_Y), 
                "🔓"
            )
    
    def _draw_close_button(self, painter: QPainter) -> None:
        """Draw close button."""
        close_x: float = self.PANEL_WIDTH - self.CLOSE_BUTTON_X_OFFSET
        close_y: float = self.CLOSE_BUTTON_Y_OFFSET
        button_color: QColor = self.COLOR_CLOSE_BUTTON if self._close_button_hovered else self.COLOR_CLOSE_BUTTON_IDLE
        
        painter.setPen(QPen(button_color, 2))
        painter.drawLine(
            int(close_x), 
            int(close_y), 
            int(close_x + self.CLOSE_BUTTON_LINE_LENGTH), 
            int(close_y + self.CLOSE_BUTTON_LINE_LENGTH)
        )
        painter.drawLine(
            int(close_x + self.CLOSE_BUTTON_LINE_LENGTH), 
            int(close_y), 
            int(close_x), 
            int(close_y + self.CLOSE_BUTTON_LINE_LENGTH)
        )
    
    def _draw_header(self, painter: QPainter) -> None:
        """Draw header with person name."""
        if not self.person:
            return
        
        painter.setPen(QPen(self.COLOR_TEXT))
        title_font: QFont = QFont("Segoe UI", 12, QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.drawText(
            QRectF(
                self.PADDING, 
                self.HEADER_TEXT_Y_OFFSET, 
                self.PANEL_WIDTH - self.HEADER_RIGHT_MARGIN, 
                self.HEADER_TEXT_HEIGHT
            ), 
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 
            self.person.full_name
        )
    
    def _draw_content(self, painter: QPainter) -> None:
        """Draw all content sections."""
        y: float = self.INITIAL_CONTENT_Y
        normal_font: QFont = QFont("Segoe UI", 9)
        section_font: QFont = QFont("Segoe UI", 10, QFont.Weight.Bold)
        
        section_methods: list[Callable] = [
            self._draw_statistics,
            self._draw_relationships,
            self._draw_descendants,
            self._draw_events
        ]
        
        for section_method in section_methods:
            y = section_method(painter, y, section_font, normal_font)
    
    def _draw_statistics(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        """Draw statistics section."""
        if not self.person:
            return y
        
        y = self._draw_section_header(painter, y, section_font, "Statistics")
        
        painter.setFont(normal_font)
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        
        stats: list[str] = [
            f"Birth: {self._format_single_date(self.person.birth_year, self.person.birth_month, self.person.birth_day)}",
            f"Death: {self._format_single_date(self.person.death_year, self.person.death_month, self.person.death_day)}" if self.person.is_deceased else "Status: Living",
            f"Age: {self.person.get_age(self.current_year) or 'Unknown'}",
        ]
        
        for stat in stats:
            painter.drawText(self.PADDING, int(y), stat)
            y += self.LINE_SPACING
        
        return y + self.SECTION_BOTTOM_SPACING
    
    def _draw_relationships(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        """Draw relationships section."""
        y = self._draw_section_header(painter, y, section_font, "Relationships")
        
        painter.setFont(normal_font)
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        
        siblings: dict[str, list[str]] = self.relationships.get('siblings', {})
        
        sibling_types: list[tuple[str, str]] = [
            ('brothers', 'Brothers'),
            ('half_brothers', 'Half-Brothers'),
            ('sisters', 'Sisters'),
            ('half_sisters', 'Half-Sisters'),
            ('other', 'Other Siblings'),
            ('half_other', 'Half-Siblings (Other)')
        ]
        
        for key, label in sibling_types:
            sibling_list: list[str] = siblings.get(key, [])
            if sibling_list:
                y = self._draw_sibling_group(painter, y, label, sibling_list)
        
        y += self.SECTION_BOTTOM_SPACING
        y = self._draw_separator_line(painter, y)
        return y

    def _draw_sibling_group(self, painter: QPainter, y: float, label: str, sibling_list: list[str]) -> float:
        """Draw a group of siblings with overflow handling."""
        displayed_names: str = ', '.join(sibling_list[:self.SIBLING_DISPLAY_COUNT])
        painter.drawText(self.PADDING, int(y), f"{label}: {displayed_names}")
        y += self.LINE_SPACING
        
        overflow_count: int = len(sibling_list) - self.SIBLING_DISPLAY_COUNT
        if overflow_count > 0:
            painter.drawText(
                self.PADDING + self.SIBLING_OVERFLOW_INDENT, 
                int(y), 
                f"...and {overflow_count} more"
            )
            y += self.LINE_SPACING
        
        return y
    
    def _draw_descendants(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        """Draw descendants section with collapsible generations."""
        descendants: dict = self.relationships.get('descendants', {})
        descendants_by_generation: dict = descendants.get('by_generation', {})
        all_descendants: list[dict] = descendants.get('all', [])
        
        if not all_descendants:
            return y
        
        is_collapsed: bool = self._collapsed_generations.get('descendants', False)
        arrow: str = "▶" if is_collapsed else "▼"
        
        painter.setFont(section_font)
        painter.setPen(QPen(self.COLOR_TEXT))
        painter.drawText(self.PADDING, int(y), f"Descendants ({len(all_descendants)}) {arrow}")
        self._get_generation_header_rect(y, 'descendants')
        
        y += self.SECTION_HEADER_SPACING
        
        if is_collapsed:
            y += self.SECTION_BOTTOM_SPACING
            y = self._draw_separator_line(painter, y)
            return y

        descendants_section_max_y: float = self.PANEL_HEIGHT - self.DESCENDANTS_MAX_Y_OFFSET
        
        generation_order: list[str] = sorted(
            descendants_by_generation.keys(),
            key=lambda x: (x.count('great_'), x)
        )
        
        for generation_key in generation_order:
            generation_list: list[dict] = descendants_by_generation[generation_key]
            if not generation_list:
                continue
            
            if y > descendants_section_max_y:
                break
            
            y = self._draw_generation_group(painter, y, generation_key, generation_list, normal_font, descendants_section_max_y)
        
        y += self.SECTION_BOTTOM_SPACING
        y = self._draw_separator_line(painter, y)
        return y

    def _draw_generation_group(
        self, 
        painter: QPainter, 
        y: float, 
        generation_key: str, 
        generation_list: list[dict],
        normal_font: QFont,
        max_y: float
    ) -> float:
        """Draw a collapsible generation group."""
        is_collapsed: bool = self._collapsed_generations.get(generation_key, True)
        arrow: str = "▶" if is_collapsed else "▼"
        
        generation_name: str = self._get_generation_display_name(generation_key)
        
        self._get_generation_header_rect(y, generation_key)
        
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        painter.setPen(QPen(self.COLOR_TEXT))
        painter.drawText(
            self.PADDING + self.INDENT_LEVEL_1, 
            int(y), 
            f"{arrow} {generation_name} ({len(generation_list)})"
        )
        y += self.GENERATION_GROUP_SPACING
        
        if is_collapsed:
            return y
        
        painter.setFont(normal_font)
        
        for person in generation_list:
            if y > max_y:
                remaining: int = len(generation_list) - generation_list.index(person)
                painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
                painter.drawText(self.PADDING + self.INDENT_LEVEL_2, int(y), f"...and {remaining} more")
                break
            
            y = self._draw_person_entry(painter, y, person)
        
        return y

    def _draw_person_entry(self, painter: QPainter, y: float, person: dict) -> float:
        """Draw a single person entry with name, gender, and dates on separate lines."""
        person_name: str = f"{person['first_name']} {person['last_name']}"
        gender_symbol: str = self._get_gender_symbol(person.get('gender', 'Unknown'))
        
        painter.setPen(QPen(self.COLOR_TEXT))
        painter.drawText(self.PADDING + self.INDENT_LEVEL_2, int(y), f"{person_name} {gender_symbol}")
        y += self.PERSON_ENTRY_NAME_OFFSET
        
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        painter.setFont(QFont("Segoe UI", 8))
        
        has_arrival: bool = person.get('arrival_year') is not None
        
        if has_arrival:
            arrival_text: str = self._format_single_date(
                person.get('arrival_year'),
                person.get('arrival_month'),
                person.get('arrival_day')
            )
            
            has_departure: bool = person.get('moved_out_year') is not None
            
            if has_departure:
                departure_text: str = self._format_single_date(
                    person.get('moved_out_year'),
                    person.get('moved_out_month'),
                    person.get('moved_out_day')
                )
                painter.drawText(self.PADDING + self.INDENT_LEVEL_3, int(y), f"Arr: {arrival_text} - Dep: {departure_text}")
            else:
                painter.drawText(self.PADDING + self.INDENT_LEVEL_3, int(y), f"Arrival: {arrival_text}")
            
            y += self.PERSON_ENTRY_ARRIVAL_OFFSET
        
        birth_text: str = self._format_single_date(
            person.get('birth_year'),
            person.get('birth_month'),
            person.get('birth_day')
        )
        
        has_death: bool = person.get('death_year') is not None
        
        if has_death:
            death_text: str = self._format_single_date(
                person.get('death_year'),
                person.get('death_month'),
                person.get('death_day')
            )
            painter.drawText(self.PADDING + self.INDENT_LEVEL_3, int(y), f"b. {birth_text} - d. {death_text}")
        else:
            painter.drawText(self.PADDING + self.INDENT_LEVEL_3, int(y), f"b. {birth_text}")
        
        painter.setFont(QFont("Segoe UI", 9))
        y += self.PERSON_ENTRY_DATE_OFFSET
        
        return y
    
    def _draw_events(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        """Draw events timeline section."""
        y = self._draw_section_header(painter, y, section_font, f"Life Events ({len(self.events)})")
        
        painter.setFont(normal_font)
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        
        max_y: float = self.PANEL_HEIGHT - self.PADDING
        event_count: int = 0
        
        for event in self.events:
            if y > max_y - self.EVENTS_MAX_Y_OFFSET:
                remaining_events: int = len(self.events) - event_count
                painter.drawText(self.PADDING, int(y), f"...and {remaining_events} more")
                break
            
            event_dict: dict = dict(event)
            event_year: str = str(event_dict.get('start_year', '?'))
            event_title: str = event_dict.get('event_title', 'Unknown')
            event_type: str = event_dict.get('event_type', '')
            
            painter.drawText(self.PADDING, int(y), f"{event_year}: {event_title}")
            y += self.LINE_SPACING_SMALL
            
            if event_type:
                painter.drawText(self.PADDING + self.EVENT_TYPE_INDENT, int(y), f"({event_type})")
                y += self.LINE_SPACING_SMALL
            
            event_count += 1
            y += self.LINE_SPACING_TINY
        
        return y
    
    # ========================================
    # Qt Event Handlers
    # ========================================
    
    def boundingRect(self) -> QRectF:
        """Define widget bounds for Qt rendering system."""
        return QRectF(0, 0, self.PANEL_WIDTH, self.PANEL_HEIGHT)

    def hoverEnterEvent(self, event) -> None:
        """Track when mouse enters tooltip and start lock delay timer."""
        self.is_hovered = True
        self._lock_delay_timer.start(self.LOCK_START_DELAY)
        super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event) -> None:
        """Track close button, lock icon, and generation header hover states."""
        mouse_position = event.pos()
        
        close_rect: QRectF = self._get_close_button_rect()
        self._close_button_hovered = close_rect.contains(mouse_position)
        
        lock_rect: QRectF = self._get_lock_icon_rect()
        lock_icon_hovered: bool = lock_rect.contains(mouse_position)
        
        hovering_header: bool = False
        for rect in self._generation_click_rects.values():
            if rect.contains(mouse_position):
                hovering_header = True
                break
        
        is_hovering_interactive_element: bool = self._close_button_hovered or hovering_header or lock_icon_hovered
        
        if is_hovering_interactive_element:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        self.update()
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        """Track when mouse leaves tooltip and potentially hide."""
        self.is_hovered = False
        self._lock_delay_timer.stop()
        self._hover_timer.stop()
        self._animation_timer.stop()
        
        if not self.is_locked:
            QTimer.singleShot(self.HOVER_HIDE_DELAY, self._check_self_hide)
        
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        """Handle clicks on close button, lock icon, generation headers, or start drag."""
        is_left_click: bool = event.button() == Qt.MouseButton.LeftButton
        
        if not is_left_click:
            super().mousePressEvent(event)
            return
        
        click_position = event.pos()
        
        close_rect: QRectF = self._get_close_button_rect()
        clicked_close_button: bool = close_rect.contains(click_position)
        
        if clicked_close_button:
            self.closed.emit()
            if self.scene():
                self.scene().removeItem(self)
            return
        
        lock_rect: QRectF = self._get_lock_icon_rect()
        clicked_lock_icon: bool = lock_rect.contains(click_position)
        
        if clicked_lock_icon:
            self.is_locked = not self.is_locked
            if self.is_locked:
                self._lock_delay_timer.stop()
                self._hover_timer.stop()
                self._animation_timer.stop()
            self.update()
            return
        
        for generation_key, rect in self._generation_click_rects.items():
            if rect.contains(click_position):
                self._toggle_generation(generation_key)
                return
        
        self._is_being_dragged = True
        self._drag_start_pos = click_position
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """Handle dragging."""
        if self._is_being_dragged:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Handle drag end and mark as manually moved."""
        is_left_click: bool = event.button() == Qt.MouseButton.LeftButton
        
        if is_left_click and self._is_being_dragged:
            self.manually_moved.emit()
            self._is_being_dragged = False
        
        super().mouseReleaseEvent(event)