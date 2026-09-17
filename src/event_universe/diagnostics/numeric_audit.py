"""Static defense against accidental non-integer math in all physical modules.

This is a guardrail, not a proof against arbitrary dynamically loaded Python.
Runtime input/state checks and local-law tests provide complementary coverage.
"""

import ast
from pathlib import Path

FORBIDDEN_NAMES = {"float", "complex", "sqrt", "log", "sin", "cos", "tan", "hypot", "normalize"}
FORBIDDEN_MODULES = {"math", "cmath", "numpy", "scipy", "decimal", "fractions", "random"}


def static_integer_audit(source_path: str | Path) -> list[tuple[int, str]]:
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
            if name in FORBIDDEN_NAMES:
                violations.append((node.lineno, f"forbidden call: {name}"))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
            if any(name.split(".")[0] in FORBIDDEN_MODULES for name in names):
                violations.append((node.lineno, "non-core numeric import"))
    return violations


def audit_physical_modules() -> dict[str, list[tuple[int, str]]]:
    root = Path(__file__).parents[1]
    return {
        str(path.relative_to(root)): static_integer_audit(path)
        for folder in ("core", "fields")
        for path in sorted((root / folder).rglob("*.py"))
    }
