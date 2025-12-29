"""Dialog implementations for user interactions."""

from .add_person_dialog import AddPersonDialog
from .end_marriage_dialog import EndMarriageDialog
from .create_marriage_dialog import CreateMarriageDialog
from .create_child_dialog import CreateChildDialog
from .create_event_dialog import CreateEventDialog
from .edit_event_dialog import EditEventDialog

__all__ = [
    'AddPersonDialog',
    'EndMarriageDialog',
    'CreateMarriageDialog',
    'CreateChildDialog',
    'CreateEventDialog',
    'EditEventDialog'
]