"""Offline evidence restoration cannot overwrite live code or conflicting data."""
import hashlib
import gzip
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research.clock_selection.archive import build,materialize,evidence_path,PREFIX


class ClockEvidenceArchiveTests(unittest.TestCase):
    def fixture(self,folder):
        root=Path(folder)/'source';evidence=root/PREFIX;evidence.mkdir(parents=True)
        (evidence/'a.json').write_text('{"status":"failed target"}\n')
        (evidence/'b.json').write_text('{"complete":true}\n')
        parts=Path(folder)/'parts';receipt=build(parts,root=root)
        return root,parts,receipt['manifest_sha256']

    def test_check_restore_idempotence_and_conflict_before_any_write(self):
        with TemporaryDirectory() as folder:
            source,parts,pin=self.fixture(folder);target=Path(folder)/'restored';target.mkdir()
            report=materialize(root=target,parts=parts,expected_manifest_sha256=pin,check_only=True)
            self.assertEqual(report['verified_files'],2);self.assertFalse((target/PREFIX).exists())
            conflict=target/PREFIX;conflict.mkdir(parents=True);(conflict/'b.json').write_text('conflict')
            with self.assertRaises(FileExistsError):materialize(root=target,parts=parts,expected_manifest_sha256=pin)
            self.assertFalse((conflict/'a.json').exists())
            (conflict/'b.json').unlink()
            self.assertEqual(materialize(root=target,parts=parts,expected_manifest_sha256=pin)['restored_files'],2)
            self.assertEqual(materialize(root=target,parts=parts,expected_manifest_sha256=pin)['unchanged_files'],2)
            self.assertEqual((source/PREFIX/'a.json').read_bytes(),(conflict/'a.json').read_bytes())

    def test_corrupted_part_refuses_all_writes(self):
        with TemporaryDirectory() as folder:
            _,parts,pin=self.fixture(folder);target=Path(folder)/'restored';target.mkdir()
            path=parts/'part-000.bin';raw=path.read_bytes();path.write_bytes(raw[:-1]+bytes([raw[-1]^1]))
            with self.assertRaises(ValueError):materialize(root=target,parts=parts,expected_manifest_sha256=pin)
            self.assertFalse((target/PREFIX).exists())

    def test_explicit_lossless_gzip_representation_restores_original_bytes(self):
        with TemporaryDirectory() as folder:
            root=Path(folder)/'source';evidence=root/PREFIX;evidence.mkdir(parents=True)
            raw=b'{"all states": [1,2,3], "passed": false}\n'*50
            compressed=gzip.compress(raw,mtime=0)
            (evidence/'audit.json').write_bytes(raw);(evidence/'audit.json.gz').write_bytes(compressed)
            manifest=root/'representations.json'
            manifest.write_text(json.dumps({'format':'universe24-evidence-lossless-representations-v1','files':[
                {'path':PREFIX+'audit.json','gzip_path':PREFIX+'audit.json.gz','bytes':len(raw),
                 'sha256':hashlib.sha256(raw).hexdigest(),'gzip_sha256':hashlib.sha256(compressed).hexdigest()}]}))
            parts=Path(folder)/'parts';receipt=build(parts,root=root,representations=manifest)
            target=Path(folder)/'restored';target.mkdir()
            report=materialize(root=target,parts=parts,expected_manifest_sha256=receipt['manifest_sha256'])
            self.assertEqual(report['restored_files'],2)
            self.assertEqual((target/PREFIX/'audit.json').read_bytes(),raw)
            self.assertEqual((target/PREFIX/'audit.json.gz').read_bytes(),compressed)
            (evidence/'audit.json').write_bytes(raw+b'changed')
            with self.assertRaises(ValueError):build(Path(folder)/'bad-parts',root=root,representations=manifest)

    def test_namespace_and_symlink_guards_exclude_live_code(self):
        for path in ('universe24/core/rule3.py','tests/test_x.py','research/clock_selection/run.py',
                     '/research/clock_selection/evidence/a','research/clock_selection/evidence/../run.py',
                     'research/clock_selection/evidence/./a','research/clock_selection/evidence\\a'):
            self.assertFalse(evidence_path(path),path)
        with TemporaryDirectory() as folder:
            _,parts,pin=self.fixture(folder);target=Path(folder)/'restored';target.mkdir()
            parent=target/'research/clock_selection';parent.mkdir(parents=True)
            outside=Path(folder)/'outside';outside.mkdir();(parent/'evidence').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(ValueError):materialize(root=target,parts=parts,expected_manifest_sha256=pin)
            self.assertEqual(list(outside.iterdir()),[])


if __name__=='__main__':unittest.main()
