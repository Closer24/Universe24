"""Acceptance tests for collection completeness and same-history evidence."""
from __future__ import annotations

import copy
import gzip
import hashlib
from pathlib import Path
import tempfile
import unittest

from universe24.core import exact_json
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle
from validation.local_unification import geometry, organization
from validation.local_unification.run_all import inspect_joint_run, validate_panel


class PanelCompletenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        cls.report = organization.audit(cls.root / "panel", full_panel=False)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_complete_quick_panel_keeps_every_control(self):
        result = validate_panel(self.report, full_panel=False)
        self.assertEqual(result["cases"], 9)
        self.assertEqual(result["shared_cases"], 3)
        self.assertEqual(result["designed_repeat_use_cases"], 48)
        self.assertTrue(result["all_declared_trials_retained"])

    def test_missing_duplicate_and_mixed_horizon_trials_are_rejected(self):
        missing = copy.deepcopy(self.report)
        missing["cases"].pop()
        duplicate = copy.deepcopy(self.report)
        duplicate["cases"][-1] = copy.deepcopy(duplicate["cases"][0])
        horizon = copy.deepcopy(self.report)
        horizon["cases"][0]["steps"] -= 1
        for changed in (missing, duplicate, horizon):
            with self.subTest(change=changed["cases"][-1]["variant"]):
                with self.assertRaises(ValueError):
                    validate_panel(changed, full_panel=False)

    def test_stale_source_and_mixed_law_are_rejected(self):
        stale = copy.deepcopy(self.report)
        stale["source_sha256"] = "0" * 64
        mixed = copy.deepcopy(self.report)
        mixed["cases"][0]["tensor_hash"] = "0" * 64
        for changed in (stale, mixed):
            with self.assertRaises(ValueError):
                validate_panel(changed, full_panel=False)

    def test_rechecks_archived_seed_and_horizon_after_checksum_refresh(self):
        with gzip.open(self.report["complete_panel_archive"], "rt", encoding="utf-8") as stream:
            rows = [exact_json.loads(line) for line in stream]
        for change in ("seed", "horizon"):
            changed_rows = copy.deepcopy(rows)
            if change == "seed":
                changed_rows[0]["states"][0]["r"][0][0] = (
                    changed_rows[0]["states"][0]["r"][0][0] + 1) % 6
            else:
                changed_rows[0]["states"].pop()
            archive = self.root / (change + ".jsonl.gz")
            with gzip.open(archive, "wt", encoding="utf-8") as stream:
                for row in changed_rows:
                    stream.write(exact_json.dumps(row, sort_keys=True) + "\n")
            changed = copy.deepcopy(self.report)
            changed["complete_panel_archive"] = str(archive)
            changed["complete_panel_archive_sha256"] = hashlib.sha256(archive.read_bytes()).hexdigest()
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    validate_panel(changed, full_panel=False)

    def test_missing_same_law_supply_control_is_rejected(self):
        changed = copy.deepcopy(self.report)
        changed["repeated_task"]["cases"] = [
            row for row in changed["repeated_task"]["cases"]
            if row["variant"] != "late_supply_removed"]
        with self.assertRaises(ValueError):
            validate_panel(changed, full_panel=False)

    def test_quick_evidence_cannot_claim_full_coverage(self):
        with self.assertRaises(ValueError):
            validate_panel(self.report, full_panel=True)


class JointHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        tensor, seed, cls.protocol = geometry.prepare_fixture(L=11, steps=2)
        channels = [
            {"index": index, "name": name, "label": tensor.labels[index],
             "owner": "collection-test", "purpose": "complete retained test state"}
            for index, name in enumerate(tensor.names)]
        bundle = create_bundle(
            tensor, seed, channels=channels, protocol=default_protocol(),
            model={"id": "local-unification-collection-test", "version": "1",
                   "domain": "finite null-source chart"})
        run_bundle(bundle, cls.root / "runtime", 2)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_actual_twelve_channel_history_joins_without_physics_promotion(self):
        result = inspect_joint_run(self.root / "runtime", self.protocol, out=self.root / "joint")
        self.assertEqual(result["identity"]["channels"], 12)
        self.assertEqual(result["identity"]["steps"], 2)
        self.assertEqual(result["statuses"]["independent_full_scalar_replay"], "passed")
        self.assertEqual(result["statuses"]["finite_null_source_chart"], "passed")
        # Each cohort sees only one supplied correction in this shorter run.
        self.assertEqual(result["statuses"]["finite_repeat_use"], "failed")
        self.assertEqual(result["statuses"]["global_periodic_positive_source_chart"], "failed")
        self.assertEqual(result["statuses"]["operational_proper_clock"], "not_tested")
        self.assertEqual(result["physical_acceptance"], "not_granted")
        self.assertEqual(result["join"]["identity_join"], "passed")

    def test_modified_initial_profile_metadata_is_rejected(self):
        changed = copy.deepcopy(self.protocol)
        changed["initial_profiles"][0][0] += 1
        with self.assertRaises(ValueError):
            inspect_joint_run(self.root / "runtime", changed)

    def test_different_requested_horizon_is_rejected(self):
        changed = copy.deepcopy(self.protocol)
        changed["microsteps"] = 4
        with self.assertRaises(ValueError):
            inspect_joint_run(self.root / "runtime", changed)


if __name__ == "__main__":
    unittest.main()
