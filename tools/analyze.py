"""Reverse-engineering helper: static analysis of a Python codebase.

For every module under the given directories it reports:
  * lines of code
  * classes and functions (with line numbers and whether they have docstrings)
  * imports of other project modules (the dependency graph)
  * module-level statements that run on import (side effects)
  * functions that read or modify module-level (global) state

It also prints a Mermaid dependency graph that can be pasted into Markdown.

Usage:
    python3.12 tools/analyze.py <project_dir> [<project_dir> ...]
"""

import ast
import sys
from pathlib import Path

SKIP_DIRS = {".venv", "venv", "__pycache__", ".git", "tests", "tools"}


def find_modules(root: Path) -> dict[str, Path]:
    """Map dotted module names (e.g. 'utils.helpers') to file paths."""
    modules = {}
    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts) or path.name == "__init__.py":
            continue
        modules[".".join(rel.with_suffix("").parts)] = path
    return modules


def module_globals(tree: ast.Module) -> set[str]:
    """Names assigned at module level."""
    names = set()
    for node in tree.body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        for t in targets:
            if isinstance(t, ast.Name):
                names.add(t.id)
    return names


def analyze(root: Path) -> None:
    modules = find_modules(root)
    edges = []
    print(f"\n{'#' * 70}\n# Project: {root.name}\n{'#' * 70}")

    for name, path in modules.items():
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        loc = sum(1 for line in source.splitlines() if line.strip() and not line.strip().startswith("#"))
        globals_ = module_globals(tree)
        print(f"\nModule: {name}  ({path.relative_to(root)}, {loc} LOC)")

        # Dependencies on other project modules
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in modules:
                imported = ", ".join(a.name for a in node.names)
                print(f"  imports  {node.module}: {imported}")
                edges.append((name, node.module, imported))
            elif isinstance(node, ast.Import):
                for a in node.names:
                    if a.name in modules:
                        edges.append((name, a.name, "*"))

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                doc = "doc" if ast.get_docstring(node) else "NO DOC"
                print(f"  class    {node.name} (line {node.lineno}, {doc})")
            elif isinstance(node, ast.FunctionDef):
                doc = "doc" if ast.get_docstring(node) else "NO DOC"
                used = sorted(
                    {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and n.id in globals_}
                )
                note = f", uses globals: {', '.join(used)}" if used else ""
                print(f"  function {node.name}() (line {node.lineno}, {doc}{note})")
            elif isinstance(node, (ast.Expr, ast.For, ast.While, ast.With)) and not (
                isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
            ):
                print(f"  SIDE EFFECT: top-level statement runs on import (line {node.lineno})")

    print("\nMermaid dependency graph:\n")
    print("```mermaid\ngraph TD")
    for src, dst, names in edges:
        print(f'    {src.replace(".", "_")}["{src}"] -->|{names}| {dst.replace(".", "_")}["{dst}"]')
    print("```")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        analyze(Path(arg).resolve())
