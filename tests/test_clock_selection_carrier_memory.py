"""Regression guards for the downstream terminal-record observer."""
import copy
import json
import unittest
from research.clock_selection import carrier_memory as cm


def _registered_fake_group():
    p=json.loads(cm.PROTOCOL.read_text());family=next(cm.groups(p));rows=[]
    for case in family:
        phase=0 if case['control'] in ('00','01','11') else 2
        centers=[[*cm.PHASES[(phase+t)%4],0] for t in range(121)]
        clock={'center_trace':centers,'region_trace':[[value]*336 for value in centers],
               'complete_canonical_orbit':True,'holds':{'terminal':{'passed':True}}}
        obs={'incoming':{name:{'passed':True} for name in ('writer','probe')},'active_boundary_hit':False,
             'whole_board_period4':True,'epochs':{name:{'truth_table_pass':True} for name in ('early','late')},
             'clocks':{'receiver':copy.deepcopy(clock),'controller':copy.deepcopy(clock)},'C_counts':{'0':0,'1':0,'2':0}}
        rows.append({'case':case,'observations':obs})
    return p,rows


class TerminalRecordGuardTests(unittest.TestCase):
    def test_writer_armed_difference_cannot_replace_distinct_terminal_record(self):
        p,rows=_registered_fake_group();result=cm.assess(rows,p)
        assert result['weaker_writer_armed_record']
        assert not result['primary_terminal_record']
        assert not result['comparisons_11_against']['00']['full336_differs_every_state']
        assert not result['comparisons_11_against']['01']['fixed_nonzero_phase']
    
    
    def test_full_region_difference_without_phase_difference_is_insufficient(self):
        p,rows=_registered_fake_group()
        for row in rows:
            if row['case']['control']=='11':
                for frame in row['observations']['clocks']['receiver']['region_trace']:
                    frame[-1]=[0,0,4]
        result=cm.assess(rows,p)
        assert result['comparisons_11_against']['00']['full336_differs_every_state']
        assert not result['comparisons_11_against']['00']['fixed_nonzero_phase']
        assert not result['primary_terminal_record']

if __name__ == "__main__":
    unittest.main()
