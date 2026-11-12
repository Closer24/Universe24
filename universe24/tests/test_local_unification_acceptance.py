"""Adversarial tests of the independent complete-state acceptance boundary."""
from __future__ import annotations
from copy import deepcopy
import gzip
import hashlib
from pathlib import Path
import shutil
import tempfile
import unittest
from universe24.core import exact_json
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle
from validation.local_unification import acceptance, geometry

class IndependentAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name)
        cls.run_dir = cls.root/"actual-twelve"
        cls.tensor, cls.seed, cls.protocol = geometry.prepare_fixture(L=11, steps=2)
        channels = [
            {"index": index, "name": cls.tensor.names[index],
             "label": cls.tensor.labels[index], "owner": "acceptance-test",
             "purpose": "complete state including source profiles"}
            for index in range(cls.tensor.G)
        ]
        bundle = create_bundle(cls.tensor, cls.seed, channels=channels,
                               protocol=default_protocol(),
                               model={"id": "independent-acceptance-test", "version": "1",
                                      "domain": "finite causal chart"})
        cls.runtime_report = run_bundle(bundle, cls.run_dir, 2)
        cls.bundle_id = bundle.bundle_id

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def _copy(self, name):
        destination = self.root/name
        shutil.copytree(self.run_dir, destination)
        return destination

    def _replace_records(self, run, filename, records):
        payload = "".join(acceptance._dump(record)+"\n" for record in records).encode()
        target = run/filename
        target.write_bytes(gzip.compress(payload, mtime=0))
        report_path = run/"validation.json"
        report = exact_json.loads(report_path.read_text())
        report["files"][filename] = hashlib.sha256(target.read_bytes()).hexdigest()
        report_path.write_text(acceptance._dump(report)+"\n")

    def test_full_twelve_state_oracle_inverse_clicks_and_same_source(self):
        out = self.root/"independent-report.json"
        result = acceptance.audit_saved_run(self.run_dir, protocol=self.protocol, out=out)
        self.assertEqual(result["tensor_hash"], self.tensor.fingerprint)
        self.assertEqual(result["bundle_id"], self.bundle_id)
        self.assertEqual(result["run_id"], self.runtime_report["run_id"])
        self.assertEqual(result["seed_hash"], acceptance._hash(self.seed.to_dict()))
        self.assertEqual(result["steps"], 2)
        self.assertEqual(result["channels_per_node"], 12)
        self.assertEqual(result["scalar_forward_inverse_register_comparisons"],
                         2*3*12*11**3*2)
        self.assertEqual(result["independent_canonical_clicks"], self.runtime_report["click_count"])
        self.assertEqual(result["complete_legal_carry_classes"], list(range(6)))
        self.assertEqual(result["ledger"]["selected_steps"], [1, 2])
        self.assertGreater(result["ledger"]["interior_source_checks"], 0)
        self.assertEqual(result["ledger"]["exact_local_balances"], 2*11**3*2)
        self.assertEqual(result["ledger"]["macro_stream_comparisons"], 2*11**3)
        self.assertEqual(result["scope"]["same_state_discrete_source_chart"], "passed")
        self.assertEqual(exact_json.loads(out.read_text()), result)

    def test_wrong_source_tensor_cannot_borrow_native_collision_evidence(self):
        with self.assertRaisesRegex(ValueError, "source specification"):
            acceptance.validate_tensor(geometry.build_tensor(source_coupling=False))
        data = deepcopy(self.seed.to_dict())
        for field in ("a", "b", "r"):
            data[field] = data[field][:8]
        with self.assertRaisesRegex(ValueError, "channels"):
            acceptance.scalar_step(self.tensor, data)

    def test_rehashed_corruption_of_geometry_register_is_rejected(self):
        run = self._copy("corrupt-profile")
        records = list(acceptance._records(run/"full_trace.jsonl.gz"))
        records[0]["after"]["b"][8][0] += 1
        self._replace_records(run, "full_trace.jsonl.gz", records)
        with self.assertRaisesRegex(ValueError, "scalar forward mismatch"):
            acceptance.audit_saved_run(run, protocol=self.protocol)

    def test_rehashed_boolean_old_state_alias_is_rejected(self):
        run = self._copy("boolean-old-state")
        records = list(acceptance._records(run/"full_trace.jsonl.gz"))
        records[0]["before"]["b"][0][0] = bool(records[0]["before"]["b"][0][0])
        self._replace_records(run, "full_trace.jsonl.gz", records)
        with self.assertRaisesRegex(ValueError, "noninteger"):
            acceptance.audit_saved_run(run, protocol=self.protocol)

    def test_rehashed_boolean_click_alias_is_rejected(self):
        run = self._copy("boolean-click")
        records = list(acceptance._records(run/"clicks.jsonl.gz"))
        records[0]["step"] = True
        self._replace_records(run, "clicks.jsonl.gz", records)
        with self.assertRaisesRegex(ValueError, "canonical click differs"):
            acceptance.audit_saved_run(run, protocol=self.protocol)

    def test_geometry_protocol_must_match_actual_history(self):
        states = [self.seed.to_dict()]
        states.extend(record["after"] for record in acceptance._records(self.run_dir/"full_trace.jsonl.gz"))
        for change in ({"microsteps": 4}, {"interior_coordinate": 0},
                       {"receiver_coordinate": 6}, {"ticks_per_macro": 2.0}):
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    acceptance.inspect_history(states, protocol={**self.protocol, **change})
        bad = deepcopy(states[0])
        bad["b"][8][(5*11)*11] += 1
        with self.assertRaisesRegex(ValueError, "source constraint"):
            acceptance.inspect_history([bad, *states[1:]], protocol=self.protocol)

    def test_illegal_carry_cannot_enter_scalar_oracle(self):
        before = self.seed.to_dict()
        before["r"][11][0] = 6
        with self.assertRaisesRegex(ValueError, "illegal carry"):
            acceptance.scalar_step(self.tensor, before)

if __name__ == "__main__":
    unittest.main()
