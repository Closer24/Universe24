"""Fixed signed spatial coupling, derived from 2O, with exactly six spatial ports."""
from dataclasses import dataclass, field
from functools import lru_cache
import hashlib
import json
from .group_2o import DIRECTIONS, IDENTITY, QY, QZ, conjugate, group, multiply, rotate_inverse

@dataclass(frozen=True, slots=True)
class Coupling:
    body_signs: tuple[int,int,int]=(1,1,1)
    ports: tuple[tuple[int,...],...]=field(init=False,repr=False)
    weights: tuple[tuple[int,...],...]=field(init=False,repr=False)

    def __post_init__(self):
        signs=tuple(self.body_signs)
        if len(signs)!=3 or any(type(s) is not int or s not in (-1,1) for s in signs):
            raise ValueError("body_signs must be exactly three +/-1 integers")
        object.__setattr__(self,"body_signs",signs)
        algebra=group()
        ids={q:i for i,q in enumerate(algebra.quaternions)}
        qz3=multiply(multiply(QZ,QZ),QZ)
        actions=(IDENTITY,IDENTITY,QY,conjugate(QY),qz3,conjugate(qz3))
        rows,weights=[],[]
        for direction in DIRECTIONS:
            row,weight=[],[]
            for g,rotation in enumerate(algebra.rotations):
                u=DIRECTIONS.index(rotate_inverse(rotation,direction))
                row.append(algebra.multiplication[g][ids[actions[u]]])
                weight.append(signs[u//2])
            rows.append(tuple(row))
            weights.append(tuple(weight))
        object.__setattr__(self,"ports",tuple(rows))
        object.__setattr__(self,"weights",tuple(weights))
        self.validate()

    def validate(self):
        for d in range(6):
            if sorted(self.ports[d])!=list(range(48)):
                raise ValueError("Each directional coupling must be a signed permutation")
            for g in range(48):
                h=self.ports[d][g]
                if self.ports[d^1][h]!=g or self.weights[d^1][h]!=self.weights[d][g]:
                    raise ValueError("Nonreciprocal connection")

    def matrix(self,d:int)->tuple[tuple[int,...],...]:
        if type(d) is not int or not 0<=d<6:
            raise ValueError("Direction must be 0..5")
        return tuple(tuple(self.weights[d][g] if h==self.ports[d][g] else 0
                           for h in range(48)) for g in range(48))

    def positive_matrices(self):
        return tuple(self.matrix(d) for d in (0,2,4))

    def tensor(self):
        return tuple(self.matrix(d) for d in range(6))

    @property
    def fingerprint(self):
        blob=json.dumps(["universe24-2O-body-013-v1",self.ports,self.weights],separators=(",",":")).encode()
        return hashlib.sha256(blob).hexdigest()

@lru_cache(maxsize=8)
def coupling(body_signs=(1,1,1)):
    return Coupling(body_signs)
