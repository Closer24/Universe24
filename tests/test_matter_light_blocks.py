"""Published matter/light building blocks: catalog integrity, a fast native replay subset and the command line."""
import contextlib
import io
import json
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
