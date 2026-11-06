"""Generic contract tests. No experiment-specific update laws."""
import unittest
from universe24.core import Channel,Coupling,Cube,Engine,State,VACUUM
from universe24.core.group_2o import group,DIRECTIONS,rotate
from universe24.core.rule3 import forward,inverse
from universe24.experiments import from_dict,checkpoint_data
from universe24.observation import clicks,classify,balance_residuals,signed_account,expected_account_change

class ModelTests(unittest.TestCase):
    def test_group(self):
        g=group()
        self.assertEqual(len(g.quaternions),48)
        self.assertEqual(g.central,14)
        self.assertEqual(len(set(g.rotations)),24)
        self.assertEqual(g.power(1,8),0)
        for a in range(48):
            self.assertEqual(g.multiplication[a][g.inverses[a]],0)
            self.assertEqual(g.multiplication[0][a],a)

    def test_coupling(self):
        for mask in range(8):
            signs=tuple(-1 if mask&(1<<i) else 1 for i in range(3))
            c=Coupling(signs)
            self.assertEqual(len(c.tensor()),6)
            for d in range(6):
                matrix=c.matrix(d)
                self.assertEqual(len(matrix),48)
                for row in matrix:
                    self.assertEqual(sum(abs(x) for x in row),1)
                self.assertEqual(matrix,tuple(tuple(c.matrix(d^1)[j][i]
                                                for j in range(48)) for i in range(48)))
            self.assertEqual(c.fingerprint,Coupling(signs).fingerprint)

    def test_scalar_exact_inverse(self):
        for a in (-10**35,-2,0,7):
            for b in (-3,0,9):
                for r in range(6):
                    for u in (-11,-1,0,2,13):
                        old=Channel(a,b,r)
                        self.assertEqual(inverse(forward(old,u),u),old)

    def test_cube_six_distinct(self):
        for side in (3,4,9):
            cube=Cube(side)
            for g in (0,14,47):
                addr=(0,0,0,g)
                self.assertEqual(len(set(cube.adjacent(addr,d,g)[:3] for d in range(6))),6)

    def test_spatial_only_and_equal_snapshots(self):
        for signs in ((1,1,1),(1,-1,1)):
            engine=Engine(Coupling(signs))
            state=State(Cube(5),VACUUM,{(2,2,2,0):Channel(0,2,2)})
            initial=state
            for _ in range(8):
                nxt=engine.advance(state)
                self.assertEqual(engine.rewind(nxt),state)
                self.assertEqual(balance_residuals(state,nxt,engine),{})
                self.assertEqual(signed_account(nxt)-signed_account(state),
                                 expected_account_change(state,engine))
                state=nxt
            for _ in range(8):
                state=engine.rewind(state)
            self.assertEqual(state,initial)

    def test_pure_observation(self):
        engine=Engine()
        old=State(Cube(4),VACUUM,{(1,1,1,0):Channel(0,2,2)})
        new=engine.advance(old)
        seen=list(clicks(old,new,1))
        self.assertEqual(engine.advance(old),new)
        self.assertTrue(all(0<=event.kind<=2 for event in seen))
        self.assertIsNone(classify(VACUUM,VACUUM))

    def test_config_data_only(self):
        exp=from_dict({"side":5,"coupling_signs":[1,-1,1],
                       "seed_changes":[{"position":[1,1,1],"channel":0,"state":[0,2,2]}],
                       "steps":4})
        self.assertEqual(exp.steps,4)
        self.assertEqual(len(exp.initial.cells),1)
        checkpoint=checkpoint_data(exp.initial,exp.engine,0)
        self.assertEqual(checkpoint["coupling_fingerprint"],exp.engine.coupling.fingerprint)
        with self.assertRaises(ValueError):
            from_dict({"side":5,"runtime_injection":"forbidden"})

    def test_immutable_state(self):
        state=State(Cube(3),cells={(0,0,0,0):Channel(0,1,2)})
        with self.assertRaises(TypeError):
            state.cells[(0,0,0,0)]=Channel(0,0,2)

if __name__=="__main__":
    unittest.main()
