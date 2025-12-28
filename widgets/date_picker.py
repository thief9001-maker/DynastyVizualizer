"""Custom date picker widget supporting flexible precision."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QSpinBox, QLabel, QCheckBox
)
from PySide6.QtCore import Signal


class MonthSpinBox(QSpinBox):
    """Custom spinbox that displays month names instead of just numbers."""
    
    yearAdjustNeeded = Signal(int)
    
    MONTH_NAMES = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    def __init__(self, parent=None):
        """Initialize month spinbox."""
        super().__init__(parent)
        self.setWrapping(True)
    
    def textFromValue(self, value: int) -> str:
        """Convert internal value (1-12) to display text."""
        if 1 <= value <= 12:
            return f"{self.MONTH_NAMES[value - 1]} ({value})"
        return str(value)
    
    def valueFromText(self, text: str) -> int:
        """Convert display text back to internal value (1-12)."""
        if "(" in text and ")" in text:
            try:
                return int(text.split("(")[1].split(")")[0])
            except (ValueError, IndexError):
                pass
        
        text_lower = text.lower().strip()
        for i, month in enumerate(self.MONTH_NAMES, start=1):
            if month.lower().startswith(text_lower):
                return i
        
        try:
            return int(text)
        except ValueError:
            return 1
    
    def stepBy(self, steps: int) -> None:
        """Override step behavior to handle year adjustment on wrap."""
        old_value = self.value()
        super().stepBy(steps)
        new_value = self.value()
        
        if steps > 0 and old_value == 12 and new_value == 1:
            self.yearAdjustNeeded.emit(1)
        elif steps < 0 and old_value == 1 and new_value == 12:
            self.yearAdjustNeeded.emit(-1)


class DatePicker(QWidget):
    """Widget for entering dates with flexible precision (Year + Month)."""
    
    dateChanged = Signal()
    
    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the date picker widget."""
        super().__init__(parent)
        
        self.min_year: int | None = None
        self.min_month: int | None = None
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Year Section
        year_layout = QVBoxLayout()
        year_label = QLabel("Year", self)
        self.year_spin = QSpinBox(self)
        self.year_spin.setRange(1500, 2000)
        self.year_spin.setValue(1721)
        self.year_spin.valueChanged.connect(self._on_date_changed)
        
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_spin)
        
        # Month Section
        month_layout = QVBoxLayout()
        month_label = QLabel("Month", self)
        
        month_controls = QHBoxLayout()
        self.month_spin = MonthSpinBox(self)
        self.month_spin.setRange(1, 12)
        self.month_spin.setValue(1)
        self.month_spin.valueChanged.connect(self._on_date_changed)
        self.month_spin.yearAdjustNeeded.connect(self._on_year_adjust)
        
        self.unknown_check = QCheckBox("Unknown", self)
        self.unknown_check.setChecked(False)
        self.unknown_check.stateChanged.connect(self._on_unknown_toggled)
        
        month_controls.addWidget(self.month_spin)
        month_controls.addWidget(self.unknown_check)
        
        month_layout.addWidget(month_label)
        month_layout.addLayout(month_controls)
        
        main_layout.addLayout(year_layout)
        main_layout.addLayout(month_layout)
        main_layout.addStretch()
        
        self._update_month_state()
    
    def set_min_date(self, min_year: int, min_month: int | None = None) -> None:
        """Set minimum allowable date."""
        self.min_year = min_year
        self.min_month = min_month if min_month else 1
        
        if self.min_year:
            self.year_spin.setMinimum(self.min_year)
    
    def _on_year_adjust(self, direction: int) -> None:
        """Adjust year when month wraps around."""
        current_year = self.year_spin.value()
        new_year = current_year + direction
        
        if self.year_spin.minimum() <= new_year <= self.year_spin.maximum():
            self.year_spin.setValue(new_year)
    
    def _on_unknown_toggled(self) -> None:
        """Handle unknown checkbox state change."""
        self._update_month_state()
        self._on_date_changed()
    
    def _update_month_state(self) -> None:
        """Enable or disable month spinbox based on unknown checkbox."""
        is_unknown = self.unknown_check.isChecked()
        self.month_spin.setEnabled(not is_unknown)
    
    def _on_date_changed(self) -> None:
        """Internal handler when date changes - emits signal."""
        self.dateChanged.emit()
    
    def get_date(self) -> tuple[int, int | None]:
        """Get the selected date as (year, month) tuple."""
        year = self.year_spin.value()
        
        if self.unknown_check.isChecked():
            return (year, None)
        else:
            return (year, self.month_spin.value())
    
    def set_date(self, year: int, month: int | str | None = None) -> None:
        """Set the date to specific values."""
        self.year_spin.setValue(year)
        
        if month is None or month == "":
            self.unknown_check.setChecked(True)
        else:
            self.unknown_check.setChecked(False)
            
            if isinstance(month, str):
                month_num = self._month_name_to_number(month)
                if month_num is not None:
                    self.month_spin.setValue(month_num)
                else:
                    self.unknown_check.setChecked(True)
            else:
                self.month_spin.setValue(int(month))
        
        self._update_month_state()

    def _month_name_to_number(self, month_name: str) -> int | None:
        """Convert month name to number (1-12)."""
        month_map = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        return month_map.get(month_name.lower())
    
    def clear(self) -> None:
        """Reset to default values (1721, Unknown)."""
        self.set_date(1721, None)