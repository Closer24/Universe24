"""Exact binary octahedral group 2O. Construction-time mathematics, no evolution gates."""
from dataclasses import dataclass
from functools import lru_cache

Pair = tuple[int, int]
Quaternion = tuple[Pair, Pair, Pair, Pair]
Vector = tuple[int, int, int]
Matrix3 = tuple[Vector, Vector, Vector]
ZERO = (0, 0)
ONE = (2, 0)
ROOT_HALF = (0, 1)
IDENTITY = (ONE, ZERO, ZERO, ZERO)
QX = (ROOT_HALF, ROOT_HALF, ZERO, ZERO)
QY = (ROOT_HALF, ZERO, ROOT_HALF, ZERO)
QZ = (ROOT_HALF, ZERO, ZERO, ROOT_HALF)
DIRECTIONS = ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
_TERMS = (
    ((0,0,1),(1,1,-1),(2,2,-1),(3,3,-1)),
    ((0,1,1),(1,0,1),(2,3,1),(3,2,-1)),
    ((0,2,1),(1,3,-1),(2,0,1),(3,1,1)),
    ((0,3,1),(1,2,1),(2,1,-1),(3,0,1)),
)

def multiply(q: Quaternion, h: Quaternion) -> Quaternion:
    out = []
    for terms in _TERMS:
        a = b = 0
        for i,j,sign in terms:
            c,d = q[i]
            e,f = h[j]
            a += sign*(c*e + 2*d*f)
            b += sign*(c*f + d*e)
        if a%2 or b%2:
            raise ArithmeticError("Unexpected quaternion representation")
        out.append((a//2,b//2))
    return tuple(out)

def conjugate(q: Quaternion) -> Quaternion:
    return (q[0],) + tuple((-a,-b) for a,b in q[1:])

def rotate(matrix: Matrix3, vector: Vector) -> Vector:
    return tuple(sum(matrix[i][j]*vector[j] for j in range(3)) for i in range(3))

def rotate_inverse(matrix: Matrix3, vector: Vector) -> Vector:
    return tuple(sum(matrix[j][i]*vector[j] for j in range(3)) for i in range(3))

@dataclass(frozen=True, slots=True)
class Group2O:
    quaternions: tuple[Quaternion,...]
    multiplication: tuple[tuple[int,...],...]
    inverses: tuple[int,...]
    rotations: tuple[Matrix3,...]
    central: int
    def power(self,g:int,n:int)->int:
        if type(g) is not int or not 0<=g<48 or type(n) is not int:
            raise ValueError("Bad group label or power")
        if n<0:
            g,n=self.inverses[g],-n
        ans=0
        while n:
            if n&1: ans=self.multiplication[ans][g]
            g=self.multiplication[g][g]
            n//=2
        return ans

@lru_cache(maxsize=1)
def group()->Group2O:
    qs=[IDENTITY]
    labels={IDENTITY:0}
    for q in qs:
        for generator in (QX,QY):
            h=multiply(q,generator)
            if h not in labels:
                labels[h]=len(qs)
                qs.append(h)
    if len(qs)!=48:
        raise ArithmeticError("Expected 48 2O elements")
    table=tuple(tuple(labels[multiply(q,h)] for h in qs) for q in qs)
    inverses=tuple(labels[conjugate(q)] for q in qs)
    rotations=[]
    for q in qs:
        columns=[]
        for axis in range(3):
            basis=[ZERO]*4
            basis[axis+1]=ONE
            v=multiply(multiply(q,tuple(basis)),conjugate(q))
            if v[0]!=ZERO or any(b!=0 or a%2 for a,b in v[1:]):
                raise ArithmeticError("Nonintegral cube rotation")
            columns.append(tuple(a//2 for a,_ in v[1:]))
        rotations.append(tuple(tuple(columns[j][i] for j in range(3)) for i in range(3)))
    central=labels[((-2,0),ZERO,ZERO,ZERO)]
    if central!=14:
        raise ArithmeticError("Unexpected group ordering")
    return Group2O(tuple(qs),table,inverses,tuple(rotations),central)
