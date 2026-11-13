"""Retained light-to-memory exchange in the installed Rule3 runtime.

This is an exactly conservative, reversible detector precursor. It transfers
integer stream amplitudes to retained memory during an internally transported
arming pulse. It does not establish photon quantization, a Born measure, a
material clock, recoil stress or a general Maxwell/matter coupling.
"""
from functools import lru_cache
import gzip
import hashlib
from pathlib import Path

import numpy as np

from .algebra.group_2o import group
from .core import GearType, State, Tensor, exact_json
from .core.symmetry import CONTRACT, require_equivariant
from .light import orientations
from .system.bundle import create_bundle
from .system.decoder import default_protocol

MODEL_ID = 'universe24/light-memory48'
MEMORY_PORT, ARM_PORT, SELECTOR_PORT = 1, 6, 2
ZERO = (0, 0, 0)


def roles(root):
    if type(root) is not int or not 0 <= root < 48:
        raise ValueError('root must be an exact 2O label in 0..47')
    row = group().multiplication[root]
    return {'light': root, 'memory': row[MEMORY_PORT], 'arming': row[ARM_PORT],
            'selector': row[group().multiplication[MEMORY_PORT][SELECTOR_PORT]]}


@lru_cache(maxsize=1)
def detector_tensor():
    """One uniform, quadratic, one-face, exactly 2O-covariant polynomial."""
    algebra = group()
    terms = []
    def term(target, coefficient, *factors):
        terms.append((target, coefficient, [(g, offset, 'b') for g, offset in factors]))
    for g, (n, _, _) in enumerate(orientations()):
        minus = tuple(-v for v in n)
        m, c, selector = (algebra.multiplication[g][p]
                          for p in (MEMORY_PORT, ARM_PORT, SELECTOR_PORT))
        # Free transport, or a stationary history where a retained selector is 1.
        for offset in (minus, n):
            term(g, 3, (g, offset))
            term(g, -3, (selector, ZERO), (g, offset))
        term(g, 6, (selector, ZERO), (g, ZERO))
        # Forward controlled exchange: arming uses the complete OLD snapshot.
        term(g, 3, (c, ZERO), (m, ZERO))
        term(g, -3, (c, ZERO), (g, minus))
        term(m, 3, (c, ZERO), (g, minus))
        term(m, -3, (c, ZERO), (m, ZERO))
        # Inverse exchange with the counterpropagating arming history.
        term(g, 3, (c, ZERO), (m, n))
        term(g, -3, (c, ZERO), (g, n))
        term(m, 3, (c, minus), (g, ZERO))
        term(m, -3, (c, minus), (m, ZERO))
    law = Tensor([GearType(f'detection_g{g:02d}', 'official') for g in range(48)],
                 terms, strict_support=True)
    require_equivariant(law)
    return law


def sector_map(values, L, root, *, inverse=False):
    """Preparation/validation oracle only. Engine alone advances retained state."""
    if type(inverse) is not bool:
        raise ValueError('inverse must be Boolean')
    values = np.asarray(values, dtype=object)
    if values.shape != (48, L ** 3):
        raise ValueError('all 48 complete rows are required')
    ports = roles(root)
    if any(type(v) is not int and not isinstance(v, np.integer) for v in values.flat):
        raise ValueError('exact integer rows required')
    if np.any(np.delete(values, list(ports.values()), axis=0)):
        raise ValueError('state is outside the declared four-role preparation')
    if np.any(values[ports['selector']] != 1):
        raise ValueError('retained memory selector must be uniformly one')
    p, m, c = (values[ports[name]].reshape(L, L, L) for name in ('light', 'memory', 'arming'))
    if np.any((c != 0) & (c != 1)):
        raise ValueError('arming occupancy must be Boolean')
    direction = orientations()[root][0]
    axis = next(i for i, value in enumerate(direction) if value)
    sign = direction[axis]
    output = values.copy()
    if inverse:
        previous_p = np.roll(p, -sign, axis=axis)
        next_m = np.roll(m, -sign, axis=axis)
        previous_c = np.roll(c, sign, axis=axis)
        rows = (previous_p + c * (next_m - previous_p), m + previous_c * (p - m), previous_c)
    else:
        incoming = np.roll(p, sign, axis=axis)
        rows = (incoming + c * (m - incoming), m + c * (incoming - m), np.roll(c, -sign, axis=axis))
    for name, row in zip(('light', 'memory', 'arming'), rows):
        output[ports[name]] = row.reshape(-1)
    return output


def make_detector_bundle(*, L=13, root=0, light_position=2, arm_position=7,
                         amplitude=1, armed=True):
    """Complete planar preparation; every selector, arming pulse and carry retained."""
    for name, value, minimum in (('L', L, 3), ('light_position', light_position, 0),
                                 ('arm_position', arm_position, 0), ('amplitude', amplitude, 0)):
        if type(value) is not int or value < minimum:
            raise ValueError(f'{name} must be an exact integer >= {minimum}')
    if light_position >= L or arm_position >= L or type(armed) is not bool:
        raise ValueError('positions must fit the lattice and armed must be Boolean')
    ports = roles(root)
    direction = orientations()[root][0]
    axis = next(i for i, value in enumerate(direction) if value)
    coordinates = np.indices((L, L, L)).reshape(3, -1)
    values = np.zeros((48, L ** 3), dtype=object)
    values[ports['light']] = amplitude * (coordinates[axis] == light_position).astype(object)
    values[ports['arming']] = int(armed) * (coordinates[axis] == arm_position).astype(object)
    values[ports['selector']] = 1
    previous = sector_map(values, L, root, inverse=True)
    carries = np.asarray([(g + coordinates.sum(axis=0)) % 6 for g in range(48)])
    seed = State(L, previous, values, carries)
    law = detector_tensor()
    channels = [{'index': g, 'name': gear.name, 'label': gear.label,
                 'owner': 'shared-light-memory', 'purpose': 'full 2O regular representation; a,b,r retained'}
                for g, gear in enumerate(law.gears)]
    model = {'id': MODEL_ID, 'version': '1', 'role': 'universe-candidate', 'symmetry': CONTRACT,
             'domain': 'planar integer-amplitude transport and reversible memory exchange',
             'preparation': {'L': L, 'root': root, 'light_position': light_position,
                             'arm_position': arm_position, 'amplitude': amplitude, 'armed': armed},
             'roles': ports, 'energy_account': 'sum(light**2 + memory**2); dimensionless, not calibrated hbar*omega',
             'scope': ['48 complete dynamical channels; no external arming or resets',
                       'memory persists until the retained arming pulse revisits it',
                       'counterpropagating arming pulse is a prepared resource, not a material clock',
                       'no photon-number calibration, Born measure, recoil stress or Einstein backreaction']}
    return create_bundle(law, seed, channels=channels, protocol=default_protocol(), model=model)


def energy_account(state, root):
    """Exact positive quadratic account on the declared exchange sector."""
    ports = roles(root)
    result = {name: sum(int(v) ** 2 for v in state.b[ports[name]])
              for name in ('light', 'memory', 'arming', 'selector')}
    result['light_plus_memory'] = result['light'] + result['memory']
    return result


def observe_detector_run(directory):
    """Replay first, then interpret complete retained exchanges, including releases.

    This observer cannot update the Engine, invent detection probabilities or
    change the canonical arithmetic click stream. The reported energy units
    are a conserved model account, not joules or photon numbers.
    """
    from .system.bundle import load_bundle
    from .system.runtime import verify_run

    directory = Path(directory)
    verified = verify_run(directory)
    bundle = load_bundle(directory / 'bundle')
    if bundle.model.get('id') != MODEL_ID:
        raise ValueError('a prepared light-memory bundle is required')
    preparation = bundle.model.get('preparation', {})
    expected = make_detector_bundle(**preparation)
    if expected.bundle_id != bundle.bundle_id:
        raise ValueError('detector interpretation differs from complete prepared inputs')
    root = preparation['root']
    ports = roles(root)
    direction = orientations()[root][0]
    axis = next(i for i, value in enumerate(direction) if value)
    sign, L = direction[axis], bundle.seed.L
    initial = energy_account(bundle.seed, root)
    accounts = [dict(step=0, **{k: str(v) for k, v in initial.items()})]
    arithmetic_ids = {}
    with gzip.open(directory / 'clicks.jsonl.gz', 'rt') as stream:
        for line in stream:
            event = exact_json.loads(line)
            if event['channel'] == ports['memory']:
                arithmetic_ids[event['step'], event['node']] = event['event_id']
    events, opportunities = [], 0
    outcomes = dict(capture=0, release=0, exchange=0, no_transfer=0)
    with gzip.open(directory / 'full_trace.jsonl.gz', 'rt') as stream:
        for tick, line in enumerate(stream, 1):
            transition = exact_json.loads(line)
            before, after = (State.from_dict(transition[bank]) for bank in ('before', 'after'))
            next_values = sector_map(before.b, L, root)
            if (not np.array_equal(after.b, next_values)
                    or not np.array_equal(before.a, sector_map(before.b, L, root, inverse=True))):
                raise ValueError('saved trajectory left the declared exchange sector')
            account = energy_account(after, root)
            if any(account[k] != initial[k] for k in ('light_plus_memory', 'arming', 'selector')):
                raise ValueError('retained excitation account changed')
            accounts.append(dict(step=tick, **{k: str(v) for k, v in account.items()}))
            incoming = np.roll(before.b[ports['light']].reshape(L, L, L), sign, axis=axis).reshape(-1)
            for node in np.flatnonzero(before.b[ports['arming']]):
                node = int(node)
                opportunities += 1
                arriving, stored = int(incoming[node]), int(before.b[ports['memory'], node])
                if arriving == stored:
                    outcomes['no_transfer'] += 1
                    continue
                kind = 'capture' if stored == 0 else 'release' if arriving == 0 else 'exchange'
                outcomes[kind] += 1
                events.append({'step': tick, 'node': node, 'xyz': list(before.lattice.coords(node)),
                               'kind': kind, 'incoming_amplitude': str(arriving),
                               'memory_before': str(stored), 'memory_after': str(arriving),
                               'outgoing_amplitude': str(stored),
                               'energy_to_memory': str(arriving ** 2 - stored ** 2),
                               'arithmetic_event_id': arithmetic_ids.get((tick, node)),
                               'photon_number': None})
    return {'schema': 'universe24/light-memory-observation/1', 'run_id': verified['run_id'],
            'bundle_id': verified['bundle_id'], 'tensor_hash': verified['tensor_hash'],
            'model_contract': verified['model_contract'], 'steps': verified['steps'],
            'observer_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'channels': 48, 'retained_integers_per_node': 144,
            'arithmetic_click_count': verified['click_count'], 'arming_opportunities': opportunities,
            'outcomes': outcomes, 'events': events, 'accounts': accounts,
            'checks': {'complete_replay': 'passed', 'independent_exchange_rule': 'passed',
                       'exact_excitation_account': 'passed', '2o_covariance': 'passed'},
            'interpretation': 'retained amplitude transfer; capture events are not calibrated photon counts',
            'memory_lifetime': 'until the retained arming pulse revisits; releases are included',
            'physical_gates': {'energy_frequency_calibration': 'not_tested', 'photon_number': 'not_tested',
                               'born_measure': 'not_tested', 'single_photon_anticorrelation': 'not_tested',
                               'material_clock_and_recoil': 'not_tested', 'general_physical_acceptance': 'blocked'}}
