"""Run the Universe24 Einstein event board through integer Rule3.

python -m universe24 --steps 1 --out runs/universe24
All physical updates are computed inside Engine.step. No RHS callback feeds
the Engine. Reference/readout arithmetic is never used to advance the state.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import argparse
from fractions import Fraction
import gzip
import hashlib
import json
import time
import numpy as np
from universe24.core import Engine, State
from universe24.layers.adm import compile_adm, FIELDS, PAIRS
from universe24.prepare.einstein import homogeneous_scalar, gauge_wave, inhomogeneous_scalar
from universe24.observe.simplex_metric import signed_intervals, metric_from_intervals
from universe24.observe.event_board import export_event_board


def exact_fraction(value):
    return {'numerator_hex':format(value.numerator,'x'),'denominator_hex':format(value.denominator,'x')}


def run(program, integer_data, parameters, out=None, verify_arithmetic=True):
    L=next(iter(integer_data.values())).shape[0]
    names=tuple(parameters.get('fields',FIELDS))
    if parameters.get('lapse')=='geodesic' and not np.all(integer_data['alpha']==integer_data['alpha'].flat[0]):
        raise ValueError('geodesic slicing requires a spatially uniform initial lapse')
    if parameters.get('dark_matter') and np.any(integer_data['rho_dark']<0):
        raise ValueError('dark rest density must be nonnegative')
    seed=program.prepare(L,integer_data)
    wave=None
    if getattr(program,'causal_wave',False):
        from universe24.prepare.causal_wave import default_wave_info
        from universe24.observe.causal_wave import wave_frame
        wave={'preparation':default_wave_info(L),
              'frames':[wave_frame(seed,program.tensor,0,namespace='causal_wave.wave')],
              'first_C2_microtick':None,'C2_records':0,
              'meaning':'Optional causal component on the same Engine board; audit clicks, no coupling to Einstein stress-energy.',
              'cone':'Periodic face-edge computational bound from complete initial a,b support, not a metric-null geodesic.'}
    engine=Engine(program.tensor)
    state=seed
    started=time.monotonic()
    stream=None
    click_stream=None
    component_stream=None
    component_summary={}
    official_count=0
    if out is not None:
        out=Path(out);out.mkdir(parents=True,exist_ok=True)
        stream=gzip.open(out/'full_trace.jsonl.gz','wt')
        click_stream=gzip.open(out/'official_events.jsonl.gz','wt')
        click_stream.write(json.dumps({'format':'Universe24-official-events-v1',
            'definition':'Engine official changed-triple clicks of retained physical numerator/denominator registers',
            'columns':['microtick','gear','node','quotient_hex','kind'],
            'tensor_fingerprint':program.tensor.fingerprint})+'\n')
        if hasattr(program,'assembly'):
            component_stream=gzip.open(out/'component_events.jsonl.gz','wt')
            component_stream.write(json.dumps({'format':'Universe24-component-events-v1',
                'meaning':'Passive computational messages and audit clicks; not an additional gravitational source',
                'tensor_fingerprint':program.tensor.fingerprint})+'\n')
        stream.write(json.dumps({'format':'Rule3-full-triples-delta-v2','seed':seed.to_dict(),
                                 'tensor_fingerprint':program.tensor.fingerprint,
                                 'rule':'after.a=before.b; explicit b and r deltas below, hex integers'})+'\n')
    try:
        for tick in range(1,program.ticks+1):
            after=engine.step(state)
            # Arithmetic gates preserve remainders; independent message receivers
            # may emit C1/C2. Never impose the arithmetic identity on all owners.
            lo,hi=program.assembly.spans['einstein'] if hasattr(program,'assembly') else (0,program.tensor.G)
            assert np.array_equal(after.r[lo:hi],seed.r[lo:hi])
            all_clicks=engine.clicks(state,after,tick) if click_stream or hasattr(program,'assembly') else None
            if wave is not None:
                memory=program.assembly.channel('causal_wave','wave.memory')
                c2=int(np.count_nonzero((all_clicks.gear==memory)&(all_clicks.kind==2)))
                wave['C2_records']+=c2
                if c2 and wave['first_C2_microtick'] is None:
                    wave['first_C2_microtick']=tick
                wave['frames'].append(wave_frame(after,program.tensor,tick,all_clicks,namespace='causal_wave.wave'))
            if click_stream:
                clicks=all_clicks.select('official')
                official_count+=len(clicks)
                for gear,node,quotient,kind in zip(clicks.gear,clicks.node,clicks.quotient,clicks.kind):
                    click_stream.write(json.dumps([tick,int(gear),int(node),format(int(quotient),'x'),int(kind)],separators=(',',':'))+'\n')
            if stream:
                gears,nodes=np.nonzero(after.b!=state.b)
                changes=[[int(g),int(n),format(int(after.b[g,n]),'x')] for g,n in zip(gears,nodes)]
                rg,rn=np.nonzero(after.r!=state.r)
                remainders=[[int(g),int(n),format(int(after.r[g,n]),'x')] for g,n in zip(rg,rn)]
                stream.write(json.dumps({'tick':tick,'b':changes,'r':remainders},separators=(',',':'))+'\n')
            if hasattr(program,'assembly'):
                observed=program.observe_components(state,after,tick,all_clicks)
                for name,row in observed['components'].items():
                    counts=component_summary.setdefault(name,{'changed_triple_clicks':0,'C0':0,'C1':0,'C2':0})
                    counts['changed_triple_clicks']+=row['changed_triple_clicks']
                    for k,v in row['classes'].items():counts['C'+k]+=v
                if 'messages' in observed:
                    component_summary['communication']['message_records']=component_summary['communication'].get('message_records',0)+len(observed['messages'])
                if component_stream:component_stream.write(json.dumps(observed,separators=(',',':'))+'\n')
            state=after
    finally:
        if stream:stream.close()
        if click_stream:click_stream.close()
        if component_stream:component_stream.close()
    if verify_arithmetic:
        expected=program.evaluate_integer_dag(seed)
        for wire,value in expected.items():
            assert np.all(state.b[program.tensor.gear_index(program.names[wire])]==value), wire
    assert engine.rewind(state,program.ticks).same_as(seed)
    samples=[]
    coordinate_steps=[Fraction(parameters['dt'])]+[Fraction(parameters['dx'])]*3
    tangent_basis=[[coordinate_steps[i] if i==j else Fraction(0) for j in range(4)] for i in range(4)]
    for step in range(parameters['steps']+1):
        field_values={name:[program.read(state,f'{step}.{name}',node) for node in range(L**3)] for name in names}
        constraints={name:[program.read(state,f'{step}.constraint.{name}',node) for node in range(L**3)]
                     for name in ('H','M0','M1','M2')}
        evolution_residual=Fraction(0)
        if step < parameters['steps']:
            h=Fraction(parameters['dt'])
            for name in names:
                for node in range(L**3):
                    residual=(program.read(state,f'{step+1}.{name}',node)-field_values[name][node]
                              -h*program.read(state,f'{step}.update_rhs.{name}',node))
                    evolution_residual=max(evolution_residual,abs(residual))
            assert evolution_residual==0
            if parameters['method']=='midpoint':
                assert all(program.read(state,f'{step}.midpoint.{name}',node)>0
                           for name in ('minor1','minor2','minor3','alpha') for node in range(L**3))
        matrices=[]
        for node in range(L**3):
            metric=[[program.read(state,f'{step}.metric.{min(i,j)}{max(i,j)}',node) for j in range(4)] for i in range(4)]
            lengths=signed_intervals(metric,tangent_basis)
            reconstructed=metric_from_intervals(lengths,tangent_basis)
            assert reconstructed.tolist()==metric
            assert field_values['g00'][node]>0
            assert field_values['g00'][node]*field_values['g11'][node]-field_values['g01'][node]**2>0
            assert program.read(state,f'{step}.det_gamma',node)>0 and field_values['alpha'][node]>0
            if parameters.get('dark_matter'):assert field_values['rho_dark'][node]>=0
            if node==0:
                matrices={'metric':[[exact_fraction(v) for v in row] for row in metric],
                          'signed_squared_tangent_links':{f'{i}-{j}':exact_fraction(Fraction(v)) for (i,j),v in lengths.items()}}
        samples.append({'step':step,'time':str(step*Fraction(parameters['dt'])),
                        'field_node0':{name:float(values[0]) for name,values in field_values.items()},
                        'field_ranges':{name:[min(map(float,values)),max(map(float,values))] for name,values in field_values.items()},
                        'constraint_max':{name:float(max(map(abs,values))) for name,values in constraints.items()},
                        'constraint_node0_exact':{name:exact_fraction(values[0]) for name,values in constraints.items()},
                        'discrete_evolution_max_residual':str(evolution_residual) if step<parameters['steps'] else None,
                        'geometry_node0_exact':matrices})
        if out:
            # Physical states use exact integer pairs, without decimal digit limits or pickle.
            with gzip.open(out/f'physical_{step}.json.gz','wt') as file:
                json.dump({name:[exact_fraction(v) for v in values] for name,values in field_values.items()},file)
            spatial_links={}
            angles={}
            for axis in range(3):
                offset=tuple(1 if j==axis else 0 for j in range(3))
                neighbors=state.lattice.shift_index(offset)
                values=field_values[f'g{axis}{axis}']
                spatial_links[str(axis)]=[exact_fraction(Fraction(parameters['dx'])**2*(values[node]+values[int(neighbors[node])])/2)
                                          for node in range(L**3)]
            for i,j in ((0,1),(0,2),(1,2)):
                values=[]
                for node in range(L**3):
                    cross=field_values[f'g{i}{j}'][node]
                    values.append({'cosine_sign':1 if cross>0 else (-1 if cross<0 else 0),
                                   'cosine_squared':exact_fraction(cross**2/(field_values[f'g{i}{i}'][node]*field_values[f'g{j}{j}'][node]))})
                angles[f'{i}{j}']=values
            with gzip.open(out/f'geometry_{step}.json.gz','wt') as file:
                json.dump({'shared_spatial_edge_squared_lengths':spatial_links,'local_angle_data':angles,
                           'definition':'unique edge uses the average endpoint metric; finite-length approximation, not an exact geodesic distance'},file)
    result={'parameters':dict(parameters,L=L),'physical_model':'nonlinear Einstein + '+('complex' if parameters.get('complex_matter') else 'real')+' Klein-Gordon'+(' + normal-comoving pressureless dark matter' if parameters.get('dark_matter') else '')+'; prescribed static shift',
            'runtime':'unchanged Rule3 Engine only; compiled finite-horizon rational arithmetic',
            'gears':program.tensor.G,'monomials':len(program.tensor.monomials),'rank':program.tensor.rank,
            'engine_ticks':program.ticks,'clock_period':program.period,
            'physical_snapshot_ready_ticks':{
                str(step):max((program.ready[term.wire] for name in names
                    for term in (program.outputs[f'{step}.{name}'].num,program.outputs[f'{step}.{name}'].den)
                    if term.wire is not None),default=0) for step in range(parameters['steps']+1)},
            'all_arithmetic_registers_verified':verify_arithmetic,'complete_rewind_exact':True,
            'no_support_violations':not program.tensor.support_violations(),
            'arbitrary_precision_used':engine.stats['pyint_steps']>0,
            'tensor_fingerprint':program.tensor.fingerprint,'engine_stats':engine.stats,
            'official_event_records':official_count if out else None,
            'event_chart':{'label':'(physical step, cube node)','coordinates':'(step*dt, ix*dx, iy*dx, iz*dx)',
                           'tangent_basis_diagonal':list(map(str,coordinate_steps)),
                           'meaning':'physical mesh events have an explicit metric readout; raw arithmetic microtick clicks are not identified with all continuum events'},
            'maximum_integer_bits':max(abs(int(v)).bit_length() for v in state.b.ravel()),
            'seconds':time.monotonic()-started,'samples':samples,
            'limits':['finite compiled horizon; retained workspace grows with requested steps',
                      'constraints propagate with discretization error; no claim of exact continuum GR',
                      'prototype ADM integrator; long-time stability and strong-field production use not validated',
                      'matter/antimatter is a classical complex scalar with opposite U(1) charge, not a quantum Standard Model or annihilation simulator',
                      'dark matter is irrotational single-stream dust before caustics; no particle identity or multistream halo model']}
    if wave is not None:
        result['causal_wave']={k:v for k,v in wave.items() if k!='frames'}
    if out:
        if hasattr(program,'assembly'):
            result['channel_allocation']=program.channel_manifest(include_channels=False)
            result['component_observations']=component_summary
            (out/'channels.json').write_text(json.dumps(program.channel_manifest(),indent=2)+'\n')
        result['event_board']=export_event_board(program,state,parameters,out,causal_wave=wave)
        (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
        (out/'tensor.json').write_text(json.dumps(program.tensor.to_dict(),separators=(',',':'))+'\n')
    return result


def replay_trace(path):
    """Recover every complete (a,b,r) snapshot from a lossless delta journal."""
    with gzip.open(path,'rt') as stream:
        header=json.loads(next(stream));state=State.from_dict(header['seed'])
        if header['format'] not in ('Rule3-full-triples-delta-v1','Rule3-full-triples-delta-v2'):
            raise ValueError('unknown trace format')
        yield state
        for expected_tick,line in enumerate(stream,1):
            record=json.loads(line)
            if record['tick']!=expected_tick:raise ValueError('missing/reordered tick')
            b=state.b.astype(object).copy()
            for gear,node,value in record['b']:b[gear,node]=int(value,16)
            r=state.r.copy()
            for gear,node,value in record.get('r',[]):r[gear,node]=int(value,16)
            state=State(state.L,state.b,b,r)
            yield state


def main(argv=None):
    source_hashes={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in (
        Path(__file__),ROOT/'universe24/layers/adm.py',ROOT/'universe24/algebra/integer_circuit.py',
        ROOT/'universe24/prepare/einstein.py',ROOT/'universe24/observe/event_board.py',ROOT/'universe24/core/engine.py',
        ROOT/'universe24/observe/metric_clocks.py',
        ROOT/'universe24/core/channels.py',ROOT/'universe24/layers/universe.py',
        ROOT/'universe24/layers/communication.py',ROOT/'universe24/layers/reference_model.py',
        ROOT/'universe24/prepare/communication.py',ROOT/'universe24/prepare/reference_model.py')}
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',choices=('universe','matter','antimatter','scalar','massless','gauge','inhomogeneous','dark'),default='universe')
    parser.add_argument('--steps',type=int,default=1)
    parser.add_argument('--L',type=int,default=3)
    parser.add_argument('--dt',default='1/64')
    parser.add_argument('--method',choices=('euler','midpoint'),default='euler')
    parser.add_argument('--out',type=Path,default=Path('runs/universe24'))
    parser.add_argument('--rewind',action='store_true',help='Exact rewind is always verified; retained for explicit run scripts.')
    parser.add_argument('--no-communication',action='store_true',help='Run only the Einstein physical component.')
    parser.add_argument('--probe-experiment',action='store_true',help='Add the independent 26-channel test chart (L>=5); not a validated physical clock.')
    parser.add_argument('--causal-wave',action='store_true',help='Add a local wave, C2 memory and response field with a computational cone display.')
    parser.add_argument('--max-channels',type=int,help='Reject construction above this per-node channel budget; never truncate fields.')
    parser.add_argument('--plan',action='store_true',help='Export channel allocation before running any Engine updates.')
    args=parser.parse_args(argv)
    if args.probe_experiment and (args.L<5 or args.L%2!=1):
        parser.error('--probe-experiment requires odd --L >= 5')
    info={}
    complex_matter=args.case in ('universe','matter','antimatter')
    dark_matter=args.case in ('universe','dark')
    if args.case in ('inhomogeneous','dark','universe','matter','antimatter'):
        data,scale,info=inhomogeneous_scalar(args.L,dark_matter=dark_matter,complex_matter=complex_matter);mass=1
        if args.case in ('matter','antimatter'):
            data['Pi_chi']=(1 if args.case=='matter' else -1)*np.abs(data['Pi_chi'])
            info['charge_preparation']=args.case
    elif args.case=='gauge':
        scale=1<<24;data=gauge_wave(args.L,scale);mass=0
    else:
        scale=4096;mass=0 if args.case=='massless' else 1
        data=homogeneous_scalar(args.L,scale,mass)
    program,parameters=compile_adm(steps=args.steps,dt=Fraction(args.dt),dx=Fraction(1,args.L),scale=scale,
                                   mass_squared=mass,method=args.method,dark_matter=dark_matter,complex_matter=complex_matter)
    from universe24.layers.universe import UniverseProgram
    program=UniverseProgram(program,parameters,communication=not args.no_communication,
                            probe_experiment=args.probe_experiment,causal_wave=args.causal_wave,max_channels=args.max_channels)
    if args.plan:
        args.out.mkdir(parents=True,exist_ok=True)
        (args.out/'channels.json').write_text(json.dumps(program.channel_manifest(),indent=2)+'\n')
        print(json.dumps(program.assembly.manifest(include_channels=False),indent=2))
        return
    print(json.dumps({'phase':'compiled','gears':program.tensor.G,'ticks':program.ticks}),flush=True)
    if args.causal_wave:
        for name in ('layers','prepare','observe'):
            path=ROOT/'universe24'/name/'causal_wave.py'
            source_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    report=run(program,data,parameters,args.out)
    report['initial_data']=info
    report['source_sha256_at_start']=source_hashes
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('gears','monomials','engine_ticks','complete_rewind_exact','maximum_integer_bits','seconds')},indent=2))
    print(json.dumps([{'step':s['step'],'constraints':s['constraint_max']} for s in report['samples']],indent=2))


if __name__=='__main__':main()
