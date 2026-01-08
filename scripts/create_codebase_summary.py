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

from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

OUTPUT_FILE: str = "dynasty_codebase.txt"
PROJECT_NAME: str = "DynastyVizualizer"

IGNORE_PATTERNS: set[str] = {
    "__pycache__", ".git", ".pytest_cache", ".venv", "venv", "env",
    ".env", "*.pyc", "*.pyo", "*.pyd", ".DS_Store", "*.egg-info",
    "dist", "build", ".idea", ".vscode", "*.dyn", "*.backup",
    "node_modules", "*.md", "dynasty_codebase.txt"
}

SOURCE_EXTENSIONS: set[str] = {".py"}
CONFIG_FILES: set[str] = {"requirements.txt"}

INDENT: str = "\t"
MAX_FILES_PER_LINE: int = 50

# ------------------------------------------------------------------
# File Discovery
# ------------------------------------------------------------------

def should_ignore(path: Path) -> bool:
    """Check if path or any parent should be ignored."""
    path_str: str = str(path)
    
    for part in path.parts:
        if part in IGNORE_PATTERNS:
            return True
    
    name: str = path.name
    for pattern in IGNORE_PATTERNS:
        if "*" in pattern:
            ext: str = pattern.replace("*", "")
            if path_str.endswith(ext):
                return True
    
    if name == OUTPUT_FILE:
        return True
    
    return False


def discover_files(root_dir: Path) -> tuple[list[Path], list[Path]]:
    """Discover all source and config files."""
    source_files: list[Path] = []
    config_files: list[Path] = []
    
    for path in sorted(root_dir.rglob("*")):
        if path.is_dir():
            continue
        
        if should_ignore(path):
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


# ------------------------------------------------------------------
# File Analysis
# ------------------------------------------------------------------

def count_code_lines(filepath: Path) -> int:
    """Count non-empty, non-comment lines."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            count: int = 0
            in_multiline: bool = False
            
            for line in f:
                stripped: str = line.strip()
                
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


def read_file_content(filepath: Path) -> str:
    """Read file content with multiple encoding support."""
    for encoding in ['utf-8', 'utf-16', 'utf-16-le', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content: str = f.read()
                if '\x00' not in content or encoding.startswith('utf-16'):
                    return content
        except (UnicodeDecodeError, Exception):
            continue
    
    try:
        with open(filepath, 'rb') as f:
            return f.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"[Error: {e}]"


# ------------------------------------------------------------------
# File Categorization
# ------------------------------------------------------------------

def categorize_files(source_files: list[Path], root: Path) -> dict[str, list[Path]]:
    """Organize files by category with hierarchy."""
    categories: dict[str, list[Path]] = {
        "Core": [],
        "Database": [],
        "Models": [],
        "Actions": [],
        "Commands": [],
        "Dialogs": [],
        "Views": [],
        "Widgets": [],
        "Utils": [],
        "Scripts": []
    }
    
    for f in source_files:
        rel_path: str = get_relative_path(f, root)
        parent: str = str(Path(rel_path).parent)
        
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


def get_file_depth(filepath: str) -> int:
    """Get nesting depth of file based on directory separators."""
    parts: tuple[str, ...] = Path(filepath).parts
    
    if len(parts) == 1:
        return 0
    
    return len(parts) - 2


def format_file_index(categories: dict[str, list[Path]], root: Path) -> str:
    """Format file index with hierarchical indentation."""
    output: list[str] = ["FILE INDEX:"]
    
    for category, files in categories.items():
        if not files:
            continue
        
        output.append(f"{category}:")
        
        sorted_files: list[Path] = sorted(files, key=lambda f: get_relative_path(f, root))
        
        for filepath in sorted_files:
            rel_path: str = get_relative_path(filepath, root)
            depth: int = get_file_depth(rel_path)
            indent: str = INDENT * (depth + 1)
            
            output.append(f"{indent}{rel_path},")
    
    return "\n".join(output)


# ------------------------------------------------------------------
# Summary Generation
# ------------------------------------------------------------------

def write_header(out, stats: dict) -> None:
    """Write compact header to output file."""
    out.write(f"{'='*70}\n")
    out.write(f"{PROJECT_NAME} - Complete Codebase\n")
    out.write(f"{'='*70}\n")
    out.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    out.write(f"Files: {stats['implemented']}/{stats['total']} implemented | ")
    out.write(f"{stats['code_lines']} code lines\n")
    out.write(f"Tech: PySide6, SQLite, Python 3.10+ | MVC + Command pattern\n")
    out.write(f"Status: Phase 1 Complete, Phase 2 ~35% (Add Person done)\n")
    out.write(f"{'='*70}\n\n")


def write_context(out) -> None:
    """Write quick context section."""
    out.write("QUICK CONTEXT:\n")
    out.write("Family tree/genealogy GUI for gaming (Ostriv). Features: Person CRUD,\n")
    out.write("undo/redo, flexible dates, special char support, DB migration.\n")
    out.write("Pattern: User Action → Dialog → Command → Repository → Database\n\n")


def write_file_index(out, categories: dict[str, list[Path]], root: Path) -> None:
    """Write hierarchical file index."""
    out.write(format_file_index(categories, root))
    out.write(f"\n\n{'='*70}\n")
    out.write("COMPLETE SOURCE CODE\n")
    out.write(f"{'='*70}\n\n")


def write_category_code(out, category: str, files: list[Path], root: Path) -> None:
    """Write code for a single category."""
    if not files:
        return
    
    out.write(f"\n{'─'*70}\n")
    out.write(f"{category.upper()}\n")
    out.write(f"{'─'*70}\n\n")
    
    for filepath in sorted(files):
        rel_path: str = get_relative_path(filepath, root)
        lines: int = count_code_lines(filepath)
        status: str = "✅" if lines > 20 else "📋"
        
        out.write(f">> {status} {rel_path} ({lines} code lines)\n")
        out.write(read_file_content(filepath))
        out.write("\n\n")
        
        print(f"✅ {rel_path} ({lines} lines)")


def write_config_files(out, config_files: list[Path], root: Path) -> None:
    """Write configuration files section."""
    if not config_files:
        return
    
    out.write(f"\n{'─'*70}\n")
    out.write("CONFIGURATION\n")
    out.write(f"{'─'*70}\n\n")
    
    for filepath in config_files:
        rel_path: str = get_relative_path(filepath, root)
        out.write(f">> {rel_path}\n")
        out.write(read_file_content(filepath))
        out.write("\n\n")


def write_footer(out, stats: dict) -> None:
    """Write compact footer."""
    out.write(f"\n{'='*70}\n")
    out.write(f"END - {stats['implemented']}/{stats['total']} files, ")
    out.write(f"{stats['code_lines']} code lines\n")
    out.write(f"{'='*70}\n")


def calculate_stats(source_files: list[Path]) -> dict:
    """Calculate file statistics."""
    total: int = len(source_files)
    implemented: int = sum(1 for f in source_files if count_code_lines(f) > 20)
    code_lines: int = sum(count_code_lines(f) for f in source_files)
    
    return {
        'total': total,
        'implemented': implemented,
        'code_lines': code_lines
    }


def generate_summary(root_dir: Path) -> None:
    """Generate the token-efficient codebase snapshot."""
    print(f"🔍 Discovering files in {PROJECT_NAME}...")
    source_files, config_files = discover_files(root_dir)
    
    stats: dict = calculate_stats(source_files)
    
    print(f"📊 Found {stats['total']} files ({stats['implemented']} implemented, ")
    print(f"    {stats['code_lines']} code lines)")
    
    categories: dict[str, list[Path]] = categorize_files(source_files, root_dir)
    output_path: Path = root_dir / OUTPUT_FILE
    
    with open(output_path, 'w', encoding='utf-8') as out:
        write_header(out, stats)
        write_context(out)
        write_file_index(out, categories, root_dir)
        
        for category, files in categories.items():
            write_category_code(out, category, files, root_dir)
        
        write_config_files(out, config_files, root_dir)
        write_footer(out, stats)
    
    print(f"\n✅ Generated {OUTPUT_FILE}")
    print(f"📊 {stats['implemented']}/{stats['total']} files, {stats['code_lines']:,} code lines")
    print(f"📄 Output: {output_path}")
    print(f"🤖 Token-optimized for LLM consumption!\n")


# ------------------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------------------

def main() -> None:
    """Main entry point for script."""
    script_dir: Path = Path(__file__).parent
    project_root: Path = script_dir.parent
    os.chdir(project_root)
    
    print(f"{'='*60}")
    print(f"  {PROJECT_NAME} - Codebase Generator")
    print(f"{'='*60}\n")
    
    generate_summary(project_root)


if __name__ == "__main__":
    main()