"""Validate the exact staged tree using only its declared archives and dependencies."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time

HERE=Path(__file__).resolve().parent


def main():
    setup=json.loads((HERE/'staged_checkout.json').read_text())
    fresh=Path(setup['fresh_checkout'])
    env=dict(os.environ,PYTHONPATH='/workspace/scratch/1966445260ce/clock-python-deps')
    scratch=HERE/'fresh-test-temporary';scratch.mkdir(exist_ok=False)
    env.update(TMPDIR=str(scratch),TMP=str(scratch),TEMP=str(scratch))
    commands=[
        ('environment',[sys.executable,'-c','import sys,mpmath,z3,json; print(json.dumps({"python":sys.version,"mpmath":mpmath.__version__,"z3":z3.get_version_string()}))']),
        ('baseline_restore',[sys.executable,'-m','research.experiments.materialize_evidence']),
        ('baseline_check',[sys.executable,'-m','research.experiments.materialize_evidence','--check-only']),
        ('research_restore',[sys.executable,'-m','research.clock_selection.archive','materialize']),
        ('research_check',[sys.executable,'-m','research.clock_selection.archive','materialize','--check-only']),
        ('full_tests',[sys.executable,'-m','unittest','discover','-s','tests','-v']),
        ('reference_impulse',[sys.executable,'-m','universe24','--config','examples/impulse.json','--audit']),
        ('reference_signed_impulse',[sys.executable,'-m','universe24','--config','examples/signed_impulse.json','--audit']),
        ('record_index',[sys.executable,'-m','research.clock_selection.run','verify-index','--index','research/clock_selection/evidence/index_final/index.json'])]
    receipt={**setup,'started_utc':datetime.now(timezone.utc).isoformat(),'dependency_directory':env['PYTHONPATH'],
        'scope':'Fresh staged source tree, only declared evidence archives restored, full tests and required reference CLI audits. No new research study.',
        'commands':[],'complete':False,'passed':False}
    output=HERE/'fresh_validation.json'
    if output.exists():raise FileExistsError(output)
    for name,command in commands:
        start=time.monotonic();p=subprocess.run(command,cwd=fresh,env=env,capture_output=True,timeout=900)
        logs={}
        for suffix,data in [('stdout',p.stdout),('stderr',p.stderr)]:
            path=HERE/f'fresh_{name}.{suffix}.txt';path.write_bytes(data)
            logs[suffix]={'file':path.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        row={'name':name,'command':command,'returncode':p.returncode,'wall_seconds':time.monotonic()-start,'logs':logs}
        receipt['commands'].append(row);output.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'check':name,'returncode':p.returncode,'wall_seconds':row['wall_seconds']}),flush=True)
        if p.returncode:raise RuntimeError('Fresh validation failed: '+name)
    protected=['universe24','research/reference','research/components','research/presenter','research/experiments','research/staged_blocks']
    diff=subprocess.check_output(['git','diff','--name-only',setup['baseline_commit'],'--',*protected],cwd=fresh,text=True)
    assert not diff
    receipt.update(complete=True,passed=True,protected_runtime_diff=[],finished_utc=datetime.now(timezone.utc).isoformat())
    output.write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':main()
