"""Exact observer checks against independently evaluated pinned proposal data."""
import copy
from fractions import Fraction as F
from pathlib import Path
from types import SimpleNamespace
import unittest

from universe24.core import exact_json
from universe24.core.engine import State
from universe24.core.lattice import lattice
from validation.team48_observables import (
    FRAME_HASH, FRAME_SOURCE, SOURCE_COMMIT, SOURCE_HASHES, TENSOR_HASH,
    decode_fields, expand_fields, matter_observables, node_observables, rational,
    validate_provenance,
)


FIXTURE = Path(__file__).with_name("fixtures")/"team48_observables_oracle.json"


class Team48ObserverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.oracle = exact_json.loads(FIXTURE.read_text())

    def vacuum(self):
        fields = {name: [0]*27 for name in self.oracle["fields"]}
        for a in range(3):
            fields[f"diag_p{a}"] = [1]*27
        return fields

    def test_pinned_independent_oracle_metric_stress_charge_and_constraints(self):
        oracle = self.oracle
        self.assertEqual(oracle["source_commit"], SOURCE_COMMIT)
        for name, fingerprint in oracle["source_sha256"].items():
            self.assertEqual(fingerprint, FRAME_HASH if name == FRAME_SOURCE else SOURCE_HASHES[name])
        expanded = expand_fields(oracle["fields"])
        for expected in oracle["expected"]:
            actual = node_observables(expanded, L=3, node=expected["node"])
            for key in ("B", "gamma", "gamma_inv"):
                self.assertEqual(actual["geometry"][key], expected[key])
            mapping = {"rho_total": "rho", "momentum_frame": "momentum", "stress_frame": "stress",
                       "rho_maxwell": "rho_maxwell", "rho_dust": "dust_density", "potential": "potential",
                       "electric_charge": "electric_charge", "electric_current_frame": "electric_current"}
            for actual_key, expected_key in mapping.items():
                self.assertEqual(actual["matter"][actual_key], expected["diagnostic"][expected_key])
            self.assertEqual(actual["connection_ricci_frame"], expected["diagnostic"]["ricci"])
            for key, value in actual["constraints"].items():
                self.assertEqual(value, expected["constraints"][key], key)

    def test_flat_vacuum_and_zero_source(self):
        actual = node_observables(expand_fields(self.vacuum()), L=3, node=0)
        self.assertEqual(actual["matter"]["rho_total"], rational(0))
        self.assertEqual(actual["matter"]["electric_charge"], rational(0))
        self.assertEqual(actual["geometry"]["gamma"], rational([[int(i == j) for j in range(3)] for i in range(3)]))
        self.assertEqual(actual["geometry"]["face_link_squared_lengths"], rational([1, 1, 1]))
        self.assertEqual(actual["geometry"]["metric_status"], "positive_definite")
        self.assertTrue(all(value == rational(0) for value in actual["constraints"].values()))

    def test_conjugate_charge_sectors_preserve_energy_momentum_and_stress(self):
        f = {name: values[1] for name, values in self.oracle["fields"].items()}
        opposite = dict(f)
        for name in opposite:
            if name in ("chi", "Pi_chi") or name.startswith(("Xi_chi", "A", "E", "M")):
                opposite[name] = -opposite[name]
        positive, negative = (matter_observables(fields) for fields in (f, opposite))
        self.assertNotEqual(positive["electric_charge"], 0)
        self.assertEqual(negative["electric_charge"], -positive["electric_charge"])
        self.assertEqual(negative["electric_current_frame"], [-v for v in positive["electric_current_frame"]])
        for key in ("rho_total", "momentum_frame", "stress_frame"):
            self.assertEqual(positive[key], negative[key])

    def test_dust_positivity_is_signed_square_without_clipping(self):
        f = {name: values[0] for name, values in self.vacuum().items()}
        for sign in (-1, 1):
            f["dust_amplitude"] = sign*3
            result = matter_observables(f)
            self.assertEqual(result["rho_dust"], 9)
            self.assertEqual(result["rho_total"], 9)
            self.assertEqual(result["momentum_frame"], [0, 0, 0])
            self.assertEqual(result["stress_frame"], [[0]*3 for _ in range(3)])

    def test_literal_composite_difference_not_continuum_product_rule(self):
        fields = self.vacuum()
        lat = lattice(3)
        fields["diag_p1"][0] = 3
        fields["diag_p1"][lat.neighbour(0, 0)] = 2
        fields["diag_p1"][lat.neighbour(0, 1)] = 1
        result = node_observables(expand_fields(fields), L=3, node=0)
        self.assertEqual(result["constraints"]["C011"], rational(F(3, 2)))
        self.assertNotEqual(result["constraints"]["C011"], rational(3))

    def test_no_diagonal_neighbor_reads_or_mutation(self):
        fields = copy.deepcopy(self.oracle["fields"])
        saved = copy.deepcopy(fields)
        first = node_observables(expand_fields(fields), L=3, node=0)
        self.assertEqual(fields, saved)
        for values in fields.values():
            values[lattice(3).index(1, 1, 1)] += 100
        self.assertEqual(node_observables(expand_fields(fields), L=3, node=0), first)

    def test_degenerate_geometry_is_reported_not_repaired(self):
        fields = self.vacuum()
        fields["diag_p1"] = [0]*27
        actual = node_observables(expand_fields(fields), L=3, node=0)
        self.assertEqual(actual["geometry"]["metric_status"], "degenerate")
        self.assertIsNone(actual["geometry"]["gamma"])
        self.assertIsNone(actual["geometry"]["det_gamma"])

    def test_large_integer_sources_and_no_float_or_bool_coercion(self):
        f = {name: values[0] for name, values in self.vacuum().items()}
        big = 2**20000+9
        f["phi"] = big
        result = matter_observables(f, mass_squared=F(2, 3))
        self.assertEqual(result["rho_scalar"], F(big*big, 3))
        self.assertEqual(exact_json.loads(exact_json.dumps(rational(result)))["rho_scalar"], rational(F(big*big, 3)))
        for bad in (0.0, True):
            f["phi"] = bad
            with self.assertRaises(TypeError):
                matter_observables(f)
        for bad in (0.1, True):
            with self.assertRaises(TypeError):
                node_observables(expand_fields(self.vacuum()), L=3, node=0, cosmological=bad)
        self.assertEqual(node_observables(expand_fields(self.vacuum()), L=3, node=0,
                                         cosmological=F(1, 2))["constraints"]["H"], rational(-1))

    def phase_fixture(self):
        names = ["phase.staggered"]+["field."+name for name in self.oracle["fields"]]
        offsets = {name: int(name.startswith(("G", "Xi_", "M")) or name in ("B01", "B02", "B12"))
                   for name in self.oracle["fields"]}
        manifest = {"channels_by_index": names, "phase_index": 0, "model": "charged_positive", "phase_offsets": offsets}
        state = State(3, [[-1]*27]+[[0]*27 for _ in range(43)],
                      [[1]*27]+[[i]*27 for i in range(1, 44)], [[0]*27 for _ in range(44)])
        return names, manifest, state

    def test_phase_is_read_from_retained_state_and_static_offsets(self):
        names, manifest, state = self.phase_fixture()
        decoded, phase = decode_fields(state, names, manifest)
        self.assertEqual(phase, [-1, 1])
        for i, name in enumerate(names[1:], 1):
            field = name.removeprefix("field.")
            self.assertEqual(decoded[field], [(1 if manifest["phase_offsets"][field] else -1)*i]*27)
        state.a[0, 1] = 1
        with self.assertRaises(ValueError):
            decode_fields(state, names, manifest)

    def test_altered_phase_metadata_and_mutated_float_state_rejected(self):
        names, manifest, state = self.phase_fixture()
        manifest["phase_offsets"]["phi"] = 1
        with self.assertRaises(ValueError):
            decode_fields(state, names, manifest)
        names, manifest, state = self.phase_fixture()
        state.b = state.b.astype(float)
        state.b[1, 0] = 1.9
        with self.assertRaises(TypeError):
            decode_fields(state, names, manifest)

    def test_provenance_rejects_source_tensor_and_parameter_mutation(self):
        report = {"run_id": "run", "bundle_id": "bundle", "steps": 3}
        integration = {**report, "source_commit": SOURCE_COMMIT, "tensor_hash": TENSOR_HASH,
                       "parameters": {"dt": 1, "dx": 1, "mass_squared": 1, "coupling": 1, "cosmological": 0},
                       "proposal_source_sha256": dict(SOURCE_HASHES)}
        reference = {"manifest": {"fingerprint": TENSOR_HASH}, "source_sha256": dict(SOURCE_HASHES)}
        bundle = SimpleNamespace(bundle_id="bundle", tensor=SimpleNamespace(fingerprint=TENSOR_HASH))
        self.assertTrue(validate_provenance(integration, reference, bundle, report)["pinned_commit_and_formula_hash_metadata"])
        changes = [("source_commit", "wrong"), ("tensor_hash", "wrong"), ("run_id", "other"),
                   ("parameters", {**integration["parameters"], "dt": True}),
                   ("proposal_source_sha256", {**SOURCE_HASHES, next(iter(SOURCE_HASHES)): "wrong"})]
        for key, value in changes:
            bad = copy.deepcopy(integration)
            bad[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_provenance(bad, reference, bundle, report)


if __name__ == "__main__":
    unittest.main()
