"""Pure synchronous reference executor. No runtime injections or observer callbacks."""
from dataclasses import dataclass,field
from typing import Iterator
from .coupling import Coupling
from .state import Address,Channel,State,channel
from .rule3 import forward,inverse

@dataclass(frozen=True,slots=True)
class Engine:
    coupling:Coupling=field(default_factory=Coupling)
    def __post_init__(self):
        if not isinstance(self.coupling,Coupling):
            raise TypeError("Expected fixed Coupling")

    def input_sums(self,state:State,component:int=1)->dict[Address,int]:
        if component not in (0,1): raise ValueError("component must be a or b")
        totals={}
        for address,triple in state.cells.items():
            value=triple[component]
            if value==0: continue
            g=address[3]
            for d in range(6):
                receiver=state.cube.adjacent(address,d,self.coupling.ports[d][g])
                totals[receiver]=totals.get(receiver,0)+self.coupling.weights[d][g]*value
        return totals

    def advance(self,state:State)->State:
        sums=self.input_sums(state)
        cells={}
        for address in state.cells.keys() | sums.keys():
            new=forward(state.cells.get(address,state.background),sums.get(address,0))
            if new!=state.background: cells[address]=new
        return State(state.cube,state.background,cells)

    def rewind(self,state:State)->State:
        """Inverse for audit/reconstruction; never a forward runtime gate."""
        sums=self.input_sums(state,component=0)
        cells={}
        for address in state.cells.keys() | sums.keys():
            old=inverse(state.cells.get(address,state.background),sums.get(address,0))
            if old!=state.background: cells[address]=old
        return State(state.cube,state.background,cells)

    def evolve(self,initial:State,steps:int)->Iterator[State]:
        if type(steps) is not int or steps<0: raise ValueError("steps must be nonnegative")
        state=initial
        yield state
        for _ in range(steps):
            state=self.advance(state)
            yield state

    def update_node(self,node:tuple[Channel,...],neighbors:tuple[tuple[Channel,...],...]):
        """Six neighbor states, ordered +x,-x,+y,-y,+z,-z, same old snapshot."""
        if len(node)!=48 or len(neighbors)!=6 or any(len(n)!=48 for n in neighbors):
            raise ValueError("Expected 48-channel node and six 48-channel neighbors")
        old=tuple(channel(s) for s in node)
        other=tuple(tuple(channel(s) for s in n) for n in neighbors)
        return tuple(forward(old[g],sum(self.coupling.weights[d][g]*
                     other[d][self.coupling.ports[d][g]].b for d in range(6)))
                     for g in range(48))
