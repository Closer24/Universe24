"""Exact finite observations of closed-board signal-clock preparations.

Every forward state is obtained from Engine.advance. All observations below
read completed immutable snapshots; they never supply an evolution decision.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import time

from universe24.experiments.config import checkpoint_data
from universe24.observation.clicks import classify
from .preparation import prepare


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        handle.write(canonical(value)+'\n')


def run_case(case, source_mask, *, deadline_cpu, max_cells=20000,
             audit=False, output=None, prepare_function=prepare):
    # The optional data-only factory is called once, before the first update.
    # It cannot supply callbacks or intervene in the evolution loop.
    engine,initial,locations = prepare_function(case,source_mask)
    state = initial
    rows=[]; checkpoints=[]; inverse_ok=True; stationary=True
    maximum=0; margin=case['side']; events=[]
    detector=locations['detector']
    previous_symbol=None; previous_values=None; arithmetic_events=[]
    initial_margin=min(min(p,case['side']-1-p) for address in initial.cells for p in address[:3])
    for t in range(case['steps']+1):
        if time.process_time() > deadline_cpu:
            raise TimeoutError('Declared computation budget exhausted')
        if len(state.cells)>max_cells:
            raise MemoryError('Declared retained-channel bound exceeded')
        maximum=max(maximum,len(state.cells))
        stationary &= state==initial
        if state.cells:
            margin=min(margin,min(min(p,case['side']-1-p)
                                  for address in state.cells for p in address[:3]))
        values=[state.at(address) for address in detector]
        symbol=[v.r for v in values]
        sums=engine.input_sums(state)
        inputs=[sums.get(address,0) for address in detector]
        # Six source-counter terms are retained separately from the sum.
        terms=[]
        for address in detector:
            terms.append([{'direction':d,
                'address':list(state.cube.adjacent(address,d,engine.coupling.ports[d][address[3]])),
                'weight':engine.coupling.weights[d][address[3]],
                'b':state.at(state.cube.adjacent(address,d,engine.coupling.ports[d][address[3]])).b}
                for d in range(6)])
        if previous_symbol is not None and symbol != previous_symbol:
            events.append(t)
        arithmetic=[]
        if previous_values is not None:
            for address,old,new in zip(detector,previous_values,values):
                classified=classify(old,new)
                if classified is not None:
                    kind,quotient=classified
                    event={'step':t,'address':list(address),'kind':kind,'quotient':quotient}
                    arithmetic.append(event); arithmetic_events.append(event)
        rows.append({'step':t,'detector':[list(v) for v in values],
                     'memory':symbol,'next_input':inputs,'six_inputs':terms,
                     'arithmetic_events':arithmetic})
        previous_symbol=symbol;previous_values=values
        if output is not None:
            checkpoints.append(checkpoint_data(state,engine,t))
        if t<case['steps']:
            new=engine.advance(state)
            if audit:
                inverse_ok &= engine.rewind(new)==state
            state=new
    if audit:
        rewound=state
        for _ in range(case['steps']):
            if time.process_time()>deadline_cpu:
                raise TimeoutError('Declared computation budget exhausted in rewind')
            rewound=engine.rewind(rewound)
        full_rewind=rewound==initial
    else:
        full_rewind=None
    result={'id':case['id'],'preparation':case,'source_mask':list(source_mask),
            'locations':{k:[list(a) for a in v] if k!='origin' else list(v)
                         for k,v in locations.items()},
            'initial_sha256':digest(checkpoint_data(initial,engine,0)),
            'final_sha256':digest(checkpoint_data(state,engine,case['steps'])),
            'coupling_fingerprint':engine.coupling.fingerprint,
            'record_event_times':events,'arithmetic_events':arithmetic_events,
            'trace':rows,'entire_board_stationary':stationary,
            'max_stored_channels':maximum,'minimum_boundary_margin':margin,
            'initial_boundary_margin':initial_margin,
            'inverse_audited':audit,'all_one_step_inverses':inverse_ok if audit else None,
            'complete_rewind':full_rewind}
    if output is not None:
        output=Path(output);output.mkdir(parents=True,exist_ok=False)
        with (output/'states.jsonl').open('x',encoding='utf-8') as handle:
            for cp in checkpoints:
                handle.write(canonical(cp)+'\n')
        write_json(output/'initial.json',checkpoints[0])
        write_json(output/'final.json',checkpoints[-1])
        write_json(output/'result.json',result)
    return result


def waiting_verdict(result, expected_windows, minimum_silence=4):
    """Fixed remainder-event criterion; never suppress an inconvenient edge."""
    clicks=result['record_event_times']; trace=result['trace']
    count=len(expected_windows)
    correct_count=len(clicks)==count
    expected_arrivals=correct_count and all(lo<=t<=hi for t,(lo,hi)
                                          in zip(clicks,expected_windows))
    symbols=[trace[0]['memory']]+[trace[t]['memory'] for t in clicks]
    distinct=correct_count and len({tuple(s) for s in symbols})==count+1
    silence=correct_count and (not clicks or
        (clicks[0]>=minimum_silence and
         all(b-a>=minimum_silence+1 for a,b in zip(clicks,clicks[1:])) and
         len(trace)-1-clicks[-1]>=minimum_silence))
    # Fixed minimum quiet windows, not a posthoc interval around any edge.
    quiet_steps=set()
    if clicks:
        quiet_steps.update(range(clicks[0]-minimum_silence,clicks[0]-1))
        for t in clicks:
            quiet_steps.update(range(t,t+minimum_silence))
    quiet_complete=all(0<=t<len(trace)-1 for t in quiet_steps)
    zero_between=quiet_complete and all(trace[t]['next_input']==[0,0] for t in quiet_steps)
    incident_at_events=all(any(v!=0 for v in trace[t-1]['next_input'])
                           and any(term['b']!=0 for port in trace[t-1]['six_inputs']
                                   for term in port) for t in clicks)
    complete=len(trace)==result['preparation']['steps']+1 and [r['step'] for r in trace]==list(range(len(trace)))
    boundary=result['initial_boundary_margin']>result['preparation']['steps']
    guarded=all(bool(trace[t]['arithmetic_events']) for t in clicks)
    only_at_records=all(event['step'] in clicks for event in result['arithmetic_events'])
    passed=all((correct_count,expected_arrivals,distinct,silence,zero_between,
                incident_at_events,boundary,complete))
    return {'event_count':correct_count,'predeclared_windows':expected_arrivals,
            'distinct_record_symbols':distinct,'minimum_silent_samples':silence,
            'registered_quiet_input_steps':sorted(quiet_steps),
            'zero_net_input_in_registered_waits':zero_between,
            'nonzero_incident_counter_and_input_at_events':incident_at_events,
            'boundary_separated':boundary,'complete_horizon':complete,
            'guarded_arithmetic_at_every_record':guarded,
            'no_extra_guarded_arithmetic_events':only_at_records,
            'record_milestone_passed':passed,
            'guarded_click_milestone_passed':passed and guarded and only_at_records,
            'passed':passed and guarded and only_at_records}
