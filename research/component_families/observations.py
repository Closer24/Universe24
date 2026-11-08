"""Fixed finite behavioral checks, separate from preparation and evolution."""
from itertools import product
from universe24 import State, Channel
from universe24.core.group_2o import DIRECTIONS
from research.components import (BoardSpec, GuideSegment, EvenPacketSource,
                                 LocalizedSixClock, place, finalize)
from . import oracle


def translated(state, delta):
    side = state.cube.side
    return State(state.cube, state.background, {
        tuple((a[i] + delta[i]) % side for i in range(3)) + (a[3],): v
        for a, v in state.cells.items()})


def register_region(origin):
    centers = {(origin[0] + x, origin[1] - 1, origin[2]) for x in (1, 2)}
    nodes = centers | {tuple(x[i] + d[i] for i in range(3))
                       for x in centers for d in DIRECTIONS}
    return tuple(sorted((*x, g) for x in nodes for g in range(48)))


def _probe(case, delay):
    side, m = case['side'], case['side'] // 2
    at = (m - 7, m - 1, m - delay)
    initial = finalize(BoardSpec(side), [
        place(GuideSegment(start=0, stop=side - 1,
                           sockets=tuple(range(m - delay, m - delay + 4)),
                           remainder_pair=(0, 0)), at=(at[0], at[1], 0),
              orientation=13, name='guide'),
        place(EvenPacketSource(), at=at, orientation=13, name='packet')]).initial
    shift = case['preparation'].get('translation', (0, 0, 0))
    return translated(initial, shift)


def _probe_region(case, delay, t):
    side, m = case['side'], case['side'] // 2
    shift = case['preparation'].get('translation', (0, 0, 0))
    return tuple(((m - 7 + dx + shift[0]) % side,
                  (m - 1 + dy + shift[1]) % side,
                  (m - delay + t + dz + shift[2]) % side, g)
                 for dx, dy, dz, g in product((-1, 0, 1), (-1, 0, 1), range(4), range(48)))


def expected_register_checks(case):
    """Map every published behavioral check to its original fixed acceptance flag."""
    original = case['expected_observations']['checks']
    if case['kind'] == 'repeat':
        result = {key: original[key] for key in (
            'written_remainder_hold', 'no_register_native_C_during_write',
            'complete_region_static_during_hold', 'exact_full_reference_clock',
            'read1_incoming_contract', 'read1_native_C_contract', 'read1_outgoing_contract',
            'read2_incoming_contract', 'read2_native_C_contract', 'read2_outgoing_contract')}
        result['restoration_windows'] = (original['complete_region_restored_between_reads'] and
                                         original['complete_region_restored_final6'])
        return result
    mapping = {'written_remainder_hold': 'written_remainder_by2',
               'read1_incoming_contract': 'incoming_contract',
               'read1_native_C_contract': 'native_click_bit_contract',
               'read1_outgoing_contract': 'outgoing_contract',
               'restoration_windows': 'complete_region_restored_all_final6_states'}
    result = {key: original[value] for key, value in mapping.items()}
    result.update({key: original[key] for key in (
        'no_register_native_C_during_write', 'complete_region_static_during_hold',
        'exact_full_reference_clock')})
    return result


def validate_register_checks(case, checks):
    expected = expected_register_checks(case)
    if checks != expected or any(type(v) is not bool for v in checks.values()):
        raise AssertionError('Individual fixed register acceptance outcomes changed')


def register_observations(case, prepared, states):
    params = case['preparation']
    writer, masks = int(params['writer_present']), params['probes_present']
    delays = params['probe_delays']
    origin = tuple(case['origin'])
    region, core = register_region(origin), prepared.ports['register.core']
    first = tuple(sorted(core)[:2])
    at = lambda t, a: tuple(states[t].at(a))
    hold_end = delays[0] - 6
    checks = {
        'written_remainder_hold': all(at(t, a) == (0, 0, 2 * writer)
                                      for t in range(2, hold_end) for a in core),
        'no_register_native_C_during_write': all(
            oracle.click(at(t - 1, a), at(t, a)) is None
            for t in range(1, 9) for a in core),
        'complete_region_static_during_hold': all(
            at(t, a) == at(8, a) for t in range(8, hold_end) for a in region)}
    reads = []
    for i, (delay, present) in enumerate(zip(delays, masks)):
        template = _probe(case, delay)
        incoming = []
        for t in range(delay - 10, delay - 7):
            expected = translated(template, (0, 0, t))
            incoming.append(all(states[t].at(a) == expected.at(a)
                                for a in _probe_region(case, delay, t)))
        accepted = []
        for lag in range(-3, 4):
            matches = []
            for t in range(delay + 8, delay + 12):
                expected = translated(template, (0, 0, t + lag))
                matches.append(all(states[t].at(a) == expected.at(a)
                                   for a in _probe_region(case, delay, t + lag)))
            if all(matches):
                accepted.append(lag)
        t = delay - 3
        native = [{'step': t, 'address': list(a), 'before': list(at(t - 1, a)),
                   'u': oracle.input_at(states[t - 1].cells, a, case['side']),
                   'after': list(at(t, a)),
                   'native_C_kind': oracle.click(at(t - 1, a), at(t, a))} for a in first]
        valid_click = all(r['before'] == [0, 0, 2 * writer] and
                          r['u'] == (-1 if present else 0) and
                          r['native_C_kind'] == (2 if present and not writer else None)
                          for r in native)
        checks[f'read{i+1}_incoming_contract'] = all(incoming) if present else True
        checks[f'read{i+1}_native_C_contract'] = valid_click
        checks[f'read{i+1}_outgoing_contract'] = accepted == ([0] if present and not writer else [])
        reads.append({'incoming': incoming, 'fixed_first_arrival': native,
                      'outgoing_accepted_lags': accepted})
    windows = [(51, 57)] if case['kind'] == 'register' else [(44, 50), (83, 89)]
    checks['restoration_windows'] = all(at(t, a) == at(8, a)
                                        for start, end in windows for t in range(start, end) for a in region)
    ref = tuple(case['reference_origin'])
    templates = [dict(LocalizedSixClock(phase=t).cells) for t in range(6)]
    checks['exact_full_reference_clock'] = all(
        at(t, tuple(ref[i] + a[i] for i in range(3)) + (a[3],)) == v
        for t in range(len(states)) for a, v in templates[t % 6].items())
    refaddr = (*ref, 0)
    events = [t for t in range(1, len(states)) if oracle.click(at(t - 1, refaddr), at(t, refaddr)) is not None]
    ordinals = [sum(t <= delay - 3 for t in events) for delay in delays]
    # Compare the fixed read/output fields to the previously audited originals.
    original = case['expected_observations']
    word = [(t, oracle.click(at(t - 1, refaddr), at(t, refaddr)),
             at(t, refaddr)[1] + at(t - 1, refaddr)[0]) for t in events]
    original_word = [(e['step'], e['kind'], int(e['ell']))
                     for e in original['reference']['native_event_word']]
    expected_ordinals = (original['reference']['ordinals_at_read_steps'] if case['kind'] == 'repeat'
                         else [original['reference']['ordinal_through_first_read_step']])
    if list(refaddr) != original['reference']['address'] or word != original_word or ordinals != expected_ordinals:
        raise AssertionError('Fixed reference address, native event word or ordinal changed')
    if case['kind'] == 'register' and sum(t <= 2 for t in events) != original['reference']['ordinal_through_write_completion_step2']:
        raise AssertionError('Write-completion reference ordinal changed')
    expected_reads = original.get('reads', [{'fixed_first_arrival': original.get('fixed_read'),
                                            'outgoing_accepted_lags': original.get('outgoing_accepted_lags')}])
    for actual, expected in zip(reads, expected_reads):
        if actual['fixed_first_arrival'] != expected['fixed_first_arrival']:
            raise AssertionError('Original fixed native-C readout differs')
        if actual['outgoing_accepted_lags'] != expected['outgoing_accepted_lags']:
            raise AssertionError('Original fixed outgoing-template result differs')
    validate_register_checks(case, checks)
    composition = all(checks.values())
    expected_composition = not (case['kind'] == 'repeat' and all(masks))
    if composition != expected_composition:
        raise AssertionError('Registered composition outcome changed')
    if not expected_composition:
        if reads[1]['incoming'] != [False, False, False] or any(
                r['u'] != 0 for r in reads[1]['fixed_first_arrival']):
            raise AssertionError('Expected second-input interference diagnostic changed')
    return {'checks': checks, 'reads': reads, 'reference_read_ordinals': ordinals,
            'scientific_composition_passed': composition,
            'scope': 'Source-overlap halo clearing; positive C2 means unwritten. '
                     'Repeated-read input failure is retained, not redefined as a successful read.'}


def scatter_observations(case, prepared, states):
    origin, side = tuple(case['origin']), case['side']
    x0 = origin[0]
    guide = State(states[0].cube, states[0].background,
                  {(x, *origin[1:], g): Channel(0, 0, 0) for x in range(side) for g in (0, 14)})
    detector = {a: states[0].at(a) for a in prepared.ports['target.core']}
    def merge(patches):
        cells, seen = dict(guide.cells), set()
        for patch in patches:
            if seen & patch.keys():
                raise AssertionError('Overlapping scatter templates')
            seen.update(patch)
            cells.update(patch)
        return State(guide.cube, guide.background, cells)
    def shifted(patch, dx):
        return {((a[0] + dx) % side, *a[1:]): v for a, v in patch.items()}
    positions = [x0 + 48, x0 + 42, x0 + 27 - 48]
    patches = []
    for pos, velocity in zip(positions, (1, 1, -1)):
        patch = {a: states[48].at(a) for a in states[48].cells.keys() | guide.cells.keys()
                 if (a[0] - pos) % side in range(4) and states[48].at(a) != guide.at(a)}
        if len(patch) != 24 or sum(bool(v.a or v.b) for v in patch.values()) != 8:
            raise AssertionError('Incomplete scatter packet')
        one = merge([patch])
        if oracle.step(one.cells, side) != dict(translated(one, (velocity, 0, 0)).cells):
            raise AssertionError('Isolated scatter packet translation failed')
        patches.append(patch)
    if patches[1] != shifted(patches[0], -6):
        raise AssertionError('Delayed full packet differs')
    mirror = {((positions[2] + 3 - ((a[0] - positions[0]) % side)) % side, *a[1:]): v
              for a, v in patches[0].items()}
    if patches[2] != mirror:
        raise AssertionError('Reflected full packet differs')
    for t in range(24, 49):
        if merge([detector, *[shifted(p, v * (t - 48)) for p, v in zip(patches, (1, 1, -1))]]) != states[t]:
            raise AssertionError('Whole-state scatter factorization failed')
    return {'complete_factorization_states': [24, 48], 'packet_sizes': [24, 24, 24],
            'velocities': [1, 1, -1], 'one_step_translation_verified': True,
            'scope': 'Prepared three-packet scatterer; target resets. No retained remote memory.'}


def observe(case, prepared, states):
    kind = case['kind']
    if kind in ('register', 'repeat'):
        return register_observations(case, prepared, states)
    if kind == 'scatterer':
        if not case['preparation'].get('target_present', True):
            if not all(s == translated(states[0], (t, 0, 0)) for t, s in enumerate(states)):
                raise AssertionError('Source-only scatterer control changed')
            return {'full_state_translation_every_step': True, 'target_present': False}
        return scatter_observations(case, prepared, states)
    if kind in ('six', 'five'):
        period = 6 if kind == 'six' else 5
        if not all(states[t] == states[t % period] for t in range(len(states))):
            raise AssertionError('Complete clock recurrence failed')
        if any(states[t] == states[0] for t in range(1, period)):
            raise AssertionError('Claimed clock period is not minimal')
        return {'minimal_full_state_period': period}
    if kind == 'packet':
        if not all(state == translated(states[0], (t, 0, 0)) for t, state in enumerate(states)):
            raise AssertionError('Complete packet translation failed')
        return {'full_state_translation_every_step': True, 'lattice_velocity': [1, 0, 0]}
    params = case['preparation']
    masks = params['first_active'], params['second_active']
    if all(masks):
        if not all(states[t] == states[t % 6] for t in range(len(states))):
            raise AssertionError('Joint cooperative period failed')
    elif any(masks):
        if not any(states[2].at(a).a or states[2].at(a).b for a in prepared.ports['body.shared']):
            raise AssertionError('Single-core shared-halo failure disappeared')
    elif any(s != states[0] for s in states):
        raise AssertionError('Counter-masked hardware must remain static')
    return {'joint_period_six': all(masks), 'single_core_shared_halo_leak_step2': sum(masks) == 1}
