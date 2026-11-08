"""Lossless, generic, read-only recording for The Presenter.

The reference Engine is the only producer of forward states. This module records
complete sparse states, audits reversibility and exports portable decimal strings.
It never changes the process-wide Python integer conversion guard.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

from universe24.core import Coupling, Engine, State
from universe24.core.group_2o import DIRECTIONS
from universe24.core.state import Channel, Cube
from universe24.experiments.config import from_dict

ROOT = Path(__file__).resolve().parents[2]
FORMAT = 'universe24-presenter-v1'
MODEL = 'universe24-2O-body-013-v1'
SAFE_INTEGER = 2**53 - 1
MAX_FRAMES = 10000
MAX_CELLS = 500_000
MAX_BYTES = 64 * 1024 * 1024
MAX_SECONDS = 120
MAX_COUNTER_DIGITS = 100_000
MAX_EXPERIMENTS = 64
MAX_READOUTS = 256
MAX_CLAUSES = 1024
_DECIMAL = re.compile(r'(?:0|-[1-9][0-9]*|[1-9][0-9]*)\Z')


class ResourceLimitError(ValueError):
    """The explicit recording budget cannot hold this complete experiment."""


def decimal_string(value):
    """Convert an arbitrary Python integer without the global decimal guard."""
    if type(value) is not int:
        raise TypeError('Counter must be a Python integer')
    if value == 0:
        return '0'
    negative = value < 0
    value = abs(value)
    chunks = []
    while value:
        value, chunk = divmod(value, 1_000_000_000)
        chunks.append(chunk)
    digits = str(chunks[-1]) + ''.join(f'{chunk:09d}' for chunk in reversed(chunks[:-1]))
    if len(digits) > MAX_COUNTER_DIGITS:
        raise ResourceLimitError('Counter exceeds the explicit 100000-digit Presenter limit')
    return ('-' if negative else '') + digits


def parse_decimal(text):
    """Read a canonical decimal string using only at-most-nine-digit int calls."""
    if type(text) is not str or _DECIMAL.fullmatch(text) is None:
        raise ValueError('Expected a canonical decimal integer string')
    negative = text.startswith('-')
    digits = text[1:] if negative else text
    if len(digits) > MAX_COUNTER_DIGITS:
        raise ResourceLimitError('Counter exceeds the explicit 100000-digit Presenter limit')
    value = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start:start + 9]
        value = value * 10**len(chunk) + int(chunk)
    return -value if negative else value


def _json_int(text):
    # JSON permits -0; normalize it to the same integer as the reference loader.
    return 0 if text == '-0' else parse_decimal(text)


def loads_strict(text):
    def members(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON member: {key}')
            result[key] = value
        return result

    def invalid_number(token):
        raise ValueError('Native experiment/checkpoint numbers must be integers')

    return json.loads(text, object_pairs_hook=members, parse_int=_json_int,
                      parse_float=invalid_number, parse_constant=invalid_number)


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)


def _safe(value, name, minimum=0):
    if type(value) is not int or not minimum <= value <= SAFE_INTEGER:
        raise ValueError(f'{name} must be an integer in {minimum}..{SAFE_INTEGER}')
    return value


def _limits(max_frames, max_cells, max_bytes, max_seconds):
    for value, name in ((max_frames, 'max_frames'), (max_cells, 'max_cells'),
                        (max_bytes, 'max_bytes')):
        if type(value) is not int or value <= 0:
            raise ValueError(f'{name} must be a positive integer')
    if type(max_seconds) not in (int, float) or not 0 < max_seconds < float('inf'):
        raise ValueError('max_seconds must be finite and positive')
    return {'max_frames': max_frames, 'max_cells': max_cells,
            'max_bytes': max_bytes, 'max_seconds': max_seconds,
            'max_counter_digits': MAX_COUNTER_DIGITS}


def _deadline(started, limits):
    if time.monotonic() - started > limits['max_seconds']:
        raise ResourceLimitError('Recording time budget exceeded; no partial run is accepted')


def _core_hashes():
    files = sorted((ROOT / 'universe24').rglob('*.py')) + [Path(__file__).resolve()]
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in files}


def _provenance(limits, mode):
    def git(*args):
        try:
            return subprocess.check_output(['git', *args], cwd=ROOT, text=True,
                                           stderr=subprocess.DEVNULL).strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    return {'recorder': FORMAT, 'mode': mode, 'source_sha256': _core_hashes(),
            'checkout_commit': git('rev-parse', 'HEAD'),
            'working_tree_dirty': bool(git('status', '--porcelain')),
            'limits': limits,
            'observation_policy': 'Read-only; no state or coupling intervention.'}


def _finish_provenance(provenance, *, full_rewind):
    if provenance['source_sha256'] != _core_hashes():
        raise ValueError('Source changed during recording; output is not accepted')
    provenance['source_unchanged_during_capture'] = True
    provenance['full_rewind_equal'] = full_rewind


def coupling_data(coupling):
    """Export the actual fixed tensor, and verify the current reference family."""
    if not isinstance(coupling, Coupling):
        raise TypeError('Expected a reference Coupling')
    expected = Coupling(coupling.body_signs)
    if coupling.ports != expected.ports or coupling.weights != expected.weights:
        raise ValueError('Coupling is not the declared fixed reference tensor')
    return {'model': MODEL, 'body_signs': list(coupling.body_signs),
            'directions': [list(d) for d in DIRECTIONS],
            'ports': [list(row) for row in coupling.ports],
            'weights': [list(row) for row in coupling.weights],
            'fingerprint': coupling.fingerprint}


def _background(state):
    return [decimal_string(state.background.a), decimal_string(state.background.b),
            state.background.r]


def state_data(state):
    return {'side': _safe(state.cube.side, 'side', 3), 'background': _background(state),
            'cells': [[*address, decimal_string(triple.a), decimal_string(triple.b), triple.r]
                      for address, triple in sorted(state.cells.items())]}


def state_sha256(state):
    return hashlib.sha256(canonical(state_data(state)).encode('ascii')).hexdigest()


def _readouts(readouts, cube):
    values = [] if readouts is None else copy.deepcopy(readouts)
    if not isinstance(values, list) or len(values) > MAX_READOUTS:
        raise ValueError(f'readouts must be a list of at most {MAX_READOUTS} declarations')
    ids = set()
    clause_count = 0
    for readout in values:
        if not isinstance(readout, dict) or set(readout) != {'id', 'label', 'kind', 'clauses'}:
            raise ValueError('Readout requires id, label, kind and clauses only')
        if not isinstance(readout['id'], str) or not readout['id'] or readout['id'] in ids:
            raise ValueError('Readout IDs must be nonempty and unique')
        ids.add(readout['id'])
        if not isinstance(readout['label'], str) or readout['kind'] != 'all_equal':
            raise ValueError('Unsupported readout declaration')
        if not isinstance(readout['clauses'], list) or not readout['clauses']:
            raise ValueError('Readout must have at least one fixed clause')
        clause_count += len(readout['clauses'])
        for clause in readout['clauses']:
            if not isinstance(clause, dict) or set(clause) != {'address', 'component', 'equals'}:
                raise ValueError('Readout clause requires address, component and equals only')
            clause['address'] = list(cube.validate_address(clause['address']))
            if clause['component'] not in ('a', 'b', 'r'):
                raise ValueError('Readout component must be a, b or r')
            target = parse_decimal(clause['equals'])
            if clause['component'] == 'r' and not 0 <= target < 6:
                raise ValueError('Remainder readout target must be 0..5')
    if clause_count > MAX_CLAUSES:
        raise ResourceLimitError(f'At most {MAX_CLAUSES} readout clauses are supported')
    return values


def _view(view, initial):
    if view is None:
        if initial.cells:
            first = min(initial.cells)
            return {'position': list(first[:3]), 'channel': first[3]}
        return {'position': [initial.cube.side // 2] * 3, 'channel': 0}
    if not isinstance(view, dict) or set(view) != {'position', 'channel'}:
        raise ValueError('view requires position and channel only')
    if not isinstance(view['position'], (list, tuple)) or len(view['position']) != 3:
        raise ValueError('view.position must contain three coordinates')
    address = initial.cube.validate_address((*view['position'], view['channel']))
    return {'position': list(address[:3]), 'channel': address[3]}


def _experiment(engine, initial, id, title, description, readouts, view, provenance):
    if not isinstance(engine, Engine) or not isinstance(initial, State):
        raise TypeError('Expected Engine and State')
    if not isinstance(id, str) or not id or not isinstance(title, str) or not isinstance(description, str):
        raise ValueError('Experiment id must be nonempty; title and description must be strings')
    return {'id': id, 'title': title, 'description': description,
            'side': _safe(initial.cube.side, 'side', 3), 'background': _background(initial),
            'coupling': coupling_data(engine.coupling), 'frames': [],
            'readouts': _readouts(readouts, initial.cube), 'view': _view(view, initial),
            'provenance': provenance}


def _append_frame(experiment, state, step, forward, inverse, totals, limits):
    if len(experiment['frames']) >= limits['max_frames']:
        raise ResourceLimitError('Frame budget exceeded; no frames were silently dropped')
    totals['cells'] += len(state.cells)
    if totals['cells'] > limits['max_cells']:
        raise ResourceLimitError('Complete sparse-cell budget exceeded; no channels were omitted')
    physical = state_data(state)
    encoded = canonical(physical)
    totals['bytes'] += len(encoded)
    if totals['bytes'] > limits['max_bytes']:
        raise ResourceLimitError('Serialized-state byte budget exceeded; no counters were truncated')
    experiment['frames'].append({'step': _safe(step, 'step'), 'cells': physical['cells'],
        'state_sha256': hashlib.sha256(encoded.encode('ascii')).hexdigest(),
        'audit': {'forward_equal': forward, 'inverse_equal': inverse}})


def _size_check(data, limits):
    if len(canonical(data).encode('ascii')) > limits['max_bytes']:
        raise ResourceLimitError('Portable JSON byte budget exceeded; output was not truncated')


def capture(engine, initial, steps, *, id='experiment', title='Experiment',
            description='', start_step=0, readouts=None, view=None,
            max_frames=MAX_FRAMES, max_cells=MAX_CELLS, max_bytes=MAX_BYTES,
            max_seconds=MAX_SECONDS):
    """Record any reference preparation; every full state and remainder is kept."""
    steps = _safe(steps, 'steps')
    start_step = _safe(start_step, 'start_step')
    _safe(start_step + steps, 'final step')
    limits = _limits(max_frames, max_cells, max_bytes, max_seconds)
    if steps + 1 > max_frames:
        raise ResourceLimitError('Requested steps exceed the complete-frame budget')
    started = time.monotonic()
    provenance = _provenance(limits, 'capture')
    result = _experiment(engine, initial, id, title, description, readouts, view, provenance)
    state = initial
    totals = {'cells': 0, 'bytes': 0}
    _append_frame(result, state, start_step, None, None, totals, limits)
    for offset in range(1, steps + 1):
        _deadline(started, limits)
        next_state = engine.advance(state)
        inverse_equal = engine.rewind(next_state) == state
        if not inverse_equal:
            raise ValueError(f'Full-state inverse failed at step {start_step + offset}')
        _append_frame(result, next_state, start_step + offset, True, True, totals, limits)
        state = next_state
    for _ in range(steps):
        _deadline(started, limits)
        state = engine.rewind(state)
    if state != initial:
        raise ValueError('Complete trajectory rewind did not recover the preparation')
    _finish_provenance(provenance, full_rewind=True)
    provenance['initial_state_sha256'] = result['frames'][0]['state_sha256']
    _size_check(result, limits)
    return result


def _checkpoint(data):
    required = {'format', 'completed_steps', 'coupling_fingerprint', 'experiment'}
    if not isinstance(data, dict) or set(data) != required:
        raise ValueError('Expected a complete native Universe24 checkpoint')
    if data['format'] != 'universe24-checkpoint-v1':
        raise ValueError('Unsupported checkpoint format')
    step = _safe(data['completed_steps'], 'completed_steps')
    experiment = from_dict(data['experiment'])
    _safe(experiment.initial.cube.side, 'side', 3)
    if data['coupling_fingerprint'] != experiment.engine.coupling.fingerprint:
        raise ValueError('Checkpoint coupling fingerprint mismatch')
    return experiment.engine, experiment.initial, step


def _read_bytes(path, max_bytes):
    path = Path(path)
    if path.stat().st_size > max_bytes:
        raise ResourceLimitError('Input byte budget exceeded')
    with path.open('rb') as handle:
        raw = handle.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ResourceLimitError('Input byte budget exceeded')
    return raw


def _read_file(path, max_bytes):
    return _read_bytes(path, max_bytes).decode('utf-8-sig')


def from_trace(path, *, id='experiment', title='Recorded experiment', description='',
               readouts=None, view=None, max_frames=MAX_FRAMES, max_cells=MAX_CELLS,
               max_bytes=MAX_BYTES, max_seconds=MAX_SECONDS):
    """Import complete consecutive native checkpoints, including a single snapshot."""
    limits = _limits(max_frames, max_cells, max_bytes, max_seconds)
    started = time.monotonic()
    raw = _read_bytes(path, max_bytes)
    text = raw.decode('utf-8-sig')
    try:
        single = loads_strict(text)
    except json.JSONDecodeError as exc:
        if exc.msg != 'Extra data':
            raise
        documents = [loads_strict(line) for line in text.splitlines() if line.strip()]
    else:
        documents = [single]
    if not documents or len(documents) > max_frames:
        raise ResourceLimitError('Trace must contain 1..max_frames complete snapshots')
    engine, initial, start_step = _checkpoint(documents[0])
    provenance = _provenance(limits, 'native_trace' if len(documents) > 1 else 'native_checkpoint')
    provenance['input_sha256'] = hashlib.sha256(raw).hexdigest()
    result = _experiment(engine, initial, id, title, description, readouts, view, provenance)
    totals = {'cells': 0, 'bytes': 0}
    state = initial
    for offset, document in enumerate(documents):
        _deadline(started, limits)
        current_engine, current, step = _checkpoint(document)
        if step != start_step + offset:
            raise ValueError('Trace steps must be consecutive; gaps are not interpolated')
        if current.cube != initial.cube or current.background != initial.background:
            raise ValueError('Geometry and background must remain fixed through a trace')
        if current_engine.coupling != engine.coupling:
            raise ValueError('Coupling must remain fixed through a trace')
        if offset:
            if engine.advance(state) != current:
                raise ValueError(f'Full-state forward mismatch at trace step {step}')
            if engine.rewind(current) != state:
                raise ValueError(f'Full-state inverse mismatch at trace step {step}')
        _append_frame(result, current, step, True if offset else None,
                      True if offset else None, totals, limits)
        state = current
    for _ in range(len(documents) - 1):
        _deadline(started, limits)
        state = engine.rewind(state)
    if state != initial:
        raise ValueError('Complete imported trajectory rewind failed')
    _finish_provenance(provenance, full_rewind=True)
    provenance['initial_state_sha256'] = result['frames'][0]['state_sha256']
    _size_check(result, limits)
    return result


def _portable_state(frame, side, background):
    if not isinstance(frame, dict) or set(frame) != {'step', 'cells', 'state_sha256', 'audit'}:
        raise ValueError('Invalid Presenter frame fields')
    _safe(frame['step'], 'frame step')
    if not isinstance(frame['cells'], list):
        raise ValueError('Frame cells must be a list')
    cube = Cube(side)
    cells = {}
    previous = None
    for row in frame['cells']:
        if not isinstance(row, list) or len(row) != 7:
            raise ValueError('Sparse rows require x,y,z,g,a,b,r')
        address = cube.validate_address(row[:4])
        if previous is not None and address <= previous:
            raise ValueError('Sparse addresses must be sorted and unique')
        previous = address
        a, b = parse_decimal(row[4]), parse_decimal(row[5])
        if type(row[6]) is not int or not 0 <= row[6] < 6:
            raise ValueError('Remainder must be an integer in 0..5')
        triple = Channel(a, b, row[6])
        if triple == background:
            raise ValueError('Sparse rows must omit exact background triples')
        cells[address] = triple
    state = State(cube, background, cells)
    if frame['state_sha256'] != state_sha256(state):
        raise ValueError('Portable state SHA-256 mismatch')
    return state


def validate_bundle(data, *, max_frames=MAX_FRAMES, max_cells=MAX_CELLS,
                    max_bytes=MAX_BYTES, max_seconds=MAX_SECONDS):
    """Validate complete portable states before writing; return the same data."""
    limits = _limits(max_frames, max_cells, max_bytes, max_seconds)
    started = time.monotonic()
    if not isinstance(data, dict) or set(data) != {'format', 'title', 'catalog', 'experiments'}:
        raise ValueError('Invalid Presenter bundle fields')
    if data['format'] != FORMAT or not isinstance(data['title'], str):
        raise ValueError('Unsupported Presenter bundle format/title')
    catalog = [coupling_data(Coupling(signs)) for signs in product((-1, 1), repeat=3)]
    if canonical(data['catalog']) != canonical(catalog):
        raise ValueError('Portable catalog must contain all eight reference couplings in sign order')
    experiments = data['experiments']
    if not isinstance(experiments, list) or len(experiments) > MAX_EXPERIMENTS:
        raise ResourceLimitError(f'At most {MAX_EXPERIMENTS} experiments are supported')
    total_cells = 0
    ids = set()
    for experiment in experiments:
        _deadline(started, limits)
        required = {'id', 'title', 'description', 'side', 'background', 'coupling',
                    'frames', 'readouts', 'view', 'provenance'}
        if not isinstance(experiment, dict) or set(experiment) != required:
            raise ValueError('Invalid Presenter experiment fields')
        side = _safe(experiment['side'], 'side', 3)
        bg = experiment['background']
        if (not isinstance(bg, list) or len(bg) != 3 or bg[:2] != ['0', '0']
                or type(bg[2]) is not int or not 0 <= bg[2] < 6):
            raise ValueError('Portable background must be ["0","0",r] with r in0..5')
        background = Channel(0, 0, bg[2])
        coupling = experiment['coupling']
        if not isinstance(coupling, dict) or canonical(coupling) not in {canonical(item) for item in catalog}:
            raise ValueError('Portable coupling is not in the fixed reference family')
        engine = Engine(Coupling(tuple(coupling['body_signs'])))
        frames = experiment['frames']
        if not isinstance(frames, list) or not 1 <= len(frames) <= max_frames:
            raise ResourceLimitError('Each experiment needs 1..max_frames complete snapshots')
        if not isinstance(experiment['provenance'], dict):
            raise ValueError('Experiment provenance must be an object')
        initial = _portable_state(frames[0], side, background)
        _experiment(engine, initial, experiment['id'], experiment['title'],
                    experiment['description'], experiment['readouts'], experiment['view'], {})
        if experiment['id'] in ids:
            raise ValueError('Experiment IDs must be unique')
        ids.add(experiment['id'])
        state = initial
        for offset, frame in enumerate(frames):
            _deadline(started, limits)
            total_cells += len(frame['cells'])
            if total_cells > max_cells:
                raise ResourceLimitError('Bundle complete sparse-cell budget exceeded')
            current = initial if offset == 0 else _portable_state(frame, side, background)
            if frame['step'] != frames[0]['step'] + offset:
                raise ValueError('Portable frame steps must be consecutive')
            expected_audit = {'forward_equal': True if offset else None,
                              'inverse_equal': True if offset else None}
            if canonical(frame['audit']) != canonical(expected_audit):
                raise ValueError('Portable frame audit must match its verified transition scope')
            if offset and (engine.advance(state) != current or engine.rewind(current) != state):
                raise ValueError('Portable trace fails complete-state Rule3 verification')
            state = current
    _size_check(data, limits)
    return data


def bundle(experiments, *, title='The Presenter'):
    """Package experiments without experiment-specific presentation assumptions."""
    data = {'format': FORMAT, 'title': title,
            'catalog': [coupling_data(Coupling(signs)) for signs in product((-1, 1), repeat=3)],
            'experiments': list(experiments)}
    return validate_bundle(data)


def write_bundle(path, data, *, max_frames=MAX_FRAMES, max_cells=MAX_CELLS,
                 max_bytes=MAX_BYTES, max_seconds=MAX_SECONDS):
    """Validate first, then publish atomically without overwriting any existing file."""
    path = Path(path)
    if path.exists():
        raise FileExistsError(f'Refusing to overwrite {path}')
    validate_bundle(data, max_frames=max_frames, max_cells=max_cells,
                    max_bytes=max_bytes, max_seconds=max_seconds)
    encoded = (canonical(data) + '\n').encode('ascii')
    if len(encoded) > max_bytes:
        raise ResourceLimitError('Final output byte budget exceeded')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.presenter-', suffix='.tmp',
                                         dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        # Same-directory hard link is an atomic create-if-absent operation.
        os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--config', type=Path)
    source.add_argument('--checkpoint', type=Path)
    source.add_argument('--trace', type=Path)
    parser.add_argument('--steps', type=int)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--title', default='Experiment')
    parser.add_argument('--id', default='experiment')
    parser.add_argument('--max-frames', type=int, default=MAX_FRAMES)
    parser.add_argument('--max-cells', type=int, default=MAX_CELLS)
    parser.add_argument('--max-bytes', type=int, default=MAX_BYTES)
    parser.add_argument('--max-seconds', type=float, default=MAX_SECONDS)
    args = parser.parse_args(argv)
    limits = {'max_frames': args.max_frames, 'max_cells': args.max_cells,
              'max_bytes': args.max_bytes, 'max_seconds': args.max_seconds}
    try:
        if args.output.exists():
            raise FileExistsError(f'Refusing to overwrite {args.output}')
        _limits(**limits)
        if args.trace:
            if args.steps is not None:
                raise ValueError('--steps cannot alter an imported trace')
            experiment = from_trace(args.trace, id=args.id, title=args.title, **limits)
        elif args.checkpoint:
            engine, initial, start = _checkpoint(loads_strict(_read_file(args.checkpoint, args.max_bytes)))
            experiment = capture(engine, initial, 0 if args.steps is None else args.steps,
                                 id=args.id, title=args.title, start_step=start, **limits)
        else:
            configuration = from_dict(loads_strict(_read_file(args.config, args.max_bytes)))
            experiment = capture(configuration.engine, configuration.initial,
                                 configuration.steps if args.steps is None else args.steps,
                                 id=args.id, title=args.title, **limits)
        data = {'format': FORMAT, 'title': 'The Presenter',
                'catalog': [coupling_data(Coupling(signs)) for signs in product((-1, 1), repeat=3)],
                'experiments': [experiment]}
        write_bundle(args.output, data, **limits)
    except (ValueError, TypeError, OSError, ResourceLimitError) as exc:
        parser.exit(2, f'The Presenter: {exc}\n')
    print(json.dumps({'output': str(args.output), 'experiments': 1,
                      'frames': len(experiment['frames']),
                      'full_state_verified': True, 'core_modified': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
