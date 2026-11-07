"""Independent exact-matrix algebra and hand-derived arithmetic anchors."""
from itertools import product
from pathlib import Path
import ast
import hashlib
import json
import os
import unittest
from research.reference import algebra,coupling,forward,inverse
from research.reference.algebra import CX,CY,IDENTITY,matmul,transpose,explicit_matrices
from universe24.core.group_2o import group
from universe24.core.coupling import Coupling
from universe24.core.rule3 import forward as production_forward,inverse as production_inverse
from universe24.core.state import Channel


class ReferenceAlgebraTests(unittest.TestCase):
    def assert_table_equal(self,expected,actual,case,**context):
        if expected==actual:return
        path=[];left,right=expected,actual
        while isinstance(left,(tuple,list)) and isinstance(right,(tuple,list)) and len(left)==len(right):
            i=next(i for i,(a,b) in enumerate(zip(left,right)) if a!=b)
            path.append(i);left,right=left[i],right[i]
        report={'format':'universe24-algebra-counterexample-v1','case':case,
                'context':context,'index':path,'expected':left,'actual':right,
                'reproduction_command':'python -m unittest discover -s tests -p test_reference_algebra.py -v'}
        raw=json.dumps(report,sort_keys=True,indent=2)+'\n'
        target=os.environ.get('U24_COUNTEREXAMPLE_DIR')
        if target:
            folder=Path(target);folder.mkdir(parents=True,exist_ok=True)
            dest=folder/('algebra-'+hashlib.sha256(raw.encode()).hexdigest()[:16]+'.json')
            if not dest.exists():dest.write_text(raw)
        self.fail(raw)

    def test_reference_has_no_production_import(self):
        root=Path(__file__).resolve().parents[1]/'research/reference'
        for path in root.glob('*.py'):
            tree=ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node,ast.Import):
                    self.assertFalse(any(n.name.split('.')[0]=='universe24' for n in node.names),path)
                if isinstance(node,ast.ImportFrom):
                    self.assertNotEqual((node.module or '').split('.')[0],'universe24',path)

    def test_closed_form_and_label_anchors(self):
        ref=algebra()
        self.assertEqual(set(ref.matrices),set(explicit_matrices()))
        self.assertEqual(len(ref.matrices),48)
        self.assertEqual(ref.matrices[:3],(IDENTITY,CX,CY))
        self.assertEqual(ref.central,14)
        self.assertEqual(ref.matrices[14],tuple(tuple(-x for x in row) for row in IDENTITY))
        self.assertEqual(len(set(ref.rotations)),24)
        self.assertEqual(ref.rotations[1],((1,0,0),(0,0,-1),(0,1,0)))
        self.assertEqual(ref.rotations[2],((0,0,1),(0,1,0),(-1,0,0)))
        for m in ref.matrices:
            self.assertEqual(matmul(m,transpose(m)),IDENTITY)

    def test_all_products_inverses_and_rotations(self):
        ref=algebra();actual=group()
        self.assert_table_equal(ref.multiplication,actual.multiplication,"multiplication") # all 2304
        self.assert_table_equal(ref.inverses,actual.inverses,"inverses") # all 48
        self.assert_table_equal(ref.rotations,actual.rotations,"rotations") # all 48 labels
        for i in range(48):
            self.assertEqual(ref.multiplication[i][ref.inverses[i]],0)
            self.assertEqual(ref.multiplication[ref.inverses[i]][i],0)

    def test_all_coupling_choices(self):
        for signs in product((-1,1),repeat=3):
            with self.subTest(signs=signs):
                ref=coupling(signs);actual=Coupling(signs)
                self.assert_table_equal(ref.ports,actual.ports,"coupling_ports",signs=signs) # 6*48 entries each
                self.assert_table_equal(ref.weights,actual.weights,"coupling_weights",signs=signs)
                for d in range(6):
                    self.assertEqual(sorted(ref.ports[d]),list(range(48)))
                    for g in range(48):
                        h=ref.ports[d][g]
                        self.assertEqual(ref.ports[d^1][h],g)
                        self.assertEqual(ref.weights[d^1][h],ref.weights[d][g])

    def test_hand_derived_rule3_anchors(self):
        cases=[((2,5,1),10,(5,1,3)),
               ((0,0,2),0,(0,0,2)),
               ((0,0,2),1,(0,0,4)),
               ((0,0,2),2,(0,1,0)),
               ((0,0,0),-1,(0,-1,4)),
               ((0,0,1),-1,(0,-1,5)),
               ((-2,3,5),-4,(3,1,3)),
               ((2,-3,0),3,(-3,-1,0))]
        for old,u,expected in cases:
            self.assertEqual(forward(old,u),expected)
            self.assertEqual(production_forward(Channel(*old),u),expected)
            self.assertEqual(inverse(expected,u),old)
            self.assertEqual(production_inverse(Channel(*expected),u),old)

    def test_scalar_both_directions_and_all_remainders(self):
        values=(-10**80,-3,0,7,10**81)
        for a,b,r,u in product(values,values,range(6),(-10**82,-4,-3,-1,0,1,2,3,10**83)):
            old=(a,b,r);nxt=forward(old,u)
            self.assertEqual(nxt,production_forward(Channel(*old),u))
            self.assertEqual(inverse(nxt,u),old)
            self.assertEqual(forward(inverse(old,u),u),old)
            self.assertEqual(production_inverse(Channel(*old),u),inverse(old,u))
            self.assertEqual(nxt[2]%2,r%2)


if __name__=='__main__':unittest.main()
