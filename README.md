# DynastyVizualizer

A beautiful, feature-rich family tree visualization and genealogy management application for games with multi-generational families.

## Overview

DynastyVizualizer brings professional genealogy software features to gaming communities. Originally designed for [Ostriv](https://store.steampowered.com/app/773790/Ostriv/), it provides an intuitive interface for tracking complex family dynasties across generations, with support for multiple visualization modes, relationship tracing, portrait galleries, and historical event tracking.

### Why DynastyVizualizer?

- **Multiple Views**: Visualize your dynasty as an interactive tree, chronological timeline, data table, or statistics dashboard
- **Intelligent Layouts**: Automatic generational hierarchy with cohort positioning (families that move in together are displayed near age-peers)
- **Rich Relationships**: Track marriages, divorces, remarriages, affairs, step-families, and complex genealogical connections
- **Visual Customization**: Themeable UI with skins (parchment, blueprint, modern), portrait galleries, and family color coding
- **Powerful Search**: Real-time filtering and relationship path tracing between any two people
- **Full History**: Personal event logs, job changes, illnesses, injuries, and major historical events
- **Undo/Redo Everything**: Every operation is reversible, from data edits to UI changes

---

## Current Features (v0.1 - Early Development)

### ✅ Implemented (Phase 1 Complete + Phase 2 Started)
- ✅ Database & File Management
  - Create and manage dynasty database files (`.dyn` format)
  - Comprehensive database schema with 8 tables (flexible date support)
  - SQLite-based data persistence with automatic migration support
  - File operations (New, Open, Save, Save As) - **fully functional**
  - Unsaved changes tracking and prompting
- ✅ Application Framework
  - Clean, professional UI framework with menu structure
  - Undo/redo infrastructure (Command pattern framework)
  - Settings management system with disk persistence (QSettings)
- ✅ **Keyboard Shortcuts** - All menu actions have customizable shortcuts:
  - **File**: Ctrl+N (New), Ctrl+O (Open), Ctrl+S (Save), Ctrl+Shift+S (Save As), Ctrl+Q (Exit)
  - **Edit**: Ctrl+Z (Undo), Ctrl+Y (Redo), Ctrl+P (Add Person), Del (Remove Person)
  - **View**: Ctrl+1 (Family Trees), Ctrl+2 (Timeline), Ctrl+3 (Dynasty), Ctrl+4 (Data Table)
  - **Tools**: F5 (Rebuild Scene), Ctrl+R (Recompute Generations)
  - **Settings**: Ctrl+, (Open Settings)
  - **Help**: F1 (About)
- ✅ **Add Person Feature** (COMPLETE) - Full implementation with undo/redo:
  - **Person data model** - Complete dataclass with 25 fields:
    - Name fields: first, middle, last, maiden, nickname
    - Flexible date support: birth/death/arrival/moved_out (year/month/day)
    - Relationships: father, mother, family
    - Game fields: dynasty_id, is_founder, education
    - Computed properties: full_name, display_name, is_deceased, age calculations
    - Date formatting methods with European format support
  - **PersonRepository** - Full CRUD operations:
    - Create: insert(), insert_with_id() (preserves ID on redo)
    - Read: get_by_id(), get_all(), get_by_name(), get_children(), get_alive_in_year()
    - Update: update()
    - Delete: delete()
  - **AddPersonCommand** - Undoable command with ID preservation:
    - run() method for execution
    - undo() method for reversal
    - Preserves person ID across undo/redo cycles
  - **AddPersonDialog** - Professional dialog interface:
    - Special character toolbar (á, ý, ó, é, í) for non-English names
    - Required fields: first name, last name, birth year
    - Optional fields: gender, notes
    - Input validation with error messages
    - Close warning for unsaved changes (Qt built-in)
  - **Database migration system** - Automatic schema upgrade:
    - Safely adds new columns to existing databases
    - Creates backup before migration
    - Preserves all existing data

### 🚧 In Progress (Phase 1-2 Completion)
- 🚧 Settings dialog UI (keyboard shortcut customization, appearance, formats)
- 🚧 Help menu (About dialog)
- 🚧 Remove Person dialog with confirmation
- 🚧 Edit Person dialog (modify existing people)

---

## Planned Features

### 🎯 Phase 2: Data Management (Weeks 3-5) - In Progress (~35% Complete)
- ✅ Person data model with dataclass (25 fields, computed properties, date formatting)
- ✅ PersonRepository with full CRUD operations and search methods
- ✅ AddPersonCommand with undo/redo and ID preservation
- ✅ AddPersonDialog with special character support and validation
- ✅ Database migration system for schema upgrades
- 📋 EditPersonCommand and EditPersonDialog
- 📋 RemovePersonCommand and RemovePersonDialog with confirmation
- 📋 Create marriages and parent-child relationships
- 📋 Track multiple marriages and divorces
- 📋 Support for portraits with date-based switching
- 📋 Personal event logs (jobs, illnesses, residences, etc.)

**Next**: Edit Person dialog, Remove Person dialog, Marriage creation

### 🌳 Phase 3: Interactive Family Tree (Weeks 6-10)
- 📋 Visual person boxes with portraits, names, and key dates
- 📋 **Drag-and-drop**: Reposition people or drag onto each other to create marriages
- 📋 Automatic generational layout with cohort positioning
- 📋 **In-place editing**: Click any field to edit directly
- 📋 **Gear icon**: Opens extended details panel with tabs for:
  - Basic info and all editable fields
  - Personal event history
  - Relationship overview
  - Portrait gallery
- 📋 Generation bands showing hierarchical levels
- 📋 Scrollable, zoomable canvas (pan with middle-mouse, zoom with scroll wheel)
- 📋 Right-click context menus for quick actions

### 🔍 Phase 4: Relationship Analysis (Weeks 11-13)
- 📋 **Single-click**: Highlight immediate family (parents, spouses, children)
- 📋 **Double-click**: Set as "primary" person and label all relationships
  - Brothers, sisters, grandparents, uncles, aunts, cousins
  - Step-parents, step-siblings, half-siblings
  - "1st removed", "2nd removed" for distant relatives
- 📋 **Ctrl+Click two people**: Find and highlight relationship path
  - Visual gradient (green → yellow → red by distance)
  - Popup explaining relationship ("Alice is Bob's great-aunt's grandson")
  - Dim unrelated people
- 📋 **Real-time search**: Type names to filter tree and auto-scroll to matches

### 📅 Phase 5: Timeline View (Weeks 14-17)
- 📋 Horizontal scrolling timeline with family lifespans
- 📋 Collapsible family bars showing move-in to extinction dates
- 📋 Individual lifespan bars with event markers:
  - Marriages, children born, job changes, illnesses
  - Clickable icons showing event details
- 📋 **Major events**: Add historical context (wars, plagues, disasters)
  - Vertical lines across all families
  - Date ranges for ongoing events
- 📋 **Sticky headers**: Family bars stay pinned while scrolling through members
- 📋 Portrait thumbnails on person bars

### 📊 Phase 6: Data Tables & Import (Weeks 18-20)
- 📋 Spreadsheet-style editing for power users
- 📋 Sortable, filterable tables for people, marriages, events
- 📋 Family statistics table with computed metrics:
  - Member count (living/total)
  - Longest-lived member
  - Most children (father/mother separately)
- 📋 **CSV Import**: Bulk data entry with flexible date formats
  - Auto-detection of date formats (YYYY-MM-DD, DD-MM-YYYY, etc.)
  - Column mapping and validation preview
  - Error correction before import

### 📈 Phase 7: Statistics & Validation (Weeks 21-23)
- 📋 Family dashboard with key metrics:
  - Population over time
  - Lifespan averages
  - Family size distributions
- 📋 Interactive charts (population trends, deaths per year)
- 📋 **Family comparison**: Ctrl+Click families to compare side-by-side
  - Member counts, lifespans, intermarriage statistics
  - Shared ancestors
- 📋 **Data validation tools**:
  - Find overlapping marriages
  - Detect impossible dates (child born before parent)
  - Identify circular parentage
  - Clickable validation reports

### 🎨 Phase 8: Visual Customization (Weeks 24-26)
- 📋 **UI Skins**: Choose from multiple themes
  - Default (clean, modern)
  - Parchment (aged paper aesthetic)
  - Blueprint (technical drawing)
  - Medieval (illuminated manuscript)
  - Import custom skins
- 📋 **Portrait Management**:
  - Multiple portraits per person
  - Date-based portrait switching ("looked like this from 1705-1720")
  - Auto-cycle or manual selection
  - Portrait gallery view
- 📋 **Family Color Coding** (optional):
  - Visual family identification
  - Relationship distance gradient (green=close, red=distant)
  - Toggle on/off in preferences

### ⚙️ Phase 9: Polish & Convenience (Weeks 27-30)
- 📋 Comprehensive preferences dialog (date formats, auto-save, behavior)
- 📋 **Keyboard shortcuts**:
  - Ctrl+N/O/S (File operations)
  - Ctrl+Z/Y (Undo/Redo)
  - Ctrl+F (Search), Ctrl+P (Add Person), Del (Delete)
  - Ctrl+1/2/3/4 (Switch views)
  - Ctrl+Plus/Minus/0 (Zoom)
- 📋 **Export functionality**:
  - Save tree view as high-resolution PNG/JPG
  - Export entire tree (not just viewport)
  - Optional PDF export (multi-page)
- 📋 **Right-click workflows**:
  - "Get Married" → searchable spouse selector
  - "Create Child" → searchable partner selector
  - Quick access to all common operations
- 📋 First-run tutorial and sample dynasty
- 📋 Auto-save with configurable intervals

### 🚀 Future Possibilities (Post-Release)
- 📋 Multi-dynasty support (work on multiple dynasties simultaneously)
- 📋 Game-specific integrations (Ostriv, Crusader Kings 3 save file import)
- 📋 Cloud sync and collaboration features
- 📋 Mobile version (touch-optimized interface)
- 📋 Advanced genealogy (trait tracking, DNA simulation)
- 📋 Research citations and media attachments

---

## Installation

### Requirements
- **Python 3.10 or higher**
- **PySide6** (Qt for Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/thief9001-maker/DynastyVizualizer.git
cd DynastyVizualizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

---

## Usage Guide

### Creating a New Dynasty
1. Launch DynastyVizualizer
2. Go to **File → New Dynasty**
3. Choose a location and name for your `.dyn` file
4. Start adding people and families

### Managing People
- **Add Person**: Right-click canvas or use **Edit → Add Person**
- **Edit Person**: Double-click person box or click gear icon for extended panel
- **Quick Edit**: Click any field (name, dates) to edit in-place
- **Delete Person**: Select and press Delete, or right-click → Delete

### Creating Relationships
- **Marriage (Drag-Drop)**: Drag a person box onto another to create a marriage
- **Marriage (Right-Click)**: Right-click person → "Get Married" → search for spouse
- **Add Child**: Right-click marriage node → "Add Child"

### Navigation
- **Pan**: Middle-mouse drag or scrollbars
- **Zoom**: Ctrl + Scroll wheel
- **Search**: Ctrl+F to open search bar, type name to filter tree
- **Switch Views**: Ctrl+1 (Tree), Ctrl+2 (Timeline), Ctrl+3 (Table), Ctrl+4 (Stats)

### Saving Your Work
- **Save**: File → Save (Ctrl+S)
- **Save As**: File → Save As (Ctrl+Shift+S)
- **Auto-Save**: Configurable in preferences (Phase 9)
- The application will prompt you before closing with unsaved changes

---

## Technical Architecture

DynastyVizualizer uses a clean **MVC (Model-View-Controller)** architecture combined with the **Command Pattern** for comprehensive undo/redo support:

- **Model**: SQLite database with Person, Marriage, Event, Portrait, Family, and MajorEvent tables
- **View**: PySide6 (Qt) widgets for multiple visualization modes
- **Controller**: Action handlers coordinating user interactions
- **Command Pattern**: Every operation is undoable/redoable (data edits, UI changes, imports)

This architecture scales seamlessly from simple operations to complex features like draggable UI elements, relationship tracing, and bulk data import.

See [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md) for comprehensive technical documentation.

---

## Development Status

**Current Phase**: Phase 1 Complete, Phase 2 In Progress
**Progress**: ~15% of total project
**Lines of Code**: ~1,900 (estimated final: 8,000-12,000)
**Next Milestone**: Complete Edit/Remove Person dialogs, begin marriage creation

### What Works Now
- ✅ Application launches with menu bar and keyboard shortcuts
- ✅ File → New Dynasty (creates `.dyn` database)
- ✅ File → Open Dynasty (loads existing database)
- ✅ File → Save / Save As (persists changes)
- ✅ File → Exit (with unsaved changes prompt)
- ✅ Database schema with all 8 tables
- ✅ Migration script for existing files
- ✅ **Edit → Add Person** (full dialog with undo/redo)
  - Special character support for non-English names
  - Input validation
  - Preserves ID on undo/redo

### What's Next (Completing Phase 2)
- 🚧 Edit → Remove Person (with confirmation)
- 🚧 Edit → Edit Person (modify existing person)
- 🚧 Help → About (application info dialog)
- 🚧 Marriage creation dialog
- 🚧 Parent-child relationship assignment

### Roadmap Summary

| Phase | Description | Status | Progress | Weeks |
|-------|-------------|--------|----------|-------|
| **1** | Foundation (Database, Menus, Framework) | ✅ Complete | 100% | 1-2 |
| **2** | Data Models & CRUD Dialogs | 🚧 In Progress | ~35% | 2-5 |
| **3** | Interactive Family Tree (QGraphicsView) | 📋 Planned | 0% | 6-10 |
| **4** | Relationship Analysis & Tracing | 📋 Planned | 0% | 11-13 |
| **5** | Timeline View | 📋 Planned | 0% | 14-17 |
| **6** | Data Tables & CSV Import | 📋 Planned | 0% | 18-20 |
| **7** | Statistics & Validation | 📋 Planned | 0% | 21-23 |
| **8** | Visual Customization (Skins, Portraits) | 📋 Planned | 0% | 24-26 |
| **9** | Polish & Convenience | 📋 Planned | 0% | 27-30 |
| **10** | Future Enhancements | 📋 Post-Release | 0% | TBD |

---

## Database Schema

Dynasty files (`.dyn`) are SQLite databases with flexible date handling and comprehensive relationship tracking.

### Core Tables
- **Person**: Names, dates (birth/death/arrival), parent references, portraits
- **Marriage**: Spouse pairs, marriage dates, dissolution dates and reasons
- **Event**: Personal history (jobs, illnesses, moves) with start/end dates

### Extended Tables (Included from Start)
- **Portrait**: Multiple images per person with date ranges
- **Family**: Dynasty grouping with move-in dates, coat of arms, colors
- **MajorEvent**: Historical context markers (wars, plagues, festivals)
- **PersonPosition**: Custom drag-and-drop positions
- **Settings**: User preferences

### Flexible Date Support

All date fields support three levels of precision:
- **Year Only**: `1705` (for unknown month/day)
- **Year/Month**: `March 1705` (typical for Ostriv)
- **Year/Month/Day**: `March 15, 1705` (real-world genealogy)

This design seamlessly supports both game contexts (like Ostriv without day precision) and real-world genealogy.

See [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md) for complete SQL schemas.

---

## Contributing

This project follows strict coding conventions for consistency and maintainability.

### Coding Standards
- **Type Hints**: Python 3.10+ syntax (`X | None`, lowercase `list[T]`, `dict[K, V]`)
- **Docstrings**: Concise single-line format (5-15 words, imperative verbs)
- **Code Style**: PEP 8 compliant
- **Architecture**: Follow MVC + Command patterns

### Development Workflow
1. Review scaffolded files in project structure
2. Implement following established patterns (see reference files)
3. Add undo/redo support via Command pattern
4. Update UI integration
5. Test thoroughly (especially undo/redo)

See [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md) for complete style guide and file templates.

---

## Technology Stack

- **Python 3.10+** - Modern Python with type hints
- **PySide6 6.10.1** - Qt framework for rich, cross-platform GUI
- **SQLite** - Embedded database for `.dyn` file persistence
- **Command Pattern** - Comprehensive undo/redo architecture

**Future Dependencies** (Phase 7+):
- **matplotlib** or **Qt Charts** - Statistics visualizations
- **Pillow** - Image processing for portraits

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built for the [Ostriv](https://store.steampowered.com/app/773790/Ostriv/) gaming community
- Developed with PySide6 (Qt for Python)
- Inspired by professional genealogy software with a focus on gaming use cases

---

## Project Links

- **Repository**: https://github.com/thief9001-maker/DynastyVizualizer
- **Issue Tracker**: https://github.com/thief9001-maker/DynastyVizualizer/issues
- **Technical Documentation**: [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md)
- **Code Sharing Utility**: [scripts/create_codebase_summary.py](scripts/create_codebase_summary.py)

---

## Support

Found a bug? Have a feature request? Please [open an issue](https://github.com/thief9001-maker/DynastyVizualizer/issues) on GitHub.

For questions about Ostriv-specific use cases, visit the Ostriv community forums.

---

**Version**: 0.1.0-dev
**Status**: Early Development (Phase 1 Complete, Phase 2: ~35% Complete)
**Last Updated**: 2025-12-13

---

## Vision Statement

DynastyVizualizer aims to be the definitive tool for managing complex family dynasties in gaming. We're building something that looks professional, feels intuitive, and provides the depth that dynasty-management enthusiasts crave—whether you're tracking three generations in Ostriv or twenty generations in Crusader Kings.

Every feature is designed with both power users and newcomers in mind: drag-and-drop for quick marriages, but also detailed event logs for deep genealogical research. Real-time search to find anyone instantly, but also relationship path tracing to discover how that random villager is actually your character's third cousin twice removed.

This is a labor of love for gaming communities who care about their virtual families as much as we do. 🏰👨‍👩‍👧‍👦
