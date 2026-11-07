"""Independent algebra and complete-state checks for prepared clock candidates."""
import itertools
import json
from pathlib import Path
import unittest

from research.components import BoardSpec, TensorSpec, finalize, place
from research.reference.algebra import coupling as independent_coupling, algebra as independent_algebra
from research.staged_blocks.orbit import (ShieldedOrbit, prepare_orbit,
                                         registered_cases, PROTOCOL)
from universe24 import Channel, State
from universe24.core.group_2o import DIRECTIONS
from universe24.observation.clicks import classify


class ShieldedOrbitTests(unittest.TestCase):
    def test_passive_halo_existence_exact_domain(self):
        for a,b,w in itertools.product(range(-3,4), range(-3,4), (-1,1)):
            prefix = (0,b,b-a,-a,0)
            allowed = [r for r in range(6) if all(0 <= r+2*w*u < 6 for u in prefix)]
            self.assertEqual(bool(allowed), abs(a)+abs(b) <= 2)

    def test_complete_states_against_independent_recipient_formula(self):
        # Independent matrix receiver lookup, including mixed signs, all labels,
        # wrapped L3 geometry and nontrivial retained halos. No engine table is
        # used to construct the expected receiving addresses.
        pairs = ((1,0),(0,1),(1,-1),(2,0),(0,-2),(0,0))
        for signs, g in itertools.product(((-1,-1,-1),(1,-1,1),(1,1,1)), range(48)):
            a,b = pairs[g % len(pairs)]
            r, phase = g % 6, g % 4
            prepared = prepare_orbit(side=3, location=(0,2,1), body_signs=signs,
                                     channel=g, a=a, b=b, r=r, phase=phase)
            oracle = independent_coupling(signs)
            recipients = []
            prefix = (0,b,b-a,-a)
            for d,delta in enumerate(DIRECTIONS):
                receivers = [h for h in range(48) if oracle.ports[d ^ 1][h] == g]
                self.assertEqual(len(receivers),1)
                h = receivers[0]
                w = oracle.weights[d ^ 1][h]
                possible = [v for v in (0,2,4) if all(0 <= v+2*w*u < 6 for u in (*prefix,0))]
                rr = min(possible, key=lambda v:abs(v-2))
                addr = tuple((x+y)%3 for x,y in zip((0,2,1),delta))+(h,)
                recipients.append((addr,w,rr))
            state = prepared.initial
            for t in range(9):
                p = (phase+t)%4
                aa,bb = ((a,b),(b,-a),(-a,-b),(-b,a))[p]
                expected = {(0,2,1,g):(aa,bb,r)}
                expected.update({addr:(0,0,rr+2*w*prefix[p]) for addr,w,rr in recipients})
                self.assertEqual(state,State(state.cube,Channel(0,0,2),expected))
                after = prepared.engine.advance(state)
                self.assertEqual(prepared.engine.rewind(after),state)
                self.assertFalse(any(classify(state.at(ad),after.at(ad)) for ad in state.cells.keys()|after.cells.keys()))
                state = after

    def test_complete_phase_and_source_off_preserve_remainders(self):
        for a,b,phase in itertools.product((-1,0,1),(-1,0,1),range(4)):
            on = prepare_orbit(a=a,b=b,phase=phase)
            off = prepare_orbit(a=a,b=b,phase=phase,present=False)
            for address in on.initial.cells.keys()|off.initial.cells.keys():
                self.assertEqual(on.initial.at(address).r,off.initial.at(address).r)
            self.assertEqual(off.engine.advance(off.initial),off.initial)
            phase_next = prepare_orbit(a=a,b=b,phase=(phase+1)%4)
            self.assertEqual(on.engine.advance(on.initial),phase_next.initial)

    def test_custom_guide_halo_and_validation(self):
        patch = ShieldedOrbit(a=0,b=1,halo_remainders=(0,2,2,2,2,2))
        prepared = finalize(BoardSpec(5),[place(patch,at=(2,2,2),name='orbit')])
        state = prepared.initial
        for _ in range(4):
            state = prepared.engine.advance(state)
        self.assertEqual(state,prepared.initial)
        with self.assertRaises(ValueError):
            ShieldedOrbit(a=1,b=0,halo_remainders=(0,2,2,2,2,2))
        for invalid in ({'a':3},{'a':True},{'channel':48},{'phase':4},{'r':6}):
            with self.assertRaises(ValueError):
                ShieldedOrbit(**invalid)

    def test_tensor_and_initial_overlap_conflicts_are_rejected(self):
        with self.assertRaises(ValueError):
            finalize(BoardSpec(5),[place(ShieldedOrbit(tensor=TensorSpec((-1,1,1))),at=(2,2,2),name='clock')])
        with self.assertRaises(ValueError):
            finalize(BoardSpec(5),[place(ShieldedOrbit(),at=(2,2,2),name='one'),
                                   place(ShieldedOrbit(a=0,b=1),at=(2,2,2),name='two')])
        patch = ShieldedOrbit()
        self.assertEqual(len(patch.cells),336)
        self.assertEqual(len(patch.ports['halo']),6)

    def test_frozen_case_family(self):
        cases = registered_cases(json.loads(PROTOCOL.read_text()))
        self.assertEqual(len(cases),744)
        self.assertEqual(len({case['id'] for case in cases}),744)
        self.assertEqual(sum(c['family'] != 'disturbance' for c in cases),720)

    def test_mixed_y_sign_has_local_gauge_obstruction(self):
        positive = independent_coupling((1,1,1))
        mixed = independent_coupling((1,-1,1))
        observed = []
        for directions, expected_channels, expected_weights in (
            ((4,0,3),(0,25,35,12),(1,-1,1)),
            ((3,0,4),(0,45,18,12),(-1,1,-1)),
        ):
            position, g, ratio, channels, weights = (0,0,0), 0, 1, [0], []
            for d in directions:
                self.assertEqual(positive.ports[d][g],mixed.ports[d][g])
                weight = mixed.weights[d][g]
                ratio *= weight * positive.weights[d][g]
                weights.append(weight)
                g = positive.ports[d][g]
                channels.append(g)
                position = tuple(x+y for x,y in zip(position,DIRECTIONS[d]))
            self.assertEqual(tuple(channels),expected_channels)
            self.assertEqual(tuple(weights),expected_weights)
            observed.append(((*position,g),ratio))
        self.assertEqual(observed,[((1,-1,1,12),-1),((1,-1,1,12),1)])

    def test_exact_channel_and_checkerboard_gauge_edge_relation(self):
        diagonals = ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))
        characters = []
        for rotation in independent_algebra().rotations:
            permutation = []
            for vector in diagonals:
                image = tuple(sum(rotation[i][j]*vector[j] for j in range(3)) for i in range(3))
                permutation.append(next(k for k,v in enumerate(diagonals)
                                        if image == v or image == tuple(-x for x in v)))
            inversions = sum(permutation[i] > permutation[j] for i in range(4) for j in range(i+1,4))
            characters.append((-1)**inversions)
        for signs,k,l in itertools.product(itertools.product((-1,1),repeat=3),(0,1),(0,1)):
            old = independent_coupling(signs)
            new_signs = (signs[0]*(-1)**k,signs[1]*(-1)**(k+l),signs[2]*(-1)**(k+l))
            new = independent_coupling(new_signs)
            for d,g in itertools.product(range(6),range(48)):
                h = old.ports[d][g]
                self.assertEqual(h,new.ports[d][g])
                # An unwrapped nearest-neighbor step changes spatial parity.
                ratio = (-1)**k * characters[g]**l * characters[h]**l
                self.assertEqual(new.weights[d][g],ratio*old.weights[d][g])


if __name__ == '__main__':
    unittest.main()
