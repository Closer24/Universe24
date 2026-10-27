"""The physical modules hold integer mathematics only: no float, no `/`, no non-integer import, dtype or numpy function; the root left everywhere (tests/test_rule3.py holds that gate); and the one division act Rule3's, no raw floor division or modulo outside core/rule3.py but the named index wraps and shape divisions. PHYSICAL_MODULES is every module of the package, of core/ and of loader/, read from the tree (the hand list, the checkers' self-tests, the composed literals' gate, the conventions table and the import-cycle check struck or folded 2026-10-24 with the tests' audit: the composed literals tools/engine_gates.py's numbers ratchet, the rule's arithmetic sites tools/record_code_shape.py's)."""

import ast
import io
import tokenize
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "event_universe"

PHYSICAL_MODULES = tuple(  # every module of the package, of core/ and of loader/ but the package markers, read from the tree so that no module escapes the gate unnamed (2026-10-24: the hand list and its own test folded here)
    sorted(
        path.relative_to(SRC).as_posix()
        for folder in (SRC, SRC / "core", SRC / "loader")
        for path in folder.glob("*.py")
        if path.name != "__init__.py"
    )
)

FORBIDDEN_IMPORTS = {"random", "fractions", "decimal", "cmath", "statistics"}
MATH_ALLOWED, NUMPY_DTYPES_ALLOWED = set[str](), {"int64"}
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


CORE, DIVISIONS = "core/acts.py", {ast.FloorDiv, ast.Mod}  # core/rule3.py before NL-S1


DIVISION_CALLS = {"divmod", "np.floor_divide", "np.mod", "np.remainder", "np.fmod"}
INDEX_ARITHMETIC = (  # the named exceptions: the module, the operator, the function, its responsibility
    ("core/ports.py", ast.Mod, "shifted", "the periodic wrap of a Node's index along the shifted axis"),
    (
        "core/ports.py",
        ast.Mod,
        "wrap",
        "the periodic wrap of a Node's index or an axis, the torus's own",
    ),
)
# the record's writer and readers, no act of the Node: their quotients are readings at a named scale
READERS = tuple(
    f"{n}.py" for n in "run decoder gates events circle board bangs clicks predicates symmetries".split()
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
    """The arithmetic of the engine is Rule3's division act (core/acts.divide, the one carried division, and the quotient and remainder readings on it in core/rule3.py; ALGEBRA.md #the-four-acts): a raw floor division or modulo on a number of the law is refused in every other module of the engine (`//`, `%`, their augmented forms, `divmod`, numpy's floor division and remainder), and the index wraps and the row's shape divisions are the named exceptions (INDEX_ARITHMETIC, each by module, operator and function, no level, share, count or pace among them), refused in turn when one no longer stands in the code."""
    allowed = {(name, kind, function) for name, kind, function, _reason in INDEX_ARITHMETIC}
    standing, offenders = set(), []
    for path in sorted(p for p in SRC.rglob("*.py") if p.relative_to(SRC).as_posix() != CORE):
        name, source = path.relative_to(SRC).as_posix(), path.read_text(encoding="utf-8")
        if name in READERS:
            continue
        for line, kind, function in divisions(ast.parse(source)):
            if (name, kind, function) in allowed:
                standing.add((name, kind, function))
            else:
                offenders.append(f"{name}:{line} {function}: {source.splitlines()[line - 1].strip()}")
    assert offenders == [], offenders
    assert standing == allowed, sorted(allowed - standing)
    assert divisions(ast.parse((SRC / CORE).read_text(encoding="utf-8"))), "the act's home divides"
