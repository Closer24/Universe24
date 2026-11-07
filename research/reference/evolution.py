"""Independent dense gather executor; all state is an explicit immutable tuple.

Flat index = (((x*L+y)*L+z)*48+g). These functions do not accept production
State/Coupling objects and do not import the production package. All next triples
are evaluated from one old tuple. Inverse is audit/reconstruction only.
"""
from functools import lru_cache
from itertools import product
from .algebra import coupling, DIRECTIONS


def addresses(side):
    return (xyz+(g,) for xyz in product(range(side),repeat=3) for g in range(48))


def index(address,side):
    x,y,z,g=address
    return ((x*side+y)*side+z)*48+g


def flatten(mapping,side,background=(0,0,2)):
    return tuple(tuple(mapping.get(addr,background)) for addr in addresses(side))


def forward(old,neighbor_sum):
    a,b,r=old
    numerator=2*neighbor_sum+r
    quotient=numerator//6
    return b,quotient-a,numerator-6*quotient


def inverse(new,old_neighbor_sum):
    next_a,next_b,next_r=new
    offset=next_r-2*old_neighbor_sum
    r=offset-6*(offset//6)
    a=(2*old_neighbor_sum+r-next_r)//6-next_b
    return a,next_a,r


@lru_cache(maxsize=8)
def neighbor_indices(side):
    if type(side) is not int or side<3:
        raise ValueError('side must be an integer >=3')
    # Ports are sign-independent; derive them from the independent matrices.
    ports=coupling().ports
    return tuple(tuple(index(((x+dx)%side,(y+dy)%side,(z+dz)%side,ports[d][g]),side)
                       for d,(dx,dy,dz) in enumerate(DIRECTIONS))
                 for x,y,z,g in addresses(side))


def _step(state,side,signs,reverse,order):
    if len(state)!=48*side**3:
        raise ValueError('Expected a complete dense state')
    graph=neighbor_indices(side);weights=coupling(tuple(signs)).weights
    component=0 if reverse else 1
    scalar=inverse if reverse else forward
    result=[None]*len(state)
    traversal=range(len(state)) if order is None else tuple(order)
    if order is not None and sorted(traversal)!=list(range(len(state))):
        raise ValueError('Traversal must visit every address exactly once')
    for i in traversal:
        g=i%48
        u=sum(weights[d][g]*state[j][component] for d,j in enumerate(graph[i]))
        result[i]=scalar(state[i],u)
    return tuple(result)


def advance(state,side,signs=(1,1,1),*,order=None):
    return _step(state,side,signs,False,order)


def rewind(state,side,signs=(1,1,1),*,order=None):
    return _step(state,side,signs,True,order)
