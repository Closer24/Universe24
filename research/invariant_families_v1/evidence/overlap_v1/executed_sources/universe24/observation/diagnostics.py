"""Passive exact balance checks; Q is NOT identified with physical energy."""
from ..core.engine import Engine
from ..core.state import Channel,State

def signed_account(state:State)->int:
    return sum(6*(s.b-s.a)+s.r-state.background.r for s in state.cells.values())

def expected_account_change(state:State,engine:Engine)->int:
    return sum(2*(sum(engine.coupling.weights[d][addr[3]] for d in range(6))-6)*s.b
               for addr,s in state.cells.items())

def balance_residuals(before:State,after:State,engine:Engine)->dict:
    if before.cube!=after.cube or before.background!=after.background:
        raise ValueError("States must have same geometry/background")
    sums=engine.input_sums(before)
    bad={}
    for addr in before.cells.keys() | after.cells.keys() | sums.keys():
        old=before.cells.get(addr,before.background)
        new=after.cells.get(addr,after.background)
        delta=6*(new.b-new.a-old.b+old.a)+new.r-old.r
        residual=delta-(2*sums.get(addr,0)-12*old.b)
        if residual: bad[addr]=residual
    return bad

def time_reverse(state:State)->State:
    def reflect(s:Channel)->Channel:
        return Channel(s.b,s.a,4+2*(s.r%2)-s.r)
    return State(state.cube,reflect(state.background),
                 {addr:reflect(s) for addr,s in state.cells.items()})
