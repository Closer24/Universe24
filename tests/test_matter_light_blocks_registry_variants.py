"""Registry metadata of the explicitly separate candidate couplings: the five recorded tables rebuild from their
constructions with research.coupling_variants_v1, and the published variant block carries exactly its table (its
catalog entry as {"kind": "variant", "label", "fingerprint"}; its registry record and card name the label)."""
import hashlib
import json
from pathlib import Path
import unittest

from research.coupling_variants_v1 import VariantCoupling, load
from research.matter_light_blocks_v1 import verify as V

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research/matter_light_blocks_v1/registry/data"


def rebuild(record) -> VariantCoupling:
    """The table of a ``variant_couplings`` record, from its construction, named as in its label."""
    name = record["label"].split(":", 1)[1].rsplit("@", 1)[0]
    c = record["construction"]
    if c["kind"] == "axial":
        return VariantCoupling.axial(name, tuple(c["m"]), tuple(c["signs"]))
    if c["kind"] == "body_actions":
        return VariantCoupling.from_body_actions(name, tuple(c["actions"]), tuple(c["weights"]))
    raise ValueError(f"unknown construction {c['kind']}")


class VariantCouplingRecords(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((DATA / "registry.json").read_text(encoding="utf-8"))
        self.records = self.registry["variant_couplings"]

    def test_the_five_tables_rebuild_from_their_constructions(self):
        self.assertEqual(len(self.records), 5)
        labels = set()
        for record in self.records:
            with self.subTest(label=record["label"]):
                table = rebuild(record)                 # validated: covariant, reciprocal, unit weights
                self.assertTrue(table.is_variant)
                self.assertEqual(table.label, record["label"])
                for f in record["files"]:
                    self.assertEqual(f["fingerprint"], table.fingerprint)
                    path = ROOT / f["file"]
                    if path.exists():                  # files outside the curated tree are archived (README)
                        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest()[:16], f["sha256_prefix"])
                        self.assertEqual(load(path).engine.coupling.fingerprint, table.fingerprint)
                labels.add(table.label)
        self.assertEqual(len(labels), 5)
        self.assertEqual(rebuild(next(r for r in self.records if "chiral-077" in r["label"])).fingerprint,
                         "80d977155f54c04632bd55bd7dedef8894548dc4010aeb8ebaa0fdf6928bb32e")

    def test_the_variant_block_names_its_table(self):
        chiral = next(r for r in self.records if r["label"] == "variant:chiral-011-mpp@190301d802c5")
        table = rebuild(chiral)
        form = {"kind": "variant", "label": table.label, "fingerprint": table.fingerprint}
        self.assertEqual(table.label.rsplit("@", 1)[1], table.fingerprint[:12])        # the label's 12 hex
        variant_blocks = [e for e in V.load_catalog()["entries"] if (e.get("coupling") or {}).get("kind") == "variant"]
        self.assertTrue(variant_blocks)
        for entry in variant_blocks:
            with self.subTest(block=entry["name"]):
                self.assertEqual(entry["coupling"], form)
                self.assertIsNone(entry["signs"])
                self.assertEqual(V.experiment_of(entry).engine.coupling, table)
                self.assertIn(entry["name"], self.registry["published_roles"])
        cards = json.loads((DATA / "cards.json").read_text(encoding="utf-8"))["cards"]
        self.assertEqual(sorted(cards), sorted(b["id"] for b in self.registry["blocks"]))
        record = next(b for b in self.registry["blocks"] if b["id"] == "interaction.chiral_two_sector_board@1")
        self.assertEqual(record["coupling"].split(" ", 1)[0], table.label)          # free text naming the label
        self.assertEqual(cards[record["id"]]["coupling"], record["coupling"])


if __name__ == "__main__":
    unittest.main()
