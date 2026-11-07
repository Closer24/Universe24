"""The integration layer must retain complete recordings and reject ambiguity."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research.presenter.export import capture
from research.staged_blocks.export import export_pages, export_records, partition_experiments, read_recordings
from research.staged_blocks.run import collect
from universe24 import Coupling, Cube, Engine, State


class StagedIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = Engine(Coupling())
        initial = State(Cube(5), (0, 0, 2), {(2, 2, 2, 0): (1, 0, 2)})
        cls.experiment = capture(engine, initial, 4, id="unseen-orbit", title="Unseen preparation")

    def write_record(self, folder, name="record.json.gz", experiment=None):
        path = folder / name
        data = json.dumps({"experiment": experiment or self.experiment}).encode()
        path.write_bytes(gzip.compress(data, mtime=0) if name.endswith(".gz") else data)
        return path

    def test_full_native_frames_survive_packaging(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            source = self.write_record(folder)
            report = export_records([source], folder / "presenter")
            output = json.loads((folder / "presenter/experiments.json").read_text())
            self.assertEqual(output["experiments"], [self.experiment])
            self.assertEqual(report["frames"], 5)
            self.assertEqual(report["inputs"][0]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            html = (folder / "presenter/The_Presenter.html").read_text()
            self.assertIn("Unseen preparation", html)
            self.assertIn('id="embedded-recordings"', html)

    def test_duplicate_ids_are_not_silently_replaced(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            first = self.write_record(folder, "a.json.gz")
            second = self.write_record(folder, "b.json")
            with self.assertRaisesRegex(ValueError, "Duplicate experiment IDs"):
                export_records([first, second], folder / "presenter")
            self.assertFalse((folder / "presenter").exists())

    def test_remainder_corruption_cannot_be_displayed_as_valid(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            broken = copy.deepcopy(self.experiment)
            broken["frames"][1]["cells"][0][-1] = 5
            source = self.write_record(folder, experiment=broken)
            with self.assertRaises(ValueError):
                export_records([source], folder / "presenter")

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            source = self.write_record(folder)
            output = folder / "presenter"
            output.mkdir()
            marker = output / "keep.txt"
            marker.write_text("original")
            with self.assertRaises(FileExistsError):
                export_records([source], output)
            self.assertEqual(marker.read_text(), "original")

    def test_duplicate_json_members_are_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "duplicate.json"
            path.write_text('{"experiment":{},"experiment":{}}')
            with self.assertRaisesRegex(ValueError, "Duplicate artifact member"):
                read_recordings(path)

    def test_decompressed_budget_is_enforced(self):
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / "large.json.gz"
            path.write_bytes(gzip.compress(b" " * 2048, mtime=0))
            with patch("research.staged_blocks.export.MAX_BYTES", 1024):
                with self.assertRaisesRegex(ValueError, "Decoded artifact"):
                    read_recordings(path)

    def test_collection_retains_empty_solver_scope_and_hashes(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            study = folder / "solver"
            study.mkdir()
            (study / "protocol.json").write_text('{"frozen":true}')
            (study / "result.json").write_text('{"status":"inconclusive_resource"}')
            result = collect({"synthesis": study}, folder / "report", presenter=False)
            manifest = json.loads((folder / "report/audit_manifest.json").read_text())
            self.assertEqual(result["complete_records"], 0)
            self.assertEqual(result["audit_status"], "not_run")
            entry = manifest["studies"][0]
            self.assertEqual(entry["records"], [])
            for key in ("protocol", "result"):
                path = folder / "report" / entry[key]["path"]
                self.assertEqual(entry[key]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_separate_studies_keep_distinct_identity_and_protocols(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            studies = {}
            for label in ("positive", "signed"):
                study = folder / label
                study.mkdir()
                (study / "protocol.json").write_text(json.dumps({"id": label}))
                (study / "result.json").write_text('{"status":"completed"}')
                studies[label + ":interaction"] = study
            collect(studies, folder / "report", presenter=False)
            manifest = json.loads((folder / "report/audit_manifest.json").read_text())
            self.assertEqual([s["id"] for s in manifest["studies"]], ["positive", "signed"])
            self.assertEqual([s["kind"] for s in manifest["studies"]], ["interaction", "interaction"])
            self.assertNotEqual(*[s["protocol"]["sha256"] for s in manifest["studies"]])

    def test_page_union_retains_every_complete_recording(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            expected, paths = [], []
            for index in range(4):
                experiment = copy.deepcopy(self.experiment)
                experiment["id"] = "complete-" + str(index)
                expected.append(experiment)
                paths.append(self.write_record(folder, str(index) + ".json.gz", experiment))
            result = export_pages(paths, folder / "pages", max_experiments=2)
            self.assertEqual([p["experiments"] for p in result["pages"]],
                             [["complete-0", "complete-1"], ["complete-2", "complete-3"]])
            retained = []
            for page in result["pages"]:
                retained.extend(json.loads((folder / "pages" / page["bundle"]).read_text())["experiments"])
                self.assertTrue((folder / "pages" / page["html"]).is_file())
            self.assertEqual(retained, expected)
            inventory = (folder / "pages/index.html").read_text()
            for experiment in expected:
                self.assertIn(experiment["id"], inventory)
            self.assertEqual(partition_experiments(expected, title="T", max_experiments=2),
                             partition_experiments(expected, title="T", max_experiments=2))

    def test_page_cell_boundary_is_exact_and_never_splits_one_experiment(self):
        rows = sum(len(f["cells"]) for f in self.experiment["frames"])
        second = copy.deepcopy(self.experiment)
        second["id"] = "second"
        pages = partition_experiments([self.experiment, second], title="T", max_cells=rows)
        self.assertEqual(pages, [[self.experiment], [second]])
        with self.assertRaisesRegex(ValueError, "One complete experiment exceeds"):
            partition_experiments([self.experiment], title="T", max_cells=rows-1)
        with self.assertRaisesRegex(ValueError, "cannot enlarge"):
            partition_experiments([self.experiment], title="T", max_cells=500001)


if __name__ == "__main__":
    unittest.main()
