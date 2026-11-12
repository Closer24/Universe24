"""Execute the owner's fixed branch-cleanup snapshot with atomic Git leases."""
import argparse
import json
from pathlib import Path
import subprocess


def git(*args, capture=True):
    return subprocess.check_output(['git', *args], text=True).strip() if capture else subprocess.check_call(['git', *args])


def plan(snapshot):
    if snapshot['repository'] != 'Closer24/Universe24' or snapshot['default_branch'] != 'main':
        raise ValueError('Unexpected repository/default branch')
    prefix = snapshot['archive_prefix']
    if prefix != 'archive/consolidation/':
        raise ValueError('Unexpected archive namespace')
    branches = snapshot['branches']
    names = [row['branch'] for row in branches]
    if len(names) != len(set(names)) or 'main' in names or not names:
        raise ValueError('Duplicate, empty or protected cleanup plan')
    remote = dict(line.split()[::-1] for line in git('ls-remote', '--heads', '--tags', 'origin').splitlines())
    specs, leases = [], []
    for row in branches:
        branch, sha = row['branch'], row['sha']
        head, tag = 'refs/heads/' + branch, 'refs/tags/' + prefix + branch
        git('check-ref-format', head)
        git('check-ref-format', tag)
        if len(sha) != 40 or any(c not in '0123456789abcdef' for c in sha):
            raise ValueError('Invalid exact source identity')
        if head not in remote:
            if remote.get(tag) == sha:
                continue  # A completed run is idempotent.
            raise ValueError('Branch disappeared without its exact archive: ' + branch)
        if remote[head] != sha:
            raise ValueError('Branch moved; inspect the new work before deleting: ' + branch)
        if tag in remote and remote[tag] != sha:
            raise ValueError('Archive tag already has another identity: ' + tag)
        git('cat-file', '-e', sha + '^{commit}')
        specs += [sha + ':' + tag, ':' + head]
        leases.append('--force-with-lease=' + head + ':' + sha)
    return specs, leases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    snapshot = json.loads(Path('.github/branch-cleanup.json').read_text())
    specs, leases = plan(snapshot)
    print('Exact branches retained as archive tags:', len(specs) // 2, flush=True)
    if specs:
        command = ['push', '--atomic', *leases, 'origin', *specs]
        git(*command[:1], '--dry-run', *command[1:], capture=False)
        if args.apply:
            git(*command, capture=False)
    if args.apply:
        heads = git('ls-remote', '--heads', 'origin').splitlines()
        if len(heads) != 1 or heads[0].split()[1] != 'refs/heads/main':
            raise ValueError('Additional branch appeared; preserve it for inspection')
        print('Verified: main is the only branch; exact archived heads are retained.')


if __name__ == '__main__':
    main()
