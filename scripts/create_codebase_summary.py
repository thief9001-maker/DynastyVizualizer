"""
Auto-generate CODEBASE_SUMMARY.md - Complete codebase snapshot optimized for LLMs.

This script creates a token-efficient, complete snapshot of the entire codebase
that LLMs (Claude, ChatGPT) can use to understand the full project state.

Usage:
    python scripts/create_codebase_summary.py

Output:
    CODEBASE_SUMMARY.md - Complete codebase with all source files

Features:
    - Auto-discovers all non-ignored files
    - Includes full source code for all files
    - Token-efficient format (minimal prose, maximum code)
    - LLM-optimized structure (clear sections, easy to parse)
    - Includes essential metadata and project status
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Tuple


# Configuration
OUTPUT_FILE = "CODEBASE_SUMMARY.md"
PROJECT_NAME = "DynastyVizualizer"

# Files/directories to ignore (gitignore-style)
IGNORE_PATTERNS = {
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    ".env",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".DS_Store",
    "*.egg-info",
    "dist",
    "build",
    ".idea",
    ".vscode",
    "*.dyn",
    "*.backup",
    "node_modules",
}

# File extensions to include as source code
SOURCE_EXTENSIONS = {".py"}

# Config files to include
CONFIG_FILES = {"requirements.txt", "LICENSE"}

# Documentation files (extract minimal info only)
DOC_FILES = {"README.md", "dynasty_codebase.md"}


def should_ignore(path: Path) -> bool:
    """Check if path should be ignored based on patterns."""
    path_str = str(path)
    name = path.name

    # Check exact matches
    if name in IGNORE_PATTERNS:
        return True

    # Check wildcard patterns
    for pattern in IGNORE_PATTERNS:
        if "*" in pattern:
            ext = pattern.replace("*", "")
            if path_str.endswith(ext):
                return True

    # Ignore the output file itself
    if name == OUTPUT_FILE:
        return True

    return False


def count_lines(filepath: Path) -> int:
    """Count total lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def count_code_lines(filepath: Path) -> int:
    """Count non-empty, non-comment lines."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            count = 0
            in_multiline_string = False

            for line in f:
                stripped = line.strip()

                # Skip empty lines
                if not stripped:
                    continue

                # Toggle multiline string state
                if '"""' in stripped or "'''" in stripped:
                    in_multiline_string = not in_multiline_string
                    continue

                # Skip if in multiline string or comment
                if in_multiline_string or stripped.startswith('#'):
                    continue

                count += 1

            return count
    except Exception:
        return 0


def discover_files(root_dir: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Discover all files in the project.

    Returns:
        (source_files, config_files, doc_files)
    """
    source_files = []
    config_files = []
    doc_files = []

    for path in sorted(root_dir.rglob("*")):
        # Skip directories and ignored files
        if path.is_dir() or should_ignore(path):
            continue

        # Categorize files
        if path.suffix in SOURCE_EXTENSIONS:
            source_files.append(path)
        elif path.name in CONFIG_FILES:
            config_files.append(path)
        elif path.name in DOC_FILES:
            doc_files.append(path)

    return source_files, config_files, doc_files


def get_relative_path(filepath: Path, root: Path) -> str:
    """Get path relative to project root."""
    try:
        return str(filepath.relative_to(root))
    except ValueError:
        return str(filepath)


def read_file_content(filepath: Path) -> str:
    """Read file content safely, trying multiple encodings."""
    # Try common encodings
    for encoding in ['utf-8', 'utf-16', 'utf-16-le', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                # Check if content looks reasonable (no null bytes everywhere)
                if '\x00' not in content or encoding.startswith('utf-16'):
                    return content
        except (UnicodeDecodeError, Exception):
            continue

    # Fallback: read as binary and decode with error handling
    try:
        with open(filepath, 'rb') as f:
            return f.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"[Error reading file: {e}]"


def extract_quick_reference(doc_files: List[Path], root: Path) -> str:
    """Extract minimal quick reference from dynasty_codebase.md."""
    dynasty_file = None
    for f in doc_files:
        if f.name == "dynasty_codebase.md":
            dynasty_file = f
            break

    if not dynasty_file:
        return "No quick reference available."

    content = read_file_content(dynasty_file)

    # Extract just the first section (up to first ---) for minimal context
    lines = content.split('\n')
    ref_lines = []
    section_count = 0

    for line in lines:
        if line.strip() == '---':
            section_count += 1
            if section_count >= 2:  # Stop after first major section
                break
        ref_lines.append(line)

    return '\n'.join(ref_lines[:40])  # Limit to ~40 lines max


def build_file_tree(source_files: List[Path], root: Path) -> str:
    """Build visual file tree."""
    # Group files by directory
    tree_dict = {}

    for filepath in source_files:
        rel_path = get_relative_path(filepath, root)
        parts = Path(rel_path).parts

        current = tree_dict
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        # Mark file as implemented (✅) if it has substantial code
        lines = count_code_lines(filepath)
        marker = " ✅" if lines > 20 else " 📋"
        current[parts[-1]] = marker

    # Build tree string
    def build_tree_recursive(d, prefix="", is_last=True):
        lines = []
        items = sorted(d.items())

        for i, (key, value) in enumerate(items):
            is_last_item = (i == len(items) - 1)
            connector = "└── " if is_last_item else "├── "

            if isinstance(value, str):  # It's a file
                lines.append(f"{prefix}{connector}{key}{value}")
            else:  # It's a directory
                lines.append(f"{prefix}{connector}{key}/")
                extension = "    " if is_last_item else "│   "
                lines.extend(build_tree_recursive(value, prefix + extension, is_last_item))

        return lines

    tree_lines = [f"{PROJECT_NAME}/"] + build_tree_recursive(tree_dict)
    return '\n'.join(tree_lines)


def generate_summary(root_dir: Path) -> None:
    """Generate the complete codebase summary."""

    print(f"🔍 Discovering files in {PROJECT_NAME}...")
    source_files, config_files, doc_files = discover_files(root_dir)

    # Calculate statistics
    total_files = len(source_files)
    implemented_files = sum(1 for f in source_files if count_code_lines(f) > 20)
    total_lines = sum(count_lines(f) for f in source_files)
    code_lines = sum(count_code_lines(f) for f in source_files)

    print(f"📊 Found {total_files} Python files ({implemented_files} implemented)")
    print(f"📏 Total: {total_lines} lines ({code_lines} code lines)")

    # Generate output
    output_path = root_dir / OUTPUT_FILE

    with open(output_path, 'w', encoding='utf-8') as out:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Header
        out.write(f"# {PROJECT_NAME} - Complete Codebase Snapshot\n\n")
        out.write(f"**Generated**: {timestamp}\n")
        out.write(f"**Files**: {implemented_files} implemented / {total_files} total\n")
        out.write(f"**Lines**: ~{code_lines:,} code / ~{total_lines:,} total\n")
        out.write(f"**Status**: Phase 1 Complete, Phase 2 In Progress\n\n")
        out.write("---\n\n")

        # Quick Reference
        out.write("## Quick Reference\n\n")
        quick_ref = extract_quick_reference(doc_files, root_dir)
        out.write(quick_ref)
        out.write("\n\n---\n\n")

        # File Tree
        out.write("## File Structure\n\n")
        out.write("```\n")
        out.write(build_file_tree(source_files, root_dir))
        out.write("\n```\n\n")
        out.write("Legend: ✅ Implemented (>20 code lines) | 📋 Scaffolded\n\n")
        out.write("---\n\n")

        # Implementation Status
        out.write("## Implementation Status\n\n")
        out.write(f"**Implemented**: {implemented_files}/{total_files} files\n\n")

        # Group by directory
        by_dir = {}
        for f in source_files:
            rel_path = get_relative_path(f, root_dir)
            dir_name = str(Path(rel_path).parent)
            if dir_name == ".":
                dir_name = "root"

            if dir_name not in by_dir:
                by_dir[dir_name] = []

            lines = count_code_lines(f)
            status = "✅" if lines > 20 else "📋"
            by_dir[dir_name].append((Path(rel_path).name, lines, status))

        for dir_name in sorted(by_dir.keys()):
            out.write(f"**{dir_name}/**\n")
            for name, lines, status in sorted(by_dir[dir_name]):
                out.write(f"- {status} `{name}` ({lines} lines)\n")
            out.write("\n")

        out.write("---\n\n")

        # Complete Source Code
        out.write("## Complete Source Code\n\n")

        # Group files by category for better organization
        categories = {
            "Core": ["main.py"],
            "Database": [],
            "Models": [],
            "Actions": [],
            "Commands": [],
            "Dialogs": [],
            "Views": [],
            "Widgets": [],
            "Utils": [],
            "Scripts": [],
        }

        for f in source_files:
            rel_path = get_relative_path(f, root_dir)
            parent = str(Path(rel_path).parent)

            if "database" in parent:
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
            elif rel_path not in categories["Core"]:
                categories["Core"].append(f)

        # Output each category
        for category, files in categories.items():
            if not files or (len(files) == 1 and isinstance(files[0], str)):
                continue

            out.write(f"### {category}\n\n")

            for filepath in sorted(files):
                if isinstance(filepath, str):
                    filepath = root_dir / filepath

                rel_path = get_relative_path(filepath, root_dir)
                lines = count_lines(filepath)

                out.write(f"#### {rel_path} ({lines} lines)\n\n")
                out.write("```python\n")
                out.write(read_file_content(filepath))
                out.write("\n```\n\n")

                print(f"✅ Included {rel_path} ({lines} lines)")

        # Configuration Files
        if config_files:
            out.write("---\n\n")
            out.write("## Configuration\n\n")

            for filepath in config_files:
                rel_path = get_relative_path(filepath, root_dir)
                out.write(f"### {rel_path}\n\n")
                out.write("```\n")
                out.write(read_file_content(filepath))
                out.write("\n```\n\n")

        # Footer
        out.write("---\n\n")
        out.write(f"**End of {PROJECT_NAME} Codebase Snapshot**\n\n")
        out.write(f"- **Files**: {implemented_files} implemented / {total_files} total\n")
        out.write(f"- **Lines**: {code_lines:,} code / {total_lines:,} total\n")
        out.write(f"- **Generated**: {timestamp}\n")

    print(f"\n✅ Successfully generated {OUTPUT_FILE}")
    print(f"📊 {implemented_files}/{total_files} files, {code_lines:,} code lines")
    print(f"📄 Output: {output_path}")
    print(f"🤖 Ready for LLM consumption!\n")


if __name__ == "__main__":
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    print(f"{'='*60}")
    print(f"  {PROJECT_NAME} - Codebase Summary Generator")
    print(f"{'='*60}\n")

    generate_summary(project_root)
