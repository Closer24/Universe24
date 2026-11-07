"""Offline evidence restoration must not become an alternate code installer."""
from pathlib import Path
import tempfile
import unittest

from research.experiments.materialize_evidence import (
    ARCHIVE, PARTS, ROOT, destination, evidence_path, materialize,
)


class EvidenceMaterializationTests(unittest.TestCase):
    def setUp(self):
        (ROOT / 'runs').mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT / 'runs')
        self.root = Path(self.temporary.name).resolve()
        self.addCleanup(self.temporary.cleanup)
        parts = self.root / PARTS
        parts.parent.mkdir(parents=True)
        parts.symlink_to(ROOT / PARTS, target_is_directory=True)

    def test_targets_exclude_live_code_and_path_escapes(self):
        for path in ('universe24/core/rule3.py', 'research/components/recipes.py',
                     'research/experiments/run.py', 'tests/test_model.py',
                     'README.md', '../research/signal_clocks/evidence/evil',
                     'research/signal_clocks/evidence/../../../../evil'):
            with self.assertRaises(ValueError):
                destination(self.root, path)
        self.assertTrue(evidence_path('research/component_studies/selection_evidence_v1/source/universe24/core/rule3.py'))
        outside = self.root / 'outside'
        outside.mkdir()
        (self.root / 'research/signal_clocks').mkdir()
        (self.root / 'research/signal_clocks/evidence').symlink_to(outside)
        with self.assertRaises(ValueError):
            destination(self.root, 'research/signal_clocks/evidence/evil.json')

    def test_complete_archive_verification_is_read_only(self):
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*'))
        result = materialize(self.root, check_only=True)
        self.assertEqual(result['complete_recordings'], 1234)
        self.assertEqual(result['recorded_states'], 51638)
        self.assertEqual(result['live_runtime_files_written'], 0)
        self.assertEqual(result['restored_files'], 0)
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*')))

    def test_conflict_is_rejected_before_any_restoration(self):
        conflict = self.root / 'research/presenter/demo/The_Presenter.html'
        conflict.parent.mkdir(parents=True)
        conflict.write_bytes(b'Preserve this existing file')
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*'))
        with self.assertRaises(FileExistsError):
            materialize(self.root)
        self.assertEqual(conflict.read_bytes(), b'Preserve this existing file')
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob('*')))

    def test_corrupt_archive_is_rejected_before_writes(self):
        archive = self.root / ARCHIVE
        archive.write_bytes(b'Not the pinned delivery')
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            materialize(self.root)
        self.assertEqual(archive.read_bytes(), b'Not the pinned delivery')

    def local_parts(self):
        folder = self.root / PARTS
        folder.unlink()
        folder.mkdir()
        for path in (ROOT / PARTS).iterdir():
            (folder / path.name).symlink_to(path)
        return folder

    def test_missing_part_is_rejected_before_writes(self):
        folder = self.local_parts()
        (folder / 'part-041.bin').unlink()
        with self.assertRaises(FileNotFoundError):
            materialize(self.root)
        self.assertFalse((self.root / 'research/component_studies').exists())

    def test_corrupt_part_is_rejected_before_writes(self):
        folder = self.local_parts()
        target = folder / 'part-000.bin'
        raw = bytearray(target.read_bytes())
        raw[0] ^= 1
        target.unlink()
        target.write_bytes(raw)
        with self.assertRaisesRegex(ValueError, 'Archive part SHA-256'):
            materialize(self.root)
        self.assertFalse((self.root / 'research/component_studies').exists())

    def test_reordered_manifest_is_rejected_before_writes(self):
        import json
        folder = self.local_parts()
        target = folder / 'manifest.json'
        data = json.loads(target.read_bytes())
        data['parts'][0], data['parts'][1] = data['parts'][1], data['parts'][0]
        target.unlink()
        target.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'manifest SHA-256'):
            materialize(self.root)
        self.assertFalse((self.root / 'research/component_studies').exists())


if __name__ == '__main__':
    unittest.main()
