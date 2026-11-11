"""Exact recurring-burst audit. Observers never alter the integer dynamics."""
from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import argparse
from collections import deque
from functools import reduce
from math import gcd
import gzip
import hashlib
import json
import platform

import numpy as np
from universe24.core import Engine, State, Tensor
from universe24.core.lattice import DIRECTIONS, ZERO
from validation.demos.communication.run_communication import build
from universe24.layers.communication import LANES, NAMESPACE, RECEIVER
from universe24.observe.reference_model import state_hash
from universe24.prepare.communication import message_seed

PROTOCOL = 'recurrent-bursts-v1'
COEFFICIENTS = (-3, -2, -1, 1, 2, 3)
FAMILIES = ('linear', 'cubic', 'spring')
FEEDBACK_WHY = 'Explicit experimental local reference/message feedback; no physical potential or complexity law asserted.'


def rows_for(tensor, prefix):
    return [i for i, name in enumerate(tensor.names) if name.startswith(prefix + '.')]


def structural_snapshot(state, rows, previous=()):
    """Scale-invariant finite-board diagnostics, computed with exact integers."""
    fields = [[int(v) for v in state.b[g]] for g in rows]
    weights = [sum(abs(field[n]) for field in fields) for n in range(state.N)]
    total = sum(weights)
    balls = [sum(weights[j] for j in {n, *(state.lattice.neighbour(n, d) for d in range(6))})
             for n in range(state.N)]
    maximum = max(balls, default=0)
    signatures = tuple(tuple((field[n] > 0) - (field[n] < 0) for field in fields)
                       for n in range(state.N))
    sites = {s for s in signatures if any(s)}
    edges = set()
    for n, here in enumerate(signatures):
        for d in (0, 2, 4):
            there = signatures[state.lattice.neighbour(n, d)]
            if any(here) or any(there):
                edges.add(tuple(sorted((here, there))))
    persistent = set()
    if len(previous) == 2:
        persistent = {s for n, s in enumerate(signatures) if any(s)
                      and all(old[n] == s for old in previous)}
    flat = [v for field in fields for v in field]
    divisor = reduce(gcd, (abs(v) for v in flat), 0) or 1
    normalized = [v // divisor for v in flat]
    fingerprint = hashlib.sha256(json.dumps(normalized, separators=(',', ':')).encode()).hexdigest()
    row = dict(reference_mass=str(total), compact_ball_mass=str(maximum),
               compact=bool(total and 4*maximum >= 3*total),
               dispersed=bool(total and 2*maximum < total),
               active_sites=sum(v != 0 for v in weights),
               site_pattern_types=len(sites), edge_pattern_types=len(edges),
               persistent_pattern_types=len(persistent), normalized_fingerprint=fingerprint)
    return row, signatures


def score(row):
    return tuple(row[k] for k in ('site_pattern_types', 'edge_pattern_types', 'persistent_pattern_types'))


def progressive_reassemblies(events):
    if len(events) < 4 or any(e['persistent_pattern_types'] == 0 for e in events):
        return False
    values = [score(e) for e in events]
    return all(all(b >= a for a, b in zip(left, right)) and right != left
               for left, right in zip(values, values[1:]))


class ReassemblyTracker:
    """Hysteresis distinguishes expansion/contraction from a constant cluster."""
    def __init__(self):
        self.had_compact = False
        self.departed = False
        self.initial_compact_update = None
        self.events = []

    def observe(self, row):
        if row['compact']:
            if not self.had_compact:
                self.had_compact = True
                self.initial_compact_update = row['update']
            elif self.departed:
                self.events.append(dict(row))
            self.departed = False
        elif row['dispersed'] and self.had_compact:
            self.departed = True


def candidate_tensor(source, family='baseline', coefficient=0):
    if family not in ('baseline', 'disconnected') + FAMILIES:
        raise ValueError('unknown feedback family')
    if type(coefficient) is not int:
        raise TypeError('feedback coefficient must be an integer')
    if family in FAMILIES and coefficient == 0:
        raise ValueError('candidate feedback must be nonzero')
    names = source.names
    receiver = source.gear_index(RECEIVER)
    carriers = {source.gear_index(f'{NAMESPACE}.{lane}') for lane in LANES}
    terms = []
    for m in source.monomials:
        reception = m.target == receiver and any(f.gear in carriers for f in m.factors)
        if reception and family in ('disconnected', 'spring'):
            continue
        term = (names[m.target], m.coeff,
                tuple((names[f.gear], f.offset, f.field) for f in m.factors))
        why = source.designations.get((m.target, m.factors))
        if why:
            term += ({'designated_one_way': why},)
        terms.append(term)
    meta = {'designated_one_way': FEEDBACK_WHY}
    for lane, direction in zip(LANES, DIRECTIONS):
        channel = f'{NAMESPACE}.{lane}'
        remote = (RECEIVER, direction, 'b')
        local = (channel, ZERO, 'b')
        if family == 'linear':
            terms.append((channel, coefficient, (remote,), meta))
        elif family == 'cubic':
            terms.append((channel, coefficient, (remote, local, local), meta))
        elif family == 'spring':
            upstream = tuple(-v for v in direction)
            terms.extend(((channel, coefficient, (remote,), meta),
                          (channel, -coefficient, (local,), meta),
                          (RECEIVER, coefficient, ((channel, upstream, 'b'),), meta),
                          (RECEIVER, -coefficient, ((RECEIVER, ZERO, 'b'),), meta)))
    return Tensor(source.gears, terms, strict_support=True)


def run_case(*, L=5, steps=160, family='baseline', coefficient=0,
             amplitude=3, max_bits=128, out=None):
    if type(steps) is not int or steps < 1 or type(max_bits) is not int or max_bits < 1:
        raise ValueError('positive integer horizon and bit budget required')
    if type(amplitude) is not int:
        raise TypeError('amplitude must be an integer')
    origin = (L//2,) * 3
    if family == 'periodic_control':
        names = [f'ref.shell_{lane}' for lane in LANES]
        terms = [(name, 3, ((name, offset, 'b'),))
                 for name, d in zip(names, DIRECTIONS)
                 for offset in (d, tuple(-v for v in d))]
        tensor = Tensor(names, terms, strict_support=True)
        engine = Engine(tensor)
        empty = engine.vacuum(L, [0] * 6)
        a, b = empty.a.astype(object), empty.b.astype(object)
        b[:, empty.lattice.index(*origin)] = amplitude
        for g, d in enumerate(DIRECTIONS):
            a[g] = b[g, empty.lattice.shift_index(d)]
        seed = State(L, a, b, empty.r)
    else:
        _, base, _, empty, _ = build(L, 'none')
        tensor = candidate_tensor(base, family, coefficient)
        engine = Engine(tensor)
        seed = message_seed(empty, tensor, [(lane, origin, amplitude) for lane in LANES])
    state = seed.copy()
    reference = rows_for(tensor, 'ref')
    carriers = rows_for(tensor, 'comm')
    history = deque(maxlen=2)
    tracker = ReassemblyTracker()
    samples, focus_updates, full_returns = [], [], []
    hashes = []
    stop = 'requested_horizon'
    prior_focus = None
    for tick in range(steps+1):
        row, signatures = structural_snapshot(state, reference, tuple(history))
        history.append(signatures)
        carrier_mass = [sum(abs(int(state.b[g, n])) for g in carriers) for n in range(state.N)]
        mass = sum(carrier_mass)
        focused = bool(mass and max(carrier_mass) == mass)
        if focused and prior_focus is False:
            focus_updates.append(tick)
        prior_focus = focused
        bits = state.max_abs().bit_length()
        row.update(update=tick, maximum_counter_bits=bits, carrier_focused=focused)
        tracker.observe(row)
        samples.append(row)
        hashes.append(state_hash(state, range(tensor.G)))
        if tick and state.same_as(seed):
            full_returns.append(tick)
        if bits > max_bits:
            stop = 'counter_bit_limit'
            break
        if tick < steps:
            state = engine.step(state)
    completed = len(samples)-1
    exact = engine.rewind(state, completed).same_as(seed)
    if not exact:
        raise AssertionError('complete retained seed was not recovered')
    event_gate = len(tracker.events) >= 4
    growth_gate = progressive_reassemblies(tracker.events)
    gates = dict(recurrent_reference_bursts=event_gate,
                 growing_structural_proxies=growth_gate,
                 complete_information_recovery=exact,
                 feedback_attribution_demonstrated=None,
                 stagnation_trigger_demonstrated=None)
    # A one-step message intervention does not attribute reassembly to feedback.
    # Nor does this experiment provide a local stagnation detector. Unknown is
    # not success; both causal claims need their own matched controls.
    goal = all(value is True for value in gates.values())
    result = dict(protocol=PROTOCOL, parameters=dict(L=L, steps=steps, family=family,
                  coefficient=coefficient, amplitude=amplitude, max_bits=max_bits),
                  completed_updates=completed, stop_reason=stop,
                  tensor_fingerprint=tensor.fingerprint, dynamics_fingerprint=tensor.dynamics_fingerprint,
                  initial_hash=hashes[0], final_hash=hashes[-1], exact_rewind=exact,
                  full_state_returns=full_returns, carrier_focus_updates=focus_updates,
                  initial_compact_update=tracker.initial_compact_update,
                  reference_reassemblies=tracker.events,
                  maximum_counter_bits=max(row['maximum_counter_bits'] for row in samples),
                  maximum_site_pattern_types=max(row['site_pattern_types'] for row in samples),
                  maximum_edge_pattern_types=max(row['edge_pattern_types'] for row in samples),
                  maximum_persistent_pattern_types=max(row['persistent_pattern_types'] for row in samples),
                  gates=gates, user_goal_demonstrated=goal,
                  samples=samples, state_hashes=hashes)
    if out is not None:
        path = Path(out)
        path.mkdir(parents=True, exist_ok=True)
        (path/'tensor.json').write_text(tensor.to_json()+'\n')
        for name, values in (('initial', seed.to_dict()), ('final', state.to_dict())):
            with gzip.open(path/(name+'.json.gz'), 'wt') as f:
                json.dump(values, f, separators=(',', ':'))
        (path/'report.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def feedback_interventions():
    """Matched complete-seed interventions, executed through the common engine."""
    _, base, _, empty, _ = build(5, 'none')
    origin = empty.lattice.index(2,2,2)
    neighbor = empty.lattice.index(3,2,2)
    seed = empty.copy()
    channel = base.gear_index('comm.px')
    receiver = base.gear_index(RECEIVER)
    seed.b[channel,origin] = 3
    changed = seed.copy()
    changed.b[receiver,neighbor] = 3
    results = []
    for family in ('baseline',) + FAMILIES:
        for coefficient in ((0,) if family == 'baseline' else COEFFICIENTS):
            tensor = candidate_tensor(base,family,coefficient)
            engine = Engine(tensor)
            left, right = engine.step(seed), engine.step(changed)
            effects = int(np.count_nonzero(left.b[48:] != right.b[48:]))
            results.append(dict(family=family,coefficient=coefficient,
                                changed_message_registers=effects,
                                reference_perturbation='initial R00.b at one downstream neighbor += 3',
                                exact_inverse=engine.inverse_step(right).same_as(changed)))
    return results


def compact(case):
    return {k: v for k, v in case.items() if k not in ('samples', 'state_hashes')}


def run_grid(out, baseline_steps=600, candidate_steps=160):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for L in (3, 5, 7):
        r = run_case(L=L, steps=baseline_steps, out=out/f'baseline_L{L}')
        results.append(compact(r))
        print(json.dumps({'case': f'baseline_L{L}', 'bursts': len(r['reference_reassemblies']),
                          'carrier_returns': len(r['carrier_focus_updates']), 'stop': r['stop_reason']}), flush=True)
    for name, family, amplitude in (('no_messages', 'baseline', 0),
                                    ('disconnected', 'disconnected', 3),
                                    ('double_payload', 'baseline', 6)):
        r = run_case(steps=candidate_steps, family=family, amplitude=amplitude, out=out/name)
        results.append(compact(r))
    # Post-grid detector calibration: an exact periodic shell, not a new
    # success candidate. Its known recurrence must fail the growth gate.
    r = run_case(L=7, steps=70, family='periodic_control', out=out/'periodic_control')
    results.append(compact(r))
    for family in FAMILIES:
        for coefficient in COEFFICIENTS:
            name = f'{family}_{coefficient}'
            r = run_case(steps=candidate_steps, family=family, coefficient=coefficient, out=out/name)
            results.append(compact(r))
            print(json.dumps({'case': name, 'bursts': len(r['reference_reassemblies']),
                              'completed': r['completed_updates'], 'stop': r['stop_reason']}), flush=True)
    report = dict(protocol=PROTOCOL, python=platform.python_version(), numpy=np.__version__,
                  base_communication_commit='90d8638c1ebf86021dde3371766acb42e0a42ee6',
                  source_sha256={name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
                      'validation/cosmology/recurrent_bursts.py', 'validation/cosmology/PROTOCOL.md',
                      'universe24/core/engine.py', 'universe24/core/tensor.py',
                      'universe24/layers/communication.py', 'universe24/prepare/communication.py',
                      'universe24/layers/reference_model.py')},
                  cases=results, feedback_interventions=feedback_interventions(),
                  user_goal_demonstrated=any(c['user_goal_demonstrated'] for c in results),
                  interpretation='Finite diagnostic search; no cosmological or universal complexity claim.')
    (out/'SUMMARY.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('runs/recurrent-bursts'))
    args = parser.parse_args(argv)
    report = run_grid(args.out)
    print(json.dumps({'cases': len(report['cases']), 'user_goal_demonstrated': report['user_goal_demonstrated']}))


if __name__ == '__main__':
    main()
