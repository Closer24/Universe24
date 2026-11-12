"""Join the board and completion handoffs without changing either physical law.

Run ``python -m validation.integration_contract.massive45``. Exact tensor and
complete-state agreement is a mechanical integration gate. Constraint failure
is deliberately retained as a separate physical result.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np

from universe24.core import Engine
from universe24.system.bundle import canonical_bytes
from validation.completion import common45, formulation
from validation.geodesic_board.run import build_program
from validation.geometry.team48 import refinement_integer_projective as projective

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_TENSORS = {
    F(1, 64): '6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0',
    F(1, 32): 'fbbf8f9b4128563e786ff0b57069fe18320698451c0ac9acb0c947c568cfc617',
}


def independent_weak_seed(program):
    """Explicit common fixture; all six carry classes, no hidden old slice."""
    values = np.zeros((44, 27), dtype=object)
    for axis in range(3):
        values[program.fields.index(f'B{axis}{axis}')] = 1
        values[program.fields.index(f'K{axis}{axis}')] = F(-1, 10)
    values[program.fields.index('phi')] = F(1, 5)
    values[program.fields.index('dust_amplitude')] = F(1, 10)
    carries = np.array([[(channel+node) % 6 for node in range(27)]
                        for channel in range(45)], dtype=object)
    return projective.prepare(program, values, L=3, denominator=100,
                              remainders=carries)


def reduced_constraint(program, state):
    """Independent isotropic scalar/dust expression; not general spatial GR."""
    raw = projective.readout(program, state)
    def field(name):
        return raw[program.fields.index(name), 0]
    return (6*field('K00')**2-field('Pi_phi')**2-field('phi')**2
            -2*field('dust_amplitude')**2)


def check_handoff(dt):
    dt = F(dt)
    board = build_program(dt=dt, dx=F(1, 4), mass_squared=1)
    completion = common45.build45(dt=dt, dx=F(1, 4), mass_squared=1)
    assert board.fields == completion.fields
    assert board.tensor.fingerprint == completion.tensor.fingerprint == EXPECTED_TENSORS[dt]
    assert board.tensor.G == completion.tensor.G == 45
    assert len(board.tensor) == len(completion.tensor) == 889
    assert board.tensor.rank-1 == completion.tensor.rank-1 == 2
    assert not board.tensor.support_violations() and not completion.tensor.support_violations()
    seeds = [independent_weak_seed(program) for program in (board, completion)]
    assert seeds[0].same_as(seeds[1])
    assert seeds[1].same_as(common45.weak_seed(completion))
    assert set(int(v) for v in seeds[0].r.flat) == set(range(6))
    assert reduced_constraint(board, seeds[0]) == 0
    engines = [Engine(program.tensor) for program in (board, completion)]
    states = seeds[:]
    first_defect, max_bits = None, 0
    for tick in range(1, 4):
        for index, (program, engine) in enumerate(zip((board, completion), engines)):
            before = states[index]
            after = engine.step(before)
            assert after.same_as(formulation.previous.scalar_oracle(program.tensor, before))
            assert engine.inverse_step(after).same_as(before)
            assert np.array_equal(after.r, seeds[index].r)
            states[index] = after
        assert states[0].same_as(states[1])
        max_bits = max(max_bits, max(abs(int(v)).bit_length()
            for array in (states[0].a, states[0].b, states[0].r) for v in array.flat))
        if tick == 1:
            # At k=-1/10, p=0, phi=1/5, d=1/10, the continuum RHS is
            # (kdot,pdot,phidot,ddot)=(1/200,-1/5,0,-3/200).
            # Its quadratic norm is 6/40000-1/25-18/40000=-403/10000.
            first_defect = reduced_constraint(board, states[0])
            assert first_defect == -F(403, 10000)*dt**2 != 0
            _, full_constraints, _ = formulation.equations(
                common45.decode_fields(completion, states[1]), lambda *_: F(0))
            assert full_constraints['H'] == first_defect
    for engine, state, seed in zip(engines, states, seeds):
        assert engine.rewind(state, 3).same_as(seed)
    return {'dt': str(dt), 'dx': '1/4', 'mass_squared': 1,
            'tensor_sha256': board.tensor.fingerprint,
            'channels': 45, 'retained_integers_per_node': 135,
            'steps': 3, 'nodes': 27, 'max_retained_bits': max_bits,
            'complete_state_sha256': hashlib.sha256(canonical_bytes(states[0].to_dict())).hexdigest(),
            'same_tensor_complete_states_oracle_and_rewind': 'passed',
            'initial_H': '0', 'first_step_H': str(first_defect),
            'discrete_Einstein_constraint': 'failed',
            'operational_clock_detector_and_Born': 'not_tested'}


def audit():
    sources = ('validation/geodesic_board/run.py',
               'validation/completion/common45.py', 'validation/completion/formulation.py',
               'validation/integration_contract/massive45.py')
    return {'schema': 'universe24/cross-team-integration/1',
            'source_handoffs': {'board': 'ff21c878cc2e6e9d0969c3538e0c676fcdab616f',
                                'completion': '8c53e69f4b466dcbd2da7dab7e3c365bd9731766'},
            'current_source_sha256': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                      for name in sources},
            'cases': [check_handoff(dt) for dt in EXPECTED_TENSORS],
            'scope': 'One shared massive45 tensor, not a new supported physical model.'}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
