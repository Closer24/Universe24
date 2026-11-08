"""Replay compact golden evidence with native and independent full-state audits.

python -m research.component_families.verify --output runs/family-verification
Add --case ID (repeatable) and --presenter for complete local HTML recordings.
"""
import argparse
import gzip
import hashlib
import html
import json
from pathlib import Path
import time

from universe24 import Channel
from research.components import plain
from universe24.observation.clicks import classify
from research.presenter.export import (_portable_state, loads_strict, parse_decimal,
                                       state_sha256, coupling_data, capture, bundle, write_bundle)
from research.presenter.build import build
from research.experiments.run import source_hashes
from .cases import prepare
from .observations import observe
from . import oracle

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / 'evidence'
INDEX_SHA256 = '1ae8008055227dfb3e937d225c4619167f2080541fab66ad6e8bd881d86de800'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory(directory=EVIDENCE):
    directory = Path(directory).absolute()
    if any(p.is_symlink() for p in (directory, *directory.parents)) or not directory.is_dir():
        raise ValueError('Evidence directory and its parents must be real directories')
    for name in ('index.json', 'provenance.json'):
        if (directory / name).is_symlink() or not (directory / name).is_file():
            raise ValueError('Evidence index/provenance must be direct regular files')
    index_bytes = (directory / 'index.json').read_bytes()
    if hashlib.sha256(index_bytes).hexdigest() != INDEX_SHA256:
        raise ValueError('Evidence inventory hash differs from the published inventory')
    index = loads_strict(index_bytes.decode())
    if index['format'] != 'universe24-family-evidence-index-v1':
        raise ValueError('Unsupported evidence inventory')
    if sha(directory / 'provenance.json') != index['provenance_sha256']:
        raise ValueError('Original-source provenance hash differs')
    ids, paths = set(), set()
    for row in index['records']:
        name = row['path']
        if row['id'] in ids or name in paths or Path(name).name != name:
            raise ValueError('Duplicate or redirected evidence entry')
        if name != row['id'] + '.json.gz' or (directory / name).is_symlink() or not (directory / name).is_file():
            raise ValueError('Evidence must be a direct local file with its exact ID')
        ids.add(row['id']); paths.add(name)
        if sha(directory / name) != row['sha256']:
            raise ValueError('Evidence file digest differs: ' + name)
    if (len(ids), sum(r['states'] for r in index['records']), sum(r['steps'] for r in index['records'])) != (
            index['cases'], index['states'], index['transitions']):
        raise ValueError('Evidence counts differ')
    if {p.name for p in directory.iterdir()} != paths | {'index.json', 'provenance.json'}:
        raise ValueError('Unexpected evidence files or directories')
    return index


def load_case(row, directory=EVIDENCE):
    raw = (Path(directory) / row['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise ValueError('Consumed evidence bytes differ from the published digest')
    case = loads_strict(gzip.decompress(raw).decode())
    if case['format'] != 'universe24-family-golden-v1' or case['id'] != row['id']:
        raise ValueError('Evidence identity differs')
    if case['steps'] != row['steps'] or len(case['state_sha256']) != row['states']:
        raise ValueError('Evidence horizon differs')
    if len(case['state_sha256']) != case['steps'] + 1 or case['initial']['step'] != 0:
        raise ValueError('Expected every complete state from step zero')
    if case['initial']['state_sha256'] != case['state_sha256'][0]:
        raise ValueError('Initial trace digest differs')
    if case['original']['record_sha256'] != row['original_record_sha256']:
        raise ValueError('Original audited record digest differs')
    return case


def verify_case(case):
    prepared = prepare(case)
    bg = Channel(parse_decimal(case['background'][0]), parse_decimal(case['background'][1]), case['background'][2])
    initial = _portable_state(case['initial'], case['side'], bg)
    if initial != prepared.initial or coupling_data(prepared.engine.coupling) != case['coupling']:
        raise AssertionError('Published component preparation differs from audited complete initial state')
    independent, _ = oracle.routing(tuple(case['coupling']['body_signs']))
    if list(map(list, independent.ports)) != case['coupling']['ports'] or list(map(list, independent.weights)) != case['coupling']['weights']:
        raise AssertionError('Independent matrix-derived coupling differs')
    signs = tuple(case['coupling']['body_signs'])
    states, events = [initial], 0
    for t in range(1, case['steps'] + 1):
        old = states[-1]
        new = prepared.engine.advance(old)
        expected = oracle.step(old.cells, case['side'], tuple(bg), signs)
        if dict(new.cells) != expected or state_sha256(new) != case['state_sha256'][t]:
            raise AssertionError(f'Complete forward state differs at {t}')
        if prepared.engine.rewind(new) != old or oracle.step(expected, case['side'], tuple(bg), signs, True) != dict(old.cells):
            raise AssertionError(f'Complete inverse state differs at {t}')
        for address in old.cells.keys() | new.cells.keys():
            before, after = old.at(address), new.at(address)
            native = classify(before, after)
            independent_kind = oracle.click(before, after)
            if (None if native is None else native[0]) != independent_kind:
                raise AssertionError('Native arithmetic event classification differs')
            events += independent_kind is not None
        states.append(new)
    rewound = states[-1]
    for _ in range(case['steps']):
        rewound = prepared.engine.rewind(rewound)
    if rewound != initial:
        raise AssertionError('Full trajectory rewind differs')
    q_values = {sum(3 * (v.b - v.a) + v.r // 2 - bg.r // 2 for v in s.cells.values()) for s in states}
    if len(q_values) != 1:
        raise AssertionError('Exact +++ algebraic q balance failed')
    behavior = observe(case, prepared, states)
    return {'id': case['id'], 'states': len(states), 'transitions': case['steps'],
            'native_C_events': events, 'complete_native_and_matrix_replay': True,
            'every_state_matches_original_sha256': True, 'full_rewind': True,
            'algebraic_q': next(iter(q_values)), 'behavior': behavior}, prepared


def run(output, ids=(), presenter=False):
    start = time.process_time()
    index = inventory()
    selected = set(ids)
    if selected - {r['id'] for r in index['records']}:
        raise ValueError('Unknown published case ID')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    sources = source_hashes()
    root = HERE.parents[1]
    for folder in (HERE, root / 'research/reference'):
        for path in folder.glob('*.py'):
            sources[str(path.relative_to(root))] = sha(path)
    rows, links = [], []
    try:
        for row in index['records']:
            if selected and row['id'] not in selected:
                continue
            case = load_case(row)
            result, prepared = verify_case(case)
            rows.append(result)
            print(json.dumps({'id': case['id'], 'verified': True,
                              'scientific_composition': result['behavior'].get('scientific_composition_passed')}), flush=True)
            if presenter:
                page = output / case['id']
                page.mkdir()
                experiment = capture(prepared.engine, prepared.initial, case['steps'],
                                     id=case['id'], title=case['id'], view=case['view'],
                                     description='Complete audited initial-only building-block experiment. '
                                     'Register writes overlap the source halo; C2 reads UNWRITTEN. '
                                     'Two simultaneous read probes fail the second-input contract.',
                                     max_seconds=120)
                if [f['state_sha256'] for f in experiment['frames']] != case['state_sha256']:
                    raise AssertionError('Presenter recording differs from verified complete trajectory')
                experiment['provenance']['component_sources'] = sources
                experiment['provenance']['published_golden_sha256'] = row['sha256']
                write_bundle(page / 'experiments.json', bundle([experiment]))
                build(page / 'experiments.json', page / 'The_Presenter.html')
                (page / 'assembly.json').write_text(json.dumps(plain(prepared.manifest), indent=2) + '\n')
                links.append(f'<li><a href="{html.escape(case["id"])}/The_Presenter.html">{html.escape(case["id"])}</a></li>')
        if any(sha(root / name) != digest for name, digest in sources.items()):
            raise RuntimeError('Source files changed during verification')
        report = {'format': 'universe24-family-verification-v1', 'passed': True,
                  'cases': len(rows), 'states': sum(r['states'] for r in rows),
                  'transitions': sum(r['transitions'] for r in rows), 'rows': rows,
                  'inventory_sha256': INDEX_SHA256, 'source_sha256': sources,
                  'CPU_seconds_after_imports': time.process_time() - start,
                  'scope': 'Published subset only. Evidence validity includes negative scientific outcomes; '
                           'no physical particles, gravity, selection or unlimited memory claim.'}
        (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
        if presenter:
            (output / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Building blocks</title>'
                '<h1>Building-block recordings</h1><p>Complete native states; drag the cube to rotate. '
                'Use a browser that executes JavaScript, not an attachment preview.</p><ul>' + ''.join(links) + '</ul>')
        return report
    except Exception as exc:
        (output / 'failure.json').write_text(json.dumps({'type': type(exc).__name__, 'message': str(exc),
                                                        'completed_ids': [r['id'] for r in rows]}, indent=2) + '\n')
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--case', action='append', default=[])
    parser.add_argument('--presenter', action='store_true')
    args = parser.parse_args()
    run(args.output, args.case, args.presenter)


if __name__ == '__main__':
    main()
