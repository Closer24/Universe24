"""Structural no-path certificates, distinct from observed interactions."""
import unittest

from universe24.core import Tensor
from universe24.core.lattice import ZERO
from universe24.tools.system_inventory import inventory,reference_inventory


class SystemInventoryTests(unittest.TestCase):
    def test_directed_reachability_and_canonical_cancellation(self):
        t=Tensor(['left.a','middle.b','right.c','isolated.d'],[
            ('middle.b',1,(('left.a',ZERO,'a'),)),
            ('right.c',1,(('middle.b',ZERO,'b'),)),
            ('isolated.d',2,(('left.a',ZERO,'b'),)),
            ('isolated.d',-2,(('left.a',ZERO,'b'),)),
        ])
        report=inventory(t)
        n={r['name']:r for r in report['namespaces']}
        self.assertEqual(n['left']['can_reach_namespaces'],['middle','right'])
        self.assertEqual(n['right']['can_reach_namespaces'],[])
        self.assertEqual(n['isolated']['reads_from'],[])
        self.assertEqual(report['independent_namespace_groups'],[['isolated'],['left','middle','right']])
        self.assertEqual(report['factor_reads_by_field'],{'a':1,'b':1})

    def test_reference_has_explicit_structural_census(self):
        report=reference_inventory()
        self.assertEqual(report['D'],6)
        self.assertEqual(report['gear_types'],48)
        self.assertEqual(report['rank'],2)
        self.assertEqual(report['monomials'],288)
        self.assertEqual(report['independent_namespace_groups'],[['ref']])
        self.assertEqual(report['strict_physical_support_violations'],0)
        self.assertEqual(report['designations'],0)
        blocks=report['builder_blocks']
        self.assertEqual(len(blocks),1)
        self.assertEqual(blocks[0]['name'],'ref')
        self.assertEqual(blocks[0]['declared_gear_types'],48)
        self.assertEqual(blocks[0]['raw_terms'],288)
        self.assertEqual([row['size'] for row in report['gear_dependency_components']],[48])
