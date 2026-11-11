"""Equation coverage, independent continuum limits, and exact Rule3 compilation."""
from fractions import Fraction
import gzip
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
import sympy as sp
from universe24.core import Engine
from experiments.geometry.integer_circuit import Circuit
from experiments.geometry.adm_equations import compile_adm, FIELDS, ArrayField, system, flat_data
from experiments.geometry.adm_initial_data import homogeneous_scalar, numeric_fields, inhomogeneous_scalar
from experiments.geometry.adm_integer import run, replay_trace
from experiments.geometry.full_gr_audit import einstein_from_jet, symbolic_jet


def execute(program, data):
    L=next(iter(data.values())).shape[0]
    seed=program.prepare(L,data)
    engine=Engine(program.tensor)
    final=engine.run(seed,program.ticks)
    expected=program.evaluate_integer_dag(seed)
    for wire,value in expected.items():
        np.testing.assert_array_equal(final.b[program.tensor.gear_index(program.names[wire])],
                                      np.broadcast_to(value,(L**3,)))
    if not engine.rewind(final,program.ticks).same_as(seed):
        raise AssertionError('complete retained state did not rewind')
    return final


class TestIntegerCompiler(unittest.TestCase):
    def test_exact_rational_multiaxis_routing_and_reverse(self):
        c=Circuit();x=c.input('x',8);y=c.input('y',8)
        expression=(x.shift((1,0,0))*y.shift((0,1,0))+x*y)/(1+y)
        program=c.compile({'answer':expression})
        data={'x':np.arange(27).reshape(3,3,3)+1,'y':np.arange(27).reshape(3,3,3)+2}
        state=execute(program,data)
        expected=(Fraction(10,8)*Fraction(5,8)+Fraction(1,8)*Fraction(2,8))/(1+Fraction(2,8))
        self.assertEqual(program.read(state,'answer'),expected)
        self.assertEqual(program.tensor.rank,4)
        self.assertFalse(program.tensor.support_violations())
        self.assertTrue(all(f.field=='b' for m in program.tensor.monomials for f in m.factors))

    def test_symbolic_cancellation_and_large_integers(self):
        c=Circuit();x=c.input('x');y=c.input('y')
        program=c.compile({'answer':((x*y+x)/(y+1))**2})
        data={'x':np.full((3,3,3),1<<100,dtype=object),'y':np.full((3,3,3),5)}
        state=execute(program,data)
        self.assertEqual(program.read(state,'answer'),1<<200)

    def test_clock_and_workspace_are_retained_not_runtime_injections(self):
        c=Circuit();x=c.input('x');program=c.compile({'result':(x*x+3)**2})
        seed=program.prepare(3,{'x':np.full((3,3,3),2)})
        engine=Engine(program.tensor)
        state=seed
        for _ in range(program.ticks):
            state=engine.step(state)
            np.testing.assert_array_equal(state.r,seed.r)
        self.assertEqual(program.read(state,'result'),49)
        self.assertGreater(program.period,program.ticks)


class TestFullADM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program,cls.parameters=compile_adm(scale=4096,dt=Fraction(1,64),dx=Fraction(1,3))
        cls.data=homogeneous_scalar(3)
        cls.final=execute(cls.program,cls.data)

    def test_all_six_evolution_and_four_constraints_present(self):
        self.assertEqual(len(FIELDS),18)
        for step in (0,1):
            for name in ('H','M0','M1','M2'):
                self.assertIn(f'{step}.constraint.{name}',self.program.outputs)
            for i in range(4):
                for j in range(i,4):
                    self.assertIn(f'{step}.metric.{i}{j}',self.program.outputs)
                    self.assertIn(f'{step}.stress.{i}{j}',self.program.outputs)
        for name in FIELDS:
            value=(self.program.read(self.final,f'1.{name}')-self.program.read(self.final,f'0.{name}')
                   -Fraction(1,64)*self.program.read(self.final,f'0.update_rhs.{name}'))
            self.assertEqual(value,0)

    def test_constraint_compatible_scalar_and_time_error(self):
        for name in ('H','M0','M1','M2'):
            self.assertEqual(self.program.read(self.final,f'0.constraint.{name}'),0)
        self.assertLess(abs(float(self.program.read(self.final,'1.constraint.H'))),1e-5)
        self.assertNotEqual(self.program.read(self.final,'1.phi'),self.program.read(self.final,'0.phi'))
        self.assertNotEqual(self.program.read(self.final,'1.g00'),1)

    def test_matter_sources_geometry_with_correct_coefficient(self):
        control={name:value.copy() for name,value in self.data.items()}
        control['phi'][:]=0
        state=execute(self.program,control)
        # Control deliberately violates the old initial constraint; isolates the source term.
        expected=-Fraction(1,64)*Fraction(1,128)
        for name in ('K00','K11','K22'):
            self.assertEqual(self.program.read(self.final,'1.'+name)-self.program.read(state,'1.'+name),expected)
        self.assertNotEqual(self.program.read(state,'0.constraint.H'),0)

    def test_geometry_feeds_back_on_scalar(self):
        changed={name:value.copy() for name,value in self.data.items()}
        changed['K00']+=4096//32
        state=execute(self.program,changed)
        expected=Fraction(1,64)*Fraction(1,32)*Fraction(3,32)
        self.assertEqual(self.program.read(state,'1.Pi')-self.program.read(self.final,'1.Pi'),expected)

    def test_spatially_general_equations_compile_exactly(self):
        p,_=compile_adm(scale=64,dt=Fraction(1,128),dx=Fraction(1,3))
        data=flat_data(3,64);rng=np.random.default_rng(821)
        for name in FIELDS:
            data[name]+=rng.integers(-1,2,size=(3,3,3))
        # Positive definite metric and lapse; arbitrary data are NOT a constrained GR solution.
        final=execute(p,data)
        self.assertNotEqual(p.read(final,'0.constraint.H'),0)
        self.assertNotEqual(p.read(final,'0.metric.01'),0)
        self.assertTrue(any(p.read(final,f'1.{name}',0)!=p.read(final,f'1.{name}',1) for name in FIELDS))

    def test_flat_vacuum_and_lossless_complete_trace(self):
        with tempfile.TemporaryDirectory() as temp:
            result=run(self.program,flat_data(3),self.parameters,Path(temp))
            states=iter(replay_trace(Path(temp)/'full_trace.jsonl.gz'))
            before=next(states);count=1
            engine=Engine(self.program.tensor)
            for after in states:
                self.assertTrue(engine.step(before).same_as(after))
                before=after;count+=1
            self.assertEqual(count,self.program.ticks+1)
            self.assertTrue(result['complete_rewind_exact'])
            self.assertTrue(all(value==0 for sample in result['samples'] for value in sample['constraint_max'].values()))


class TestIndependentPhysics(unittest.TestCase):
    def test_massless_anisotropic_solution_with_full_4D_einstein_tensor(self):
        t,x,y,z=sp.symbols('t x y z',real=True)
        H=[sp.Rational(1,16),sp.Rational(1,16),sp.Rational(1,32)];theta=sum(H)
        metric=sp.diag(-sp.exp(2*theta*t),*[sp.exp(2*h*t) for h in H])
        result=einstein_from_jet(*symbolic_jet(metric,(t,x,y,z),{t:0,x:0,y:0,z:0}))
        # phi=t/8; at t=0, canonical real-scalar stress is diag(1,1,1,1)/128.
        self.assertEqual(result['G'],sp.eye(4)/128)
        rhs,constraints,_=system(numeric_fields(homogeneous_scalar(3,mass_squared=0),4096),mass_squared=0)
        self.assertAlmostEqual(float(rhs['alpha'].data[0,0,0]),float(theta))
        for i,h in enumerate(H):
            self.assertAlmostEqual(float(rhs[f'g{i}{i}'].data[0,0,0]),float(2*h))
            self.assertAlmostEqual(float(rhs[f'K{i}{i}'].data[0,0,0]),float(h*(theta-2*h)))
        self.assertTrue(all(np.max(np.abs(v.data))<1e-15 for v in constraints.values()))

    def test_spatial_discretization_converges_on_nonlinear_metric(self):
        errors=[]
        for L in (9,17,33):
            x=np.indices((L,L,L))[0]/L;u=.01*np.cos(2*np.pi*x)
            up=-.01*2*np.pi*np.sin(2*np.pi*x);upp=-.01*(2*np.pi)**2*np.cos(2*np.pi*x)
            data={name:np.zeros((L,L,L)) for name in FIELDS}
            for name in ('g00','g11','g22'):data[name]=np.exp(4*u)
            data['alpha'][:]=1
            _,_,diagnostic=system({name:ArrayField(v) for name,v in data.items()},Fraction(1,L),0)
            # For gamma=e^(4u) delta: Rxx=-4u'', Ryy=Rzz=-2u''-4u'^2.
            expected=[-4*upp,-2*upp-4*up*up,-2*upp-4*up*up]
            errors.append(max(float(np.max(np.abs(diagnostic['Ricci3'][i][i].data-expected[i]))) for i in range(3)))
        self.assertLess(errors[1],errors[0]/3)
        self.assertLess(errors[2],errors[1]/3)

    def test_inhomogeneous_initial_constraints_are_solved(self):
        data,scale,info=inhomogeneous_scalar()
        _,constraints,_=system(numeric_fields(data,scale),Fraction(1,3),1)
        self.assertLess(info['unquantized_H_max'],1e-10)
        self.assertLess(np.max(np.abs(constraints['H'].data)),1e-6)
        self.assertLess(max(np.max(np.abs(constraints[f'M{i}'].data)) for i in range(3)),1e-12)
        self.assertGreater(np.ptp(data['phi']),0)
        self.assertTrue(np.all(data['g01']!=0))

    def test_cosmological_constant_sign(self):
        data=flat_data(3,4096)
        for name in ('K00','K11','K22'):data[name][:]=-4096//16
        rhs,constraints,_=system(numeric_fields(data,4096),mass_squared=0,cosmological=Fraction(3,256))
        self.assertLess(np.max(np.abs(constraints['H'].data)),1e-15)
        self.assertAlmostEqual(rhs['K00'].data[0,0,0],-2/256)


class TestDarkMatter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program,cls.parameters=compile_adm(dark_matter=True,dt=Fraction(1,64))
        cls.data=flat_data(3)
        for name in ('K00','K11','K22'):cls.data[name][:]=-4096//16
        cls.data['rho_dark']=np.full((3,3,3),3*4096//256)
        cls.final=execute(cls.program,cls.data)

    def test_dark_density_sources_metric_and_evolves(self):
        p,f=self.program,self.final
        self.assertEqual(p.read(f,'0.constraint.H'),0)
        self.assertEqual(p.read(f,'0.stress.00'),Fraction(3,256))
        self.assertEqual(p.read(f,'0.stress.11'),0)
        self.assertEqual(p.read(f,'0.rhs.K00'),-Fraction(1,512))
        self.assertEqual(p.read(f,'1.rho_dark'),Fraction(3,256)*(1-Fraction(3,1024)))
        self.assertEqual(p.read(f,'1.alpha'),1)

    def test_geodesic_dust_rejects_incompatible_lapse(self):
        with self.assertRaises(ValueError):compile_adm(dark_matter=True,lapse='harmonic')
        data={name:value.copy() for name,value in self.data.items()};data['alpha'][0,0,0]+=1
        with self.assertRaisesRegex(ValueError,'uniform'):
            run(self.program,data,self.parameters)

    def test_independent_full_einstein_dust_solution(self):
        t,x,y,z=sp.symbols('t x y z',real=True)
        scale=(1+sp.Rational(3,32)*t)**sp.Rational(2,3)
        metric=sp.diag(-1,scale**2,scale**2,scale**2)
        result=einstein_from_jet(*symbolic_jet(metric,(t,x,y,z),{t:0,x:0,y:0,z:0}))
        self.assertEqual(result['G'],sp.diag(sp.Rational(3,256),0,0,0))


if __name__=='__main__':unittest.main()
