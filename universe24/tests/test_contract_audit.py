"""Regressions for readout isolation, exact data and a fixed tensor contract."""
import math
import unittest
import numpy as np
from universe24.core import Engine, GearType, State, Tensor
from universe24.core.engine import OBJ
from universe24.core.lattice import ZERO
from universe24.observe.choice import kinds
from universe24.observe.one import state_hash
from universe24.observe.readout import official_clicks, own_frame_series

class ContractRegression(unittest.TestCase):
    def test_official_readout_excludes_audit_gears(self):
        t = Tensor([GearType('visible'), GearType('diagnostic', 'audit')],
                   [('visible', 3, ()), ('diagnostic', 3, ())])
        e = Engine(t)
        s = e.vacuum(3, [0, 0]); n = e.step(s)
        self.assertEqual(len(e.clicks(s, n)), 54)
        log = official_clicks(e, s, n)
        self.assertEqual(len(log), 27)
        self.assertEqual(set(log.label), {'official'})
        self.assertTrue(np.all(log.gear == 0))
        self.assertTrue(e.inverse_step(n).same_as(s))

    def test_fixed_point_carry_is_not_an_official_click(self):
        t = Tensor(['g'], [('g', 6, ())])
        e = Engine(t)
        a = np.ones((1, 27), dtype=np.int64)
        s = State(3, a, a.copy(), 2*a)
        n = e.step(s)
        self.assertTrue(n.same_as(s))
        self.assertEqual(len(e.clicks(s, n, stream='raw')), 27)
        self.assertEqual(len(official_clicks(e, s, n)), 0)

    def test_hash_is_storage_independent(self):
        a = np.arange(27, dtype=np.int64).reshape(1, 27)
        s = State(3, a, a-2, a % 6)
        obj = State._raw(3, s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ))
        self.assertEqual(state_hash(s, [0]), state_hash(obj, [0]))
        obj.r[0, 0] += 1
        self.assertNotEqual(state_hash(s, [0]), state_hash(obj, [0]))

    def test_large_coefficient_kind_is_exact(self):
        amplitude = 1 << 80
        t = Tensor(['g'], [('g', 2*amplitude, ())])
        e = Engine(t); s = e.vacuum(3, [0]); n = e.step(s)
        np.testing.assert_array_equal(kinds(t, e.D, s, n, 'g'), np.full(27, 2))

    def test_clicks_survive_large_counter_snapshot_reload(self):
        import json
        amplitude = 1 << 80
        # Zero and nonzero remainders, positive and negative carries, and an
        # empty event set must all retain identical records across serialization.
        for coeff in (0, 3*amplitude, 4*amplitude, -4*amplitude):
            t = Tensor(['g'], [('g', coeff, ())])
            e = Engine(t); s = e.vacuum(3, [0]); n = e.step(s)
            before, after = [State.from_dict(json.loads(json.dumps(v.to_dict()))) for v in (s,n)]
            for stream in ('raw', 'official'):
                self.assertEqual(e.clicks(before,after,stream=stream).rows(),
                                 e.clicks(s,n,stream=stream).rows())

    def test_rewind_rejects_invalid_horizons(self):
        e = Engine(Tensor(['g'], []))
        s = e.vacuum(3, [0])
        self.assertTrue(e.rewind(s,0).same_as(s))
        self.assertTrue(e.rewind(e.run(s,2),2).same_as(s))
        for steps in (-1, True, 1.5, '1'):
            with self.assertRaises(ValueError): e.rewind(s,steps)

    def test_engine_ignores_names_labels_link_metadata_and_field_signs(self):
        # Identical indexed polynomials with deliberately different physical
        # names and observer metadata must produce the same complete history.
        source = Tensor(['first','second'], [
            ('first',2,(('first',ZERO,'b'),('second',(1,0,0),'b'))),
            ('second',-1,(('first',ZERO,'a'),)),
        ])
        renamed = Tensor([
            GearType('gravity',label='audit',link=0,sign=-1,sign_why='metadata control'),
            GearType('photon',label='official',link=2),
        ],source.monomials)
        a=np.arange(54).reshape(2,27)%5-2
        initial=State(3,a,a+1,(a+2)%6)
        e,f=Engine(source),Engine(renamed)
        left=right=initial
        for _ in range(8):
            left,right=e.step(left),f.step(right)
            self.assertTrue(left.same_as(right))
        self.assertTrue(e.rewind(left,8).same_as(initial))
        self.assertTrue(f.rewind(right,8).same_as(initial))

    def test_tensor_cannot_change_under_compiled_engine(self):
        t = Tensor(['g'], [('g', 2, (('g', ZERO, 'b'),))])
        e = Engine(t); s = e.vacuum(3, [0]); e.step(s)
        for field, value in [('monomials', ()), ('stages', ()), ('gears', ())]:
            with self.assertRaises(AttributeError): setattr(t, field, value)
        with self.assertRaises(TypeError): t._index['g'] = 2
        with self.assertRaises(TypeError): t.designations[(0, ())] = 'changed'
        with self.assertRaises(AttributeError): del t.monomials
        self.assertEqual(Tensor.from_json(t.to_json()), t)
        for field,value in [('tensor',Tensor(['g'],[])),('D',12)]:
            with self.assertRaises(AttributeError):setattr(e,field,value)
            with self.assertRaises(AttributeError):delattr(e,field)

    def test_carrier_decoder_rejects_unsupported_angle(self):
        with self.assertRaises(ValueError): own_frame_series([1,2,3], 0.2)
        self.assertEqual(own_frame_series([1,2,3], math.pi/2), [1,-3])

    def test_run_report_keeps_each_update_and_actual_click_counts(self):
        from argparse import Namespace
        from universe24.demos.one.run_one import run, build, compare
        args=Namespace(L=3,bang='pulse',rng=13,tmax=3,budget=120,tag='test',
                       max_bits=256,rewind=True)
        report=run(args)
        self.assertEqual(report['t_end'],3)
        self.assertEqual([row['step'] for row in report['rows']],[1,2,3])
        _,t,e,s,_=build(3,'pulse',13)
        count=0
        for step in range(1,4):
            n=e.step(s)
            log=official_clicks(e,s,n,step)
            count+=len(log)
            s=n
        self.assertEqual(sum(row['official_records'] for row in report['rows']),count)
        self.assertTrue(report['rewind']['exact'])
        with self.assertRaises(ValueError):compare({'hashes':[]},report)

    def test_offline_decoder_rejects_nonofficial_or_duplicate_records(self):
        import gzip,json,tempfile
        from pathlib import Path
        from universe24.tools.audit_contract import decode_saved_clicks
        row=dict(step=1,xyz=[0,0,0],gear='cosmic.M1',kind=1,quotient=2,label='official')
        with tempfile.TemporaryDirectory(dir='.') as tmp:
            p=Path(tmp)/'events.jsonl.gz'
            def write(rows):
                with gzip.open(p,'wt') as f:
                    for r in rows:f.write(json.dumps(r)+'\n')
            write([row]);self.assertEqual(decode_saved_clicks(p)['records'],1)
            for rows in ([row,row],[dict(row,label='audit')],[dict(row,quotient=0)],
                         [dict(row,step=2),dict(row,step=1)]):
                write(rows)
                with self.assertRaises(ValueError):decode_saved_clicks(p)
