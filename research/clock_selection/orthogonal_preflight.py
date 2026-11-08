"""Data-only crossed guide assembly. No forward/inverse evolution occurs here."""
import argparse, gzip, hashlib, itertools, json, time
from pathlib import Path
from research.components import BoardSpec, Patch, TensorSpec, finalize, place, plain
from research.staged_blocks.orbit import ShieldedOrbit
from research.presenter.export import canonical, state_data, state_sha256
from universe24.core.group_2o import DIRECTIONS


def packet(axis, primary, companion, present, tensor):
    cells, core = {}, []
    longitudinal = (2*axis,2*axis+1)
    assert all(tensor.ports[d][g]==g and tensor.weights[d][g]==1 for d in longitudinal for g in (primary,companion))
    def assign(a,v):
        if a in cells and cells[a]!=v: raise ValueError('Conflicting packet halo')
        cells[a]=v
    for i in range(4):
        xyz=tuple(i if j==axis else 0 for j in range(3))
        a=((1 if i==0 else -1 if i==2 else 0) if present else 0)
        b=((1 if i==1 else -1 if i==3 else 0) if present else 0)
        for g,s,r in ((primary,1,4),(companion,-1,0)):
            addr=(*xyz,g);assign(addr,(s*a,s*b,r));core.append(addr)
    for i in (1,2):
        xyz=tuple(i if j==axis else 0 for j in range(3))
        for d in range(6):
            if d in longitudinal: continue
            pos=tuple(xyz[j]+DIRECTIONS[d][j] for j in range(3))
            for g,s in ((primary,1),(companion,-1)):
                assign((*pos,tensor.ports[d][g]),(0,0,2-2*s*tensor.weights[d][g]))
    return Patch('orthogonal-packet',cells,tensor=tensor,sources={'packet':core},ports={'core':core})


def crossed_inputs(side=129,phase=0,r=0,gap=32,control='11'):
    if type(gap)!=int or gap<0 or type(side)!=int or side<2*(17+gap)+5 or phase not in range(4) or r not in (0,4) or control not in ('00','10','01','11'):
        raise ValueError('Invalid crossed-input preparation')
    tensor,c=TensorSpec(),side//2
    writer_start,probe_start=-17,-17-gap
    writer=packet(0,0,14,control[0]=='1',tensor)
    probe=packet(1,15,39,control[1]=='1',tensor)
    orbit=ShieldedOrbit(channel=2,a=0,b=1,r=r,phase=phase,tensor=tensor,halo_remainders=(0,2,2,0,2,2))
    joint=dict(orbit.cells)
    for address in ((0,-1,0,14),(1,0,0,39)):
        if joint[address]!=(0,0,2):raise ValueError('Guide companion intersects active halo')
        joint[address]=(0,0,4)
    interface=Patch('crossed-clock-interface',joint,tensor=tensor,ports={'clock':[(0,0,0,2)],'region':tuple(joint)},sources={'clock':[(0,0,0,2)]})
    wx,py={},{}
    for i in range(-c,side-c):
        if i not in (0,*range(writer_start,writer_start+4)):
            for g,rho in ((0,0),(14,4)):wx[(i,-1,0,g)]=(0,0,rho)
        if i not in (0,*range(probe_start,probe_start+4)):
            for g,rho in ((15,0),(39,4)):py[(1,i,0,g)]=(0,0,rho)
    pieces=(place(Patch('writer-guide',wx,tensor=tensor),at=(c,c,c),name='writer_guide'),
            place(Patch('probe-guide',py,tensor=tensor),at=(c,c,c),name='probe_guide'),
            place(writer,at=(c+writer_start,c-1,c),name='writer'),
            place(probe,at=(c+1,c+probe_start,c),name='probe'),
            place(interface,at=(c,c,c),name='interface'))
    return finalize(BoardSpec(side,tensor=tensor),pieces)


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'preparations').mkdir()
    protocol={'question':'Immutable complete crossed-input preparation compatibility only','sides':[129,161],'remainders':[0,4],'phases':[0,1,2,3],'gap':32,'controls':['00','10','01','11'],'cases':64,'cpu_budget_seconds':60,'trajectories':0,'clock_base_halo':[0,2,2,0,2,2],'source_masks':'counter-only; all remainders retained','claim_limit':'No carrier crossing or clock response has been simulated.'}
    raw=canonical(protocol)+'\n';(output/'protocol.json').write_text(raw)
    source=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (output/'registration.json').write_text(canonical({'source_sha256':source,'protocol_sha256':hashlib.sha256(raw.encode()).hexdigest(),'before_preparations':True})+'\n')
    start=time.process_time();rows=[];checks=[]
    for side,r,phase in itertools.product(protocol['sides'],protocol['remainders'],protocol['phases']):
        group={}
        for mask in protocol['controls']:
            if time.process_time()-start>60:raise TimeoutError('Preflight CPU budget')
            p=crossed_inputs(side,phase,r,32,mask);group[mask]=p
            name=f'L{side}-r{r}-p{phase}-{mask}'
            body={'case':{'side':side,'r':r,'phase':phase,'gap':32,'control':mask},'manifest':plain(p.manifest),'initial':state_data(p.initial),'state_sha256':state_sha256(p.initial)}
            data=gzip.compress((canonical(body)+'\n').encode(),mtime=0);file='preparations/'+name+'.json.gz';(output/file).write_bytes(data)
            rows.append({'id':name,'record':file,'sha256':hashlib.sha256(data).hexdigest(),'state_sha256':body['state_sha256'],'composition_pass':True})
        addresses=set().union(*(p.initial.cells for p in group.values()))
        sources=[set(group['11'].sources[k+'.packet']) for k in ('writer','probe')]
        matched=all(len({p.initial.at(a).r for p in group.values()})==1 for a in addresses)
        masks=True
        for mask,p in group.items():
            for a in addresses:
                expected=group['11'].initial.at(a)
                if any(mask[i]=='0' and a in sources[i] for i in (0,1)):expected=(0,0,expected.r)
                masks &= p.initial.at(a)==expected
        checks.append({'side':side,'r':r,'phase':phase,'same_remainders':matched,'exact_counter_masks':masks,'disjoint_sources':not bool(sources[0]&sources[1])})
    result={'status':'completed','cases':rows,'groups':checks,'composition_passes':len(rows),'all_control_checks':all(all(g[k] for k in ('same_remainders','exact_counter_masks','disjoint_sources')) for g in checks),'cpu_seconds':time.process_time()-start,'trajectories':0,'source_sha256':source,'claim_limit':protocol['claim_limit']}
    assert source==hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (output/'result.json').write_text(canonical(result)+'\n');print(canonical({k:v for k,v in result.items() if k not in ('cases','groups')}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);run(parser.parse_args().output)
