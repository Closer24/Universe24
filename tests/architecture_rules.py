"""Static layer checks used by the suite; these do not execute inspected code."""

import ast
from importlib.util import resolve_name

GENERIC_LAYERS = {"core", "fields"}
COMPOSITION_MODULES = {"disturbance_api"}
FORBIDDEN_GENERIC_TYPES = {"Config", "NodeState", "ParticleState", "Simulation"}


def import_targets(tree, module):
    package = (
        module.removesuffix(".__init__") if module.endswith(".__init__") else module.rsplit(".", 1)[0]
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom):
            target = node.module or ""
            if node.level:
                target = resolve_name("." * node.level + target, package)
            yield node.lineno, target
            for alias in node.names:
                yield node.lineno, target + "." + alias.name


class RuntimeArithmetic(ast.NodeVisitor):
    """Find runtime formulas while allowing type unions and literal configuration."""

    def __init__(self):
        self.lines = []

    def visit_FunctionDef(self, node):
        for statement in node.body:
            self.visit(statement)
        for default in (*node.args.defaults, *node.args.kw_defaults):
            if default is not None:
                self.visit(default)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_AnnAssign(self, node):
        if node.value is not None:
            self.visit(node.value)

    def visit_BinOp(self, node):
        self.lines.append(node.lineno)

    def visit_AugAssign(self, node):
        self.lines.append(node.lineno)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, (ast.UAdd, ast.USub)) and not isinstance(node.operand, ast.Constant):
            self.lines.append(node.lineno)
        self.generic_visit(node)


def violations(source, module):
    """Check absolute/relative imports and formula-free API assembly."""
    tree = ast.parse(source)
    relative = module.removeprefix("event_universe.")
    layer = relative.split(".")[0]
    found = []
    if layer == "fields":
        forbidden_world_members = {
            "nodes",
            "particles",
            "occupancy",
            "active",
            "transits",
            "history",
            "paths",
            "force_records",
            "step",
            "run",
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr in forbidden_world_members:
                found.append((node.lineno, "local calculation accesses world state or replay"))
    for line, target in import_targets(tree, module):
        if target.startswith("event_universe."):
            dependency = target.removeprefix("event_universe.")
            target_layer = dependency.split(".")[0]
            if layer == "core" and target_layer != "core":
                found.append((line, "core imports another layer"))
            if layer == "fields":
                if not (
                    dependency == "core.disturbance_state"
                    or dependency.startswith("core.disturbance_state.")
                    or dependency == "core.spatial_state"
                    or dependency.startswith("core.spatial_state.")
                    or dependency == "core.coupling_selectors"
                    or dependency.startswith("core.coupling_selectors.")
                    or dependency == "core.validation"
                    or dependency.startswith("core.validation.")
                    or dependency == "core.sampling_contract"
                    or dependency.startswith("core.sampling_contract.")
                    or dependency == "core.integer"
                    or dependency.startswith("core.integer.")
                    or dependency == "core.node_conservation"
                    or dependency.startswith("core.node_conservation.")
                    or target_layer == layer
                ):
                    found.append((line, "generic calculation imports another layer"))
                if dependency.rsplit(".", 1)[-1] in FORBIDDEN_GENERIC_TYPES:
                    found.append((line, "generic calculation imports model state"))
        elif layer in GENERIC_LAYERS and target.split(".")[0] in {
            "matplotlib",
            "PIL",
            "json",
            "pathlib",
            "os",
            "subprocess",
        }:
            found.append((line, "physical code imports output or storage"))
    if relative in COMPOSITION_MODULES:
        arithmetic = RuntimeArithmetic()
        arithmetic.visit(tree)
        found.extend(
            (line, "runtime arithmetic belongs in a reusable calculation") for line in arithmetic.lines
        )
    return found
