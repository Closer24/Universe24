"""Strict, finite experiment data compiled into the existing quantum owner."""

from dataclasses import dataclass

from event_universe.core.disturbance_engine import cycle_timing
from event_universe.core.lattice import PeriodicLattice
from event_universe.core.state import DIRECTIONS, Address, checked
from event_universe.initialization import _address, _array, _integer, _object, _text
from event_universe.quantum import Amplitude, EventNetworkConfig, LocalInstrument, LocalUnitary
from event_universe.quantum.event_rules import Matrix
from event_universe.quantum.mode_rules import IDENTITY, Mode, validate_sectors

QUANTUM_EXPERIMENT_SCHEMA = "local-coherent-modes-v1"


@dataclass(frozen=True, slots=True)
class Action:
    start: int
    departure: int
    end: int
    kind: str
    sites: tuple[int, ...]
    cost: int
    matrix: LocalUnitary | None
    instrument: LocalInstrument | None = None
    ticket: int | None = None
    port: int | None = None
    origins: tuple[Address, ...] = ()
    destination: Address | None = None


@dataclass(frozen=True, slots=True)
class QuantumInitialization:
    model_id: str
    modes: tuple[Mode, ...]
    quantity_names: tuple[str, ...]
    network: EventNetworkConfig
    actions: tuple[Action, ...]
    groups: tuple[tuple[str, tuple[int, ...]], ...]
    ticks: int
    link_ticks: int
    normal_budget: int


def _named(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    names = {_text(key, label) for key in value}
    return _object(value, label, names, names)


def _matrix(value: object) -> Matrix:
    rows = _array(value, "matrix", 16, 2)
    result = []
    for row in rows:
        values = []
        for entry in _array(row, "matrix row", len(rows), len(rows)):
            pair = [entry, 0] if type(entry) is int else _array(entry, "complex coefficient", 2, 2)
            values.append(Amplitude(_integer(pair[0], "real"), _integer(pair[1], "imaginary")))
        result.append(tuple(values))
    return tuple(result)


def parse_quantum_initialization(value: object) -> QuantumInitialization:
    required = {
        "schema",
        "model_id",
        "shape",
        "boundary",
        "link_ticks",
        "normal_budget",
        "ticks",
        "quantities",
        "modes",
        "state",
        "rules",
        "actions",
        "groups",
    }
    raw = _object(value, "quantum initialization", required | {"budgets"}, required)
    if raw["schema"] != QUANTUM_EXPERIMENT_SCHEMA:
        raise ValueError("explicit local coherent mode schema required")
    shape = _address(raw["shape"], "shape", 1)
    boundary = _text(raw["boundary"], "boundary")
    tau = _integer(raw["link_ticks"], "link_ticks", 1)
    budget = _integer(raw["normal_budget"], "normal_budget", 1)
    ticks = _integer(raw["ticks"], "ticks", 1)
    if ticks > 10_000:
        raise ValueError("finite experiment tick capacity exceeded")
    names = tuple(_text(x, "quantity") for x in _array(raw["quantities"], "quantities", 8, 1))
    if len(set(names)) != len(names):
        raise ValueError("duplicate quantity name")
    modes = []
    for entry in _array(raw["modes"], "modes", 30, 1):
        obj = _object(
            entry, "mode", {"name", "position", "quantities"}, {"name", "position", "quantities"}
        )
        quantities = _object(obj["quantities"], "mode quantities", set(names), set(names))
        modes.append(
            Mode(
                _text(obj["name"], "mode name"),
                _address(obj["position"], "position", 0),
                tuple(_integer(quantities[n], n) for n in names),
            )
        )
    indices = {mode.name: i for i, mode in enumerate(modes)}
    if len(indices) != len(modes):
        raise ValueError("duplicate mode name")

    def sites(value: object, limit: int, minimum: int = 1) -> tuple[int, ...]:
        labels = tuple(
            _text(x, "mode reference") for x in _array(value, "mode references", limit, minimum)
        )
        if len(set(labels)) != len(labels) or any(name not in indices for name in labels):
            raise ValueError("duplicate or unknown mode reference")
        return tuple(indices[name] for name in labels)

    state = []
    for entry in _array(raw["state"], "state", 4096, 1):
        obj = _object(entry, "state term", {"occupied", "amplitude"}, {"occupied", "amplitude"})
        pair = _array(obj["amplitude"], "amplitude", 2, 2)
        state.append(
            (
                sum(1 << q for q in sites(obj["occupied"], 30, 0)),
                Amplitude(_integer(pair[0], "real"), _integer(pair[1], "imaginary")),
            )
        )
    limits = {"max_nodes", "max_eval_nodes", "max_terms", "max_records"}
    capacities = _object(raw.get("budgets", {}), "budgets", limits, set())
    network = EventNetworkConfig(
        tuple(mode.address for mode in modes),
        modes_per_cell=8,
        shape=shape,
        boundary=boundary,
        initial_state=tuple(sorted(state)),
        max_nodes=_integer(capacities.get("max_nodes", 10000), "max_nodes", 1),
        max_eval_nodes=_integer(capacities.get("max_eval_nodes", 10000), "max_eval_nodes", 1),
        max_terms=_integer(capacities.get("max_terms", 4096), "max_terms", 1),
        max_records=_integer(capacities.get("max_records", 1024), "max_records", 1),
    )
    rules: dict[str, LocalUnitary | LocalInstrument] = {}
    for name, entry in _named(raw["rules"], "rules").items():
        obj = _object(entry, "rule", {"matrix", "branches"}, set())
        if set(obj) == {"matrix"}:
            rules[name] = LocalUnitary(_matrix(obj["matrix"]))
        elif set(obj) == {"branches"}:
            rules[name] = LocalInstrument(
                tuple(_matrix(v) for v in _array(obj["branches"], "branches", 4, 1))
            )
        else:
            raise ValueError("a rule supplies exactly one matrix or one complete instrument")
    if len(rules) > 64:
        raise ValueError("rule capacity exceeded")
    actions = []
    for entry in _array(raw["actions"], "actions", 512):
        required_action = {"tick", "kind", "modes", "cost"}
        obj = _object(entry, "action", required_action | {"rule", "ticket", "port"}, required_action)
        kind = _text(obj["kind"], "action kind")
        selected = sites(obj["modes"], 4)
        cost = _integer(obj["cost"], "action cost", 1)
        start = _integer(obj["tick"], "action tick", 0)
        port = None
        ticket = None
        matrix = None
        instrument = None
        if kind in ("local", "observe"):
            if "port" in obj:
                raise ValueError("interaction cannot select a transport port")
            rule = rules.get(_text(obj.get("rule"), "rule reference"))
            if kind == "local" and isinstance(rule, LocalUnitary) and "ticket" not in obj:
                matrix = rule
            elif kind == "observe" and isinstance(rule, LocalInstrument) and len(selected) == 1:
                instrument = rule
                ticket = None if obj.get("ticket") is None else _integer(obj["ticket"], "ticket", 0)
            else:
                raise ValueError("action and rule kind disagree")
        elif kind in ("link", "escape"):
            if "rule" in obj or "ticket" in obj:
                raise ValueError("transport cannot select a rule or outcome")
            port = _integer(obj.get("port"), "port", 0)
            if port >= 6:
                raise ValueError("transport requires a cardinal port")
            if len(selected) != 1:
                raise ValueError("one mode per directed transport action required")
            if kind == "escape":
                matrix = LocalUnitary(IDENTITY)
        else:
            raise ValueError("unknown action kind")
        labels = tuple(modes[q].quantities for q in selected)
        for coefficients in (
            instrument.branches
            if instrument is not None
            else (matrix.matrix,)
            if matrix is not None
            else ()
        ):
            validate_sectors(coefficients, labels)
        actions.append(
            Action(start, start, start, kind, selected, cost, matrix, instrument, ticket, port)
        )
    compiled = _schedule(tuple(actions), tuple(modes), budget, tau, ticks, shape, boundary)
    groups = tuple(
        (name, sites(members, 8)) for name, members in _named(raw["groups"], "groups").items()
    )
    if len(groups) > 16:
        raise ValueError("diagnostic group capacity exceeded")
    return QuantumInitialization(
        _text(raw["model_id"], "model_id"),
        tuple(modes),
        names,
        network,
        compiled,
        groups,
        ticks,
        tau,
        budget,
    )


def _schedule(
    actions: tuple[Action, ...],
    modes: tuple[Mode, ...],
    budget: int,
    tau: int,
    ticks: int,
    shape: Address,
    boundary: str,
) -> tuple[Action, ...]:
    """Host setup validates a finite local clock plan; no amplitudes are read.

    Whole cells are reserved through completion. Simultaneous disjoint actions
    share each cell's total priced work and therefore its common extra delay.
    """
    from dataclasses import replace

    busy: dict[Address, int] = {}
    retired: set[int] = set()
    result: list[Action] = []
    positions = [mode.address for mode in modes]
    arrived: set[int] = set()
    for start in sorted({a.start for a in actions}):
        for i, earlier in enumerate(result):
            if i not in arrived and earlier.end <= start:
                arrived.add(i)
                if earlier.destination is not None:
                    positions[earlier.sites[0]] = earlier.destination
        batch = []
        for action in (a for a in actions if a.start == start):
            origins = tuple(positions[q] for q in action.sites)
            destination = None
            if action.kind in ("local", "observe"):
                if len(set(origins)) != 1:
                    raise ValueError("interaction must use modes in the same cell")
            else:
                assert action.port is not None
                x, y, z = origins[0]
                dx, dy, dz = DIRECTIONS[action.port]
                neighbor = (checked(x + dx), checked(y + dy), checked(z + dz))
                outside = any(not 0 <= neighbor[i] < shape[i] for i in range(3))
                if action.kind == "escape":
                    if boundary != "open" or not outside:
                        raise ValueError("escape requires an open terminal link")
                else:
                    if boundary == "open" and outside:
                        raise ValueError("open boundary requires an explicit escape")
                    destination = (
                        PeriodicLattice(shape).neighbor(origins[0], action.port)
                        if boundary == "periodic"
                        else neighbor
                    )
                    if destination == origins[0]:
                        raise ValueError("transport must reach a distinct cell")
            batch.append(replace(action, origins=origins, destination=destination))
        used: set[int] = set()
        costs: dict[Address, int] = {}
        observers: set[Address] = set()
        for action in batch:
            for site in action.sites:
                if site in used or site in retired:
                    raise ValueError("mode is already reserved or has escaped")
                used.add(site)
            cells = set(action.origins) | (
                {action.destination} if action.destination is not None else set()
            )
            for cell in cells:
                if busy.get(cell, 0) > start:
                    raise ValueError("cell is still waiting or has a fixed in-flight transfer")
            for cell in set(action.origins):
                costs[cell] = checked(costs.get(cell, 0) + action.cost)
            if action.kind == "observe":
                cell = action.origins[0]
                if cell in observers:
                    raise ValueError("at most one instrument per cell cycle")
                observers.add(cell)
        for action in batch:
            cells = set(action.origins) | (
                {action.destination} if action.destination is not None else set()
            )
            # A destination reservation is not a remote computation-cost read.
            extra = cycle_timing(costs[action.origins[0]], budget, tau)[0]
            departure = checked(start + extra)
            end = checked(departure + (tau if action.kind in ("link", "escape") else 1))
            if end > ticks:
                raise ValueError("scheduled completion exceeds the experiment duration")
            result.append(replace(action, departure=departure, end=end))
            for cell in cells:
                busy[cell] = max(busy.get(cell, 0), end)
            if action.kind == "escape":
                retired.update(action.sites)
    return tuple(result)
