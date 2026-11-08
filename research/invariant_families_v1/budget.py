"""Measure and bound the complete dedicated invariant-family CLI workflow."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]

def run(output):
    output=Path(output).resolve()
    if output.exists():raise FileExistsError(output)
    protocol=json.loads((HERE/'protocol.json').read_text());budget=protocol['budget']
    before=resource.getrusage(resource.RUSAGE_CHILDREN);wall=time.monotonic();timeout=False
    def limits():resource.setrlimit(resource.RLIMIT_CPU,(budget['child_cpu_soft_limit'],budget['child_cpu_hard_limit']))
    try:
        completed=subprocess.run([sys.executable,'-u','-m','research.invariant_families_v1.run','--output',str(output)],
                                 cwd=ROOT,preexec_fn=limits,timeout=budget['max_wall_seconds'],check=False)
        returncode=completed.returncode
    except subprocess.TimeoutExpired:
        timeout=True;returncode=None
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    child_cpu=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime)
    output.mkdir(parents=True,exist_ok=True)
    hashes={str(path.relative_to(output)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(output.rglob('*')) if path.is_file()}
    (output/'archive_hashes.json').write_text(json.dumps(hashes,sort_keys=True,indent=2)+'\n')
    total_cpu=child_cpu+time.process_time();elapsed=time.monotonic()-wall
    total_bytes=sum(path.stat().st_size for path in output.rglob('*') if path.is_file())
    result_path=output/'result.json';result=json.loads(result_path.read_text()) if result_path.exists() else {}
    receipt={'scope':'Entire dedicated wrapper process CPU plus child user/system CPU, including imports, preflight, capture, inverses, analysis, compression, export and archive hashing.',
             'child_cpu_seconds':child_cpu,'wrapper_cpu_seconds_at_receipt':time.process_time(),'whole_workflow_cpu_seconds':total_cpu,
             'whole_workflow_wall_seconds':elapsed,'returncode':returncode,'timeout':timeout,
             'child_completed_cases':result.get('completed_cases',0),'child_status':result.get('status','no_complete_result'),
             'bytes_before_receipt':total_bytes,'cpu_budget_seconds':budget['max_cpu_seconds'],'wall_budget_seconds':budget['max_wall_seconds'],
             'budget_passed':total_cpu<=budget['max_cpu_seconds'] and elapsed<=budget['max_wall_seconds'] and total_bytes+4096<=budget['max_recorded_bytes'],
             'all_work_completed':returncode==0 and result.get('status')=='completed',
             'protocol_sha256':hashlib.sha256((HERE/'protocol.json').read_bytes()).hexdigest()}
    (output/'outer_budget.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt,sort_keys=True),flush=True)
    return receipt

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();run(args.output)

if __name__=='__main__':main()
