"""Integrated regression of the prepared guide, including its limitations."""
import importlib.util
from pathlib import Path
import unittest
from universe24 import Coupling,Engine
P=Path(__file__).resolve().parents[1]/'research'/'signal_memory'/'run.py'
spec=importlib.util.spec_from_file_location('guide_runner',P);guide=importlib.util.module_from_spec(spec);spec.loader.exec_module(guide)

class GuideRecordTests(unittest.TestCase):
    def setUp(self):
        self.engine=Engine(Coupling((1,1,1)))
    def trajectory(self,control='none',L=101):
        initial,origin=guide.prepare({'N':18,'L':L,'j':2,'control':control})
        states=list(self.engine.evolve(initial,40))
        return states,(origin[0]+2,origin[1],origin[2]),origin
    def test_first_record_and_reactivation(self):
        states,target,_=self.trajectory()
        bits=[guide.memory(s,target) for s in states]
        self.assertEqual(bits[:37],[int(2<=t<36) for t in range(37)])
        self.assertEqual(bits[40],1) # No claim of unique permanent detection.
        for old,new in zip(states,states[1:]):self.assertEqual(self.engine.rewind(new),old)
    def test_no_source_and_source_only_controls(self):
        for control in ('no_source','source_only'):
            states,target,_=self.trajectory(control)
            self.assertFalse(any(guide.memory(s,target) for s in states))
    def test_complete_state_size_independence(self):
        a,_,oa=self.trajectory(L=101);b,_,ob=self.trajectory(L=121)
        self.assertEqual([guide.normalized(s,oa) for s in a],[guide.normalized(s,ob) for s in b])
    def test_parity_perturbation_exposes_readout_limit(self):
        states,target,_=self.trajectory('r_plus_one')
        self.assertFalse(any(guide.memory(s,target) for s in states))
        self.assertNotEqual(states[2].at((*target,0)).b,0)
        self.assertEqual(states[2].at((*target,0)).r%2,1)

if __name__=='__main__':unittest.main()
