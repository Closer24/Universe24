"""Immutable exact state on a closed periodic cube. No clock or click log."""
from dataclasses import dataclass,field
from types import MappingProxyType
from typing import Iterable,Mapping,NamedTuple
from .group_2o import DIRECTIONS

Address=tuple[int,int,int,int]
class Channel(NamedTuple):
    a:int
    b:int
    r:int
VACUUM=Channel(0,0,2)

def channel(value:Iterable[int])->Channel:
    values=tuple(value)
    if len(values)!=3 or any(type(x) is not int for x in values):
        raise TypeError("Expected exactly three Python integers")
    if not 0<=values[2]<6:
        raise ValueError("Remainder must be 0..5")
    return Channel(*values)

@dataclass(frozen=True,slots=True)
class Cube:
    side:int
    def __post_init__(self):
        if type(self.side) is not int or self.side<3:
            raise ValueError("side must be an integer >=3")
    @property
    def node_count(self):
        return self.side**3
    def validate_address(self,value)->Address:
        addr=tuple(value)
        if len(addr)!=4 or any(type(x) is not int for x in addr):
            raise TypeError("Address must be four integers")
        if not all(0<=x<self.side for x in addr[:3]) or not 0<=addr[3]<48:
            raise ValueError("Address outside cube/channel range")
        return addr
    def adjacent(self,address:Address,direction:int,sender:int)->Address:
        dx,dy,dz=DIRECTIONS[direction]
        x,y,z,_=address
        return ((x+dx)%self.side,(y+dy)%self.side,(z+dz)%self.side,sender)

@dataclass(frozen=True,slots=True)
class State:
    cube:Cube
    background:Channel=VACUUM
    cells:Mapping[Address,Channel]=field(default_factory=dict)
    def __post_init__(self):
        if not isinstance(self.cube,Cube):
            raise TypeError("Expected Cube")
        bg=channel(self.background)
        if bg.a or bg.b:
            raise ValueError("Sparse background must have a=b=0")
        data={}
        for address,values in self.cells.items():
            key=self.cube.validate_address(address)
            value=channel(values)
            if value!=bg: data[key]=value
        object.__setattr__(self,"background",bg)
        object.__setattr__(self,"cells",MappingProxyType(data))
    def at(self,address:Address)->Channel:
        key=self.cube.validate_address(address)
        return self.cells.get(key,self.background)
    def node(self,position):
        if len(position)!=3: raise ValueError("Expected three coordinates")
        return tuple(self.at((*position,g)) for g in range(48))
