"""Finite all-register comparison of independent dense and sparse executors."""
from itertools import product
from pathlib import Path
import hashlib
import json
import os
import random
import time
import unittest
from research.reference import addresses,index,flatten,advance,rewind
from universe24 import Channel,Coupling,Cube,Engine,State


def generated_case(side,density,seed,background=(0,0,2)):
    """Fixed order/PRNG; preserve generator plus explicit preparation on failure."""
    rng=random.Random(seed);cells={}
    for addr in addresses(side):
        if density=='dense' or rng.randrange(13)==0:
            cells[addr]=(rng.randrange(-5,6),rng.randrange(-5,6),rng.randrange(6))
    return State(Cube(side),Channel(*background),cells)


def mismatch_details(initial,signs,seed,density,step,expected,actual):
    side=initial.cube.side
    position=next(i for i,(a,b) in enumerate(zip(expected,actual)) if a!=b)
    address=list(addresses(side))[position]
    return {'format':'universe24-reference-counterexample-v1',
            'side':side,'signs':list(signs),'background':list(initial.background),
            'seed':seed,'density':density,'step':step,'first_differing_address':list(address),
            'expected':list(expected[position]),'actual':list(actual[position]),
            'initial':{'side':side,'coupling_signs':list(signs),
                       'background':list(initial.background),
                       'seed_changes':[{'position':list(a[:3]),'channel':a[3],'state':list(v)}
                                       for a,v in sorted(initial.cells.items())]},
            'reproduction_command':'python -m unittest discover -s tests -p test_reference_evolution.py -v'}


class ReferenceEvolutionTests(unittest.TestCase):
    def assert_state_equal(self,expected,actual,initial,signs,seed,density,step,stage="forward"):
        if expected==actual:return
        report=mismatch_details(initial,signs,seed,density,step,expected,actual)
        report["stage"]=stage
        target=os.environ.get('U24_COUNTEREXAMPLE_DIR')
        if target:
            folder=Path(target);folder.mkdir(parents=True,exist_ok=True)
            raw=json.dumps(report,sort_keys=True,indent=2)+'\n'
            path=folder/('reference-'+hashlib.sha256(raw.encode()).hexdigest()[:16]+'.json')
            # Never overwrite prior evidence, including a failed original case.
            if not path.exists():path.write_text(raw)
        self.fail(json.dumps(report,sort_keys=True))

    def test_96_full_state_trajectories(self):
        start=time.process_time();cases=0
        for signs,side,density,seed in product(product((-1,1),repeat=3),(3,4,5),('sparse','dense'),(24001,24002)):
            with self.subTest(signs=signs,L=side,density=density,seed=seed):
                self.assertLess(time.process_time()-start,300,'Declared 300 CPU second budget exhausted')
                engine=Engine(Coupling(signs));initial=generated_case(side,density,seed)
                dense=flatten(initial.cells,side,initial.background);old_dense=dense;state=initial
                for step in range(1,9):
                    before=state;old_dense=dense
                    dense=advance(dense,side,signs);state=engine.advance(state)
                    actual=flatten(state.cells,side,state.background)
                    self.assert_state_equal(dense,actual,initial,signs,seed,density,step)
                    self.assert_state_equal(old_dense,rewind(dense,side,signs),initial,signs,seed,density,step,"reference_inverse")
                    self.assert_state_equal(flatten(before.cells,side,before.background),
                                            flatten(engine.rewind(state).cells,side,state.background),
                                            initial,signs,seed,density,step,"production_inverse")
                    # Audit the other composition on a valid current state.
                    self.assert_state_equal(old_dense,advance(rewind(old_dense,side,signs),side,signs),
                                            initial,signs,seed,density,step,"other_inverse_composition")
                for _ in range(8):
                    dense=rewind(dense,side,signs);state=engine.rewind(state)
                self.assert_state_equal(flatten(initial.cells,side,initial.background),dense,
                                        initial,signs,seed,density,8,"complete_reference_rewind")
                self.assert_state_equal(flatten(initial.cells,side,initial.background),
                                        flatten(state.cells,side,state.background),
                                        initial,signs,seed,density,8,"complete_production_rewind")
                cases+=1
        self.assertEqual(cases,96)

    def test_all_background_remainders(self):
        for signs,r in product(product((-1,1),repeat=3),range(6)):
            initial=generated_case(3,'sparse',24003,(0,0,r));engine=Engine(Coupling(signs))
            dense=flatten(initial.cells,3,initial.background);nxt=advance(dense,3,signs)
            state=engine.advance(initial)
            self.assert_state_equal(nxt,flatten(state.cells,3,state.background),initial,signs,24003,'sparse',1)
            self.assertEqual(rewind(nxt,3,signs),dense)

    def test_coordinate_boundaries_and_iteration_order(self):
        for signs in ((1,1,1),(1,-1,1)):
            initial=State(Cube(3),cells={(0,0,0,2):Channel(2,5,1),(2,2,2,14):Channel(-3,-7,5)})
            dense=flatten(initial.cells,3)
            expected=advance(dense,3,signs)
            backwards=advance(dense,3,signs,order=reversed(range(len(dense))))
            self.assertEqual(expected,backwards)
            engine=Engine(Coupling(signs));actual=engine.advance(initial)
            self.assert_state_equal(expected,flatten(actual.cells,3),initial,signs,None,'boundary',1)
            reverse_insert=State(Cube(3),cells=dict(reversed(list(initial.cells.items()))))
            self.assertEqual(engine.advance(reverse_insert),actual)
            self.assertEqual(rewind(expected,3,signs,order=reversed(range(len(dense)))),dense)

    def test_size_independence_inside_nonwrapping_cone(self):
        # Initial support translated to cube center; radius <= 3 never wraps.
        histories=[]
        for side in (9,13):
            mid=side//2;initial=State(Cube(side),cells={(mid,mid,mid,2):Channel(0,3,2)})
            state=initial;engine=Engine(Coupling((1,-1,1)));states=[]
            for _ in range(4):
                states.append({(x-mid,y-mid,z-mid,g):tuple(v) for (x,y,z,g),v in state.cells.items()})
                state=engine.advance(state)
            histories.append(states)
        self.assertEqual(*histories)


if __name__=='__main__':unittest.main()
