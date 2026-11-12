"""Exercise destructive ref planning against an isolated local bare remote."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('archive', Path(__file__).with_name('archive_branches.py'))
archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = Path.cwd()
        root = Path(self.tmp.name)
        subprocess.check_call(['git', 'init', '--bare', '-q', str(root / 'remote')])
        (root / 'work').mkdir()
        os.chdir(root / 'work')
        archive.git('init', '-q', '-b', 'main')
        archive.git('config', 'user.email', 'test@example.invalid')
        archive.git('config', 'user.name', 'Cleanup test')
        archive.git('commit', '-q', '--allow-empty', '-m', 'baseline')
        self.sha = archive.git('rev-parse', 'HEAD')
        archive.git('remote', 'add', 'origin', str(root / 'remote'))
        archive.git('push', '-q', 'origin', 'HEAD:main', 'HEAD:research/a', 'HEAD:research/b')
        self.snapshot = dict(repository='Closer24/Universe24', default_branch='main',
                             archive_prefix='archive/consolidation/', branches=[
                                 dict(branch=name, sha=self.sha) for name in ('research/a', 'research/b')])

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def test_atomic_archive_delete_and_idempotent_replay(self):
        specs, leases = archive.plan(self.snapshot)
        archive.git('push', '--atomic', *leases, 'origin', *specs)
        self.assertEqual(archive.git('ls-remote', '--heads', 'origin').split()[1], 'refs/heads/main')
        tags = archive.git('ls-remote', '--tags', 'origin').splitlines()
        self.assertEqual(len(tags), 2)
        self.assertTrue(all(line.split()[0] == self.sha for line in tags))
        self.assertEqual(archive.plan(self.snapshot), ([], []))

    def test_main_and_duplicate_names_are_rejected(self):
        self.snapshot['branches'].append(dict(branch='main', sha=self.sha))
        with self.assertRaises(ValueError):
            archive.plan(self.snapshot)
        self.snapshot['branches'][-1]['branch'] = 'research/a'
        with self.assertRaises(ValueError):
            archive.plan(self.snapshot)

    def test_moved_head_is_rejected(self):
        archive.git('commit', '-q', '--allow-empty', '-m', 'new work')
        archive.git('push', '-q', 'origin', 'HEAD:research/a')
        with self.assertRaises(ValueError):
            archive.plan(self.snapshot)

    def test_post_plan_race_preserves_all_refs_atomically(self):
        specs, leases = archive.plan(self.snapshot)
        archive.git('commit', '-q', '--allow-empty', '-m', 'concurrent work')
        archive.git('push', '-q', 'origin', 'HEAD:research/a')
        with self.assertRaises(subprocess.CalledProcessError):
            archive.git('push', '--atomic', *leases, 'origin', *specs)
        self.assertEqual(len(archive.git('ls-remote', '--heads', 'origin').splitlines()), 3)
        self.assertEqual(archive.git('ls-remote', '--tags', 'origin'), '')


if __name__ == '__main__':
    unittest.main()
