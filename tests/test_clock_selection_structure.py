"""Regression against confusing event-class pair tables with physical products."""
import json,unittest
from universe24 import Cube,State,Channel,Engine
from research.clock_selection import structure as s
class StructureObservationTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads(s.PROTOCOL.read_text())
        self.case={'id':'test','side':161,'phase':1,'delay':4,'kind':'encounter','control':'11'}
    def test_empty_products_survive_nonempty_class_pair_table(self):
        quiet=State(Cube(161));obs=s.observe(self.case,[quiet]*49,self.p)
        self.assertEqual(obs['isolated_product_templates'],[])
        self.assertEqual(len(obs['C_class_lag_coexistence'][0]['ordered_distinct_event_pairs']),9)
        self.assertEqual(obs['separated_product_pairs'],[])
        self.assertFalse(obs['separated_products_without_parent'])
    def test_two_complete_isolated_products_are_not_class_pair_rows(self):
        centers=((80,81,78),(80,81,82));cells={}
        for center in centers:
            for address,value in s.template('single',0):
                cells[(*s.add(center,address[:3]),address[3])]=Channel(*value)
        state=State(Cube(161),cells=cells);engine=Engine(s.CP);states=[state]
        for _ in range(48):states.append(engine.advance(states[-1]))
        obs=s.observe(self.case,states,self.p)
        self.assertEqual({tuple(v['origin']) for v in obs['isolated_product_templates']},set(centers))
        self.assertEqual(len(obs['separated_product_pairs']),1)
        self.assertTrue(obs['separated_products_without_parent'])
    def test_complete_pair_formula_and_native_capture_budget_units(self):
        case={**self.case,'control':'01','side':193};ready=s.spec(case,self.p)
        self.assertEqual(ready['budget']['max_cells'],20000*49)
        from research.experiments.run import assemble
        assembled=assemble(ready);state=assembled.initial;origin=(96,97,96)
        for t in range(11):
            self.assertTrue(s.matches(state,origin,'pair',(1+t)%5))
            state=assembled.engine.advance(state)
if __name__=='__main__':unittest.main()
