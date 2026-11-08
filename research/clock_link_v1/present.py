"""Record these prepared assemblies with the unchanged generic Presenter."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from research.components import BoardSpec, finalize
from research.presenter.export import capture, bundle, write_bundle
from research.presenter.build import build
from research.clock_link_v1.components import assemble_clock_link, clock_link_parts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    examples=[('canonical','Clock link | four round trips',{},168),
              ('delayed','Control | delayed source',{'delay':1},169),
              ('source-off','Control | source absent',{'source_present':False},1),
              ('long-guide','Control | endpoint beyond horizon',{'terminated':False},168)]
    recordings=[]
    for identifier,title,parameters,horizon in examples:
        prepared=assemble_clock_link(**parameters)
        recordings.append(capture(prepared.engine,prepared.initial,horizon,
            id=identifier,title=title,description='Prepared phase-front link under fixed +++ Rule3. Cyclic records; no physical light, time or gravity claim.',
            view={'position':[4,4,4],'channel':0},max_seconds=120))
    parts=clock_link_parts(distance=20,name_prefix='a-')+clock_link_parts(
        distance=28,origin=(48,16,48),delay=1,orientation=4,name_prefix='b-')
    prepared=finalize(BoardSpec(389),parts)
    recordings.append(capture(prepared.engine,prepared.initial,233,
        id='two-links',title='Composition | two separated clock links',
        description='Two properly rotated preparations on one board. Demonstrates coexistence, not inter-link interaction. The second source is (48,16,48), channel4.',
        view={'position':[48,16,48],'channel':4},max_seconds=120))
    write_bundle(args.output/'experiments.json',bundle(recordings,title='Autonomous guided clock links'))
    html,manifest=build(args.output/'experiments.json',args.output/'The_Presenter.html')
    print(json.dumps({'html':str(html),'manifest':str(manifest),
                      'experiments':len(recordings),
                      'complete_states':sum(len(e['frames']) for e in recordings),
                      'actual_browser_execution_checked':False},indent=2))


if __name__=='__main__':
    main()
