"""Passive independent inspection of the final split evidence transport."""
from pathlib import Path,PurePosixPath
import ast,hashlib,io,json,gzip,stat,time,zipfile
ROOT=Path('/workspace/scratch/1966445260ce/Universe24-clock-selection');P=ROOT/'research/clock_selection/artifacts/evidence_v1.parts';EXPECTED='8cb2881871ffc969ded5c0d0c7cd5408f84d97b99c50b1d189466f3a9a8becb1';H=lambda b:hashlib.sha256(b).hexdigest();start=time.process_time();raw=(P/'manifest.json').read_bytes();assert H(raw)==EXPECTED;m=json.loads(raw);chunks=[]
for i,item in enumerate(m['parts']):
 assert item['file']==f'part-{i:03d}.bin';b=(P/item['file']).read_bytes();assert len(b)==item['bytes'] and H(b)==item['sha256'];chunks.append(b)
b=b''.join(chunks);del chunks;assert len(b)==m['archive_bytes'] and H(b)==m['archive_sha256'];old=(P/'executed_builder.py').read_bytes();new=(ROOT/'research/clock_selection/archive.py').read_bytes();assert H(old)==m['builder_sha256']=='dd31cf1938738f7dc2ef6988a711213b34955a652b54c6d515f7453154ae0e3a';trees=[ast.parse(old),ast.parse(new)]
for tree in trees:
 for n in tree.body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PINNED_MANIFEST_SHA256' for t in n.targets):n.value=ast.Constant('NORMALIZED_PIN')
assert ast.dump(trees[0])==ast.dump(trees[1]);checks=[]
with zipfile.ZipFile(io.BytesIO(b)) as z:
 names=z.namelist();assert len(names)==len(set(names));iraw=z.read('inventory.json');assert H(iraw)==m['inventory_sha256'];items=json.loads(iraw)['files'];paths={i['path'] for i in items};assert len(paths)==len(items)==m['expanded_files'];assert sum(i['bytes'] for i in items)==m['expanded_bytes'];assert set(names)=={i['path'] for i in items if 'gzip_source' not in i}|{'inventory.json'}
 for item in items:
  p=PurePosixPath(item['path']);assert not p.is_absolute() and '..' not in p.parts and p.parts[:3]==('research','clock_selection','evidence');source=item.get('gzip_source',item['path']);info=z.getinfo(source);assert not stat.S_ISLNK(info.external_attr>>16) and not info.is_dir();sha=hashlib.sha256();n=0
  with z.open(source) as fh:
   stream=gzip.GzipFile(fileobj=fh) if 'gzip_source' in item else fh
   while True:
    block=stream.read(min(1024*1024,item['bytes']+1-n))
    if not block:break
    n+=len(block);sha.update(block);assert n<=item['bytes']
  assert n==item['bytes'] and sha.hexdigest()==item['sha256'];assert H((ROOT/item['path']).read_bytes())==item['sha256']
  if 'gzip_source' in item:checks.append(dict(path=item['path'],bytes=n,sha256=sha.hexdigest(),source=source,exact_source_and_decoded_match=True))
 required=['write_probe_v1/abort.json','structure_v1/failure.json','structure_v1_corrected/result.json','structure_v1_analysis/result.json','two_outlet_v1/interruption_receipt.json','two_outlet_v1_retry01/timing_scope.json','coherent_wave_v1/budget_receipt.json','independent_audit/activation_v1_schema_failure.json','independent_audit/carrier_memory_v1.json','independent_audit/model_contract_final_checkpoint.json','document_alignment/receipt.json']
 for suffix in required:assert 'research/clock_selection/evidence/'+suffix in paths,suffix
 assert not any('tmpyy2c1ks1' in path for path in paths)
out=dict(passed=True,manifest_sha256=EXPECTED,archive_sha256=m['archive_sha256'],part_count=len(m['parts']),transport_bytes=m['archive_bytes'],decoded_files=len(items),decoded_bytes=m['expanded_bytes'],all_declared_contents_independently_hashed=True,all_contents_match_live_frozen_evidence=True,lossless_original_audit_checks=checks,required_failure_and_source_receipts_present=required,source_delta_only_manifest_pin=True,unrelated_temporary_directory_excluded=True,CI_review='Pinned-source restoration then check-only is performed before the established test/reproducibility job. Research arithmetic and optional solver are installed. Configured CI is not a completed remote CI result.',new_native_trajectories=0,scope='Independent archive byte/content and scope review. Fresh-checkout materialization and test result review are separate integration steps.',reviewer_source_sha256=H(Path(__file__).read_bytes()),cpu_seconds=time.process_time()-start)
p=ROOT.parent/'clock_transport_independent_review.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('required_failure_and_source_receipts_present','lossless_original_audit_checks')}))
