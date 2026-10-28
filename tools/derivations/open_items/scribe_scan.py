"""Sofer's gate on every package under src: the owner's rules as a script that refuses a push.

The owner's words of 2026-10-28, 04:3x, 04:5x and 05:0x UTC: no number in the code, whole numbers only, no cosine, sine or
circularity that makes a phenomenon happen, no state beyond the Node-clock; "your laws should be in scripts, so that they cannot
push at all what breaks our lawfulness, and let it be logical and smart".

How it decides. A push may not raise the count of any rule's hits, at any (rule, file, detail), above the same file's at the push's
merge base: what stands at the base stands, a new hit is a REFUSAL (BLOCK) or a NOTE (WARN) by the rule's tier. A hit leaves the list
by being removed and enters it only by the owner's word (scribe_scan_allowed.json, written by Sofer on that word, with the
row of the ledger that holds it). The key of a hit holds no line number, so a moved or reformatted line is no new hit.

  python scribe_scan.py                        the working tree against its merge base (CHECK_BASE, else origin/engine-5.0-test)
  python scribe_scan.py TREE [--base REV]      TREE a directory or a git revision; the base a revision
  python scribe_scan.py --patch FILE           the patch applied on the base in a scratch worktree, then the same check
  python scribe_scan.py TREE --baseline FILE   the tree against the list of departures that stand (Sofer's audit of the whole)
  python scribe_scan.py TREE --all [--summary] every hit of the tree, by rule and file (--summary: the counts only)
  python scribe_scan.py --write-baseline FILE  [TREE]  the tree's hits written as the list that stands
  python scribe_scan.py --rules                the rules, their tiers and the law each one keeps
  python scribe_scan.py --install              the git pre-push hook of this clone
  python scribe_scan.py --hook                 git's pre-push call (the refs on stdin); --claude-hook: Claude Code's call before `git push`

Exit status 1 on a refusal, 0 otherwise (2: the call itself is wrong). Read with the repository's own interpreter, Python 3.14
(venv314/bin/python); an older one runs the script again under it.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import keyword
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import tokenize
from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from typing import Any

PACKAGE = "src/event_universe"
TESTS = "tests"
SCOPES = ("src", TESTS)  # every package under src, and the tests for the rule PIN alone
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASELINE = HERE / "scribe_scan_baseline.json"
ALLOWED = HERE / "scribe_scan_allowed.json"
BASES = ("origin/engine-5.0-test", "origin/main")
PUBLISHED = "origin/scribe-5"  # where the owner's approvals stand, written by Sofer alone
# the gate's own files: a push that changes one needs the owner's word, and says so
OWN = (
    "tools/derivations/open_items/scribe_scan.py",
    "tools/derivations/open_items/scribe_scan_selftest.py",
    "tools/derivations/open_items/scribe_scan_allowed.json",
    "tools/derivations/open_items/scribe_scan_baseline.json",
    ".claude/settings.json",
)

# rule: (tier, the line the refusal prints with the law it keeps)
RULES: dict[str, tuple[str, str]] = {
    "NUMBER": (
        "BLOCK",
        "a number beyond 0 and 1: numbers stand in the world, universe and setting files (law: No number in the code)",
    ),
    "FLOAT": (
        "BLOCK",
        "a float, a true division, round() or pow(): whole numbers only (law: No float anywhere in the system)",
    ),
    "IMPORT": (
        "BLOCK",
        "math, random, fractions, decimal, statistics, scipy, sympy: integers and Rule3 only (law: No float anywhere)",
    ),
    "DTYPE": (
        "BLOCK",
        "a numpy constructor with no dtype makes a float (law: No float anywhere in the system)",
    ),
    "CIRCLE": (
        "BLOCK",
        "a cosine, sine, tangent, pi or other circular function (law: No circularity that makes a phenomenon happen)",
    ),
    "ROOT": (
        "BLOCK",
        "a call of an integer root, the integer sine by search: no new call (law: No circularity that makes a phenomenon happen)",
    ),
    "WORD": (
        "BLOCK",
        "a circular word in a name (cosine, sine, angle, theta, circle, quaternion ...): an angle or circle used as a rule",
    ),
    "TEXT": (
        "WARN",
        "a circular word in a string, docstring or comment: read it, a rotation or a closed form may be described there",
    ),
    "STATE": (
        "BLOCK",
        "state outside a Node-clock: a module-level container, a global, an id() key (law: Locality is never broken)",
    ),
    "MEMO": (
        "WARN",
        "a module-level cache is state beyond the Node-clock: only a pure function of integers may stand so, and say it",
    ),
    "TABLE": (
        "BLOCK",
        "a typed table of integers in the code (a quarter turn, a singlet): a world's data stands in the world file",
    ),
    "MIX": (
        "BLOCK",
        "a tuple of bilinear sums: a rotation or hypercomplex product by a setting outside Rule3 (law: No circularity ...)",
    ),
    "LOGREAD": (
        "BLOCK",
        "an act reads the great clock's log, a global read: only the readers read the record (law: Locality is never broken)",
    ),
    "LOOP": (
        "BLOCK",
        "a loop (for, while, a comprehension, map, filter, reduce, itertools, np.vectorize, a function that calls itself) in an engine module: no loop that makes a formula, the machine is one tensor operation (the owner's words of 2026-10-28, 06:5x and 09:0x); the count per file and kind may not rise",
    ),
    "OPERATION": (
        "BLOCK",
        "a power, a shift, an exclusive or, or a floor division or remainder outside the carry's home (core/acts.py, core/rule3.py): the step does multiplication, addition and Rule3 alone (the owner's word of 2026-10-28, 09:0x)",
    ),
    "REFUSE": (
        "BLOCK",
        "a raise in an engine module: a refusal by name is a rule written for a phenomenon (the exclusion's refusals were such); the count per file may not rise (the owner's word of 2026-10-28, 09:0x: no declarations)",
    ),
    "CLAMP": (
        "BLOCK",
        "min, max, abs, clip or where in an engine module: a bound or a branch written as a clamp, where the step does multiplication, addition and Rule3 alone (the owner's word of 2026-10-28, 08:0x, through David)",
    ),
    "PIN": (
        "WARN",
        "an assert against an integer beyond 0 and 1 in a test: a pinned value is a verdict the code wrote; the plan's tests read properties and two independent readings (the count per file may not rise)",
    ),
    "COMPARE": (
        "WARN",
        "an ordering comparison in an engine module: a threshold read by order and not as the quotient of a carry (the same word); the count may not rise",
    ),
    "ISOLATE": (
        "BLOCK",
        "an import that crosses the new engine's folders: the decoder and the record import the standard library and the record alone (no numpy, no engine, no runner), the engine imports neither the decoder nor the runner nor the current engine, the runner neither the decoder nor the current engine; a judge that runs the defendant's code cannot catch it (the owner's word of 2026-10-28, 10:1x: the decoder out of the engine)",
    ),
    "BRANCH": (
        "WARN",
        "a branch (if, a conditional expression, match) in an engine module: the law says there is no if on a train (The Node-clock and the Mesh are generic; there is no if) and a whether is the indicator 1 - 1 div (q + 1) of a carry's quotient; a branch the formula does not hold is a declaration (the count per file may not rise)",
    ),
}

BAD_IMPORTS = frozenset("math cmath statistics random fractions decimal scipy sympy mpmath".split())
NUMPY_NAMES = frozenset({"np", "numpy"})
NP_FLOAT = frozenset(
    "sqrt cbrt exp expm1 log log2 log10 log1p mean average median std var linspace logspace fft linalg random e inf nan "
    "float16 float32 float64 float_ double true_divide divide power complex_ complex64 complex128 complex256 csingle cdouble "
    "clongdouble floor ceil trunc rint around round fix".split()
)
CIRCULAR_FUNCTIONS = frozenset(
    "cos sin tan acos asin atan atan2 arccos arcsin arctan arctan2 sinh cosh tanh radians degrees deg2rad rad2deg "
    "hypot unwrap angle".split()
)
ROOTS = frozenset("largest_below isqrt integer_root sqrt cbrt sine_rim".split())
CLAMPS = frozenset(
    "min max abs clip where minimum maximum absolute fmin fmax sign select piecewise choose heaviside copysign".split()
)
ORDERING = (ast.Lt, ast.LtE, ast.Gt, ast.GtE)
FOREIGN_OPERATORS = {ast.Pow: "**", ast.LShift: "<<", ast.RShift: ">>", ast.BitXor: "^"}
OPERATION_CALLS = frozenset(
    "divmod floor_divide remainder mod fmod left_shift right_shift bitwise_xor floordiv lshift rshift xor".split()
)  # the foreign operations under their function names (np.mod, operator.xor ...)
ITERATING_BARE = frozenset(
    "map filter iter reduce accumulate starmap vectorize permutations combinations groupby".split()
)
ITERATING_MODULES = {
    "itertools": frozenset(
        "product permutations combinations combinations_with_replacement groupby accumulate starmap takewhile dropwhile".split()
    ),
    "functools": frozenset({"reduce"}),
}  # a loop under a function's name (the comprehension rule's dodges)
ITERATING_NUMPY = frozenset("vectorize apply_along_axis apply_over_axes fromfunction frompyfunc".split())
NEW_ENGINE = "tensor24"  # the new engine's package under src (Tensor24's section 31): four folders, each gated by its own rules
STRICT = (
    NEW_ENGINE + "/engine/",
    NEW_ENGINE + "/record/",
)  # a note of PROMOTED is a refusal here: it starts at 0 and stays
PROMOTED = frozenset({"COMPARE", "BRANCH", "MEMO"})
READER_FOLDERS = (
    NEW_ENGINE + "/runner/",
    NEW_ENGINE + "/decoder/",
)  # the readers' exemptions, by folder
CARRY_HOME = frozenset(
    {"core/acts.py", "core/rule3.py", NEW_ENGINE + "/engine/carry.py"}
)  # where Rule3's division and remainder are written
COMPARE_CALLS = frozenset(
    "lt le gt ge less greater less_equal greater_equal sorted sort argsort lexsort partition searchsorted isclose "
    "bisect bisect_left bisect_right insort heappush heappop nlargest nsmallest".split()
)  # a comparison under a function's name, in the new engine
NEEDS_DTYPE_NEW = frozenset(
    "array asarray arange fromiter".split()
)  # an array of Python integers needs its dtype, in the new engine
NEEDS_DTYPE = frozenset("zeros ones empty full eye identity linspace".split())
CIRCULAR_WORDS = frozenset(
    "cos sin tan cosine sine tangent arccos arcsin arctan atan atan2 acos asin theta angle angles radian radians degree "
    "degrees circle circles circular quaternion quaternions trig trigonometric sinusoid sinusoidal tsirelson lorentz "
    "planck coulomb pi".split()
)
BORN = re.compile(r"\bBorn\b")
SHOWN = 40  # the hits a refusal prints, the rest counted
CONTAINERS = frozenset("dict list set defaultdict OrderedDict Counter deque".split())
MUTATORS = frozenset(
    "append extend insert pop remove clear update setdefault add discard popitem sort reverse".split()
)
MEMOS = frozenset({"cache", "lru_cache", "cached_property"})
# the modules that read a finished chart and run no step (Sofer's audit of 2026-10-28): they may read the log
READERS = frozenset(
    "run.py gates.py predicates.py reckoner.py rim.py swings.py great_clock.py strikes.py clicks.py events.py "
    "symmetries.py phenomena.py".split()
)


def is_reader(rel: str) -> bool:
    """A module that reads a finished chart or record and runs no step: by name in the current engine, by folder in the new."""
    return rel in READERS or rel.startswith(READER_FOLDERS)


TEXT_TOKENS = {tokenize.STRING, tokenize.COMMENT}
if hasattr(tokenize, "FSTRING_MIDDLE"):
    TEXT_TOKENS.add(tokenize.FSTRING_MIDDLE)


@dataclass(frozen=True)
class Hit:
    """One hit of one rule: its key holds no line, so a moved line is the same hit."""

    rule: str
    rel: str
    line: int
    detail: str
    where: str = ""
    col: int = 0  # keeps two hits of one kind on one line apart; not part of the key

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.rule, self.rel, self.detail)

    @property
    def tier(self) -> str:
        tier = RULES[self.rule][0]
        return (
            "BLOCK" if tier == "WARN" and self.rule in PROMOTED and self.rel.startswith(STRICT) else tier
        )


def words_of(text: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return [w.lower() for w in re.findall(r"[A-Za-z]+", spaced)]


def integer_leaves(node: ast.AST) -> list[int] | None:
    """The integers of a literal tuple or list of integers (nested, signed); None where a leaf is not one."""
    if isinstance(node, ast.Tuple | ast.List):
        found: list[int] = []
        for element in node.elts:
            leaves = integer_leaves(element)
            if leaves is None:
                return None
            found += leaves
        return found
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub | ast.UAdd):
        return integer_leaves(node.operand)
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, int)
        and not isinstance(node.value, bool)
    ):
        return [node.value]
    return None


def products(node: ast.AST) -> int:
    return sum(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult) for n in ast.walk(node))


def sums(node: ast.AST) -> bool:
    return any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add | ast.Sub) for n in ast.walk(node))


def callee_name(call: ast.Call) -> str:
    f = call.func
    return f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ""


def imported_names(rel: str, node: ast.Import | ast.ImportFrom) -> list[str]:
    """The full dotted names an import brings in; a relative import is resolved from the module's own folder."""
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    parts = rel.split("/")[:-1]
    base = (parts[: len(parts) - (node.level - 1)] if node.level else []) + (
        node.module.split(".") if node.module else []
    )
    stem = ".".join(base)
    return [stem if alias.name == "*" else f"{stem}.{alias.name}" for alias in node.names]


def import_ok(rel: str, name: str) -> bool:
    """Whether a module of the new engine may import `name` (the folders' walls; other modules import freely)."""
    top = name.split(".")[0]
    own = NEW_ENGINE + "."
    if rel.startswith(NEW_ENGINE + "/decoder/"):
        return (
            top in sys.stdlib_module_names
            or name == NEW_ENGINE + ".record"
            or name.startswith((own + "record.", own + "decoder"))
        )
    if rel.startswith(NEW_ENGINE + "/record/"):
        return top in sys.stdlib_module_names or name.startswith(own + "record")
    if rel.startswith(NEW_ENGINE + "/engine/"):
        return not (name.startswith((own + "decoder", own + "runner")) or top == "event_universe")
    if rel.startswith(NEW_ENGINE + "/runner/"):
        return not (name.startswith(own + "decoder") or top == "event_universe")
    return True


def scan(rel: str, source: str) -> list[Hit]:
    """Every hit of every rule in one module (rel: its path inside src/event_universe, another package's under its name; a test's under tests/, the rule PIN alone)."""
    tree = ast.parse(source)
    if rel.startswith(TESTS + "/"):
        return [
            Hit("PIN", rel, node.lineno, "assert", "", node.col_offset)
            for node in ast.walk(tree)
            if isinstance(node, ast.Assert)
            and any(
                isinstance(c, ast.Constant)
                and isinstance(c.value, int | float)
                and not isinstance(c.value, bool)
                and c.value not in (0, 1)
                for c in ast.walk(node.test)
            )
        ]
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    hits: list[Hit] = []

    def where(node: ast.AST) -> str:
        names: list[str] = []
        cursor: ast.AST | None = node
        while cursor is not None:
            if isinstance(cursor, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                names.append(cursor.name)
            cursor = parents.get(cursor)
        return ".".join(reversed(names)) or "<module>"

    def add(rule: str, node: ast.AST, detail: str) -> None:
        hits.append(
            Hit(
                rule,
                rel,
                getattr(node, "lineno", 0),
                detail,
                where(node),
                getattr(node, "col_offset", 0),
            )
        )

    numpy = set(NUMPY_NAMES)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            numpy |= {a.asname or a.name for a in node.names if a.name == "numpy"}
        if isinstance(node, ast.Import | ast.ImportFrom):
            for name in imported_names(rel, node):
                if not import_ok(rel, name):
                    add("ISOLATE", node, name)
    module_containers: dict[str, ast.stmt] = {}
    for stmt in tree.body:
        value = stmt.value if isinstance(stmt, ast.Assign | ast.AnnAssign) else None
        targets = (
            stmt.targets
            if isinstance(stmt, ast.Assign)
            else [stmt.target]
            if isinstance(stmt, ast.AnnAssign)
            else []
        )
        names = [t.id for t in targets if isinstance(t, ast.Name)]
        if value is None or not names:
            continue
        literal = isinstance(
            value, ast.Dict | ast.List | ast.Set | ast.DictComp | ast.ListComp | ast.SetComp
        )
        built = isinstance(value, ast.Call) and callee_name(value) in CONTAINERS
        if literal or built:
            emptied = (
                (isinstance(value, ast.Dict) and not value.keys)
                or (isinstance(value, ast.List | ast.Set) and not value.elts)
                or (isinstance(value, ast.Call) and not value.args and not value.keywords)
            )
            for name in names:
                module_containers[name] = stmt
                if emptied:
                    add("STATE", stmt, f"module-level container {name}")
        if isinstance(value, ast.Call) and callee_name(value) in MEMOS:
            add("MEMO", stmt, f"{names[0]} = {callee_name(value)}(...)")

    written: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            add("STATE", node, "global " + ", ".join(node.names))
            written |= set(node.names)
        elif isinstance(node, ast.Assign | ast.AugAssign | ast.Delete):
            for target in node.targets if isinstance(node, ast.Assign | ast.Delete) else [node.target]:
                base = (
                    target.value
                    if isinstance(target, ast.Subscript)
                    else target
                    if isinstance(node, ast.AugAssign)
                    else None
                )
                if isinstance(base, ast.Name):
                    written.add(base.id)
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in MUTATORS
        ):
            if isinstance(node.func.value, ast.Name):
                written.add(node.func.value.id)
    for name, stmt in module_containers.items():
        if name in written and not any(
            h.rule == "STATE" and h.detail == f"module-level container {name}" for h in hits
        ):
            add("STATE", stmt, f"module-level container {name}")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in BAD_IMPORTS:
                    add("IMPORT", node, alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.split(".")[0] in BAD_IMPORTS:
                add("IMPORT", node, module)
            if module.split(".")[0] in numpy:
                for alias in node.names:
                    rule = (
                        "CIRCLE"
                        if alias.name in CIRCULAR_FUNCTIONS | {"pi"}
                        else "FLOAT"
                        if alias.name in NP_FLOAT
                        else ""
                    )
                    if rule:
                        add(rule, node, f"numpy.{alias.name}")
        elif isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, int | float | complex) and not isinstance(value, bool):
                if isinstance(value, float | complex):
                    add("FLOAT", node, f"literal {value!r}")
                if value not in (0, 1):
                    add("NUMBER", node, repr(value))
        elif isinstance(node, ast.BinOp | ast.AugAssign) and isinstance(node.op, ast.Div):
            add("FLOAT", node, "true division")
        elif (
            isinstance(node, ast.BinOp | ast.AugAssign)
            and not is_reader(rel)
            and (
                type(node.op) in FOREIGN_OPERATORS
                or (isinstance(node.op, ast.FloorDiv | ast.Mod) and rel not in CARRY_HOME)
            )
        ):
            add(
                "OPERATION",
                node,
                FOREIGN_OPERATORS.get(type(node.op), "//" if isinstance(node.op, ast.FloorDiv) else "%"),
            )
        elif isinstance(node, ast.Raise) and not is_reader(rel):
            add("REFUSE", node, "raise")
        elif isinstance(node, ast.Call):
            name = callee_name(node)
            if isinstance(node.func, ast.Name) and name in {"round", "complex", "pow"}:
                add("FLOAT", node, f"{name}()")
            if rel not in CARRY_HOME and not is_reader(rel) and name in OPERATION_CALLS:
                spelt = (
                    isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and (node.func.value.id in numpy or node.func.value.id == "operator")
                )
                if name == "divmod" or spelt:
                    add("OPERATION", node, name if name == "divmod" else f"{name}()")
            if not is_reader(rel):
                module = (
                    node.func.value.id
                    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                    else ""
                )
                if (
                    (isinstance(node.func, ast.Name) and name in ITERATING_BARE)
                    or name in ITERATING_MODULES.get(module, frozenset())
                    or (module in numpy and name in ITERATING_NUMPY)
                ):
                    add("LOOP", node, "call")
                if isinstance(node.func, ast.Name):
                    cursor: ast.AST | None = parents.get(node)
                    while cursor is not None and not isinstance(
                        cursor, ast.FunctionDef | ast.AsyncFunctionDef
                    ):
                        cursor = parents.get(cursor)
                    if (
                        isinstance(cursor, ast.FunctionDef | ast.AsyncFunctionDef)
                        and cursor.name == name
                        and not isinstance(parents.get(cursor), ast.ClassDef)
                    ):
                        add("LOOP", node, "recursion")
            if isinstance(node.func, ast.Name) and name == "id":
                add("STATE", node, "id()")
            if name in ROOTS:
                add("ROOT", node, name)
            if name in CLAMPS and not is_reader(rel):
                add("CLAMP", node, f"{name}()")
            if rel.startswith(NEW_ENGINE + "/") and not is_reader(rel) and name in COMPARE_CALLS:
                add("COMPARE", node, "call")
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if (
                    node.func.value.id in numpy
                    and (
                        name in NEEDS_DTYPE
                        or (name in NEEDS_DTYPE_NEW and rel.startswith(NEW_ENGINE + "/"))
                    )
                    and not any(k.arg == "dtype" for k in node.keywords)
                ):
                    add("DTYPE", node, f"np.{name}")
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id in numpy:
                if node.attr in NP_FLOAT:
                    add("FLOAT", node, f"np.{node.attr}")
                if node.attr in CIRCULAR_FUNCTIONS or node.attr == "pi":
                    add("CIRCLE", node, f"np.{node.attr}")
            if node.attr == "log" and isinstance(node.ctx, ast.Load) and not is_reader(rel):
                above = parents.get(node)
                call = parents.get(above) if above is not None else None
                appends = (
                    isinstance(above, ast.Attribute)
                    and above.attr in MUTATORS
                    and isinstance(call, ast.Call)
                )
                if not appends:
                    add("LOGREAD", node, "log read")
        elif isinstance(node, ast.Name):
            if node.id in {"float", "complex"}:
                add("FLOAT", node, node.id)
            if node.id in CIRCULAR_FUNCTIONS or node.id == "pi":
                add("CIRCLE", node, node.id)
        elif isinstance(
            node,
            ast.For
            | ast.AsyncFor
            | ast.While
            | ast.ListComp
            | ast.SetComp
            | ast.DictComp
            | ast.GeneratorExp,
        ) and not is_reader(rel):
            add(
                "LOOP",
                node,
                "for"
                if isinstance(node, ast.For | ast.AsyncFor)
                else "while"
                if isinstance(node, ast.While)
                else "comprehension",
            )
        elif (
            isinstance(node, ast.Compare)
            and not is_reader(rel)
            and any(isinstance(op, ORDERING) for op in node.ops)
        ):
            add("COMPARE", node, "ordering")
        elif isinstance(node, ast.If | ast.IfExp | ast.Match) and not is_reader(rel):
            guard = (
                isinstance(node, ast.If)
                and isinstance(node.test, ast.Name)
                and node.test.id == "TYPE_CHECKING"
            )
            if not guard:
                add(
                    "BRANCH",
                    node,
                    "if"
                    if isinstance(node, ast.If)
                    else "match"
                    if isinstance(node, ast.Match)
                    else "ternary",
                )
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            for decorator in node.decorator_list:
                found = (
                    callee_name(decorator)
                    if isinstance(decorator, ast.Call)
                    else (
                        decorator.id
                        if isinstance(decorator, ast.Name)
                        else decorator.attr
                        if isinstance(decorator, ast.Attribute)
                        else ""
                    )
                )
                if found in MEMOS:
                    add("MEMO", node, f"@{found} {node.name}")
        if isinstance(node, ast.Tuple | ast.List):
            above = parents.get(node)
            indexing = isinstance(above, ast.Subscript) and above.slice is node
            if not indexing and not isinstance(above, ast.Tuple | ast.List):
                leaves = integer_leaves(node)
                if leaves is not None and len(leaves) >= 3 and any(leaves):
                    add("TABLE", node, "table " + ast.unparse(node)[:48])
            if isinstance(node, ast.Tuple) and not indexing and len(node.elts) >= 3:
                if all(products(e) >= 2 and sums(e) for e in node.elts):
                    add("MIX", node, f"{len(node.elts)} bilinear sums")

    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type == tokenize.NAME and not keyword.iskeyword(token.string):
                if any(w in CIRCULAR_WORDS for w in words_of(token.string)):
                    hits.append(Hit("WORD", rel, token.start[0], token.string))
            elif token.type in TEXT_TOKENS:
                found_words = sorted({w for w in words_of(token.string) if w in CIRCULAR_WORDS})
                if BORN.search(token.string):
                    found_words.append("Born")
                if found_words:
                    hits.append(Hit("TEXT", rel, token.start[0], "/".join(found_words)))
    except tokenize.TokenError:
        pass
    return sorted(set(hits), key=lambda h: (h.rel, h.line, h.rule, h.detail))


def git(repo: Path, *args: str, stdin: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, input=stdin, check=False)


def resolve(repo: Path, rev: str) -> str | None:
    found = git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    return found.stdout.decode().strip() if found.returncode == 0 else None


def rel_of(path: str) -> str:
    """A file's key path: inside src/event_universe as it was, another package under its own name, a test under tests/."""
    for prefix in (PACKAGE + "/", "src/"):
        if path.startswith(prefix):
            return path[len(prefix) :]
    return path


def sources_at(repo: Path, rev: str) -> dict[str, str]:
    """The modules of every package under src and the tests at a revision, read from git without a checkout."""
    listing = git(repo, "ls-tree", "-r", "--name-only", rev, "--", *SCOPES).stdout.decode().split("\n")
    paths = [p for p in listing if p.endswith(".py")]
    if not paths:
        return {}
    payload = git(
        repo, "cat-file", "--batch", stdin="".join(f"{rev}:{p}\n" for p in paths).encode()
    ).stdout
    stream = io.BytesIO(payload)
    found: dict[str, str] = {}
    for path in paths:
        _oid, _kind, size = stream.readline().split()
        found[rel_of(path)] = stream.read(int(size)).decode("utf-8")
        stream.read(1)
    return found


def sources_in(root: Path) -> dict[str, str]:
    return {
        rel_of(p.relative_to(root).as_posix()): p.read_text(encoding="utf-8")
        for scope in SCOPES
        if (root / scope).is_dir()
        for p in sorted((root / scope).rglob("*.py"))
    }


def hits_of(sources: dict[str, str]) -> list[Hit]:
    found: list[Hit] = []
    for rel, text in sorted(sources.items()):
        try:
            found += scan(rel, text)
        except SyntaxError as error:
            raise SystemExit(
                f"the gate cannot parse {rel}: {error} (read it with venv314/bin/python)"
            ) from None
    return found


def standing(path: Path) -> Counter[tuple[str, str, str]]:
    """A list of hits that stands: 'RULE|file|detail' per line, a repeat a count."""
    if not path.is_file():
        return Counter()
    keys = [tuple(k.split("|", 2)) for k in json.loads(path.read_text(encoding="utf-8"))]
    return Counter((r, f, d) for r, f, d in keys)


def allowance(repo: Path = REPO) -> Counter[tuple[str, str, str]]:
    """What the owner's word lets stand: entries {rule, file, detail, count, word, row}, read from Sofer's published branch
    (origin/scribe-5), so that a push cannot approve itself by editing its own copy; the working file where that ref is absent."""
    relative = ALLOWED.relative_to(REPO).as_posix()
    shown = git(repo, "show", f"{PUBLISHED}:{relative}")
    if shown.returncode == 0:
        text = shown.stdout.decode()
    elif ALLOWED.is_file():
        text = ALLOWED.read_text(encoding="utf-8")
    else:
        return Counter()
    held: Counter[tuple[str, str, str]] = Counter()
    for entry in json.loads(text):
        held[(entry["rule"], entry["file"], entry["detail"])] += int(entry.get("count", 1))
    return held


def above(now: Iterable[Hit], stands: Counter[tuple[str, str, str]]) -> list[Hit]:
    """The hits above what stands at their key (the last by line), less what the owner's word allows."""
    stands = stands + allowance()
    found: list[Hit] = []
    for key, group in groupby(sorted(now, key=lambda h: (h.key, h.line)), key=lambda h: h.key):
        members = list(group)
        extra = len(members) - stands.get(key, 0)
        if extra > 0:
            found += members[-extra:]
    return sorted(found, key=lambda h: (h.rel, h.line, h.rule))


def merge_base(repo: Path, base: str | None, tree_rev: str) -> tuple[str, str]:
    """The base ref (given, CHECK_BASE, else the first of BASES that resolves) and its merge base with the tree's revision."""
    names = (
        [base] if base else [os.environ["CHECK_BASE"]] if os.environ.get("CHECK_BASE") else list(BASES)
    )
    for name in names:
        commit = resolve(repo, name)
        if commit:
            found = git(repo, "merge-base", commit, tree_rev)
            if found.returncode == 0:
                return name, found.stdout.decode().strip()
    raise SystemExit(
        f"the merge base of {tree_rev[:9]} with {names} cannot be found: fetch the base or set CHECK_BASE"
    )


def moved(repo: Path, *revs: str, cached: bool = False) -> dict[str, str]:
    """The modules git reads as moved between the revisions (or the index and the revision), new path to old."""
    flags = ["diff", "-M", "--name-status", "--diff-filter=R", *(["--cached"] if cached else [])]
    listing = git(repo, *flags, *revs, "--", *SCOPES).stdout.decode().splitlines()
    found: dict[str, str] = {}
    for line in listing:
        _status, old, new = line.split("\t")
        if old.endswith(".py") and new.endswith(".py"):
            found[rel_of(new)] = rel_of(old)
    return found


def stood(hits: Iterable[Hit], moves: dict[str, str]) -> Counter[tuple[str, str, str]]:
    """The base's hits as counts per key, a moved module's under its new path (a rename is no new hit)."""
    renamed = {old: new for new, old in moves.items()}
    return Counter((h.rule, renamed.get(h.rel, h.rel), h.detail) for h in hits)


def report(label: str, new: list[Hit], base_label: str, out: Any = sys.stdout) -> int:
    """Print the refusals and the notes; 1 where a refusal stands."""
    refusals = [h for h in new if h.tier == "BLOCK"]
    notes = [h for h in new if h.tier == "WARN"]
    print(
        f"Sofer's gate: {label} against {base_label}: refusals {len(refusals)}, notes {len(notes)}",
        file=out,
    )
    for hit in (refusals + notes)[:SHOWN]:
        mark = "REFUSED" if hit.tier == "BLOCK" else "note   "
        place = f" in {hit.where}" if hit.where and hit.where != "<module>" else ""
        print(f"  {mark} {hit.rule:7s} {hit.rel}:{hit.line}{place}: {hit.detail}", file=out)
    if len(new) > SHOWN:
        print(
            f"  ... and {len(new) - SHOWN} more (scribe_scan.py TREE --base REV lists them all)",
            file=out,
        )
    for rule in sorted({h.rule for h in new}):
        print(f"  {rule}: {RULES[rule][1]}", file=out)
    if refusals:
        print(
            "  These are the owner's rules (docs/ALGEBRA.md): the push is refused and nothing was sent.\n"
            "  If a rule or a law must be broken, STOP and tell the owner, the Boss and David in the thread at once (his order of\n"
            "  2026-10-28, 04:5x UTC); only his word lets a hit stand (scribe_scan_allowed.json, written by Sofer on that word).\n"
            "  Do not weaken or go round this gate (--no-verify, an edited list or script): Sofer reads every push and reports it.",
            file=out,
        )
    return 1 if refusals else 0


def delta_line(before: list[Hit], after: list[Hit]) -> str:
    """The hits by rule from the base to the push: what falls toward the end state of 0 and what rises."""
    was, now = Counter(h.rule for h in before), Counter(h.rule for h in after)
    moved_rules = [
        f"{rule} {was[rule]} to {now[rule]}"
        for rule in sorted(set(was) | set(now))
        if was[rule] != now[rule]
    ]
    return "counts from the base: " + (", ".join(moved_rules) if moved_rules else "unchanged")


def check_revision(repo: Path, rev: str, base: str | None, out: Any = sys.stdout) -> int:
    """The tree at `rev` against its merge base: 1 on a refusal."""
    commit = resolve(repo, rev)
    if commit is None:
        print(f"the gate cannot resolve {rev}", file=out)
        return 0
    name, mb = merge_base(repo, base, commit)
    touched = git(repo, "diff", "--name-only", mb, commit, "--", *SCOPES, *OWN).stdout.decode().split()
    if not touched:
        return 0
    before, after = hits_of(sources_at(repo, mb)), hits_of(sources_at(repo, commit))
    stands = stood(before, moved(repo, mb, commit))
    new = above(after, stands)
    own = [p for p in touched if p in OWN]
    status = report(f"{commit[:9]}", new, f"its merge base {mb[:9]} with {name}", out) if new else 0
    print(f"  {delta_line(before, after)}", file=out)
    if own:
        print(
            f"  note: this push changes the gate's own files {own}: the owner's word is needed for it",
            file=out,
        )
    return status


@contextmanager
def scratch(repo: Path, commit: str) -> Iterator[Path]:
    """A detached worktree of the commit, removed after."""
    with tempfile.TemporaryDirectory() as directory:
        place = Path(directory) / "tree"
        git(repo, "worktree", "add", "--detach", str(place), commit)
        try:
            yield place
        finally:
            git(repo, "worktree", "remove", "--force", str(place))


def check_patch(repo: Path, patch: Path, base: str | None) -> int:
    name, commit = merge_base(repo, base, "HEAD") if base is None else (base, resolve(repo, base) or "")
    with scratch(repo, commit) as tree:
        applied = git(tree, "apply", "--3way", str(patch.resolve()))
        if applied.returncode != 0:
            print(f"the patch does not apply on {commit[:9]}: {applied.stderr.decode().strip()}")
            return 2
        git(tree, "add", "-A")
        before, after = hits_of(sources_at(repo, commit)), hits_of(sources_in(tree))
        stands = stood(before, moved(tree, commit, cached=True))
        new = above(after, stands)
    base_label = name if name == commit[:9] else f"{name} ({commit[:9]})"
    status = (
        report(f"the patch {patch.name}", new, base_label) if new else _clean(patch.name, base_label)
    )
    print(f"  {delta_line(before, after)}")
    return status


def _clean(label: str, base: str) -> int:
    print(f"Sofer's gate: {label} against {base}: no refusal, no note")
    return 0


def pushes(command: str, cwd: str) -> list[tuple[Path, str]]:
    """The (directory, revision) of every `git push` in a shell command line: its refspecs' sources, else HEAD."""
    found: list[tuple[Path, str]] = []
    where = Path(cwd)
    for segment in re.split(r"&&|\|\||;|\n|\|", command):
        try:
            words = shlex.split(segment)
        except ValueError:
            continue
        if words[:1] == ["cd"] and len(words) > 1:
            where = (where / words[1]) if not words[1].startswith("/") else Path(words[1])
            continue
        if words[:1] != ["git"] or "push" not in words:
            continue
        index, folder = 1, where
        while index < len(words) and words[index] != "push":
            if words[index] == "-C" and index + 1 < len(words):
                folder = (
                    (where / words[index + 1])
                    if not words[index + 1].startswith("/")
                    else Path(words[index + 1])
                )
                index += 1
            index += 1
        rest = [w for w in words[index + 1 :] if not w.startswith("-")]
        if "--delete" in words or "-d" in words:
            continue
        specs = rest[1:] or ["HEAD"]
        for spec in specs:
            source = spec.lstrip("+").split(":")[0]
            if source:
                found.append((folder, source))
    return found


def claude_hook(base: str | None) -> int:
    """Claude Code's PreToolUse call: a Bash command holding `git push` is checked before it runs; exit 2 refuses it."""
    try:
        event = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    if event.get("tool_name") != "Bash":
        return 0
    command = str(event.get("tool_input", {}).get("command", ""))
    if "git" not in command or "push" not in command:
        return 0
    refused = False
    seen: set[tuple[str, str]] = set()
    for folder, rev in pushes(command, str(event.get("cwd") or os.getcwd())):
        top = git(folder, "rev-parse", "--show-toplevel").stdout.decode().strip()
        if not top or (top, rev) in seen:
            continue
        seen.add((top, rev))
        try:
            refused |= check_revision(Path(top), rev, base, sys.stderr) == 1
        except SystemExit as error:
            print(f"the gate could not run ({error}); the push is not held by it", file=sys.stderr)
    return 2 if refused else 0


def push_hook(base: str | None) -> int:
    """Git's pre-push call: lines `<local ref> <local oid> <remote ref> <remote oid>` on stdin."""
    refused = False
    for line in sys.stdin.read().splitlines():
        parts = line.split()
        if len(parts) == 4 and set(parts[1]) != {"0"}:
            try:
                refused |= check_revision(REPO, parts[1], base, sys.stderr) == 1
            except SystemExit as error:
                print(f"the gate could not run ({error}); the push is not held by it", file=sys.stderr)
    return 1 if refused else 0


def guarded(call: Callable[[str | None], int], base: str | None) -> int:
    """A caller's run: the gate's own fault never holds a push, it says so and lets it go (Sofer's scan reads it after)."""
    try:
        return call(base)
    except (Exception, SystemExit) as error:
        print(f"Sofer's gate could not run ({error!r}); this push is not held by it", file=sys.stderr)
        return 0


def install() -> int:
    """Write .git/hooks/pre-push for this clone (a foreign hook is never overwritten)."""
    hooks = Path(git(REPO, "rev-parse", "--git-path", "hooks").stdout.decode().strip())
    hooks = hooks if hooks.is_absolute() else REPO / hooks
    target = hooks / "pre-push"
    marker = "# installed by tools/derivations/open_items/scribe_scan.py --install"
    if target.exists() and marker not in target.read_text(encoding="utf-8"):
        print(
            f'{target} exists and is not Sofer\'s: chain `python {Path(__file__).resolve()} --hook "$@"` into it by hand'
        )
        return 2
    python = REPO / "venv314" / "bin" / "python"
    interpreter = str(python) if python.is_file() else sys.executable
    hooks.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"#!/bin/sh\n{marker} (the owner, 2026-10-28, 05:0x UTC: the laws in scripts that refuse the push)\n"
        f'script="{Path(__file__).resolve()}"\n[ -f "$script" ] || exit 0\n'
        f'exec "{interpreter}" "$script" --hook "$@"\n',
        encoding="utf-8",
    )
    target.chmod(0o755)
    print(
        f"installed {target}: a push that raises a count of Sofer's rules is refused (git push --no-verify goes round it, and is reported)"
    )
    return 0


def ensure_python() -> None:
    """The tree is Python 3.14's: an older interpreter runs this script again under the repository's own."""
    if (sys.version_info.major, sys.version_info.minor) >= (3, 14):
        return
    for candidate in (str(REPO / "venv314" / "bin" / "python"), shutil.which("python3.14") or ""):
        if candidate and Path(candidate).is_file():
            os.execv(candidate, [candidate, *sys.argv])


def summary(found: list[Hit]) -> None:
    by_rule = Counter(h.rule for h in found)
    print("hits by rule:", dict(sorted(by_rule.items())))
    by_file: dict[str, Counter[str]] = {}
    for h in found:
        by_file.setdefault(h.rel, Counter())[h.rule] += 1
    for rel in sorted(by_file):
        print(f"  {rel:34s} {dict(sorted(by_file[rel].items()))}")


def main(argv: list[str]) -> int:
    ensure_python()
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "tree", nargs="?", help="a directory or a git revision (default: the working tree of this clone)"
    )
    parser.add_argument(
        "--base",
        help="the revision the merge base is taken with (default CHECK_BASE, else origin/engine-5.0-test)",
    )
    parser.add_argument(
        "--baseline",
        nargs="?",
        const=str(BASELINE),
        help="compare with the list that stands, not a merge base",
    )
    parser.add_argument(
        "--write-baseline", metavar="FILE", help="write the tree's hits as the list that stands"
    )
    parser.add_argument(
        "--patch", type=Path, help="a patch to apply on the base in a scratch worktree, then check"
    )
    parser.add_argument("--all", action="store_true", help="every hit of the tree")
    parser.add_argument("--summary", action="store_true", help="with --all: the counts only")
    parser.add_argument("--rules", action="store_true")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--hook", action="store_true")
    parser.add_argument("--claude-hook", action="store_true")
    args, extra = parser.parse_known_args(argv)  # git's pre-push call adds the remote's name and url
    if extra and not (args.hook or args.claude_hook):
        parser.error(f"unrecognized arguments: {' '.join(extra)}")
    if args.rules:
        for rule, (tier, line) in RULES.items():
            print(f"{rule:8s} {tier:5s} {line}")
        return 0
    if args.install:
        return install()
    if args.hook:
        return guarded(push_hook, args.base)
    if args.claude_hook:
        return guarded(claude_hook, args.base)
    if args.patch:
        return check_patch(REPO, args.patch, args.base)
    by_rev = bool(args.tree and not Path(args.tree).is_dir() and resolve(REPO, args.tree))
    if by_rev:
        repo, rev, sources, label = REPO, args.tree, sources_at(REPO, args.tree), args.tree
    else:
        root = Path(args.tree or REPO).resolve()
        top = git(root, "rev-parse", "--show-toplevel").stdout.decode().strip()
        repo, rev, sources, label = (
            Path(top or root),
            "HEAD",
            sources_in(root),
            str(args.tree or "the working tree"),
        )
    found = hits_of(sources)
    if args.write_baseline:
        Path(args.write_baseline).write_text(
            json.dumps(sorted("|".join(h.key) for h in found), indent=0) + "\n", encoding="utf-8"
        )
        print(f"written: {len(found)} hits in {len(sources)} modules")
        return 0
    if args.all:
        summary(found) if args.summary else [
            print(f"{h.tier:5s} {h.rule:7s} {h.rel}:{h.line}  {h.detail}") for h in found
        ]
        return 0
    if args.baseline:
        return report(
            label,
            above(found, standing(Path(args.baseline))),
            f"the list that stands ({Path(args.baseline).name})",
        )
    name, mb = merge_base(repo, args.base, rev)
    moves = moved(repo, mb, rev) if by_rev else moved(repo, mb)
    new = above(found, stood(hits_of(sources_at(repo, mb)), moves))
    return (
        report(label, new, f"its merge base {mb[:9]} with {name}")
        if new
        else _clean(label, f"its merge base {mb[:9]} with {name}")
    )


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)  # the reader of a pipe (head) closed it
