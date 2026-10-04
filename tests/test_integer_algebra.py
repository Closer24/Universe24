"""The physical modules hold integer mathematics only: no float, no `/`, no non-integer import, dtype or numpy function; the root left everywhere (tests/test_rule3.py holds that gate); and the one division act Rule3's, no raw floor division or modulo outside core/rule3.py but the named index wraps and shape divisions. PHYSICAL_MODULES names every module that runs a physical step of the interval or forms the tables it reads, each one's docstring saying why."""

import ast
import io
import random
import tokenize
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.core.rule3 import coefficients, rule3
from event_universe.features.currents import Levels, Neighbours, current, tension
from event_universe.features.read import link_tension

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "event_universe"

PHYSICAL_MODULES = ("node.py", "game_board.py", "share.py", "reports.py", "credit.py", "world_files.py")
PHYSICAL_MODULES += ("records.py", "bookings.py", "meeting.py", "conversion.py", "front.py", "plane.py")
PHYSICAL_MODULES += ("giving.py", "lay.py")
PHYSICAL_MODULES += ("growth.py", "core/rule3.py", "core/integer.py", "core/paces.py", "core/ports.py")
PHYSICAL_MODULES += tuple(f"loader/{m}.py" for m in ("world", "keys", "mode", "faces", "messages"))
PHYSICAL_MODULES += ("loader/derived.py", "loader/draw.py", "loader/universe.py", "loader/lay.py")
PHYSICAL_MODULES += ("resonance.py", "node_reader.py", "loader/node_reader_rows.py")
PHYSICAL_MODULES += ("loader/node_reader_declaration.py",)

FORBIDDEN_IMPORTS = {"random", "fractions", "decimal", "cmath", "statistics"}
MATH_ALLOWED, NUMPY_DTYPES_ALLOWED = {"gcd", "isqrt"}, {"int64"}
FLOATS = "complex128 complex64 complex_ complexfloating float128 float16 float32 float64 float_ floating"
NUMPY_DTYPES_FORBIDDEN = {*FLOATS.split(), *"int16 int32 int8 uint16 uint32 uint64 uint8".split()}
NUMPY_FORBIDDEN = set("arctan2 average cbrt cos divide exp float hypot log log10 log2 mean".split())
NUMPY_FORBIDDEN |= set("power sin sqrt std tan true_divide var".split())
BUILTIN_DTYPES_ALLOWED = {"bool", "object", "int", "kind"}  # kind: the loader's choice by the width
ROOT_NAMES = {"isqrt", "integer_root"}


def float_literals(source: str) -> list[int]:
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    numbers = [(t.start[0], t.string.lower()) for t in tokens if t.type == tokenize.NUMBER]
    decimal = [(line, text) for line, text in numbers if not text.startswith(("0x", "0o", "0b"))]
    return [line for line, text in decimal if "." in text or "e" in text or text.endswith("j")]


def true_divisions(source: str) -> list[int]:
    """The lines of every `/` operator token (`//` is one token, `//=` another)."""
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    return [t.start[0] for t in tokens if t.type == tokenize.OP and t.string in ("/", "/=")]


def forbidden_imports(tree: ast.AST) -> list[str]:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import | ast.ImportFrom):
            aliased = [a for a in node.names if a.asname not in (None, a.name)]
        if isinstance(node, ast.Import):
            found += [a.name for a in node.names if a.name.split(".")[0] in FORBIDDEN_IMPORTS]
            found += [f"math aliased as {a.asname}" for a in aliased if a.name == "math"]
        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            found += [node.module or ""] * (module in FORBIDDEN_IMPORTS)
            if module == "math":
                found += [f"math.{a.name}" for a in node.names if a.name not in MATH_ALLOWED]
            found += [f"{a.name} aliased as {a.asname}" for a in aliased if a.name in ROOT_NAMES]
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            found += [f"math.{node.attr}"] * (node.value.id == "math" and node.attr not in MATH_ALLOWED)
    return found


ALLOCATIONS_NEEDING_DTYPE = {"zeros", "ones", "empty", "full"}
NUMPY_CHAINS = {*"fft geomspace interp linalg linspace logspace polyfit polynomial random".split()}
METHODS_FORBIDDEN = {"mean", "std", "var"}


def numpy_chain(node: ast.AST) -> list[str] | None:
    chain: list[str] = []
    while isinstance(node, ast.Attribute):
        chain, node = [node.attr, *chain], node.value
    return chain if isinstance(node, ast.Name) and node.id == "np" else None


def is_integer_literal(node: ast.AST) -> bool:
    """A literal that is an integer or a (nested) list or tuple of integers and booleans."""
    if isinstance(node, (ast.List, ast.Tuple)):
        return all(is_integer_literal(item) for item in node.elts)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        return is_integer_literal(node.operand)
    return not isinstance(node, ast.Constant) or isinstance(node.value, (int, bool))  # a name, a call


def numpy_violations(tree: ast.AST) -> list[str]:
    found = []
    for node in ast.walk(tree):
        chain = numpy_chain(node) if isinstance(node, ast.Attribute) else None
        if chain and chain[0] in NUMPY_DTYPES_FORBIDDEN | NUMPY_FORBIDDEN | NUMPY_CHAINS:
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


FEATURES = sorted(p.relative_to(SRC).as_posix() for p in (SRC / "features").glob("*/__init__.py"))


@pytest.mark.parametrize("name", sorted(PHYSICAL_MODULES) + FEATURES)
def test_a_physical_module_holds_integer_mathematics_only(name: str) -> None:
    """Every physical module, and every feature's folder under the same gate (issue #1154 cut 2), found by its folder and never listed."""
    tree = ast.parse(source := (SRC / name).read_text(encoding="utf-8"))
    assert float_literals(source) == [], (name, float_literals(source))
    assert true_divisions(source) == [], (name, true_divisions(source))
    assert forbidden_imports(tree) == [], (name, forbidden_imports(tree))
    assert numpy_violations(tree) == [], (name, numpy_violations(tree))


def test_the_module_list_names_every_module_that_runs_a_step() -> None:
    """Every module of the package, of `core/` and of `loader/` but the package markers is a physical module here, so a new one cannot escape the gate unnamed. Every float literal, true division, forbidden import and numpy departure from the integers is caught; integer numpy, the carry, the greatest common divisor and a hexadecimal literal pass."""
    files = [path for folder in (SRC, SRC / "core", SRC / "loader") for path in folder.glob("*.py")]
    modules = {path.relative_to(SRC).as_posix() for path in files if path.name != "__init__.py"}
    assert modules == set(PHYSICAL_MODULES), sorted(modules ^ set(PHYSICAL_MODULES))
    SOURCES = {"x = 1.5\n": float_literals, "x = 3 / 2\n": true_divisions, "x /= 2\n": true_divisions}
    IMPORT_CHECKS = ("import random\n", "from math import sqrt\n", "import math\ny = math.sqrt(4)\n")
    IMPORT_CHECKS += ("import math as m\n", "from math import isqrt as r\n")
    NUMPY_CHECKS = ("y = np.sqrt(x)\n", "y = np.zeros(3, dtype=np.float64)\n", "y = x.mean()\n")
    NUMPY_CHECKS += ("y = np.zeros(3, dtype=float)\n", "y = np.zeros(3)\n", "y = np.full(3, 0)\n")
    NUMPY_CHECKS += ("y = np.array([1.5, 2])\n", "y = float(x)\n", "y = x.astype(np.int32)\n")
    NUMPY_CHECKS += ("y = x.astype(dtype)\n", "y = np.linalg.norm(x)\n", "y = np.linspace(0, 1, 3)\n")
    NUMPY_CHECKS += ("y = np.random.default_rng()\n", "y = x.astype(scale)\n")
    PASSING = "import numpy as np\nimport math\nx = np.zeros(3, dtype=np.int64)\no = np.full(2, None, dtype=object)\n"
    PASSING += "y = 7 // 2\ng = math.gcd(6, 4)\nh = 0x1F\nk = np.arange(4)\nr = np.array([1, -2, 3])\nz = x.astype(object)\nm = np.ones(3, dtype=bool)\n"
    assert all(checker(source) != [] for source, checker in SOURCES.items())
    assert all(forbidden_imports(ast.parse(source)) != [] for source in IMPORT_CHECKS)
    assert all(numpy_violations(ast.parse("import numpy as np\n" + text)) for text in NUMPY_CHECKS)
    assert float_literals(PASSING) == [] and true_divisions(PASSING) == []
    assert forbidden_imports(tree := ast.parse(PASSING)) == [] and numpy_violations(tree) == []


RULE3, DIVISIONS = "core/rule3.py", {ast.FloorDiv, ast.Mod}


def literal_products(tree: ast.AST) -> list[int]:
    """Every product, sum, difference or power of two integer literals (`2 * 2`, `1 + 3`, `2 ** 10`), by line: a number composed in the engine and named nowhere."""
    return [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp)
        and all(isinstance(x, ast.Constant) and type(x.value) is int for x in (node.left, node.right))
    ]


def test_a_composed_product_of_literals_is_refused_outside_core_rule3() -> None:
    """No number in the engine (the owner's word of 2026-10-03, "where there are numbers, throw them out or close them"; PR D): outside core/rule3.py no two integer literals are multiplied, added, subtracted or raised to each other, since the product would be a number the engine should take from a name of the Ports and the levels or from the run's files; Rule3's own 2, 3, 6 and 12 stand in its home."""
    offenders = [
        f"{path.relative_to(SRC).as_posix()}:{line}"
        for path in sorted(SRC.rglob("*.py"))
        if path.relative_to(SRC).as_posix() != RULE3
        for line in literal_products(ast.parse(path.read_text(encoding="utf-8")))
    ]
    assert offenders == [], offenders
    assert literal_products(ast.parse("x = 2 * 2\ny = 1 + 3\nz = 2**10\n")) == [1, 2, 3]
    assert literal_products(ast.parse("x = 2 * a\ny = -3\nz = (1, 2)\n")) == []


DIVISION_CALLS = {"divmod", "np.floor_divide", "np.mod", "np.remainder", "np.fmod"}
INDEX_ARITHMETIC = (  # the named exceptions: the module, the operator, the function, its responsibility
    ("core/ports.py", ast.Mod, "shifted", "the periodic wrap of a Node's index along the shifted axis"),
    ("loader/faces.py", ast.Mod, "connected", "the periodic wrap of a walked neighbour's coordinate"),
    ("growth.py", ast.Mod, "reached", "a line's number against the family's width, a part's first line"),
    ("growth.py", ast.Mod, "resized", "a line's number against the family's width, a part's first line"),
    ("loader/derived.py", ast.FloorDiv, "width", "a row's lines over its parts and records, exact"),
    ("loader/derived.py", ast.FloorDiv, "planes", "a part's width over the plane's two lines, exact"),
)


def divisions(tree: ast.AST) -> list[tuple[int, type[ast.AST], str]]:
    """Every raw division of a module, its line, its operator's kind and the enclosing function's name: `//` and `%` in an expression or an augmented assignment, and the calls `divmod` and numpy's floor division and remainder (DIVISION_CALLS), counted as a floor division."""
    functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    spans = [(n.lineno, n.end_lineno or n.lineno, n.name) for n in functions]
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp | ast.AugAssign) and type(node.op) in DIVISIONS:
            kind = type(node.op)
        elif isinstance(node, ast.Call) and ast.unparse(node.func) in DIVISION_CALLS:
            kind = ast.FloorDiv
        else:
            continue
        inner = [span for span in spans if span[0] <= node.lineno <= span[1]]
        found.append((node.lineno, kind, max(inner)[2] if inner else ""))
    return found


def test_floor_division_and_modulo_are_refused_outside_core_rule3() -> None:
    """The arithmetic of the engine is Rule3's division act (`division_forward` and its fixed point in core/rule3.py; ALGEBRA.md #the-four-acts): a raw floor division or modulo on a number of the law is refused in every other module of the engine (`//`, `%`, their augmented forms, `divmod`, numpy's floor division and remainder), and the index wraps and the row's shape divisions are the named exceptions (INDEX_ARITHMETIC, each by module, operator and function, no level, share, count or pace among them), refused in turn when one no longer stands in the code."""
    allowed = {(name, kind, function) for name, kind, function, _reason in INDEX_ARITHMETIC}
    standing, offenders = set(), []
    for path in sorted(p for p in SRC.rglob("*.py") if p.relative_to(SRC).as_posix() != RULE3):
        name, source = path.relative_to(SRC).as_posix(), path.read_text(encoding="utf-8")
        for line, kind, function in divisions(ast.parse(source)):
            if (name, kind, function) in allowed:
                standing.add((name, kind, function))
            else:
                offenders.append(f"{name}:{line} {function}: {source.splitlines()[line - 1].strip()}")
    assert offenders == [], offenders
    assert standing == allowed, sorted(allowed - standing)
    assert divisions(ast.parse((SRC / RULE3).read_text(encoding="utf-8"))), "the act's home divides"
    REFUSED = ("x = a // b\n", "x %= b\n", "q, r = divmod(a, b)\n", "y = np.floor_divide(a, b)\n")
    assert all(divisions(ast.parse(text)) for text in (*REFUSED, "y = np.mod(a, b)\n", "x = a % b\n"))
    assert divisions(ast.parse("x = a * b + c\ny = np.pad(a, w)\n")) == []


def ring_step(now, before, carry, reads, self_coefficient, wall):  # type: ignore[no-untyped-def]
    """One interval of Rule3 on a ring folded to one axis: the two axis neighbours read, the four folded Ports read the Node itself."""
    n = len(now)
    nexts, carries = [], []
    for i in range(n):
        arrivals = (now[(i + 1) % n], now[(i - 1) % n], now[i], now[i], now[i], now[i])
        value, rest = rule3(reads, arrivals, self_coefficient, wall, now[i], before[i], carry[i])
        nexts.append(int(value))
        carries.append(int(rest))
    return nexts, carries


def two_level_form(a, b, reads, self_coefficient, wall):  # type: ignore[no-untyped-def]
    """Q(a, b) = SUM_i (a_i^2 + b_i^2) - (1 / w) SUM_i (SUM_j R_ij a_j + S a_i) b_i at uniform paces (row 7 of the conventions)."""
    n = len(a)
    total = Fraction(0)
    for i in range(n):
        linked = (
            reads[0] * (a[(i + 1) % n] + a[(i - 1) % n])
            + sum(reads[2:]) * a[i]
            + self_coefficient * a[i]
        )
        total += a[i] * a[i] + b[i] * b[i] - Fraction(linked * b[i], wall)
    return total


def momentum(num, now, before):  # type: ignore[no-untyped-def]
    """P_a(i) = (F_(i, i-a) - F_(i, i+a)) / num on the ring, F_ij = num (now_i before_j - before_i now_j) (row 5 of the conventions)."""
    n = len(now)
    flux = [
        current(num, Levels(now[i], before[i]), Levels(now[(i + d) % n], before[(i + d) % n]))
        for i in range(n)
        for d in (-1, 1)
    ]
    return [Fraction(flux[2 * i] - flux[2 * i + 1], num) for i in range(n)]


def test_the_conventions_tables_identities_hold_on_small_integers() -> None:
    """Rows 5 to 8 of the conventions table (ALGEBRA.md, The conventions and the units) on small integers at the toy pair [2, 3]: (5) the momentum identity with the carried remainders, w [P_a(t+1) - P_a(t)] = R [G(i) - G(i-1)] - [delta_i Delta now_i - now_i Delta delta_i], delta = r - r', on a nine-Node ring, every Node of forty random states; (6) the Node's own tension on the axis wave [2, 0, -2, 0] is +4 x the weight at every Node and the Link's reading the mean of its two ends, their sum the Link's booking; (7) with the rounding the two-level form Q walks by SUM epsilon_i (next_i - before_i) and the three-level form E_3 by SUM [epsilon_i(t) next_i - epsilon_i(t+1) now_i], epsilon = (r - r') / w, exactly; (8) the weighted coefficients R_ij / p_i^2 are the same from both ends of a Link at different paces, D M symmetric."""
    num, den, gamma, ring = 2, 3, 20, 9
    wave = [2, 0, -2, 0]
    for i in range(4):
        n = Neighbours(now=wave[i], ahead=wave[(i + 1) % 4], behind=wave[(i - 1) % 4])
        assert tension(1, n) == 4 and tension(3, n) == 12
    assert (
        link_tension([(1, 4, 4)]) == 4
    )  # the mean of the two ends' parts, their sum 8 the Link's booking
    reads, self_coefficient, wall = coefficients(num, den, gamma, gamma, gamma)
    draw = random.Random(24)
    for _ in range(40):
        before = [draw.randint(-50, 50) for _ in range(ring)]
        now = [draw.randint(-50, 50) for _ in range(ring)]
        carry = [draw.randrange(wall) for _ in range(ring)]
        nexts, carry_next = ring_step(now, before, carry, reads, self_coefficient, wall)
        after, carry_after = ring_step(nexts, now, carry_next, reads, self_coefficient, wall)
        epsilon = [Fraction(r - r_next, wall) for r, r_next in zip(carry, carry_next, strict=True)]
        epsilon_next = [
            Fraction(r - r_after, wall) for r, r_after in zip(carry_next, carry_after, strict=True)
        ]
        walk_q = two_level_form(nexts, now, reads, self_coefficient, wall) - two_level_form(
            now, before, reads, self_coefficient, wall
        )
        assert walk_q == sum(e * (x - b) for e, x, b in zip(epsilon, nexts, before, strict=True))
        three = [Fraction(n * n - x * b) for n, x, b in zip(now, nexts, before, strict=True)]
        three_next = [Fraction(x * x - a * n) for x, a, n in zip(nexts, after, now, strict=True)]
        assert sum(three_next) - sum(three) == sum(
            e * x - e2 * n for e, e2, x, n in zip(epsilon, epsilon_next, nexts, now, strict=True)
        )
        delta = [r - r_next for r, r_next in zip(carry, carry_next, strict=True)]
        p_now, p_next = momentum(num, now, before), momentum(num, nexts, now)
        for i in range(ring):
            h = [now[(j - 1) % ring] * now[(j + 1) % ring] - now[j] * now[j] for j in range(ring)]
            stress = [h[j] + h[(j + 1) % ring] for j in range(ring)]  # G_aa(j) = h(j) + h(j + 1)
            centred_now = now[(i + 1) % ring] - now[(i - 1) % ring]
            centred_delta = delta[(i + 1) % ring] - delta[(i - 1) % ring]
            remainder_term = delta[i] * centred_now - now[i] * centred_delta
            assert (
                wall * (p_next[i] - p_now[i])
                == reads[0] * (stress[i] - stress[(i - 1) % ring]) - remainder_term
            )
    for clock_i, clock_j in ((gamma, gamma - 3), (gamma - 2, gamma - 7)):
        pace_i, pace_j = clock_i * clock_i // gamma, clock_j * clock_j // gamma
        reads_i = coefficients(num, den, gamma, clock_i, pace_i, factors=(5,) * 6, unit=2)[0]
        reads_j = coefficients(num, den, gamma, clock_j, pace_j, factors=(5,) * 6, unit=2)[0]
        assert Fraction(reads_i[0], pace_i * pace_i) == Fraction(reads_j[0], pace_j * pace_j)
