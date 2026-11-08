"""Passive final identity/coverage receipt; never executes a board update."""
from pathlib import Path
import hashlib
import json

from research.clock_selection.provenance import verify_sources
from research.clock_selection.run import verify_index

ROOT=Path(__file__).resolve().parents[3]
HERE=ROOT/'research/clock_selection'
EVIDENCE=HERE/'evidence'


def identity(path):
    h=hashlib.sha256()
    with path.open('rb') as handle:
        for data in iter(lambda:handle.read(1024*1024),b''):h.update(data)
    return {'path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':h.hexdigest()}


def main():
    index=EVIDENCE/'index_final/index.json'
    data=json.loads(index.read_text())
    assert data['records']==890
    certificates=[identity(p) for p in sorted((EVIDENCE/'independent_audit').glob('*')) if p.is_file()]
    partial=[]
    for name in ('structure_v1','two_outlet_v1'):
        partial.extend(identity(p) for p in sorted((EVIDENCE/name/'records').glob('*.json.gz')))
    assert len(partial)==24
    sources=[]
    for path in sorted(EVIDENCE.rglob('manifest.json')):
        item=json.loads(path.read_text())
        if item.get('format')=='universe24-clock-selection-source-snapshot-v1':
            outcome=verify_sources(path.parent)
            assert outcome['archive_verified']
            sources.append({'manifest':identity(path),**outcome})
    exceptions={row['manifest']['path']:row['live_mismatches'] for row in sources if not row['live_sources_unchanged']}
    assert exceptions=={
        'research/clock_selection/evidence/recurrence_long_v1/source_provenance/manifest.json':['research/clock_selection/recurrence_long.py'],
        'research/clock_selection/evidence/two_outlet_v1/source_provenance/manifest.json':['research/clock_selection/two_outlet.py']}
    reports=[];checks={}
    for name in ('presenter_dom_smoke','presenter_dom_smoke_additional','presenter_dom_smoke_waves',
                 'presenter_dom_smoke_final','presenter_dom_smoke_activation_route',
                 'presenter_dom_smoke_carrier_memory','presenter_dom_smoke_carrier_memory_combined'):
        path=EVIDENCE/name/'report.json';report=json.loads(path.read_text());assert report['passed']
        reports.append(identity(path))
        for page in report['bundles']:
            assert hashlib.sha256((ROOT/page['input']).read_bytes()).hexdigest()==page['input_sha256']
            for check in page['checks']:
                key=check['experiment']
                if key in checks:assert checks[key]['retained_state_sha256']==check['retained_state_sha256']
                checks[key]=check
    selection=json.loads((HERE/'presentation_collection_v3.json').read_text())
    selected=[];frames=0
    for entry in selection['studies']:
        manifest=json.loads((HERE/entry['package']/'manifest.json').read_text())
        selected.extend(manifest['experiments']);frames+=manifest['frames']
    assert len(selected)==len(set(selected))==131
    assert frames==21963
    assert all(key in checks for key in selected)
    assert sum(checks[key]['frames'] for key in selected)==frames
    outcome={'format':'universe24-clock-final-evidence-identity-v1',
        'index':identity(index),'verification':verify_index(index),
        'registered_studies':15,'complete_study_records':890,'complete_states':76322,
        'forward_transitions_independently_inverted':75432,'full_rewinds':890,
        'counts_source':'independent_review.md plus independent_review_addendum.md; identity verification is not a new scientific audit',
        'partial_duplicate_attempt_records':partial,'source_snapshots':sources,
        'source_exception_scope':'Only the explicitly retained failed original long-capture and interrupted original two-outlet producers differ from current corrected files. Their archived bytes still verify.',
        'authoritative_structural_result':identity(EVIDENCE/'structure_v1_analysis/result.json'),
        'superseded_structural_observer':'structure_v1_corrected/result.json contains the withdrawn product-observer result; complete native frames remain valid. Do not derive scientific verdicts from that field.',
        'independent_audit_files':certificates,'presenter_reports':reports,
        'selected_complete_presenter_experiments':131,'selected_native_frames':21963,
        'presenter_scope':'Application JavaScript and native Canvas with explicit geometry; no real-browser CSS, native touch, Safari/iPad or attachment-preview certification.',
        'scientific_scope':'Use the claim register and corrected reports. Native integrity, target acceptance and resource compliance remain separate.'}
    path=EVIDENCE/'index_final/verification.json'
    if path.exists():raise FileExistsError(path)
    path.write_text(json.dumps(outcome,indent=2)+'\n')
    print(json.dumps({'records':890,'files_verified':outcome['verification']['files_verified'],
        'partial_duplicates':len(partial),'presenter_experiments':131,'native_frames':21963}))


if __name__=='__main__':main()
