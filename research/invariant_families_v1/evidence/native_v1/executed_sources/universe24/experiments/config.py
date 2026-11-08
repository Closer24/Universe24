"""Data-only initial states and checkpoints. No runtime injections."""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
from ..core import Coupling,Cube,Engine,State,VACUUM
from ..core.state import channel

def _keys(data,allowed,required):
    if not isinstance(data,dict): raise TypeError("Expected JSON object")
    if set(data)-allowed: raise ValueError(f"Unsupported keys: {sorted(set(data)-allowed)}")
    if required-set(data): raise ValueError(f"Missing keys: {sorted(required-set(data))}")

@dataclass(frozen=True,slots=True)
class Experiment:
    engine:Engine
    initial:State
    steps:int
    def __post_init__(self):
        if not isinstance(self.engine,Engine) or not isinstance(self.initial,State):
            raise TypeError("Expected Engine and State")
        if type(self.steps) is not int or self.steps<0:
            raise ValueError("steps must be nonnegative")

def from_dict(data:dict[str,Any])->Experiment:
    _keys(data,{"side","coupling_signs","background","seed_changes","steps"},{"side"})
    cube=Cube(data["side"])
    engine=Engine(Coupling(tuple(data.get("coupling_signs",[1,1,1]))))
    background=channel(data.get("background",VACUUM))
    cells={}
    changes=data.get("seed_changes",[])
    if not isinstance(changes,list): raise TypeError("seed_changes must be list")
    for entry in changes:
        _keys(entry,{"position","channel","state"},{"position","channel","state"})
        if not isinstance(entry["position"],(tuple,list)) or len(entry["position"])!=3:
            raise ValueError("position must have three coordinates")
        address=cube.validate_address((*entry["position"],entry["channel"]))
        if address in cells: raise ValueError(f"Duplicate seed address: {address}")
        cells[address]=channel(entry["state"])
    return Experiment(engine,State(cube,background,cells),data.get("steps",0))

def load(path:str|Path)->Experiment:
    with Path(path).open(encoding="utf-8") as handle:
        return from_dict(json.load(handle))

def checkpoint_data(state:State,engine:Engine,completed_steps:int)->dict:
    if type(completed_steps) is not int or completed_steps<0:
        raise ValueError("Invalid steps")
    return {"format":"universe24-checkpoint-v1","completed_steps":completed_steps,
            "coupling_fingerprint":engine.coupling.fingerprint,
            "experiment":{"side":state.cube.side,
                          "coupling_signs":list(engine.coupling.body_signs),
                          "background":list(state.background),"steps":0,
                          "seed_changes":[{"position":list(addr[:3]),"channel":addr[3],"state":list(s)}
                                          for addr,s in sorted(state.cells.items())]}}

def read_checkpoint(path:str|Path):
    with Path(path).open(encoding="utf-8") as handle: data=json.load(handle)
    _keys(data,{"format","completed_steps","coupling_fingerprint","experiment"},
          {"format","completed_steps","coupling_fingerprint","experiment"})
    if data["format"]!="universe24-checkpoint-v1": raise ValueError("Bad checkpoint format")
    experiment=from_dict(data["experiment"])
    if data["coupling_fingerprint"]!=experiment.engine.coupling.fingerprint:
        raise ValueError("Coupling fingerprint mismatch")
    n=data["completed_steps"]
    if type(n) is not int or n<0: raise ValueError("Bad step index")
    return experiment.engine,experiment.initial,n
