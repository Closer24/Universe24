"""Passive arithmetic readout. C2 is NOT a physical selection operator."""
from dataclasses import dataclass
from typing import Iterator
from ..core.state import Address,Channel,State

@dataclass(frozen=True,slots=True)
class Click:
    step:int
    address:Address
    kind:int
    quotient:int
    before:Channel
    after:Channel

def classify(before:Channel,after:Channel)->tuple[int,int]|None:
    if before.r%2!=after.r%2:
        raise ValueError("Remainder parity changed")
    quotient=after.b+before.a
    if quotient==0 or before==after: return None
    kind=((after.r-before.r)//2)%3
    return kind,quotient

def clicks(before:State,after:State,step:int)->Iterator[Click]:
    if before.cube!=after.cube or before.background!=after.background:
        raise ValueError("Cannot compare states from different cubes")
    if type(step) is not int or step<1: raise ValueError("Invalid step index")
    for address in sorted(before.cells.keys() | after.cells.keys()):
        old=before.cells.get(address,before.background)
        new=after.cells.get(address,after.background)
        result=classify(old,new)
        if result is not None:
            kind,quotient=result
            yield Click(step,address,kind,quotient,old,new)
