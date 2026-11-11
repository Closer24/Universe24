"""Current integer preparations and algebra; these checks do not prove physics.

The removed calibration suites tested a different large-divisor model. This
suite retains finite algebra and exact integer invariants that remain meaningful.
"""
import unittest
import numpy as np
from universe24.core import Engine, State, Tensor, compose
from universe24.layers.reference_model import reference_system
from universe24.layers.matter import algebra, build_matter
from universe24.layers.chiral import chiral_algebra
from universe24.layers.gauge import ALGEBRAS
from universe24.layers.electroweak import hypercharge_generators
from universe24.prepare import vacuum_state, with_gears
from universe24.prepare.reference_model import reference_seed
from universe24.prepare.system import random_system_state


class FixedSixPreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = reference_system()
        cls.tensor = compose(*cls.system.blocks)
        cls.engine = Engine(cls.tensor)

    def test_default_integer_seed_is_complete_and_repeatable(self):
        seed, info = reference_seed(self.system,self.tensor,5)
        repeat, info2 = reference_seed(self.system,self.tensor,5)
        self.assertTrue(seed.same_as(repeat)); self.assertEqual(info,info2)
        self.assertEqual(seed.G,48); self.assertEqual(info["amplitude"],3)
        self.assertEqual(np.count_nonzero(seed.b),1)
        self.assertTrue(all(isinstance(v,(int,np.integer)) for array in (seed.a,seed.b,seed.r) for v in array.flat))
        self.assertTrue(all(0 <= int(r) < 6 for r in seed.r.flat))
        self.assertNotIn("Q",info)

    def test_all_preparations_rewind_without_mutating_seed(self):
        for kind in ("pulse","standing","none"):
            seed,info = reference_seed(self.system,self.tensor,3,bang=kind)
            initial=seed.copy()
            final=self.engine.run(seed,12)
            self.assertTrue(self.engine.rewind(final,12).same_as(seed),kind)
            self.assertTrue(seed.same_as(initial),kind)
            if kind == "none": self.assertTrue(final.same_as(seed))
        with self.assertRaisesRegex(ValueError,"retired"):
            reference_seed(self.system,self.tensor,3,bang="jpure")
        with self.assertRaises(TypeError):
            reference_seed(self.system,self.tensor,3,rng_seed=1.5)

    def test_pulse_records_are_nontrivial_and_inside_local_cone(self):
        seed,_=reference_seed(self.system,self.tensor,7)
        initial=seed.copy()
        control,_=reference_seed(self.system,self.tensor,7,bang="none")
        origin=seed.lattice.index(3,3,3)
        origin_xyz=seed.lattice.coords(origin)
        total=0
        for tick in range(1,7):
            nxt=self.engine.step(seed)
            total += len(list(self.engine.clicks(seed,nxt,tick).rows()))
            seed=nxt;control=self.engine.step(control)
            changed=np.any((seed.a != control.a)|(seed.b != control.b)|(seed.r != control.r),axis=0)
            for node in np.flatnonzero(changed):
                xyz=seed.lattice.coords(int(node))
                distance=sum(min(abs(x-y),7-abs(x-y)) for x,y in zip(xyz,origin_xyz))
                self.assertLessEqual(distance,tick)
        self.assertGreater(total,0)
        self.assertTrue(self.engine.rewind(seed,6).same_as(initial))

    def test_random_data_and_bigint_injection_are_exact(self):
        seed=random_system_state(self.system,self.tensor,3,seed=5)
        self.assertTrue(all(0 <= int(r) < 6 for r in seed.r.flat))
        name=self.tensor.names[0]
        large=2**120+7
        prepared=with_gears(seed,self.tensor,{(name,(0,0,0)):(-large,large,5)})
        self.assertEqual(prepared.gear(0,0),(-large,large,5))
        self.assertTrue(self.engine.inverse_step(self.engine.step(prepared)).same_as(prepared))
        self.assertNotEqual(seed.gear(0,0),prepared.gear(0,0))

    def test_generic_integer_matrix_block_keeps_fixed_six_inverse(self):
        block=build_matter(hop=1,mass=2,wilson=0)
        tensor=compose(block); engine=Engine(tensor)
        seed=vacuum_state(tensor,3,block)
        seed=with_gears(seed,tensor,{("matter.X0",(1,1,1)):(-2**90,2**91,5)})
        self.assertEqual(engine.D,6)
        self.assertTrue(engine.rewind(engine.run(seed,8),8).same_as(seed))
        self.assertEqual(tensor.support_violations(),[])

    def test_seed_setters_reject_fractional_data_and_invalid_remainders(self):
        seed,_=reference_seed(self.system,self.tensor,3,bang="none")
        name=self.tensor.names[0]
        with self.assertRaises(TypeError):
            with_gears(seed,self.tensor,{(name,(0,0,0)):(1.5,2,3)})
        for remainder in (-1,6,1.5,True):
            with self.assertRaises(ValueError):
                with_gears(seed,self.tensor,{(name,(0,0,0)):(1,2,remainder)})
        from universe24.prepare.seed import l0_dark_seed
        with self.assertRaises(TypeError):
            l0_dark_seed(seed,self.tensor,(0,0,0),1,v=[1.5]+[0]*47)

    def test_rounded_and_calibrated_preparations_are_explicitly_retired(self):
        from universe24.prepare.em import dirac_packet
        from universe24.prepare.em_compact import gauss_links
        from universe24.prepare.seed import m0_band_vector
        from universe24.prepare.gravity import with_clocks
        calls=(lambda:dirac_packet({},3,1,1.0,3),
               lambda:gauss_links(None,None,None,1,6),
               lambda:m0_band_vector(),
               lambda:with_clocks(None,None,"g",1,[],3))
        for call in calls:
            with self.assertRaisesRegex(NotImplementedError,"retired"):
                call()


class ExactFiniteAlgebraTests(unittest.TestCase):
    def test_integer_quaternion_and_clifford_relations(self):
        for species in ("pair","single"):
            alg=algebra(species); eye=np.eye(alg["n"],dtype=np.int64)
            for i,p in enumerate(alg["P"]):
                np.testing.assert_array_equal(p @ p,-eye)
                for j,q in enumerate(alg["P"]):
                    if i != j: np.testing.assert_array_equal(p @ q + q @ p,0*eye)
                np.testing.assert_array_equal(p @ alg["W0"]+alg["W0"] @ p,0*eye)
            np.testing.assert_array_equal(alg["J"] @ alg["J"],-eye)
            np.testing.assert_array_equal(alg["K"] @ alg["K"],-eye)
            np.testing.assert_array_equal(alg["J"] @ alg["K"],-alg["K"] @ alg["J"])

    def test_quaternion_and_gaussian_units_form_exact_matrix_groups(self):
        for name in ("su2","u1"):
            alg=ALGEBRAS[name]
            matrices=[np.asarray(alg.left_matrix(x),dtype=object) for x in alg.group]
            keys={tuple(m.flat) for m in matrices}
            eye=np.eye(alg.m,dtype=object)
            self.assertIn(tuple(eye.flat),keys)
            for left in matrices:
                np.testing.assert_array_equal(left.T @ left,eye)
                for right in matrices: self.assertIn(tuple((left @ right).flat),keys)

    def test_chiral_projectors_and_hypercharge_are_algebra_not_particle_claims(self):
        alg=chiral_algebra(); eye=np.eye(32,dtype=np.int64)
        np.testing.assert_array_equal(alg["PiW"] @ alg["PiW"],2*alg["PiW"])
        np.testing.assert_array_equal(alg["PiW"]+alg["PiS"],2*eye)
        np.testing.assert_array_equal(alg["PiW"] @ alg["PiS"],0*eye)
        t1,t2,t3=alg["t"]
        np.testing.assert_array_equal(t1 @ t2,t3)
        for matter,higgs in hypercharge_generators().values():
            np.testing.assert_array_equal(matter.T,-matter)
            np.testing.assert_array_equal(higgs.T,-higgs)
