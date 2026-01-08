"""Custom date picker widget supporting flexible precision."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QSpinBox, QLabel, QCheckBox
)
from PySide6.QtCore import Signal

from utils.date_formatter import DateFormatter

if TYPE_CHECKING:
    pass


class MonthSpinBox(QSpinBox):
    """Custom spinbox that displays month names instead of just numbers."""
    
    yearAdjustNeeded: Signal = Signal(int)
    
    MONTH_MIN: int = 1
    MONTH_MAX: int = 12
    MONTH_JANUARY_NUM: int = 1
    MONTH_DECEMBER_NUM: int = 12
    DEFAULT_MONTH: int = 1
    
    DISPLAY_FORMAT: str = "{name} ({num})"
    TEXT_SEPARATOR_OPEN: str = "("
    TEXT_SEPARATOR_CLOSE: str = ")"
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize month spinbox."""
        super().__init__(parent)
        self.setWrapping(True)
    
    def textFromValue(self, value: int) -> str:
        """Convert internal value (1-12) to display text."""
        if not (self.MONTH_MIN <= value <= self.MONTH_MAX):
            return str(value)
        
        month_name: str | None = DateFormatter.MONTHS_FULL.get(value)
        if month_name is None:
            return str(value)
        
        return self.DISPLAY_FORMAT.format(name=month_name, num=value)
    
    def valueFromText(self, text: str) -> int:
        """Convert display text back to internal value (1-12)."""
        value: int | None = self._extract_number_from_text(text)
        if value is not None:
            return value
        
        value = self._match_month_name(text)
        if value is not None:
            return value
        
        value = self._parse_as_integer(text)
        return value if value is not None else self.DEFAULT_MONTH
    
    def _extract_number_from_text(self, text: str) -> int | None:
        """Extract month number from formatted text like 'January (1)'."""
        if self.TEXT_SEPARATOR_OPEN not in text or self.TEXT_SEPARATOR_CLOSE not in text:
            return None
        
        try:
            number_part: str = text.split(self.TEXT_SEPARATOR_OPEN)[1].split(self.TEXT_SEPARATOR_CLOSE)[0]
            return int(number_part)
        except (ValueError, IndexError):
            return None
    
    def _match_month_name(self, text: str) -> int | None:
        """Match text against month names using DateFormatter."""
        return DateFormatter.month_name_to_int(text.strip())
    
    def _parse_as_integer(self, text: str) -> int | None:
        """Try to parse text as integer."""
        try:
            return int(text)
        except ValueError:
            return None
    
    def stepBy(self, steps: int) -> None:
        """Override step behavior to handle year adjustment on wrap."""
        old_value: int = self.value()
        super().stepBy(steps)
        new_value: int = self.value()
        
        if self._wrapped_forward(old_value, new_value, steps):
            self.yearAdjustNeeded.emit(1)
        elif self._wrapped_backward(old_value, new_value, steps):
            self.yearAdjustNeeded.emit(-1)
    
    def _wrapped_forward(self, old_value: int, new_value: int, steps: int) -> bool:
        """Check if month wrapped forward from December to January."""
        return steps > 0 and old_value == self.MONTH_DECEMBER_NUM and new_value == self.MONTH_JANUARY_NUM
    
    def _wrapped_backward(self, old_value: int, new_value: int, steps: int) -> bool:
        """Check if month wrapped backward from January to December."""
        return steps < 0 and old_value == self.MONTH_JANUARY_NUM and new_value == self.MONTH_DECEMBER_NUM


class DatePicker(QWidget):
    """Widget for entering dates with flexible precision (Year + Month)."""
    
    dateChanged: Signal = Signal()
    
    LABEL_YEAR: str = "Year"
    LABEL_MONTH: str = "Month"
    CHECKBOX_UNKNOWN: str = "Unknown"
    
    YEAR_MIN_DEFAULT: int = 1500
    YEAR_MAX_DEFAULT: int = 2000
    YEAR_DEFAULT: int = 1721
    
    MONTH_MIN: int = 1
    MONTH_MAX: int = 12
    MONTH_DEFAULT: int = 1
    
    LAYOUT_MARGIN: int = 0
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the date picker widget."""
        super().__init__(parent)
        
        self.min_year: int | None = None
        self.min_month: int | None = None
        
        self._setup_ui()
        self._update_month_state()
    
    def _setup_ui(self) -> None:
        """Create the date picker layout."""
        main_layout: QHBoxLayout = QHBoxLayout(self)
        main_layout.setContentsMargins(self.LAYOUT_MARGIN, self.LAYOUT_MARGIN, self.LAYOUT_MARGIN, self.LAYOUT_MARGIN)
        
        year_layout: QVBoxLayout = self._create_year_section()
        month_layout: QVBoxLayout = self._create_month_section()
        
        main_layout.addLayout(year_layout)
        main_layout.addLayout(month_layout)
        main_layout.addStretch()
    
    def _create_year_section(self) -> QVBoxLayout:
        """Create year input section."""
        year_layout: QVBoxLayout = QVBoxLayout()
        
        year_label: QLabel = QLabel(self.LABEL_YEAR, self)
        
        self.year_spin: QSpinBox = QSpinBox(self)
        self.year_spin.setRange(self.YEAR_MIN_DEFAULT, self.YEAR_MAX_DEFAULT)
        self.year_spin.setValue(self.YEAR_DEFAULT)
        self.year_spin.valueChanged.connect(self._on_date_changed)
        
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_spin)
        
        return year_layout
    
    def _create_month_section(self) -> QVBoxLayout:
        """Create month input section with unknown checkbox."""
        month_layout: QVBoxLayout = QVBoxLayout()
        
        month_label: QLabel = QLabel(self.LABEL_MONTH, self)
        month_controls: QHBoxLayout = self._create_month_controls()
        
        month_layout.addWidget(month_label)
        month_layout.addLayout(month_controls)
        
        return month_layout
    
    def _create_month_controls(self) -> QHBoxLayout:
        """Create month spinbox and unknown checkbox."""
        month_controls: QHBoxLayout = QHBoxLayout()
        
        self.month_spin: MonthSpinBox = MonthSpinBox(self)
        self.month_spin.setRange(self.MONTH_MIN, self.MONTH_MAX)
        self.month_spin.setValue(self.MONTH_DEFAULT)
        self.month_spin.valueChanged.connect(self._on_date_changed)
        self.month_spin.yearAdjustNeeded.connect(self._on_year_adjust)
        
        self.unknown_check: QCheckBox = QCheckBox(self.CHECKBOX_UNKNOWN, self)
        self.unknown_check.setChecked(False)
        self.unknown_check.stateChanged.connect(self._on_unknown_toggled)
        
        month_controls.addWidget(self.month_spin)
        month_controls.addWidget(self.unknown_check)
        
        return month_controls
    
    def set_min_date(self, min_year: int, min_month: int | None = None) -> None:
        """Set minimum allowable date."""
        self.min_year = min_year
        self.min_month = min_month if min_month else self.MONTH_MIN
        
        if self.min_year:
            self.year_spin.setMinimum(self.min_year)
    
    def _on_year_adjust(self, direction: int) -> None:
        """Adjust year when month wraps around."""
        current_year: int = self.year_spin.value()
        new_year: int = current_year + direction
        
        if self.year_spin.minimum() <= new_year <= self.year_spin.maximum():
            self.year_spin.setValue(new_year)
    
    def _on_unknown_toggled(self) -> None:
        """Handle unknown checkbox state change."""
        self._update_month_state()
        self._on_date_changed()
    
    def _update_month_state(self) -> None:
        """Enable or disable month spinbox based on unknown checkbox."""
        is_unknown: bool = self.unknown_check.isChecked()
        self.month_spin.setEnabled(not is_unknown)
    
    def _on_date_changed(self) -> None:
        """Internal handler when date changes - emits signal."""
        self.dateChanged.emit()
    
    def get_date(self) -> tuple[int, int | None]:
        """Get the selected date as (year, month) tuple."""
        year: int = self.year_spin.value()
        
        if self.unknown_check.isChecked():
            return (year, None)
        
        return (year, self.month_spin.value())
    
    def set_date(self, year: int, month: int | str | None = None) -> None:
        """Set the date to specific values."""
        self.year_spin.setValue(year)
        
        if month is None or month == "":
            self.unknown_check.setChecked(True)
            self._update_month_state()
            return
        
        self.unknown_check.setChecked(False)
        
        if isinstance(month, str):
            self._set_month_from_string(month)
        else:
            self.month_spin.setValue(int(month))
        
        self._update_month_state()
    
    def _set_month_from_string(self, month_name: str) -> None:
        """Set month value from string name."""
        month_num: int | None = DateFormatter.month_name_to_int(month_name)
        
        if month_num is not None:
            self.month_spin.setValue(month_num)
        else:
            self.unknown_check.setChecked(True)
    
    def clear(self) -> None:
        """Reset to default values (1721, Unknown)."""
        self.set_date(self.YEAR_DEFAULT, None)