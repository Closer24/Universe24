"""Strict authoring boundary for the finite private36 shared-pair experiment."""

from event_universe.core.disturbance_state import unpack
from event_universe.core.private_register import CUBIC_PORT_PAIRS, PrivateKey, RegisterDatum
from event_universe.core.private_transport import PeriodicWiring, RouteTemplate
from event_universe.core.private_worklist import PrivateSimulation
from event_universe.integration.private_contacts import DetectorDefinition, PrivateContacts


def prepare(document, *, strategy="sparse"):
    expected = {
        "profile",
        "shape",
        "boundary",
        "ticks",
        "wiring",
        "seeds",
        "detectors",
        "pair_ids",
        "seed",
        "number_stream",
        "oracle",
    }
    if type(document) is not dict or set(document) != expected:
        raise ValueError("private36 input has missing or unsupported keys")
    if document["profile"] != "private-register-bond-v1" or document["oracle"] != "shared_bond":
        raise ValueError("explicit private36 profile and shared bond owner required")
    shape = document["shape"]
    if (
        type(shape) is not list
        or len(shape) != 3
        or any(type(n) is not int or not 3 <= n <= 32 for n in shape)
    ):
        raise ValueError("three extents from three to 32 preserve six distinct neighbors")
    if document["boundary"] != "periodic":
        raise ValueError("this finite experiment requires explicit periodic boundaries")
    ticks = document["ticks"]
    if type(ticks) is not int or not 1 <= ticks <= 10000:
        raise ValueError("ticks must be a bounded positive integer")
    routes = []
    for row in document["wiring"]:
        if set(row) != {"source", "offset", "target", "transit_ticks"}:
            raise ValueError("channel keys must be explicit")
        routes.append(
            RouteTemplate(
                tuple(row["source"]), tuple(row["offset"]), tuple(row["target"]), row["transit_ticks"]
            )
        )
    wiring = PeriodicWiring(tuple(shape), tuple(routes), pairs=CUBIC_PORT_PAIRS)
    bindings = []
    for row in document["detectors"]:
        if set(row) != {"node", "register", "end", "setting"}:
            raise ValueError("detector keys must be explicit")
        key = PrivateKey(tuple(row["node"]), *row["register"])
        if key not in wiring.channels:
            raise ValueError("detector lies outside the configured world")
        bindings.append((key, DetectorDefinition(row["end"], row["setting"])))
    if {definition.end for _, definition in bindings} != {1, 2}:
        raise ValueError("both detector ends must be configured")
    contacts = PrivateContacts(
        tuple(bindings),
        tuple(document["pair_ids"]),
        seed=document["seed"],
        stream=tuple(document["number_stream"]),
    )
    seeds = []
    owners = {}
    for row in document["seeds"]:
        if set(row) != {"node", "register", "codes"}:
            raise ValueError("seed keys must be explicit")
        key = PrivateKey(tuple(row["node"]), *row["register"])
        datum = RegisterDatum(tuple(row["codes"]))
        values = unpack(datum.codes)
        if len(values) != 2 or values[0] not in contacts.quantum.slots or values[1] not in (1, 2):
            raise ValueError("a seed owns one declared pair endpoint")
        if values in owners:
            raise ValueError("duplicate pair endpoint inventory owner")
        owners[values] = key.node
        seeds.append((key, datum))
    for pair in contacts.quantum.slots:
        if (pair, 1) not in owners or (pair, 2) not in owners or owners[pair, 1] != owners[pair, 2]:
            raise ValueError("both pair tokens must begin at one common source Node")
    return PrivateSimulation(wiring, tuple(seeds), strategy=strategy, contacts=contacts), ticks
