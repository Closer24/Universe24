"""Independent replay and fixed-window audit of the 32-return extension."""
from __future__ import annotations
import argparse,gzip,hashlib,itertools,json,time
from pathlib import Path
from research.clock_selection import audit_recurrence as short
from research.clock_selection.audit import ROOT,load,file_digest,native_digest,canonical,audit_record

PROTOCOL_SHA='735da2e80a97e778a6629f9d3f0bf07bbca40b9a428fc3d660790a69f44621cd'

def planned():
    return [dict(id=f'long-ring-L{L}',side=L,stage='discovery' if L==48 else 'holdout',phase=2,
        clock_remainder=0,guide_target_channel=0,compensation_direction=None,control=m,pristine=False)
        for L,m in itertools.product((48,52),('00','10','01','11'))]

def period(states):
    hashes=[native_digest(s) for s in states];seen={};pairs=[]
    for t,h in enumerate(hashes):
        if h in seen:
            assert states[seen[h]]==states[t]
            pairs.append([seen[h],t])
        else:seen[h]=t
    lag=min((b-a for a,b in pairs),default=None)
    overlap=None if lag is None else all(states[t]==states[t+lag] for t in range(len(states)-lag))
    closed=lag is not None and states[0]==states[lag]
    return dict(full_state_hashes=hashes,first_repeat=pairs[0] if pairs else None,
        smallest_observed_period=lag,all_shifted_overlaps_equal=overlap,initial_state_closes=closed,
        full_board_period_certified=bool(closed and overlap))

def observe(case,states):
    out=short.observations(case,states);L=case['side'];c=L//2;track=out['packet_tracking']
    for n in range(3,33):
        shift=n*L;start=shift+32;end=shift+40;region=out['region_trace'];center=out['center_trace']
        checks=dict(complete_lag_four=all(region[t]==region[t+4] for t in range(start,end-3)),
            unit_clock_r0=all(a*a+b*b==1 and r==0 for a,b,r in center[start:end+1]),
            other_pairs_zero=all(not any(v[:2]) for f in region[start:end+1] for g,v in enumerate(f) if g!=2),
            individual_external_terms_zero=all(not out['boundary_inputs'][t]['nonzero_external_terms'] for t in range(start,end)),
            center_u_zero=all(out['center_inputs'][t]['u']==0 for t in range(start,end)),
            center_ell_zero=all(center[t+1][1]+center[t][0]==0 for t in range(start,end)))
        events=[[e['step'],e['kind'],e['ell']] for e in out['all_C'] if e['address']==[c+8,c,c,0] and shift+21<=e['step']<=shift+28]
        incoming=[track[shift+t] for t in (4,5,6,7)];outgoing=[track[shift+t] for t in (24,25,26,27)]
        out['cycles'].append(dict(cycle=n,incoming_matches=incoming,incoming_complete=all(incoming),
            outgoing_matches=outgoing,outgoing_complete=all(outgoing),continuous_return=all(track[24+(n-1)*L:8+n*L]),
            hold_start=start,hold_through=end,hold_checks=checks,complete_hold=all(checks.values()),outlet_C=events,
            exact_outlet_C_signature=events==[[shift+21,2,-1],[shift+25,1,1]]))
    scans=[]
    for state in states:
        candidates=[x for x in range(L) if state.at((x,c,c,0))==(1,0,4)]
        scans.append([x for x in candidates if short.wrapped_matches(state,x,c)])
    first=next((t for t in range(28,len(states)) if not scans[t]),None)
    after=None if first is None else next((t for t in range(first+1,len(states)) if scans[t]),None)
    out['whole_board_period']=period(states)
    out['supplemental_template_scan']=dict(origins_at_every_state=scans,scan_start_for_loss=28,
        first_empty_state_after_initial_output_window=first,first_subsequent_nonempty_state=after,
        reappearance_after_loss=after is not None,
        interpretation='Exact matching templates only; discontinuity prevents identifying the later match as uninterrupted transport or an approved trial.')
    out['native_horizon_complete']=len(states)==32*L+41
    return out

def assess_group(rows,p):
    base=short.assess_group(rows,p['claim']);by={r['case']['control']:r for r in rows};L=rows[0]['case']['side']
    traces={m:r['observations']['cycles'] for m,r in by.items()};initial=traces['11'][0];returns=[]
    for n in range(1,33):
        cur,prior=traces['11'][n],traces['11'][n-1]
        continuous=all(by['11']['observations']['packet_tracking'][24:8+n*L])
        genuine=bool(initial['incoming_complete'] and initial['outgoing_complete'] and continuous)
        eligible=genuine and cur['incoming_complete'] and prior['complete_hold']
        comparator=traces['10'][n]['incoming_complete'];different=cur['outgoing_complete']!=traces['10'][n]['outgoing_complete']
        returns.append(dict(cycle=n,genuine_continuous_return=genuine,
            continuous_from_previous_scheduled_output=cur['continuous_return'],continuous_from_initial_output=continuous,
            phase_prediction_eligible=eligible,predicted_output=False,observed_output=cur['outgoing_complete'],
            prediction_matches=None if not eligible else not cur['outgoing_complete'],packet_only_input_valid=comparator,
            output_differs_from_packet_only=different,bounded_clock_conditioned_return=bool(base['control_checks'] and eligible and comparator and different),
            raw_C_signature=cur['exact_outlet_C_signature']))
    outputs=[r['outgoing_complete'] for r in traces['11']]
    return dict(base,returns=returns,scheduled_output_by_cycle=outputs,
        scheduled_output_change_cycles=[n for n in range(1,len(outputs)) if outputs[n]!=outputs[n-1]],
        supplemental_template_reappearance=by['11']['observations']['supplemental_template_scan']['reappearance_after_loss'],
        whole_board_period_by_control={m:{k:v for k,v in r['observations']['whole_board_period'].items() if k!='full_state_hashes'} for m,r in by.items()})

def audit(study,output,budget=600):
    study,output=Path(study),Path(output);assert not output.exists();start=time.process_time()
    report=dict(passed=False,auditor_sha256=file_digest(__file__),helper_sha256=file_digest(short.__file__),
        protocol_sha256=PROTOCOL_SHA,records=[],groups=[],failure=None)
    try:
        p,result,registration=(load(study/f) for f in ('protocol.json','result.json','registration.json'))
        assert file_digest(study/'protocol.json')==registration['protocol_sha256']==PROTOCOL_SHA
        assert registration['cases']==planned() and result['registered_cases']==result['completed_cases']==8
        assert result['not_run_cases']==[] and result['status']=='completed'
        for path,sha in registration['source_sha256'].items():
            assert file_digest(ROOT/path)==file_digest(study/'source_provenance'/'source'/path)==sha,path
        grouped=[]
        for case,entry in zip(planned(),result['cases']):
            assert entry['case']==case;path=study/entry['record'];assert file_digest(path)==entry['record_gzip_sha256']
            raw=gzip.decompress(path.read_bytes());assert hashlib.sha256(raw).hexdigest()==entry['record_sha256'];record=json.loads(raw)
            assert record['case']==case and record['protocol_sha256']==PROTOCOL_SHA
            integrity,states=audit_record({k:v for k,v in record.items() if k!='observations'},
                expected_initial=short.expected_initial(case),deadline=start+budget)
            out=observe(case,states)
            assert out==record['observations'],[k for k in out if out[k]!=record['observations'].get(k)]
            assert entry['frames']==len(states)==32*case['side']+41 and entry['transitions']==len(states)-1
            assert file_digest(study/entry['native'])==entry['native_sha256']
            native=load(study/entry['native']);assert native['experiments']==[record['experiment']]
            report['records'].append(dict(case=case,integrity=integrity,period={k:v for k,v in out['whole_board_period'].items() if k!='full_state_hashes'},
                supplemental_reappearance=out['supplemental_template_scan']['reappearance_after_loss']))
            grouped.append(dict(case=case,states=states,observations=out))
            if len(grouped)==4:
                group=assess_group(grouped,p);assert result['groups'][len(report['groups'])]==group
                report['groups'].append(group);grouped=[]
            print(canonical({'audited_long_records':len(report['records']),'registered':8}),flush=True)
        assert not grouped
        for key,item in (('genuine_continuous_returns','genuine_continuous_return'),('bounded_clock_conditioned_returns','bounded_clock_conditioned_return')):
            assert result[key]==sum(r[item] for g in report['groups'] for r in g['returns'])
        assert result['supplemental_joint_reappearances']==sum(g['supplemental_template_reappearance'] for g in report['groups'])
        report.update(passed=True,full_states=sum(r['integrity']['states'] for r in report['records']),
            transitions=sum(r['integrity']['forward_transitions'] for r in report['records']),full_rewinds=8,sources_unchanged=True)
    except Exception as exc:report['failure']=f'{type(exc).__name__}: {exc}'
    report['cpu_seconds']=time.process_time()-start;output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--study',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    report=audit(args.study,args.output);print(canonical({k:report[k] for k in ('passed','failure','cpu_seconds')}))
    raise SystemExit(0 if report['passed'] else 1)
