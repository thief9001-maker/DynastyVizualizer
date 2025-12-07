# DynastyVizualizer

A family tree visualization and management application for the game [Ostriv](https://store.steampowered.com/app/773790/Ostriv/).

## Overview

DynastyVizualizer provides an intuitive GUI for creating, editing, and visualizing multi-generational family dynasties. Track births, deaths, marriages, occupations, and other life events across your Ostriv settlement's families.

## Features

### Current Features (v0.1)
- ✅ Create and manage dynasty database files (`.dyn` format)
- ✅ SQLite-based data persistence
- ✅ Undo/redo support for all operations
- ✅ File operations (New, Open, Save, Save As)
- ✅ Unsaved changes tracking and prompting

### Planned Features
- 📋 Person, marriage, and event data management
- 📋 Interactive dynasty tree visualization
- 📋 Timeline view for chronological events
- 📋 Data table view for spreadsheet-like editing
- 📋 Data validation tools (marriages, parentage)
- 📋 Generation computation
- 📋 Import/export capabilities

## Installation

### Requirements
- Python 3.10 or higher
- PySide6 (Qt for Python)

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

## Usage

### Creating a New Dynasty
1. Launch the application
2. Go to **File → New Dynasty**
3. Choose a location and name for your `.dyn` file
4. Start adding families and persons (upcoming feature)

### Opening an Existing Dynasty
1. Go to **File → Open Dynasty**
2. Select a `.dyn` file
3. View and edit your dynasty (upcoming feature)

### Saving Your Work
- **File → Save** - Save changes to current file
- **File → Save As** - Save to a new file location
- The application will prompt you to save unsaved changes when exiting

## Architecture

DynastyVizualizer uses a clean MVC architecture with the Command pattern for undo/redo functionality:

- **Model**: SQLite database with Person, Marriage, and Event tables
- **View**: PySide6 (Qt) widgets for visualization
- **Controller**: Action handlers coordinating user interactions
- **Command Pattern**: All data modifications are undoable/redoable

See [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md) for detailed technical documentation.

## Development Status

**Current Phase**: Core Infrastructure (Phase 1)
**Progress**: ~15% complete
**Lines of Code**: ~532 lines across 9 implemented files

### Project Phases
1. ✅ **Core Infrastructure** - Application framework, database, file operations
2. 🚧 **Data Models** - Person, Marriage, Event classes (in progress)
3. 📋 **Views & Visualization** - Dynasty tree, timeline, data table widgets
4. 📋 **Commands & Operations** - Full CRUD with undo/redo
5. 📋 **Polish & Features** - Validation, import/export, preferences

## Database Schema

Dynasty files (`.dyn`) are SQLite databases with the following structure:

### Person Table
Stores individual family members with birth, death, and arrival dates, plus parent references.

### Marriage Table
Tracks marriages between persons, including marriage and dissolution dates.

### Event Table
Records life events (occupations, residences, etc.) associated with persons.

See [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md) for complete SQL schema.

## Contributing

### Coding Standards
This project follows strict coding conventions for consistency:

- **Type Hints**: Python 3.10+ syntax (`X | None`, lowercase `list[T]`)
- **Docstrings**: Concise single-line format (5-15 words)
- **Code Style**: PEP 8 compliant
- **Architecture**: Follow established MVC + Command patterns

See [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md) for complete style guide.

### Development Workflow
1. Check scaffolded files in the project structure
2. Implement following the established patterns
3. Add undo/redo support via Command pattern
4. Update UI to integrate new features
5. Test with sample dynasty files

## Technology Stack

- **Python 3.10+** - Modern Python with type hints
- **PySide6** - Qt framework for rich GUI
- **SQLite** - Embedded database for data persistence
- **Command Pattern** - Comprehensive undo/redo support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the [Ostriv](https://store.steampowered.com/app/773790/Ostriv/) community
- Developed using PySide6 (Qt for Python)

## Project Links

- **Repository**: https://github.com/thief9001-maker/DynastyVizualizer
- **Issue Tracker**: https://github.com/thief9001-maker/DynastyVizualizer/issues
- **Documentation**: [CODEBASE_SUMMARY.md](CODEBASE_SUMMARY.md)

---

**Version**: 0.1.0-dev
**Status**: Early Development
**Last Updated**: 2025-12-07
