import sys
from PySide6.QtWidgets import QApplication

from database.db_manager import DatabaseManager
from database.person_repository import PersonRepository
from dialogs.edit_person_dialog import EditPersonDialog

app = QApplication(sys.argv)

# Open database
db = DatabaseManager(None)
db.open_database("Struggberg Family Tree 1.dyn")  # Use your actual .dyn file

# Get a person to edit
repo = PersonRepository(db)
people = repo.get_all()

if people:
    person = people[0]  # Edit the first person
    
    dialog = EditPersonDialog(db, person)
    result = dialog.exec()
    
    if result:
        print("User clicked Save")
    else:
        print("User clicked Cancel")
else:
    print("No people in database!")

sys.exit(0)