"""Bounded rational quantities with positive-coded payloads and dimensional vectors."""

from dataclasses import dataclass
from math import gcd

LIMIT = (1 << 30) - 1
WORK_LIMIT = (1 << 63) - 1


def checked(value):
    if type(value) is not int or abs(value) > WORK_LIMIT:
        raise OverflowError("Working integer exceeds signed 64-bit bounds")
    return value


@dataclass(frozen=True)
class Rational:
    code: int
    denominator: int

    def __post_init__(self):
        if type(self.code) is not int or not 1 <= self.code <= 2 * LIMIT + 1:
            raise ValueError("Invalid positive numerator code")
        if type(self.denominator) is not int or not 1 <= self.denominator <= LIMIT:
            raise ValueError("Invalid positive denominator")
        if gcd(abs(self.numerator), self.denominator) != 1:
            raise ValueError("Payload must be reduced")

    @property
    def numerator(self):
        return self.code // 2 if self.code % 2 else -(self.code // 2)

    @classmethod
    def make(cls, numerator, denominator=1):
        checked(numerator)
        checked(denominator)
        if denominator == 0:
            raise ZeroDivisionError("Zero rational denominator")
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        factor = gcd(numerator, denominator)
        numerator, denominator = numerator // factor, denominator // factor
        if abs(numerator) > LIMIT or denominator > LIMIT:
            raise OverflowError("Reduced rational exceeds payload bounds")
        return cls(2 * abs(numerator) + int(numerator >= 0), denominator)

    def __add__(self, other):
        return Rational.make(
            checked(
                checked(self.numerator * other.denominator) + checked(other.numerator * self.denominator)
            ),
            checked(self.denominator * other.denominator),
        )

    def __neg__(self):
        return Rational.make(-self.numerator, self.denominator)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        return Rational.make(
            checked(self.numerator * other.numerator),
            checked(self.denominator * other.denominator),
        )

    def __truediv__(self, other):
        return Rational.make(
            checked(self.numerator * other.denominator),
            checked(self.denominator * other.numerator),
        )

    def __lt__(self, other):
        return checked(self.numerator * other.denominator) < checked(other.numerator * self.denominator)

    def json(self):
        return {"code": self.code, "denominator": self.denominator}


ZERO = Rational.make(0)
ONE = Rational.make(1)


def rational(value):
    if type(value) is int:
        return Rational.make(value)
    if isinstance(value, dict) and set(value) == {"n", "d"}:
        return Rational.make(value["n"], value["d"])
    raise ValueError("Use an integer or an explicit {n,d} rational")


@dataclass(frozen=True)
class Quantity:
    components: tuple[Rational, ...]
    dimension: tuple[int, int] = (0, 0)

    def __post_init__(self):
        if not isinstance(self.components, tuple) or not all(
            isinstance(v, Rational) for v in self.components
        ):
            raise ValueError("Components must be immutable rational payloads")
        if len(self.components) not in (1, 3):
            raise ValueError("Only scalars and three-vectors are supported")
        if len(self.dimension) != 2 or any(type(x) is not int or abs(x) > 32 for x in self.dimension):
            raise ValueError("Invalid bounded dimension")

    def same(self, other):
        if self.dimension != other.dimension or len(self.components) != len(other.components):
            raise ValueError("Incompatible dimensions or component counts")

    def add(self, other):
        self.same(other)
        return Quantity(
            tuple(a + b for a, b in zip(self.components, other.components, strict=True)),
            self.dimension,
        )

    def neg(self):
        return Quantity(tuple(-a for a in self.components), self.dimension)

    def sub(self, other):
        return self.add(other.neg())

    def mul(self, other):
        if len(self.components) != 1 and len(other.components) != 1:
            raise ValueError("Vector products must explicitly select dot or cross")
        size = max(len(self.components), len(other.components))
        left = self.components * size if len(self.components) == 1 else self.components
        right = other.components * size if len(other.components) == 1 else other.components
        return Quantity(
            tuple(a * b for a, b in zip(left, right, strict=True)),
            tuple(a + b for a, b in zip(self.dimension, other.dimension, strict=True)),
        )

    def div(self, other):
        if len(other.components) != 1:
            raise ValueError("Division requires a scalar divisor")
        return Quantity(
            tuple(a / other.components[0] for a in self.components),
            tuple(a - b for a, b in zip(self.dimension, other.dimension, strict=True)),
        )

    def dot(self, other):
        if len(self.components) != 3 or len(other.components) != 3:
            raise ValueError("Dot product requires two three-vectors")
        result = ZERO
        for a, b in zip(self.components, other.components, strict=True):
            result = result + a * b
        return Quantity(
            (result,), tuple(a + b for a, b in zip(self.dimension, other.dimension, strict=True))
        )

    def cross(self, other):
        if len(self.components) != 3 or len(other.components) != 3:
            raise ValueError("Cross product requires two three-vectors")
        a, b = self.components, other.components
        return Quantity(
            (
                a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0],
            ),
            tuple(x + y for x, y in zip(self.dimension, other.dimension, strict=True)),
        )

    def json(self):
        return {
            "dimension": list(self.dimension),
            "payload": [v.json() for v in self.components],
        }


def literal(value, dimension=(0, 0)):
    values = value if isinstance(value, list) else [value]
    return Quantity(tuple(rational(v) for v in values), tuple(dimension))


def evaluate(node, context, units, budget=None, depth=0):
    """A small bounded AST; no eval, callback, imports or remote state references."""
    budget = [0] if budget is None else budget
    budget[0] += 1
    if budget[0] > 128 or depth > 16:
        raise ValueError("Expression budget exceeded")
    if not isinstance(node, dict):
        return literal(node)
    if set(node) == {"ref"}:
        return context[node["ref"]]
    if "value" in node:
        if set(node) - {"value", "unit"}:
            raise ValueError("Unknown literal keys")
        return literal(node["value"], units[node.get("unit", "one")])
    if set(node) != {"op", "args"}:
        raise ValueError("Invalid expression node")
    op, args = node["op"], node["args"]
    arity = 1 if op in ("neg", "norm2") else 2
    if not isinstance(args, list) or len(args) != arity:
        raise ValueError("Invalid expression arity")
    values = [evaluate(a, context, units, budget, depth + 1) for a in args]
    if not all(isinstance(q, Quantity) for q in values):
        raise ValueError("Arithmetic requires quantities")
    a = values[0]
    if op == "neg":
        return a.neg()
    if op == "norm2":
        return a.dot(a)
    b = values[1]
    if op == "eq":
        a.same(b)
        return a == b
    if op == "gt":
        a.same(b)
        if len(a.components) != 1:
            raise ValueError("Comparison requires scalars")
        return b.components[0] < a.components[0]
    methods = {
        "add": Quantity.add,
        "sub": Quantity.sub,
        "mul": Quantity.mul,
        "div": Quantity.div,
        "dot": Quantity.dot,
        "cross": Quantity.cross,
    }
    if op not in methods:
        raise ValueError("Unsupported expression operation")
    return methods[op](a, b)
