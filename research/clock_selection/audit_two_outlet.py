"""Independent initial algebra and full-state audit for orthogonal outlets."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from research.clock_selection.audit import Snapshot,coupling,DIRECTIONS,file_digest,native_digest

PROTOCOL_SHA='d46fb7bf62815fa2f0c6c66950d0fded0cdd9a86c0ce47bac40e3a06c042545c'
AXES={'X':(0,0,14),'Y':(1,15,39)}

def sources(case):
    c=case['side']//2
    return {'X':(c-19,c-1,c),'Y':(c+1,c-19-case['gap'],c)}

def packet(axis_name,origin):
    axis,primary,companion=AXES[axis_name];matrix=coupling((1,1,1));cells={}
    assert all(matrix.ports[d][g]==g for d in (2*axis,2*axis+1) for g in (primary,companion))
    for k in range(4):
        point=list(origin);point[axis]+=k
        a=(1,0,-1,0)[k];b=(0,1,0,-1)[k]
        cells[(*point,primary)]=(a,b,4);cells[(*point,companion)]=(-a,-b,0)
    for k in (1,2):
        point=list(origin);point[axis]+=k
        for d,delta in enumerate(DIRECTIONS):
            if d//2==axis:continue
            target=tuple(point[j]+delta[j] for j in range(3))
            for source,sign in ((primary,1),(companion,-1)):
                recipients=[g for g in range(48) if matrix.ports[d^1][g]==source];assert len(recipients)==1
                g=recipients[0];cells[(*target,g)]=(0,0,2-2*sign*matrix.weights[d^1][g])
    assert len(cells)==24
    return cells

def initial(case):
    side=case['side'];c=side//2;cells={};isolated=case['stage']=='isolated';matrix=coupling((1,1,1))
    def put(a,v):
        assert a not in cells or cells[a]==v,('Incompatible initial assignments',a)
        cells[a]=v
    for name in ((case['axis'],) if isolated else ('X','Y')):
        axis,primary,companion=AXES[name];origin=sources(case)[name];present=case['control']['XY'.index(name)]=='1'
        for i in range(side):
            if present and origin[axis]<=i<origin[axis]+4:continue
            if not isolated and case['clock_mode']!='bare' and i==c:continue
            point=list(origin);point[axis]=i
            put((*point,primary),(0,0,0));put((*point,companion),(0,0,4))
        if present:
            for a,v in packet(name,origin).items():put(a,v)
    if not isolated and case['clock_mode']!='bare':
        center=(c,c,c);nodes=(center,*(tuple(c+delta[j] for j in range(3)) for delta in DIRECTIONS))
        local={(*n,g):(0,0,2) for n in nodes for g in range(48)};phase=case['phase']
        pair=((0,1),(1,0),(0,-1),(-1,0))[phase] if case['clock_mode']=='on' else (0,0)
        local[(*center,2)]=(*pair,0)
        for d,node in enumerate(nodes[1:]):
            recipient=[g for g in range(48) if matrix.ports[d^1][g]==2];assert len(recipient)==1
            g=recipient[0];local[(*node,g)]=(0,0,(0,2,2,0,2,2)[d]+(2*matrix.weights[d^1][g] if phase in (1,2) else 0))
        for a in ((c,c-1,c,14),(c+1,c,c,39)):
            assert local[a]==(0,0,2);local[a]=(0,0,4)
        for a,v in local.items():put(a,v)
    return Snapshot(side,(0,0,2),cells)

def geometries():
    out=[dict(id=f'orthogonal-L{L}-bare-gap{gap}',side=L,gap=gap,phase=0,clock_mode='bare',stage='crossed')
        for L,gap in ((369,0),(369,34),(369,36),(385,0))]
    for side,phases,modes in ((369,range(4),('on','counter_off')),(385,(3,),('on',))):
        out.extend(dict(id=f'orthogonal-L{side}-p{phase}-{mode}-gap{gap}',side=side,gap=gap,phase=phase,clock_mode=mode,stage='encounter')
            for phase,gap,mode in itertools.product(phases,(0,34,36),modes))
    return out

def planned():
    return [dict(id=f'orthogonal-isolated-{axis}-gap{gap}',side=369,axis=axis,gap=gap,phase=0,
        clock_mode='bare',stage='isolated',control='10' if axis=='X' else '01')
        for axis,gap in (('X',0),('Y',0),('Y',34),('Y',36))]+[
        dict(g,control=m) for g in geometries() for m in ('00','10','01','11')]

def preflight(output):
    from research.clock_selection import two_outlet as producer
    output=Path(output);assert not output.exists();p=json.loads(producer.PROTOCOL.read_bytes())
    assert file_digest(producer.PROTOCOL)==PROTOCOL_SHA
    checked=[]
    for case in planned():
        actual=producer.prepare(case,p).initial
        native=Snapshot(case['side'],tuple(actual.background),{a:tuple(v) for a,v in actual.cells.items()})
        expected=initial(case);assert native==expected,case
        checked.append(dict(case=case,initial_sha256=native_digest(expected),complete_initial_equal=True))
    report=dict(passed=True,complete_preparations=len(checked),new_trajectories=0,protocol_sha256=PROTOCOL_SHA,
        auditor_sha256=file_digest(__file__),producer_sha256=file_digest(producer.__file__),records=checked,
        scope='Independent exact-matrix initial reconstruction; no functional evolution claim.')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'complete_preparations':len(checked),'new_trajectories':0}))

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--preflight-output',required=True);args=ap.parse_args()
    preflight(args.preflight_output)
