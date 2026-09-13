"""Explicit headless 4x4 controller; not a native ScalarEngine event source."""

import argparse
import json

from event_universe.quantum import (
    EVENT_NETWORK_MODEL_ID,
    Amplitude,
    DeferredQuantum,
    EventNetworkConfig,
    LocalInstrument,
    LocalUnitary,
)


def run_trial(ticket: int = 24) -> dict[str, object]:
    """Use the chosen event backend with an explicitly supplied integer ticket.

    The 3:4 rule is demonstration data, not a derived free-particle law. The
    controller chooses when to request the position instrument. No physical
    engine, detector fixture or automatic collapse criterion is introduced.
    """
    zero, one = Amplitude(0, 0), Amplitude(1, 0)
    three, four, minus_four, five = (
        Amplitude(3, 0),
        Amplitude(4, 0),
        Amplitude(-4, 0),
        Amplitude(5, 0),
    )
    splitter = LocalUnitary(
        (
            (five, zero, zero, zero),
            (zero, three, minus_four, zero),
            (zero, four, three, zero),
            (zero, zero, zero, five),
        )
    )
    position = LocalInstrument((((one, zero), (zero, zero)), ((zero, zero), (zero, one))))
    owner = DeferredQuantum()
    space = owner.bind_event_network(
        EventNetworkConfig(tuple((x, y, 0) for y in range(4) for x in range(4)), (5,))
    )
    space.step(((splitter, (5, 6)),))
    before = space.query(5)
    decision = space.prepare(1, 5, position)
    tick_before = space.tick
    record = space.commit(decision, ticket)
    after = space.query(5)
    return {
        "model": EVENT_NETWORK_MODEL_ID,
        "grid": [4, 4, 1],
        "source_register_index": 5,
        "source_tick": 0,
        "example_split_amplitudes": [3, 4],
        "weights_before_empty_occupied": before.weights,
        "ticket": ticket,
        "outcome": record.outcome,
        "weights_after_empty_occupied": after.weights,
        "tick_before_decision": tick_before,
        "tick_after_decision": space.tick,
        "extra_world_ticks": after.world_ticks,
        "retained_joint_state": space.joint_state(),
        "successful_queries": owner.query_stats.successful_queries,
        "host_evaluated_nodes": owner.query_stats.host_evaluated_nodes,
        "physical_trigger": "explicit controller request, not a universal collapse law",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket", type=int, default=24)
    args = parser.parse_args()
    print(json.dumps(run_trial(args.ticket), indent=2))


if __name__ == "__main__":
    main()
