"""The shape of tests/, held against the merge base (issue #1211; the model owner, 2026-09-27: the bulk must not come back).

Every count is compared with the same count at the merge base (CHECK_BASE, else origin/main),
read from git, so no baseline file is kept: a pull request may lower a count, never raise it.

(a) Size. tests/ holds no more lines than at the merge base: it only shrinks, and a pull
    request that adds tests offsets them by deletions (the model owner, 2026-09-27); a test
    file above 600 lines holds no more than at the merge base, and a new one stays under.
    A test the Boss gives room by name (ROOM: the test, its lines and the reason, recorded
    here) adds that room to the base's size while it stands with
    at most those lines; nothing else grows the budget. A file the Boss gives a budget (ROOM:
    the file alone, its lines and the reason; the owner's word of 2026-10-29, 02:5x UTC) takes
    room as a test does, grows within it with no new entry, and is refused above it.
(b) Copied setup. No test module imports another `test_*.py`: shared builders live in
    `tests/frame.py`. A function of 8 lines or more whose abstracted
    body appears twice across tests/ is refused beyond the merge base's groups.
(c) History. Across tests/, the docstring and comment lines that carry a history marker, and
    the docstrings beyond three lines, stay at or below the merge base's (a moved helper moves
    its count with it).
(d) Retired code. Across tests/, the module-wide skips and the skips that name cancelled or
    retired code stay at or below the merge base's; a public function of `src/` that
    nothing in `src/`, `tools/` or `examples/` names is refused unless the merge base has it.
"""

from __future__ import annotations

import ast
import hashlib
import io
import re
import subprocess
import sys
import tokenize
from pathlib import Path

import merge_base
from record_code_shape import Abstracted, docstring_of

ROOT = Path(__file__).resolve().parents[1]
FILE_LINES = 600
DUPLICATE_LINES = 8
DOCSTRING_LINES = 3
HISTORY = re.compile(r"\b(?:SINCE|HISTORY|BUILD\.md|[Ss]uperseded|[Pp]reviously|[Rr]ecords? \d{3,})\b")
RETIRED = re.compile(r"CANCELLED|[Rr]etired")
TENSOR24_FRAME = "Tensor24's frame: the property tests any engine of the Node-clock must pass, locality, purity, rename, the 24's images and the run back, here and in fresh interpreters, with the board, its Spokes and its Meshes they are read on, the helpers the whole's test reads, and the half-open split on the edge's dial that the engine's and the run's tests read (the owner's words of 2026-10-30, one small test per generic part, \"only when yes and when no, by the standards in the world\"); 237 lines, its own at the merge of the edge, and now the owner's slack beside it (SLACK); 278 at the union on node-all (the converger's merges on the owner's word of 2026-10-31, 06:0x UTC, the code-clean auditor's A5): node-onelaw's clocks' plan of no term and a one-leg plan read as a matrix (7 lines), and node-edge's state turned by a lift moved here from the run test and every edge's two sides at their Node-clock (34), the old engine's out path (the auditor's B10) left to the fold's cut."
TENSOR24_DECODER_MEASURE = "Tensor24's decoder's measurement file, Animate's, its budget on Animate's word under decision 26: the Meshes between two sites, the shorter way round each of the board's sides, read twice, and the past cone one Mesh a round on them, as the click world's cone check reads them (the Boss's D8), failing on its own mutant; the cone check on takes, the twin reading and the duration on 1.2's whole clicks, readers of lines no run writes, cut with their tests on the owner's word of 2026-10-31, 01:2x UTC (\"Unnecessary tests: throw them out\"; the test pruner's cut); 21 lines and the owner's 40 of slack."
TENSOR24_FILES = "Tensor24's three files, stage 0 of the build the owner approved at 16:0x UTC on 2026-10-28: one test of the one generic checker, every example folder's three files holding, every rule refusing its own broken file by name with its edge holding (the push's switch refused above 1 and below 0, the key's oddness refused even and below 1), two departures named once, and the tool, on the owner's words of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\") and 10:2x UTC (\"why so many tests for so simple a system, one act of a generic node\")."
TENSOR24_RUN = "Tensor24's whole system once, on our bang, the three example files, on the owner's words of 2026-10-30, 09:2x UTC (\"what is generic, test only it, and then the whole\") and 10:2x UTC (\"why so many tests for so simple a system, one act of a generic node\"): laid by one formula on every row (the clock's read at k0 = Spokes x senses, the drive's teeth senses on the square's 00 and ii rows), a round the naive round reading the square's slots by name, every order of the trains and the 24's turns nothing to the act (the clock found by its place the mutant), the run to a record and a ledger of the schema the decoder reads, the run back exact and 0 where it misses, a departure, a broken promise or a lay outside the wave's window named with nothing written, by the run and its tool, and an even key named, and a pair world kept as NOT_CLOSED 37's record, its departures the width's own if any, and the width's promise at its edge (counts of 2^w - 1 in both slots named by none, 2^w and -2^w in either slot named, a free gear crossing the width by inertia in its one round named with nothing written; the seventh code reader's BLOCKING 3); 295 lines, its own at the reader's fold, and now the owner's slack beside it (SLACK)."
TENSOR24_WORLDS = "Tensor24's shipped worlds beside our bang, one parametrized function, on the owner's word of 2026-10-31 through the Boss (unnecessary tests go out, preventing fakes matters most) and the pruner's finding that only our bang's run was guarded: the click, live, mesh and well worlds each run their first rounds out and back by the run tool's own function, the run back exact, the state's digest, its count of click lines and their digest the ones the run wrote in tests/tensor24_prefixes.jsonl (derive/boss/prefixes/write.py), never typed in the test, each record read by the decoder's reader with no cause, the click world run to its first click, the no case's own digest written too, and the written worlds every example folder but our bang's; its no, the setting changed by one count, reaching another digest; 34 lines, and now the owner's slack beside it (SLACK)."
TENSOR24_ALGEBRA = "Tensor24's algebra: Rule3's carry, its tie rule and its whether, one test with its yes and its no (the owner's words of 2026-10-30, one small test per generic part, \"only when yes and when no, by the standards in the world\")."
TENSOR24_KINDS = "Tensor24's kinds and tables, the Node-clock's initialization from its star: the 24 a group, the five kinds its irreducible representations, the tables its channels, the four-vector's square and the joint, one test with its yes and its no (the owner's words of 2026-10-30, one small test per generic part, \"only when yes and when no, by the standards in the world\")."
TENSOR24_LIFTS = "Tensor24's lifts, items 1 and 2 of HALF2's section 2 on the Boss's build order of 2026-10-31, 02:2x UTC, by the hostile mathematician's measured construction (hf_math/probe_hm4): the 48 as the words u w^k z^m from the Node-clock's star, each once, of doubled norm senses^2, every product a lift with remainder 0 and the probe's closure of z and w the same 48 (the no: with no z, Hurwitz's 24), each lift's turn its sandwich and one of the 24 (the no: no reflection, no flat candidate), the eight kinds orthonormal on the 48 with the full turn -1 on the three half-speed ones, and the 8-gear train the probe's Ind_C6(lam) and the 24-gear train, the half-speed hand on the three axes (the 8-gear train laid on each axis row by each lift's turn, in place of the classes +-h since the doublets' piece, its character on all 48 the same), the probe's Ind_{+-1}(sign), each up to its gears' order and senses and a train of the product (the no: two gears swapped), each reading failing on its own mutant, and the eighth code reader's minors (each lift its word u w^k z^m by the test's own product, read through its unit part, its turn and its trains, as the lifts keep no word since the eighth reader's second read, w^d = -1 and z^senses = i, every carry of the lifts exact, T1 on the 48 the turns); 210 lines, and the owner's slack beside it (SLACK)."
TENSOR24_HALF = "Tensor24's half-speed trains in the runner, HALF2's section 2 from item 4, on the Boss's build order of 2026-10-31, 03:0x UTC: the files' eight kinds and the two half-speed trains they admit by character, the 8-gear train on the cosets of C6 and the 24-gear train, the half-speed hand on the three axes (the 8-gear train on each axis row), every other mix refused by name (an r2 part, not -I on the full turn, neither train's), and both refused in a file run, by the run and by the files tool, as no family couples a half-speed train in this build (test worlds only), and a half-speed train beside the click world's clocks no square, not the held hand, untied (the twist keeps its character, so its speed unties it), gripped, its rows its gears and its drive's teeth 1, the force's path, and its rows its cosets, each gear on its coset's row and a component past the last coset refused by name, and a half-speed world laid in memory through load.load and the act, both trains beside the square with the push on, at the rest 6 den Gamma^2 and at 6, every one of the 48 lifts turning the run with the teeth rounding and the run back exact, each passing pair a half-speed row with itself, no gradient term on one (the yes the carry's flip under signed permutations, each of which turns the run in this build; the no: at the rest 6 a negated gear's tooth not flipped, and at both dials a shear of the 8-gear train's gears, no signed permutation), the hand split under the 24 whole units into its three doublets alike but for omega's charge (E5/2 = E1/2 the doublet 2, G3/2 2' + 2'', the hand 4 of each, the 8-gear train 2' and 2'' twice with no 2; Pi_2 + Pi_c = 12 I and Pi_2 Pi_c = 0, each 12 times a projector, its trace 12 times its gears, a third on each axis row; Q central and antisymmetric, Q Pi_2 = 0 and Q Q = -Pi_c, kept by the 24 and sent to -Q by each r2 lift; the 48 turning the hand's run with the push on, the no a shear at both dials), and the board with its sites turned, each lift on its trains' gears with its own turn on the sites and the square's slots turning the run alike (the no the same), the dot's kept form read with its carry's remainder 0 and one form for every kind (the seventh reader's two minors on bb063b5ef), each reading failing on its own mutant; 339 lines, and the owner's slack beside it (SLACK)."
TENSOR24_LOAD = "Tensor24's load: the board and its Meshes, every gear on its train's rows with its click tooth at its birth, the square by its kinds' character with its 0i rows odd under the mirror, the teeth at rest, the grips, s, T_k and T_d from the files' integers, the chosen key and notch read into the click and the potential, one case per refusal and the round's promise at the edges of its dial; the plans laid from the kinds' tables and the star: the passing's pairs (the square's at 0 by its flag), the coupling family's frame by character (the held rows' own spring and their grips 0, the tie on the dot product's diagonal, the hands' tie once, the board's wave untied, the two tied hands swapped in the file laying the same plan), and term 5's push in the books' form at the dial senses (every gliding row's momenta in and out onto the 00 slot at k0 = Spokes x senses, the clock's read from the star, but the rows the push lands on; a tent's two Meshes' stretches squared onto its ii slot; nothing elsewhere; the drive's teeth senses on the 00 and ii rows; push 0 pushing nothing; either order of the trains), and the gradient vertex through the Mesh (-mesh onto each M_i's row from the wave's difference along i and +mesh onto the wave's row from M_i's, each term laid once with its other two readings the unit, one potential's two pushes, never a push laid twice or a cubic vertex; the wave with no vector hand laying nothing), each test with its yes and its no (the owner's words of 2026-10-30, one small test per generic part, \"only when yes and when no, by the standards in the world\"); 155 lines, its own at the gradient vertex (B5), the Boss's ceiling of 155, and now the owner's slack beside it (SLACK); 211 at the union on node-all (the converger's merges on the owner's word of 2026-10-31, 06:0x UTC, the code-clean auditor's A5): node-onelaw's whole action times one factor (28 lines), and node-edge's edges with their naive model (28), load.scaled's test with its function (the auditor's B5) left to the fold's cut or keep."
TENSOR24_ENGINE = "Tensor24's engine: the Node-clock's one act on the edge in its generic parts, J by the vertex law, the act against its naive model on the edge (the 00 count first, the half-open split, the state with its click tooth, the click of no term, J from the plan and the Mesh plan) with the frame's properties, the click tooth carrying the passing of a pair at one Node-clock with the mirror keeping it (the books, the teeth summing to key - 1, the run back with the quotients negated; the no: a lone hand clicking nowhere, and the click tooth flipped under the mirror not returning the teeth), the metric pushed in the books' form on the push's readings (the six stretches per row, the two momenta, the unit: the tent along z pushing the zz slot alone, the gliding hand the 00 slot alone, at k0 read from the clock read), the 24 turning the act alike under the twisted action on the square's rows laid, under the push with the clock moving and T_d above 1 (a negated row's counts negated and its two teeth flipped; the no: with the teeth kept, the three turns that negate no row hold alone), and its run back where every tooth stands within its edge's dial, the mirror by parity its own inverse, and one round under the push whose 00 slot reads the momenta of no row the push lands on (hypothesis (d)) (the no: a tooth past its dial, a tooth not flipped on an even row, the push reading the ii rows' momenta, and one half of the passing alone), each one test with its yes and its no, the cases a mutant once caught kept as plain assertions, each named (the owner's words of 2026-10-30, one small test per generic part, \"only when yes and when no, by the standards in the world\"); 300 lines, its own at the run back under the push and the flipped click tooth's no (the first hostile code reader's B1 and M2), the Boss's ceiling, and now the owner's slack beside it (SLACK); 364 at the union on node-all (the converger's merges on the owner's word of 2026-10-31, 06:0x UTC, the code-clean auditor's A5): node-onelaw's monomial of any number of legs and the naive model's clocks' plan (37 lines), and node-edge's click of no edge and two hands clicking on their edge's two sides (28), one line less as git merged them, the edge check twice and the four turned states (the auditor's C8) left to the fold's cut."
TENSOR24_DECODER = "Tensor24's decoder, Animate's, on the build the owner approved at 16:0x UTC on 2026-10-28 (\"Approved, build it. You on the engine. Animate on the decoder.\"): the record and its ledger read under the schema's rules, each broken one not read with its own cause, the tool naming every cause it meets and raising on none, each test failing on its own mutant; and the click world on schema 1.3 (the night's C5, the owner's build order of 2026-10-30, 23:5x UTC: \"Build a basic decoder on the clicks that knows how to show the physics there\"): the click lines listed and counted, the books at each click, the cone check by the lay's cone, D6 and D7 not read, and a record of no click line refused, each with its yes and its no; row 15 on whole clicks and the ledger's wind, a reader of lines no run writes, cut with its tests and its laws on the owner's word of 2026-10-31, 01:2x UTC (\"Unnecessary tests: throw them out\"; the test pruner's cut); 393 lines and the owner's 40 of slack. The old engine's records and their reader cut with their tests on the Boss's fold order of 2026-10-31, 07:5x UTC (the code-clean auditor's B1, B2 and C1): the whole, rate and books lines and the old ledger line gone, the reader's generic rules held once, on click lines and the ledger's Count lines, the decoder's second file folded in; 393 lines with the owner's slack beside it (SLACK)."
TENSOR24_DECODER_MEETINGS = "Tensor24's decoder's click-board test file, writer C's, its budget on the Boss's word under decision 26 (a second file for the new tests takes its own budget): the click board read as the clocks' meetings (the owner's word of 2026-10-31, 00:3x UTC; FRAMES.md 13b, on SHADOW's answer): the meetings, each clock's line of meetings counted with no duration, and light's echo, not read while no rule tells light's lines, and the fourth code reader's fold of C5 (the cone not read where no line could stand outside it, the books in row 15's order, each reading's own check for a record of no click line, the setting read by its name with its gears on the board), each with its yes, its no where it has one, and failing on its own mutant; 158 lines, and now the owner's slack beside it (SLACK), on the owner's list (M8) with C6."
TENSOR24_EDGES = "Tensor24's Mesh edges, writer B's, its room on the Boss's word of 2026-10-31, 05:2x UTC (\"granted\"): term 6's gradient vertex split by the Spoke it reads across (the wave's edge note, onelaw sections 1 and 3, both hostile readers' sound), on the mesh world's own files at a test's key above 1 (the readers' B2 and B3): the split the engine's Mesh contraction with 0 entries missed, one coupling at both ends, every edge's books closed in every round, the run back exact with the teeth carried from the forward run's end, and the line's 8 turns and a cube's 24 in memory, each with its no (a run back restarted at the teeth's birth missing, a tooth not complemented opening the books, the Mesh teeth left on their Spokes under a turn missing); 80 lines and the owner's slack beside it (SLACK)."
# every test file's budget is its present lines and a fixed slack, on the owner's word of 2026-10-31, 01:2x UTC
# ("unnecessary blockers and bureaucracy: throw them out"), in place of an exact budget; the other rules stand
SLACK = 40
TENSOR24_DECODER_SIDES = "Tensor24's decoder on schema 1.4's sides, writer C's, its budget on the Boss's word under decision 26 (a second file for the new tests takes its own budget) and his rulings of 2026-10-31, 04:3x and 04:4x UTC: one click line for the three clicks, one entry per edge side with its scalar tooth, each edge closing at its place (the owner's word of 03:4x UTC), on records written in memory: a place where three clocks meet read, and every rule of the sides refused by its own cause and read without the guard; on the owner's list (M8); raised to 102 by writer E for the books across a Mesh, each side booked at both its places, their yes and their no (the Boss's word of 06:0x UTC)."
ROOM = {  # the room given by name: the test or the file, its lines and the reason
    "tests/frame.py": (278 + SLACK, TENSOR24_FRAME),
    "tests/test_the_tensor24_engine.py": (364 + SLACK, TENSOR24_ENGINE),
    "tests/test_the_tensor24_algebra.py": (34 + SLACK, TENSOR24_ALGEBRA),
    "tests/test_the_tensor24_decoder.py": (393 + SLACK, TENSOR24_DECODER),
    "tests/test_the_tensor24_decoder_measure.py": (21 + SLACK, TENSOR24_DECODER_MEASURE),
    "tests/test_the_tensor24_decoder_meetings.py": (158 + SLACK, TENSOR24_DECODER_MEETINGS),
    "tests/test_the_tensor24_decoder_sides.py": (102 + SLACK, TENSOR24_DECODER_SIDES),
    "tests/test_the_tensor24_files.py": (310 + SLACK, TENSOR24_FILES),
    "tests/test_the_tensor24_run.py": (295 + SLACK, TENSOR24_RUN),
    "tests/test_the_tensor24_worlds.py": (34 + SLACK, TENSOR24_WORLDS),
    "tests/test_the_tensor24_kinds.py": (80 + SLACK, TENSOR24_KINDS),
    "tests/test_the_tensor24_lifts.py": (210 + SLACK, TENSOR24_LIFTS),
    "tests/test_the_tensor24_half.py": (339 + SLACK, TENSOR24_HALF),
    "tests/test_the_tensor24_load.py": (211 + SLACK, TENSOR24_LOAD),
    "tests/test_the_tensor24_edges.py": (80 + SLACK, TENSOR24_EDGES),
}
CALLERS = ("src/", "tools/", "examples/")

Snapshot = dict[str, str]


def working_tree(root: Path) -> Snapshot:
    """Every Python file of src/, tools/, examples/ and tests/ in the working tree."""
    found: Snapshot = {}
    for folder in ("src", "tools", "examples", "tests"):
        for path in sorted((root / folder).rglob("*.py")):
            found[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
    return found


def at_ref(root: Path, ref: str) -> Snapshot | None:
    """The same files at `ref`, or None where git cannot show it."""
    try:
        names = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref, "--", "src", "tools", "examples", "tests"],
            capture_output=True,
            text=True,
            cwd=root,
            check=True,
        ).stdout.split()
        names = [name for name in names if name.endswith(".py")]
        batch = subprocess.run(
            ["git", "cat-file", "--batch"],
            input="".join(f"{ref}:{name}\n" for name in names).encode(),
            capture_output=True,
            cwd=root,
            check=True,
        ).stdout
    except OSError, subprocess.CalledProcessError:
        return None
    found: Snapshot = {}
    offset = 0
    for name in names:
        header_end = batch.index(b"\n", offset)
        size = int(batch[offset:header_end].split()[2])
        found[name] = batch[header_end + 1 : header_end + 1 + size].decode("utf-8")
        offset = header_end + 1 + size + 1
    return found


def tests_of(snapshot: Snapshot) -> Snapshot:
    return {name: text for name, text in snapshot.items() if name.startswith("tests/")}


def lines_in(snapshot: Snapshot, folder: str) -> int:
    return sum(len(text.splitlines()) for name, text in snapshot.items() if name.startswith(folder))


def file_counts(text: str) -> dict[str, int]:
    """Per test file: its lines, history-marked lines, long docstrings and retirement skips."""
    tree = ast.parse(text)
    marked: set[int] = set()
    long_docstrings = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            doc = docstring_of(node)
            if doc is not None:
                end = doc.end_lineno or doc.lineno
                long_docstrings += end - doc.lineno + 1 > DOCSTRING_LINES
                source = text.splitlines()[doc.lineno - 1 : end]
                marked.update(doc.lineno + i for i, line in enumerate(source) if HISTORY.search(line))
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type == tokenize.COMMENT and HISTORY.search(token.string):
            marked.add(token.start[0])
    skip_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets
        ):
            if "skip" in ast.unparse(node.value):
                skip_lines.add(node.lineno)
        elif isinstance(node, ast.Call) and "skip" in ast.unparse(node.func):
            if RETIRED.search(ast.unparse(node)):
                skip_lines.add(node.lineno)
    skips = len(skip_lines)
    return {
        "lines": len(text.splitlines()),
        "history_lines": len(marked),
        "long_docstrings": long_docstrings,
        "retirement_skips": skips,
    }


def test_imports(snapshot: Snapshot) -> list[str]:
    """Every import of a `test_*.py` module by another test file."""
    found = []
    for name, text in tests_of(snapshot).items():
        for node in ast.walk(ast.parse(text)):
            module = node.module if isinstance(node, ast.ImportFrom) else None
            modules = [a.name for a in node.names] if isinstance(node, ast.Import) else [module or ""]
            for imported in modules:
                if imported.split(".")[-1].startswith("test_"):
                    found.append(f"{name} imports {imported}: move the helper to tests/frame.py")
    return found


def duplicate_groups(snapshot: Snapshot) -> dict[str, list[str]]:
    """Every abstracted body of a function of 8 lines or more that appears twice across tests/."""
    groups: dict[str, list[str]] = {}
    for name, text in tests_of(snapshot).items():
        for node in ast.walk(ast.parse(text)):
            if (
                isinstance(node, ast.FunctionDef)
                and (node.end_lineno or node.lineno) - node.lineno + 1 >= DUPLICATE_LINES
            ):
                copy = ast.parse(ast.unparse(node)).body[0]
                digest = hashlib.sha256(ast.dump(Abstracted().visit(copy)).encode()).hexdigest()[:16]
                groups.setdefault(digest, []).append(f"{name}:{node.name}")
    return {digest: sorted(names) for digest, names in groups.items() if len(names) > 1}


def uncalled(snapshot: Snapshot) -> set[str]:
    """The public top-level functions of src/ that nothing else names."""
    callers = "\n".join(text for name, text in snapshot.items() if name.startswith(CALLERS))
    found = set()
    for name, text in snapshot.items():
        if not name.startswith("src/"):
            continue
        for node in ast.parse(text).body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                if len(re.findall(rf"\b{node.name}\b", callers)) <= 1:
                    found.add(f"{name}:{node.name}")
    return found


def room_of(snapshot: Snapshot) -> int:
    """The room the named tests take in a snapshot: per ROOM entry whose test stands in its file, the fewer of its named lines and the test's own (the def through its last line), so a test keeps its room only while it holds it; 0 for a test that is gone. An entry that names a file alone is the file's budget, and the file takes the fewer of it and its own lines."""
    found = 0
    for name, (lines, _reason) in ROOM.items():
        path, _, function = name.partition("::")
        if path not in snapshot:
            continue
        if not function:
            found += min(lines, len(snapshot[path].splitlines()))
            continue
        for node in ast.walk(ast.parse(snapshot[path])):
            if isinstance(node, ast.FunctionDef) and node.name == function and node.end_lineno:
                found += min(lines, node.end_lineno - node.lineno + 1)
    return found


def over_budget(snapshot: Snapshot) -> list[str]:
    """Every file above the budget its ROOM entry gives it."""
    return [
        f"{name} has {len(snapshot[name].splitlines())} lines, above its budget of {lines}; raise the budget with its reason, or cut"
        for name, (lines, _reason) in ROOM.items()
        if "::" not in name and name in snapshot and len(snapshot[name].splitlines()) > lines
    ]


def violations(head: Snapshot, base: Snapshot | None) -> list[str]:
    """Every way the head departs from the shape, each one line; with no base, the head is its own base."""
    base = head if base is None else base
    found: list[str] = []
    # the room a push may take is what the head's budgets grant beyond what the base's already hold
    head_tests = lines_in(head, "tests/")
    base_tests = lines_in(base, "tests/") + room_of(head) - room_of(base)
    if head_tests > base_tests:
        found.append(
            f"tests/ grew from {base_tests} to {head_tests} lines; offset the new tests by deletions in the same pull request"
        )
    found.extend(over_budget(head))
    before = {name: file_counts(text) for name, text in tests_of(base).items()}
    after = {name: file_counts(text) for name, text in tests_of(head).items()}
    for name, counts in after.items():
        was = before.get(name, {"lines": 0})["lines"]
        if counts["lines"] > FILE_LINES and counts["lines"] > was:
            found.append(
                f"{name} has {counts['lines']} lines, above {FILE_LINES} and the merge base's {was}"
            )
    for key in ("history_lines", "long_docstrings", "retirement_skips"):
        total, was = sum(c[key] for c in after.values()), sum(c[key] for c in before.values())
        if total > was:
            found.append(f"tests/: {key.replace('_', ' ')} grew from {was} to {total}")
    found.extend(test_imports(head))
    base_groups = duplicate_groups(base)
    for digest, names in duplicate_groups(head).items():
        if len(names) > len(base_groups.get(digest, [])):
            found.append(f"copied setup: {', '.join(names)} share one body; keep one in tests/frame.py")
    for name in sorted(uncalled(head) - uncalled(base)):
        found.append(f"{name} is called nowhere in src/, tools/ or examples/: delete it with its tests")
    return found


def base_ref() -> str:
    return merge_base.base_ref()


def main() -> None:
    """Print every way tests/ has grown against the merge base and exit 1 where it has; nothing printed and exit 0 where the shape holds."""
    root = Path(__file__).resolve().parents[1]
    found = violations(working_tree(root), at_ref(root, base_ref()))
    print("\n".join(found) or "the shape of tests/ holds against the merge base")
    sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
