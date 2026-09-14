"""A lamp facing a mirror: the Kerengonen standing wave and its half-wavelength period.

A held lamp at the left fires along the axis every tick on a 64-step field; a
mirror record at the right absorbs what reaches it and re-emits the whole
stock back along the reflected heading at the phase it absorbed, one advance
on. Incident and reflected rays meet at every Node between them, and the
sampled value along the line is the coherent sum: a standing wave whose
period is `64 / (2 x advance)` links. Two advances are run. Every number is a
read-only world/event audit at host lattice coordinates; no wavelength unit
or constant is identified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

SIZE = 41
CENTER = SIZE // 2
LAMP_X = CENTER - 16
MIRROR_X = CENTER + 16
PHASE_STEPS = 64
ADVANCES = (2, 4, 8)
PER_TICK = 16  # 8 quanta each way per tick
TICKS = 96
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def document(advance: int, ticks: int = TICKS, mirror: bool = True) -> dict:
    field = {
        "field": "quanta",
        "baseline": 0,
        "transport": "ray",
        "headings": [[1, 0, 0], [-1, 0, 0]],
        "rays_per_tick": 2,
        "ray_slots": 16,
        "kerengonen": {"phase_steps": PHASE_STEPS, "phase_advance": advance},
    }
    emissions = [
        {
            "type": "lamp",
            "field": "quanta",
            "amount": PER_TICK,
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
        }
    ]
    couplings = []
    if mirror:
        emissions.append(
            {
                "type": "mirror",
                "field": "quanta",
                "amount": {"field": "quanta"},
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": "carried",
                "kerengonen_mirror": "x",
            }
        )
        couplings.append(
            {
                "name": "mirror_absorbs",
                "type": "mirror",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        )
    return {
        "schema_version": 1,
        "model_id": "kerengonen-mirror-standing-wave-probe-v1",
        "shape": [SIZE, 3, 3],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [
            {
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": PER_TICK * ticks, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "mirror",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [field],
        "emissions": emissions,
        "spatial_couplings": couplings,
        "seeds": [{"position": [LAMP_X, 1, 1], "type": "lamp"}]
        + ([{"position": [MIRROR_X, 1, 1], "type": "mirror"}] if mirror else []),
    }


def run(raw: dict) -> dict:
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    readings = {
        x - CENTER: world.spatial_values((x, 1, 1))["quanta"]["value"][0]
        for x in range(LAMP_X + 1, MIRROR_X)
    }
    mirror = [
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == 1
    ]
    totals, escaped = world.totals(), world.escaped_totals()
    return {
        "readings": readings,
        "mirror_momentum": list(mirror[0]["momentum"]) if mirror else None,
        "quanta_closed": totals["quanta"][0] + escaped["quanta"][0] == initial,
    }


def period(readings: dict[int, int]) -> int | None:
    values = [readings[x] for x in sorted(readings)]
    for candidate in range(2, len(values) // 2):
        if all(values[i] == values[i + candidate] for i in range(len(values) - candidate)):
            return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    for advance in ADVANCES:
        standing = run(document(advance))
        free = run(document(advance, mirror=False))
        results.append(
            {
                "advance": advance,
                "predicted_period": PHASE_STEPS // (2 * advance),
                "measured_period": period(standing["readings"]),
                "readings": standing["readings"],
                "without_mirror": free["readings"],
                "mirror_momentum": standing["mirror_momentum"],
                "quanta_closed": standing["quanta_closed"] and free["quanta_closed"],
            }
        )
    report = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "phase_steps": PHASE_STEPS,
        "quanta_per_tick_each_way": PER_TICK // 2,
        "ticks": TICKS,
        "results": results,
    }
    (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    for result in results:
        line = [result["readings"][x] for x in sorted(result["readings"])]
        print(
            "advance",
            result["advance"],
            "period predicted",
            result["predicted_period"],
            "measured",
            result["measured_period"],
            "closed",
            result["quanta_closed"],
            "mirror momentum",
            result["mirror_momentum"],
        )
        print("  line", line[:24])
        print("  free", [result["without_mirror"][x] for x in sorted(result["without_mirror"])][:8])
    print("Wrote report: " + str(args.output / "summary.json"))


if __name__ == "__main__":
    main()
