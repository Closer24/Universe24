"""Exact tensor components, independently differentiated and contracted."""
from fractions import Fraction as Q
import unittest
from experiments.geometry.tensor_board import point,bivector,PAIRS


class TestTensorBoard(unittest.TestCase):
    def test_all_256_riemann_entries_against_metric_derivatives(self):
        import sympy as s
        u,v,x,y=s.symbols('u v x y');coords=(u,v,x,y)
        A,B,C=[s.Function(name)(u) for name in ('A','B','C')]
        H=(A+C)*x*x+2*B*x*y+(-A+C)*y*y
        g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]]);inv=g.inv()
        gamma=[[[s.simplify(sum(inv[a,k]*(s.diff(g[k,c],coords[b])+
            s.diff(g[k,b],coords[c])-s.diff(g[b,c],coords[k])) for k in range(4))/2)
            for c in range(4)] for b in range(4)] for a in range(4)]
        R=[[[[s.simplify(s.diff(gamma[a][d][b],coords[c])-s.diff(gamma[a][c][b],coords[d])+
            sum(gamma[a][c][k]*gamma[k][d][b]-gamma[a][d][k]*gamma[k][c][b] for k in range(4)))
            for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
        # Compare symbolically, not just at one amplitude or one spatial point.
        expected={}
        K=((-A-C,-B),(-B,A-C))
        for i in range(2):
            for j in range(2):
                for a,b,sign1 in ((0,i+2,1),(i+2,0,-1)):
                    for c,d,sign2 in ((0,j+2,1),(j+2,0,-1)):
                        expected[a,b,c,d]=sign1*sign2*K[i][j]
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        lower=s.simplify(sum(g[a,k]*R[k][b][c][d] for k in range(4)))
                        self.assertEqual(s.simplify(lower-expected.get((a,b,c,d),0)),0)
        sample=point(A=Q(1,7),B=Q(-2,9),E1=Q(1,3),E2=Q(1,5),x=Q(2,3),y=-1)
        substitutions={A:s.Rational(1,7),B:s.Rational(-2,9),C:-s.Rational(1,2)*(s.Rational(1,9)+s.Rational(1,25))}
        for key,value in expected.items():self.assertEqual(s.Rational(sample['riemann'][key]),value.subs(substitutions))

    def test_inverse_and_einstein_source_are_independent(self):
        p=point(A=Q(1,20),B=Q(1,30),E1=Q(1,8),E2=Q(1,9),x=2,y=-1)
        for i in range(4):
            for j in range(4):
                self.assertEqual(sum(p['metric'][i][k]*p['inverse'][k][j] for k in range(4)),int(i==j))
                self.assertEqual(p['residual'][i][j],0)
        self.assertEqual(p['stress'][0][0],Q(1,64)+Q(1,81))
        bad=point(E1=Q(1,8),trace_override=0)
        self.assertEqual(bad['residual'][0][0],-Q(1,64))

    def test_vacuum_and_radiation_have_different_weyl_parts(self):
        vacuum=point(A=Q(1,20),B=Q(1,30))
        self.assertTrue(any(v for v in vacuum['weyl'].values()))
        self.assertFalse(any(v for row in vacuum['ricci'] for v in row))
        radiation=point(E1=Q(1,8))
        self.assertFalse(any(v for v in radiation['weyl'].values()))
        self.assertTrue(any(v for v in radiation['riemann'].values()))
        self.assertEqual(radiation['scalar'],0)

    def test_bivectors_represent_every_component(self):
        tensor=point(A=Q(1,7),B=Q(1,9),E1=Q(1,8))['riemann'];matrix=bivector(tensor)
        def pair(i,j):
            return (PAIRS.index((min(i,j),max(i,j))),1 if i<j else -1)
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        value=0
                        if a!=b and c!=d:
                            i,si=pair(a,b);j,sj=pair(c,d);value=si*sj*matrix[i][j]
                        self.assertEqual(value,tensor.get((a,b,c,d),0))


if __name__=='__main__':unittest.main()
