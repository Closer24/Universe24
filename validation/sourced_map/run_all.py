"""Execute eight scoped sourced-map audits and bind evidence to source."""
from hashlib import sha256
import gzip
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASELINE = 'f4f64e062f07b3ca119eccf655df746be206908b'
AUDITS = (
    ('physical_map', 'runs/sourced-map/physical_map.json'),
    ('projective', 'runs/sourced-map/projective.json'),
    ('native', 'runs/sourced_map/native.json'),
    ('variational', 'runs/sourced-map/variational.json'),
    ('oracle', 'runs/sourced-map/oracle.json'),
    ('domain', 'runs/sourced-map/domain.json'),
    ('runtime', 'runs/sourced-map/runtime.json'),
    ('review', 'runs/sourced-map/review.json'),
)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def check_source_hashes(value):
    count = 0
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ('source_sha256', 'source_hashes') and isinstance(child, dict):
                for name, expected in child.items():
                    path = ROOT / name
                    if not path.is_file() or file_hash(path) != expected:
                        raise ValueError(f'Stale recorded source: {name}')
                    count += 1
            else:
                count += check_source_hashes(child)
    elif isinstance(value, list):
        for child in value:
            count += check_source_hashes(child)
    return count


def main():
    output = ROOT / 'runs/sourced-map'
    logs = output / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, relative_output in AUDITS:
        module = 'validation.sourced_map.' + name
        process = subprocess.run([sys.executable, '-m', module], cwd=ROOT,
                                 capture_output=True, text=True)
        log = logs / (name + '.txt')
        log.write_text(process.stdout + process.stderr)
        if process.returncode:
            print(process.stdout, end='')
            print(process.stderr, end='', file=sys.stderr)
            raise RuntimeError(f'{module} failed; see {log}')
        evidence = ROOT / relative_output
        data = json.loads(evidence.read_text())
        checked = check_source_hashes(data)
        source = ROOT / 'validation/sourced_map' / (name + '.py')
        if isinstance(data.get('source_sha256'), str):
            if data['source_sha256'] != file_hash(source):
                raise ValueError(f'Stale primary source: {name}')
            checked += 1
        committed = evidence
        if evidence.stat().st_size > 150_000:
            committed = evidence.with_suffix(evidence.suffix + '.gz')
            committed.write_bytes(gzip.compress(evidence.read_bytes(), mtime=0))
            if gzip.decompress(committed.read_bytes()) != evidence.read_bytes():
                raise ValueError(f'Evidence compression mismatch: {name}')
        rows.append({'module': module, 'execution': 'passed',
                     'raw_output': relative_output, 'raw_sha256': file_hash(evidence),
                     'committed_evidence': str(committed.relative_to(ROOT)),
                     'evidence_sha256': file_hash(committed),
                     'source_sha256': {str(source.relative_to(ROOT)): file_hash(source)},
                     'verified_recorded_source_hashes': checked,
                     'log': str(log.relative_to(ROOT))})
        print(f'{name}: passed ({checked} recorded source hashes)', flush=True)
    sources = {str(path.relative_to(ROOT)): file_hash(path)
               for path in sorted((ROOT / 'validation/sourced_map').glob('*.py'))}
    collection = {
        'schema': 'universe24/sourced-map/collection/1', 'baseline_commit': BASELINE,
        'audits': rows, 'source_sha256': sources,
        'positive_scope': 'Exact sampled sourced expanding flat homogeneous massless scalar plus dust FLRW, on the declared complete-state chart.',
        'general_physical_acceptance': 'not_established',
        'unimplemented': ['massive scalar native constraint-preserving map',
                          'spatial and anisotropic Einstein dynamics',
                          'operational clock/apparatus and physical click interpretation'],
    }
    (output / 'collection.json').write_text(json.dumps(collection, indent=2) + '\n')
    print('Eight scoped audits passed; general physical gates remain open.')


if __name__ == '__main__':
    main()
