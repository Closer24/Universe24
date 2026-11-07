import unittest
import random
from itertools import product
from universe24.core import Channel,Coupling,Cube,Engine,State
from universe24.core.group_2o import group
from research.reflection_audit import (INVERSION,MIRROR_X,direction_map,search,
    verify_certificate,weighted_covariance,naive_counterexample,transform,
    channel_signs,negate_channel,mirror_x_lift)


class ReflectionAuditTests(unittest.TestCase):
    def test_improper_maps_need_signs_for_current_coupling(self):
        coupling=Coupling((1,-1,1))
        for rotation in set(group().rotations):
            improper=tuple(tuple(-v for v in row) for row in rotation)
            solutions,certificates=search(improper)
            self.assertEqual(len(solutions),8)
            self.assertEqual(len(certificates),40)
            for p in solutions:
                self.assertFalse(weighted_covariance(coupling,improper,p))
                sigma=channel_signs(coupling,improper,p)
                self.assertIsNotNone(sigma)
                self.assertTrue(weighted_covariance(coupling,improper,p,sigma))
            for certificate in certificates:
                self.assertTrue(verify_certificate(Coupling().ports,direction_map(improper),certificate))

    def test_search_has_positive_rotation_controls(self):
        for matrix in set(group().rotations):
            solutions,_=search(matrix)
            self.assertTrue(solutions)

    def test_weighted_rotation_covariance(self):
        algebra=group()
        for signs in product((-1,1),repeat=3):
            coupling=Coupling(signs)
            for h in range(48):
                self.assertTrue(weighted_covariance(coupling,algebra.rotations[h],algebra.multiplication[h]))

    def test_exact_state_covariance_and_mirror_failure(self):
        rng=random.Random(24048);cube=Cube(5);algebra=group()
        state=State(cube,cells={(rng.randrange(5),rng.randrange(5),rng.randrange(5),rng.randrange(48)):
                   Channel(rng.randrange(-20,21),rng.randrange(-20,21),rng.randrange(6)) for _ in range(80)})
        engine=Engine(Coupling((1,-1,1)));after=engine.advance(state)
        for h in range(48):
            self.assertEqual(engine.advance(transform(state,algebra.rotations[h],algebra.multiplication[h])),
                             transform(after,algebra.rotations[h],algebra.multiplication[h]))
        self.assertTrue(naive_counterexample()['differences'])

    def test_scalar_sign_reversal_retains_every_remainder(self):
        from universe24.core.rule3 import forward
        for a,b,r,u in product((-10**30,0,11),(-7,0,10**31),range(6),(-10**35,-1,0,1,32)):
            value=Channel(a,b,r)
            self.assertEqual(negate_channel(negate_channel(value)),value)
            self.assertEqual(forward(negate_channel(value),-u),negate_channel(forward(value,u)))

    def test_signed_reflections_full_state_and_all_weights(self):
        rng=random.Random(48024);algebra=group()
        for weights in product((-1,1),repeat=3):
            engine=Engine(Coupling(weights))
            state=State(Cube(5),cells={(rng.randrange(5),rng.randrange(5),rng.randrange(5),rng.randrange(48)):
                        Channel(rng.randrange(-100,101),rng.randrange(-100,101),rng.randrange(6)) for _ in range(60)})
            after=engine.advance(state)
            for matrix in set(algebra.rotations):
                improper=tuple(tuple(-v for v in row) for row in matrix)
                permutation=search(improper)[0][0]
                sigma=channel_signs(engine.coupling,improper,permutation)
                self.assertEqual(engine.advance(transform(state,improper,permutation,sigma)),
                                 transform(after,improper,permutation,sigma))

    def test_mirror_square_and_fourth_power(self):
        engine=Engine(Coupling((1,-1,1)));p,sigma=mirror_x_lift(engine.coupling)
        seed=State(Cube(7),cells={(1,2,3,g):Channel(g-25,2*g-30,g%6) for g in range(48)})
        once=transform(seed,MIRROR_X,p,sigma)
        twice=transform(once,MIRROR_X,p,sigma)
        central=group().multiplication[group().central]
        identity=((1,0,0),(0,1,0),(0,0,1))
        self.assertEqual(twice,transform(seed,identity,central,(-1,)*48))
        self.assertNotEqual(twice,seed)
        self.assertEqual(transform(transform(twice,MIRROR_X,p,sigma),MIRROR_X,p,sigma),seed)
