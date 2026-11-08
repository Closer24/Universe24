"""Independent 4x4 exact-matrix construction of the specified binary octahedral group.

No production imports or copied multiplication/routing tables. Arithmetic uses
rational polynomials modulo x*x-2, rather than the core's scaled quaternion
product. The closed-form 48-element set is checked against generator closure;
BFS with Cx then Cy is used only for the documented channel-label convention.
"""
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


@dataclass(frozen=True, slots=True)
class Radical:
    """a + b*sqrt(2), with exact rational coefficients."""
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        return Radical(self.a + other.a, self.b + other.b)

    def __neg__(self):
        return Radical(-self.a, -self.b)

    def __mul__(self, other):
        return Radical(self.a*other.a + 2*self.b*other.b,
                       self.a*other.b + self.b*other.a)

    def integer(self):
        if self.b or self.a.denominator != 1:
            raise ValueError('Not an integer')
        return int(self.a)


ZERO = Radical()
ONE = Radical(Fraction(1))
HALF = Radical(Fraction(1, 2))
ROOT_HALF = Radical(Fraction(0), Fraction(1, 2))
DIRECTIONS = ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1))


def transpose(matrix):
    return tuple(zip(*matrix))


def matmul(left, right):
    """Ordinary matrix multiplication over the quadratic field."""
    cols = transpose(right)
    return tuple(tuple(sum((a*b for a,b in zip(row,col)), ZERO)
                       for col in cols) for row in left)


def left_matrix(coordinates):
    """Matrix C(q) from appendix A4; used without quaternion multiplication."""
    w,x,y,z = coordinates
    return ((w,-x,-y,-z), (x,w,-z,y), (y,z,w,-x), (z,-y,x,w))


IDENTITY = left_matrix((ONE,ZERO,ZERO,ZERO))
CX = left_matrix((ROOT_HALF,ROOT_HALF,ZERO,ZERO))
CY = left_matrix((ROOT_HALF,ZERO,ROOT_HALF,ZERO))
CZ = left_matrix((ROOT_HALF,ZERO,ZERO,ROOT_HALF))


def explicit_matrices():
    """8 coordinate units + 16 half-sign vectors + 24 paired root-half vectors."""
    result = set()
    for axis in range(4):
        for sign in (-1,1):
            q = [ZERO]*4
            q[axis] = ONE if sign == 1 else -ONE
            result.add(left_matrix(q))
    for signs in product((-1,1), repeat=4):
        result.add(left_matrix(tuple(HALF if s == 1 else -HALF for s in signs)))
    for i,j in combinations(range(4),2):
        for si,sj in product((-1,1),repeat=2):
            q = [ZERO]*4
            q[i] = ROOT_HALF if si == 1 else -ROOT_HALF
            q[j] = ROOT_HALF if sj == 1 else -ROOT_HALF
            result.add(left_matrix(q))
    return frozenset(result)


@dataclass(frozen=True)
class MatrixAlgebra:
    matrices: tuple
    multiplication: tuple
    inverses: tuple
    rotations: tuple
    central: int


@lru_cache(maxsize=1)
def algebra():
    expected = explicit_matrices()
    if len(expected) != 48:
        raise ArithmeticError('Closed-form set is not 48 elements')
    matrices = [IDENTITY]
    labels = {IDENTITY: 0}
    for matrix in matrices:
        for generator in (CX,CY):
            nxt = matmul(matrix,generator)
            if nxt not in expected:
                raise ArithmeticError('Generator escaped closed-form group')
            if nxt not in labels:
                labels[nxt] = len(matrices)
                matrices.append(nxt)
    if frozenset(matrices) != expected:
        raise ArithmeticError('Generator closure differs from explicit group')
    multiplication = tuple(tuple(labels[matmul(a,b)] for b in matrices)
                           for a in matrices)
    inverses = tuple(labels[transpose(m)] for m in matrices)
    basis=[]
    for axis in range(3):
        q=[ZERO]*4;q[axis+1]=ONE
        basis.append(left_matrix(q))
    rotations=[]
    for m in matrices:
        cols=[]
        for unit in basis:
            transformed=matmul(matmul(m,unit),transpose(m))
            if transformed[0][0] != ZERO:
                raise ArithmeticError('Non-spatial conjugated unit')
            cols.append(tuple(transformed[i][0].integer() for i in (1,2,3)))
        rotations.append(tuple(zip(*cols)))
    minus_identity=tuple(tuple(-v for v in row) for row in IDENTITY)
    return MatrixAlgebra(tuple(matrices),multiplication,inverses,tuple(rotations),
                         labels[minus_identity])


@dataclass(frozen=True)
class MatrixCoupling:
    ports: tuple
    weights: tuple


@lru_cache(maxsize=8)
def coupling(signs=(1,1,1)):
    if len(signs)!=3 or any(type(s) is not int or s not in (-1,1) for s in signs):
        raise ValueError('Three integer signs are required')
    group=algebra();labels={m:i for i,m in enumerate(group.matrices)}
    z3=matmul(matmul(CZ,CZ),CZ)
    actions=(IDENTITY,IDENTITY,CY,transpose(CY),z3,transpose(z3))
    routes=[];weights=[]
    for d in DIRECTIONS:
        row=[];sign_row=[]
        for m,rot in zip(group.matrices,group.rotations):
            body=tuple(sum(rot[j][i]*d[j] for j in range(3)) for i in range(3))
            axis=DIRECTIONS.index(body)
            row.append(labels[matmul(m,actions[axis])])
            sign_row.append(signs[axis//2])
        routes.append(tuple(row));weights.append(tuple(sign_row))
    return MatrixCoupling(tuple(routes),tuple(weights))
