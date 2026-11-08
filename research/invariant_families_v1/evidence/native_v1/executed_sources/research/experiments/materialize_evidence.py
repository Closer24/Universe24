"""Restore declared research evidence from the pinned local delivery archive.

This is offline file restoration, not a simulation. Live engine, research
modules, tests, documentation and configuration are never archive targets.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = Path('research/artifacts/Universe24_Components.zip')
PARTS = Path('research/artifacts/Universe24_Components.parts')
PARTS_MANIFEST_SHA256 = '43732bc06a039b1c0ed139aa3b95df729ce331cdc7b3223e35a50073408e08e7'
ARCHIVE_SHA256 = '696ae53fe6fb76cd08ff0cfe6544f25d0063c68256c4e49293b9bfd3d2baa5e7'
PREFIX = 'Universe24_Components/'
STUDIES = frozenset({
    'confirmation_search_evidence_v1', 'confirmation_buffer_evidence_v1',
    'confirmation_packet_evidence_v1', 'selection_evidence_v1',
    'selection_followup_evidence_v1', 'selection_receiver_evidence_v1',
})


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def file_digest(path):
    result = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def evidence_path(value):
    """The explicit data namespaces; live executable namespaces are excluded."""
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '\\' in value:
        raise ValueError('Invalid evidence path')
    parts = path.parts
    if len(parts) >= 4 and parts[:2] == ('research', 'component_studies'):
        return parts[2] in STUDIES
    for prefix in (('research', 'signal_clocks', 'evidence'),
                   ('research', 'experiments', 'evidence'),
                   ('research', 'presenter', 'demo'),
                   ('research', 'presenter', 'evidence')):
        if len(parts) > len(prefix) and parts[:len(prefix)] == prefix:
            return True
    if len(parts) >= 4 and parts[:3] == ('research', 'component_review', 'source'):
        return True  # Immutable historical source snapshots are evidence, not imports.
    return False


def destination(root, value):
    if not evidence_path(value):
        raise ValueError('Target is outside the declared evidence namespaces: ' + value)
    target = root / value
    if not target.resolve().is_relative_to(root):
        raise ValueError('Evidence target escapes the repository')
    for parent in (target, *target.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError('Symlinks are not evidence targets')
    return target


def archive_source(root):
    """Read the original archive or reconstruct its exact bytes, without writes."""
    archive = root / ARCHIVE
    if archive.exists():
        if file_digest(archive) != ARCHIVE_SHA256:
            raise ValueError('Delivery archive SHA-256 mismatch; no files restored')
        return archive
    folder = root / PARTS
    raw_manifest = (folder / 'manifest.json').read_bytes()
    if digest(raw_manifest) != PARTS_MANIFEST_SHA256:
        raise ValueError('Archive parts manifest SHA-256 mismatch; no files restored')
    manifest = json.loads(raw_manifest)
    if (manifest['format'] != 'universe24-delivery-parts-v1'
            or manifest['archive'] != ARCHIVE.name
            or manifest['archive_sha256'] != ARCHIVE_SHA256
            or manifest['archive_bytes'] != 44029448
            or manifest['part_bytes'] != 1048576
            or len(manifest['parts']) != 42):
        raise ValueError('Unexpected archive parts specification')
    chunks = []
    for index, record in enumerate(manifest['parts']):
        if record['file'] != f'part-{index:03d}.bin':
            raise ValueError('Archive parts are out of order or escape their directory')
        raw = (folder / record['file']).read_bytes()
        if len(raw) != record['bytes'] or digest(raw) != record['sha256']:
            raise ValueError('Archive part SHA-256 or length mismatch; no files restored')
        chunks.append(raw)
    raw = b''.join(chunks)
    if len(raw) != manifest['archive_bytes'] or digest(raw) != ARCHIVE_SHA256:
        raise ValueError('Reconstructed archive SHA-256 mismatch; no files restored')
    return BytesIO(raw)


def materialize(root=ROOT, *, check_only=False):
    root = Path(root).resolve()
    archive = archive_source(root)
    with ZipFile(archive) as bundle:
        names = bundle.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive member')
        inventory = json.loads(bundle.read(PREFIX + 'archive_manifest.json'))
        records = {item['path']: item for item in inventory['files']}
        if len(records) != len(inventory['files']):
            raise ValueError('Duplicate inventory path')

        def checked(member):
            record = records[member]
            raw = bundle.read(member)
            if len(raw) != record['bytes'] or digest(raw) != record['sha256']:
                raise ValueError('Archive member hash mismatch: ' + member)
            return raw

        plan = {}
        repository_prefix = PREFIX + 'repository/'
        collection_prefix = PREFIX + 'collection/'
        for member, record in records.items():
            if member.startswith(repository_prefix):
                relative = member[len(repository_prefix):]
                if evidence_path(relative):
                    plan[relative] = (member, False, record['sha256'])
            elif member.startswith(collection_prefix):
                relative = 'research/experiments/evidence/assembly_v1/complete_collection/' + member[len(collection_prefix):]
                plan[relative] = (member, False, record['sha256'])

        collection = json.loads(checked(collection_prefix + 'manifest.json'))
        if (collection['experiments'], collection['frames'], len(collection['full_recordings'])) != (1234, 51638, 1234):
            raise ValueError('Unexpected complete-recording counts')
        for item in collection['full_recordings']:
            relative = item['original_path']
            if not relative.startswith('research/component_studies/') or not evidence_path(relative):
                raise ValueError('Native recording escapes its declared study')
            member = collection_prefix + item['file']
            encoded = checked(member)
            if digest(encoded) != item['archive_sha256']:
                raise ValueError('Recording archive hash mismatch')
            decoded = gzip.decompress(encoded)
            if digest(decoded) != item['decoded_sha256']:
                raise ValueError('Decoded recording hash mismatch')
            decompress = not relative.endswith('.gz')
            raw = decoded if decompress else encoded
            if digest(raw) != item['original_sha256']:
                raise ValueError('Original recording hash mismatch')
            existing = plan.get(relative)
            candidate = (member, decompress, item['original_sha256'])
            if existing is not None and existing[2] != candidate[2]:
                raise ValueError('Conflicting archive target')
            plan[relative] = candidate

        def content(item):
            raw = checked(item[0])
            raw = gzip.decompress(raw) if item[1] else raw
            if digest(raw) != item[2]:
                raise ValueError('Evidence content hash mismatch')
            return raw

        # Validate the entire plan before making any change. A conflicting file
        # is never overwritten, and an interrupted copy can be safely resumed.
        unchanged = 0
        for relative, item in sorted(plan.items()):
            target = destination(root, relative)
            content(item)
            if target.exists():
                if not target.is_file() or file_digest(target) != item[2]:
                    raise FileExistsError('Different existing evidence: ' + relative)
                unchanged += 1
        restored = 0
        if not check_only:
            for relative, item in sorted(plan.items()):
                target = destination(root, relative)
                if target.exists():
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as handle:
                    handle.write(content(item))
                restored += 1
        return {'format': 'universe24-evidence-materialization-v1',
                'archive_sha256': ARCHIVE_SHA256, 'check_only': check_only,
                'verified_files': len(plan), 'restored_files': restored,
                'unchanged_files': unchanged, 'complete_recordings': 1234,
                'recorded_states': 51638, 'live_runtime_files_written': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    print(json.dumps(materialize(check_only=args.check_only), indent=2))


if __name__ == '__main__':
    main()
