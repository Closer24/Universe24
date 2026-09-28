"""The write's gate (the model owner's word of 2026-09-28, 09:05 Israel time, through the Closer): every level written onto the GameBoard is one act of the write (features/write) or Rule3's own step (core/rule3); the loop applies the folders' writes and the step's levels at the sites named here and nowhere else, and no folder writes a level itself. A new site of a write into a record's `now`, `before`, `im_now`, `im_before` or `remainder` anywhere under `src/event_universe` (an item assigned or augmented, or the attribute rebound) fails by module, function, kind and level."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "event_universe"
LEVELS = frozenset({"now", "before", "im_now", "im_before", "remainder"})
Site = tuple[str, str, str, str]  # (module, function, "index" or "rebind", the level's name)

# the sites the loop writes levels at, each the application of a declared act: the record's own
# step (Rule3, `_advance`, `_advance_inverse`, `_advance_node_record`, pair.second_level), the
# giving's shell write through the write's line (after_step.shell_write), the hold's writes and
# the source's through the line (`_hold`, `_source_stage`), THE START through the line
# (assembly.start_at_rest) and the bodies' own records at the load (assembly.bodies)
SITES: frozenset[Site] = frozenset(
    {
        ("events/after_step.py", "shell_write", "index", "before"),
        ("events/after_step.py", "shell_write", "index", "im_now"),
        ("events/after_step.py", "shell_write", "index", "now"),
        ("events/assembly.py", "bodies", "index", "before"),
        ("events/assembly.py", "bodies", "index", "now"),
        ("events/assembly.py", "start_at_rest", "index", "before"),
        ("events/assembly.py", "start_at_rest", "index", "now"),
        ("events/assembly.py", "start_at_rest", "index", "remainder"),
        ("events/detector_law.py", "_advance", "index", "remainder"),
        ("events/detector_law.py", "_advance", "rebind", "before"),
        ("events/detector_law.py", "_advance", "rebind", "im_before"),
        ("events/detector_law.py", "_advance", "rebind", "im_now"),
        ("events/detector_law.py", "_advance", "rebind", "now"),
        ("events/detector_law.py", "_advance", "rebind", "remainder"),
        ("events/detector_law.py", "_advance_inverse", "index", "remainder"),
        ("events/detector_law.py", "_advance_inverse", "rebind", "before"),
        ("events/detector_law.py", "_advance_inverse", "rebind", "im_before"),
        ("events/detector_law.py", "_advance_inverse", "rebind", "im_now"),
        ("events/detector_law.py", "_advance_inverse", "rebind", "now"),
        ("events/detector_law.py", "_advance_inverse", "rebind", "remainder"),
        ("events/detector_law.py", "_advance_node_record", "rebind", "before"),
        ("events/detector_law.py", "_advance_node_record", "rebind", "now"),
        ("events/detector_law.py", "_advance_node_record", "rebind", "remainder"),
        ("events/detector_law.py", "_hold", "index", "before"),
        ("events/detector_law.py", "_hold", "index", "now"),
        ("events/detector_law.py", "_hold", "index", "remainder"),
        ("events/detector_law.py", "_source_stage", "index", "now"),
        ("events/pair.py", "second_level", "rebind", "im_before"),
        ("events/pair.py", "second_level", "rebind", "im_now"),
    }
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


def test_the_folders_calling_rule3s_division_act_are_the_named_ones():
    """The callers of Rule3's division act (`carried`, `division_forward`, `division_back`) among the folders are the named ones: the write, the four level writers through their fallback `carried_line` (the hold also reading the dipole back, the recoil also checking its wall), and the folders dividing a body's own value and no level (the spin's step; the feed and the induction, derived by the law and leaving the engine); a new folder with a division of its own fails by name."""
    calls: dict[str, set[str]] = {}
    for path in sorted((PACKAGE / "features").rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"carried", "division_forward", "division_back"}:
                    calls.setdefault(str(path.relative_to(PACKAGE)), set()).add(node.func.id)
    assert calls == {
        "features/feed/__init__.py": {"division_forward", "division_back"},
        "features/giving/__init__.py": {"carried"},
        "features/hold/__init__.py": {"carried", "division_back"},
        "features/induction/__init__.py": {"division_forward", "division_back"},
        "features/recoil/__init__.py": {"carried", "division_forward"},
        "features/source/__init__.py": {"carried"},
        "features/spins_step/__init__.py": {"carried"},
        "features/write/__init__.py": {"carried"},
    }
