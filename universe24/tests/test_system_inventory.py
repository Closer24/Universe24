"""Structural no-path certificates, distinct from observed interactions."""
import unittest

from universe24.core import Tensor
from universe24.core.lattice import ZERO
from universe24.tools.system_inventory import inventory,default_inventory


class SystemInventoryTests(unittest.TestCase):
    def test_directed_reachability_and_canonical_cancellation(self):
        t=Tensor(['left.a','middle.b','right.c','isolated.d'],[
            ('middle.b',1,(('left.a',ZERO,'a'),)),
            ('right.c',1,(('middle.b',ZERO,'b'),)),
            ('isolated.d',2,(('left.a',ZERO,'b'),)),
            ('isolated.d',-2,(('left.a',ZERO,'b'),)),
        ],Q=1)
        report=inventory(t)
        n={r['name']:r for r in report['namespaces']}
        self.assertEqual(n['left']['can_reach_namespaces'],['middle','right'])
        self.assertEqual(n['right']['can_reach_namespaces'],[])
        self.assertEqual(n['isolated']['reads_from'],[])
        self.assertEqual(report['independent_namespace_groups'],[['isolated'],['left','middle','right']])
        self.assertEqual(report['factor_reads_by_field'],{'a':1,'b':1})

    def test_default_components_are_not_a_fully_connected_physics_model(self):
        report=default_inventory()
        self.assertEqual(report['gear_types'],382)
        self.assertEqual(report['rank'],4)
        self.assertEqual(report['monomials'],18592)
        self.assertEqual(report['independent_namespace_groups'],[
            ['arm1','arm2','exit','gate','router'],
            ['beta','bgk','chiral','em','matter','matter2','metric','ref','wsu2'],
            ['cosmic'],['su2'],['su3'],['u1'],
        ])
        blocks={b['name']:b for b in report['builder_blocks']}
        self.assertEqual(len(blocks),22)
        self.assertEqual(blocks['ehop']['declared_gear_types'],0)
        self.assertGreater(blocks['ehop']['raw_terms'],0)
        self.assertEqual(sum(b['declared_gear_types'] for b in blocks.values()),382)
        self.assertEqual(sum(c['size'] for c in report['gear_dependency_components']),382)
