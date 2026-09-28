"""The physical modules hold integer mathematics only: no float, no `/`, no non-integer import, dtype or numpy function, and a root only in the functions ALLOWED_ROOTS names, each with its reason."""

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
    "loader/world.py": "the loop's classes built from the checked files and the load-time constants (the flight table, the labels)",
    "loader/mode.py": "the body's mode as the loader reads it: the period by the one-Node rule from the clock pair, no root",
    "loader/frame.py": "the frame of the files: the schemas the loader reads them through; no arithmetic",
    "loader/cards.py": "the cards' schemas collected from the register; no arithmetic",
    "events/detector_law.py": "the engine: the record's rows at Nodes, the six-neighbour rule, the receivers' take, the first-rung click (no law's name, ALGEBRA.md #the-primitives)",
    "events/records.py": "the records' bookkeeping the loop steps: the live record, a body's Node record, the block, the books, the runner's layer; no arithmetic",
    "events/assembly.py": "the assembly of the engine's state from the loaded world before the first interval: the detectors' map, the arrays and caches, the bodies' blocks and own records, the held families' records; integer arrays alone",
    "events/geometry.py": "the engine's geometry: the Node sets, boxes, masks and Ports of a body or a detector from the GameBoard's shape through the core's and the loader's one copy of each rule, and the pair arrays' cache",
    "events/output.py": "the engine's readings and output lines: the exact rationals of the books, the leak test, the record's click line, the books, the contents and the state stream; reads the simulation, writes the lines",
    "events/guards.py": "the engine's run-time guards bound as its methods: the start's arrays to freeze, an act's grants, a card's writes, a write applied by name, the generic act's term, start view and own record, the pace guard",
    "events/live.py": "the records' making and release: the ledger's stamps, the held records and levels, a body's own record, a planted record, a detector by name, a record's receiver, ladder and release; functions taking the engine, bound as its methods",
    "events/after_step.py": "the acts after the step the engine hooks per record: the hand's check at a click, the lifetime's end, the polariser's turn and its set's share, the polariser bodies' terms; functions taking the engine, bound as its methods",
    "events/body_language.py": "the recoil written into the body and told as one event line beside the click; integer kicks and sums, no arithmetic of its own",
    "events/record_well.py": "the well of a body with a record: its record's one interval and its form laid after it, D_i div T by the source's act through the write's line; no arithmetic of its own beyond the count",
    "events/inverse.py": "the inverse's returns: the interval's bookings at the detectors' Ports and the body's clock taken back; integer sums and differences, no arithmetic of its own",
    "events/pair.py": "the pair record of rank 2 in the loop: the two rows of one giving, the labels' clicks by their own ladders on the rows' bookings summed, the collapse to rank 1 at the first click; functions taking the engine",
    "core/rule3.py": "the one rule in one place: its coefficients at a Node from the paces, the step, its inverse and the form's term (ALGEBRA.md #the-line, #the-direction, #the-interval), and the ladder's rungs (ALGEBRA.md #the-ladder)",
    "events/primitives.py": "the primitives of the freeze (ALGEBRA.md #what-is-open): the internal representation's exact tables and the transport with its remainders, the clicks list and the momenta's share, the helicity sign",
    "core/integer.py": "the bounded integer primitives: the carry, the apportioning, the roots at load",
    "core/readings.py": "the run's readings declared in the world file and written in one format: a detector's clicks, a family's level, support and total, a body's centre, the records alive (record 2199 item 1); reads state, writes nothing into the run",
    "core/main_loop.py": "the main loop: the walk of the step file's acts through the register, the interval's frame (the clock, the deferred writes, the closing) and the run-time guards of the views, the writers and the Ports; the stages the engine's, handed in",
    "core/ports.py": "the six Ports of every Node: the arrival of an array through one Port and the six arrivals once per array per interval, the outward Ports of a mask; the one shift across Nodes of the package",
    "core/step.py": "the step file: the interval's places and the ordered names of the primitives the loop calls, one shared file with its digest ",
    "core/register.py": "the register of primitives: one name to one function, found by the features' folders, each with its place, word, reads, writes and order (records 2212 and 2221; issue #1154)",
    "core/primitive.py": "the interface of a primitive: the term of the files, the interval's start, the primitive's own record, its writes; apply(term, start, own) -> writes (records 2212 and 2221; issue #1154)",
    "core/schema.py": "the kinds of a value of the files and one generic check that refuses by name; a folder's schema on its card in the register (record 2226; ALGEBRA.md #the-primitives)",
    "core/game_board.py": "the GameBoard's addresses, the six headings, the cube's group of 48",
}

FORBIDDEN_IMPORTS = {"random", "fractions", "decimal", "cmath", "statistics"}
MATH_ALLOWED = {"gcd", "isqrt"}
NUMPY_DTYPES_ALLOWED = {"int64"}
NUMPY_DTYPES_FORBIDDEN = {
    "int8",
    "int16",
    "int32",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "float16",
    "float32",
    "float64",
    "float128",
    "floating",
    "float_",
    "complex64",
    "complex128",
    "complexfloating",
    "complex_",
}
NUMPY_FORBIDDEN = {
    "sqrt",
    "mean",
    "float",
    "true_divide",
    "divide",
    "exp",
    "log",
    "sin",
    "cos",
    "tan",
    "average",
    "std",
    "var",
    "cbrt",
    "power",
    "log2",
    "log10",
    "arctan2",
    "hypot",
}
BUILTIN_DTYPES_ALLOWED = {"bool", "object", "int"}
ROOT_NAMES = {"isqrt", "integer_root"}

# Every root in the physical modules today, by (module, function), with its
# reason; `None` is the module level. The set found must equal this set.
ALLOWED_ROOTS: dict[tuple[str, str | None], str] = {
    # empty: no physical module takes a root today (docs/CANCELLED_WORLDS.md)
}


def physical_sources() -> dict[str, str]:
    return {name: (SRC / name).read_text(encoding="utf-8") for name in PHYSICAL_MODULES}


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
    return [
        token.start[0]
        for token in tokenize.generate_tokens(io.StringIO(source).readline)
        if token.type == tokenize.OP and token.string in ("/", "/=")
    ]


def forbidden_imports(tree: ast.AST) -> list[str]:
    """Every forbidden import, and every alias of `math`, `isqrt` or `integer_root` (an alias would hide a root from `roots`, so aliasing them is itself a violation)."""
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
NUMPY_CHAIN_FORBIDDEN = {
    "linalg",
    "linspace",
    "logspace",
    "geomspace",
    "fft",
    "random",
    "polyfit",
    "interp",
    "polynomial",
}
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
    """Every `np.<chain>` that names a forbidden dtype, a function that leaves the integers or a forbidden family (`np.linalg.*`, `np.linspace`, `np.random.*`, `np.fft.*`, `np.polyfit`, `np.interp`); every allocation `np.zeros`, `np.ones`, `np.empty`, `np.full` without a `dtype` keyword (float64 by default) and every `np.array` of a non-integer literal; every call of the builtin `float`; every method call `.mean`, `.std`, `.var`; every `dtype=` or `.astype(...)` argument that is not `np.int64`, `bool`, `object`, `int` or the name `dtype` (a variable carrying one)."""
    found = []
    for node in ast.walk(tree):
        chain = numpy_chain(node) if isinstance(node, ast.Attribute) else None
        if chain:
            head = chain[0]
            if (
                head in NUMPY_DTYPES_FORBIDDEN
                or head in NUMPY_FORBIDDEN
                or head in NUMPY_CHAIN_FORBIDDEN
            ):
                found.append(f"np.{'.'.join(chain)} at line {node.lineno}")
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        keywords = {k.arg for k in node.keywords}
        if isinstance(callee, ast.Name) and callee.id == "float":
            found.append(f"float() at line {node.lineno}")
        if isinstance(callee, ast.Attribute):
            if callee.attr in METHODS_FORBIDDEN:
                found.append(f".{callee.attr}() at line {node.lineno}")
            call_chain = numpy_chain(callee)
            if call_chain and len(call_chain) == 1:
                if call_chain[0] in ALLOCATIONS_NEEDING_DTYPE and "dtype" not in keywords:
                    found.append(f"np.{call_chain[0]} without dtype at line {node.lineno}")
                if (
                    call_chain[0] in ("array", "asarray")
                    and node.args
                    and not is_integer_literal(node.args[0])
                ):
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


def root_aliases(tree: ast.AST) -> tuple[set[str], set[str]]:
    """The local names bound to `isqrt` or `integer_root` (with or without an alias) and the local names of the `math` module."""
    names: set[str] = set()
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "math":
                    modules.add(alias.asname or "math")
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in ROOT_NAMES:
                    names.add(alias.asname or alias.name)
    return names | ROOT_NAMES, modules | {"math"}


def roots(tree: ast.AST) -> set[tuple[str | None, int]]:
    """Every call of `isqrt` or `integer_root`, under any alias, with its enclosing function."""
    names, modules = root_aliases(tree)
    found: set[tuple[str | None, int]] = set()

    def walk(node: ast.AST, function: str | None) -> None:
        for child in ast.iter_child_nodes(node):
            inner = (
                child.name if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) else function
            )
            if isinstance(child, ast.Call):
                callee = child.func
                if isinstance(callee, ast.Name) and callee.id in names:
                    found.add((inner, child.lineno))
                elif (
                    isinstance(callee, ast.Attribute)
                    and callee.attr in ROOT_NAMES
                    and (not isinstance(callee.value, ast.Name) or callee.value.id in modules)
                ):
                    found.add((inner, child.lineno))
            walk(child, inner)

    walk(tree, None)
    return found


@pytest.mark.parametrize("name", sorted(PHYSICAL_MODULES))
def test_a_physical_module_holds_integer_mathematics_only(name: str) -> None:
    source = (SRC / name).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert float_literals(source) == [], (name, float_literals(source))
    assert true_divisions(source) == [], (name, true_divisions(source))
    assert forbidden_imports(tree) == [], (name, forbidden_imports(tree))
    assert numpy_violations(tree) == [], (name, numpy_violations(tree))


def test_every_root_is_listed_with_its_reason_and_the_list_is_the_inventory() -> None:
    found = {
        (name, function)
        for name, source in physical_sources().items()
        for function, _ in roots(ast.parse(source))
    }
    listed = set(ALLOWED_ROOTS)
    assert found - listed == set(), f"a root outside the list: {sorted(found - listed, key=str)}"
    assert listed - found == set(), f"a listed root no longer there: {sorted(listed - found, key=str)}"
    for key, reason in ALLOWED_ROOTS.items():
        assert reason.startswith(("at load", "AT RUN TIME", "a predicate", "the integer square root")), (
            key
        )


def features_modules() -> list[str]:
    """Every feature's module, found by its folder (no list to keep: record 2221 (3))."""
    return sorted(path.relative_to(SRC).as_posix() for path in (SRC / "features").glob("*/__init__.py"))


@pytest.mark.parametrize("name", features_modules())
def test_a_feature_holds_integer_mathematics_only(name: str) -> None:
    """A feature's folder is a physical module under the same gate as the engine's (issue #1154 cut 2), found by its folder and never listed."""
    source = (SRC / name).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert float_literals(source) == [], (name, float_literals(source))
    assert true_divisions(source) == [], (name, true_divisions(source))
    assert forbidden_imports(tree) == [], (name, forbidden_imports(tree))
    assert numpy_violations(tree) == [], (name, numpy_violations(tree))


def test_the_module_list_names_every_module_that_runs_a_step() -> None:
    """Every module of `events/`, `core/` and `loader/` but the package markers is a physical module here, so a new one cannot escape the gate unnamed."""
    modules = {
        path.relative_to(SRC).as_posix()
        for folder in ("events", "core", "loader")
        for path in (SRC / folder).glob("*.py")
        if path.name not in ("__init__.py", "run.py")
    }
    assert modules == set(PHYSICAL_MODULES), sorted(modules ^ set(PHYSICAL_MODULES))


@pytest.mark.parametrize(
    "source,checker",
    [
        ("x = 1.5\n", lambda s, t: float_literals(s)),
        ("x = 3 / 2\n", lambda s, t: true_divisions(s)),
        ("x /= 2\n", lambda s, t: true_divisions(s)),
        ("import random\n", lambda s, t: forbidden_imports(t)),
        ("from math import sqrt\n", lambda s, t: forbidden_imports(t)),
        ("import math\ny = math.sqrt(4)\n", lambda s, t: forbidden_imports(t)),
        ("import numpy as np\ny = np.sqrt(x)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.zeros(3, dtype=np.float64)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = x.astype(np.int32)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.zeros(3, dtype=float)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.zeros(3)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.full(3, 0)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.array([1.5, 2])\n", lambda s, t: numpy_violations(t)),
        ("y = float(x)\n", lambda s, t: numpy_violations(t)),
        ("y = x.mean()\n", lambda s, t: numpy_violations(t)),
        ("y = x.astype(scale)\n", lambda s, t: numpy_violations(t)),
        ("y = x.astype(dtype)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.linalg.norm(x)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.linspace(0, 1, 3)\n", lambda s, t: numpy_violations(t)),
        ("import numpy as np\ny = np.random.default_rng()\n", lambda s, t: numpy_violations(t)),
        ("import math as m\n", lambda s, t: forbidden_imports(t)),
        ("from math import isqrt as r\n", lambda s, t: forbidden_imports(t)),
    ],
)
def test_the_gate_catches_each_violation(source: str, checker) -> None:
    assert checker(source, ast.parse(source)) != []


def test_the_gate_passes_integer_numpy_and_the_carry() -> None:
    source = (
        "import numpy as np\nimport math\n"
        "x = np.zeros(3, dtype=np.int64)\nm = np.ones(3, dtype=bool)\no = np.full(2, None, dtype=object)\n"
        "y = 7 // 2\ng = math.gcd(6, 4)\nh = 0x1F\nk = np.arange(4)\nr = np.array([1, -2, 3])\nz = x.astype(object)\n"
    )
    tree = ast.parse(source)
    assert float_literals(source) == [] and true_divisions(source) == []
    assert forbidden_imports(tree) == [] and numpy_violations(tree) == []


def test_a_root_outside_the_list_is_found_with_its_function() -> None:
    source = "import math\ndef wall(x):\n    return math.isqrt(x)\n"
    assert roots(ast.parse(source)) == {("wall", 3)}


@pytest.mark.parametrize(
    "source",
    [
        "from math import isqrt as r\ndef wall(x):\n    return r(x)\n",
        "import math as m\ndef wall(x):\n    return m.isqrt(x)\n",
        "from event_universe.core.integer import integer_root as ir\ndef wall(x):\n    return ir(x)\n",
    ],
)
def test_a_root_under_an_alias_is_still_found(source: str) -> None:
    assert roots(ast.parse(source)) == {("wall", 3)}
