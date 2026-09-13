"""One-shot breaking migration from Cell vocabulary to canonical Node vocabulary.

This script is intentionally temporary. It updates tracked active text files, removes
compatibility shims, and leaves immutable historical evidence untouched.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Historical evidence must remain source-accurate. These are not active contracts.
SKIP_PREFIXES = ("tests/reference/",)
SKIP_FILES = {
    "docs/VALIDATION.md",
}

DELETE_FILES = {
    "src/event_universe/diagnostics/cell_contract.py",
    "tests/test_cell_state_contract.py",
}

# Specific identifier migrations run before generic prose/variable rewrites.
EXACT = (
    ("slots_per_cell", "slots_per_node"),
    ("max_particles_per_cell", "max_particles_per_node"),
    ("DisturbanceCell", "DisturbanceNodeState"),
    ("SpatialCell", "SpatialNodeState"),
    ("CellView", "NodeView"),
    ("CellState", "NodeState"),
    ("LinkCell", "LinkNodeState"),
    ("StreamCell", "StreamNodeState"),
    ("CELL_REGISTERS", "NODE_REGISTERS"),
    ("ZERO_CELL", "ZERO_NODE"),
    ("validate_cell", "validate_node"),
    ("cell_state_violations", "node_state_violations"),
    ("cell_contract", "node_contract"),
    ("test_cell_state_contract", "test_node_state_contract"),
    ("_cells", "_nodes"),
    (".cells", ".nodes"),
    ("_cell_", "_node_"),
    ("cell_", "node_"),
    ("_cell", "_node"),
    ("cells_", "nodes_"),
    ("_cells", "_nodes"),
)

# External standard/package strings are not simulator vocabulary.
RESTORE_EXTERNAL = (
    ("Sec-Fetch-Node", "Sec-Fetch-Site"),
    ("node-packages", "site-packages"),
)

# Remove temporary compatibility blocks introduced by the first, non-breaking PR.
REMOVE_SNIPPETS = {
    "src/event_universe/core/disturbance_state.py": (
        '''    @property\n    def slots_per_node(self) -> int:\n        """Canonical name for the legacy ``slots_per_cell`` configuration field."""\n        return self.slots_per_cell\n\n''',
        '''# Legacy compatibility names. They are not separate physical concepts; new code\n# must use DisturbanceNodeState and NodeView.\nDisturbanceCell = DisturbanceNodeState\nCellView = NodeView\n''',
    ),
    "src/event_universe/core/spatial_state.py": (
        '''# Legacy compatibility name. It is not a separate physical concept; new code\n# must use SpatialNodeState.\nSpatialCell = SpatialNodeState\n''',
    ),
    "src/event_universe/disturbance_api.py": (
        '''    @property\n    def nodes(self) -> Mapping[Address3, NodeView]:\n        """Canonical public view of the local NodeState map."""\n        return self.cells\n\n''',
    ),
}


def tracked_files() -> list[str]:
    return subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()


def is_skipped(path: str) -> bool:
    return path in SKIP_FILES or path.startswith(SKIP_PREFIXES)


def migrate_text(path: str, text: str) -> str:
    for snippet in REMOVE_SNIPPETS.get(path, ()):
        text = text.replace(snippet, "")

    for old, new in EXACT:
        text = text.replace(old, new)

    # Plain-language and local-variable vocabulary. Word boundaries avoid words
    # such as "cellular" and external identifiers restored below.
    for old, new in (
        (r"\bCells\b", "Nodes"),
        (r"\bcells\b", "nodes"),
        (r"\bCell\b", "Node"),
        (r"\bcell\b", "node"),
    ):
        text = re.sub(old, new, text)

    for new, old in RESTORE_EXTERNAL:
        text = text.replace(new, old)
    return text


def rename_paths(paths: list[str]) -> None:
    # Only remaining active filenames using the old physical noun are renamed.
    # Known compatibility-path collisions were deleted above.
    for source in sorted(paths, key=len, reverse=True):
        if is_skipped(source) or "cell" not in source.lower():
            continue
        if source in DELETE_FILES or not (ROOT / source).exists():
            continue
        target = re.sub("cell", "node", source, flags=re.IGNORECASE)
        if target == source:
            continue
        target_path = ROOT / target
        if target_path.exists():
            raise RuntimeError(f"cannot rename {source}: target already exists: {target}")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "mv", source, target], cwd=ROOT, check=True)


def fix_breaking_contract_tests() -> None:
    path = ROOT / "tests/test_node_terminology.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "def test_canonical_state_types_use_node_names_with_legacy_aliases_only():",
        "def test_canonical_state_types_use_node_names_after_breaking_migration():",
    )
    text = text.replace(
        "    assert disturbance_state.InitialState.slots_per_node.fget is not None\n",
        '    assert "slots_per_node" in disturbance_state.InitialState.__dataclass_fields__\n',
    )
    # These assertions were useful only while compatibility aliases existed.
    text = text.replace(
        "    assert disturbance_state.DisturbanceNodeState is disturbance_state.DisturbanceNodeState\n",
        "",
    )
    text = text.replace(
        "    assert disturbance_state.NodeView is disturbance_state.NodeView\n",
        "",
    )
    text = text.replace(
        "    assert spatial_state.SpatialNodeState is spatial_state.SpatialNodeState\n",
        "",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    paths = tracked_files()

    for path in DELETE_FILES:
        file_path = ROOT / path
        if file_path.exists():
            file_path.unlink()

    for path in paths:
        if path in DELETE_FILES or is_skipped(path):
            continue
        file_path = ROOT / path
        if not file_path.is_file():
            continue
        try:
            before = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        after = migrate_text(path, before)
        if after != before:
            file_path.write_text(after, encoding="utf-8")

    rename_paths(paths)
    fix_breaking_contract_tests()

    # The canonical active contract no longer describes compatibility aliases.
    terminology = ROOT / "docs/TERMINOLOGY.md"
    text = terminology.read_text(encoding="utf-8")
    text = text.replace(
        "Configuration keys that predate this contract may remain temporarily for backward compatibility. "
        "Their documentation must describe them using the canonical Node vocabulary and migration must not "
        "silently change physical behavior.\n",
        "The active API and configuration use the canonical Node vocabulary directly; no Cell compatibility alias is retained.\n",
    )
    terminology.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
