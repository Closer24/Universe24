"""The claims map's gate: docs/CLAIMS.md is byte for byte what tools/claims_map.py writes from tools/derivations/proofs_inventory.json, one section per row, so the map and the inventory cannot drift apart."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_the_claims_map_is_the_inventorys_map_with_one_section_per_row():
    """The generator's own check (`--check`): the file equals the rendered text, and the `## ` sections count the inventory's rows."""
    spec = importlib.util.spec_from_file_location("claims_map", ROOT / "tools" / "claims_map.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.rows()
    text = module.render(rows)
    assert module.departure(text) is None, module.departure(text)
    assert sum(line.startswith("## ") for line in text.splitlines()) == len(rows), len(rows)
