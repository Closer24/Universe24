"""Hash and native-readback review of restored, previously audited OR competition."""
import json
from pathlib import Path
from research.clock_selection.audit import ROOT,load,file_digest,all_events,input_terms
from research.staged_blocks.audit import read_states

def main():
    result=[]
    for study,review in (('selection_evidence_v1','selection_review'),('selection_followup_evidence_v1','selection_followup_review'),('selection_receiver_evidence_v1','joined_receiver_review')):
        folder=ROOT/'research/component_studies'/study;certificate=ROOT/'research/component_review'/(review+'.json')
        r=load(certificate);data=load(folder/'result.json')
        assert r['passed'] is True and file_digest(folder/'result.json')==r['evidence_result_sha256']
        assert file_digest(folder/'protocol.json')==data['protocol_sha256']
        for row in r.get('full_replays',[]):assert file_digest(ROOT/row['path'])==row['trace_sha256']
        result.append(dict(study=study,result_sha256=file_digest(folder/'result.json'),prior_audit_sha256=file_digest(certificate),
            prior_audit_scope=r['scope'],prior_full_replays=r.get('full_oracle_replayed_runs',r.get('runs'))))
    witnesses=[]
    for name,winner in (('receiver-joint-OR-NO-s1',-1),('receiver-joint-NO-OR-s1',1)):
        folder=ROOT/'research/component_studies/selection_receiver_evidence_v1/cases'/name
        analysis=load(folder/'analysis.json');bundle=folder/'experiments.json'
        assert file_digest(bundle)==analysis['portable_bundle_sha256']
        states=read_states(load(bundle)['experiments'][0]);events=all_events(states)[0]
        target=(64+winner*8,64,64);loser=(64-winner*8,64,64)
        selected=[e for e in events if tuple(e['address'][:3])==target];times=sorted({e['step'] for e in selected})
        assert times==list(range(12,49,2)) and len(selected)==29
        record=[[s.at((*target,g))[2] for g in (0,14)] for s in states]
        assert record[12]==[0,0] and next(t for t in range(13,49) if record[t]!=[0,0])==14
        assert all(states[t].at((*loser,g))==states[0].at((*loser,g)) for t in range(49) for g in range(48))
        sums,_=input_terms(states[11],[(*target,g) for g in (0,14)],(1,1,1));assert sums==[1,-1]
        witnesses.append(dict(case=name,bundle_sha256=file_digest(bundle),first_C=12,C_bearing_updates=len(times),
            individual_channel_C_events=len(selected),first_record_loss=14,first_input=sums,loser_all48_quiet=True))
    out=ROOT/'research/clock_selection/evidence/independent_audit/prior_competition_context.json';assert not out.exists()
    out.write_text(json.dumps(dict(passed=True,auditor_sha256=file_digest(__file__),studies=result,receiver_native_readbacks=witnesses,
        new_trajectories=0,new_forward_inverse_replays=0,
        scope='Previously audited finite OR/NO prepared competition is available. This pass checks restored evidence identity and two complete native receiver readbacks; it does not repeat all648 prior trajectories. Higher-cooperation preference, input-controlled reversal, internally computed unique approval and retaining single-click memory remain unestablished.'),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'restored_studies':3,'native_receiver_readbacks':2}))

if __name__=='__main__':main()
