"""Generate six exact demonstrations and independent generic import fixtures.

All preparations are data. Every update uses the unchanged reference Engine.
The optional standalone build is a packaging step after all runs have ended.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from universe24.core import Coupling, Cube, Engine, State
from universe24.core.state import Channel
from universe24.experiments.config import checkpoint_data, from_dict
from .export import bundle, canonical, capture, from_trace, write_bundle

ROOT = Path(__file__).resolve().parents[2]
GUIDE = ROOT / 'research/building_blocks/evidence/cases/guide_N24/states.jsonl'
CPU_BUDGET = 120


def _write(path, data):
    with path.open('x', encoding='ascii') as handle:
        handle.write(canonical(data) + '\n')


def _budget(started):
    if time.process_time() - started > CPU_BUDGET:
        raise TimeoutError('Demonstration generation exceeded its 120 CPU-second budget')


def boundary_preparation(*, side, signs, background, address):
    """Six fixed old-snapshot contributions of -5, including periodic wrap."""
    engine, cube = Engine(Coupling(signs)), Cube(side)
    cells = {address: Channel(123, -77, 3)}
    for d in range(6):
        sender = engine.coupling.ports[d][address[3]]
        weight = engine.coupling.weights[d][address[3]]
        neighbor = cube.adjacent(address, d, sender)
        cells[neighbor] = Channel(0, -5 * weight, background)
    off_axis = (side // 2, side // 2 + 1, side // 3, 31)
    if off_axis in cells:
        raise AssertionError('Off-axis fixture unexpectedly overlaps an input')
    cells[off_axis] = Channel(-9, 11, 1)
    initial = State(cube, Channel(0, 0, background), cells)
    assert engine.input_sums(initial)[address] == -30
    assert engine.advance(initial).at(address) == Channel(-77, -133, 3)
    return engine, initial


def _huge(*, id):
    magnitude = 10 ** 5000
    initial = State(Cube(5), Channel(0, 0, 2), {
        (2, 1, 3, 47): Channel(magnitude, -magnitude + 17, 4),
    })
    return capture(Engine(Coupling((-1, -1, 1))), initial, 2, id=id,
                   title='5,001-digit counters',
                   description='Exact large signed counters on channel 47; the hand shows direction only. '
                               'Open the channel details to inspect every decimal digit.',
                   view={'position': [2, 1, 3], 'channel': 47})


def _guide():
    # These optional observers are frozen preparation metadata. The renderer
    # evaluates the same generic all_equal clauses for any address/component.
    readouts = [{
        'id': f'M{offset}', 'label': f'M{offset}: prepared remainder record',
        'kind': 'all_equal',
        'clauses': [
            {'address': [63 + offset, 75, 75, 0], 'component': 'r', 'equals': '0'},
            {'address': [63 + offset, 75, 75, 14], 'component': 'r', 'equals': '4'},
        ],
    } for offset in (6, 12)]
    return from_trace(GUIDE, id='prepared-guide', title='A signal starts two clock records',
                      description='Complete 57-frame native guide_N24 trace. Readouts M6 and M12 '
                                  'are fixed remainder predicates; all other channels and off-axis '
                                  'remainders are retained. The record has finite retention.',
                      readouts=readouts, view={'position': [69, 75, 75], 'channel': 0})


def make_demonstrations(started):
    source = ROOT / 'examples/impulse.json'
    experiment = from_dict(json.loads(source.read_text(encoding='utf-8')))
    positive = capture(experiment.engine, experiment.initial, experiment.steps,
                       id='positive-impulse', title='Positive impulse',
                       description='The existing impulse.json preparation, recorded without modification. '
                                   'Follow the neighboring counter dials and retained remainders.',
                       view={'position': [4, 4, 4], 'channel': 0})
    positive['provenance']['preparation_file'] = 'examples/impulse.json'
    positive['provenance']['preparation_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    _budget(started)
    target = (0, 8, 3, 47)
    engine, initial = boundary_preparation(side=9, signs=(1, -1, 1),
                                            background=2, address=target)
    boundary = capture(engine, initial, 4, id='signed-boundary',
                       title='Signed inputs across a cube boundary',
                       description='Channel 47 receives six signed contributions with u=-30. '
                                   'The first transition crosses periodic boundaries and tests '
                                   'negative Euclidean division; extra channel 31 is off axis.',
                       view={'position': list(target[:3]), 'channel': target[3]})
    _budget(started)
    cells = {}
    for position in ((5, 5, 5), (6, 5, 5)):
        cells[(*position, 0)] = Channel(-1, -1, 0)
        cells[(*position, 14)] = Channel(1, 1, 4)
    clocks = capture(Engine(), State(Cube(11), Channel(0, 0, 2), cells), 20,
                     id='adjacent-clocks', title='Two prepared neighboring clocks',
                     description='Two initially adjacent counter motifs evolve together through '
                                 'the same six-neighbor coupling. Compare their actual phases '
                                 'and inspect the complete remainder field.',
                     view={'position': [5, 5, 5], 'channel': 0})
    _budget(started)
    guide = _guide()
    _budget(started)
    cells = {(3, 3, 3, g): Channel(0, 0, g % 6) for g in range(48)}
    cells[(1, 5, 2, 31)] = Channel(0, 0, 0)
    cells[(6, 0, 4, 47)] = Channel(0, 0, 1)
    remainders = capture(Engine(Coupling((-1, 1, -1))),
                         State(Cube(7), Channel(0, 0, 5), cells), 4,
                         id='stationary-remainders', title='A stationary remainder field',
                         description='Background remainder 5; all 48 channels at the selected node '
                                     'cycle through remainder labels 0..5 in the preparation. '
                                     'All counters remain zero, so the full state is stationary. '
                                     'Channels equal to the background remain inspectable.',
                         view={'position': [3, 3, 3], 'channel': 47})
    assert len({frame['state_sha256'] for frame in remainders['frames']}) == 1
    huge = _huge(id='large-integer-demo')
    _budget(started)
    return [positive, boundary, clocks, guide, remainders, huge]


def make_fixtures(directory, started):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    target = (10, 0, 7, 47)
    engine, initial = boundary_preparation(side=11, signs=(-1, 1, -1),
                                            background=5, address=target)
    readouts = [{
        'id': 'negative-transition-record', 'label': 'Target b=-133 and remainder=3',
        'kind': 'all_equal',
        'clauses': [
            {'address': list(target), 'component': 'b', 'equals': '-133'},
            {'address': list(target), 'component': 'r', 'equals': '3'},
        ],
    }, {
        'id': 'initial-marker', 'label': 'Initial target counter a=123',
        'kind': 'all_equal',
        'clauses': [{'address': list(target), 'component': 'a', 'equals': '123'}],
    }]
    unseen = capture(engine, initial, 3, id='unseen-boundary-47',
                     title='Independent imported boundary case',
                     description='A held-out preparation using channels 47 and 31, background 5 '
                                 'and fixed signs (-1,+1,-1). No corresponding demo identifier exists.',
                     readouts=readouts, view={'position': list(target[:3]), 'channel': target[3]})
    write_bundle(directory / 'unseen.json', bundle([unseen]))
    write_bundle(directory / 'huge.json', bundle([_huge(id='unseen-precision-47')]))
    checkpoints = []
    state = initial
    for step in range(4):
        checkpoints.append(checkpoint_data(state, engine, step))
        if step < 3:
            state = engine.advance(state)
    _write(directory / 'snapshot.json', checkpoints[2])
    with (directory / 'trace.jsonl').open('x', encoding='ascii') as handle:
        for checkpoint in checkpoints:
            handle.write(canonical(checkpoint) + '\n')
    _write(directory / 'browser_manifest.json', {
        'unseen_bundle': 'unseen.json', 'huge_bundle': 'huge.json',
        'native_snapshot': 'snapshot.json', 'native_trace': 'trace.jsonl',
    })
    _budget(started)
    return directory


def generate(output, *, fixtures=None, standalone=True):
    output = Path(output)
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite existing demonstration directory: {output}')
    if fixtures is not None and Path(fixtures).exists():
        raise FileExistsError(f'Refusing to overwrite existing fixture directory: {fixtures}')
    started = time.process_time()
    experiments = make_demonstrations(started)
    data = bundle(experiments)
    _budget(started)
    output.mkdir(parents=True, exist_ok=False)
    bundle_path = write_bundle(output / 'experiments.json', data)
    if fixtures is not None:
        make_fixtures(fixtures, started)
    if standalone:
        from .build import build
        build(bundle_path, output / 'The_Presenter.html')
    _budget(started)
    paths = list(output.glob('*'))
    if fixtures is not None:
        paths += list(Path(fixtures).glob('*'))
    manifest = {
        'format': 'universe24-presenter-demonstrations-v1',
        'cpu_budget_seconds': CPU_BUDGET,
        'cpu_seconds': round(time.process_time() - started, 6),
        'experiments': [{
            'id': experiment['id'], 'frames': len(experiment['frames']),
            'transitions': len(experiment['frames']) - 1,
            'side': experiment['side'],
            'coupling_fingerprint': experiment['coupling']['fingerprint'],
            'full_rewind_equal': experiment['provenance']['full_rewind_equal'],
        } for experiment in experiments],
        'source_sha256': {
            'research/presenter/demo.py': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            str(GUIDE.relative_to(ROOT)): hashlib.sha256(GUIDE.read_bytes()).hexdigest(),
        },
        'artifact_sha256': {str(path.resolve().relative_to(ROOT)) if path.resolve().is_relative_to(ROOT)
                           else str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest()
                           for path in sorted(paths) if path.is_file()},
        'scope': 'Six examples exercise generic presentation. They do not establish light, particles or physical measurement.',
    }
    _write(output / 'generation_manifest.json', manifest)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New demonstration directory')
    parser.add_argument('--fixtures', type=Path, help='Optional new browser-fixture directory')
    parser.add_argument('--data-only', action='store_true', help='Create bundles before UI assets are available')
    args = parser.parse_args(argv)
    output = generate(args.output, fixtures=args.fixtures, standalone=not args.data_only)
    print(json.dumps({'output': str(output), 'standalone': not args.data_only}))


if __name__ == '__main__':
    main()
