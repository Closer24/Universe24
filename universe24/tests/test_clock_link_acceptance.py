"""Independent mechanical and negative-control checks for clock-link records."""
import unittest

import numpy as np

from universe24.core.engine import Engine, State
from universe24.core.tensor import Tensor
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol, decode_transition, make_transition
from validation.clock_links.model import append_phase_observers
from validation.clock_links.acceptance_audit import (
    base_independence, causal_audit, compare_trajectory, passive_audit,
    scalar_step, structural_certificate, synthetic_seed,
)


def frozen44(real=1, imaginary=1):
    """Explicit test fixture, not a geometry or physical carrier model."""
    names = ["field.phi", "field.chi"] + [f"test_unused_{i}" for i in range(42)]
    tensor = Tensor(names, [(name, 6, [(name, (0, 0, 0), "b")]) for name in names], strict_support=True)
    values = np.zeros((44, 27), dtype=object)
    values[0], values[1] = real, imaginary
    seed = State(3, values, values.copy(), np.zeros_like(values))
    channels = [dict(index=i, name=name, label="official", owner="frozen-test-source",
                     purpose="test-only algebraic carrier; no physics") for i, name in enumerate(names)]
    return create_bundle(tensor, seed, channels=channels, protocol=default_protocol(),
                         model={"id": "frozen44-test", "version": "1", "domain": "test fixture only"})


class ClockLinkAcceptanceTests(unittest.TestCase):
    def test_complete48_independent_scalar_signed_bigints_all_carries(self):
        bundle = append_phase_observers(frozen44())
        self.assertEqual(bundle.tensor.G, 48)
        for carry in range(6):
            result = compare_trajectory(bundle.tensor,
                                        synthetic_seed(48, carry=carry, huge=carry == 5), 3)
            self.assertEqual(result["independent_scalar_oracle"], "passed")
            self.assertEqual(result["complete_rewind"], "passed")
        self.assertGreater(result["maximum_integer_bits_by_step"][0], 100)

    def test_structural_and_complete_cone_certificates(self):
        bundle = append_phase_observers(frozen44())
        certificate = structural_certificate(bundle.tensor)
        self.assertEqual(certificate["retained_integers_per_node"], 144)
        self.assertEqual(certificate["strict_physical_support"], "passed")
        cones = causal_audit(bundle.tensor)
        self.assertEqual(cones["perturbations"], 21)
        self.assertGreater(cones["retained_integer_outside_cone_checks"], 0)

    def test_observer_is_passive_and_source_cannot_read_history(self):
        bundle = append_phase_observers(frozen44())
        self.assertEqual(passive_audit(bundle.tensor, bundle.seed)["state_and_tensor_passivity"], "passed")
        independent = base_independence(bundle)
        self.assertTrue(independent["arbitrary_apparatus_history_cannot_change_source"])
        self.assertIn("blocked", independent["complexity_selection"])

    def test_positive_intensity_can_have_no_canonical_record(self):
        # I0=2 and I_axis=8. a=b=I/2 is a stationary retained apparatus.
        apparatus = np.array([[1] * 27, *([[4] * 27] * 3)], dtype=object)
        bundle = append_phase_observers(frozen44(), apparatus_a=apparatus, apparatus_b=apparatus)
        state = bundle.seed
        after = scalar_step(bundle.tensor, state)
        self.assertTrue(after.same_as(state))
        events = decode_transition(make_transition(bundle.tensor, state, after, run_id="stationary", step=1), bundle.tensor)
        self.assertEqual(events, [])
        self.assertEqual(int(after.b[44, 0]) + int(state.a[44, 0]), 2)

    def test_zero_drive_keeps_hidden_motion_without_clicks(self):
        apparatus = np.ones((4, 27), dtype=object)
        bundle = append_phase_observers(frozen44(real=0, imaginary=0), apparatus_a=apparatus)
        before = bundle.seed
        after = Engine(bundle.tensor).step(before)
        self.assertFalse(after.same_as(before))
        events = decode_transition(make_transition(bundle.tensor, before, after, run_id="zero-drive", step=1), bundle.tensor)
        self.assertEqual(events, [])
        self.assertTrue(Engine(bundle.tensor).inverse_step(after).same_as(before))


if __name__ == "__main__":
    unittest.main()
