"""Audit compact null-covector geometry against the retained pp-wave coframe.

The new two-channel model transports F, not arbitrary old E/W/clock states.
Every full compact (a,b,r) snapshot is exported; geometry is passive readout.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from validation.geometry import ppwave_palatini_local as reference
from universe24.algebra.null_covector import ETA, NullCoframe
from universe24.core import Engine
from universe24.core.channels import ChannelAssembly, Component
from universe24.layers.null_wave import build
from universe24.observe.null_wave import geometry
from universe24.prepare.null_wave import prepare


def encoded(record):
    return (json.dumps(record, sort_keys=True, separators=(',', ':'))+'\n').encode()


def run(L=5, P=256, trace_path=None):
    reference_tensor = reference.build()
    old, _ = reference.prepare(reference_tensor, L=L, P=P)
    local_tensor = build()
    xyz = old.lattice.all_coords().astype(object)
    x, y, z = xyz[:, 0]-L//2, xyz[:, 1]-L//2, xyz[:, 2]
    profile = (z % 5-2)*(x*x-y*y) + 2*((2*z+1) % 3-1)*x*y
    remainders = np.arange(2*old.N).reshape(2, old.N) % 6
    local_seed = prepare(local_tensor, profile, L=L, remainders=remainders)
    assembly = ChannelAssembly([Component(
        'null_wave_experiment', local_tensor,
        'restricted +z profile; passive null coframe; no ADM source', 'audit')])
    state = seed = assembly.pack({'null_wave_experiment': local_seed})
    engine, old_engine = Engine(assembly.tensor), Engine(reference_tensor)
    calibration = NullCoframe(P)
    eta = np.diag(np.array(ETA, dtype=object))
    identity = np.broadcast_to(np.eye(4, dtype=object), (state.N, 4, 4))
    manifest = assembly.manifest()
    manifest['cross_component_dynamics'] = 'none; standalone experiment, not assembled with ADM'
    header = {'format': 'Universe24-compact-null-wave-trace-v1',
              'tensor': assembly.tensor.to_dict(), 'channels': manifest,
              'decoder': {'P': P, 'covector': list(calibration.covector)},
              'steps': 2*L}
    trace = [encoded(header)]
    coframe_checks = metric_checks = inverse_checks = 0
    audit_clicks = 0
    audit_classes = {str(kind): 0 for kind in (0, 1, 2)}
    for tick in range(2*L+1):
        trace.append(encoded({'tick': tick, 'state': state.to_dict()}))
        local = assembly.extract(state, 'null_wave_experiment')
        # Compare both retained histories and both banks, even when staggered.
        # Legacy connection gears and remainders are not inferred from F.
        for field in ('a', 'b'):
            for bank, offset in enumerate((0, 22)):
                actual = calibration.decode(getattr(local, field)[bank])['coframe']
                expected = getattr(old, field)[offset:offset+16].astype(object).T.reshape(state.N, 4, 4)
                assert np.array_equal(actual, expected)
                coframe_checks += state.N
        if tick % 2 == 0:
            observed = geometry(local, P=P)
            E = reference.unpack(old)[0]
            g = E.transpose(0, 2, 1) @ eta @ E
            assert np.array_equal(observed['metric'], g)
            J = observed['inverse_coframe_numerator']
            H = observed['inverse_metric_numerator']
            assert np.array_equal(E@J, P**2*identity)
            assert np.array_equal(J@E, P**2*identity)
            assert np.array_equal(g@H, P**3*identity)
            assert np.array_equal(H@g, P**3*identity)
            metric_checks += state.N
            inverse_checks += state.N
        if tick == 2*L:
            break
        before = state
        state = engine.step(before)
        assert engine.inverse_step(state).same_as(before)
        assert np.array_equal(state.r, seed.r)
        clicks = engine.clicks(before, state, tick+1).select('audit')
        audit_clicks += len(clicks)
        for kind in (0, 1, 2):
            audit_classes[str(kind)] += int(np.count_nonzero(clicks.kind == kind))
        old = old_engine.step(old)
    assert state.same_as(seed)
    assert engine.rewind(state, 2*L).same_as(seed)
    payload = b''.join(trace)
    if trace_path is not None:
        trace_path = Path(trace_path)
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.write_bytes(payload)
    sources = [Path(__file__).relative_to(ROOT),
               Path(reference.__file__).relative_to(ROOT)]
    sources += [Path(f'universe24/{path}.py') for path in (
        'algebra/null_covector', 'layers/null_wave', 'prepare/null_wave',
        'observe/null_wave', 'core/engine', 'core/tensor', 'core/lattice', 'core/channels')]
    return {
        'format': 'Universe24-compact-null-wave-audit-v1',
        'scope': 'new compact prepared-sector representation; not full-state equivalence to the 48-channel experiment',
        'preparation': {'L': L, 'P': P, 'covector': list(calibration.covector),
                        'profile': 'A(z)(x^2-y^2)+2B(z)xy; A=z%5-2; B=(2z+1)%3-1',
                        'coordinates': 'x=index_x-L//2,y=index_y-L//2,z=index_z',
                        'remainders': 'arange(2*L^3).reshape(2,L^3)%6; frozen in place'},
        'tensor': {'fingerprint': assembly.tensor.fingerprint,
                   'gears': assembly.tensor.G, 'monomials': len(assembly.tensor),
                   'input_degree': max(m.degree for m in assembly.tensor.monomials),
                   'strict_single_edge': not assembly.tensor.support_violations()},
        'channels': manifest,
        'comparison': {'old_coframe_channels': 32, 'compact_profile_channels': 2,
                       'old_connection_channels_not_retained': 12,
                       'old_signal_and_clock_channels_not_retained': 4,
                       'retained_coframe_bank_history_node_checks': coframe_checks,
                       'metric_node_checks': metric_checks,
                       'two_sided_inverse_node_checks': inverse_checks,
                       'coframe_and_metric_mismatches': 0},
        'complete_state': {'steps': 2*L, 'snapshots': 2*L+1,
                           'exact_cycle': True, 'every_step_inverse': True,
                           'exact_rewind': True, 'frozen_nonzero_remainders': True,
                           'audit_click_records': audit_clicks,
                           'audit_click_classes': audit_classes,
                           'trace_sha256': hashlib.sha256(payload).hexdigest()},
        'source_sha256': {str(path): hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
                          for path in sorted(sources)},
        'limitations': [
            'Only the declared prepared coframe histories are compared; independent connection and control states are absent.',
            'The nonperiodic transverse vacuum chart still has seam failures; no global periodic vacuum solution is claimed.',
            'F translates in a fixed +z direction; the generic null algebra does not supply other propagation laws.',
            'No proper-clock response, matter backreaction, ADM coupling or accumulated-complexity mechanism is added.',
            'Geometry is a passive exact rational readout; no denominator changes the fixed-six Engine.',
        ],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--L', type=int, default=5)
    parser.add_argument('--P', type=int, default=256)
    parser.add_argument('--out', type=Path, default=ROOT/'runs/compact-null-wave')
    args = parser.parse_args()
    report = run(args.L, args.P, args.out/'full_trace.jsonl')
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('tensor', 'comparison', 'complete_state')}, indent=2))
