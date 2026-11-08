"""Checksum-locked offline transport for clock-selection evidence only.

The builder does not delete expanded evidence. The materializer can restore only
this module's evidence subtree; live code, tests, docs and core are excluded.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
from io import BytesIO
import json
from pathlib import Path,PurePosixPath
import stat
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED,ZIP_STORED

ROOT=Path(__file__).resolve().parents[2]
PREFIX="research/clock_selection/evidence/"
PARTS=Path("research/clock_selection/artifacts/evidence_v1.parts")
REPRESENTATIONS=Path("research/clock_selection/evidence_transport_representations.json")
PINNED_MANIFEST_SHA256="UNSET_PENDING_FINAL_RESEARCH_FREEZE"
PART_BYTES=1024*1024
MAX_ARCHIVE_BYTES=300*1024*1024
MAX_EXPANDED_BYTES=2*1024*1024*1024


def digest(raw):return hashlib.sha256(raw).hexdigest()


def canonical(value):return (json.dumps(value,indent=2,sort_keys=True)+"\n").encode()


def evidence_path(value):
    if not isinstance(value,str) or "\\" in value:return False
    path=PurePosixPath(value)
    return (path.as_posix()==value and not path.is_absolute() and ".." not in path.parts
            and value.startswith(PREFIX) and len(path.parts)>3)


def destination(root,value):
    if not evidence_path(value):raise ValueError("Outside clock-selection evidence: "+str(value))
    target=root/value
    if not target.resolve().is_relative_to(root):raise ValueError("Evidence path escapes root")
    for parent in (target,*target.parents):
        if parent==root:break
        if parent.is_symlink():raise ValueError("Symlinks cannot be evidence targets")
    return target


def files(root):
    folder=root/PREFIX
    result=[]
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():raise ValueError("Evidence contains a symlink")
        if path.is_file() and '__pycache__' not in path.parts and path.suffix!='.pyc':result.append(path)
    if not result:raise ValueError("No evidence files")
    return result


def build(parts,*,root=ROOT,representations=None):
    root=Path(root).resolve();parts=Path(parts).resolve()
    if parts.exists():raise FileExistsError(parts)
    if parts.is_relative_to(root/PREFIX):raise ValueError("Archive output cannot be inside evidence")
    source=files(root);inventory=[]
    for path in source:
        raw=path.read_bytes();inventory.append({"path":path.relative_to(root).as_posix(),"bytes":len(raw),"sha256":digest(raw)})
    representation_path=root/REPRESENTATIONS if representations is None else Path(representations)
    representations=json.loads(representation_path.read_text()) if representation_path.exists() else {"format":"universe24-evidence-lossless-representations-v1","files":[]}
    if representations.get('format')!='universe24-evidence-lossless-representations-v1':raise ValueError("Invalid representation manifest")
    by_path={item['path']:item for item in inventory};represented=set()
    for item in representations['files']:
        raw_path,gz_path=item['path'],item['gzip_path']
        if raw_path in represented or raw_path==gz_path or raw_path not in by_path or gz_path not in by_path:
            raise ValueError("Invalid represented evidence paths")
        if not evidence_path(raw_path) or not evidence_path(gz_path):raise ValueError("Outside represented evidence")
        raw=(root/raw_path).read_bytes();compressed=(root/gz_path).read_bytes()
        if (len(raw)!=item['bytes'] or digest(raw)!=item['sha256'] or digest(compressed)!=item['gzip_sha256']
            or gzip.decompress(compressed)!=raw):raise ValueError("Lossless representation mismatch")
        by_path[raw_path]['gzip_source']=gz_path;represented.add(raw_path)
    if any(item.get('gzip_source') in represented for item in inventory):raise ValueError("Chained representations are forbidden")
    total=sum(item['bytes'] for item in inventory)
    if total>MAX_EXPANDED_BYTES:raise ValueError("Expanded evidence exceeds transport limit")
    inventory_raw=canonical({"format":"universe24-clock-evidence-inventory-v1","files":inventory})
    stream=BytesIO()
    with ZipFile(stream,'w',allowZip64=True) as archive:
        info=ZipInfo('inventory.json',(1980,1,1,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16
        archive.writestr(info,inventory_raw,compresslevel=9)
        for item in inventory:
            raw=(root/item['path']).read_bytes()
            if digest(raw)!=item['sha256']:raise ValueError("Evidence changed during archive build")
            if 'gzip_source' in item:continue
            info=ZipInfo(item['path'],(1980,1,1,0,0,0));info.external_attr=0o100644<<16
            info.compress_type=ZIP_STORED if Path(item['path']).suffix in ('.gz','.png','.gif','.zip') else ZIP_DEFLATED
            archive.writestr(info,raw,compresslevel=9)
    raw_archive=stream.getvalue()
    if len(raw_archive)>MAX_ARCHIVE_BYTES:raise ValueError("Archive exceeds transport limit")
    if [p.relative_to(root).as_posix() for p in files(root)]!=[r['path'] for r in inventory]:
        raise ValueError("Evidence file list changed during archive build")
    for item in inventory:
        if digest((root/item['path']).read_bytes())!=item['sha256']:raise ValueError("Evidence changed after packing")
    parts.mkdir(parents=True,exist_ok=False)
    (parts/'executed_builder.py').write_bytes(Path(__file__).read_bytes())
    chunks=[]
    for i,start in enumerate(range(0,len(raw_archive),PART_BYTES)):
        raw=raw_archive[start:start+PART_BYTES];name=f'part-{i:03d}.bin';(parts/name).write_bytes(raw)
        chunks.append({"file":name,"bytes":len(raw),"sha256":digest(raw)})
    manifest={"format":"universe24-clock-evidence-parts-v1","archive_sha256":digest(raw_archive),
        "archive_bytes":len(raw_archive),"part_bytes":PART_BYTES,"parts":chunks,"inventory_sha256":digest(inventory_raw),
        "expanded_files":len(inventory),"expanded_bytes":total,"target_prefix":PREFIX,
        "lossless_representations":representations['files'],
        "live_runtime_files_written":0,"builder_sha256":digest(Path(__file__).read_bytes())}
    manifest_raw=canonical(manifest);(parts/'manifest.json').write_bytes(manifest_raw)
    return {"parts":str(parts),"manifest_sha256":digest(manifest_raw),"archive_bytes":len(raw_archive),"expanded_files":len(inventory),"expanded_bytes":total}


def materialize(*,root=ROOT,parts=None,check_only=False,expected_manifest_sha256=PINNED_MANIFEST_SHA256):
    root=Path(root).resolve();parts=(root/PARTS if parts is None else Path(parts).resolve())
    raw=(parts/'manifest.json').read_bytes()
    if digest(raw)!=expected_manifest_sha256:raise ValueError("Pinned parts manifest hash mismatch")
    manifest=json.loads(raw)
    if (manifest.get('format')!='universe24-clock-evidence-parts-v1' or manifest.get('target_prefix')!=PREFIX
        or manifest.get('part_bytes')!=PART_BYTES or not 0<manifest.get('archive_bytes',0)<=MAX_ARCHIVE_BYTES
        or not 0<manifest.get('expanded_bytes',0)<=MAX_EXPANDED_BYTES):raise ValueError("Invalid archive contract")
    if digest((parts/'executed_builder.py').read_bytes())!=manifest['builder_sha256']:
        raise ValueError("Executed archive builder source mismatch")
    chunks=[]
    for i,item in enumerate(manifest['parts']):
        if item['file']!=f'part-{i:03d}.bin':raise ValueError("Invalid part order/path")
        data=(parts/item['file']).read_bytes()
        if len(data)!=item['bytes'] or len(data)>PART_BYTES or digest(data)!=item['sha256']:raise ValueError("Archive part mismatch")
        chunks.append(data)
    data=b''.join(chunks)
    if len(data)!=manifest['archive_bytes'] or digest(data)!=manifest['archive_sha256']:raise ValueError("Archive mismatch")
    with ZipFile(BytesIO(data)) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):raise ValueError("Duplicate archive name")
        inventory_raw=archive.read('inventory.json')
        if digest(inventory_raw)!=manifest['inventory_sha256']:raise ValueError("Inventory hash mismatch")
        inventory=json.loads(inventory_raw)
        if inventory.get('format')!='universe24-clock-evidence-inventory-v1':raise ValueError("Invalid inventory format")
        items=inventory['files'];paths=[r['path'] for r in items]
        physical_paths={item['path'] for item in items if 'gzip_source' not in item}
        if len(paths)!=len(set(paths)) or set(names)!=physical_paths|{'inventory.json'}:raise ValueError("Inventory/member mismatch")
        if len(items)!=manifest['expanded_files'] or sum(r['bytes'] for r in items)!=manifest['expanded_bytes']:raise ValueError("Inventory totals mismatch")
        by_path={item['path']:item for item in items}
        declared={item['path']:item for item in manifest.get('lossless_representations',[])}
        if len(declared)!=len(manifest.get('lossless_representations',[])):raise ValueError("Duplicate representations")
        actual={item['path'] for item in items if 'gzip_source' in item}
        if actual!=set(declared):raise ValueError("Representation inventory mismatch")
        for path in actual:
            item,entry=by_path[path],declared[path];source=item['gzip_source']
            if (source not in physical_paths or not evidence_path(source) or entry['gzip_path']!=source
                or entry['bytes']!=item['bytes'] or entry['sha256']!=item['sha256']
                or entry['gzip_sha256']!=by_path[source]['sha256']):raise ValueError("Invalid lossless representation")
        def content(item):
            source=item.get('gzip_source',item['path']);source_item=by_path[source]
            info=archive.getinfo(source)
            if stat.S_ISLNK(info.external_attr>>16) or info.is_dir() or info.file_size!=source_item['bytes']:raise ValueError("Invalid member type/size")
            raw=archive.read(source)
            if digest(raw)!=source_item['sha256']:raise ValueError("Evidence source mismatch")
            if 'gzip_source' in item:
                with gzip.GzipFile(fileobj=BytesIO(raw)) as handle:raw=handle.read(item['bytes']+1)
            if len(raw)!=item['bytes'] or digest(raw)!=item['sha256']:raise ValueError("Evidence member mismatch")
            return raw
        unchanged=0
        # Verify the complete plan and all existing files before any write.
        for item in items:
            target=destination(root,item['path']);content(item)
            if target.exists():
                if not target.is_file() or digest(target.read_bytes())!=item['sha256']:raise FileExistsError("Different existing evidence: "+item['path'])
                unchanged+=1
        restored=0
        if not check_only:
            for item in items:
                target=destination(root,item['path'])
                if target.exists():
                    if not target.is_file() or digest(target.read_bytes())!=item['sha256']:raise FileExistsError("Evidence changed during restore")
                    continue
                target.parent.mkdir(parents=True,exist_ok=True)
                with target.open('xb') as handle:handle.write(content(item))
                restored+=1
    return {"format":"universe24-clock-evidence-materialization-v1","archive_sha256":manifest['archive_sha256'],
        "check_only":check_only,"verified_files":len(items),"restored_files":restored,"unchanged_files":unchanged,"live_runtime_files_written":0}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='command',required=True)
    make=commands.add_parser('build');make.add_argument('--output',type=Path,required=True)
    restore=commands.add_parser('materialize');restore.add_argument('--check-only',action='store_true')
    args=parser.parse_args(argv)
    result=build(args.output) if args.command=='build' else materialize(check_only=args.check_only)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
