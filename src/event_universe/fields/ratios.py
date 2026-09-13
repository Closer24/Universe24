"""Opt-in exact arithmetic with fixed-width integer ratios and explicit projections."""

from dataclasses import dataclass

from event_universe.core.disturbance_state import CostMeter, Expression, Values, bounded, unpack

RATIO_BITS = 127
TEMP_BITS = 255
PROJECTIONS = frozenset(
    {
        "rational_whole",
        "rational_remainder",
        "rational_denominator",
        "rational_numerator",
        "rational_direction",
        "rational_key",
        "rational_floor",
    }
)


def limit(value: int, bits: int = RATIO_BITS) -> int:
    if type(value) is not int or abs(value).bit_length() > bits:
        raise OverflowError(f"rational {bits}-bit bound exceeded")
    return value


def gcd(a: int, b: int) -> int:
    a, b = abs(limit(a, TEMP_BITS)), abs(limit(b, TEMP_BITS))
    for _ in range(512):
        if not b:
            return a
        a, b = b, a % b
    raise OverflowError("bounded rational Euclid iteration limit exceeded")


@dataclass(frozen=True, slots=True)
class Ratio:
    numerator: int
    denominator: int = 1

    def __post_init__(self) -> None:
        n, d = limit(self.numerator, TEMP_BITS), limit(self.denominator, TEMP_BITS)
        if not d:
            raise ValueError("rational denominator must be nonzero")
        if d < 0:
            n, d = -n, -d
        factor = gcd(n, d)
        object.__setattr__(self, "numerator", limit(n // factor))
        object.__setattr__(self, "denominator", limit(d // factor))

    def add(self, other: Ratio) -> Ratio:
        factor = gcd(self.denominator, other.denominator)
        a, b = self.denominator // factor, other.denominator // factor
        return Ratio(
            limit(self.numerator * b + other.numerator * a, TEMP_BITS),
            limit(a * other.denominator, TEMP_BITS),
        )

    def neg(self) -> Ratio:
        return Ratio(-self.numerator, self.denominator)

    def mul(self, other: Ratio) -> Ratio:
        a = gcd(self.numerator, other.denominator)
        b = gcd(other.numerator, self.denominator)
        return Ratio(
            limit((self.numerator // a) * (other.numerator // b), TEMP_BITS),
            limit((self.denominator // b) * (other.denominator // a), TEMP_BITS),
        )

    def div(self, other: Ratio) -> Ratio:
        return self.mul(Ratio(other.denominator, other.numerator))

    def less(self, other: Ratio) -> bool:
        return limit(self.numerator * other.denominator, TEMP_BITS) < limit(
            other.numerator * self.denominator, TEMP_BITS
        )


def common(values: tuple[Ratio, ...]) -> int:
    denominator = 1
    for value in values:
        denominator = limit((denominator // gcd(denominator, value.denominator)) * value.denominator)
    return denominator


def project(name: str, values: tuple[Ratio, ...]) -> tuple[int, ...]:
    if name == "rational_key":
        return tuple(component for v in values for component in (v.numerator, v.denominator))
    if name == "rational_floor":
        return tuple(bounded(v.numerator // v.denominator) for v in values)
    if name == "rational_whole":
        return tuple(
            bounded((1 if v.numerator >= 0 else -1) * (abs(v.numerator) // v.denominator))
            for v in values
        )
    denominator = common(values)
    numerators = tuple(limit(v.numerator * (denominator // v.denominator)) for v in values)
    if name == "rational_direction":
        factor = 0
        for value in numerators:
            factor = gcd(factor, value)
        return tuple(bounded(v // factor) if factor else 0 for v in numerators)
    if name == "rational_denominator":
        return (bounded(denominator),)
    if name == "rational_remainder":
        return tuple(bounded((1 if n >= 0 else -1) * (abs(n) % denominator)) for n in numerators)
    if name == "rational_numerator":
        return tuple(bounded(n) for n in numerators)
    raise ValueError("unknown rational projection")


def evaluate_ratio(
    expression: Expression,
    left: Values,
    right: Values,
    meter: CostMeter,
    spatial_fluxes: Values = (),
    *,
    ports: tuple[Values, ...] = (),
    outgoing: tuple[Values, ...] = (),
    participants: tuple[Values, ...] = (),
    received_masks: tuple[int, ...] = (),
    node_cost: int | None = None,
) -> tuple[Ratio, ...]:
    # Fixed worst-case arithmetic tariff, independent of numerator magnitude.
    meter.charge("evaluate", 65536)
    op = expression.op
    if op == "literal":
        return tuple(Ratio(v) for v in expression.literal)
    if op == "node_cost":
        if node_cost is None or bounded(node_cost) < 0:
            raise ValueError("node cost requires an explicitly supplied committed local value")
        return (Ratio(node_cost),)
    if op == "field":
        owners = participants or (left, right)
        if not 0 <= expression.side < len(owners):
            raise ValueError("rational field expression participant is unavailable")
        return tuple(Ratio(v) for v in unpack(owners[expression.side][expression.field]))
    if op == "received_present":
        if not 0 <= expression.field < len(received_masks) or not 0 <= expression.port < 6:
            raise ValueError("received presence requires explicitly supplied local port masks")
        mask = received_masks[expression.field]
        if type(mask) is not int or not 0 <= mask < 64:
            raise ValueError("received mask requires six bounded port bits")
        return (Ratio(int(bool(mask & (1 << expression.port)))),)
    if op == "flux":
        if not spatial_fluxes:
            raise ValueError("rational flux requires an explicit sample")
        return tuple(Ratio(v) for v in unpack(spatial_fluxes[expression.field]))
    if op in ("received", "outgoing"):
        channels = ports if op == "received" else outgoing
        if len(channels) != 6:
            raise ValueError("rational port expression requires six local channels")
        return tuple(Ratio(v) for v in unpack(channels[expression.port][expression.field]))
    args = tuple(
        evaluate_ratio(
            a,
            left,
            right,
            meter,
            spatial_fluxes,
            ports=ports,
            outgoing=outgoing,
            participants=participants,
            received_masks=received_masks,
            node_cost=node_cost,
        )
        for a in expression.arguments
    )
    if op in PROJECTIONS:
        return tuple(Ratio(v) for v in project(op, args[0]))
    if op == "neg":
        return tuple(v.neg() for v in args[0])
    if op == "abs":
        return tuple(Ratio(abs(v.numerator), v.denominator) for v in args[0])
    if op == "component":
        return (args[0][expression.component],)
    if op == "vector":
        return tuple(a[0] for a in args)
    if op in ("sum", "dot", "transform"):
        vectors = (
            ((args[0], tuple(Ratio(1) for _ in args[0])),)
            if op == "sum"
            else ((args[0], args[1]),)
            if op == "dot"
            else tuple((args[0], tuple(Ratio(v) for v in row)) for row in expression.matrix)
        )
        result = []
        for a, b in vectors:
            total = Ratio(0)
            for x, y in zip(a, b, strict=True):
                total = total.add(x.mul(y))
            result.append(total)
        return tuple(result)
    if op == "cross":
        a, b = args
        return tuple(a[i].mul(b[j]).add(a[j].mul(b[i]).neg()) for i, j in ((1, 2), (2, 0), (0, 1)))
    if op == "eq":
        return (Ratio(int(args[0][0] == args[1][0])),)
    if op == "gt":
        return (Ratio(int(args[1][0].less(args[0][0]))),)
    size = max(len(a) for a in args)
    first, second = (a * size if len(a) == 1 else a for a in args)
    result = []
    for first_value, second_value in zip(first, second, strict=True):
        if op == "add":
            value = first_value.add(second_value)
        elif op == "sub":
            value = first_value.add(second_value.neg())
        elif op == "mul":
            value = first_value.mul(second_value)
        elif op in ("ratio", "exact_div"):
            value = first_value.div(second_value)
            if op == "exact_div" and value.denominator != 1:
                raise ValueError("exact_div requires an integer result even in a rational region")
        elif op == "min":
            value = first_value if first_value.less(second_value) else second_value
        elif op == "max":
            value = second_value if first_value.less(second_value) else first_value
        else:
            raise ValueError(f"unsupported rational operation {op}")
        result.append(value)
    return tuple(result)
