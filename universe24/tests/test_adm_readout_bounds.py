"""Independent checks that passive physical summaries cannot overclaim growth."""
import copy
from fractions import Fraction
from math import nextafter
import unittest

from experiments.cosmology.audit_adm_readouts import audit


def report(ranges):
    return {'parameters':{'L':3,'dark_matter':True,'scale':4096,
            'fields':['rho_dark','phi','beta0','beta1','beta2']},
            'complete_rewind_exact':True,
            'samples':[{'step':i,'field_ranges':dict(
                rho_dark=density,phi=phi,beta0=[0.,0.],beta1=[0.,0.],beta2=[0.,0.])}
                for i,(density,phi) in enumerate(ranges)]}


class ADMReadoutBoundsTests(unittest.TestCase):
    def test_saved_rounded_extrema_bound_every_exact_face_ball(self):
        density=[Fraction(1,7)+Fraction(i*i,10001) for i in range(27)]
        data=report([([float(min(density)),float(max(density))],[1.,2.])])
        saved=copy.deepcopy(data)
        result=audit(data)
        upper=Fraction(result['samples'][0]['dust_ball_fraction_upper_bound'])
        total=sum(density)
        index=lambda x,y,z:(x%3)*9+(y%3)*3+z%3
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    points={(x,y,z),(x+1,y,z),(x-1,y,z),(x,y+1,z),
                            (x,y-1,z),(x,y,z+1),(x,y,z-1)}
                    exact=sum(density[index(*p)] for p in points)/total
                    self.assertGreaterEqual(upper,exact)
        self.assertEqual(data,saved)

    def test_uncertain_sign_and_later_zero_are_not_uniform_patterns(self):
        data=report([([1.,2.],[1.,2.]),([1.,2.],[-1.,1.]),([1.,2.],[0.,0.])])
        result=audit(data)
        self.assertEqual(result['samples'][0]['site_sign_pattern_types'],1)
        self.assertIsNone(result['samples'][1]['site_sign_pattern_types'])
        # A later zero range might hide underflow; only frozen beta and exactly
        # represented initial integers justify zero without a retained field.
        self.assertIsNone(result['samples'][2]['site_sign_pattern_types'])

    def test_density_underflow_and_incomplete_history_fail_clearly(self):
        tiny=nextafter(0.,1.)
        with self.assertRaisesRegex(ValueError,'lower bound'):
            audit(report([([tiny,tiny],[1.,1.])]))
        data=report([([1.,1.],[1.,1.])]);data['samples'][0]['step']=1
        with self.assertRaisesRegex(ValueError,'starting at zero'):
            audit(data)
