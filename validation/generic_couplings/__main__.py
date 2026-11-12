"""Reproduce exact generic-coupling controls and saved full45/six equivalence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from . import geometry, native, sector
from .runtime import run_runtime_pair


def run(out: Path) -> dict:
    out = Path(out)
    if out.exists():
        raise ValueError('audit output must be a new directory')
    audits = {'native': native.audit(), 'geometry': geometry.audit(), 'sector': sector.audit()}
    audits['runtime'] = run_runtime_pair(out / 'runtime')
    root = Path(__file__).resolve().parents[2]
    sources = list(Path(__file__).parent.glob('*.py')) + [
        root / 'validation/geodesic_board/run.py',
        root / 'validation/geometry/team48/refinement_integer_projective.py',
        root / 'validation/geometry/team48/matter_dust_square.py',
        root / 'validation/research_eight/07_hyperbolic_symbol.py',
    ]
    evidence = {'schema': 'universe24/generic-couplings-audit/1', 'audits': audits,
                'source_hashes': {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in sorted(sources)},
                'physical_acceptance': 'not_established',
                'domain': 'exact identities and homogeneous isotropic neutral scalar/dust restriction; '
                          'not general45 compression, operational clocks or Einstein/Born acceptance'}
    out.mkdir(parents=True, exist_ok=True)
    (out / 'evidence.json').write_text(json.dumps(evidence, indent=2, sort_keys=True) + '\n')
    return evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    evidence = run(args.out)
    print(json.dumps({'status': 'passed', 'evidence': str(args.out / 'evidence.json'),
                      'audits': list(evidence['audits']),
                      'physical_acceptance': evidence['physical_acceptance']}, indent=2))


if __name__ == '__main__':
    main()
