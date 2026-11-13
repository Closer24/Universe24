"""All-six-face clock/signal collision on exactly 48 regular 2O channels.

Each directional face has eight retained channels. Three are spatial Boolean
signal/memory/clock fields and five are retained marker bits. Markers are part
of b, not an external orientation or scheduling table. The fixed tensor is
defined on every raw state; its natural invariant domain is the coded sector.
"""
from __future__ import annotations
from functools import lru_cache
import itertools
import numpy as np
from universe24.algebra.group_2o import group,DIRECTIONS
from universe24.core import Tensor,GearType,State
from universe24.core.symmetry import require_equivariant, CONTRACT
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol

MODEL_ID = 'universe24/six-face-clock48'

ZERO=(0,0,0)
H_GENERATOR=1
LIVE=(0,1,2)
FIXED={3:0,4:0,5:0,6:1,7:1}
FORWARD3 = ((-3, (0,)),
 (3, (8,)),
 (6, (0, 1)),
 (3, (0, 5)),
 (-3, (0, 6)),
 (3, (0, 14)),
 (3, (0, 15)),
 (3, (1, 6)),
 (-3, (1, 8)),
 (-3, (1, 15)),
 (-3, (3, 7)),
 (3, (4, 7)),
 (-3, (5, 8)),
 (-6, (0, 1, 6)),
 (3, (0, 3, 7)),
 (3, (0, 4, 6)),
 (-3, (0, 4, 7)),
 (-3, (0, 4, 15)),
 (3, (1, 2, 6)),
 (3, (1, 5, 8)))
INVERSE3 = ((-3, (0,)),
 (-3, (1,)),
 (3, (8,)),
 (3, (9,)),
 (6, (0, 1)),
 (3, (0, 5)),
 (3, (0, 7)),
 (6, (1, 6)),
 (-3, (1, 7)),
 (-3, (3, 7)),
 (3, (4, 7)),
 (-3, (5, 8)),
 (-3, (6, 9)),
 (-3, (8, 9)),
 (-6, (0, 1, 6)),
 (3, (0, 3, 7)),
 (3, (0, 4, 6)),
 (-6, (0, 4, 7)),
 (3, (5, 8, 9)),
 (3, (6, 9, 10)))
TABLE={(0,0,0):(0,0,0),(0,0,1):(0,1,0),(0,1,0):(0,0,1),(0,1,1):(1,1,0),
       (1,0,0):(1,0,0),(1,0,1):(1,0,1),(1,1,0):(0,1,1),(1,1,1):(1,1,1)}

@lru_cache(maxsize=1)
def frames():
    return tuple(tuple(rotation[i][0] for i in range(3)) for rotation in group().rotations)

@lru_cache(maxsize=1)
def stabilizer():return tuple(group().power(H_GENERATOR,k) for k in range(8))

@lru_cache(maxsize=1)
def face_roots():
    directions=frames()
    return tuple(next(g for g,n in enumerate(directions) if n==direction) for direction in DIRECTIONS)

def face_roles(root):
    if type(root) is not int or not 0<=root<48:raise ValueError('root must be exact label in 0..47')
    labels=tuple(group().multiplication[root][h] for h in stabilizer())
    return {'root':root,'direction':frames()[root],'signal':labels[0],'memory':labels[1],'clock':labels[2],
            'marker_zero':labels[3:6],'marker_one':labels[6:8],'labels':labels}

def decode_faces(values,L):
    """Passive full-state domain check and unique retained-marker decoding."""
    if type(L) is not int or L < 3:raise ValueError('L must be an exact integer >=3')
    raw=np.asarray(values,dtype=object)
    if raw.shape!=(48,L**3):raise ValueError('complete 48-channel state required')
    if any(type(v) is not int and not isinstance(v,np.integer) for v in raw.flat):raise ValueError('exact integer values required')
    x=raw-1
    if np.any((x!=0)&(x!=1)):raise ValueError('all retained deviations must be Boolean')
    decoded=[];tab=group().multiplication
    for base in face_roots():
        matches=[]
        for h in stabilizer():
            root=tab[base][h];roles=face_roles(root)
            if all(np.all(x[roles['labels'][k]]==value) for k,value in FIXED.items()):matches.append(roles)
        if len(matches)!=1:raise ValueError('each face needs one spatially uniform retained marker phase')
        decoded.append(matches[0])
    return decoded

def sector_map(values,L,*,inverse=False):
    """Independent three-bit truth-table oracle; never used by Engine updates."""
    decoded=decode_faces(values,L);x=np.asarray(values,dtype=object)-1;out=x.copy()
    for roles in decoded:
        p,m,c=(x[roles[name]].reshape(L,L,L) for name in ('signal','memory','clock'))
        n=roles['direction'];axis=next(k for k,v in enumerate(n) if v);sign=n[axis]
        if not inverse:p=np.roll(p,sign,axis=axis)
        result=np.empty((3,L**3),dtype=object)
        for at,triple in enumerate(zip(p.flat,m.flat,c.flat)):result[:,at]=TABLE[tuple(map(int,triple))]
        if inverse:result[0]=np.roll(result[0].reshape(L,L,L),-sign,axis=axis).reshape(-1)
        for name,row in zip(('signal','memory','clock'),result):out[roles[name]]=row
    return out+1

@lru_cache(maxsize=1)
def coupling_tensor():
    """A single fixed integer cubic tensor; no runtime interpolation or callbacks."""
    terms=[];tab=group().multiplication;hs=stabilizer()
    for target,n in enumerate(frames()):
        for prototype,offset in ((FORWARD3,tuple(-v for v in n)),(INVERSE3,n)):
            for coefficient,monomial in prototype:
                factors=[(tab[target][hs[k%8]],ZERO if k<8 else offset,'b') for k in monomial]
                # Raw retained state b=1+x, and u_raw=6+3F(x)+3F^-1(x).
                for keep in itertools.product((False,True),repeat=len(factors)):
                    terms.append((target,coefficient*(-1)**(len(factors)-sum(keep)),[factor for factor,use in zip(factors,keep) if use]))
        terms.append((target,6,[]))
    tensor=Tensor([GearType(f'face_clock_g{g:02d}','official') for g in range(48)],terms,strict_support=True)
    require_equivariant(tensor)
    return tensor

def prepare_fields(*,L,signal,memory,clock,phases=(0,0,0,0,0,0),carry=None):
    """Complete six-face preparation. Fields have shape (6,N) or (6,L,L,L)."""
    if type(L) is not int or L<3:raise ValueError('L must be an exact integer >=3')
    if len(phases)!=6 or any(type(k) is not int or not 0<=k<8 for k in phases):raise ValueError('six exact phases 0..7 required')
    rows=[]
    for supplied in (signal,memory,clock):
        raw=np.asarray(supplied,dtype=object)
        if raw.shape not in ((6,L**3),(6,L,L,L)):raise ValueError('every field must cover all six faces and all nodes')
        if any(type(v) is not int and not isinstance(v,np.integer) for v in raw.flat):raise ValueError('exact Boolean integers required')
        if np.any((raw!=0)&(raw!=1)):raise ValueError('Boolean field values required')
        rows.append(raw.reshape(6,L**3))
    values=np.ones((48,L**3),dtype=object);tab=group().multiplication;hs=stabilizer()
    for face,(base,phase) in enumerate(zip(face_roots(),phases)):
        roles=face_roles(tab[base][hs[phase]])
        for k,value in FIXED.items():values[roles['labels'][k]]+=value
        for name,field in zip(('signal','memory','clock'),rows):values[roles[name]]+=field[face]
    old=sector_map(values,L,inverse=True)
    if carry is None:
        carry=np.ones((48,L**3),dtype=int)
    else:
        carry=np.asarray(carry,dtype=object)
        if carry.shape!=(48,L**3):raise ValueError('every carry must be explicitly supplied')
        if any(type(v) is not int and not isinstance(v,np.integer) for v in carry.flat):
            raise ValueError('exact integer carries required')
        if np.any((carry<1)|(carry>5)):raise ValueError('positive preparation carries must be in 1..5')
    return State(L,old,values,carry)

def electromagnetic_fields(state):
    """Passive marker-decoded transverse frame readout, not general Maxwell."""
    E=np.zeros((3,state.N),dtype=object);B=np.zeros_like(E)
    for roles in decode_faces(state.b,state.L):
        rotation=group().rotations[roles['root']];p=state.b[roles['signal']]-1
        for axis in range(3):
            E[axis]+=rotation[axis][1]*p;B[axis]+=rotation[axis][2]*p
    return E,B


def _planes(L, direction, sites):
    sites=tuple(sites)
    if any(type(site) is not int or not 0<=site<L for site in sites):
        raise ValueError('plane positions must be exact integers in 0..L-1')
    axis=next(k for k,v in enumerate(direction) if v)
    return np.isin(np.indices((L,L,L))[axis].reshape(-1),sites).astype(object)*1


def make_model_bundle(*, L=7, root=None, signal_sites=(0,), memory_sites=(), clock_sites=(2,)):
    """Seal one law with all six faces active by default.

    An explicit root selects one face and its marker phase for a directional
    preparation. The other faces retain their complete empty coded states.
    This changes only the seed, never the coupling.
    """
    if type(L) is not int or L<3:raise ValueError('L must be an exact integer >=3')
    bases=face_roots();hs=stabilizer();tab=group().multiplication
    phases=[0]*6
    if root is None:
        active=tuple(range(6))
    else:
        selected=face_roles(root)
        face=DIRECTIONS.index(selected['direction'])
        phases[face]=next(k for k,h in enumerate(hs) if tab[bases[face]][h]==root)
        active=(face,)
    signal_sites, memory_sites, clock_sites = map(tuple, (signal_sites, memory_sites, clock_sites))
    fields=[np.zeros((6,L**3),dtype=object) for _ in range(3)]
    for face in active:
        direction=frames()[bases[face]]
        for values,sites in zip(fields,(signal_sites,memory_sites,clock_sites)):
            values[face]=_planes(L,direction,sites)
    seed=prepare_fields(L=L,signal=fields[0],memory=fields[1],clock=fields[2],phases=tuple(phases))
    tensor=coupling_tensor()
    return create_bundle(tensor,seed,
        channels=[{'index':g,'name':gear.name,'label':gear.label,'owner':'six-face-clock48',
                   'purpose':'counted internal face channel; data or retained marker, no extra link state'}
                  for g,gear in enumerate(tensor.gears)],
        protocol=default_protocol(),
        model={'id':MODEL_ID,'version':'1','role':'universe-candidate','symmetry':CONTRACT,
               'domain':'six simultaneous spatial Boolean face circuits with uniform retained marker phases',
               'bias':1,'active_faces':list(active),'marker_phases':phases,
               'clock':'local reversible phase; Engine index is not retained proper time',
               'physics_acceptance':'blocked'})


def excitation_account(state):
    """Conserved logical accounts per face, not calibrated physical energy."""
    accounts=[]
    for face,roles in enumerate(decode_faces(state.b,state.L)):
        p,m,c=(state.b[roles[name]]-1 for name in ('signal','memory','clock'))
        accounts.append({'face':face,'direction':roles['direction'],
                         'free_signal':sum(map(int,p)), 'stored_signal':sum(map(int,m*c)),
                         'signal_charge':sum(map(int,p+m*c)),
                         'clock_sites':sum(map(int,m+c-m*c))})
    return accounts
