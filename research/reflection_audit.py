"""Exact audit of uniform signed channel maps for cubic spatial symmetries.

No change to dynamics. Exhaustive propagation replaces enumeration of 48!
permutations: the internal colored-port graph is connected, so the image of
channel 0 forces every other image, or produces a contradiction.
"""
from collections import deque
from itertools import product
import json
from pathlib import Path
from universe24.core import Channel, Coupling, Cube, Engine, State
from universe24.core.group_2o import DIRECTIONS, group, rotate

MIRROR_X=((-1,0,0),(0,1,0),(0,0,1))
INVERSION=((-1,0,0),(0,-1,0),(0,0,-1))


def direction_map(matrix):
    return tuple(DIRECTIONS.index(rotate(matrix,d)) for d in DIRECTIONS)


def walk(ports,start,word):
    for d in word:start=ports[d][start]
    return start


def attempt(ports,directions,image_zero):
    mapping={0:image_zero};inverse={image_zero:0};paths={0:()}
    pending=deque([0])
    while pending:
        source=pending.popleft()
        for d in range(6):
            neighbor=ports[d][source]
            image=ports[directions[d]][mapping[source]]
            new_path=paths[source]+(d,)
            if neighbor in mapping:
                if mapping[neighbor]!=image:
                    return None,{'image_zero':image_zero,'reason':'one source, two images',
                                 'path_a':paths[neighbor],'path_b':new_path}
            elif image in inverse:
                other=inverse[image]
                return None,{'image_zero':image_zero,'reason':'two sources, one image',
                             'path_a':paths[other],'path_b':new_path}
            else:
                mapping[neighbor]=image;inverse[image]=neighbor
                paths[neighbor]=new_path;pending.append(neighbor)
    if len(mapping)!=48:
        raise AssertionError('Disconnected graph needs additional root assignments')
    return tuple(mapping[g] for g in range(48)),None


def verify_certificate(ports,directions,certificate):
    a,b=certificate['path_a'],certificate['path_b']
    source_a,source_b=walk(ports,0,a),walk(ports,0,b)
    image_a=walk(ports,certificate['image_zero'],tuple(directions[d] for d in a))
    image_b=walk(ports,certificate['image_zero'],tuple(directions[d] for d in b))
    if certificate['reason']=='one source, two images':
        return source_a==source_b and image_a!=image_b
    return source_a!=source_b and image_a==image_b


def search(matrix):
    ports=Coupling().ports;directions=direction_map(matrix)
    solutions=[];certificates=[]
    for image in range(48):
        permutation,certificate=attempt(ports,directions,image)
        if permutation is not None:solutions.append(permutation)
        else:
            assert verify_certificate(ports,directions,certificate)
            certificates.append(certificate)
    return solutions,certificates


def channel_signs(coupling,matrix,permutation):
    directions=direction_map(matrix);signs={0:1};pending=deque([0])
    while pending:
        g=pending.popleft()
        for d in range(6):
            h=coupling.ports[d][g]
            sign=signs[g]*coupling.weights[d][g]*coupling.weights[directions[d]][permutation[g]]
            if h in signs:
                if signs[h]!=sign:return None
            else:signs[h]=sign;pending.append(h)
    assert len(signs)==48
    return tuple(signs[g] for g in range(48))


def weighted_covariance(coupling,matrix,permutation,signs=(1,)*48):
    directions=direction_map(matrix)
    return all(
        permutation[coupling.ports[d][g]]==coupling.ports[directions[d]][permutation[g]]
        and signs[g]*coupling.weights[d][g]==coupling.weights[directions[d]][permutation[g]]*signs[coupling.ports[d][g]]
        for d in range(6) for g in range(48))


def negate_channel(value):
    a,b,r=value
    return Channel(-a,-b,4-r+2*(r%2))


def transform(state,matrix,permutation=tuple(range(48)),signs=(1,)*48):
    side=state.cube.side
    if any(sign==-1 for sign in signs) and negate_channel(state.background)!=state.background:
        raise ValueError('Sparse uniform background must be fixed under sign reversal')
    return State(state.cube,state.background,
                 {(*(v%side for v in rotate(matrix,a[:3])),permutation[a[3]]):
                  s if signs[a[3]]==1 else negate_channel(s)
                  for a,s in state.cells.items()})


def mirror_x_lift(coupling):
    # Choose a reproducible minimal-order spatial-mirror lift, not the first
    # graph isomorphism (some of those have order 8).
    permutation=next(p for p in search(MIRROR_X)[0] if p[0]==10)
    signs=channel_signs(coupling,MIRROR_X,permutation)
    assert signs is not None
    assert weighted_covariance(coupling,MIRROR_X,permutation,signs)
    return permutation,signs


def naive_counterexample():
    engine=Engine(Coupling((1,-1,1)))
    seed=State(Cube(7),cells={(0,0,0,2):Channel(0,3,2)})
    mirror_then_evolve=engine.advance(transform(seed,MIRROR_X))
    evolve_then_mirror=transform(engine.advance(seed),MIRROR_X)
    assert mirror_then_evolve!=evolve_then_mirror
    differences=[{'address':a,'mirror_then_evolve':list(mirror_then_evolve.at(a)),
                  'evolve_then_mirror':list(evolve_then_mirror.at(a))}
                 for a in sorted(mirror_then_evolve.cells.keys()|evolve_then_mirror.cells.keys())
                 if mirror_then_evolve.at(a)!=evolve_then_mirror.at(a)]
    return {'side':7,'source':[0,0,0,2],'initial_triple':[0,3,2],'differences':differences}


def main():
    algebra=group();proper=sorted(set(algebra.rotations))
    improper=[tuple(tuple(-x for x in row) for row in m) for m in proper]
    counts=[];coupling=Coupling((1,-1,1))
    for matrix in improper:
        solutions,certificates=search(matrix)
        assert len(solutions)==8 and len(certificates)==40
        plain=[p for p in solutions if weighted_covariance(coupling,matrix,p)]
        signed=[p for p in solutions if channel_signs(coupling,matrix,p) is not None]
        assert len(plain)==0 and len(signed)==8
        counts.append({'matrix':matrix,'support_permutations':len(solutions),
                       'plain_weighted_symmetries':len(plain),'signed_weighted_symmetries':len(signed)})
    for signs in product((-1,1),repeat=3):
        coupling=Coupling(signs)
        for h in range(48):
            assert weighted_covariance(coupling,algebra.rotations[h],algebra.multiplication[h])
    sign_variants=[]
    for weights in product((-1,1),repeat=3):
        c=Coupling(weights);total=0
        for matrix in improper:
            for p in search(matrix)[0]:
                sigma=channel_signs(c,matrix,p)
                assert sigma is not None and weighted_covariance(c,matrix,p,sigma)
                total+=1
        sign_variants.append({'body_signs':weights,'verified_signed_lifts':total})
    permutation,signs=mirror_x_lift(Coupling((1,-1,1)))
    central=algebra.multiplication[algebra.central]
    assert tuple(permutation[permutation[g]] for g in range(48))==central
    assert all(signs[g]*signs[permutation[g]]==-1 for g in range(48))
    result={'scope':'spatial cubic symmetry with a uniform signed channel permutation and retained-remainder map',
            'proper_spatial_rotations':24,'lifted_rotations_checked':48,
            'coupling_sign_choices_checked':8,'improper_results':counts,
            'sign_variants':sign_variants,
            'mirror_x_lift':{'spatial_matrix':MIRROR_X,'permutation':permutation,'signs':signs,
                             'square':'central channel permutation together with global counter/impulse negation',
                             'order':4},
            'naive_mirror_counterexample':naive_counterexample(),
            'limitation':'Combined lifted symmetry; not an involution of full retained state and not a proved physical parity representation.'}
    Path(__file__).with_name('reflection_audit_results.json').write_text(
        json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print('Rotations PASS. All 24 improper maps admit signed lifts, for all 8 coupling choices. Mirror lift order: 4.')


if __name__=='__main__':main()
