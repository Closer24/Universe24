"""Bound and measure the full dedicated invariant-overlap producer workflow."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = ROOT/'research/clock_selection/invariant_overlap_protocol.json'


def run(output):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError(output)
    p = json.loads(PROTOCOL.read_text())
    budget = p['budget']
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall = time.monotonic()
    timeout = False
    def limits():
        resource.setrlimit(resource.RLIMIT_CPU, (18, 19))
    try:
        child = subprocess.run([sys.executable, '-u', '-m',
            'research.invariant_families_v1.overlap', '--output', str(output)],
            cwd=ROOT, preexec_fn=limits, timeout=budget['max_wall_seconds']-10, check=False)
        returncode = child.returncode
    except subprocess.TimeoutExpired:
        timeout = True
        returncode = None
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    child_cpu = after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime
    output.mkdir(parents=True, exist_ok=True)
    hashes = {str(f.relative_to(output)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in sorted(output.rglob('*')) if f.is_file()}
    (output/'archive_hashes.json').write_text(json.dumps(hashes, sort_keys=True, indent=2)+'\n')
    result_path = output/'result.json'
    result = json.loads(result_path.read_text()) if result_path.exists() else {}
    used_bytes = sum(f.stat().st_size for f in output.rglob('*') if f.is_file())
    whole_cpu = child_cpu+time.process_time()
    elapsed = time.monotonic()-wall
    receipt = {'scope': 'Dedicated wrapper CPU plus complete child user/system CPU, including imports, static preflight, capture, inverse checks, observations, compression, Presenter export and source/archive hashing.',
        'whole_producer_cpu_seconds': whole_cpu, 'child_cpu_seconds': child_cpu,
        'wrapper_cpu_seconds_at_receipt': time.process_time(), 'wall_seconds': elapsed,
        'returncode': returncode, 'timeout': timeout, 'bytes_before_receipt': used_bytes,
        'producer_cpu_budget_seconds': budget['producer_cpu_seconds'],
        'separate_independent_audit_cpu_budget_seconds': budget['independent_audit_cpu_seconds'],
        'whole_study_cpu_budget_seconds': budget['max_total_study_cpu_seconds'],
        'whole_study_cpu_certified': False, 'independent_audit_pending': True,
        'producer_budget_passed': whole_cpu <= budget['producer_cpu_seconds']
            and elapsed <= budget['max_wall_seconds'] and used_bytes+8192 <= budget['max_recorded_bytes'],
        'all_native_work_completed': returncode == 0 and result.get('status') == 'completed',
        'completed_cases': result.get('completed_cases', 0),
        'protocol_sha256': hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()}
    (output/'outer_budget.json').write_text(json.dumps(receipt, sort_keys=True, indent=2)+'\n')
    print(json.dumps(receipt, sort_keys=True), flush=True)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    run(args.output)


if __name__ == '__main__':
    main()
