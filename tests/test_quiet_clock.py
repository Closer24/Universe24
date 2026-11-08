"""Initial clock contracts and immutable composition; no trajectory before approval."""
import unittest
from research.clock_selection.quiet_clock import QuietClock,outgoing_recipients
from research.components import BoardSpec,Patch,TensorSpec,finalize,place


class QuietClockContractTests(unittest.TestCase):
    def test_complete_contract_and_integer_amplitude_boundary(self):
        for a,b in ((0,1),(0,2),(1,1),(-1,-1)):
            patch=QuietClock(a=a,b=b)
            self.assertEqual(len(patch.cells),336)
            self.assertEqual(len(patch.ports['outgoing_recipients']),6)
            self.assertEqual(patch.evidence_domains[0]['counter_period'],4)
        for a,b in ((0,0),(0,3),(2,1)):
            with self.assertRaises(ValueError):QuietClock(a=a,b=b)
        with self.assertRaises(TypeError):QuietClock(a=True)

    def test_remainder_interval_and_parity_are_explicit(self):
        even=QuietClock(a=0,b=2,halo_parity=0)
        odd=QuietClock(a=0,b=2,r=3,halo_parity=1)
        for address in even.ports['outgoing_recipients']:
            self.assertEqual(dict(odd.cells)[address].r,dict(even.cells)[address].r+1)
        with self.assertRaises(ValueError):QuietClock(a=0,b=2,halo_remainders=(2,)*6)
        self.assertEqual(dict(QuietClock(r=5).cells)[(0,0,0,0)].r,5)

    def test_outgoing_map_is_inverse_of_opposite_input_row(self):
        from research.reference.algebra import coupling
        tensor=TensorSpec.from_signs((1,-1,1));reference=coupling((1,-1,1))
        for g in (0,2,14,39,47):
            for d,(address,weight) in enumerate(outgoing_recipients(tensor,g)):
                expected=[h for h in range(48) if reference.ports[d^1][h]==g]
                self.assertEqual([address[3]],expected)
                self.assertEqual(weight,reference.weights[d^1][address[3]])

    def test_full_halo_conflicts_rejected_without_overwrite(self):
        clock=QuietClock();address=clock.ports['outgoing_recipients'][0]
        old=dict(clock.cells)[address]
        conflict=Patch('conflict',{address:(0,0,(old.r+1)%6)})
        with self.assertRaisesRegex(ValueError,'conflict'):
            finalize(BoardSpec(5),[place(clock,at=(2,2,2),name='clock'),place(conflict,at=(2,2,2),name='other')])


if __name__=='__main__':unittest.main()
