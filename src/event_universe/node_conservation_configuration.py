"""Validate externally defined local transition readouts without running a world."""

from dataclasses import replace
from typing import TYPE_CHECKING

from .core.disturbance_state import MAX_FIELDS, MAX_TYPES, Address3, InitialState, pack, unpack
from .core.node_conservation import (
    CarrierReadout,
    ConservedReadout,
    LocalInventory,
    NodeConservationDefinition,
)

if TYPE_CHECKING:
    from .fields.node_conservation import LocalBalanceGuard


def parse_node_conservation(value: object, initial: InitialState) -> NodeConservationDefinition:
    # The ordinary initialization owner calls this after resolving its layouts.
    # Reuse its expression parser rather than create a second expression language.
    from .initialization import _array, _Expressions, _index, _integer, _object, _text

    if not initial.node_execution:
        raise ValueError("conservation_contract requires node_execution")
    if initial.schema_version != 1 or initial.event_program is not None:
        raise ValueError("node conservation requires schema 1 without a native event program")
    if initial.emissions or any(
        update.source for kind in initial.disturbances for update in kind.updates
    ):
        raise ValueError("node conservation requires owned transfers without external sources")
    if any(any(unpack(field.baseline)) for field in initial.spatial_fields):
        raise ValueError("node conservation requires zero spatial baselines")
    obj = _object(value, "conservation_contract", {"name", "quantities"}, {"name", "quantities"})
    fields = {field.name: index for index, field in enumerate(initial.fields)}
    names: set[str] = set()
    quantities: list[ConservedReadout] = []
    for raw in _array(obj["quantities"], "conservation quantities", MAX_FIELDS, 1):
        required = {"name", "components", "units", "carriers"}
        row = _object(raw, "conserved readout", required | {"spatial"}, required)
        name = _text(row["name"], "conserved readout name")
        if name in names:
            raise ValueError("duplicate conserved readout name")
        names.add(name)
        size = _integer(row["components"], "conserved readout components", 1)
        if size > 32:
            raise ValueError("conserved readouts support at most 32 components")
        covered: set[int] = set()
        carriers: list[CarrierReadout] = []
        for item in _array(row["carriers"], "conserved carrier readouts", MAX_TYPES):
            carrier = _object(item, "carrier readout", {"requires", "value"}, {"requires", "value"})
            owned = tuple(
                _index(key, fields, "readout property")
                for key in _array(carrier["requires"], "readout requires", MAX_FIELDS, 1)
            )
            if len(set(owned)) != len(owned):
                raise ValueError("duplicate readout property")
            kinds = tuple(
                index
                for index, kind in enumerate(initial.disturbances)
                if set(owned) <= set(kind.fields)
            )
            if not kinds or covered.intersection(kinds):
                raise ValueError("readouts must cover each disturbance layout exactly once")
            if any(initial.disturbances[index].cost_field in owned for index in kinds):
                raise ValueError("conserved readouts cannot depend on computation cost reporters")
            expression = _Expressions(initial.fields, owned, ()).parse(carrier["value"], size)
            carriers.append(CarrierReadout(kinds, expression))
            covered.update(kinds)
        if covered != set(range(len(initial.disturbances))):
            raise ValueError("conserved readouts must cover every disturbance layout")
        if bool(initial.spatial_fields) != ("spatial" in row):
            raise ValueError("each conserved readout must cover the configured spatial fields")
        spatial = None
        if "spatial" in row:
            owned = tuple(field.field for field in initial.spatial_fields)
            spatial = _Expressions(initial.fields, (), owned).parse(row["spatial"], size)
        quantities.append(
            ConservedReadout(name, size, _text(row["units"], "readout units"), tuple(carriers), spatial)
        )
    result = NodeConservationDefinition(
        _text(obj["name"], "conservation contract name"), tuple(quantities)
    )
    from .fields.node_conservation import LocalBalanceGuard

    guard = LocalBalanceGuard(initial.fields, initial.spatial_fields, initial.operation_costs, result)
    guard.validate_empty()
    _validate_initial_readouts(initial, guard)
    return result


def _validate_initial_readouts(initial: InitialState, guard: LocalBalanceGuard) -> None:
    """Validate known initial owners per Node without constructing or advancing a world."""
    empty = LocalInventory(
        spatial=tuple(
            (pack((0,) * initial.fields[item.field].components),) * 8 for item in initial.spatial_fields
        )
    )
    inventories: dict[Address3, LocalInventory] = {}
    for carrier in initial.seeds:
        inventory = inventories.get(carrier.position, empty)
        inventories[carrier.position] = replace(inventory, records=(*inventory.records, carrier.record))
    for spatial in initial.spatial_seeds:
        inventory = inventories.get(spatial.position, empty)
        populations = list(inventory.spatial)
        populations[spatial.spatial_field] = spatial.populations
        inventories[spatial.position] = replace(inventory, spatial=tuple(populations))
    for position, inventory in inventories.items():
        try:
            guard.measure(inventory)
        except (ValueError, ArithmeticError) as error:
            raise ValueError(f"initial conservation readouts at Node {position}: {error}") from error
