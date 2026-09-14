"""Passive named Node readouts over actual resident and in-flight owners."""

from event_universe.core.conservation_state import InventoryView
from event_universe.core.disturbance_state import InitialState
from event_universe.core.node_conservation import LocalInventory
from event_universe.fields.node_conservation import LocalBalanceGuard


def node_contract_report(initial: InitialState, view: InventoryView) -> dict[str, object]:
    """Project an immutable host snapshot without advancing or repairing a Node.

    Global summation is host accounting and does not impose a global integer
    register bound. Each local readout retains its checked working-integer bound.
    Open-boundary escaped stock is outside this explicitly reported inventory.
    """
    definition = initial.conservation_contract
    if definition is None:
        raise ValueError("a Node conservation contract is required for named readouts")
    guard = LocalBalanceGuard(
        initial.fields, initial.spatial_fields, initial.operation_costs, definition
    )
    totals = [[0] * quantity.components for quantity in definition.quantities]

    def add(inventory: LocalInventory) -> None:
        for target, values in zip(totals, guard.measure(inventory), strict=True):
            for index, value in enumerate(values):
                target[index] += value

    error_message = None
    try:
        for node in view.nodes:
            add(
                LocalInventory(
                    records=node.records, spatial=tuple(state.populations for state in node.spatial)
                )
            )
        for packet in view.packets:
            add(
                LocalInventory(
                    carrier_packets=() if packet.record is None else (packet.record,),
                    spatial_packets=() if not packet.spatial else (packet.spatial,),
                )
            )
    except (ValueError, OverflowError) as error:
        # A diagnostic failure must not prevent the runner from saving its failure
        # metadata. Do not expose a partial aggregate as a valid measurement.
        error_message = str(error)
    return {
        "name": definition.name,
        "mode": "exact_pre_commit",
        "scope": "resident_and_in_flight",
        "measurement_error": error_message,
        "quantities": [
            {
                "name": quantity.name,
                "components": quantity.components,
                "units": quantity.units,
                "value": tuple(values) if error_message is None else None,
            }
            for quantity, values in zip(definition.quantities, totals, strict=True)
        ],
    }
