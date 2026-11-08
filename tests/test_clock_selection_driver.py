"""Evidence indexing must retain negative outcomes and detect altered bytes."""
import json
from pathlib import Path
import tempfile
import unittest

from research.clock_selection.run import index_studies, verify_index
from research.clock_selection.provenance import freeze_sources, verify_sources


class ClockSelectionDriverTests(unittest.TestCase):
    def test_archived_source_tampering_is_distinct_from_live_source_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "snapshot"
            source = "research/clock_selection/provenance.py"
            freeze_sources(target, [source], metadata={"seed": 0})
            first = verify_sources(target)
            self.assertTrue(first["archive_verified"])
            self.assertTrue(first["live_sources_unchanged"])
            (target / "source" / source).write_text("altered archived bytes")
            changed = verify_sources(target)
            self.assertFalse(changed["archive_verified"])
            self.assertTrue(changed["live_sources_unchanged"])
            with self.assertRaises(FileExistsError):
                freeze_sources(target, [source])

    def test_failed_result_is_preserved_and_record_tampering_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            study = root / "study"
            (study / "records").mkdir(parents=True)
            (study / "protocol.json").write_text('{"criterion":"fixed"}')
            original = '{"accepted":false,"reason":"no conditional response"}'
            (study / "result.json").write_text(original)
            record = study / "records" / "failed-case.json"
            record.write_text('{"complete_record":"retained"}')
            result = index_studies({"pilot": study}, root / "index")
            self.assertEqual(result["records"], 1)
            self.assertEqual((study / "result.json").read_text(), original)
            self.assertEqual(verify_index(root / "index" / "index.json")["files_verified"], 3)
            record.write_text('{"complete_record":"altered"}')
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                verify_index(root / "index" / "index.json")

    def test_empty_solver_scope_is_retained_and_existing_output_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            study = root / "solver"
            study.mkdir()
            for name, value in (("protocol", {"budget": 1}),
                                ("result", {"status": "inconclusive"})):
                (study / (name + ".json")).write_text(json.dumps(value))
            result = index_studies({"solver": study}, root / "index")
            self.assertEqual(result["records"], 0)
            self.assertEqual(len(result["studies"]), 1)
            with self.assertRaises(FileExistsError):
                index_studies({"solver": study}, root / "index")


if __name__ == "__main__":
    unittest.main()
