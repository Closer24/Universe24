"""Run the eight scoped generic-structure audits; never promotes physics gates."""
from hashlib import sha256
import gzip
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
AUDITS = (
    ('interactions', 'runs/generic-structure/interactions.json'),
    ('constraint_certificate', 'runs/generic-structure/constraints.json'),
    ('native_schedule', 'runs/generic_structure/native_schedule.json'),
    ('packet_clock', 'runs/generic-structure/packet_clock.json'),
    ('symmetry_sector', 'runs/generic-structure/symmetry_sector.json'),
    ('contracts', 'runs/generic_structure/contracts/06_contracts.json'),
    ('frame_primitive', 'runs/generic-structure/frame_primitive.json'),
    ('independent_review', 'runs/generic-structure/independent_review.json'),
)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def verify_hash_maps(value):
    """Check recorded source maps; scope/status strings are not proof tokens."""
    count = 0
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ('source_sha256', 'source_hashes') and isinstance(child, dict):
                for name, expected in child.items():
                    path = ROOT / name
                    if not path.is_file() or file_hash(path) != expected:
                        raise ValueError(f'Stale source evidence: {name}')
                    count += 1
            else:
                count += verify_hash_maps(child)
    elif isinstance(value, list):
        for child in value:
            count += verify_hash_maps(child)
    return count


def main():
    destination = ROOT/'runs/generic-structure'
    destination.mkdir(parents=True, exist_ok=True)
    logs = destination/'logs'
    logs.mkdir(exist_ok=True)
    rows = []
    for name, output in AUDITS:
        module = 'validation.generic_structure.'+name
        completed = subprocess.run([sys.executable, '-m', module], cwd=ROOT,
                                   capture_output=True, text=True)
        log_path = logs/(name+'.txt')
        log_path.write_text(completed.stdout+completed.stderr)
        if completed.returncode:
            print(completed.stdout, end='')
            print(completed.stderr, end='', file=sys.stderr)
            raise RuntimeError(f'{module} failed; see {log_path}')
        path = ROOT/output
        data = json.loads(path.read_text())
        count = verify_hash_maps(data)
        source = ROOT/'validation/generic_structure'/(name+'.py')
        if isinstance(data.get('source_sha256'), str):
            if data['source_sha256'] != file_hash(source):
                raise ValueError(f'Stale primary audit source: {name}')
            count += 1
        stored = path
        # Preserve complete large traces without bloating the review diff.
        # The audit still emits its documented ordinary JSON for local use.
        if path.stat().st_size > 150_000:
            stored = path.with_suffix(path.suffix+'.gz')
            stored.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            if gzip.decompress(stored.read_bytes()) != path.read_bytes():
                raise ValueError('Archive mismatch')
        rows.append({'module': module, 'execution': 'passed',
                     'raw_output': output, 'raw_sha256': file_hash(path),
                     'committed_evidence': str(stored.relative_to(ROOT)),
                     'evidence_sha256': file_hash(stored),
                     'source_sha256': {str(source.relative_to(ROOT)): file_hash(source)},
                     'verified_recorded_source_hashes': count,
                     'log': str(log_path.relative_to(ROOT))})
        print(f'{name}: passed ({count} recorded source hashes)', flush=True)
    sources = {str(p.relative_to(ROOT)): file_hash(p)
               for p in sorted((ROOT/'validation/generic_structure').glob('*.py'))}
    result = {
        'schema': 'universe24/generic-structure/collection/1',
        'baseline_commit': '8c53e69f4b466dcbd2da7dab7e3c365bd9731766',
        'audits': rows, 'source_sha256': sources,
        'meaning': 'The listed executable scoped assertions and retained negative controls passed.',
        'physical_acceptance': 'not_established',
        'unimplemented': ['general native constraint-preserving Einstein map',
                          'one coupled <=48 accepted physical model',
                          'operational proper clocks and physical detector records'],
    }
    (destination/'collection.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Eight scoped audits passed; physical acceptance remains unestablished.')


if __name__ == '__main__':
    main()
