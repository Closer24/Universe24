import itertools
import unittest

import numpy as np

from universe24.core import Engine, State, Tensor, GearType
from universe24.core.lattice import DIRECTIONS
from validation.selection.clocks import build_native_gate, first_order, prepare_gate
from validation.selection.complexity import (SORT_GATE, IDENTITY_GATE, sorting_collision,
    history_intervention, axial_motifs, structure_trace, episode_gate, projective_phase_relations)


class NativeSelectionComplexityTests(unittest.TestCase):
    def test_collision_is_permutation_and_retains_source_order(self):
        self.assertEqual(len(set(SORT_GATE)), 8)
        self.assertEqual(sorting_collision(0,0,1), (1,1,0))
        self.assertEqual(sorting_collision(0,1,0), (0,1,0))
        for m,x,y in itertools.product(range(2),repeat=3):
            new_m,new_x,new_y=sorting_collision(m,x,y)
            self.assertEqual(new_x+new_y,x+y)
            self.assertEqual(new_x>=new_y,True if m==0 else new_x==new_y)

    def test_preference_uses_ready_memory_and_is_not_monotone_over_cycle(self):
        value=(0,0,1); seen=[]
        for _ in range(3):
            value=sorting_collision(*value); seen.append(value)
        self.assertEqual(seen,[(1,1,0),(1,0,1),(0,0,1)])

    def test_real_engine_matches_independent_transport_and_all_carries(self):
        current=np.asarray([[0]*27,[(n+1)%2 for n in range(27)],[n%2 for n in range(27)]],dtype=object)
        for direction in DIRECTIONS:
            law=build_native_gate(SORT_GATE,direction=direction,name="selection")
            self.assertEqual(law.G,3)
            self.assertLessEqual(max(m.degree for m in law.monomials),3)
            self.assertEqual(law.support_violations(),[])
            for carry in range(6):
                state=prepare_gate(SORT_GATE,current,3,direction,remainders=np.full((3,27),carry,dtype=object))
                expected=first_order(state.b,SORT_GATE,3,direction)
                actual=Engine(law).step(state)
                self.assertTrue(np.array_equal(actual.b,expected))
                self.assertTrue(Engine(law).inverse_step(actual).same_as(state))

    def test_equal_complete_carrier_different_memory_changes_future(self):
        for direction in DIRECTIONS:
            result=history_intervention(3,direction,26)
            self.assertTrue(any(result["coupled_carrier_component_differences"]))
            self.assertFalse(any(result["disconnected_carrier_component_differences"]))

    def test_homogeneous_empty_and_periodic_no_growth_controls(self):
        empty=np.zeros((3,27),dtype=object)
        scores=structure_trace([empty]*13,3,DIRECTIONS[0])
        self.assertEqual([r["score"] for r in scores],[0]*13)
        gate=episode_gate(scores,[0,1,0]*4)
        self.assertTrue(gate["at_least_four"])
        self.assertFalse(gate["strict_growth"])

    def test_outside_boolean_amplitudes_rejected_as_structure(self):
        with self.assertRaises(ValueError):sorting_collision(0,2,0)
        with self.assertRaises(ValueError):sorting_collision(False,1,0)
        values=np.ones((3,27),dtype=object); values[1,0]=2
        with self.assertRaises(ValueError):axial_motifs(values,3,DIRECTIONS[0])
        values[1,0]=0.5
        with self.assertRaises(ValueError):axial_motifs(values,3,DIRECTIONS[0])

    def test_mutating_memory_does_not_directly_change_score(self):
        values=np.asarray([[0]*27,[n%2 for n in range(27)],[(n//2)%2 for n in range(27)]],dtype=object)
        before=axial_motifs(values,3,DIRECTIONS[0]); values[0]=1
        self.assertEqual(before,axial_motifs(values,3,DIRECTIONS[0]))

    def test_episode_protocol_rejects_truncation(self):
        with self.assertRaises(ValueError):episode_gate([{"score":0}], [1])

    def test_projective_phase_direction_ignores_amplitude_and_denominator_representation(self):
        law=Tensor([GearType(name,'audit') for name in
                    ('projective.denominator','projective.phi','projective.chi')],[],strict_support=True)
        rows=np.asarray([[1]*27,[1]*27,[n%3 for n in range(27)]],dtype=object)
        seed=State(3,rows.copy(),rows.copy(),np.zeros((3,27),dtype=object))
        expected=projective_phase_relations(seed,law)
        scaled_values=seed.b.astype(object)
        for n in range(27):scaled_values[1:,n]*=(n+1)*10**30
        scaled=State(3,seed.a.copy(),scaled_values,seed.r.copy())
        self.assertEqual(projective_phase_relations(scaled,law),expected)
        equivalent=seed.copy();equivalent.b[:,0]*=-1
        self.assertEqual(projective_phase_relations(equivalent,law),expected)

    def test_projective_phase_reader_rejects_zero_current_denominator(self):
        law=Tensor([GearType(name,'audit') for name in
                    ('projective.denominator','projective.phi','projective.chi')],[],strict_support=True)
        rows=np.zeros((3,27),dtype=object)
        seed=State(3,rows.copy(),rows.copy(),rows.copy())
        with self.assertRaises(ValueError):projective_phase_relations(seed,law)


if __name__=="__main__":unittest.main()
