"""Static defense against accidental non-integer math in all physical modules.

This is a guardrail, not a proof against arbitrary dynamically loaded Python.
Runtime input/state checks and local-law tests provide complementary coverage.

Two audits, one per physical layer (SIMULATOR_DEFINITIONS.md, "Required
regression gates"): `core/` holds bounded integers and nothing else, so its
audit refuses every numeric library; `events/` is the engine, vectorized
over the rows of the GameBoard in integer numpy arrays, so its audit permits
numpy and refuses what would leave the integers: a float or complex literal,
true division, a float dtype or constant, the square root, the means and
the transcendental functions. Since 2026-09-21 (the architecture audit's
item 5, docs/MIGRATION.md); before, `events/` was audited by its runtime
bounds alone.
"""

import ast
from pathlib import Path

FORBIDDEN_NAMES = {"float", "complex", "sqrt", "log", "sin", "cos", "tan", "hypot", "normalize"}
FORBIDDEN_MODULES = {"math", "cmath", "numpy", "scipy", "decimal", "fractions", "random"}

# The events audit: numpy and `math` (its integer functions, `isqrt` and
# `gcd`) are permitted; these names, called or referenced, are not.
EVENTS_FORBIDDEN_NAMES = FORBIDDEN_NAMES | {
    "exp",
    "arctan",
    "arctan2",
    "mean",
    "average",
    "std",
    "var",
    "divide",
    "true_divide",
    "reciprocal",
    "power",
    "float16",
    "float32",
    "float64",
    "float128",
    "floating",
    "double",
    "linalg",
    "pi",
    "inf",
    "nan",
}
EVENTS_FORBIDDEN_MODULES = FORBIDDEN_MODULES - {"math", "numpy"}


def _violations(source_path: str | Path, names: set[str], modules: set[str]) -> list[tuple[int, str]]:
    tree = ast.parse(Path(source_path).read_text(encoding="utf-8"))
    violations: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (float, complex)):
            violations.append((node.lineno, "non-integer literal"))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            violations.append((node.lineno, "true division"))
        if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Div):
            violations.append((node.lineno, "augmented true division"))
        if isinstance(node, ast.Call):
            name = (
                node.func.id
                if isinstance(node.func, ast.Name)
                else (node.func.attr if isinstance(node.func, ast.Attribute) else "")
            )
            if name in names:
                violations.append((node.lineno, f"forbidden call: {name}"))
        elif isinstance(node, ast.Name) and node.id in names:
            violations.append((node.lineno, f"forbidden name: {node.id}"))
        elif isinstance(node, ast.Attribute) and node.attr in names:
            violations.append((node.lineno, f"forbidden name: {node.attr}"))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
            if any(name.split(".")[0] in modules for name in imported):
                violations.append((node.lineno, "non-core numeric import"))
    return violations


def static_integer_audit(source_path: str | Path) -> list[tuple[int, str]]:
    """The audit of `core/`: integers only, no numeric library."""
    return _violations(source_path, FORBIDDEN_NAMES, FORBIDDEN_MODULES)


def static_events_audit(source_path: str | Path) -> list[tuple[int, str]]:
    """The audit of `events/`: integer numpy permitted, nothing that leaves
    the integers (a float literal or dtype, true division, the square root,
    the means, the transcendental functions and constants)."""
    return _violations(source_path, EVENTS_FORBIDDEN_NAMES, EVENTS_FORBIDDEN_MODULES)


# The one module of `events/` outside the audit: the artifacts' writer, which
# holds no physics and joins paths with pathlib's `/` (the architecture
# gate's same exemption, `tests/architecture_rules.py`).
ARTIFACT_WRITER = "events/run.py"


def audit_physical_modules() -> dict[str, list[tuple[int, str]]]:
    """Every module of the three physical layers with its audit's findings (the
    features' folders audited as the engine is, integer numpy and nothing that
    leaves the integers; issue #1154 cut 2)."""
    root = Path(__file__).parents[1]
    audits = (
        ("core", static_integer_audit),
        ("features", static_events_audit),
        ("events", static_events_audit),
    )
    return {
        str(path.relative_to(root)): audit(path)
        for folder, audit in audits
        for path in sorted((root / folder).rglob("*.py"))
        if path.relative_to(root).as_posix() != ARTIFACT_WRITER
    }
