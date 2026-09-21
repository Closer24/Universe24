"""The register's verification map carried through a regeneration.

Every register (`expectations.json`) carries beside `derivations` a
`replicated` map, one entry per run block, pointing at the run's line in
`docs/REPLICATIONS.md` (the owner's rule of 2026-09-21, record 353;
docs/TEST_EXPECTATIONS.md). The replicator writes the map by its own pull
requests; a generator that rewrites its register from the worlds and the
design must not drop it. `carry_replicated` copies the map of the register
file on disk, unchanged, into the regenerated register.
"""

from __future__ import annotations

import json
from pathlib import Path

REPLICATED = "replicated"


def carry_replicated(existing: Path, register: dict[str, object]) -> dict[str, object]:
    """Return `register` with the `replicated` map of the register file at
    `existing` copied in unchanged, when that file exists and holds one;
    a register without the map on disk is returned as it is. The
    regenerated blocks are untouched: the map is the replicator's, never
    the generator's."""
    if existing.is_file():
        found = json.loads(existing.read_text(encoding="utf-8"))
        if isinstance(found, dict) and isinstance(found.get(REPLICATED), dict):
            register[REPLICATED] = json.loads(json.dumps(found[REPLICATED]))
    return register
