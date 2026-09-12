"""Independent, bounded mechanism prototype. All physical laws live in JSON."""

from dataclasses import dataclass
from math import lcm

from .algebra import ONE, ZERO, Quantity, Rational, evaluate, literal


@dataclass(frozen=True)
class Record:
    kind: str
    fields: tuple


class Lab:
    def __init__(self, definitions):
        limits = definitions["limits"]
        required = {
            "cell_capacity",
            "max_participants",
            "max_products",
            "link_capacity",
            "match_attempts",
        }
        if set(limits) != required or any(type(v) is not int or v < 1 for v in limits.values()):
            raise ValueError("Limits must be positive configuration integers")
        self.definitions = definitions
        self.capacity = limits["cell_capacity"]
        for rule in definitions["reactions"].values():
            if (
                len(rule["inputs"]) > limits["max_participants"]
                or len(rule["outputs"]) > limits["max_products"]
            ):
                raise ValueError("Reaction exceeds configured participant/product limits")
            aliases = [spec["alias"] for spec in rule["inputs"]]
            if len(set(aliases)) != len(aliases):
                raise ValueError("Duplicate input alias")
            for spec in rule["inputs"]:
                if not spec["types"] or any(kind not in definitions["types"] for kind in spec["types"]):
                    raise ValueError("Each input must explicitly list known allowed types")
        self.cells = {}
        self.links = ()
        self.next_id = 0

    def context(self, record):
        spec = self.definitions["types"][record.kind]
        context = dict(record.fields)
        if len(record.fields) > 16 or len(context) != len(record.fields):
            raise ValueError("Too many or duplicate fields")
        if set(context) != set(spec["fields"]):
            raise ValueError("Missing or extra entity fields")
        for name, field in spec["fields"].items():
            q = context[name]
            if not isinstance(q, Quantity):
                raise TypeError("Entity fields must be quantities")
            if (
                q.dimension != tuple(self.definitions["units"][field["unit"]])
                or len(q.components) != field["size"]
            ):
                raise ValueError("Invalid field unit or shape")
        derived = spec.get("derived", {})
        if len(derived) > 16 or len(spec.get("constraints", [])) > 16:
            raise ValueError("Type formula budget exceeded")
        for name, expr in derived.items():
            if name in context:
                raise ValueError("Derived field overwrites a stored field")
            context[name] = self.eval(expr, context)
        for expr in spec.get("constraints", []):
            if self.eval(expr, context) is not True:
                raise ValueError("Entity constraint failed")
        return context

    def eval(self, expression, context):
        return evaluate(expression, context, self.definitions["units"])

    def record(self, kind, values):
        spec = self.definitions["types"][kind]
        record = Record(
            kind,
            tuple(
                (
                    name,
                    value
                    if isinstance(value, Quantity)
                    else literal(value, self.definitions["units"][spec["fields"][name]["unit"]]),
                )
                for name, value in values.items()
            ),
        )
        self.context(record)
        return record

    def insert(self, cell, record):
        self.context(record)
        current = self.cells.get(cell, ())
        if len(current) >= self.capacity:
            raise ValueError("Cell capacity exceeded")
        identifier = self.next_id
        self.cells[cell] = current + ((identifier, record),)
        self.next_id += 1
        return identifier

    def totals(self, records=None):
        if records is None:
            records = [r for occupants in self.cells.values() for _, r in occupants]
            records += [r for _, _, _, r in self.links]
        totals = {
            name: self.eval(spec["zero"], {}) for name, spec in self.definitions["balances"].items()
        }
        for record in records:
            context = self.context(record)
            for name, spec in self.definitions["balances"].items():
                totals[name] = totals[name].add(self.eval(spec["expression"], context))
        return totals

    def react(self, cell, rule_name, identifiers, parameters=None):
        rule = self.definitions["reactions"][rule_name]
        inputs, outputs = rule["inputs"], rule["outputs"]
        limits = self.definitions["limits"]
        if len(inputs) > limits["max_participants"] or len(outputs) > limits["max_products"]:
            raise ValueError("Reaction exceeds configured participant/product limits")
        if len(rule.get("let", {})) > 16:
            raise ValueError("Expression budget exceeded")
        if len(identifiers) != len(inputs) or len(set(identifiers)) != len(identifiers):
            raise ValueError("Invalid participant list")
        occupants = self.cells.get(cell, ())
        local = dict(occupants)
        participants = [local[i] for i in identifiers]  # remote records are inaccessible
        # Caller order is irrelevant. Bind each distinct record to one allowed role.
        ordered = sorted(zip(identifiers, participants, strict=True), key=lambda pair: pair[0])
        attempts = [0]

        def bind(index, remaining):
            if index == len(inputs):
                return []
            for offset, (_, record) in enumerate(remaining):
                attempts[0] += 1
                if attempts[0] > limits["match_attempts"]:
                    raise ValueError("Configured matching work budget exceeded")
                if record.kind in inputs[index]["types"]:
                    rest = bind(index + 1, remaining[:offset] + remaining[offset + 1 :])
                    if rest is not None:
                        return [record] + rest
            return None

        participants = bind(0, ordered)
        if participants is None:
            raise ValueError("No allowed participant combination for this rule")
        context = {}
        supplied = parameters or {}
        if set(supplied) != set(rule.get("parameters", {})):
            raise ValueError("Unexpected reaction parameters")
        for name, spec in rule.get("parameters", {}).items():
            value = supplied[name]
            if (
                not isinstance(value, Quantity)
                or value.dimension != tuple(self.definitions["units"][spec["unit"]])
                or len(value.components) != spec["size"]
            ):
                raise ValueError("Invalid parameter")
            context[name] = value
        for spec, record in zip(inputs, participants, strict=True):
            if record.kind not in spec["types"]:
                raise ValueError("Wrong participant type")
            for name, value in self.context(record).items():
                key = spec["alias"] + "." + name
                if key in context:
                    raise ValueError("Duplicate reaction reference")
                context[key] = value
        for name, expression in rule.get("let", {}).items():
            if name in context:
                raise ValueError("Duplicate temporary name")
            context[name] = self.eval(expression, context)
        if "when" in rule and self.eval(rule["when"], context) is not True:
            raise ValueError("Reaction condition failed")
        products = [
            self.record(
                spec["type"],
                {name: self.eval(expr, context) for name, expr in spec["fields"].items()},
            )
            for spec in outputs
        ]
        if self.totals(participants) != self.totals(products):
            raise ValueError("Conservation check failed")
        remaining = tuple((i, r) for i, r in occupants if i not in identifiers)
        if len(remaining) + len(products) > self.capacity:
            raise ValueError("Product capacity exceeded")
        new = tuple((self.next_id + j, r) for j, r in enumerate(products))
        # Commit only after every field, law, balance and capacity check succeeded.
        self.cells[cell] = remaining + new
        self.next_id += len(products)
        return tuple(i for i, _ in new)

    def send(self, source, destination, identifier):
        if type(source) is not int or type(destination) is not int or abs(destination - source) != 1:
            raise ValueError("Transport is restricted to one adjacent cell")
        occupants = self.cells[source]
        record = dict(occupants)[identifier]
        if len(self.links) >= self.definitions["limits"]["link_capacity"]:
            raise ValueError("Link capacity exceeded")
        self.links += ((source, destination, identifier, record),)
        self.cells[source] = tuple((i, r) for i, r in occupants if i != identifier)

    def advance_transport(self):
        cells = dict(self.cells)
        waiting = []
        for source, destination, identifier, record in self.links:
            occupants = cells.get(destination, ())
            if len(occupants) >= self.capacity:
                waiting.append((source, destination, identifier, record))
            else:
                cells[destination] = occupants + ((identifier, record),)
        self.cells, self.links = cells, tuple(waiting)

    def scheduled(self, cell, schedule_name, identifiers, stream):
        schedule = self.definitions["schedules"][schedule_name]
        weights, branches = schedule["weights"], schedule["branches"]
        choose(weights, 0)  # validate before any state transition
        if len(weights) != len(branches):
            raise ValueError("Schedule branch count mismatch")
        following, ticket = stream.draw(sum(weights))
        if ticket is None:
            return following, None  # bounded rejection advances only the stream
        branch = branches[choose(weights, ticket)]
        if branch is None:
            return following, ()
        products = self.react(cell, branch, identifiers)
        return following, products


def choose(weights, ticket):
    if not 1 <= len(weights) <= 16 or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError("Invalid branch weights")
    total = sum(weights)
    if not 1 <= total <= (1 << 30) - 1 or type(ticket) is not int or not 0 <= ticket < total:
        raise ValueError("Invalid weighted ticket")
    for index, weight in enumerate(weights):
        if ticket < weight:
            return index
        ticket -= weight
    raise AssertionError("Unreachable")


@dataclass(frozen=True)
class RandomStream:
    seed: int

    def __post_init__(self):
        if type(self.seed) is not int or not 1 <= self.seed <= 0xFFFFFFFF:
            raise ValueError("Seed must be a nonzero uint32")

    def draw(self, total):
        if type(total) is not int or not 1 <= total <= (1 << 30) - 1:
            raise ValueError("Invalid total weight")
        x = self.seed
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        sample = x - 1
        limit = (0xFFFFFFFF // total) * total
        # One bounded attempt: a tail value defers an event, never modulo-biases it.
        return RandomStream(x), sample % total if sample < limit else None


@dataclass(frozen=True)
class Complex:
    real: Rational
    imag: Rational = ZERO

    def add(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def mul(self, other):
        return Complex(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def conjugate(self):
        return Complex(self.real, -self.imag)

    def norm2(self):
        return self.real * self.real + self.imag * self.imag


@dataclass(frozen=True)
class QuantumState:
    amplitudes: tuple[Complex, ...]

    def __post_init__(self):
        if not 1 <= len(self.amplitudes) <= 4:
            raise ValueError("Local quantum state supports at most four basis states")
        total = ZERO
        for amplitude in self.amplitudes:
            total = total + amplitude.norm2()
        if total != ONE:
            raise ValueError("Quantum state must be exactly normalized")

    def evolve(self, matrix):
        size = len(self.amplitudes)
        if len(matrix) != size or any(len(row) != size for row in matrix):
            raise ValueError("Invalid operator shape")
        for i in range(size):
            for j in range(size):
                inner = Complex(ZERO)
                for k in range(size):
                    inner = inner.add(matrix[k][i].conjugate().mul(matrix[k][j]))
                if inner != Complex(ONE if i == j else ZERO):
                    raise ValueError("Operator must be unitary")
        output = []
        for row in matrix:
            amplitude = Complex(ZERO)
            for coefficient, value in zip(row, self.amplitudes, strict=True):
                amplitude = amplitude.add(coefficient.mul(value))
            output.append(amplitude)
        return QuantumState(tuple(output))

    def weights(self):
        probabilities = [a.norm2() for a in self.amplitudes]
        denominator = lcm(*(p.denominator for p in probabilities))
        if denominator > (1 << 30) - 1:
            raise OverflowError("Born ticket budget exceeded")
        return [p.numerator * (denominator // p.denominator) for p in probabilities]

    def measure_into(self, lab, cell, branches, identifiers, ticket):
        if len(branches) != len(self.amplitudes):
            raise ValueError("Each basis state needs one reaction branch")
        selected = choose(self.weights(), ticket)
        collapsed = QuantumState(
            tuple(Complex(ONE if i == selected else ZERO) for i in range(len(branches)))
        )
        products = lab.react(cell, branches[selected], identifiers)
        return collapsed, products
