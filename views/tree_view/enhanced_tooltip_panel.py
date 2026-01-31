"""Enhanced tooltip panel for person details."""

from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtCore import Qt, QRectF, Signal, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QCursor, QFontMetrics
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from models.person import Person
    from database.db_manager import DatabaseManager
    from views.tree_view.person_box import PersonBox


class EnhancedTooltipPanel(QGraphicsWidget):
    """Enhanced tooltip showing detailed person information."""

    closed: Signal = Signal()
    manually_moved: Signal = Signal()
    navigate_to_person: Signal = Signal(int)  # person_id to jump to

    PANEL_WIDTH: int = 320
    PANEL_HEIGHT: int = 650
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
    INDENT_LEVEL_4: int = 40

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
    COLOR_LINK: QColor = QColor(30, 90, 200)
    COLOR_LINK_HOVER: QColor = QColor(60, 120, 255)
    COLOR_LINK_VISITED: QColor = QColor(120, 60, 180)
    COLOR_CLOSE_BUTTON: QColor = QColor(200, 0, 0)
    COLOR_CLOSE_BUTTON_IDLE: QColor = QColor(150, 150, 150)
    COLOR_SEPARATOR: QColor = QColor(220, 220, 220)
    COLOR_LOCK_FILL: QColor = QColor(100, 100, 255)
    COLOR_LOCK_INDICATOR: QColor = QColor(100, 100, 255, 100)
    COLOR_LOCK_ICON_INACTIVE: QColor = QColor(80, 80, 80)

    # Session-level set of person IDs that have been navigated to.
    _visited_person_ids: set[int] = set()

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
        self._ancestors: dict = {}

        self._load_person_data()
        self._load_events()
        self.relationships = self._load_relationships()
        self._ancestors = self._load_ancestors()

        self.setMinimumSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)
        self.setMaximumSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)

        self._close_button_hovered: bool = False
        self._is_being_dragged: bool = False
        self._drag_start_pos: QPoint | None = None
        self.is_hovered: bool = False
        self.is_locked: bool = False
        self.parent_person_box: 'PersonBox | None' = None

        # Collapsible sections: both ancestors and descendants start collapsed.
        self._collapsed_sections: dict[str, bool] = {
            'ancestors': True,
            'descendants': True,
        }
        # Per-person collapse state for tree sub-nodes (keyed by person_id).
        self._collapsed_people: dict[int, bool] = {}

        self._clickable_rects: list[tuple[QRectF, int]] = []  # (rect, person_id)
        self._section_click_rects: dict[str, QRectF] = {}
        self._person_toggle_rects: dict[int, QRectF] = {}
        self._hovered_link_id: int | None = None

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
        if not self.db or not self.db.conn or not self.person:
            return {}
        cursor = self.db.conn.cursor()
        siblings: dict[str, list[dict]] = {
            'brothers': [], 'sisters': [], 'other': [],
            'half_brothers': [], 'half_sisters': [], 'half_other': []
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
                shares_father: bool = sibling['father_id'] == self.person.father_id and self.person.father_id is not None
                shares_mother: bool = sibling['mother_id'] == self.person.mother_id and self.person.mother_id is not None
                is_full: bool = shares_father and shares_mother
                prefix: str = '' if is_full else 'half_'
                gender: str = sibling['gender']
                if gender == 'Male':
                    siblings[f'{prefix}brothers'].append(sibling)
                elif gender == 'Female':
                    siblings[f'{prefix}sisters'].append(sibling)
                else:
                    siblings[f'{prefix}other'].append(sibling)

        descendants: dict = self._load_descendant_tree()

        return {'siblings': siblings, 'descendants': descendants}

    # ========================================
    # Descendant Tree (per-child sub-tree)
    # ========================================

    def _load_descendant_tree(self) -> list[dict]:
        """Load children, each with their own sub-tree of grandchildren etc."""
        if not self.db or not self.db.conn:
            return []
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT id, first_name, last_name, birth_year, death_year, gender
            FROM Person
            WHERE father_id = ? OR mother_id = ?
            ORDER BY birth_year
        """, (self.person_id, self.person_id))

        children: list[dict] = []
        for row in cursor.fetchall():
            child = dict(row)
            child['children'] = self._load_subtree(child['id'], depth=1, max_depth=4)
            children.append(child)
        return children

    def _load_subtree(self, parent_id: int, depth: int, max_depth: int) -> list[dict]:
        if depth >= max_depth or not self.db or not self.db.conn:
            return []
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT id, first_name, last_name, birth_year, death_year, gender
            FROM Person
            WHERE father_id = ? OR mother_id = ?
            ORDER BY birth_year
        """, (parent_id, parent_id))
        result: list[dict] = []
        for row in cursor.fetchall():
            person = dict(row)
            person['children'] = self._load_subtree(person['id'], depth + 1, max_depth)
            result.append(person)
        return result

    # ========================================
    # Ancestor Tree
    # ========================================

    def _load_ancestors(self) -> dict:
        """Load parent → grandparent → etc. tree structure."""
        if not self.person:
            return {}
        return {
            'father': self._load_ancestor_branch(self.person.father_id, depth=0, max_depth=4),
            'mother': self._load_ancestor_branch(self.person.mother_id, depth=0, max_depth=4),
        }

    def _load_ancestor_branch(self, person_id: int | None, depth: int, max_depth: int) -> dict | None:
        if person_id is None or depth >= max_depth or not self.db or not self.db.conn:
            return None
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT id, first_name, last_name, birth_year, death_year, gender, father_id, mother_id
            FROM Person WHERE id = ?
        """, (person_id,))
        row = cursor.fetchone()
        if not row:
            return None
        person = dict(row)
        person['father'] = self._load_ancestor_branch(person.get('father_id'), depth + 1, max_depth)
        person['mother'] = self._load_ancestor_branch(person.get('mother_id'), depth + 1, max_depth)
        return person

    # ========================================
    # Helper Methods
    # ========================================

    def _get_close_button_rect(self) -> QRectF:
        close_x: float = self.PANEL_WIDTH - self.CLOSE_BUTTON_X_OFFSET
        close_y: float = self.CLOSE_BUTTON_Y_OFFSET
        return QRectF(close_x, close_y, self.CLOSE_BUTTON_SIZE, self.CLOSE_BUTTON_SIZE)

    def _get_lock_icon_rect(self) -> QRectF:
        indicator_x: float = self.PANEL_WIDTH - self.LOCK_INDICATOR_X_OFFSET
        indicator_y: float = self.LOCK_ICON_OFFSET_Y
        return QRectF(indicator_x - 5, indicator_y, self.LOCK_ICON_CLICKABLE_SIZE, 20)

    def _get_gender_symbol(self, gender: str) -> str:
        return {"Male": "♂", "Female": "♀"}.get(gender, "⚲")

    def _format_single_date(self, year, month=None, day=None) -> str:
        if year is None:
            return "?"
        from utils.date_formatter import DateFormatter, DateParts, MonthStyle
        dp = DateParts(year=year, month=month, day=day)
        return DateFormatter.format_display(dp, separator=" ", month_style=MonthStyle.ABBREVIATED)

    def _format_years(self, birth_year, death_year) -> str:
        b = f"b. {birth_year}" if birth_year else "b. ?"
        if death_year:
            return f"({b} - d. {death_year})"
        return f"({b})"

    def _start_lock_timer(self) -> None:
        if not self.is_locked:
            self._hover_timer.start(self.HOVER_LOCK_DURATION)
            self._animation_timer.start()

    def _on_hover_lock(self) -> None:
        self.is_locked = True
        self._animation_timer.stop()
        self.update()

    def _check_self_hide(self) -> None:
        if not self.is_hovered and not self.is_locked and self.scene():
            self.scene().removeItem(self)
            self.closed.emit()

    def _draw_section_header(self, painter: QPainter, y: float, section_font: QFont, text: str) -> float:
        painter.setFont(section_font)
        painter.setPen(QPen(self.COLOR_TEXT))
        painter.drawText(self.PADDING, int(y), text)
        return y + self.SECTION_HEADER_SPACING

    def _draw_separator_line(self, painter: QPainter, y: float) -> float:
        painter.setPen(QPen(self.COLOR_SEPARATOR, 1))
        painter.drawLine(self.PADDING, int(y), self.PANEL_WIDTH - self.PADDING, int(y))
        return y + self.SEPARATOR_BOTTOM_SPACING

    # ========================================
    # Link Drawing Helper
    # ========================================

    def _draw_person_link(self, painter: QPainter, x: float, y: float, person: dict, font: QFont) -> float:
        """Draw a clickable underlined person name. Returns new y after drawing."""
        pid: int = person['id']
        name: str = f"{person['first_name']} {person['last_name']}"
        symbol: str = self._get_gender_symbol(person.get('gender', 'Unknown'))
        full_text = f"{name} {symbol}"

        painter.setFont(font)
        fm = QFontMetrics(font)
        text_w = fm.horizontalAdvance(full_text)

        is_hovered = (self._hovered_link_id == pid)
        is_visited = pid in EnhancedTooltipPanel._visited_person_ids
        if is_hovered:
            color = self.COLOR_LINK_HOVER
        elif is_visited:
            color = self.COLOR_LINK_VISITED
        else:
            color = self.COLOR_LINK

        painter.setPen(QPen(color))
        painter.drawText(int(x), int(y), full_text)

        # Underline.
        underline_y = y + 2
        painter.drawLine(int(x), int(underline_y), int(x + text_w), int(underline_y))

        # Register clickable area.
        click_rect = QRectF(x, y - fm.ascent(), text_w, fm.height())
        self._clickable_rects.append((click_rect, pid))

        return y + self.LINE_SPACING

    # ========================================
    # Painting
    # ========================================

    def paint(self, painter: QPainter, option, widget=None) -> None:
        if not self.person:
            return
        # Reset interactive rects each paint cycle.
        self._clickable_rects.clear()
        self._section_click_rects.clear()
        self._person_toggle_rects.clear()

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QPen(self.COLOR_BORDER, 2))
        painter.setBrush(QBrush(self.COLOR_BG))
        painter.drawRoundedRect(QRectF(0, 0, self.PANEL_WIDTH, self.PANEL_HEIGHT), self.CORNER_RADIUS, self.CORNER_RADIUS)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.COLOR_HEADER_BG))
        painter.drawRoundedRect(QRectF(0, 0, self.PANEL_WIDTH, self.HEADER_HEIGHT), self.CORNER_RADIUS, self.CORNER_RADIUS)
        painter.drawRect(QRectF(0, self.HEADER_PARTIAL_HEIGHT, self.PANEL_WIDTH, self.HEADER_PARTIAL_HEIGHT))

        self._draw_lock_indicator(painter)
        self._draw_close_button(painter)
        self._draw_header(painter)
        self._draw_content(painter)

    def _draw_lock_indicator(self, painter: QPainter) -> None:
        ix: float = self.PANEL_WIDTH - self.LOCK_INDICATOR_X_OFFSET
        iy: float = self.LOCK_INDICATOR_Y_OFFSET
        cx: float = ix + self.LOCK_INDICATOR_SIZE / 2
        cy: float = iy + self.LOCK_INDICATOR_SIZE / 2
        if self._hover_timer.isActive():
            elapsed = self._hover_timer.interval() - self._hover_timer.remainingTime()
            fill_pct = min(1.0, elapsed / self.HOVER_LOCK_DURATION)
            painter.setPen(QPen(self.COLOR_LOCK_INDICATOR, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(int(ix), int(iy), self.LOCK_INDICATOR_SIZE, self.LOCK_INDICATOR_SIZE)
            if fill_pct > 0:
                painter.setBrush(QBrush(self.COLOR_LOCK_FILL))
                painter.drawPie(int(ix), int(iy), self.LOCK_INDICATOR_SIZE, self.LOCK_INDICATOR_SIZE, self.PIE_START_ANGLE, int(-self.PIE_FULL_CIRCLE * fill_pct))
        painter.setFont(self._font_icon_small)
        if self.is_locked:
            painter.setPen(QPen(self.COLOR_LOCK_FILL))
            painter.drawText(int(cx - self.LOCK_ICON_OFFSET_X), int(cy + self.LOCK_ICON_OFFSET_Y), "🔒")
        else:
            painter.setPen(QPen(self.COLOR_LOCK_ICON_INACTIVE))
            painter.drawText(int(cx - self.LOCK_ICON_OFFSET_X), int(cy + self.LOCK_ICON_OFFSET_Y), "🔓")

    def _draw_close_button(self, painter: QPainter) -> None:
        cx: float = self.PANEL_WIDTH - self.CLOSE_BUTTON_X_OFFSET
        cy: float = self.CLOSE_BUTTON_Y_OFFSET
        color = self.COLOR_CLOSE_BUTTON if self._close_button_hovered else self.COLOR_CLOSE_BUTTON_IDLE
        painter.setPen(QPen(color, 2))
        painter.drawLine(int(cx), int(cy), int(cx + self.CLOSE_BUTTON_LINE_LENGTH), int(cy + self.CLOSE_BUTTON_LINE_LENGTH))
        painter.drawLine(int(cx + self.CLOSE_BUTTON_LINE_LENGTH), int(cy), int(cx), int(cy + self.CLOSE_BUTTON_LINE_LENGTH))

    def _draw_header(self, painter: QPainter) -> None:
        if not self.person:
            return
        painter.setPen(QPen(self.COLOR_TEXT))
        painter.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        painter.drawText(QRectF(self.PADDING, self.HEADER_TEXT_Y_OFFSET, self.PANEL_WIDTH - self.HEADER_RIGHT_MARGIN, self.HEADER_TEXT_HEIGHT), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.person.full_name)

    def _draw_content(self, painter: QPainter) -> None:
        y: float = self.INITIAL_CONTENT_Y
        normal_font = QFont("Segoe UI", 9)
        section_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        link_font = QFont("Segoe UI", 9)
        link_font.setUnderline(False)  # We draw underline manually.

        for method in [self._draw_statistics, self._draw_ancestors, self._draw_relationships, self._draw_descendants, self._draw_events]:
            y = method(painter, y, section_font, normal_font)

    # ========================================
    # Statistics
    # ========================================

    def _draw_statistics(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        if not self.person:
            return y
        y = self._draw_section_header(painter, y, section_font, "Statistics")
        painter.setFont(normal_font)
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        stats = [
            f"Birth: {self._format_single_date(self.person.birth_year, self.person.birth_month, self.person.birth_day)}",
            f"Death: {self._format_single_date(self.person.death_year, self.person.death_month, self.person.death_day)}" if self.person.is_deceased else "Status: Living",
            f"Age: {self.person.get_age(self.current_year) or 'Unknown'}",
        ]
        for stat in stats:
            painter.drawText(self.PADDING, int(y), stat)
            y += self.LINE_SPACING
        return y + self.SECTION_BOTTOM_SPACING

    # ========================================
    # Ancestors
    # ========================================

    def _draw_ancestors(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        father = self._ancestors.get('father')
        mother = self._ancestors.get('mother')
        if not father and not mother:
            return y

        collapsed = self._collapsed_sections.get('ancestors', True)
        arrow = "▶" if collapsed else "▼"
        painter.setFont(section_font)
        painter.setPen(QPen(self.COLOR_TEXT))
        header_text = f"Ancestors {arrow}"
        painter.drawText(self.PADDING, int(y), header_text)
        fm = QFontMetrics(section_font)
        header_rect = QRectF(self.PADDING, y - fm.ascent(), fm.horizontalAdvance(header_text), fm.height())
        self._section_click_rects['ancestors'] = header_rect
        y += self.SECTION_HEADER_SPACING

        if collapsed:
            y = self._draw_separator_line(painter, y)
            return y

        link_font = QFont("Segoe UI", 9)
        max_y = self.PANEL_HEIGHT - 100

        if father:
            y = self._draw_ancestor_node(painter, y, father, "Father", self.INDENT_LEVEL_1, link_font, normal_font, max_y)
        if mother:
            y = self._draw_ancestor_node(painter, y, mother, "Mother", self.INDENT_LEVEL_1, link_font, normal_font, max_y)

        y += self.SECTION_BOTTOM_SPACING
        y = self._draw_separator_line(painter, y)
        return y

    def _draw_ancestor_node(self, painter, y, ancestor, label, indent, link_font, normal_font, max_y) -> float:
        if y > max_y or ancestor is None:
            return y
        pid = ancestor['id']
        collapsed = self._collapsed_people.get(pid, True)
        has_parents = ancestor.get('father') is not None or ancestor.get('mother') is not None
        arrow = ""
        if has_parents:
            arrow = "▶ " if collapsed else "▼ "

        # Draw label (e.g. "Father:")
        painter.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        painter.drawText(self.PADDING + indent, int(y), f"{arrow}{label}:")
        y += self.LINE_SPACING_SMALL

        # Draw clickable name.
        y = self._draw_person_link(painter, self.PADDING + indent + 10, y, ancestor, link_font)

        if has_parents:
            toggle_rect = QRectF(self.PADDING + indent, y - self.LINE_SPACING * 2, 200, self.LINE_SPACING * 2)
            self._person_toggle_rects[pid] = toggle_rect

        if not collapsed and has_parents:
            if ancestor.get('father'):
                y = self._draw_ancestor_node(painter, y, ancestor['father'], "Grandfather" if label.startswith("F") else "Grandfather (maternal)", indent + 15, link_font, normal_font, max_y)
            if ancestor.get('mother'):
                y = self._draw_ancestor_node(painter, y, ancestor['mother'], "Grandmother" if label.startswith("F") else "Grandmother (maternal)", indent + 15, link_font, normal_font, max_y)

        return y

    # ========================================
    # Relationships (siblings)
    # ========================================

    def _draw_relationships(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        y = self._draw_section_header(painter, y, section_font, "Relationships")
        painter.setFont(normal_font)
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        siblings = self.relationships.get('siblings', {})
        types = [('brothers', 'Brothers'), ('half_brothers', 'Half-Brothers'), ('sisters', 'Sisters'), ('half_sisters', 'Half-Sisters'), ('other', 'Other Siblings'), ('half_other', 'Half-Siblings (Other)')]
        link_font = QFont("Segoe UI", 9)
        for key, label in types:
            sib_list = siblings.get(key, [])
            if sib_list:
                painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                painter.setPen(QPen(self.COLOR_TEXT))
                painter.drawText(self.PADDING, int(y), f"{label}:")
                y += self.LINE_SPACING_SMALL
                for sib in sib_list[:self.SIBLING_DISPLAY_COUNT]:
                    y = self._draw_person_link(painter, self.PADDING + self.INDENT_LEVEL_1, y, sib, link_font)
                overflow = len(sib_list) - self.SIBLING_DISPLAY_COUNT
                if overflow > 0:
                    painter.setFont(normal_font)
                    painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
                    painter.drawText(self.PADDING + self.INDENT_LEVEL_2, int(y), f"...and {overflow} more")
                    y += self.LINE_SPACING
        y += self.SECTION_BOTTOM_SPACING
        y = self._draw_separator_line(painter, y)
        return y

    # ========================================
    # Descendants (tree-structured)
    # ========================================

    def _draw_descendants(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        children = self.relationships.get('descendants', [])
        if not children:
            return y

        collapsed = self._collapsed_sections.get('descendants', True)
        arrow = "▶" if collapsed else "▼"
        painter.setFont(section_font)
        painter.setPen(QPen(self.COLOR_TEXT))
        header_text = f"Descendants ({self._count_all_descendants(children)}) {arrow}"
        painter.drawText(self.PADDING, int(y), header_text)
        fm = QFontMetrics(section_font)
        self._section_click_rects['descendants'] = QRectF(self.PADDING, y - fm.ascent(), fm.horizontalAdvance(header_text), fm.height())
        y += self.SECTION_HEADER_SPACING

        if collapsed:
            y = self._draw_separator_line(painter, y)
            return y

        link_font = QFont("Segoe UI", 9)
        max_y = self.PANEL_HEIGHT - self.DESCENDANTS_MAX_Y_OFFSET

        for child in children:
            if y > max_y:
                painter.setFont(normal_font)
                painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
                painter.drawText(self.PADDING + self.INDENT_LEVEL_1, int(y), "...")
                break
            y = self._draw_descendant_node(painter, y, child, self.INDENT_LEVEL_1, link_font, normal_font, max_y)

        y += self.SECTION_BOTTOM_SPACING
        y = self._draw_separator_line(painter, y)
        return y

    def _draw_descendant_node(self, painter, y, person, indent, link_font, normal_font, max_y) -> float:
        if y > max_y:
            return y
        pid = person['id']
        has_children = bool(person.get('children'))
        collapsed = self._collapsed_people.get(pid, True)

        arrow = ""
        if has_children:
            arrow = "▶ " if collapsed else "▼ "

        # Draw arrow + person link.
        if arrow:
            painter.setFont(QFont("Segoe UI", 8))
            painter.setPen(QPen(self.COLOR_TEXT))
            painter.drawText(self.PADDING + indent, int(y), arrow)

        y = self._draw_person_link(painter, self.PADDING + indent + (15 if arrow else 0), y, person, link_font)

        # Dates below.
        painter.setFont(QFont("Segoe UI", 8))
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        date_text = self._format_years(person.get('birth_year'), person.get('death_year'))
        painter.drawText(self.PADDING + indent + 15, int(y), date_text)
        y += self.LINE_SPACING_SMALL

        if has_children:
            toggle_rect = QRectF(self.PADDING + indent, y - self.LINE_SPACING * 2.5, 250, self.LINE_SPACING * 2.5)
            self._person_toggle_rects[pid] = toggle_rect

        if not collapsed and has_children:
            for grandchild in person['children']:
                if y > max_y:
                    break
                y = self._draw_descendant_node(painter, y, grandchild, indent + 15, link_font, normal_font, max_y)

        return y

    def _count_all_descendants(self, children: list[dict]) -> int:
        count = len(children)
        for child in children:
            count += self._count_all_descendants(child.get('children', []))
        return count

    # ========================================
    # Events
    # ========================================

    def _draw_events(self, painter: QPainter, y: float, section_font: QFont, normal_font: QFont) -> float:
        y = self._draw_section_header(painter, y, section_font, f"Life Events ({len(self.events)})")
        painter.setFont(normal_font)
        painter.setPen(QPen(self.COLOR_TEXT_LIGHT))
        max_y = self.PANEL_HEIGHT - self.PADDING
        count = 0
        for event in self.events:
            if y > max_y - self.EVENTS_MAX_Y_OFFSET:
                remaining = len(self.events) - count
                painter.drawText(self.PADDING, int(y), f"...and {remaining} more")
                break
            event_dict: dict = dict(event)
            event_year = str(event_dict.get('start_year', '?'))
            event_title = event_dict.get('event_title', event_dict.get('event_name', 'Unknown'))
            event_type = event_dict.get('event_type', '')
            painter.drawText(self.PADDING, int(y), f"{event_year}: {event_title}")
            y += self.LINE_SPACING_SMALL
            if event_type:
                painter.drawText(self.PADDING + self.EVENT_TYPE_INDENT, int(y), f"({event_type})")
                y += self.LINE_SPACING_SMALL
            count += 1
            y += self.LINE_SPACING_TINY
        return y

    # ========================================
    # Qt Event Handlers
    # ========================================

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.PANEL_WIDTH, self.PANEL_HEIGHT)

    def hoverEnterEvent(self, event) -> None:
        self.is_hovered = True
        self._lock_delay_timer.start(self.LOCK_START_DELAY)
        super().hoverEnterEvent(event)

    def hoverMoveEvent(self, event) -> None:
        mouse = event.pos()
        self._close_button_hovered = self._get_close_button_rect().contains(mouse)

        # Check link hover for cursor change.
        old_hovered = self._hovered_link_id
        self._hovered_link_id = None
        for rect, pid in self._clickable_rects:
            if rect.contains(mouse):
                self._hovered_link_id = pid
                break

        any_interactive = self._close_button_hovered or self._hovered_link_id is not None
        if not any_interactive:
            for rect in self._section_click_rects.values():
                if rect.contains(mouse):
                    any_interactive = True
                    break
        if not any_interactive:
            for rect in self._person_toggle_rects.values():
                if rect.contains(mouse):
                    any_interactive = True
                    break
        if not any_interactive:
            if self._get_lock_icon_rect().contains(mouse):
                any_interactive = True

        if self._hovered_link_id is not None:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        elif any_interactive:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if old_hovered != self._hovered_link_id:
            self.update()
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.is_hovered = False
        self._hovered_link_id = None
        self._lock_delay_timer.stop()
        self._hover_timer.stop()
        self._animation_timer.stop()
        if not self.is_locked:
            QTimer.singleShot(self.HOVER_HIDE_DELAY, self._check_self_hide)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return

        pos = event.pos()

        # Close button.
        if self._get_close_button_rect().contains(pos):
            self.closed.emit()
            if self.scene():
                self.scene().removeItem(self)
            return

        # Lock icon.
        if self._get_lock_icon_rect().contains(pos):
            self.is_locked = not self.is_locked
            if self.is_locked:
                self._lock_delay_timer.stop()
                self._hover_timer.stop()
                self._animation_timer.stop()
            self.update()
            return

        # Section collapse toggles.
        for key, rect in self._section_click_rects.items():
            if rect.contains(pos):
                self._collapsed_sections[key] = not self._collapsed_sections.get(key, True)
                self.update()
                return

        # Per-person tree toggles.
        for pid, rect in self._person_toggle_rects.items():
            if rect.contains(pos):
                self._collapsed_people[pid] = not self._collapsed_people.get(pid, True)
                self.update()
                return

        # Clickable name links.
        for rect, pid in self._clickable_rects:
            if rect.contains(pos):
                EnhancedTooltipPanel._visited_person_ids.add(pid)
                self.navigate_to_person.emit(pid)
                return

        # Start drag.
        self._is_being_dragged = True
        self._drag_start_pos = pos
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._is_being_dragged:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self._is_being_dragged:
            self.manually_moved.emit()
            self._is_being_dragged = False
        super().mouseReleaseEvent(event)
