"""Published matter/light building blocks: catalog integrity and a fast native replay subset."""
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


if __name__ == "__main__":
    unittest.main()
