"""Exact algebra checks for the optional clock network, not physical certificates."""
import unittest

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import DIRECTIONS, ZERO
from universe24.core.reciprocity import check_reciprocity
from universe24.layers.clock_network import InvariantPort, build_clock_network, one_invariant_ports


class ClockNetworkTests(unittest.TestCase):
    def test_expanded_polynomial_matches_potential_derivatives(self):
        source=Tensor([GearType('x'),GearType('y',sign=-1,sign_why='signed-gradient control'),
                       GearType('u',link=0),GearType('v',link=0)],[],Q=31)
        ports=[InvariantPort('node',('x','y'),(1,2),(2,-1),3,7),
               InvariantPort('edge',('u','v'),(2,1),(4,0),2)]
        net=build_clock_network(source,ports,sectors=('node','edge'),spring=5,
                                spatial_spring=2,strict_support=True)
        t=net.tensor;e=Engine(t,t.Q)
        b=(np.arange(t.G*27).reshape(t.G,27)%11)-5
        s=State(3,np.zeros_like(b),b,np.full_like(b,9))
        expected=np.zeros_like(b,dtype=object)
        master=net.clock_index()
        clock_ids=[net.clock_index(n) for n in ('master','node','edge')]
        for c in clock_ids:
            expected[c]=net.clock_coefficient*b[c]
            for direction in DIRECTIONS:
                expected[c]+=net.spatial_spring*(b[c,s.lattice.shift_index(direction)]-b[c])
        for sector in net.sectors:
            c=net.clock_index(sector)
            expected[c]+=net.spring*(b[master]-b[c])
            expected[master]+=net.spring*(b[c]-b[master])
        for p in net.ports:
            c=net.clock_index(p.sector)
            gs=[t.gear_index(n) for n in p.gears]
            axis=t.gears[gs[0]].link
            for n in range(s.N):
                endpoints=[n] if axis is None else [n,int(s.lattice.shift_index(DIRECTIONS[2*axis])[n])]
                values=[int(b[g,n])+v for g,v in zip(gs,p.shifts)]
                E=sum(w*y*y for w,y in zip(p.weights,values))
                for end in endpoints:
                    expected[c,end]-=p.coupling*int(b[c,end])*(E-p.counterterm)
                c2=sum(int(b[c,end])**2 for end in endpoints)
                for g,w,y in zip(gs,p.weights,values):
                    expected[g,n]-=t.gears[g].sign*p.coupling*w*y*c2
        np.testing.assert_array_equal(e.inputs(s),expected)
        self.assertTrue(check_reciprocity(t).ok)
        self.assertEqual(t.support_violations(),[])
        self.assertEqual(t.rank,4)

    def test_inverse_keeps_old_a_dag_and_large_integer_state(self):
        source=Tensor(['x','y'],[('x',7,(('y',ZERO,'a'),))],Q=11)
        net=build_clock_network(source,[InvariantPort('sector',('x','y'))],
                                sectors=('sector',),spring=1,strict_support=True)
        e=Engine(net.tensor,11)
        s=e.vacuum(3,[17]*net.tensor.G)
        s.a[:]=1;s.b[:]=2
        # Constructor, rather than assignment into int64, keeps the huge value exact.
        b=s.b.astype(object);b[0,0]=1<<80;s=State(3,s.a,b,s.r)
        forward=e.run(s,3)
        self.assertTrue(e.rewind(forward,3).same_as(s))
        self.assertTrue(e.run(e.rewind(s,3),3).same_as(s))
        self.assertGreater(e.stats['pyint_steps'],0)
        self.assertEqual(len(source.stages),2)
        self.assertEqual(len(net.tensor.stages),2)

    def test_full_affine_link_norm_covariance_of_added_force(self):
        from universe24.layers.gauge import ALGEBRAS
        names=('U0','U1','U2','U3')
        source=Tensor([GearType(n,link=0) for n in names],[],Q=31)
        p=InvariantPort('s',names,shifts=(8,0,0,0))
        net=build_clock_network(source,[p],sectors=('s',),spring=2,strict_support=True)
        e=Engine(net.tensor,31);s=e.vacuum(3,[3]*net.tensor.G)
        s.b[:]=(np.arange(net.tensor.G*27).reshape(net.tensor.G,27)%7)-3
        original=e.inputs(s)
        shift=np.array([8,0,0,0])[:,None]
        for q in ALGEBRAS['su2'].group:
            R=np.asarray(ALGEBRAS['su2'].left_matrix(q),dtype=np.int64)
            transformed=s.copy()
            transformed.b[:4]=R@(s.b[:4]+shift)-shift
            response=e.inputs(transformed)
            np.testing.assert_array_equal(response[:4],R@original[:4])
            np.testing.assert_array_equal(response[4:],original[4:])
        # This is a polynomial-force covariance check, not a full-affine Rule3
        # covariance theorem for the deliberately empty source tensor.

    def test_staggered_metric_force_respects_all_cube_rotations(self):
        from universe24.algebra.group_2o import group
        from universe24.layers.one import one_system
        system=one_system();block=system.by_name('metric')
        source=Tensor([GearType('metric.'+g.name,g.label,g.link,g.sign,g.sign_why)
                       for g in block.gears],[],Q=31)
        ports=[p for p in one_invariant_ports(system)
               if all(n.startswith('metric.') for n in p.gears)]
        net=build_clock_network(source,ports,sectors=('core',),spring=2,
                                spatial_spring=1,strict_support=True)
        e=Engine(net.tensor,31);state=e.vacuum(3,[3]*net.tensor.G)
        state.b[:]=(np.arange(net.tensor.G*27).reshape(net.tensor.G,27)%13)-6
        names=net.tensor.names;index={n:i for i,n in enumerate(names)};axes='xyz'
        def transform(values,R):
            out=np.zeros_like(values)
            permutation=[next(j for j in range(3) if R[j][i]) for i in range(3)]
            signs=[R[permutation[i]][i] for i in range(3)]
            for g,name in enumerate(names):
                local=name.split('.')[-1]
                target,sign,rebase=g,1,None
                if name.startswith('metric.') and local.startswith('h0') and local!='h00':
                    i=axes.index(local[-1]);j=permutation[i]
                    target=index['metric.h0'+axes[j]];sign=signs[i]
                    if sign<0:rebase=j
                elif name.startswith('metric.') and local!='h00':
                    i,j=axes.index(local[1]),axes.index(local[2])
                    u,v=sorted((permutation[i],permutation[j]))
                    target=index['metric.h'+axes[u]+axes[v]];sign=signs[i]*signs[j]
                for n in range(state.N):
                    x=state.lattice.coords(n)
                    y=[sum(R[i][j]*x[j] for j in range(3)) for i in range(3)]
                    if rebase is not None:y[rebase]-=1
                    out[target,state.lattice.index(*y)]=sign*values[g,n]
            return out
        original=e.inputs(state)
        rotations=set(group().rotations)
        self.assertEqual(len(rotations),24)
        for R in rotations:
            transformed=state.copy();transformed.b[:]=transform(state.b,R)
            np.testing.assert_array_equal(e.inputs(transformed),transform(original,R))
        # The source is empty: this proves the added polynomial force's finite
        # cube covariance, not a full-system Lorentz or gauge theorem.

    def test_declared_port_validation_and_source_locality_scope(self):
        source=Tensor([GearType('x'),GearType('u',link=0),GearType('v',link=1)],[],Q=7)
        invalid=[InvariantPort('other',('x',)),InvariantPort('s',('x','x')),
                 InvariantPort('s',('x',),weights=(True,)),
                 InvariantPort('s',('x',),shifts=(0,1)),
                 InvariantPort('s',('u','v')),InvariantPort('s',('x','u'))]
        for p in invalid:
            with self.assertRaises(ValueError):
                build_clock_network(source,[p],sectors=('s',),spring=1)
        with self.assertRaises(ValueError):
            build_clock_network(source,[],sectors=('s',),spring=0)
        with self.assertRaises(ValueError):
            build_clock_network(Tensor(['x'],[]),[],sectors=('s',),spring=1)
        with self.assertRaises(ValueError):
            build_clock_network(source,[],sectors=('master',),spring=1)
        # Existing storage-local source uses two different physical link axes.
        wide=Tensor(source.gears,[('u',1,(('v',ZERO,'b'),))],Q=7)
        build_clock_network(wide,[],sectors=('s',),spring=1)
        with self.assertRaises(ValueError):
            build_clock_network(wide,[],sectors=('s',),spring=1,strict_support=True)

    def test_one_catalogue_covers_complete_selected_representations(self):
        from universe24.layers.one import one_system
        from universe24.core.tensor import build
        from universe24.tools.system_inventory import inventory
        system=one_system();source=build(*system.blocks)
        ports=one_invariant_ports(system)
        self.assertEqual([len(p.gears) for p in ports if p.description.startswith('complete 32')],[32])
        names={g for p in ports for g in p.gears}
        self.assertTrue(set(n for n in source.names if n.startswith('metric.'))<=names)
        self.assertFalse(any(n.startswith('em.') for n in names))
        self.assertFalse({'cosmic.Th','cosmic.Lp','cosmic.Lm'}&names)
        net=build_clock_network(source,ports,spring=source.Q//4096)
        self.assertEqual(net.tensor.G,source.G+7)
        self.assertEqual(net.tensor.rank,4)
        self.assertEqual(len(net.tensor.support_violations()),len(source.support_violations()))
        self.assertTrue(check_reciprocity(net.tensor).ok)
        self.assertEqual(len(inventory(net.tensor)['gear_dependency_components']),1)
        self.assertEqual(source.fingerprint,net.source_fingerprint)
        # Full gauge ports carry the builder-declared affine shifts, not just
        # unshifted deviation norms that would break those polynomial symmetries.
        full=one_invariant_ports(system,include_gauge_links=True,include_relays=True)
        link=next(p for p in full if p.description=='full su3.Ux field norm')
        self.assertEqual(sum(v!=0 for v in link.shifts),3)
        self.assertEqual(sum(v*v for v in link.shifts),3*65536**2)
        build_clock_network(source,full,spring=source.Q//4096)


    def test_free_clock_exact_period_six_and_constant_remainders(self):
        # 2u=D*b, so Euclidean division leaves any allowed r unchanged.
        # The integer matrix on (a,b) is [[0,1],[-1,1]], with M**3=-I.
        for Q in (1, 31, 2**80):
            D=6*Q
            tensor=Tensor(['clock'], [('clock',D//2,(('clock',ZERO,'b'),))],Q=Q)
            engine=Engine(tensor,Q)
            a=np.zeros((1,27),dtype=object)
            b=np.full((1,27),2,dtype=object)
            r=np.array([[0,D-1,D//2]*9],dtype=object)
            seed=State(3,a,b,r);state=seed
            for tick in range(1,7):
                previous=state;state=engine.step(state)
                np.testing.assert_array_equal(state.a,previous.b)
                np.testing.assert_array_equal(state.b,previous.b-previous.a)
                np.testing.assert_array_equal(state.r,seed.r)
                self.assertEqual(state.same_as(seed),tick==6)
            self.assertTrue(engine.rewind(state,6).same_as(seed))

    def test_two_clock_exact_exchange_and_period_twelve(self):
        # Q even makes D/4 integral. Equal a/b parity is the exact invariant
        # sublattice: K=(D/2)*(b_master+b_sector) is divisible by D.
        # Sum mode has period 6, difference mode period 4; no rounding is dropped.
        Q=2;D=6*Q
        source=Tensor(['spectator'],[],Q=Q)
        net=build_clock_network(source,[],sectors=('local',),spring=D//4,
                                clock_coefficient=D//2,strict_support=True)
        engine=Engine(net.tensor,Q)
        master,local=net.clock_index(),net.clock_index('local')
        a=np.zeros((3,27),dtype=np.int64);b=a.copy();b[master]=2
        # Every possible phase occurs. Distinct clock phases are allowed.
        r=np.arange(81,dtype=np.int64).reshape(3,27)%D
        seed=State(3,a,b,r);state=seed
        expected=[(2,0),(1,1),(-1,1),(-1,-1),(0,-2),(0,0),
                  (0,2),(1,1),(1,-1),(-1,-1),(-2,0),(0,0),(2,0)]
        official_rows=0
        for tick in range(1,13):
            previous=state;state=engine.step(state)
            self.assertEqual((int(state.b[master,0]),int(state.b[local,0])),expected[tick])
            np.testing.assert_array_equal(state.r,seed.r)
            np.testing.assert_array_equal(state.b[master]+state.b[local],
                                         previous.b[master]+previous.b[local]
                                         -previous.a[master]-previous.a[local])
            np.testing.assert_array_equal(state.b[master]-state.b[local],
                                         -previous.a[master]+previous.a[local])
            self.assertEqual(state.same_as(seed),tick==12)
            clicks=engine.clicks(previous,state,tick,'official')
            official_rows+=len(clicks)
            self.assertTrue(np.all(clicks.changed))
            self.assertTrue(np.all(clicks.kind==0))
        self.assertGreater(official_rows,0)
        self.assertTrue(engine.rewind(state,12).same_as(seed))
        self.assertTrue(check_reciprocity(net.tensor).ok)
        self.assertEqual(net.tensor.support_violations(),[])
        self.assertEqual(net.tensor.rank,2)

    def test_seed_controlled_norm_port_transmits_without_runtime_switch(self):
        # This is a finite prepared response test, not global boundedness.
        # At a=b=0 for both clocks the exact invariant clock state closes the
        # port. A nonzero clock seed opens a state-mediated route x -> c -> y.
        Q=31;D=6*Q
        source=Tensor(['x','y'],[(n,D//2,((n,ZERO,'b'),)) for n in ('x','y')],Q=Q)
        net=build_clock_network(source,[InvariantPort('s',('x','y'))],
                                sectors=('s',),spring=1,strict_support=True)
        engine=Engine(net.tensor,Q);outcomes={}
        for clock_amplitude in (0,4):
            a=np.zeros((4,27),dtype=np.int64);b=a.copy()
            b[0]=2;b[1]=2;b[2:]=clock_amplitude
            seed=State(3,a,b,a.copy()+D//2-1)
            other=seed.copy();other.b[0]=4
            state,control=seed,other
            first_state=first_counter=first_click=None;peak=0
            for tick in range(1,101):
                following,alternative=engine.step(state),engine.step(control)
                same_target=all(np.array_equal(getattr(following,f)[1],getattr(alternative,f)[1])
                                for f in ('a','b','r'))
                if first_state is None and not same_target:first_state=tick
                if first_counter is None and not np.array_equal(following.b[1],alternative.b[1]):
                    first_counter=tick
                rows=[r for r in engine.clicks(state,following,tick).rows() if r[2]==1]
                alt_rows=[r for r in engine.clicks(control,alternative,tick).rows() if r[2]==1]
                if first_click is None and rows!=alt_rows:first_click=tick
                if clock_amplitude==0:
                    np.testing.assert_array_equal(following.a[2:],0)
                    np.testing.assert_array_equal(following.b[2:],0)
                peak=max(peak,following.max_abs(),alternative.max_abs())
                state,control=following,alternative
            self.assertTrue(engine.rewind(state,100).same_as(seed))
            self.assertTrue(engine.rewind(control,100).same_as(other))
            self.assertLessEqual(peak,9)
            outcomes[clock_amplitude]=(first_state,first_counter,first_click)
        self.assertEqual(outcomes[0],(None,None,None))
        self.assertEqual(outcomes[4],(2,18,11))
        self.assertEqual(net.tensor.rank,4)
        self.assertEqual(net.tensor.support_violations(),[])
        self.assertTrue(check_reciprocity(net.tensor).ok)


if __name__=='__main__':
    unittest.main()
