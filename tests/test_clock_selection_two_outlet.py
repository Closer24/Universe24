"""Orthogonal preparation integrity without forward evolution."""
import json
import unittest

from universe24 import Channel, State
from research.clock_selection import two_outlet as study


class OrthogonalInputTests(unittest.TestCase):
    def setUp(self):
        self.protocol=json.loads(study.PROTOCOL.read_text())

    def test_complete_Y_template_rejects_hidden_remainder_change(self):
        case={'id':'test','side':369,'axis':'Y','gap':34,'phase':0,
              'clock_mode':'bare','stage':'isolated','control':'01'}
        state=study.prepare(case,self.protocol).initial
        origin=study.origins(case)['Y']
        self.assertTrue(study.matches(state,'Y',origin))
        cells=dict(state.cells);cells[(*origin,47)]=Channel(0,0,3)
        altered=State(state.cube,state.background,cells)
        self.assertFalse(study.matches(altered,'Y',origin))

    def test_full_source_absence_and_clock_mask_stay_local(self):
        case={'id':'test','side':369,'gap':34,'phase':2,'clock_mode':'on','stage':'encounter'}
        footprints=study.source_footprints(case)
        self.assertEqual([len(footprints[x]) for x in ('X','Y')],[24,24])
        self.assertFalse(set(footprints['X'])&set(footprints['Y']))
        self.assertTrue(study.footprint_checks(case,self.protocol)['passed'])
        on=study.prepare({**case,'control':'11'},self.protocol).initial
        off=study.prepare({**case,'control':'11','clock_mode':'counter_off'},self.protocol).initial
        addresses=on.cells.keys()|off.cells.keys();c=369//2
        self.assertEqual({a for a in addresses if on.at(a)!=off.at(a)},{(c,c,c,2)})
        self.assertTrue(all(on.at(a).r==off.at(a).r for a in addresses))


if __name__=='__main__':unittest.main()
