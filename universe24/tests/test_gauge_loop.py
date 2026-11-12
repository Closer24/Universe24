"""Independent controls for the finite-gauge research constructions.

These tests check the stated domains and counterexamples. They do not grant
Maxwell, quantum, Einstein, or physical-detector acceptance.
"""
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import random
import tempfile
import unittest

import numpy as np

from universe24.core import Engine, State
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle, verify_run
from validation.gauge_loop import model
from validation.gauge_loop import dynamic, obstructions


def scalar_static_step(state):
    """Direct four-port complex arithmetic, independent of tensor expansion."""
    rows, count = state.G, state.N
    a = [[int(state.b[row, node]) for node in range(count)] for row in range(rows)]
    b = [[0] * count for _ in range(rows)]
    r = [[0] * count for _ in range(rows)]
    lat = state.lattice
    for node in range(count):
        xyz = lat.coords(node)
        real_sum = imag_sum = 0
        for axis, link_rows in ((0, (2, 3)), (1, (4, 5))):
            for direction in (-1, 1):
                neighbor_xyz = list(xyz)
                neighbor_xyz[axis] += direction
                neighbor = lat.index(*neighbor_xyz)
                link_node = node if direction == 1 else neighbor
                lr = int(state.b[link_rows[0], link_node])
                li = direction * int(state.b[link_rows[1], link_node])
                pr, pi = int(state.b[0, neighbor]), int(state.b[1, neighbor])
                real_sum += lr * pr - li * pi
                imag_sum += lr * pi + li * pr
        inputs = [3 * real_sum, 3 * imag_sum]
        inputs.extend(6 * int(state.b[row, node]) for row in range(2, 6))
        inputs.append(3 * (int(state.b[0, node]) ** 2 + int(state.b[1, node]) ** 2))
        for row, value in enumerate(inputs):
            quotient, remainder = divmod(2 * value + int(state.r[row, node]), 6)
            b[row][node] = quotient - int(state.a[row, node])
            r[row][node] = remainder
    return State(state.L, a, b, r)


def arbitrary_state(seed=24066, bits=6):
    rng = random.Random(seed)
    bound = 1 << bits
    a = [[rng.randrange(-bound, bound) for _ in range(27)] for _ in range(7)]
    b = [[rng.randrange(-bound, bound) for _ in range(27)] for _ in range(7)]
    r = [[(row * 27 + node) % 6 for node in range(27)] for row in range(7)]
    return State(3, a, b, r)


def mechanical_bundle(tensor, seed, name):
    channels = [dict(index=i, name=gear.name, owner=name,
                     purpose="retained finite-gauge research control", label=gear.label)
                for i, gear in enumerate(tensor.gears)]
    return create_bundle(tensor, seed, channels=channels, protocol=default_protocol(),
                         model={"id": name, "version": "1", "domain": "research control only"})


def scalar_dynamic_step(state):
    """Independent scalar expansion of the three-register edge exchange."""
    a = [[int(state.b[row, n]) for n in range(state.N)] for row in range(10)]
    b, r = [[0] * state.N for _ in range(10)], [[0] * state.N for _ in range(10)]
    for node in range(state.N):
        inputs = [0] * 10
        inputs[0] = 6 * int(state.b[0, node])
        for axis in range(3):
            xyz = list(state.lattice.coords(node))
            xyz[axis] += 1
            neighbor = state.lattice.index(*xyz)
            reference = int(state.b[0, neighbor])
            chi, eta, link = 1 + 3 * axis, 2 + 3 * axis, 3 + 3 * axis
            x, y, u = (int(state.b[row, node]) for row in (chi, eta, link))
            inputs[chi] = 3 * (y + u * reference)
            inputs[eta] = 3 * (x + u * reference)
            inputs[link] = 3 * (x + y) * reference
        for row, value in enumerate(inputs):
            quotient, remainder = divmod(2 * value + int(state.r[row, node]), 6)
            b[row][node] = quotient - int(state.a[row, node])
            r[row][node] = remainder
    return State(state.L, a, b, r)


class GaugeLoopTests(unittest.TestCase):
    def test_tensor_has_complete_ownership_and_true_single_edge_support(self):
        tensor = model.build_tensor()
        self.assertEqual(tensor.G, 7)
        self.assertEqual(len(set(tensor.names)), 7)
        self.assertFalse(tensor.support_violations())
        self.assertTrue(tensor.b_only)
        self.assertLessEqual(tensor.rank - 1, 3)
        self.assertEqual([gear.link for gear in tensor.gears], [None, None, 0, 0, 1, 1, None])

    def test_expanded_tensor_matches_independent_signed_bigint_oracle(self):
        engine = Engine(model.build_tensor())
        for bits in (6, 131):
            with self.subTest(bits=bits):
                state = arbitrary_state(bits=bits)
                for _ in range(3):
                    before = state
                    state = engine.step(before)
                    self.assertTrue(state.same_as(scalar_static_step(before)))
                    self.assertTrue(engine.inverse_step(state).same_as(before))
                    self.assertTrue(np.array_equal(state.r, before.r))

    def test_local_z4_covariance_includes_every_history_and_carry(self):
        tensor = model.build_tensor()
        engine = Engine(tensor)
        state = arbitrary_state(bits=83)
        phases = [(node * node + node // 3) % 4 for node in range(state.N)]
        before_data = state.to_dict()
        transformed = model.gauge_transform(state, phases)
        self.assertEqual(state.to_dict(), before_data)
        self.assertTrue(model.inverse_gauge_transform(transformed, phases).same_as(state))
        self.assertTrue(engine.step(transformed).same_as(
            model.gauge_transform(engine.step(state), phases)))
        for bank in ("a", "b", "r"):
            self.assertTrue(np.array_equal(getattr(state, bank)[model.RECEIVER],
                                           getattr(transformed, bank)[model.RECEIVER]))
        second = [(3 * node + 2) % 4 for node in range(state.N)]
        composed = model.gauge_transform(transformed, second)
        self.assertTrue(composed.same_as(model.gauge_transform(
            state, [(x + y) % 4 for x, y in zip(phases, second)])))

    def test_flux_changes_two_path_signal_but_gauge_does_not(self):
        engine = Engine(model.build_tensor())
        for flux, expected in ((1, 4), (-1, 0)):
            for offset in range(6):
                with self.subTest(flux=flux, carry_offset=offset):
                    state = model.prepare_two_path(flux=flux, carry_offset=offset)
                    phases = [(3 * node + node // 5) % 4 for node in range(state.N)]
                    transformed = model.gauge_transform(state, phases)
                    self.assertEqual(model.plaquette(state), (flux, 0))
                    self.assertEqual(model.plaquette(transformed), (flux, 0))
                    target = state.lattice.index(1, 1, 0)
                    initial = state.copy()
                    for _ in range(2):
                        state = engine.step(state)
                        transformed = engine.step(transformed)
                        model.validate_static_domain(state)
                        model.validate_static_domain(transformed)
                    self.assertEqual(model.intensity(state, target), expected)
                    self.assertEqual(model.intensity(transformed, target), expected)
                    after = engine.step(state)
                    gauge_after = engine.step(transformed)
                    self.assertEqual(model.receiver_quotient(state, after, target), expected)
                    self.assertEqual(model.receiver_quotient(transformed, gauge_after, target), expected)
                    self.assertTrue(engine.rewind(after, 3).same_as(initial))

    def test_reader_reports_intensity_without_normalizing_or_backreacting(self):
        tensor = model.build_tensor()
        engine = Engine(tensor)
        amplitude = (1 << 147) + 3
        state = model.prepare_two_path(amplitude=amplitude)
        changed = state.copy()
        changed.a[model.RECEIVER, :] = 17
        changed.b[model.RECEIVER, :] = -29
        target = state.lattice.index(1, 1, 0)
        for step in range(3):
            before, other_before = state, changed
            state, changed = engine.step(state), engine.step(changed)
            for bank in ("a", "b", "r"):
                self.assertTrue(np.array_equal(getattr(state, bank)[:6], getattr(changed, bank)[:6]))
            if step == 2:
                self.assertEqual(model.receiver_quotient(before, state, target), 4 * amplitude ** 2)
                self.assertEqual(model.receiver_quotient(other_before, changed, target), 4 * amplitude ** 2)
        # A nonzero signal at one location can exceed one: it is not a probability.
        self.assertGreater(model.receiver_quotient(before, state, target), 1)

    def test_static_domain_rejects_moving_nonunit_or_malformed_links(self):
        for alteration in ("moving", "nonunit", "carry", "fraction"):
            state = model.prepare_two_path()
            if alteration == "moving":
                state.a[2, 0] = -1
            elif alteration == "nonunit":
                state.a[2, 0] = state.b[2, 0] = 2
            elif alteration == "carry":
                state.r[0, 0] = 6
            else:
                state.a = state.a.astype(object)
                state.b = state.b.astype(object)
                state.a[2, 0] = state.b[2, 0] = Fraction(3, 2)
            with self.subTest(alteration=alteration):
                with self.assertRaises((TypeError, ValueError)):
                    model.validate_static_domain(state)
        for kwargs in ({"flux": 0}, {"flux": True}, {"L": 3}, {"amplitude": 1.5}):
            with self.assertRaises((TypeError, ValueError)):
                model.prepare_two_path(**kwargs)

    def test_gauge_rejects_incomplete_or_noninteger_phase_fields(self):
        state = model.prepare_two_path()
        for phases in ([0] * (state.N - 1), [4] * state.N, [True] * state.N, [0.0] * state.N):
            with self.assertRaises((TypeError, ValueError)):
                model.gauge_transform(state, phases)

    def test_nonstationary_link_seed_is_not_silently_projected(self):
        engine = Engine(model.build_tensor())
        state = model.prepare_two_path()
        state.a[2, 0] = 0
        before = state.copy()
        after = engine.step(state)
        self.assertEqual(int(after.b[2, 0]), 2)
        self.assertTrue(state.same_as(before))
        self.assertTrue(engine.inverse_step(after).same_as(before))
        with self.assertRaises(ValueError):
            model.validate_static_domain(after)

    def test_uniform_matter_mode_grows_despite_unit_static_links_and_rewind(self):
        engine = Engine(model.build_tensor())
        state = model.prepare_two_path()
        state.a[0, :] = state.b[0, :] = 1
        seed = state.copy()
        values = [int(state.b[0, 0])]
        for _ in range(3):
            state = engine.step(state)
            model.validate_static_domain(state)
            self.assertTrue(all(int(value) == int(state.b[0, 0]) for value in state.b[0]))
            values.append(int(state.b[0, 0]))
        self.assertEqual(values, [1, 3, 11, 41])
        self.assertTrue(engine.rewind(state, 3).same_as(seed))

    def test_saved_run_replays_and_rejects_rehashed_receiver_corruption(self):
        tensor, state = model.build_tensor(), model.prepare_two_path()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gauge-loop"
            report = run_bundle(mechanical_bundle(tensor, state, "static-z4-control"), path, 3)
            self.assertEqual(report, verify_run(path))
            self.assertEqual(report["channels_per_node"], 7)
            self.assertTrue(all(report["acceptance_gates"][key]["status"] == "not_tested" for key in "CDEF"))
            trace = path / "full_trace.jsonl.gz"
            with gzip.open(trace, "rt", encoding="utf-8") as stream:
                records = [json.loads(line) for line in stream]
            records[2]["after"]["b"][model.RECEIVER][state.lattice.index(1, 1, 0)] += 1
            with gzip.open(trace, "wt", encoding="utf-8") as stream:
                for record in records:
                    stream.write(json.dumps(record) + "\n")
            validation_path = path / "validation.json"
            changed_report = json.loads(validation_path.read_text())
            changed_report["files"]["full_trace.jsonl.gz"] = hashlib.sha256(trace.read_bytes()).hexdigest()
            validation_path.write_text(json.dumps(changed_report))
            with self.assertRaisesRegex(ValueError, "trace mismatch"):
                verify_run(path)


class DynamicGaugeLoopTests(unittest.TestCase):
    def test_every_local_sign_assignment_has_the_declared_complete_period(self):
        import itertools
        engine = Engine(dynamic.build_tensor())
        for reference, chi, eta, link in itertools.product((-1, 1), repeat=4):
            values = np.ones((10, 27), dtype=object)
            neighbor = 9  # (1,0,0) in the L=3 cube, independently of shift maps.
            values[0, neighbor] = reference
            values[1, 0], values[2, 0], values[3, 0] = chi, eta, link
            seed = dynamic.prepare_state(values, 3)
            self.assertEqual(tuple(int(seed.a[row, 0]) for row in (1, 2, 3)),
                             (link * reference, chi, eta * reference))
            after = engine.step(seed)
            self.assertEqual(tuple(int(after.b[row, 0]) for row in (1, 2, 3)),
                             (eta, link * reference, chi * reference))
            self.assertTrue(after.same_as(scalar_dynamic_step(seed)))
            self.assertTrue(engine.step(engine.step(after)).same_as(seed))
            self.assertTrue(engine.inverse_step(after).same_as(seed))

    def test_dynamic_arbitrary_bigint_full_state_covariance_and_oracle(self):
        rng = random.Random(6608)
        tensor = dynamic.build_tensor()
        self.assertEqual(tensor.G, 10)
        self.assertFalse(tensor.support_violations())
        self.assertTrue(tensor.b_only)
        engine = Engine(tensor)
        a = [[rng.randrange(-20, 21) for _ in range(27)] for _ in range(10)]
        b = [[rng.randrange(-20, 21) for _ in range(27)] for _ in range(10)]
        r = [[(row + node) % 6 for node in range(27)] for row in range(10)]
        a[2][0], b[3][1] = -(1 << 169), (1 << 153) + 11
        state = State(3, a, b, r)
        signs = [rng.choice((-1, 1)) for _ in range(27)]
        mapped = dynamic.gauge_transform(state, signs)
        self.assertTrue(dynamic.gauge_transform(mapped, signs).same_as(state))
        after = engine.step(state)
        self.assertTrue(after.same_as(scalar_dynamic_step(state)))
        self.assertTrue(engine.step(mapped).same_as(dynamic.gauge_transform(after, signs)))
        self.assertTrue(engine.inverse_step(after).same_as(state))

    def test_current_link_changes_are_gauge_invariant_and_respond_to_matter(self):
        engine = Engine(dynamic.build_tensor())
        values = np.ones((10, 27), dtype=object)
        changed_values = values.copy()
        changed_values[1, 0] = -1
        first, changed = dynamic.prepare_state(values, 3), dynamic.prepare_state(changed_values, 3)
        for bank in ("a", "b", "r"):
            self.assertTrue(np.array_equal(getattr(first, bank)[[3, 6, 9]],
                                           getattr(changed, bank)[[3, 6, 9]]))
        base_next, changed_next = engine.step(first), engine.step(changed)
        self.assertEqual(int(base_next.b[3, 0]), 1)
        self.assertEqual(int(changed_next.b[3, 0]), -1)
        self.assertNotEqual(dynamic.wilson_plaquettes(base_next), dynamic.wilson_plaquettes(changed_next))
        self.assertNotEqual(int(engine.step(base_next).b[2, 0]),
                            int(engine.step(changed_next).b[2, 0]))
        signs = [1 if node % 3 else -1 for node in range(27)]
        self.assertEqual(dynamic.wilson_plaquettes(changed_next),
                         dynamic.wilson_plaquettes(dynamic.gauge_transform(changed_next, signs)))

    def test_preparation_rejects_non_signs_and_illegal_carries(self):
        for wrong in (0, 2, True, Fraction(1), 1.0):
            values = np.ones((10, 27), dtype=object)
            values[0, 0] = wrong
            with self.assertRaises(ValueError):
                dynamic.prepare_state(values, 3)
        for wrong in (-1, 6, True, Fraction(2), 2.0):
            remainders = np.zeros((10, 27), dtype=object)
            remainders[0, 0] = wrong
            with self.assertRaises(ValueError):
                dynamic.prepare_state(np.ones((10, 27), dtype=object), 3, remainders)

    def test_prepared_domain_requires_complete_old_history_and_wilson_requires_units(self):
        state = dynamic.prepare_fixture()
        dynamic.validate_prepared_domain(state)
        forged = state.copy()
        forged.a[1, 0] *= -1
        self.assertTrue(np.array_equal(forged.b, state.b))
        with self.assertRaises(ValueError):
            dynamic.validate_prepared_domain(forged)
        wrong_link = state.copy()
        wrong_link.b[3, 0] = 2
        with self.assertRaises(ValueError):
            dynamic.wilson_plaquettes(wrong_link)
        malformed = state.copy()
        malformed.a = malformed.a.astype(object)
        malformed.a[0, 0] = Fraction(1, 2)
        with self.assertRaises(ValueError):
            dynamic.gauge_transform(malformed, [1] * state.N)

    def test_saved_dynamic_run_stays_a_mechanical_research_control(self):
        tensor, state = dynamic.build_tensor(), dynamic.prepare_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "dynamic"
            report = run_bundle(mechanical_bundle(tensor, state, "finite-z2-exchange"), run, 4)
            self.assertEqual(report, verify_run(run))
            self.assertEqual(report["channels_per_node"], 10)
            self.assertTrue(all(report["acceptance_gates"][key]["status"] == "not_tested" for key in "CDEF"))


class HistoricalGaugeObstructionTests(unittest.TestCase):
    def test_mechanical_reversal_does_not_hide_link_or_charge_failure(self):
        norm = obstructions.unit_link_drift_control()
        charge = obstructions.gauss_carry_control()
        self.assertEqual(norm["physical_link_next"], [-1, 2])
        self.assertEqual(norm["norm_squared"], [1, 1, 5])
        self.assertEqual(charge["bare_charge_after"] - charge["bare_charge_before"], -6)
        self.assertEqual(charge["retained_carry_source"], -6)
        self.assertEqual(charge["local_balance_residual"], 0)
        self.assertTrue(norm["complete_inverse"] and charge["complete_inverse"])
        self.assertEqual((norm["claim_status"], charge["claim_status"]), ("failed", "failed"))

    def test_actual_gauge_related_click_labels_exchange_and_loop_stencil_is_rejected(self):
        click = obstructions.click_class_gauge_control()
        self.assertEqual((click["original_click"]["class"], click["gauge_click"]["class"]), ("C1", "C2"))
        self.assertEqual((click["original_click"]["quotient"], click["gauge_click"]["quotient"]), (1, -1))
        self.assertTrue(click["complete_state_covariance"])
        locality = obstructions.two_path_locality_control()
        self.assertTrue(locality["strict_constructor_rejected"])
        self.assertGreater(len(locality["witness"]["physical_support"]), 2)
        self.assertEqual(locality["claim_status"], "failed")
        groups = obstructions.finite_group_control()
        self.assertEqual(groups["exact_integer_group_sizes"],
                         {"u1_Z4": 4, "su2_Q8": 8, "su3_monomial": 96})


class GaugeAuditCollectionTests(unittest.TestCase):
    def test_saved_collection_keeps_laws_separate_and_refuses_reused_output(self):
        from validation.gauge_loop import audit
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "audit"
            report = audit.run(out)
            self.assertEqual(json.loads((out / "report.json").read_text()), report)
            cases = report["static_loop"]["saved_histories"]
            hashes = {case["tensor_hash"] for case in cases.values()}
            self.assertEqual(hashes, {model.build_tensor().fingerprint})
            self.assertEqual(len({case["bundle_id"] for case in cases.values()}), 4)
            self.assertNotIn(report["dynamic_saved_run"]["tensor_hash"], hashes)
            self.assertEqual(report["dynamic_saved_run"]["tensor_hash"], dynamic.build_tensor().fingerprint)
            self.assertTrue(all(value == "not_established" for value in report["physical_gates"].values()))
            for name in ("validation/gauge_loop/model.py", "validation/gauge_loop/dynamic.py",
                         "validation/gauge_loop/obstructions.py", "universe24/core/engine.py"):
                self.assertIn(name, report["source_hashes"])
            with self.assertRaises(FileExistsError):
                audit.run(out)


if __name__ == "__main__":
    unittest.main()
