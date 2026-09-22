"""The algebra gate: the physical modules hold integer mathematics only
(the model owner's word of 2026-09-22, record 920: the whole GameBoard is
algebra and the clicks' implementation is algebra; no code that is not
integer mathematics on the GameBoard and the clicks; the Boss's order to
the Register Architect of the same day). The six verbs of the law
(Highlights 5.4, "The six operations") act on integers; a root is the
seventh verb, outside the law (record 249), admitted only where this test
lists it by function, with its reason.

The gate reads the source as tokens and as a syntax tree, never running
a world, and asserts on every physical module: (a) no float literal token;
(b) no `/` operator token (only `//`); (c) no import of `random`,
`fractions`, `decimal`, `cmath` or `statistics`, and of `math` only its
integer functions `gcd` and `isqrt`; (d) every numpy dtype named is
`int64`, `bool` or `object` (no `float*`, `complex*`, `floating`, no
narrower integer); (e) none of numpy's functions that leave the integers
(`sqrt`, `mean`, `float`, `true_divide`, `divide`, `exp`, `log`, `sin`,
`cos`, `tan`, `average`, `std`, `var`); (f) a root (`math.isqrt` or
`core.integer.integer_root`) only in the functions ALLOWED_ROOTS names,
exactly those: a root that appears anywhere else fails, and a root that
leaves a listed function fails too, so that the list is always the
inventory. The reasons distinguish a rounding at load (a table constant,
docs/designs/vector_form/LAW.md section 6), a predicate (a perfect-square
test, no rounded number enters a reading) and a root at run time (the
seventh verb, named in docs/designs/register_paper_sources/NODE_ALGEBRA.md
section 2, pending the owner's word). The self-tests at the end write
sources with one violation each and show the gate catches them.
"""

from __future__ import annotations

import ast
import io
import tokenize
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "event_universe"

# The physical modules: every module that runs a physical step of the
# interval or forms the tables it reads, one line each why.
PHYSICAL_MODULES: dict[str, str] = {
    "events/nature_beam.py": "the Node's interval: the walk, the collision, the click's plan, the release, the border, the merge",
    "events/meeting.py": "the meeting under its key: the crowd's flow, the arc permutation, the norm",
    "events/engine.py": "the frame of the interval: the clocks, the drive, the books, the readings",
    "events/world.py": "the world file's parse and the load-time constants (the flight table, the labels)",
    "events/measured.py": "the measured event's record and the ledger of an interval",
    "events/amplitude.py": "the click's ledger: the offer, the evaluation, the Gram form, the rungs",
    "core/integer.py": "the bounded integer primitives: the carry, the apportioning, the roots at load",
    "core/phase.py": "the phase circle and its cosine and sine tables in bounded integers",
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
    (
        "events/nature_beam.py",
        "unit_label",
    ): "at load: the unit vector u_D rounded to the nearest integer vector",
    (
        "events/nature_beam.py",
        "direction_flight",
    ): "at load: the flight table's resolution T_D = isqrt(3 |D|^2 Q^2), a declared rounding",
    (
        "events/nature_beam.py",
        "flight_triple",
    ): "at load: a massive family's E'_D = isqrt(E'_0^2 + 3 p_D . p_D) per direction, a declared rounding",
    (
        "events/nature_beam.py",
        "unit_energies",
    ): "at load: the per-direction energies of the flight triple, the same rounding",
    (
        "events/nature_beam.py",
        "momentum_pair",
    ): "AT RUN TIME under the key `optical`: the pushed row's wall isqrt((R^2 + 3 |P|^2) Q^2); the seventh verb, NODE_ALGEBRA.md section 2, the owner's word pending",
    ("events/meeting.py", "arc_shift"): "at load: the bound of the arc table from the momentum bound",
    (
        "events/meeting.py",
        "meet",
    ): "AT RUN TIME under the key `meeting`: the norm of the crowd's target |t| = isqrt(t . t); the seventh verb named in LAW.md 4.3",
    (
        "events/engine.py",
        "__init__",
    ): "at load: E' = integer_root(W) once under `covariant_readings`, the declared rounding of DERIVATIONS_BEAM 17.6 M3; comparisons from then on",
    (
        "events/amplitude.py",
        "common_denominator",
    ): "a predicate at a join of two multiplicities: is the ratio a perfect square (the root squared back and compared); no rounded number enters a reading",
    ("events/world.py", None): "at load: T_HEADING = isqrt(3 Q^2), the flight's resolution on a heading",
    (
        "events/world.py",
        "body_weight",
    ): "at load: E' of a body's declared momentum under `optical`, a declared rounding",
    ("events/world.py", "scaled_label"): "at load: the label's rounding k(|a|) to the momentum scale",
    ("events/world.py", "column_scales"): "at load: the parser's refusal names the bound's root",
    ("events/world.py", "flight_bound"): "at load: the flight table's T_D for the parser's bound",
    ("events/world.py", "_covariant"): "at load: the covariant identity's E' from the declared square",
    (
        "events/world.py",
        "_same_class",
    ): "a predicate at load: is the product a perfect square (the same class of T_D)",
    (
        "events/world.py",
        "_massive_families",
    ): "at load: the parser's refusal names the largest admitted momentum",
}


def physical_sources() -> dict[str, str]:
    return {name: (SRC / name).read_text(encoding="utf-8") for name in PHYSICAL_MODULES}


def float_literals(source: str) -> list[int]:
    """The lines of every float literal token (a decimal point or an
    exponent outside a hexadecimal literal)."""
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
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                    found.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            if module in FORBIDDEN_IMPORTS:
                found.append(node.module or "")
            if module == "math":
                found.extend(f"math.{a.name}" for a in node.names if a.name not in MATH_ALLOWED)
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "math" and node.attr not in MATH_ALLOWED:
                found.append(f"math.{node.attr}")
    return found


def numpy_violations(tree: ast.AST) -> list[str]:
    """Every `np.<name>` that names a forbidden dtype or a function that
    leaves the integers, and every `dtype=` or `astype(...)` argument that
    is not `np.int64`, `bool`, `object` or a variable."""
    found = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "np"
        ):
            if node.attr in NUMPY_DTYPES_FORBIDDEN or node.attr in NUMPY_FORBIDDEN:
                found.append(f"np.{node.attr} at line {node.lineno}")
        if isinstance(node, ast.Call):
            arguments = [k.value for k in node.keywords if k.arg == "dtype"]
            if isinstance(node.func, ast.Attribute) and node.func.attr == "astype":
                arguments.extend(node.args[:1])
            for value in arguments:
                if isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name):
                    if value.value.id == "np" and value.attr not in NUMPY_DTYPES_ALLOWED:
                        found.append(f"dtype np.{value.attr} at line {node.lineno}")
                elif isinstance(value, ast.Name):
                    if value.id not in BUILTIN_DTYPES_ALLOWED and value.id != "dtype":
                        found.append(f"dtype {value.id} at line {node.lineno}")
                elif isinstance(value, ast.Constant):
                    if value.value not in ("int64", "bool", "object"):
                        found.append(f"dtype {value.value!r} at line {node.lineno}")
    return found


def roots(tree: ast.AST) -> set[tuple[str | None, int]]:
    """Every call of `isqrt` or `integer_root` with its enclosing function."""
    found: set[tuple[str | None, int]] = set()

    def walk(node: ast.AST, function: str | None) -> None:
        for child in ast.iter_child_nodes(node):
            inner = (
                child.name if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) else function
            )
            if isinstance(child, ast.Call):
                callee = child.func
                name = callee.attr if isinstance(callee, ast.Attribute) else getattr(callee, "id", "")
                if name in ROOT_NAMES:
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


def test_the_module_list_names_every_module_that_runs_a_step() -> None:
    """Every module of `events/` and `core/` but the package markers is a
    physical module here, so a new one cannot escape the gate unnamed."""
    modules = {
        path.relative_to(SRC).as_posix()
        for folder in ("events", "core")
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
    ],
)
def test_the_gate_catches_each_violation(source: str, checker) -> None:
    assert checker(source, ast.parse(source)) != []


def test_the_gate_passes_integer_numpy_and_the_carry() -> None:
    source = (
        "import numpy as np\nimport math\n"
        "x = np.zeros(3, dtype=np.int64)\nm = np.ones(3, dtype=bool)\no = np.full(2, None, dtype=object)\n"
        "y = 7 // 2\ng = math.gcd(6, 4)\nh = 0x1F\n"
    )
    tree = ast.parse(source)
    assert float_literals(source) == [] and true_divisions(source) == []
    assert forbidden_imports(tree) == [] and numpy_violations(tree) == []


def test_a_root_outside_the_list_is_found_with_its_function() -> None:
    source = "import math\ndef wall(x):\n    return math.isqrt(x)\n"
    assert roots(ast.parse(source)) == {("wall", 3)}
