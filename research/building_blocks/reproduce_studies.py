"""Regenerate all bounded studies and compare scientific data, including failures."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys

from research.reproducibility.bundle import read_json

ROOT=Path(__file__).resolve().parents[2]
STUDIES=(
    ('algebra_checks','algebra_results.json',[('python',),('checkout_commit_at_execution',)]),
    ('signal_study','signal_results.json',[('python',),('runtime_cpu_seconds',)]),
    ('component_study','component_results.json',[('python',),('summary','cpu_seconds'),('summary','wall_seconds')]),
    ('structure_study','structure_results.json',[('python',),('checkout_commit',),('working_tree_dirty',),('cpu_seconds',)]),
    ('structure_confirm','structure_results_v2.json',[('python',),('checkout_commit',),('working_tree_dirty',),('cpu_seconds',)]),
)


def strip_metadata(data,paths):
    result=copy.deepcopy(data)
    for path in paths:
        target=result
        for key in path[:-1]: target=target[key]
        del target[path[-1]]
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    results=[]
    for module,filename,excluded in STUDIES:
        destination=args.output/filename
        process=subprocess.run([sys.executable,'-m','research.building_blocks.'+module,'--output',str(destination.resolve())],cwd=ROOT,capture_output=True,text=True,timeout=180)
        (args.output/(module+'.stdout.txt')).write_text(process.stdout)
        (args.output/(module+'.stderr.txt')).write_text(process.stderr)
        if process.returncode:
            raise RuntimeError(f'{module} execution failed with {process.returncode}; see retained logs')
        expected=read_json(ROOT/'research/building_blocks'/filename)
        actual=read_json(destination)
        equal=strip_metadata(expected,excluded)==strip_metadata(actual,excluded)
        results.append({'study':module,'scientific_fields_equal':equal,'excluded_metadata_paths':['/'.join(p) for p in excluded]})
        if not equal: raise AssertionError(f'{module} differs from retained scientific evidence')
    result={'reproduced':True,'studies':results,'meaning':'Exact scientific reproduction, including rejected hypotheses; not universal acceptance or physical validation.'}
    (args.output/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
