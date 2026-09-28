"""The write's gate (the model owner's word of 2026-09-28, 09:05 Israel time, through the Closer): every level written onto the GameBoard is one act of the write (features/write) or Rule3's own step (core/rule3); the loop applies the folders' writes and the step's levels at the sites named here and nowhere else, and no folder writes a level itself. A new site of a write into a record's `now`, `before`, `im_now`, `im_before` or `remainder` anywhere under `src/event_universe` (an item assigned or augmented, or the attribute rebound) fails by module, function, kind and level; the gate reads names, so a level written through a local alias is a finding for the reader."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "event_universe"
LEVELS = frozenset({"now", "before", "im_now", "im_before", "remainder"})
Site = tuple[str, str, str, str]  # (module, function, "index" or "rebind", the level's name)

# the sites the loop writes levels at, each the application of a declared act (the record's own step by Rule3; the giving's window write through the write's line and its inverse by the folder's step back; the hold's and the source's writes through the line; THE START through the line; the bodies' own records at the load): per module, "function kind level" sites separated by ";"
SITES_TEXT = """
events/after_step.py: window_write index before; window_write index im_now; window_write index now
events/assembly.py: bodies index before; bodies index now; start_at_rest index before; start_at_rest index now; start_at_rest index remainder
events/detector_law.py: _advance index remainder; _advance rebind before; _advance rebind im_before; _advance rebind im_now; _advance rebind now; _advance rebind remainder; _advance_inverse index remainder; _advance_inverse rebind before; _advance_inverse rebind im_before; _advance_inverse rebind im_now; _advance_inverse rebind now; _advance_inverse rebind remainder; _advance_node_record rebind before; _advance_node_record rebind now; _advance_node_record rebind remainder; _hold index before; _hold index now; _hold index remainder; _point_window_inverse index before; _point_window_inverse index now; _source_stage index now
events/pair.py: second_level rebind im_before; second_level rebind im_now
"""
SITES: frozenset[Site] = frozenset(
    (module, *site.split())  # type: ignore[misc]
    for module, _, sites in (line.partition(": ") for line in SITES_TEXT.strip().splitlines())
    for site in sites.split("; ")
)


def written_object(target: ast.expr) -> ast.expr:
    """The object a subscript writes into, through a call around it (`cast(np.ndarray, live.im_now)[mask]`)."""
    while isinstance(target, ast.Call) and target.args:
        target = target.args[-1]
    return target


def write_sites(package: Path = PACKAGE) -> frozenset[Site]:
    """Every assignment or augmented assignment under the package whose target is an item of, or the attribute, `now`, `before`, `im_now`, `im_before` or `remainder` of any object, by module, enclosing function, kind and level."""
    found: set[Site] = set()

    def visit(node: ast.AST, module: str, function: str) -> None:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            function = node.name
        if isinstance(node, ast.Assign | ast.AugAssign | ast.AnnAssign):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                for element in target.elts if isinstance(target, ast.Tuple) else [target]:
                    indexed = isinstance(element, ast.Subscript)
                    held = written_object(element.value) if indexed else element
                    if isinstance(held, ast.Attribute) and held.attr in LEVELS:
                        found.add((module, function, "index" if indexed else "rebind", held.attr))
        for child in ast.iter_child_nodes(node):
            visit(child, module, function)

    for path in sorted(package.rglob("*.py")):
        module = str(path.relative_to(package))
        visit(ast.parse(path.read_text(encoding="utf-8")), module, "<module>")
    return frozenset(found)


def test_no_module_writes_a_level_outside_the_named_sites():
    """The engine's level writes are exactly the named sites: a new one (a folder writing a level itself, a write beside the write's line) fails by name, and a site that left is struck from the list."""
    found = write_sites()
    assert sorted(found - SITES) == [], "new write sites"
    assert sorted(SITES - found) == [], "sites no longer written"
