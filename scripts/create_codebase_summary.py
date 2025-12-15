"""
Generate dynasty_codebase.txt - Complete codebase snapshot optimized for LLMs.

Creates a token-efficient snapshot of ALL source code that LLMs can use to
understand the complete project state in a single context window.

Usage:
    python scripts/create_codebase_summary.py

Output:
    dynasty_codebase.txt - Complete codebase, LLM-optimized

Features:
    - Token-efficient: Minimal headers, maximum code density
    - Complete: ALL Python files included
    - Organized: Grouped by category for easy parsing
    - Compact: No visual trees, just clean code listings
    - Smart encoding: Handles UTF-8, UTF-16
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Tuple


# Configuration
OUTPUT_FILE = "dynasty_codebase.txt"
PROJECT_NAME = "DynastyVizualizer"

# Files/directories to ignore
IGNORE_PATTERNS = {
    "__pycache__", ".git", ".pytest_cache", ".venv", "venv", "env",
    ".env", "*.pyc", "*.pyo", "*.pyd", ".DS_Store", "*.egg-info",
    "dist", "build", ".idea", ".vscode", "*.dyn", "*.backup",
    "node_modules", "*.md", "dynasty_codebase.txt"
}

# File extensions to include
SOURCE_EXTENSIONS = {".py"}

# Config files to include
CONFIG_FILES = {"requirements.txt"}


def should_ignore(path: Path) -> bool:
    """Check if path or any parent should be ignored."""
    path_str = str(path)
    
    # Check if any part of the path matches ignore patterns
    for part in path.parts:
        if part in IGNORE_PATTERNS:
            return True
    
    # Check filename patterns
    name = path.name
    for pattern in IGNORE_PATTERNS:
        if "*" in pattern:
            ext = pattern.replace("*", "")
            if path_str.endswith(ext):
                return True
    
    if name == OUTPUT_FILE:
        return True
    
    return False

def count_code_lines(filepath: Path) -> int:
    """Count non-empty, non-comment lines."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            count = 0
            in_multiline = False

            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue

                if '"""' in stripped or "'''" in stripped:
                    in_multiline = not in_multiline
                    continue

                if in_multiline or stripped.startswith('#'):
                    continue

                count += 1

            return count
    except Exception:
        return 0


def discover_files(root_dir: Path) -> Tuple[List[Path], List[Path]]:
    """Discover all source and config files."""
    source_files = []
    config_files = []

    for path in sorted(root_dir.rglob("*")):
        if path.is_dir() or should_ignore(path):
            continue

        if path.suffix in SOURCE_EXTENSIONS:
            source_files.append(path)
        elif path.name in CONFIG_FILES:
            config_files.append(path)

    return source_files, config_files


def get_relative_path(filepath: Path, root: Path) -> str:
    """Get path relative to project root."""
    try:
        return str(filepath.relative_to(root))
    except ValueError:
        return str(filepath)


def read_file_content(filepath: Path) -> str:
    """Read file content with multiple encoding support."""
    for encoding in ['utf-8', 'utf-16', 'utf-16-le', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                if '\x00' not in content or encoding.startswith('utf-16'):
                    return content
        except (UnicodeDecodeError, Exception):
            continue

    try:
        with open(filepath, 'rb') as f:
            return f.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"[Error: {e}]"


def categorize_files(source_files: List[Path], root: Path) -> dict:
    """Organize files by category."""
    categories = {
        "Core": [], "Database": [], "Models": [], "Actions": [],
        "Commands": [], "Dialogs": [], "Views": [], "Widgets": [],
        "Utils": [], "Scripts": []
    }

    for f in source_files:
        rel_path = get_relative_path(f, root)
        parent = str(Path(rel_path).parent)

        if rel_path == "main.py":
            categories["Core"].append(f)
        elif "database" in parent:
            categories["Database"].append(f)
        elif "models" in parent:
            categories["Models"].append(f)
        elif "actions" in parent:
            categories["Actions"].append(f)
        elif "commands" in parent:
            categories["Commands"].append(f)
        elif "dialogs" in parent:
            categories["Dialogs"].append(f)
        elif "views" in parent:
            categories["Views"].append(f)
        elif "widgets" in parent:
            categories["Widgets"].append(f)
        elif "utils" in parent:
            categories["Utils"].append(f)
        elif "scripts" in parent:
            categories["Scripts"].append(f)
        else:
            categories["Core"].append(f)

    return categories


def generate_summary(root_dir: Path) -> None:
    """Generate the token-efficient codebase snapshot."""

    print(f"🔍 Discovering files in {PROJECT_NAME}...")
    source_files, config_files = discover_files(root_dir)

    total_files = len(source_files)
    implemented = sum(1 for f in source_files if count_code_lines(f) > 20)
    code_lines = sum(count_code_lines(f) for f in source_files)

    print(f"📊 Found {total_files} files ({implemented} implemented, {code_lines} code lines)")

    categories = categorize_files(source_files, root_dir)
    output_path = root_dir / OUTPUT_FILE

    with open(output_path, 'w', encoding='utf-8') as out:
        # Compact header
        out.write(f"{'='*70}\n")
        out.write(f"{PROJECT_NAME} - Complete Codebase\n")
        out.write(f"{'='*70}\n")
        out.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        out.write(f"Files: {implemented}/{total_files} implemented | {code_lines} code lines\n")
        out.write(f"Tech: PySide6, SQLite, Python 3.10+ | MVC + Command pattern\n")
        out.write(f"Status: Phase 1 Complete, Phase 2 ~35% (Add Person done)\n")
        out.write(f"{'='*70}\n\n")

        # Quick context
        out.write("QUICK CONTEXT:\n")
        out.write("Family tree/genealogy GUI for gaming (Ostriv). Features: Person CRUD,\n")
        out.write("undo/redo, flexible dates, special char support, DB migration.\n")
        out.write("Pattern: User Action → Dialog → Command → Repository → Database\n\n")

        # File index (compact)
        out.write("FILE INDEX:\n")
        for category, files in categories.items():
            if files:
                out.write(f"{category}: ")
                file_names = [get_relative_path(f, root_dir) for f in sorted(files)]
                out.write(", ".join(file_names[:5]))
                if len(files) > 5:
                    out.write(f", ... ({len(files)} total)")
                out.write("\n")
        out.write(f"\n{'='*70}\n")
        out.write("COMPLETE SOURCE CODE\n")
        out.write(f"{'='*70}\n\n")

        # Output code by category (compact format)
        for category, files in categories.items():
            if not files:
                continue

            out.write(f"\n{'─'*70}\n")
            out.write(f"{category.upper()}\n")
            out.write(f"{'─'*70}\n\n")

            for filepath in sorted(files):
                rel_path = get_relative_path(filepath, root_dir)
                lines = count_code_lines(filepath)
                status = "✅" if lines > 20 else "📋"

                # Compact file header
                out.write(f">> {status} {rel_path} ({lines} code lines)\n")
                out.write(read_file_content(filepath))
                out.write("\n\n")

                print(f"✅ {rel_path} ({lines} lines)")

        # Config files
        if config_files:
            out.write(f"\n{'─'*70}\n")
            out.write("CONFIGURATION\n")
            out.write(f"{'─'*70}\n\n")

            for filepath in config_files:
                rel_path = get_relative_path(filepath, root_dir)
                out.write(f">> {rel_path}\n")
                out.write(read_file_content(filepath))
                out.write("\n\n")

        # Compact footer
        out.write(f"\n{'='*70}\n")
        out.write(f"END - {implemented}/{total_files} files, {code_lines} code lines\n")
        out.write(f"{'='*70}\n")

    print(f"\n✅ Generated {OUTPUT_FILE}")
    print(f"📊 {implemented}/{total_files} files, {code_lines:,} code lines")
    print(f"📄 Output: {output_path}")
    print(f"🤖 Token-optimized for LLM consumption!\n")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    print(f"{'='*60}")
    print(f"  {PROJECT_NAME} - Codebase Generator")
    print(f"{'='*60}\n")

    generate_summary(project_root)
