"""Link the passive observer correction to independently replayed captures."""
import json
from pathlib import Path
from research.clock_selection.audit import ROOT,load,file_digest

def main():
    evidence=Path(__file__).resolve().parent/'evidence'
    analysis=evidence/'structure_v1_analysis';prior=evidence/'independent_audit'/'structure_v1.json'
    certificate=analysis/'independent_correction_check.json';assert not certificate.exists()
    verified=load(prior);result=load(analysis/'result.json');registration=load(analysis/'registration.json')
    assert verified['passed'] is True and file_digest(ROOT/registration['source_result'])==registration['source_result_sha256']
    by={r['id']:r for r in verified['records']};checked=[]
    for entry in result['cases']:
        assert file_digest(ROOT/entry['native_record'])==entry['native_record_sha256']
        path=analysis/entry['observations'];assert file_digest(path)==entry['observations_sha256']
        old=load(ROOT/entry['native_record']);new=load(path)
        assert new['case']==old['case']
        expected=dict(old['observations'])
        expected['separated_product_pairs']=by[entry['id']]['separated_product_pairs']
        # Every registered isolated-product list was independently empty.
        assert by[entry['id']]['products']==[]
        expected['separated_products_without_parent']=False
        assert new['observations']==expected
        checked.append(dict(id=entry['id'],native_sha256=entry['native_record_sha256'],corrected_observations_sha256=entry['observations_sha256']))
    assert result['groups'][4:]==verified['groups']
    assert result['new_trajectories']==0 and result['native_records_unchanged'] is True
    assert result['presenter_native_bundle_unchanged'] is True
    certificate.write_text(json.dumps(dict(passed=True,auditor_sha256=file_digest(__file__),
        independent_full_replay_sha256=file_digest(prior),corrected_result_sha256=file_digest(analysis/'result.json'),
        records=checked,new_transitions=0,scope='Only the two known faulty product observation fields changed; every other independently checked observation and all native recordings are identical.'),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'records':len(checked)}))

if __name__=='__main__':main()
