"""The physical modules hold integer mathematics only: no float, no `/`, no non-integer import, dtype or numpy function; the root left everywhere (tests/test_rule3.py holds that gate)."""

from __future__ import annotations

import ast
import io
import tokenize
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "event_universe"

# The physical modules: every module that runs a physical step of the interval or forms the tables it reads, one line each why.
PHYSICAL_MODULES: dict[str, str] = {
    "node.py": "the Node: every family's NodeState and the interval's acts on whole-board arrays, each a call of Rule3",
    "game_board.py": "the GameBoard: the NodeStates, the bodies and the detectors, the interval forward and back",
    "share.py": "the share: the count as the record's reading at every Node, in quanta over the count's wall by Rule3's division act",
    "reports.py": "the detectors' reports, the net inflow through a region's front boundary, and a body's Nodes derived for a report, readings of whole-board arrays",
    "growth.py": "the receding face: the GameBoard grown by layers of zeros as the front reaches it, taken off on the way back",
    "world_files.py": "the host's read of the world's files and their digest; no arithmetic",
    "loader/world.py": "the world's files checked into the GameBoard's world: the keys, the bodies, the messages and the detectors",
    "loader/keys.py": "the keys of the files: an object, an integer, a Node on the board, a range along an axis",
    "loader/mode.py": "the generator's mode file: every body's and message's levels within the amplitude bound and 0 beyond the board",
    "loader/faces.py": "the inner faces of the board: the Nodes declared beyond it, read as 0 through every Port",
    "loader/messages.py": "the messages, laid records of a family of quanta: their keys and their levels from the mode file",
    "loader/derived.py": "the families from the rule and the amplitude bound A derived from the width",
    "core/rule3.py": "the one rule in one place: its coefficients at a Node from the paces, the step in both directions, the division act, its fixed point iterated and the form's term (ALGEBRA.md #the-line, #the-direction)",
    "core/integer.py": "the working bound, the host's signed integer range",
    "core/ports.py": "the six Ports of every Node: the arrival of an array through one Port, the one shift across Nodes of the package",
}

FORBIDDEN_IMPORTS = {"random", "fractions", "decimal", "cmath", "statistics"}
MATH_ALLOWED, NUMPY_DTYPES_ALLOWED = {"gcd", "isqrt"}, {"int64"}
NUMPY_DTYPES_FORBIDDEN = {
    *"complex128 complex64 complex_ complexfloating float128 float16 float32 float64 float_ floating int16 int32 int8 uint16 uint32 uint64 uint8".split()
}
NUMPY_FORBIDDEN = {
    *"arctan2 average cbrt cos divide exp float hypot log log10 log2 mean power sin sqrt std tan true_divide var".split()
}
BUILTIN_DTYPES_ALLOWED = {"bool", "object", "int", "kind"}  # kind: the loader's choice by the width
ROOT_NAMES = {"isqrt", "integer_root"}


def float_literals(source: str) -> list[int]:
    """The lines of every float literal token (a decimal point or an exponent outside a hexadecimal literal)."""
    found = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.NUMBER:
            continue
        text = token.string.lower()
        if text.startswith(("0x", "0o", "0b")):
            continue
        if "." in text or "e" in text or text.endswith("j"):
            found.append(token.start[0])
    return found


def true_divisions(source: str) -> list[int]:
    """The lines of every `/` operator token (`//` is one token, `//=` another)."""
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return [t.start[0] for t in tokens if t.type == tokenize.OP and t.string in ("/", "/=")]


def forbidden_imports(tree: ast.AST) -> list[str]:
    """Every forbidden import, and every alias of `math`, `isqrt` or `integer_root` (an alias would hide a root, so aliasing them is itself a violation)."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                    found.append(alias.name)
                if alias.name == "math" and alias.asname not in (None, "math"):
                    found.append(f"math aliased as {alias.asname}")
        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            if module in FORBIDDEN_IMPORTS:
                found.append(node.module or "")
            if module == "math":
                found.extend(f"math.{a.name}" for a in node.names if a.name not in MATH_ALLOWED)
            for alias in node.names:
                if alias.name in ROOT_NAMES and alias.asname not in (None, alias.name):
                    found.append(f"{alias.name} aliased as {alias.asname}")
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "math" and node.attr not in MATH_ALLOWED:
                found.append(f"math.{node.attr}")
    return found


ALLOCATIONS_NEEDING_DTYPE = {"zeros", "ones", "empty", "full"}
NUMPY_CHAINS = {*"fft geomspace interp linalg linspace logspace polyfit polynomial random".split()}
METHODS_FORBIDDEN = {"mean", "std", "var"}


def numpy_chain(node: ast.AST) -> list[str] | None:
    """The attribute chain of an expression rooted at the name `np` (`np.linalg.norm` -> ["linalg", "norm"]), None when not rooted there."""
    chain: list[str] = []
    while isinstance(node, ast.Attribute):
        chain.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name) and node.id == "np":
        return list(reversed(chain))
    return None


def is_integer_literal(node: ast.AST) -> bool:
    """A literal that is an integer or a (nested) list or tuple of integers and booleans; anything else (a float, a string, a name) is not."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, bool)) and not isinstance(node.value, float)
    if isinstance(node, (ast.List, ast.Tuple)):
        return all(is_integer_literal(item) for item in node.elts)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        return is_integer_literal(node.operand)
    return True  # a name or a call: judged where it is made


def numpy_violations(tree: ast.AST) -> list[str]:
    """Every `np.<chain>` that names a forbidden dtype, a function that leaves the integers or a forbidden family (`np.linalg.*`, `np.linspace`, `np.random.*`, `np.fft.*`, `np.polyfit`, `np.interp`); every allocation `np.zeros`, `np.ones`, `np.empty`, `np.full` without a `dtype` keyword (float64 by default) and every `np.array` of a non-integer literal; every call of the builtin `float`; every method call `.mean`, `.std`, `.var`; every `dtype=` or `.astype(...)` argument that is not `np.int64` (the loader's one site), `bool`, `object`, `int` or the name `kind` (the loader's choice of the integers by the file's width)."""
    found = []
    for node in ast.walk(tree):
        chain = numpy_chain(node) if isinstance(node, ast.Attribute) else None
        if chain:
            head = chain[0]
            if head in NUMPY_DTYPES_FORBIDDEN or head in NUMPY_FORBIDDEN or head in NUMPY_CHAINS:
                found.append(f"np.{'.'.join(chain)} at line {node.lineno}")
        if not isinstance(node, ast.Call):
            continue
        callee, keywords = node.func, {k.arg for k in node.keywords}
        if isinstance(callee, ast.Name) and callee.id == "float":
            found.append(f"float() at line {node.lineno}")
        if isinstance(callee, ast.Attribute):
            if callee.attr in METHODS_FORBIDDEN:
                found.append(f".{callee.attr}() at line {node.lineno}")
            call_chain = numpy_chain(callee)
            if call_chain and len(call_chain) == 1:
                if call_chain[0] in ALLOCATIONS_NEEDING_DTYPE and "dtype" not in keywords:
                    found.append(f"np.{call_chain[0]} without dtype at line {node.lineno}")
                arrays = call_chain[0] in ("array", "asarray") and node.args
                if arrays and not is_integer_literal(node.args[0]):
                    found.append(f"np.{call_chain[0]} of a non-integer literal at line {node.lineno}")
        arguments = [k.value for k in node.keywords if k.arg == "dtype"]
        if isinstance(callee, ast.Attribute) and callee.attr == "astype":
            arguments.extend(node.args[:1])
        for value in arguments:
            if isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name):
                if value.value.id == "np" and value.attr not in NUMPY_DTYPES_ALLOWED:
                    found.append(f"dtype np.{value.attr} at line {node.lineno}")
            elif isinstance(value, ast.Name):
                if value.id not in BUILTIN_DTYPES_ALLOWED:
                    found.append(f"dtype {value.id} at line {node.lineno}")
            elif isinstance(value, ast.Constant):
                if value.value not in ("int64", "bool", "object"):
                    found.append(f"dtype {value.value!r} at line {node.lineno}")
            else:
                found.append(f"dtype of an unnamed form at line {node.lineno}")
    return found


def features_modules() -> list[str]:
    """Every feature's module, found by its folder (no list to keep: record 2221 (3))."""
    return sorted(path.relative_to(SRC).as_posix() for path in (SRC / "features").glob("*/__init__.py"))


@pytest.mark.parametrize("name", sorted(PHYSICAL_MODULES) + features_modules())
def test_a_physical_module_holds_integer_mathematics_only(name: str) -> None:
    """Every physical module, and every feature's folder under the same gate (issue #1154 cut 2), found by its folder and never listed."""
    source = (SRC / name).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert float_literals(source) == [], (name, float_literals(source))
    assert true_divisions(source) == [], (name, true_divisions(source))
    assert forbidden_imports(tree) == [], (name, forbidden_imports(tree))
    assert numpy_violations(tree) == [], (name, numpy_violations(tree))


def test_the_module_list_names_every_module_that_runs_a_step() -> None:
    """Every module of the package, of `core/` and of `loader/` but the package markers is a physical module here, so a new one cannot escape the gate unnamed."""
    files = [path for folder in (SRC, SRC / "core", SRC / "loader") for path in folder.glob("*.py")]
    modules = {path.relative_to(SRC).as_posix() for path in files if path.name != "__init__.py"}
    assert modules == set(PHYSICAL_MODULES), sorted(modules ^ set(PHYSICAL_MODULES))


SOURCE_CHECKS = {"x = 1.5\n": float_literals, "x = 3 / 2\n": true_divisions, "x /= 2\n": true_divisions}
IMPORT_CHECKS = ("import random\n", "from math import sqrt\n", "import math\ny = math.sqrt(4)\n")
IMPORT_CHECKS += ("import math as m\n", "from math import isqrt as r\n")
NUMPY_CHECKS = ("y = np.sqrt(x)\n", "y = np.zeros(3, dtype=np.float64)\n", "y = x.astype(np.int32)\n")
NUMPY_CHECKS += ("y = np.zeros(3, dtype=float)\n", "y = np.zeros(3)\n", "y = np.full(3, 0)\n")
NUMPY_CHECKS += ("y = np.array([1.5, 2])\n", "y = float(x)\n", "y = x.mean()\n", "y = x.astype(scale)\n")
NUMPY_CHECKS += ("y = x.astype(dtype)\n", "y = np.linalg.norm(x)\n", "y = np.linspace(0, 1, 3)\n")
NUMPY_CHECKS += ("y = np.random.default_rng()\n",)


def test_the_gate_catches_each_violation() -> None:
    """Every float literal, true division, forbidden import and numpy departure from the integers is caught."""
    assert all(checker(source) != [] for source, checker in SOURCE_CHECKS.items())
    assert all(forbidden_imports(ast.parse(source)) != [] for source in IMPORT_CHECKS)
    assert all(numpy_violations(ast.parse("import numpy as np\n" + text)) for text in NUMPY_CHECKS)


def test_the_gate_passes_integer_numpy_and_the_carry() -> None:
    source = (
        "import numpy as np\nimport math\nx = np.zeros(3, dtype=np.int64)\nm = np.ones(3, dtype=bool)\n"
    )
    source += "o = np.full(2, None, dtype=object)\ny = 7 // 2\ng = math.gcd(6, 4)\nh = 0x1F\nk = np.arange(4)\n"
    source += "r = np.array([1, -2, 3])\nz = x.astype(object)\n"
    tree = ast.parse(source)
    assert float_literals(source) == [] and true_divisions(source) == []
    assert forbidden_imports(tree) == [] and numpy_violations(tree) == []
