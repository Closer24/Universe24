"""Adversarial checks for complete blocking and source/protocol identity."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from universe24 import Channel,Cube,State
from research.signal_clocks.paired_blocker import outlet_report,prepare_paired
from research.signal_clocks.build_presenter import package


class SignalClockBlockTests(unittest.TestCase):
    def test_remainder_only_outlet_leak_defeats_strong_block(self):
        baseline=State(Cube(101),Channel(0,0,2),{})
        trace=[baseline]*41
        trace[7]=State(baseline.cube,baseline.background,{(44,50,50,47):Channel(0,0,4)})
        result=outlet_report(trace,[baseline]*41,-1)
        self.assertTrue(result['weak_b_block'])
        self.assertFalse(result['strong_complete_outlet_block'])
        self.assertEqual(result['first_leak'],{'step':7,'channel':47,'component':'r',
                         'difference':2,'actual':[0,0,4],'baseline':[0,0,2]})

    def test_unseen_a_counter_is_not_hidden_by_a_quiet_b_counter(self):
        baseline=State(Cube(101),Channel(0,0,2),{})
        trace=[baseline]*41
        trace[40]=State(baseline.cube,baseline.background,{(56,50,50,31):Channel(1,0,2)})
        result=outlet_report(trace,[baseline]*41,1)
        self.assertTrue(result['weak_b_block'])
        self.assertFalse(result['strong_complete_outlet_block'])
        self.assertEqual(result['first_leak']['component'],'a')
        self.assertEqual(result['first_leak']['step'],40)

    def test_paired_source_control_changes_only_initial_source_counters(self):
        case={'side':101,'variants':['O','N']}
        _,on,locations=prepare_paired(case,(True,))
        _,off,_=prepare_paired(case,(False,))
        source=locations['origin']
        changed={addr for addr in on.cells.keys()|off.cells.keys()if on.at(addr)!=off.at(addr)}
        self.assertEqual(changed,{(*source,0),(*source,14)})
        self.assertTrue(all(not value.a and not value.b for value in off.cells.values()))
        self.assertTrue(all(on.at(addr).r==off.at(addr).r for addr in on.cells.keys()|off.cells.keys()))

    def test_valid_hashes_cannot_disguise_changed_protocol_semantics(self):
        runs=Path(__file__).resolve().parents[1]/'runs';runs.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=runs,prefix='protocol-identity-test-')as temporary:
            root=Path(temporary)
            canonical=root/'copy.json';registered=root/'registered.json'
            canonical.write_text(json.dumps({'criterion':'two events'}))
            registered.write_text(json.dumps({'criterion':'one event'}))
            def ref(path):return {'path':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
            descriptor={'format':'universe24-signal-clock-presentation-v1',
                'protocol':ref(canonical),'cases':[{'id':'changed-protocol','title':'Invalid identity',
                    'protocol':ref(canonical),'registered_protocol':ref(registered),
                    'trace':'not-needed.jsonl','trace_sha256':'0'*64}]}
            path=root/'descriptor.json';path.write_text(json.dumps(descriptor))
            with self.assertRaisesRegex(ValueError,'Registered protocol semantics differ'):
                package(path,root/'output')
            self.assertFalse((root/'output').exists())


if __name__=='__main__':
    unittest.main()
