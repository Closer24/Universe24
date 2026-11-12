"""Rejection checks for mixing distinct research laws, seeds and source code."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from validation.selection import run_audits
from validation.selection.coupled import REFERENCE_COMMIT


def partial_reports():
    """Only fields needed to reach the early shared-input boundaries."""
    reports = {name: {} for name in run_audits.REPORTS}
    table = [[0, 0, 0]]
    reports["clocks"] = {"source_sha256": "fresh", "gate_table": table,
                         "compiled_tensors": [{"tensor_hash": "native"}]}
    reports["complexity"] = {"collision_table": [{"output": table[0]}],
                             "bridge_source_sha256": "fresh", "growth_passes": 0,
                             "growth_failures": 30, "growth_blocked": 6}
    reports["qca"] = {"native_selector_quantum_lift": {"collision_table_mxy": table}}
    reports["born"] = {"gate": {"tensor_hash": "native", "Born_measure_derived": False},
                       "artifact_sha256": {}, "saved_replay": {
                           "transitions": 4080, "by_family": {"gate": 3072, "pointer": 1008},
                           "independent_scalar_replay": True, "complete_inverse": True,
                           "canonical_records_equal": True, "complete_contiguous_trial_chains": True}}
    reports["measurement"] = {"native_pointer_observation": {"source_sha256": "fresh"}}
    reports["pointer"] = {"failed": {"exclusive_choice": True}}
    reports["coupled"] = {"current_source_sha256": "fresh", "reference_commit": REFERENCE_COMMIT,
                          "current_main_full_state_comparisons": 40, "current_main_runtime_and_replay": True,
                          "raw_reference_sha256": "fresh", "primary_bundle_id": "source-seed",
                          "verified_reference_python_blobs": {"source.py": "pinned-blob"}}
    reports["physical_phase"] = {"raw_source_sha256": "fresh"}
    reports["pointer48"] = {"channels": 48, "base_bundle_id": "source-seed", "base_tensor_hash": "source-law"}
    reports["acceptance"] = {"native": {"explicit_collision_table": [{"after": table[0]}]}}
    return reports


class SelectionCollectionTests(unittest.TestCase):
    def collect_to_first_error(self, reports):
        out = Path("/independent-collection-fixture")
        paths = {str(out / relative): reports[name] for name, relative in run_audits.REPORTS.items()}
        def read(path):
            return deepcopy(paths[str(path)])
        def bundle(path):
            if "complexity" in str(path):
                return SimpleNamespace(bundle_id="native-seed", tensor=SimpleNamespace(G=3, fingerprint="native"))
            return SimpleNamespace(bundle_id="source-seed", tensor=SimpleNamespace(G=47, fingerprint="source-law"))
        with patch.object(run_audits, "read_json", side_effect=read), \
             patch.object(run_audits, "digest", return_value="fresh"), \
             patch.object(run_audits, "load_bundle", side_effect=bundle):
            return run_audits.collect(out)

    def test_stale_lane_source_rejected(self):
        reports = partial_reports()
        reports["clocks"]["source_sha256"] = "old-source"
        with self.assertRaisesRegex(ValueError, "stale clocks report"):
            self.collect_to_first_error(reports)

    def test_different_collision_table_rejected(self):
        reports = partial_reports()
        reports["complexity"]["collision_table"][0]["output"] = [1, 0, 0]
        with self.assertRaisesRegex(ValueError, "different gates"):
            self.collect_to_first_error(reports)

    def test_same_source_law_but_different_seed_rejected(self):
        reports = partial_reports()
        reports["pointer48"]["base_bundle_id"] = "different-source-seed"
        with self.assertRaisesRegex(ValueError, "different source seed or law"):
            self.collect_to_first_error(reports)


if __name__ == "__main__":
    unittest.main()
