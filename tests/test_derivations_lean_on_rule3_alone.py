"""The derivations' gate (the owner's order of 2026-10-04, 04:20 UTC: every derived mark's script from Rule3 and nothing of the simulator; the law's sentence beside the method of derivation, step 6, "No line of the law is derived from the engine", tested here by name): every module of tools/derivations/ imports nothing of event_universe or src/ and names no run's file, a hard rule; the paper-side scripts of paper/general_formula/ that lean on the engine or read a run are a ratchet that only falls;
the modules that do not root in tools/derivations/rule3.py are a ratchet that only falls, so a new module imports rule3; rule3.py's own checks, a plane wave at the derived omega satisfying the line to rounding and the conserved form exact over 50 intervals on a periodic chain of 24 Nodes with integer levels, the remainders' walk the law's term;
and the inventory tools/derivations/paper_marks.json loads with every field, its scriptless marks a ratchet that only falls, and every mark it names scripted is its script's output to the digits printed."""

import ast
import importlib
import importlib.util
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DERIVATIONS = ROOT / "tools" / "derivations"
PAPER_SCRIPTS = ROOT / "paper" / "general_formula"
INVENTORY = DERIVATIONS / "paper_marks.json"
# the engine's package, its folder and a tool that imports it; a run's files
ENGINE = ("event_universe", "src", "click_counts")
RUN_FILE = ("runs/", ".output.json", ".look.json")
# the four modules of pull request #1854 written before rule3.py that receive no mark of the inventory
# (greens_function, two_body, units, wells); every other module roots in rule3 since the derivations' map
MODULES_WITHOUT_RULE3_ROOT = 4
# at origin/paper d75c42a9: two_slits_real_line.py imports the engine, two_slits_frames.py reads a run's look
PAPER_SCRIPTS_LEANING_ON_THE_ENGINE = 2
# the derived and computed marks of main.tex naming no script at d75c42a9 (123) whose inventory entry still has no
# script here, the status "scriptless"; a ceiling the count may only fall below (the 11 computed marks, closed by
# their readers and never by a derivation, and 7 derived marks after the derivations' map)
SCRIPTLESS_MARKS = 18
FIELDS = (
    "line",
    "mark",
    "main_section",
    "excerpt",
    "numbers",
    "source",
    "existing_script",
    "proposed_module",
    "status",
)
COMPUTED_FIELDS = ("reader", "derived_counterpart", "bound")
# scriptless: no script here yet; scripted: its script's function returns the printed numbers; differs: it does not, a finding for the hands
STATUSES = ("scriptless", "scripted", "differs")
SCRIPTED_FIELDS = ("script", "function", "expected", "digits")


def imported(tree: ast.Module) -> set[str]:
    """The top-level package of every import of a module's tree."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def leans_on_the_engine(path: Path) -> list[str]:
    """Every way a script leans on the engine or a run: an import of its package, or a run's file named in a string outside the docstrings."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = [f"imports {name}" for name in sorted(imported(tree) & set(ENGINE))]
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docstrings.add(id(first.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
            found += [f"names {marker!r}" for marker in RUN_FILE if marker in node.value]
    return found


def rule3():
    spec = importlib.util.spec_from_file_location("rule3", DERIVATIONS / "rule3.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_derivation_module_imports_the_engine_and_the_paper_scripts_leaning_on_it_only_fall():
    """(a) Every module of tools/derivations/ imports nothing of event_universe or src/ and names no run's file; the paper-side scripts in the tree that import the engine or read a run number at most the ratchet's count."""
    modules = sorted(DERIVATIONS.glob("*.py"))
    assert modules, "tools/derivations/ holds the derivation modules"
    leaning = {m.name: leans_on_the_engine(m) for m in modules}
    assert not {k: v for k, v in leaning.items() if v}, leaning
    scripts = {p.name: leans_on_the_engine(p) for p in sorted(PAPER_SCRIPTS.glob("*.py"))}
    paper_leaning = {k: v for k, v in scripts.items() if v}
    assert len(paper_leaning) <= PAPER_SCRIPTS_LEANING_ON_THE_ENGINE, paper_leaning


def test_the_modules_without_the_rule3_root_only_fall():
    """(b) The modules of tools/derivations/ that do not import rule3 number at most the ratchet's count, so a new module roots in rule3.py."""
    rootless = []
    for path in sorted(DERIVATIONS.glob("*.py")):
        if path.name == "rule3.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        if "rule3" not in imported(tree):
            rootless.append(path.name)
    assert len(rootless) <= MODULES_WITHOUT_RULE3_ROOT, rootless


def test_a_plane_wave_at_the_derived_omega_satisfies_the_line_and_the_form_is_conserved():
    """(c) rule3.py: the plane wave at cos omega = (num / (3 den)) (2 + cos k) satisfies the line to rounding on a chain; the band at the vacuum's paces is the same number; the conserved form is exact over 50 intervals on a periodic chain of 24 Nodes from integer levels, the integer step's walk of E the law's term exactly, and the backward act returns the state bit for bit."""
    law = rule3()
    for num, den in ((1, 1), (2, 3), (4000, 6000)):
        assert law.plane_wave_residual(math.pi / 4, num, den) < 1e-6
        at_paces = law.dispersion_at_paces((0.3, 0.0, 0.0), num, den, 6000, 6000, (6000,) * 3)
        assert abs(at_paces - law.plane_wave_dispersion(0.3, num, den)) < 1e-12
    assert abs(law.group_velocity(1e-3, 1, 1) - 1 / math.sqrt(3)) < 1e-5
    draw, nodes, num, den = random.Random(24), 24, 2, 3
    arrivals = law.chain_arrivals(nodes)
    now = [draw.randint(-1000, 1000) for _ in range(nodes)]
    before = [draw.randint(-1000, 1000) for _ in range(nodes)]
    start = law.conserved_form(now, before, arrivals, num, den)
    exact_now, exact_before = [Fraction(v) for v in now], [Fraction(v) for v in before]
    for _ in range(50):
        step = [
            law.step_exact(exact_now[i], exact_before[i], [exact_now[j] for j in arrivals[i]], num, den)
            for i in range(nodes)
        ]
        exact_now, exact_before = step, exact_now
    assert law.conserved_form(exact_now, exact_before, arrivals, num, den) == start
    remainders = [0] * nodes
    for _ in range(50):
        energy = law.conserved_form(now, before, arrivals, num, den)
        stepped = [
            law.step(now[i], before[i], [now[j] for j in arrivals[i]], num, den, remainders[i])
            for i in range(nodes)
        ]
        levels, carried = [s[0] for s in stepped], [s[1] for s in stepped]
        walk = law.form_walk(remainders, carried, levels, before)
        assert law.conserved_form(levels, now, arrivals, num, den) - energy == walk
        back = [
            law.step_backward(now[i], levels[i], [now[j] for j in arrivals[i]], num, den, carried[i])
            for i in range(nodes)
        ]
        assert [b[0] for b in back] == before and [b[1] for b in back] == remainders
        now, before, remainders = levels, now, carried


def test_the_inventory_loads_and_its_scriptless_marks_only_fall():
    """(d) paper_marks.json loads, names the paper's head, every entry carries the fields and a computed one its reader, counterpart and bound, and the scriptless count is at most the ratchet's."""
    document = json.loads(INVENTORY.read_text(encoding="utf-8"))
    header, marks = document["header"], document["marks"]
    assert len(header["paper_head"]) == 40 and header["main_tex"] == "paper/general_formula/main.tex"
    for entry in marks:
        assert all(field in entry for field in FIELDS), entry
        assert entry["mark"] in ("derived", "computed") and entry["status"] in STATUSES
        if entry["status"] == "scripted":
            assert all(field in entry for field in SCRIPTED_FIELDS), entry["line"]
        if entry["status"] == "differs":
            assert all(field in entry for field in SCRIPTED_FIELDS[:2] + ("computed", "reason")), entry[
                "line"
            ]
        assert entry["excerpt"].isascii() and isinstance(entry["numbers"], list)
        if entry["mark"] == "computed":
            assert all(field in entry for field in COMPUTED_FIELDS), entry["line"]
        if entry["existing_script"] is not None:
            assert entry["existing_script"].startswith(("paper/general_formula/", "tools/derivations/"))
    scriptless = sum(entry["status"] == "scriptless" for entry in marks)
    assert header["counts"]["scriptless"] == scriptless <= SCRIPTLESS_MARKS


def agrees(value: object, printed: object, digits: int) -> bool:
    """A function's number against a printed one: a "num/den" string is an exact rational, equal as Fractions; an int is equal as it stands; a float is equal rounded to `digits` decimal places (a negative count rounds to tens and hundreds, a large one reaches 10^-29)."""
    if isinstance(printed, str):
        return Fraction(value) == Fraction(printed)  # type: ignore[arg-type]
    if isinstance(printed, int):
        return value == printed
    return round(float(value), digits) == round(float(printed), digits)  # type: ignore[arg-type]


def test_every_scripted_mark_is_its_scripts_output():
    """(e) Every entry of the inventory with the status "scripted" names its script under tools/derivations/, its function, the printed numbers and their digits; the function's output (a scalar or a list) carries the printed numbers in order, each a "num/den" string equal as a Fraction, an int equal as it stands or a float equal to `digits` decimal places (one count for every number or one count per number), so a scripted mark of the paper is its script's and no number of the paper is forced; a "differs" entry is not compared, it carries `computed` and `reason` for the hands."""
    document = json.loads(INVENTORY.read_text(encoding="utf-8"))
    scripted = [entry for entry in document["marks"] if entry["status"] == "scripted"]
    assert scripted, "the inventory names scripted marks"
    if str(DERIVATIONS) not in sys.path:
        sys.path.insert(
            0, str(DERIVATIONS)
        )  # the modules import rule3 by name, as they run from their folder
    modules: dict[str, object] = {}
    for entry in scripted:
        name = Path(entry["script"]).stem
        assert (
            entry["script"] == f"tools/derivations/{name}.py" and (DERIVATIONS / f"{name}.py").exists()
        ), entry["line"]
        module = modules.setdefault(name, importlib.import_module(name))
        result = getattr(module, entry["function"])()
        values = list(result) if isinstance(result, list | tuple) else [result]
        expected = entry["expected"]
        digits = (
            entry["digits"] if isinstance(entry["digits"], list) else [entry["digits"]] * len(expected)
        )
        assert len(digits) == len(expected) and expected, entry["line"]
        position = 0
        for printed, count in zip(expected, digits, strict=True):
            while position < len(values) and not agrees(values[position], printed, count):
                position += 1
            assert position < len(values), (entry["line"], entry["function"], printed, values)
            position += 1
