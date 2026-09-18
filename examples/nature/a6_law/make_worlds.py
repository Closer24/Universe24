"""Write the worlds of experiment A6 repeated under the law of the bit
(docs/EXPERIMENTS.md, "A6 repeated under the law of the bit (2026-09-18)"): the
four gravitational tests against Einstein on the engine of features 15 to 18,
16e and 16f (bit-law-v1, node-mixing-v1, clock-readings-v1, node-is-ports-v1,
lanes-v1, return-field-v1, shadow-wait-v1, wait-reads-v1), with nothing declared
of the spread and nothing released during a run.

The mass is an external body (external-body-v1) of the family `star` at the
centre of the 25 x 25 x 25 cube (r <= 12, the machine's budget of the day),
amount 2^20 with `release` [1, 2^20 / X] so that X quanta leave on every heading
per interval of the prefill (`initial_field` `{"fill": T}`: T intervals of the
Node's mixing from the body, the fractions parked as ninths, the body
reflecting what comes home). A thing at rest cannot be held (every ray moves
one Link per interval, point 21; a held record has no clock), so the mass is a
body: it absorbs things, returns shadows and radiates nothing during the run.
The prefill refuses a fill beyond 30 intervals at X = 1 and beyond 14 at
X >= 64 (the returning shares carry a third phase on one Port of the source),
so two masses are declared at the longest fill each admits: `m16`, X = 16 for
15 intervals (1440 quanta given with the board, S = 96 per interval of fill),
and `m256`, X = 256 for 14 (21 504 quanta, S = 1536).

The light is a thing of the `light` family (clock declared, content 1, K 1:
one phase step per interval on the circle N = 64), one per lamp, each lamp its
own thing; the coupling `gravity` is the momentum table `{"star": -1}` read by
content (point 16), so one shadow quantum of the star met by a light thing
pushes it one quantum toward the star, a whole step at its next departure (the
settled rule (i)), and costs it w intervals of wait (point 23, `wait_per_quantum`
w = 1 or [11, 9]; with `wait_reads` "amplitude" the size of the coherent sum
instead, feature 16f, and then also at round 6's w = 0.7425 sqrt(S) for a
single-owner star, [65, 9] for m16, and at three times it, [196, 9], the
engine's w being the derivation's times 3 (round 6: the engine counts whole
units of amplitude times the content, the derivation reads 3|u|)).

Bending worlds (`bend_{mass}_{w}_{option}_b{b}`): six lines parallel to x at
impact parameter b (y = 12 + b and y = 12 - b, z = 12 and 12 +- 1, the
Euclidean b of the offset lines sqrt(b^2 + 1)), one light thing per line
launched at x = 0 on +X at tick 0, a mark (setting [1, 1]: every thing absorbed,
every shadow returned) at x = 24 on each line recording the arrival tick; 60
ticks (a straight pass arrives at tick 24). The controls `bend_control_a` (b = 3
and 4) and `bend_control_b` (b = 6 and 8) are the same lines without the star.

Clock worlds (`clock_{mass}_{w}_{option}`): eight clocks, each a light thing in
a cavity of six mirror bodies (`mirror`, the coupling `reflect`: the arriving
light leaves on the reversed heading) around a centre at distance r from the
star on a half-axis (+X: r = 3 and 7, -X: 4 and 8, +Y: 5 and 9, -Y: 6 and 10),
launched from the centre outward at tick 0; it alternates between the centre
and a mirror, reads the field at the centre on every other interval, a push on
its own axis turns it nowhere and a transverse push turns it toward another
mirror of the same cavity, so it stays. Its rate is its phase steps per
interval, read from the record as the intervals in which it moved (a waiting
interval advances no phase, K 1). 150 ticks. `clock_control` is the same
without the star.

The options: `law` (no `shadow_wait`, no `wait_reads`: the law as it stands),
`amp` (`wait_reads` "amplitude", no `shadow_wait`: a share turned back at a
waiting thing may mix back onto it two ticks later, as stated in the entry),
`thing` and `field` (`shadow_wait` {"per_quantum": w, "reads": ...}, feature
16e). w is `w1` (1), `w11_9` ([11, 9]), `wS` ([65, 9]) or `w3S` ([196, 9], the
amplitude reading's w for m16 in the derivation's and the engine's count).

Run:  python examples/nature/a6_law/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
N = 64  # the phase circle, one for the world (model owner, 2026-09-18)
K = 1
LIGHT = 1
SHAPE = (25, 25, 25)
STAR = (12, 12, 12)
AMOUNT = 1 << 20
# The masses: X quanta per heading per interval of the fill, T intervals.
MASSES = {"m16": (16, 15), "m256": (256, 12)}  # the closed board admits 12 at X = 256
WAITS = {"w1": 1, "w11_9": [11, 9], "wS": [65, 9], "w3S": [196, 9]}
IMPACT = (3, 4, 6, 8)
LINE_OFFSETS = ((1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1))  # (side, dz)
BEND_TICKS = 200
CLOCK_TICKS = 300
BOUNDARY = "periodic"
# The clocks: (axis, r) for the eight cavities, on the Y and Z half-axes (a
# mirror body's token heads +X, and lanes-v1 refuses a light thing leaving a
# mirror on +X, so the cavities' x-sides are absorbing marks, not mirrors).
CLOCKS = (
    ((0, 1, 0), 3),
    ((0, 1, 0), 7),
    ((0, -1, 0), 4),
    ((0, -1, 0), 8),
    ((0, 0, 1), 5),
    ((0, 0, 1), 9),
    ((0, 0, -1), 6),
    ((0, 0, -1), 10),
)


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


MOMENTUM = {
    "name": "momentum",
    "components": 3,
    "units": "quantum times heading",
    "signed": True,
    "conserved": True,
    "extensive": True,
}


def family(name, slots, *, clock=False, release=None):
    entry = {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "charge": 0,
    }
    if clock:
        entry["clock"] = True
    if release is not None:
        entry["release"] = list(release)
    return entry


def gravity_rule():
    """The light pushed by every star shadow it meets, read by its content."""
    return {
        "name": "gravity",
        "participants": [{"type": "light"}, {"type": "star"}],
        "momentum_table": {"star": -1},
        "reads": "content",
        "invariants": [
            {
                "name": "energy",
                "expression": {
                    "op": "add",
                    "args": [
                        {"field": "amount", "participant": 0},
                        {"field": "amount", "participant": 1},
                    ],
                },
            }
        ],
    }


def reflect_rule():
    """The mirror body's coupling: the arriving light leaves on the reversed
    heading, the mirror returned unchanged."""
    return {
        "name": "reflect",
        "participants": [{"type": "light"}, {"type": "mirror"}],
        "outputs": [
            {"field": "light", "amount": {"of": 0}, "heading": "reversed", "phase": "same", "input": 0},
            {"field": "mirror", "amount": {"of": 1}, "heading": "same", "phase": "same", "input": 1},
        ],
        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
    }


def base(model_id, shape, ticks, wait, option, boundary=BOUNDARY):
    document = {
        "schema_version": 1,
        "model_id": model_id,
        "shape": list(shape),
        "boundary": boundary,
        "dense_field": True,
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "N": N,
        "K": K,
        "wait_per_quantum": wait,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
    }
    if option == "amp":
        document["wait_reads"] = "amplitude"
    elif option in ("thing", "field"):
        document["shadow_wait"] = {"per_quantum": wait, "reads": option}
    elif option != "law":
        raise ValueError(option)
    return document


def lamp(name, heading):
    """A lamp of one light thing of content 1, its own thing id, emitting on
    `heading` at tick 0 and spending its content (node-is-ports-v1)."""
    kind = {
        "name": name,
        "fields": ["light", "momentum"],
        "defaults": {"light": LIGHT, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    emission = {
        "type": name,
        "field": "light",
        "amount": LIGHT,
        "denominator": 1,
        "heading": list(heading),
        "kerengonen_phase": 0,
    }
    return kind, emission


def star_body(mass):
    x, fill = MASSES[mass]
    return {"position": list(STAR), "family": "star", "amount": AMOUNT, "phase": 0}, [1, AMOUNT // x], fill


def bending_world(name, *, mass, wait_name, option, impacts, star_on=True, boundary=BOUNDARY, ticks=BEND_TICKS):
    """One bending world: the lines of each b in `impacts` (six per b); on the
    closed board the light circulates and every lap is a pass (no mark); on the
    open control a mark at x = 24 on each line records the arrival tick; the star
    at the centre when `star_on`."""
    lines = [(b, side, dz) for b in impacts for side, dz in LINE_OFFSETS]
    kinds, emissions, seeds, marks = [], [], [], []
    for index, (b, side, dz) in enumerate(lines):
        y, z = STAR[1] + side * b, STAR[2] + dz
        kind, emission = lamp(f"lamp_{index}", (1, 0, 0))
        kinds.append(kind)
        emissions.append(emission)
        seeds.append({"position": [0, y, z], "type": f"lamp_{index}"})
        if boundary == "open":
            marks.append({"position": [SHAPE[0] - 1, y, z], "setting": [1, 1]})
    body, release, fill = star_body(mass)
    document = base(f"a6-law-{name.replace('_', '-')}", SHAPE, ticks, WAITS[wait_name], option, boundary) | {
        "fields": [scalar("star"), scalar("light"), MOMENTUM],
        "disturbance_types": kinds,
        "spatial_fields": [family("star", 16, release=release), family("light", 8, clock=True)],
        "emissions": emissions,
        "seeds": seeds,
        "ray_interactions": [gravity_rule()],
        "detectors": marks,
        "external_bodies": [],
    }
    if star_on:
        document["external_bodies"] = [body]
        document["initial_field"] = {"star": {"fill": fill}}
    return document


def clock_world(name, *, mass, wait_name, option, star_on=True, boundary=BOUNDARY, ticks=CLOCK_TICKS):
    """The clock world: eight cavities (CLOCKS), each a light thing launched from
    the cavity's centre outward along its half-axis, four mirror bodies on the
    y and z sides and two absorbing marks on the x sides (a clock pushed onto x
    is absorbed and counted, and its rate is read until then)."""
    kinds, emissions, seeds, bodies, marks = [], [], [], [], []
    for index, (axis, r) in enumerate(CLOCKS):
        centre = [STAR[i] + axis[i] * r for i in range(3)]
        kind, emission = lamp(f"clock_{index}", axis)
        kinds.append(kind)
        emissions.append(emission)
        seeds.append({"position": centre, "type": f"clock_{index}"})
        for heading in HEADINGS:
            mirror = [centre[i] + heading[i] for i in range(3)]
            if any(not 0 <= mirror[i] < SHAPE[i] for i in range(3)) or tuple(mirror) == STAR:
                raise ValueError(f"a cavity at r = {r} on {axis} does not fit the board")
            if heading[0]:
                marks.append({"position": mirror, "setting": [1, 1]})
            else:
                bodies.append({"position": mirror, "family": "mirror", "amount": 1, "coupling": "reflect"})
    body, release, fill = star_body(mass)
    document = base(f"a6-law-{name.replace('_', '-')}", SHAPE, ticks, WAITS[wait_name], option, boundary) | {
        "fields": [scalar("star"), scalar("light"), scalar("mirror"), MOMENTUM],
        "disturbance_types": kinds,
        "spatial_fields": [
            family("star", 16, release=release),
            family("light", 8, clock=True),
            family("mirror", 2),
        ],
        "emissions": emissions,
        "seeds": seeds,
        "ray_interactions": [gravity_rule(), reflect_rule()],
        "detectors": marks,
        "external_bodies": bodies,
    }
    if star_on:
        document["external_bodies"] = [body] + bodies
        document["initial_field"] = {"star": {"fill": fill}}
    return document


def cases():
    """The worlds of the series in the order they are run: the clocks first (the
    slope against r under both readings), then the bending, then the options of
    feature 16e; one open-board control of each kind beside the closed board."""
    yield "clock_m16_w1_law", clock_world("clock_m16_w1_law", mass="m16", wait_name="w1", option="law")
    yield "clock_m16_w1_amp", clock_world("clock_m16_w1_amp", mass="m16", wait_name="w1", option="amp")
    yield "clock_control", clock_world("clock_control", mass="m16", wait_name="w1", option="law", star_on=False)
    for mass, wait_name, option in (
        ("m16", "w11_9", "law"),
        ("m16", "w11_9", "amp"),
        ("m256", "w1", "law"),
        ("m256", "w1", "amp"),
        ("m16", "w3S", "amp"),
        ("m16", "wS", "amp"),
    ):
        name = f"clock_{mass}_{wait_name}_{option}"
        yield name, clock_world(name, mass=mass, wait_name=wait_name, option=option)
    yield "clock_m16_w1_law_open", clock_world("clock_m16_w1_law_open", mass="m16", wait_name="w1", option="law", boundary="open", ticks=150)
    yield "bend_control", bending_world("bend_control", mass="m16", wait_name="w1", option="law", impacts=(3, 6), star_on=False)
    for mass, wait_name in (("m16", "w1"), ("m16", "w11_9")):
        for impacts in ((3, 6), (4, 8)):
            name = f"bend_{mass}_{wait_name}_law_b{impacts[0]}_{impacts[1]}"
            yield name, bending_world(name, mass=mass, wait_name=wait_name, option="law", impacts=impacts)
    yield "bend_m256_w1_law_b6_8", bending_world("bend_m256_w1_law_b6_8", mass="m256", wait_name="w1", option="law", impacts=(6, 8))
    yield "bend_m16_w1_law_b3_6_open", bending_world("bend_m16_w1_law_b3_6_open", mass="m16", wait_name="w1", option="law", impacts=(3, 6), boundary="open", ticks=60)
    for wait_name in ("w1", "w11_9"):
        for option in ("thing", "field"):
            name = f"clock_m16_{wait_name}_{option}"
            yield name, clock_world(name, mass="m16", wait_name=wait_name, option=option)
            for impacts in ((3, 6), (4, 8)):
                name = f"bend_m16_{wait_name}_{option}_b{impacts[0]}_{impacts[1]}"
                yield name, bending_world(name, mass="m16", wait_name=wait_name, option=option, impacts=impacts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path.name, document["shape"], document["ticks"])


if __name__ == "__main__":
    main()
