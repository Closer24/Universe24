"""Static layer checks used by the suite; these do not execute inspected code.

The layers: `core` holds the law-free substrate (bounded integers, the board's
addresses and headings, the phase tables) and imports nothing but `core`;
`events` is the engine and may import `core`; the host modules (the runner,
the workspace, retention, the snapshot writer) may import both. No physical
module imports output or storage libraries.
"""

import ast
from importlib.util import resolve_name

GENERIC_LAYERS = {"core", "events"}
OUTPUT_MODULES = {"matplotlib", "PIL", "json", "pathlib", "os", "subprocess"}


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


def violations(source, module):
    """Check the dependency direction of one module's imports."""
    tree = ast.parse(source)
    relative = module.removeprefix("event_universe.")
    layer = relative.split(".")[0]
    found = []
    for line, target in import_targets(tree, module):
        if target.startswith("event_universe."):
            dependency = target.removeprefix("event_universe.")
            target_layer = dependency.split(".")[0]
            if layer == "core" and target_layer != "core":
                found.append((line, "core imports another layer"))
            if layer == "events" and target_layer not in {"core", "events"} and relative != "events.run":
                found.append((line, "the engine imports a host module"))
        elif layer in GENERIC_LAYERS and target.split(".")[0] in OUTPUT_MODULES:
            if relative != "events.run":
                found.append((line, "physical code imports output or storage"))
    return found
