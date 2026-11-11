"""Finite-horizon rational arithmetic compiled into the unchanged Rule3 Engine.

Only construction/initialization/readout happen here. A travelling retained
clock gives each arithmetic register two opposite impulses; after both, its
value is stationary. All runtime operations are fixed integer polynomials.
"""
from dataclasses import dataclass
from fractions import Fraction
from collections import Counter
from functools import reduce
from math import gcd
import numpy as np
from universe24.core import Tensor, State
from universe24.core.lattice import ZERO


@dataclass(frozen=True)
class Term:
    coefficient: int
    wire: int | None = None


class Circuit:
    def __init__(self):
        self.nodes = []
        self.cache = {}
        self.factor_cache = {}
        self.inputs = {}

    def node(self, key):
        if key not in self.cache:
            self.cache[key] = len(self.nodes)
            self.nodes.append(key)
        return Term(1, self.cache[key])

    def input(self, name, scale=1):
        value = self.node(('input', name))
        self.inputs[name] = value.wire
        return Rational(self, value, Term(scale))

    def factors(self, value):
        if value.wire is None:
            return value.coefficient, Counter()
        wire = value.wire
        if wire not in self.factor_cache:
            node = self.nodes[wire]
            if node[0] == 'mul':
                _, a = self.factors(Term(1, node[1]))
                _, b = self.factors(Term(1, node[2]))
                self.factor_cache[wire] = a+b
            else:
                self.factor_cache[wire] = Counter({wire: 1})
        return value.coefficient, self.factor_cache[wire].copy()

    def product(self, coefficient, factors):
        if coefficient == 0:
            return Term(0)
        values = [Term(1, w) for w, power in sorted(factors.items()) for _ in range(power)]
        # Balanced products avoid a depth proportional to a denominator power.
        while len(values) > 1:
            values = [self.mul(values[i], values[i+1]) if i+1 < len(values) else values[i]
                      for i in range(0, len(values), 2)]
        return Term(coefficient, values[0].wire) if values else Term(coefficient)

    def mul(self, a, b):
        coefficient = a.coefficient*b.coefficient
        if coefficient == 0:
            return Term(0)
        if a.wire is None:
            return Term(coefficient, b.wire)
        if b.wire is None:
            return Term(coefficient, a.wire)
        result = self.node(('mul', *sorted((a.wire, b.wire))))
        return Term(coefficient, result.wire)

    def add(self, *values):
        values = [v for v in values if v.coefficient]
        if not values:
            return Term(0)
        factored = [self.factors(v) for v in values]
        common = factored[0][1].copy()
        for _, fac in factored[1:]:
            common &= fac
        coefficient = reduce(gcd, (abs(c) for c, _ in factored))
        terms = Counter()
        for c, fac in factored:
            v = self.product(c//coefficient, fac-common)
            terms[v.wire] += v.coefficient
        terms = tuple(sorted(((w, c) for w, c in terms.items() if c), key=lambda v: -1 if v[0] is None else v[0]))
        if not terms:
            return Term(0)
        if len(terms) == 1:
            rest = Term(terms[0][1], terms[0][0])
        else:
            rest = self.node(('add', terms))
        return self.mul(self.product(coefficient, common), rest)

    def shift(self, value, offset):
        if value.wire is None or not value.coefficient:
            return value
        shifted = self.node(('shift', value.wire, tuple(offset)))
        return Term(value.coefficient, shifted.wire)

    def rational(self, value):
        if isinstance(value, Rational):
            if value.circuit is not self:
                raise ValueError('different circuits')
            return value
        value = Fraction(value)
        return Rational(self, Term(value.numerator), Term(value.denominator))

    def dependencies(self, wire):
        node = self.nodes[wire]
        if node[0] == 'mul':
            return node[1:]
        if node[0] == 'add':
            return tuple(w for w, _ in node[1] if w is not None)
        if node[0] == 'shift':
            return (node[1],)
        return ()

    def compile(self, outputs, Q=1):
        """Prune unused arithmetic and assign two Engine ticks per DAG level."""
        wanted = set(self.inputs.values())
        pending = [v.wire for r in outputs.values() for v in (r.num, r.den) if v.wire is not None]
        while pending:
            wire = pending.pop()
            if wire in wanted:
                continue
            wanted.add(wire)
            pending.extend(self.dependencies(wire))
        ordered = sorted(wanted)
        names = {wire: f'arithmetic.w{wire}' for wire in ordered}
        ready = {}
        for wire in ordered:
            ready[wire] = 0 if self.nodes[wire][0] == 'input' else 2+max((ready[v] for v in self.dependencies(wire)), default=0)
        ticks = max(ready.values(), default=0)
        period = ticks+3  # No clock wraps onto an arithmetic pulse inside the declared horizon.
        clocks = [f'clock.c{i}' for i in range(period)]
        D = 6*Q
        terms = []
        factor = lambda name, offset=ZERO: (name, offset, 'b')
        why = {'designated_one_way': 'Finite arithmetic circuit implementing a declared ADM integrator; clock and workspace have no physical stress-energy.'}
        for wire in ordered:
            name = names[wire]
            terms.append((name, D, (factor(name),)))
            node = self.nodes[wire]
            if node[0] == 'input':
                continue
            start = ready[wire]-2
            clock = factor(clocks[(-start) % period])
            if node[0] == 'mul':
                terms.append((name, D//2, (clock, factor(names[node[1]]), factor(names[node[2]])), why))
            elif node[0] == 'add':
                for parent, coefficient in node[1]:
                    factors = (clock,) if parent is None else (clock, factor(names[parent]))
                    terms.append((name, D//2*coefficient, factors, why))
            elif node[0] == 'shift':
                terms.append((name, D//2, (clock, factor(names[node[1]], node[2])), why))
        for j, name in enumerate(clocks):
            for other in ((j-1) % period, (j+1) % period):
                terms.append((name, D//2, (factor(clocks[other]),), why))
        # Canonical factors sort by gear index. Put the clock first so an
        # inactive gate multiplies by zero BEFORE multiplying large parents.
        # This changes no circuit equation and needs no Engine special case.
        tensor = Tensor(clocks+[names[w] for w in ordered], terms, Q=Q, strict_support=True)
        return Compiled(self, tensor, outputs, names, ready, ticks, period, Q)


class Rational:
    def __init__(self, circuit, num, den):
        if den.coefficient == 0:
            raise ZeroDivisionError('identically zero symbolic denominator')
        self.circuit = circuit
        if num.coefficient == 0:
            self.num, self.den = Term(0), Term(1)
            return
        nc, nf = circuit.factors(num)
        dc, df = circuit.factors(den)
        common = nf & df
        divisor = gcd(abs(nc), abs(dc))*(1 if dc > 0 else -1)
        self.num = circuit.product(nc//divisor, nf-common)
        self.den = circuit.product(dc//divisor, df-common)

    def __add__(self, other):
        c = self.circuit
        other = c.rational(other)
        if self.den == other.den:
            return Rational(c, c.add(self.num, other.num), self.den)
        ac, af = c.factors(self.den)
        bc, bf = c.factors(other.den)
        common = af & bf
        divisor = gcd(ac, bc)
        a = c.product(ac//divisor, af-common)
        b = c.product(bc//divisor, bf-common)
        return Rational(c, c.add(c.mul(self.num, b), c.mul(other.num, a)), c.mul(self.den, b))

    __radd__ = __add__

    def __neg__(self):
        return Rational(self.circuit, Term(-self.num.coefficient, self.num.wire), self.den)

    def __sub__(self, other):
        return self + (-self.circuit.rational(other))

    def __rsub__(self, other):
        return self.circuit.rational(other) + (-self)

    def __mul__(self, other):
        c = self.circuit
        other = c.rational(other)
        return Rational(c, c.mul(self.num, other.num), c.mul(self.den, other.den))

    __rmul__ = __mul__

    def __truediv__(self, other):
        c = self.circuit
        other = c.rational(other)
        return Rational(c, c.mul(self.num, other.den), c.mul(self.den, other.num))

    def __rtruediv__(self, other):
        return self.circuit.rational(other)/self

    def __pow__(self, power):
        if type(power) is not int or power < 0:
            raise ValueError('nonnegative integer powers only')
        result = self.circuit.rational(1)
        for _ in range(power):
            result *= self
        return result

    def shift(self, offset):
        c = self.circuit
        # Distribute shifts over denominator factors, retaining cancellation.
        coefficient, factors = c.factors(self.den)
        den = Term(coefficient)
        for wire, power in factors.items():
            for _ in range(power):
                den = c.mul(den, c.shift(Term(1, wire), offset))
        return Rational(c, c.shift(self.num, offset), den)


@dataclass
class Compiled:
    circuit: Circuit
    tensor: Tensor
    outputs: dict
    names: dict
    ready: dict
    ticks: int
    period: int
    Q: int

    def prepare(self, L, integer_inputs):
        if set(integer_inputs) != set(self.circuit.inputs):
            raise ValueError('all declared integer inputs are required')
        b = np.zeros((self.tensor.G, L**3), dtype=object)
        for name, wire in self.circuit.inputs.items():
            b[self.tensor.gear_index(self.names[wire])] = np.asarray(integer_inputs[name], dtype=object).reshape(-1)
        a = b.copy()
        pulse = lambda j: 1 if j % self.period == 0 else (-1 if j % self.period == 1 else 0)
        for j in range(self.period):
            gear = self.tensor.gear_index(f'clock.c{j}')
            b[gear] = pulse(j)
            a[gear] = pulse(j-1)
        r = (17*np.arange(b.size).reshape(b.shape)+5) % (6*self.Q)
        return State(L, a, b, r)

    def read(self, state, name, node=0):
        def value(term):
            return term.coefficient if term.wire is None else term.coefficient*int(state.b[self.tensor.gear_index(self.names[term.wire]), node])
        result = self.outputs[name]
        return Fraction(value(result.num), value(result.den))

    def evaluate_integer_dag(self, state):
        """Read-only independent arithmetic oracle, NEVER used to step a state."""
        values = {}
        for wire in sorted(self.names):
            node = self.circuit.nodes[wire]
            if node[0] == 'input':
                values[wire] = state.b[self.tensor.gear_index(self.names[wire])].astype(object)
            elif node[0] == 'mul':
                values[wire] = values[node[1]]*values[node[2]]
            elif node[0] == 'add':
                values[wire] = sum(coefficient*(1 if parent is None else values[parent]) for parent, coefficient in node[1])
            elif node[0] == 'shift':
                values[wire] = values[node[1]][state.lattice.shift_index(node[2])]
        return values
