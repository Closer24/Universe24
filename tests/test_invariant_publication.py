"""Fail closed when published evidence is incomplete, changed or redirected."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research.invariant_families_v1.verify_evidence import (
    canonical, digest, inventory, verify,
)


class InvariantEvidencePublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / "research/invariant_families_v1/evidence/example.json.gz"
        self.file.parent.mkdir(parents=True)
        self.file.write_bytes(b"complete native recording")
        self.manifest = self.root / "manifest.json"

    def save(self, entries=None):
        raw = canonical({"format": "universe24-invariant-evidence-v1",
                         "files": inventory(self.root) if entries is None else entries})
        self.manifest.write_bytes(raw)
        return digest(raw)

    def check(self, pin):
        return verify(root=self.root, manifest=self.manifest,
                      expected_manifest_sha256=pin)

    def test_exact_inventory_and_modified_or_extra_file(self):
        pin = self.save()
        self.assertEqual(self.check(pin)["verified_files"], 1)
        self.file.write_bytes(b"changed")
        with self.assertRaises(ValueError):
            self.check(pin)
        self.file.write_bytes(b"complete native recording")
        self.file.with_name("extra.json").write_text("{}")
        with self.assertRaises(ValueError):
            self.check(pin)

    def test_pin_duplicate_and_traversal_rejected(self):
        pin = self.save()
        with self.assertRaises(ValueError):
            self.check("0" * 64)
        item = inventory(self.root)[0]
        for entries in ([item, item], [dict(item, path="research/invariant_families_v1/evidence/../run.py")]):
            with self.assertRaises(ValueError):
                self.check(self.save(entries))

    def test_symlink_cannot_redirect_a_valid_manifest(self):
        pin = self.save()
        other = self.root / "elsewhere"
        other.write_bytes(self.file.read_bytes())
        self.file.unlink()
        self.file.symlink_to(other)
        with self.assertRaises(ValueError):
            self.check(pin)

    def test_prefix_directory_symlink_is_rejected_before_inventory(self):
        original = self.file.parent
        moved = self.root / "elsewhere-directory"
        original.rename(moved)
        original.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(ValueError):
            inventory(self.root)


if __name__ == "__main__":
    unittest.main()
