"""Counterfactual preparation integrity and frozen acceptance safeguards."""
import unittest

from universe24 import Channel, Cube, State
from research.clock_selection.mediation import cross_initial, region_addresses, assess_group


class ClockRegionMediationTests(unittest.TestCase):
    def test_cross_copies_full_remainders_and_preserves_exterior(self):
        side=11;cube=Cube(side);bg=Channel(0,0,2)
        region=region_addresses(side);center=region[0];hidden=region[-1]
        exterior_address=(1,1,1,47)
        exterior=State(cube,bg,{center:Channel(10,-11,3),hidden:Channel(0,0,4),
                                exterior_address:Channel(-5,7,1)})
        donor=State(cube,bg,{center:Channel(-17,19,0),exterior_address:Channel(1,1,2)})
        crossed=cross_initial(exterior,donor,region)
        self.assertEqual(len(set(region)),336)
        self.assertEqual(crossed.at(center),donor.at(center))
        self.assertEqual(crossed.at(hidden),bg)
        self.assertEqual(crossed.at(exterior_address),exterior.at(exterior_address))
        self.assertEqual(cross_initial(exterior,exterior,region),exterior)

    def test_false_native_replay_or_invalid_input_rejects_group(self):
        rows=[]
        for e in ('01','11'):
            for r in ('01','11'):
                a={k:True for k in ('split_equivalence','incoming_contract','near_incoming_contract',
                    'initial_hold','strict_initial_causal_margin','no_active_boundary_contact',
                    'carrier_follows_region','C_follows_region')}
                a['native_suffix_equal']=True if e==r else None
                rows.append({'case':{'side':337,'gap':36,'exterior_source':e,'region_source':r},
                    'assessment':a,'experiment':{'provenance':{'full_rewind_equal':True}}})
        self.assertTrue(assess_group(rows)['accepted_clock_region_mediation'])
        self.assertFalse(assess_group(rows[:3])['accepted_clock_region_mediation'])
        rows[0]['assessment']['native_suffix_equal']=False
        self.assertFalse(assess_group(rows)['accepted_clock_region_mediation'])
        rows[0]['assessment']['native_suffix_equal']=True
        rows[1]['assessment']['near_incoming_contract']=False
        self.assertFalse(assess_group(rows)['accepted_clock_region_mediation'])


if __name__=='__main__':unittest.main()
