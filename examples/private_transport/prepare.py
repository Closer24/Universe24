"""Load the explicit private identity profile without changing ordinary inputs."""

import json
from pathlib import Path

from event_universe.core.private_register import PrivateKey, RegisterDatum
from event_universe.core.private_transport import PeriodicWiring, RouteTemplate


def prepare(document: dict) -> tuple[PeriodicWiring, tuple[tuple[PrivateKey, RegisterDatum], ...], int]:
    expected = {"profile", "shape", "boundary", "ticks", "local_rule", "wiring", "seeds"}
    if set(document) != expected or document["profile"] != "private-register-identity-v1":
        raise ValueError("unsupported private transport profile or configuration keys")
    if document["boundary"] != "periodic":
        raise ValueError("the private transport profile requires periodic boundaries")
    if (
        document["local_rule"] != {"operation": "identity", "wait_ticks": 0}
        or type(document["local_rule"]["wait_ticks"]) is not int
    ):
        raise ValueError("the private transport profile supports only zero-wait identity")
    ticks = document["ticks"]
    if type(ticks) is not int or not 0 <= ticks <= 10000:
        raise ValueError("recorded tick count must be an integer from 0 to 10000")
    templates = []
    for item in document["wiring"]:
        if set(item) != {"source", "offset", "target", "transit_ticks"}:
            raise ValueError("unexpected channel template keys")
        templates.append(
            RouteTemplate(
                tuple(item["source"]),
                tuple(item["offset"]),
                tuple(item["target"]),
                item["transit_ticks"],
            )
        )
    wiring = PeriodicWiring(tuple(document["shape"]), tuple(templates))
    seeds = []
    for item in document["seeds"]:
        if set(item) != {"node", "register", "codes"} or len(item["register"]) != 2:
            raise ValueError("unexpected seed input keys or Register address")
        seeds.append(
            (PrivateKey(tuple(item["node"]), *item["register"]), RegisterDatum(tuple(item["codes"])))
        )
    return wiring, tuple(seeds), ticks


def load(path: Path) -> tuple[PeriodicWiring, tuple[tuple[PrivateKey, RegisterDatum], ...], int]:
    return prepare(json.loads(path.read_text()))
