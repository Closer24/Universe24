"""Independent divisor-six L0 arithmetic oracle for Universe24 regression tests only.

This is a deliberately direct receiver-side calculation, not an installable
second model. Production code imports none of this module.
"""
from dataclasses import dataclass, field
from itertools import product
from typing import NamedTuple
import numpy as np
from universe24.algebra.coupling import Coupling
from universe24.core.engine import OBJ
from universe24.core.lattice import DIRECTIONS, lattice as _lattice

class Channel(NamedTuple):
    a: int
    b: int
    r: int
VACUUM = Channel(0, 0, 2)
REFERENCE_VACUUM_R = 2
@dataclass(frozen=True)
class Cube:
    side: int
@dataclass
class RefState:
    cube: Cube
    background: Channel = VACUUM
    cells: dict = field(default_factory=dict)
    def at(self, address):
        return self.cells.get(address, self.background)

def time_reverse(state):
    def flip(c):
        return Channel(c.b, c.a, 4 + 2*(c.r % 2) - c.r)
    return RefState(state.cube, flip(state.background), {k:flip(v) for k,v in state.cells.items()})

class RefEngine:
    def __init__(self):
        self.coupling = Coupling()
    def _evaluate(self, state, inverse):
        L=state.cube.side
        cells={}
        for x,y,z,g in product(range(L),range(L),range(L),range(48)):
            addr=(x,y,z,g)
            a,b,r=state.at(addr)
            u=sum(self.coupling.weights[d][g] * state.at(((x+dx)%L,(y+dy)%L,(z+dz)%L,
                        self.coupling.ports[d][g]))[0 if inverse else 1]
                  for d,(dx,dy,dz) in enumerate(DIRECTIONS))
            if inverse:
                old_r=(r-2*u)%6
                ch=Channel((2*u+old_r-r)//6-b, a, old_r)
            else:
                ell,rn=divmod(2*u+r,6)
                ch=Channel(b,ell-a,rn)
            if ch != state.background: cells[addr]=ch
        return RefState(state.cube,state.background,cells)
    def advance(self,state): return self._evaluate(state,False)
    def rewind(self,state): return self._evaluate(state,True)

@dataclass
class Click:
    address: tuple
    kind: int
    quotient: int

def ref_clicks(before,after,step):
    for addr in sorted(before.cells.keys() | after.cells.keys()):
        a,b=before.at(addr),after.at(addr)
        ell=b.b+a.a
        if ell and a!=b:
            yield Click(addr,((b.r-a.r)//2)%3,ell)

def reference_arrays(ref: RefState):
    """(a, b, r) object arrays of shape (48, L^3) for a universe24 state; six-valued remainders."""
    L = ref.cube.side
    lat = _lattice(L)
    a = np.empty((48, lat.N), dtype=OBJ)
    b = np.empty((48, lat.N), dtype=OBJ)
    r = np.empty((48, lat.N), dtype=OBJ)
    bg = ref.background
    a[:, :] = bg.a
    b[:, :] = bg.b
    r[:, :] = bg.r
    for (x, y, z, g), ch in ref.cells.items():
        n = lat.index(x, y, z)
        a[g, n], b[g, n], r[g, n] = ch.a, ch.b, ch.r
    return a, b, r


def to_reference_state(a, b, r, L: int, background: Channel = VACUUM) -> RefState:
    """universe24 State from (48, L^3) arrays; r must lie in 0..5."""
    lat = _lattice(L)
    cells = {}
    for g in range(48):
        for n in range(lat.N):
            rr = int(r[g, n])
            if not 0 <= rr < 6:
                raise ValueError("remainder must lie in 0..5")
            ch = Channel(int(a[g, n]), int(b[g, n]), rr)
            if ch != background:
                cells[(*lat.coords(n), g)] = ch
    return RefState(Cube(L), background, cells)

def insert_reference(state, tensor, ref_state, namespace="ref"):
    from universe24.core.engine import State
    ra,rb,rr=reference_arrays(ref_state)
    a,b,r=(v.astype(OBJ) for v in (state.a,state.b,state.r))
    for g in range(48):
        name=f"R{g:02d}" if namespace is None else f"{namespace}.R{g:02d}"
        i=tensor.gear_index(name)
        a[i],b[i],r[i]=ra[g],rb[g],rr[g]
    return State(state.L,a,b,r)
