"""Optional fixed-tensor clock interaction experiment; not a gravity model.

The recipe is frozen before the run. Every evolving register still uses the
generic scalar Rule3 engine. Complete declared quadratic forms couple sector
clocks to fields, springs connect those clocks to a master, and a sum bridge
lets matched detector records feed back without breaking their difference lock.

Examples::

    python -m universe24.tools.connected_clocks --steps 1000
    python -m universe24.tools.connected_clocks --control forward --L 4 --steps 300
    python -m universe24.tools.connected_clocks --control off --steps 300

The default source has storage-local reads but some terms touch multiple
physical edges. An explicit --strict-edge-stiffness builds a different tensor
with node mediators; it is not an equivalent rewriting of that source.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import json
from pathlib import Path
import time

import numpy as np

from ..core import Engine, State, Tensor
from ..core.tensor import compose
from ..layers.clock_bridge import build_clock_record_bridge
from ..layers.clock_network import build_clock_network, one_invariant_ports
from ..layers.one import one_system
from ..layers.resolution import lift_tensor
from ..observe.one import state_hash
from ..observe.readout import official_clicks
from ..prepare.one import one_seed
from ..prepare.resolution import lift_state
from .clock_epochs import _sector_maxima, run_epochs


@dataclass(frozen=True)
class CandidatePreset:
    resolution_factor: int = 1 << 28
    matter_divisor: int = 16
    clock_amplitude: int = 512
    gauge_probe: int = 512
    metric_probe: int = 32
    spring_divisor: int = 64
    bridge_divisor: int = 256
    reverse_probe: int = 512


PRESET = CandidatePreset()
GAUGE_PROBES = ('su2.psi_1', 'su3.psi_0r', 'u1.psi_re')
METRIC_PROBES = ('h0x', 'h0y', 'h0z', 'hxx', 'hyy', 'hzz', 'hxy', 'hxz', 'hyz')


def _hash(state):
    return state_hash(state, np.arange(state.G))


def _append_terms(tensor, extra):
    terms = []
    for monomial in tensor.monomials:
        term = (monomial.target, monomial.coeff,
                tuple((f.gear, f.offset, f.field) for f in monomial.factors))
        designation = tensor.designations.get((monomial.target, monomial.factors))
        if designation:
            term += ({'designated_one_way': designation},)
        terms.append(term)
    return Tensor(tensor.gears, terms + list(extra), Q=tensor.Q)


def build_candidate(*, L=3, rng_seed=13, bridge=True, strict_edge_stiffness=None):
    """Return final tensor, seed, clock metadata and a complete preparation manifest.

    Only L, the initial random seed, the bridge control, and the explicitly
    different strict-edge realization are selectable. Numerical coupling and
    amplitude choices live in the frozen PRESET, not in runtime callbacks.
    Clock indices in the returned metadata also apply after strict realization;
    its ``tensor`` is the pre-realization tensor, retained for that distinction.
    """
    if type(L) is not int or L < 3:
        raise ValueError('L must be a Python int at least 3')
    if type(rng_seed) is not int or rng_seed < 0:
        raise ValueError('rng_seed must be a nonnegative Python int')
    if type(bridge) is not bool:
        raise ValueError('bridge must be bool')
    system = one_system()
    source = compose(*system.blocks)
    seed, source_preparation = one_seed(system, source, L, bang='jpure', rng_seed=rng_seed)
    source_seed_hash = _hash(seed)
    matter = [g for g, name in enumerate(source.names) if name.startswith('matter.')]
    for field in ('a', 'b'):
        array = getattr(seed, field)
        for g in matter:
            array[g] = [(1 if int(value) >= 0 else -1) *
                        (abs(int(value)) // PRESET.matter_divisor) for value in array[g]]
    for name in GAUGE_PROBES:
        seed.b[source.gear_index(name), 0] = PRESET.gauge_probe
    checkerboard = np.array([PRESET.metric_probe * (-1)**sum(seed.lattice.coords(n))
                            for n in range(seed.N)], dtype=object)
    for name in METRIC_PROBES:
        g = source.gear_index('metric.' + name)
        seed.b[g], seed.a[g] = checkerboard, -checkerboard
    prepared_source_hash = _hash(seed)
    factor = PRESET.resolution_factor
    lifted = lift_tensor(source, factor)
    lifted_seed = lift_state(seed, source, factor)
    ports = tuple(replace(port, coupling=1 if any(name.startswith('metric.')
                                                 for name in port.gears) else factor)
                  for port in one_invariant_ports(system, coupling=1))
    network = build_clock_network(lifted, ports, spring=(6 * lifted.Q) // PRESET.spring_divisor)
    tensor = network.tensor
    if bridge:
        record_bridge = build_clock_record_bridge(
            Q=tensor.Q, clock='clocknet.cosmic', positive='cosmic.dp', negative='cosmic.dm',
            kappa=(6 * tensor.Q) // PRESET.bridge_divisor)
        tensor = _append_terms(tensor, record_bridge.terms)
    new = np.zeros((tensor.G - source.G, seed.N), dtype=object)
    state = State(L, np.vstack((lifted_seed.a, new + PRESET.clock_amplitude)),
                  np.vstack((lifted_seed.b, new + PRESET.clock_amplitude)),
                  np.vstack((lifted_seed.r, new + 3 * tensor.Q - 1)))
    interaction_fingerprint = tensor.fingerprint
    realization = None
    if strict_edge_stiffness is not None:
        from ..layers.strict_edge import single_edge_realization
        from ..prepare.strict_edge import lift_seed
        realization = single_edge_realization(tensor, stiffness=strict_edge_stiffness)
        state = lift_seed(state, realization)
        tensor = realization.tensor
    manifest = dict(
        recipe='optional_connected_clocks', L=L, rng_seed=rng_seed, seed_kind='jpure',
        preset=asdict(PRESET), bridge_enabled=bridge, source_Q=source.Q, Q=tensor.Q, D=6*tensor.Q,
        source_tensor_fingerprint=source.fingerprint, source_seed_hash=source_seed_hash,
        prepared_source_seed_hash=prepared_source_hash,
        interaction_tensor_fingerprint=interaction_fingerprint,
        tensor_fingerprint=tensor.fingerprint, seed_hash=_hash(state),
        source_preparation=source_preparation,
        initial_changes=dict(
            matter=dict(gears=[source.names[g] for g in matter], fields=['a', 'b'],
                        operation='integer division by 16 towards zero'),
            gauge=dict(gears=list(GAUGE_PROBES), field='b', node=[0, 0, 0], value=PRESET.gauge_probe),
            metric=dict(gears=['metric.'+name for name in METRIC_PROBES],
                        b='32*(-1)^(x+y+z)', a='-b; odd L is not a periodic Nyquist eigenmode'),
            resolution='all source tensor coefficients and Q multiplied by M; all source r multiplied by M; a,b unchanged',
            clocks=dict(gears=['clocknet.'+name for name in ('master',)+network.sectors],
                        a=PRESET.clock_amplitude, b=PRESET.clock_amplitude, remainder=3*tensor.Q-1),
            mediators='if requested, each new node mediator copies its physical link a,b,r once at initialization'),
        ports=[asdict(port) for port in network.ports],
        spring=network.spring, record_bridge_kappa=(6*tensor.Q)//PRESET.bridge_divisor if bridge else 0,
        strict_edge_stiffness=strict_edge_stiffness,
        link_mediators=[] if realization is None else [list(pair) for pair in realization.link_mediators],
        gear_count=tensor.G, tensor_rank=tensor.rank,
        physical_support_violations=len(tensor.support_violations()),
        scope='Chosen interaction tensor and seed; no gravity, synchronization, optimized complexity or quantum-physics theorem. Strict realization is a new law, not source equivalence.')
    return tensor, state, network, manifest


def perturb_seed(tensor, seed, *, direction):
    """Initial-only paired intervention; return a new seed and its exact description."""
    result = seed.copy()
    if direction == 'forward':
        dp, dm = [tensor.gear_index('cosmic.'+name) for name in ('dp', 'dm')]
        if not np.array_equal(seed.r[dp], seed.r[dm]):
            raise ValueError('forward control requires matched pair remainders')
        value = (int(seed.r[dp, 0]) + 2*tensor.Q) % (6*tensor.Q)
        result.r[dp, 0] = value
        result.r[dm, 0] = value
        description = dict(direction=direction, fields=['r'], gears=['cosmic.dp', 'cosmic.dm'],
                           node=[0, 0, 0], operation='add D/3 modulo D to the shared token',
                           before=int(seed.r[dp, 0]), after=value)
    elif direction == 'reverse':
        g = tensor.gear_index('matter.X0')
        result.b[g, 0] += PRESET.reverse_probe
        description = dict(direction=direction, fields=['b'], gears=['matter.X0'], node=[0, 0, 0],
                           operation='add 512 to one initial matter component')
    else:
        raise ValueError('direction must be forward or reverse')
    description['seed_hash'] = _hash(result)
    return result, description


def _event_maps(events):
    maps = {}
    for g, node, kind, quotient in zip(events.gear, events.node, events.kind, events.quotient):
        maps.setdefault(int(g), {})[int(node)] = (int(kind), int(quotient))
    return maps


def paired_control(tensor, seed, *, direction='forward', steps=300, max_counter_bits=128):
    """Compare two autonomous histories with one initial-only difference.

    Official records include turn kind, quotient, and event presence. These
    are reported separately: a turn-kind difference need not be a quotient
    difference. No record is fed into the engine; tensor state provides feedback.
    """
    if type(steps) is not int or steps < 1 or type(max_counter_bits) is not int or max_counter_bits < 1:
        raise ValueError('steps and max_counter_bits must be positive Python ints')
    other, intervention = perturb_seed(tensor, seed, direction=direction)
    initial, other_initial = seed.copy(), other.copy()
    engine = Engine(tensor, tensor.Q)
    if seed.G != tensor.G or int(seed.r.min()) < 0 or int(seed.r.max()) >= engine.D:
        raise ValueError('seed gear count or remainder domain does not match the tensor')
    left, right = initial, other_initial
    groups = {}
    for g, name in enumerate(tensor.names):
        groups.setdefault(name.split('.', 1)[0], []).append(g)
    dp, dm, m1, m2 = [tensor.gear_index('cosmic.'+name) for name in ('dp', 'dm', 'M1', 'M2')]
    tracked = [g for g, name in enumerate(tensor.names) if name.startswith(('clocknet.', 'cosmic.'))]
    physical_links = [g for g, gear in enumerate(tensor.gears) if gear.link is not None]
    first = {name: {} for name in ('state', 'b', 'official_record', 'official_quotient', 'official_presence', 'official_kind')}
    gear_first = {name: {} for name in ('b', 'official_record', 'official_quotient')}
    link_first = dict(state=None, b=None, r=None)
    peak = max(left.max_abs(), right.max_abs()).bit_length()
    initial_sectors = [_sector_maxima(s, groups) for s in (left, right)]
    final_sectors = [s.copy() for s in initial_sectors]
    peak_sectors = [s.copy() for s in initial_sectors]
    outside, lock, difference_identity = 0, True, True
    h00 = tensor.gear_index('metric.h00')
    peak_h00 = max(abs(int(v)) for s in (left, right) for v in s.b[h00])
    clock_peaks = {tensor.names[g]: max(abs(int(v)) for s in (left, right) for v in s.b[g])
                   for g in tracked if tensor.names[g].startswith('clocknet.')}
    distances = [sum(min(x, seed.L-x) for x in seed.lattice.coords(n)) for n in range(seed.N)]
    start = time.monotonic()
    completed = 0
    stop_reason = 'initial_counter_bit_limit' if peak > max_counter_bits else 'requested_horizon'
    ticks = () if stop_reason == 'initial_counter_bit_limit' else range(1, steps+1)
    for tick in ticks:
        after_left, after_right = engine.step(left), engine.step(right)
        completed = tick
        peak = max(peak, after_left.max_abs().bit_length(), after_right.max_abs().bit_length())
        for side, state in enumerate((after_left, after_right)):
            final_sectors[side] = _sector_maxima(state, groups)
            for name in groups:
                peak_sectors[side][name] = max(peak_sectors[side][name], final_sectors[side][name])
        field_changes = {field: getattr(after_left, field) != getattr(after_right, field) for field in ('a', 'b', 'r')}
        changed = field_changes['a'] | field_changes['b'] | field_changes['r']
        outside += sum(int(distances[n] > tick) for n in np.flatnonzero(np.any(changed, axis=0)))
        for name, rows in groups.items():
            if name not in first['state'] and np.any(changed[rows]):
                first['state'][name] = tick
            if name not in first['b'] and np.any(field_changes['b'][rows]):
                first['b'][name] = tick
        for g in tracked:
            if tensor.names[g] not in gear_first['b'] and np.any(field_changes['b'][g]):
                gear_first['b'][tensor.names[g]] = tick
        for field in link_first:
            changes = changed if field == 'state' else field_changes[field]
            if link_first[field] is None and np.any(changes[physical_links]):
                link_first[field] = tick
        left_events = _event_maps(official_clicks(engine, left, after_left, tick))
        right_events = _event_maps(official_clicks(engine, right, after_right, tick))
        for g in left_events.keys() | right_events.keys():
            l, r = left_events.get(g, {}), right_events.get(g, {})
            checks = dict(official_record=l != r,
                          official_quotient={n:v[1] for n,v in l.items()} != {n:v[1] for n,v in r.items()},
                          official_presence=l.keys() != r.keys(),
                          official_kind=any(l[n][0] != r[n][0] for n in l.keys() & r.keys()))
            name, namespace = tensor.names[g], tensor.names[g].split('.', 1)[0]
            for field, differs in checks.items():
                if differs:
                    first[field].setdefault(namespace, tick)
                    if g in tracked and field in gear_first:
                        gear_first[field].setdefault(name, tick)
        for before, after in ((left, after_left), (right, after_right)):
            lock = lock and np.array_equal(after.r[dp], after.r[dm])
            ell_difference = after.b[dp].astype(object)+before.a[dp]-after.b[dm]-before.a[dm]
            intensity = before.b[m1].astype(object)**2+before.b[m2].astype(object)**2
            difference_identity = difference_identity and np.array_equal(ell_difference, intensity)
            peak_h00 = max(peak_h00, max(abs(int(v)) for v in after.b[h00]))
            for g in tracked:
                if tensor.names[g] in clock_peaks:
                    clock_peaks[tensor.names[g]] = max(clock_peaks[tensor.names[g]], max(abs(int(v)) for v in after.b[g]))
        left, right = after_left, after_right
        if peak > max_counter_bits:
            stop_reason = 'counter_bit_limit'
            break
    exact_left = engine.rewind(left, completed).same_as(initial)
    exact_right = engine.rewind(right, completed).same_as(other_initial)
    return dict(
        tensor_fingerprint=tensor.fingerprint, initial_seed_hash=_hash(initial), intervention=intervention,
        final_seed_hashes=[_hash(left), _hash(right)], L=seed.L, requested_steps=steps,
        completed_steps=completed, stop_reason=stop_reason,
        peak_counter_bits=peak, exact_rewinds=[exact_left, exact_right],
        caller_seed_unchanged=seed.same_as(initial),
        sector_counter_bounds={name: dict(initial=[s[name] for s in initial_sectors],
                                          final=[s[name] for s in final_sectors],
                                          peak=[s[name] for s in peak_sectors]) for name in groups},
        matched_remainders=bool(lock), matched_quotient_difference_equals_reader_intensity=bool(difference_identity),
        outside_storage_cone=outside, first_namespace_difference=first,
        first_tracked_gear_difference=gear_first, first_physical_link_difference=link_first,
        peak_abs_h00=peak_h00, peak_abs_clock_b=clock_peaks, seconds=time.monotonic()-start,
        scope='Finite paired histories. Official quotient projection retains event presence; kind checks compare common events. Storage light cone uses periodic Manhattan radius t, not a derived relativistic metric.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--L', type=int, default=3)
    parser.add_argument('--rng', type=int, default=13)
    parser.add_argument('--steps', type=int, default=300)
    parser.add_argument('--control', choices=('forward', 'reverse', 'off'))
    parser.add_argument('--strict-edge-stiffness', type=int)
    parser.add_argument('--max-counter-bits', type=int, default=128)
    parser.add_argument('--sample-every', type=int, default=100)
    parser.add_argument('--out', default='runs/connected-clocks/report.json')
    args = parser.parse_args(argv)
    tensor, seed, network, manifest = build_candidate(
        L=args.L, rng_seed=args.rng, bridge=args.control != 'off',
        strict_edge_stiffness=args.strict_edge_stiffness)
    if args.control:
        result = paired_control(tensor, seed, direction='reverse' if args.control == 'reverse' else 'forward',
                                steps=args.steps, max_counter_bits=args.max_counter_bits)
        result['control'] = args.control
    else:
        result = run_epochs(tensor, seed, steps=args.steps,
                            hand_indices=[tensor.gear_index('cosmic.Th'), network.clock_index('master')],
                            reader_indices=[tensor.gear_index('cosmic.M1'), tensor.gear_index('cosmic.M2')],
                            max_counter_bits=args.max_counter_bits, sample_every=args.sample_every)
    result['preparation'] = manifest
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({name: result[name] for name in ('completed_steps', 'stop_reason', 'peak_counter_bits')}, indent=2))
    return result


if __name__ == '__main__':
    main()
