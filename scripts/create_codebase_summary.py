"""
Script to create a single text file containing your entire codebase
for sharing with Claude in chat conversations.

Usage:
1. Copy this script to your project root folder
2. Run: python scripts/create_codebase_summary.py
3. Upload the generated dynasty_codebase.txt to Claude

This script is useful for:
- Sharing code with claude.ai for architecture discussions
- Getting feedback on implementation approaches
- Planning new features with full codebase context
"""

import os
from pathlib import Path

# Configuration
OUTPUT_FILE = "dynasty_codebase.txt"
PROJECT_NAME = "DynastyVizualizer"
PROJECT_DESCRIPTION = "Family tree GUI for game Ostriv"
TECH_STACK = "PySide6, SQLite, Python 3.10+"

# Files to include (add or remove as needed)
FILES_TO_INCLUDE = [
    "main.py",
    "database/db_manager.py",
    "actions/__init__.py",
    "actions/file_actions.py",
    "actions/edit_actions.py",
    "actions/view_actions.py",
    "actions/tools_actions.py",
    "actions/help_actions.py",
    "actions/settings_actions.py",
    "commands/undo_redo_manager.py",
    "utils/settings_manager.py",
    "models/person.py",
    # Add more files here as you implement them
    # "models/person.py",
    # "models/marriage.py",
    # "models/event.py",
]

# Additional context files to include
CONTEXT_FILES = [
    "README.md",
    "CODEBASE_SUMMARY.md",
]


def count_lines(filepath):
    """Count non-empty lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return sum(1 for line in f if line.strip())
    except Exception:
        return 0


def create_summary():
    """Create the codebase summary file."""

    # Calculate total lines
    total_lines = sum(count_lines(f) for f in FILES_TO_INCLUDE if os.path.exists(f))
    file_count = sum(1 for f in FILES_TO_INCLUDE if os.path.exists(f))

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as output:
        # Write header
        output.write(f"{'='*70}\n")
        output.write(f"{'='*70}\n")
        output.write(f"  {PROJECT_NAME} - Complete Codebase\n")
        output.write(f"{'='*70}\n")
        output.write(f"{'='*70}\n\n")
        output.write(f"Project: {PROJECT_DESCRIPTION}\n")
        output.write(f"Tech Stack: {TECH_STACK}\n")
        output.write(f"Code Files: {file_count} files, ~{total_lines} lines\n")
        output.write(f"\n{'='*70}\n\n")

        # Write context files first (README, CODEBASE_SUMMARY)
        output.write("CONTEXT & DOCUMENTATION\n")
        output.write(f"{'='*70}\n\n")

        for filepath in CONTEXT_FILES:
            if not os.path.exists(filepath):
                continue

            lines = count_lines(filepath)
            print(f"📄 Adding context: {filepath} ({lines} lines)")

            output.write(f"\n{'─'*70}\n")
            output.write(f"FILE: {filepath}\n")
            output.write(f"{'─'*70}\n\n")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    output.write(f.read())
            except Exception as e:
                output.write(f"[Error reading file: {e}]\n")

            output.write("\n")

        # Write implementation files
        output.write(f"\n{'='*70}\n")
        output.write("IMPLEMENTATION CODE\n")
        output.write(f"{'='*70}\n\n")

        for filepath in FILES_TO_INCLUDE:
            if not os.path.exists(filepath):
                print(f"⚠️  Skipping {filepath} (file not found)")
                continue

            lines = count_lines(filepath)
            print(f"✅ Adding {filepath} ({lines} lines)")

            output.write(f"\n{'─'*70}\n")
            output.write(f"FILE: {filepath} ({lines} lines)\n")
            output.write(f"{'─'*70}\n\n")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    output.write(f.read())
            except Exception as e:
                output.write(f"[Error reading file: {e}]\n")

            output.write("\n")

        # Write footer
        output.write(f"\n{'='*70}\n")
        output.write(f"End of {PROJECT_NAME} codebase\n")
        output.write(f"Total: {file_count} implementation files, {total_lines} lines\n")
        output.write(f"{'='*70}\n")

    print(f"\n✅ Successfully created {OUTPUT_FILE}")
    print(f"📊 Total: {file_count} files, {total_lines} lines of code")
    print(f"📤 Ready to upload to Claude for discussion!\n")


if __name__ == "__main__":
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    print(f"Creating codebase summary for {PROJECT_NAME}...\n")
    create_summary()
