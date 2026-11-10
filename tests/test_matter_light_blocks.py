"""Published matter/light building blocks: catalog integrity, a fast native replay subset, the command line, and the
variant branch."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from universe24.experiments import from_dict
from research.matter_light_blocks_v1 import append as A
from research.matter_light_blocks_v1 import verify as V

FAST = ("fiber_x_packet", "exact_front_111_box", "spinor_screw", "spin720_ring",
        "planar_glider_100", "atom_trap_d6", "d1_local_atom_L100", "spin_module_pure4pairs_L80")


class PublishedBlocks(unittest.TestCase):
    def setUp(self):
        self.catalog = V.load_catalog()
        self.entries = {e["name"]: e for e in self.catalog["entries"]}

    def test_catalog_files_and_hashes(self):
        self.assertGreaterEqual(len(self.entries), 300)
        self.assertEqual(self.catalog["rejected"], [])
        for entry in self.entries.values():
            path = V.HERE / entry["file"]
            self.assertTrue(path.exists(), entry["name"])
            self.assertEqual(V.file_sha256(path), entry["file_sha256"], entry["name"])

    def test_official_init_format(self):
        data = json.loads((V.HERE / self.entries["fiber_x_packet"]["file"]).read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"side", "coupling_signs", "background", "steps", "seed_changes"})

    def test_fast_subset_replays_exactly(self):
        for name in FAST:
            with self.subTest(block=name):
                entry = self.entries[name]
                self.assertEqual(V.check(entry, V.replay(entry)), [])


class CommandLine(unittest.TestCase):
    """argparse: an unknown or abbreviated flag stops with exit status 2 and a usage line, and --help prints the
    usage; neither loads the catalog or replays a block."""

    def _stop(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as stop:
            V.main(argv)
        return stop.exception.code, out.getvalue(), err.getvalue()

    def test_usage_errors_exit_2_and_help(self):
        usage = "usage: python -m research.matter_light_blocks_v1.verify"
        for argv in (["--bogus"], ["--quik"], ["--lis"], ["fiber_x_packet", "-q"]):
            code, out, err = self._stop(argv)
            self.assertEqual((code, out), (2, ""), argv)
            self.assertIn(usage, err)
        code, out, err = self._stop(["--help"])
        self.assertEqual(code, 0)
        self.assertIn(usage, out)
        for flag in ("--list", "--quick"):
            self.assertIn(flag, out)
        code, out, err = self._stop(["no_such_block"])
        self.assertEqual(code, "unknown block(s): ['no_such_block']")



class VariantBlocks(unittest.TestCase):
    """Variant init files (research.coupling_variants_v1) are appended, labelled and replayed; nothing else."""
    SOURCE = "research/coupling_variants_v1/examples/impulse_axial_m017.json"
    COUPLING = {"kind": "variant", "label": "variant:axial-m017-ppp@fc4d2d79f634",
                "fingerprint": "fc4d2d79f6341c27348dda941edf1cce3366969bf2f8748de18de110a450ec0e"}

    def proposal(self, **changes):
        entry = {"name": "variant_impulse_test", "group": "light", "file": self.SOURCE, "steps": 12,
                 "what": "VARIANT axial-m017-ppp: one impulse (test entry)", "limits": "test only",
                 "status": "test", "source": "test", "origin": self.SOURCE, "added": "test",
                 "coupling": dict(self.COUPLING)}
        entry.update(changes)
        return {"entries": [entry]}

    def test_variant_entry_is_labelled_and_replayed(self):
        with tempfile.TemporaryDirectory() as tmp:
            (entry,) = A.prepare(self.proposal(), {"entries": []}, Path(tmp))      # replays and checks
            self.assertIsNone(entry["signs"])
            self.assertEqual(entry["coupling"], self.COUPLING)
            text = (Path(tmp) / entry["file"]).read_text(encoding="utf-8")
            self.assertEqual(text, (A.ROOT / self.SOURCE).read_text(encoding="utf-8"))   # canonical layout
            with self.assertRaises(ValueError):
                from_dict(json.loads(text))                    # the reference loader refuses a variant file

    def test_coupling_must_match_the_file(self):
        wrong = dict(self.COUPLING, fingerprint="0" * 64)
        for proposal in (self.proposal(coupling=wrong), self.proposal(coupling=None),
                         self.proposal(file="examples/impulse.json", steps=12)):
            with self.subTest(proposal=proposal["entries"][0]["file"]), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    A.prepare(proposal, {"entries": []}, Path(tmp))
        entry = {"name": "x", "file": "../../" + self.SOURCE, "signs": [1, 1, 1]}
        with self.assertRaises(ValueError):
            V.experiment_of(entry)                             # a variant file needs its declared table

    def test_reference_table_is_not_a_variant(self):
        from research.coupling_variants_v1 import VariantCoupling, init_data
        state = V.load_init(json.loads((A.ROOT / self.SOURCE).read_text(encoding="utf-8"))).initial
        with self.assertRaises(ValueError):
            V.load_init(init_data(VariantCoupling.reference((1, 1, 1)), state, 12))


if __name__ == "__main__":
    unittest.main()
