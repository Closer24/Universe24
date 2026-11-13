"""Cubic, conservative edge exclusion with onsite face rotation; not gravity."""
from __future__ import annotations
from functools import lru_cache
import itertools
import numpy as np
from universe24.algebra.group_2o import group
from universe24.core import Tensor, GearType, State
from universe24.core.symmetry import require_equivariant, CONTRACT
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol

MODEL_ID = 'universe24/capacity-scatter48'

G=group(); TAB=G.multiplication; ZERO=(0,0,0)
FRAMES=tuple(tuple(r[i][0] for i in range(3)) for r in G.rotations)
EDGE_ROOT=next(g for g in range(48) if G.power(g,2)==G.central and FRAMES[g]==(-1,0,0))
EDGE_POWERS=tuple(G.power(EDGE_ROOT,k) for k in range(4))
TURN=next(g for g,r in enumerate(G.rotations) if tuple(r[k][0] for k in range(3))==(0,1,0) and tuple(r[k][1] for k in range(3))==(0,0,1))
ONSITE=TAB[G.inverses[TURN]][EDGE_ROOT]
FORWARD=((1,(0,1,2)),(1,(3,)),(-1,(1,2,3)))
INVERSE=((1,(1,)),(1,(0,2,3)),(-1,(1,2,3)))


def edge_gate(bits, inverse=False):
    """A three-unit saturated quartet is held; other words cross the edge."""
    bits = tuple(bits)
    if len(bits) != 4 or any(isinstance(v, (bool, np.bool_)) or
            not isinstance(v, (int, np.integer)) or v not in (0, 1) for v in bits):
        raise ValueError('an edge word requires four exact Boolean integers')
    if sum(bits)==3:
        return tuple(bits)
    return tuple(bits[1:]+bits[:1] if inverse else bits[-1:]+bits[:-1])


def _size(L):
    if type(L) is not int or L < 3:
        raise ValueError('L must be an exact integer >=3')


def _integers(values, shape):
    raw = np.asarray(values, dtype=object)
    if raw.shape != shape:
        raise ValueError(f'complete array of shape {shape} required')
    if any(isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, np.integer)) for v in raw.flat):
        raise ValueError('exact integers required')
    return raw


def frames():
    return FRAMES


def decode_occupation(values, L):
    """Positive raw values encode a Boolean occupation; no species decoding."""
    _size(L)
    bits = _integers(values, (48, L**3)) - 1
    if np.any((bits != 0) & (bits != 1)):
        raise ValueError('raw retained values must be one plus Boolean occupation')
    return bits


@lru_cache(maxsize=4, typed=True)
def edge_quartets(L):
    """Partition all channels into four-slot neighborhoods on physical edges.

    Slots 0,2 lie at one endpoint and 1,3 at its neighbor. Both endpoint
    views identify the same quartet; no dynamic state lives in this table.
    """
    _size(L)
    seen, quartets = set(), []
    for g in range(48):
        for site in range(L**3):
            if (g, site) in seen:
                continue
            xyz = np.unravel_index(site, (L,L,L))
            neighbor = int(np.ravel_multi_index(tuple((xyz[k]+FRAMES[g][k])%L for k in range(3)), (L,L,L)))
            quartet = tuple((TAB[g][p], site if j%2==0 else neighbor) for j,p in enumerate(EDGE_POWERS))
            seen.update(quartet)
            quartets.append(quartet)
    assert len(seen) == 48*L**3
    return tuple(quartets)


def edge_stage(bits, L, inverse=False):
    """Independent finite-gate oracle; the Engine uses only its fixed tensor."""
    out = bits.copy()
    for quartet in edge_quartets(L):
        word = tuple(int(bits[g,node]) for g,node in quartet)
        for (g,node),value in zip(quartet,edge_gate(word,inverse)):
            out[g,node] = value
    return out


def sector_map(values,L,*,inverse=False):
    x = decode_occupation(values,L)
    if inverse:
        x = x[[TAB[g][G.inverses[ONSITE]] for g in range(48)]]
        out = edge_stage(x,L,True)
    else:
        out = edge_stage(x,L)[[TAB[g][ONSITE] for g in range(48)]]
    return out+1


@lru_cache(maxsize=1)
def coupling_tensor():
    terms=[]
    for target in range(48):
        forward_root=TAB[target][ONSITE]
        forward_vars=[(TAB[forward_root][p],ZERO if k%2==0 else FRAMES[forward_root],'b') for k,p in enumerate(EDGE_POWERS)]
        inverse_vars=[(TAB[TAB[target][p]][G.inverses[ONSITE]],ZERO if k%2==0 else FRAMES[target],'b') for k,p in enumerate(EDGE_POWERS)]
        for prototype,variables in ((FORWARD,forward_vars),(INVERSE,inverse_vars)):
            for coefficient,monomial in prototype:
                factors=[variables[k] for k in monomial]
                for keep in itertools.product((False,True),repeat=len(factors)):
                    terms.append((target,3*coefficient*(-1)**(len(factors)-sum(keep)),[v for v,use in zip(factors,keep) if use]))
        terms.append((target,6,[]))
    result=Tensor([GearType(f'load_g{g:02d}','official') for g in range(48)],terms,strict_support=True)
    require_equivariant(result)
    return result


def prepare_occupation(*, L, occupation, carry=None):
    """Supply all 48 occupation rows before evolution; no padding or injection."""
    _size(L)
    raw = np.asarray(occupation, dtype=object)
    if raw.shape == (48,L,L,L):
        raw = raw.reshape(48,L**3)
    bits = _integers(raw, (48,L**3))
    if np.any((bits != 0) & (bits != 1)):
        raise ValueError('Boolean occupation required')
    values = bits+1
    if carry is None:
        carry = np.ones((48,L**3), dtype=int)
    else:
        carry = _integers(carry, (48,L**3))
        if np.any((carry < 1) | (carry > 5)):
            raise ValueError('positive preparation carries must be in 1..5')
    return State(L,sector_map(values,L,inverse=True),values,carry)


def make_model_bundle(*, L=7, pattern='burst', radius=0, root=0, center=None, halo=True):
    """One coupling with explicit burst, isolated pulse or empty preparations.

    The burst's optional one-bit boundary halo breaks central-pair symmetry
    to exercise capacity feedback. It is declared initial data, not an
    emergent species or an intervention during evolution. Without the halo,
    the fully paired core is an exact free-transport control under this law.
    """
    _size(L)
    if pattern not in ('burst','pulse','vacuum'):
        raise ValueError('pattern must be burst, pulse or vacuum')
    if type(radius) is not int or not 0 <= radius <= L//2:
        raise ValueError('radius must be an exact integer in 0..L//2')
    if type(root) is not int or not 0 <= root < 48:
        raise ValueError('root must be an exact group label in 0..47')
    if type(halo) is not bool:
        raise ValueError('halo must be Boolean')
    if center is None:
        center = (L//2,)*3
    center = tuple(center)
    if len(center) != 3 or any(type(c) is not int or not 0 <= c < L for c in center):
        raise ValueError('center must contain three exact node coordinates')
    bits = np.zeros((48,L**3),dtype=object)
    coordinates = np.indices((L,L,L)).reshape(3,-1)
    halo_count, core_count = 0, 0
    if pattern == 'pulse':
        bits[root,np.ravel_multi_index(center,(L,L,L))] = 1
    elif pattern == 'burst':
        delta = np.abs(coordinates-np.asarray(center)[:,None])
        distance = np.minimum(delta,L-delta).sum(axis=0)
        core = distance <= radius
        core_count = int(core.sum())
        bits[:,core] = 1
        if halo:
            # One incoming channel at each core-to-empty boundary edge.
            bases = [next(g for g,n in enumerate(FRAMES) if n==d)
                     for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))]
            for site in np.flatnonzero(core):
                xyz = coordinates[:,site]
                for base in bases:
                    outgoing = TAB[root][base]
                    direction = FRAMES[outgoing]
                    at = int(np.ravel_multi_index(tuple((xyz[k]+direction[k])%L for k in range(3)),(L,L,L)))
                    if not core[at]:
                        incoming = TAB[outgoing][EDGE_ROOT]
                        if not bits[incoming,at]:
                            bits[incoming,at] = 1
                            halo_count += 1
    seed = prepare_occupation(L=L,occupation=bits)
    tensor = coupling_tensor()
    return create_bundle(tensor,seed,
        channels=[{'index':g,'name':gear.name,'label':gear.label,
                   'owner':'capacity-scatter48','purpose':'one counted Boolean occupation slot inside a directional node face'}
                  for g,gear in enumerate(tensor.gears)],
        protocol=default_protocol(),
        model={'id':MODEL_ID,'version':'1','role':'universe-candidate','symmetry':CONTRACT,
               'domain':'all 48 arbitrary spatial Boolean occupations, positive affine encoding',
               'node_capacity':48,'face_capacity':8,'bias':1,
               'preparation':{'pattern':pattern,'radius':radius,'root':root,'center':list(center),
                              'halo':halo if pattern=='burst' else False,
                              'core_nodes':core_count,'halo_occupation':halo_count,
                              'total_occupation':int(bits.sum())},
               'clock':'retained channel cycles; Engine index is not calibrated proper time',
               'physics_acceptance':'blocked'})
