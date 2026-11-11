"""Check historical provenance across the explicitly reviewed source migration.

Historical artifacts keep their original paths and SHA256 values. These checks
permit only the namespace relocation and the exact-JSON import substitution;
all physical outputs still have to match their historical evidence separately.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def migrated_source_hashes(historical: dict[str, str], root: Path) -> dict[str, str]:
    """Return fresh hashes after proving the known edits recover historical bytes.

    An unrelated source edit fails this check, including one that leaves the
    tested trajectory unchanged. This is a migration proof, not permission to
    update or relabel an older artifact's provenance.
    """
    fresh = {}
    for old_name, old_digest in historical.items():
        name = ('validation/' + old_name[len('experiments/'):]
                if old_name.startswith('experiments/') else old_name)
        payload = (root / name).read_bytes()
        historical_bytes = payload
        if old_name.startswith('experiments/'):
            historical_bytes = historical_bytes.replace(b'validation.', b'experiments.')
            historical_bytes = historical_bytes.replace(b'validation/', b'experiments/')
        if old_name == 'universe24/core/tensor.py':
            historical_bytes = historical_bytes.replace(
                b'from . import exact_json as json\n', b'import json\n')
        restored_digest = hashlib.sha256(historical_bytes).hexdigest()
        if restored_digest != old_digest:
            raise AssertionError(
                f'{name}: edits beyond the reviewed namespace/JSON migration; '
                f'historical SHA256 {old_digest}, reconstructed {restored_digest}')
        fresh[name] = hashlib.sha256(payload).hexdigest()
    return fresh
