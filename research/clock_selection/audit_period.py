"""Independent exact-state postanalysis of already audited recurrence captures."""
from pathlib import Path
import json
from research.clock_selection.audit import load,file_digest
from research.staged_blocks.audit import read_states

def main():
    root=Path(__file__).resolve().parent/'evidence'
    diagnostic=root/'recurrence_period_diagnostic'; saved=load(diagnostic/'result.json')
    certificate=diagnostic/'independent_check.json'; assert not certificate.exists()
    records=[]
    for row in saved['records']:
        path=root/'recurrence_v1'/'records'/row['record']
        assert file_digest(path)==row['record_file_sha256']
        raw=load(path); states=read_states(raw['experiment'])
        # Direct equality first: no producer hash or period routine decides this.
        period=next((lag for lag in range(1,len(states))
            if any(states[t]==states[t+lag] for t in range(len(states)-lag))),None)
        closed=period is not None and states[0]==states[period]
        overlaps=None if period is None else all(states[t]==states[t+period] for t in range(len(states)-period))
        assert period==row['smallest_observed_period'] and closed==row['initial_state_closes']
        assert overlaps==row['all_recorded_overlaps_equal']
        records.append({'case':raw['case'],'record_sha256':file_digest(path),'period':period,
            'initial_closure':closed,'all_overlaps_equal':overlaps,'states':len(states)})
    result={'passed':True,'auditor_sha256':file_digest(__file__),
        'diagnostic_sha256':file_digest(diagnostic/'result.json'),
        'parent_full_replay_audit_sha256':file_digest(root/'independent_audit'/'recurrence_v1.json'),
        'records':records,'new_transitions':0,
        'scope':'Exact full-state period comparison on previously independently replayed native captures.'}
    certificate.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'records':len(records)}))

if __name__=='__main__':main()
