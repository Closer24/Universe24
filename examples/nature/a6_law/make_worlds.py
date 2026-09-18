"""Write the worlds of experiment A6 repeated under the law of the bit
(docs/EXPERIMENTS.md, "A6 repeated under the law of the bit (2026-09-18)"): the
four gravitational tests against Einstein on the engine of features 15 to 18,
16e and 16f (bit-law-v1, node-mixing-v1, clock-readings-v1, node-is-ports-v1,
lanes-v1, return-field-v1, shadow-wait-v1, wait-reads-v1), with nothing declared
of the spread and nothing released during a run.

The board is closed (`boundary` `periodic`, the model owner's decision of
2026-09-18, Highlights 5.4 "The board of a run is closed"): a cube of 33 Nodes a
side with the mass at its centre (16, 16, 16), so that the field wraps around
16 Links from the mass on every axis, beyond the farthest clock (r = 10, its
outer mirror at 11) and the farthest bending line (b = 8), and beyond the reach
of the field's whole quanta (r = 8 at X = 256, the probe below); a fill of F
intervals reaches the Manhattan radius F before tick 0, so the wrap-around
meets itself at the boundary planes at tick 16 - F of the run (tick 2 for a
fill of 14). A cube of 41 was tried first (the wrap-around at 20): its runs
take 5 GB each and 10 s per tick, two at a time on the machine of the day
(16 GB), and the series did not fit. The field is settled before it is read: `standing_field` is
declared, so the dense region looks for a repeat of its state (a fixed point or
a cycle) within the run and replays the cycle from then on; the run's record
carries the iterations to the cycle and the residual (standing-field-v1). No
world of the series is open: "only closed worlds are tested" (the model owner,
2026-09-18, Highlights 5.4 "The board of a run is closed", PR #314).

The mass is an external body (external-body-v1) of the family `star`, amount
2^20 with `release` [1, 2^20 / X] so that X quanta leave on every heading per
interval of the prefill (`initial_field` `{"fill": F}`: F intervals of the
Node's mixing from the body, the fractions parked as ninths, the body absorbing
what comes home and releasing it again). A thing at rest cannot be held (every
ray moves one Link per interval, point 21; a held record has no clock), so the
mass is a body: it absorbs things, returns shadows and radiates nothing during
the run. The flux of the prefill is S = 6X quanta per interval and the
derivation's GM = S / (2 pi) (DERIVATIONS.md section 34). The masses: `m256`
(X = 256, S = 1536, GM = 244), `m64` (X = 64, S = 384, GM = 61) and `m16`
(X = 16, S = 96, GM = 15.3), the fill 14 intervals, the longest the prefill
admits on this board (it refuses a third phase on one Port of the source
once the returning shares come home; 20 is refused). The probe
(`probe_field.py`) reads the whole quanta of the prefilled field on this
41^3 board: a transient that parks as ninths within about 100 intervals,
reaching r = 4 at X = 16 and r = 8 at X = 256, so `m256` is the mass whose field the
clocks at r = 3 to 8 read at all, and `m64` and `m16` read the scaling with
S beside it.

The light is a thing of the `light` family (clock declared, content 1, K 1:
one phase step per interval on the circle N = 64), one per lamp, each lamp its
own thing; the coupling `gravity` is the momentum table `{"star": -1}` read by
content (point 16), so one shadow quantum of the star met by a light thing
pushes it one quantum toward the source of that shadow, a whole step at its
next departure when the push is transverse to its heading (the settled rule
(i); a push along its own axis turns it nowhere), and costs it w intervals of
wait (point 23, `wait_per_quantum`). `wait_reads` names what the wait counts
(feature 16f): `amount`, the whole quanta of push read (the law as written), or
`amplitude`, the whole units of the size of the coherent sum of the arriving
shadows at the thing's Node (the engine's unit: 3|u| in the derivation's, so
the engine's w is the derivation's w / 3). w is 1 first, then the GR w of
DERIVATIONS.md section 40, w_GR = 1.861 sqrt(GM) in the derivation's unit for
the star as one owner, declared to the engine as 3 x 1.861 sqrt(S / (2 pi)) as
the fraction [n, 100].

Clock worlds (`clock_{mass}_{w}_{reading}_{batch}`): four cavities, one on
each of the half-axes +Y, -Y, +Z and -Z (a mirror body's token heads +X and
lanes-v1 refuses a light thing leaving a mirror on +X, so no cavity lies on
the X axis), each a light thing between two mirror bodies (`mirror`, the
coupling `reflect`: the arriving light leaves on the reversed heading) at r - 1
and r + 1 along the half-axis, the cavity one Link aside of the axis on X (a
mirror on the axis returns the star's shadows straight to the source, whose
Port holds two phases, and the prefill refuses the third; the Euclidean r is
sqrt(r^2 + 1)), launched from the centre at r outward at tick 0. It
alternates between the centre and a mirror and reads the field at the centre on
every other interval; a push along its axis turns it nowhere or reverses it
(it stays), a transverse push (a shadow arriving on a side Port) turns it out
of the cavity, and its rate is read until then. A closed cavity of six walls
would shield it completely (a body returns every shadow), so the cavity is
open on its four sides. Batch `a` holds r = 3, 5, 8 (and 5 again on -Z, the
symmetry check), batch `b` r = 4, 6, 10 (and 6 again). 300 ticks. `m256`
under both readings at w = 1 and at the GR w, `m64` under both at w = 1;
`clock_control_{batch}` is the same without the star.

Bending worlds (`bend_{mass}_{w}_{reading}_b{b1}_{b2}`): twelve lines parallel
to X, six per impact parameter (b = 3 and 6 in one world, 4 and 8 in the
other, a world holding at most sixteen thing types), at y = 16 + b and 16 - b,
z = 16 and 16 +- 1 (the Euclidean b of the offset lines sqrt(b^2 + 1)), one
light thing per line launched at x = 0 on +X at tick 0, and a mark (setting
[1, 1]: every thing absorbed, every shadow returned) at x = 32 on each line
recording the arrival tick: a straight pass arrives at tick 32, and x_A = x_B
= 16 for the Shapiro delay. 100 ticks. `m256` under both readings at w = 1
and at the GR w, `m64` and `m16` under `amount` at w = 1; `bend_control_*`
is the same without the star.

The separating run (`sep_{option}`, DERIVATIONS.md section 37 (ix) and 43 (x)):
a source body A of the family `source` (X = 1024, fill 14: the whole quanta
of a weaker source never reach B, the probe above) at (14, 2, 8) and a
receiver B, a light thing in a Y cavity at (30, 18, 24), on the body diagonal
through both, the mass M (X = 7, S = 42, GM = 6.7, the S = 40 of section 37)
at the centre at impact parameter sqrt(72) = 8.5 from the line, and once more
with M = `m256`, whose whole quanta fill r <= 8 around it and are what the
`field` reading counts; B's coupling names `source` only
(`{"source": -1}`), so its momentum first moves at the first whole quantum of
A's field that reaches it, the front of A's field having crossed M's field on
the way; A's front stands at Manhattan radius 14 at tick 0 and B is at
Manhattan distance 48 from A (Euclidean 27.7). The options: `law` (no `shadow_wait`), `thing`
and `field` (`shadow_wait` {"per_quantum": 1, "reads": ...}, feature 16e);
`sep_nomass` is `law` without M; `sep_{option}_m256` the same with M = `m256`.
150 ticks. (No whole quantum of A reaches B, nor M's Node 17.3 Links from
A, within 150 intervals: the geometry of section 37 is not reachable in
whole quanta at this flux, and a nearer receiver would not cross M's field.)

Run:  python examples/nature/a6_law/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bit_law_migration import migrate  # noqa: E402

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
N = 64  # the phase circle, one for the world (model owner, 2026-09-18)
K = 1
LIGHT = 1
SIDE = 33
SHAPE = (SIDE, SIDE, SIDE)
STAR = (SIDE // 2, SIDE // 2, SIDE // 2)
AMOUNT = 1 << 20
# The masses: X quanta per heading per interval of the fill, and the fill.
MASSES = {"m256": (256, 14), "m64": (64, 14), "m16": (16, 14), "m7": (7, 14)}
IMPACT = (3, 4, 6, 8)
BENDING_PAIRS = ((3, 6), (4, 8))  # two worlds of twelve lines, sixteen types at most
LINE_OFFSETS = ((1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1))  # (side, dz)
BEND_TICKS = 100
CLOCK_TICKS = 300
SEP_TICKS = 150
BOUNDARY = "periodic"
# The cavities per batch: (axis, r) on the Y and Z half-axes; every cavity's
# centre is offset by one Link on X (`CAVITY_OFFSET`), so that its mirrors
# reflect the star's shadows along a line that passes the star one Link
# aside: a mirror on the axis returns them straight to the source, whose
# Port holds two phases, and the prefill refuses the third (the Euclidean r
# of the cavity is sqrt(r^2 + 1)).
CAVITY_OFFSET = (1, 0, 0)
BATCHES = {
    "a": (((0, 1, 0), 3), ((0, -1, 0), 5), ((0, 0, 1), 8), ((0, 0, -1), 5)),
    "b": (((0, 1, 0), 4), ((0, -1, 0), 6), ((0, 0, 1), 10), ((0, 0, -1), 6)),
}
# The separating run: A, B and the mass, DERIVATIONS.md section 37 (ix).
SEP_SOURCE = (14, 2, 8)
SEP_RECEIVER = (30, 18, 24)
SEP_SOURCE_X, SEP_SOURCE_FILL = 1024, 14


def flux(mass):
    """S, the prefill's flux: quanta per interval over the six headings."""
    return 6 * MASSES[mass][0]


def gm(mass):
    """The derivation's GM = S / (2 pi) (DERIVATIONS.md section 34)."""
    return flux(mass) / (2 * math.pi)


def gr_wait(mass):
    """The GR w of DERIVATIONS.md section 40 for the star as one owner,
    1.861 sqrt(GM) in the derivation's unit, times 3 for the engine's
    (wait-reads-v1 counts 3|u|), as the fraction [n, 100]."""
    return [round(100 * 3 * 1.861 * math.sqrt(gm(mass))), 100]


def waits(mass):
    return {"w1": 1, "wgr": gr_wait(mass)}


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
        "metric": "links",
        "pace": [1, 1],
        "charge": 0,
    }
    if clock:
        entry["clock"] = True
    if release is not None:
        entry["release"] = list(release)
    return entry


def gravity_rule(pusher="star"):
    """The light pushed by every shadow of `pusher` it meets, read by its content."""
    return {
        "name": "gravity",
        "participants": [{"type": "light"}, {"type": pusher}],
        "momentum_table": {pusher: -1},
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


def base(model_id, ticks, wait, reading, option, boundary=BOUNDARY):
    document = {
        "schema_version": 1,
        "model_id": model_id,
        "shape": list(SHAPE),
        "boundary": boundary,
        "dense_field": True,
        "standing_field": True,
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
    if reading == "amplitude":
        document["wait_reads"] = "amplitude"
    elif reading != "amount":
        raise ValueError(reading)
    if option in ("thing", "field"):
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


def body(position, name, x_per_heading):
    """An external body of `name` at `position` releasing `x_per_heading`
    quanta per heading per interval of the prefill; the body and its release."""
    return {"position": list(position), "family": name, "amount": AMOUNT, "phase": 0}, [
        1,
        AMOUNT // x_per_heading,
    ]


def cavity(index, centre, axis):
    """A light thing launched from `centre` along `axis` between two mirror
    bodies at centre -+ axis; the lamp's kind and emission, the seed and the
    two bodies."""
    kind, emission = lamp(f"clock_{index}", axis)
    seed = {"position": list(centre), "type": f"clock_{index}"}
    mirrors = []
    for sense in (1, -1):
        mirror = [centre[i] + sense * axis[i] for i in range(3)]
        if any(not 0 <= mirror[i] < SHAPE[i] for i in range(3)) or tuple(mirror) == STAR:
            raise ValueError(f"a cavity at {centre} on {axis} does not fit the board")
        mirrors.append({"position": mirror, "family": "mirror", "amount": 1, "coupling": "reflect"})
    return kind, emission, seed, mirrors


def clock_world(
    name, *, mass, wait_name, reading, batch, star_on=True, boundary=BOUNDARY, ticks=CLOCK_TICKS
):
    """The clock world: the four cavities of `batch` (BATCHES), each on a half-axis
    at its r from the star, open on its four sides."""
    kinds, emissions, seeds, bodies = [], [], [], []
    for index, (axis, r) in enumerate(BATCHES[batch]):
        centre = [STAR[i] + axis[i] * r + CAVITY_OFFSET[i] for i in range(3)]
        kind, emission, seed, mirrors = cavity(index, centre, axis)
        kinds.append(kind)
        emissions.append(emission)
        seeds.append(seed)
        bodies.extend(mirrors)
    star, release = body(STAR, "star", MASSES[mass][0])
    document = base(
        f"a6-law-{name.replace('_', '-')}", ticks, waits(mass)[wait_name], reading, "law", boundary
    ) | {
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
        "detectors": [],
        "external_bodies": bodies,
    }
    if star_on:
        document["external_bodies"] = [star] + bodies
        document["initial_field"] = {"star": {"fill": MASSES[mass][1]}}
    return document


def bending_world(
    name, *, mass, wait_name, reading, impacts, star_on=True, boundary=BOUNDARY, ticks=BEND_TICKS
):
    """One bending world: six lines per b in `impacts`, a mark at x = 40 on each,
    the star at the centre when `star_on`."""
    lines = [(b, side, dz) for b in impacts for side, dz in LINE_OFFSETS]
    kinds, emissions, seeds, marks = [], [], [], []
    for index, (b, side, dz) in enumerate(lines):
        y, z = STAR[1] + side * b, STAR[2] + dz
        kind, emission = lamp(f"lamp_{index}", (1, 0, 0))
        kinds.append(kind)
        emissions.append(emission)
        seeds.append({"position": [0, y, z], "type": f"lamp_{index}"})
        marks.append({"position": [SHAPE[0] - 1, y, z], "setting": [1, 1]})
    star, release = body(STAR, "star", MASSES[mass][0])
    document = base(
        f"a6-law-{name.replace('_', '-')}", ticks, waits(mass)[wait_name], reading, "law", boundary
    ) | {
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
        document["external_bodies"] = [star]
        document["initial_field"] = {"star": {"fill": MASSES[mass][1]}}
    return document


def separating_world(name, *, option, mass="m7", mass_on=True, ticks=SEP_TICKS):
    """The separating run: the source body A, the receiver B in a Y cavity, and
    the mass M at the centre under the `shadow_wait` option."""
    kind, emission, seed, mirrors = cavity(0, SEP_RECEIVER, (0, 1, 0))
    source, source_release = body(SEP_SOURCE, "source", SEP_SOURCE_X)
    star, mass_release = body(STAR, "star", MASSES[mass][0])
    document = base(f"a6-law-{name.replace('_', '-')}", ticks, 1, "amount", option) | {
        "fields": [scalar("star"), scalar("source"), scalar("light"), scalar("mirror"), MOMENTUM],
        "disturbance_types": [kind],
        "spatial_fields": [
            family("star", 16, release=mass_release),
            family("source", 16, release=source_release),
            family("light", 8, clock=True),
            family("mirror", 2),
        ],
        "emissions": [emission],
        "seeds": [seed],
        "ray_interactions": [gravity_rule("source"), reflect_rule()],
        "detectors": [],
        "external_bodies": [source] + mirrors,
        "initial_field": {"source": {"fill": SEP_SOURCE_FILL}},
    }
    if mass_on:
        document["external_bodies"] = [star, source] + mirrors
        document["initial_field"]["star"] = {"fill": MASSES[mass][1]}
    return document


def cases():
    """The worlds of the series in the order they are run (four at a time, the
    machine's cores): the clocks of m256 at w = 1 (the two slopes), the bending
    of m256 at w = 1, the controls, the separating run, the GR w, the scaling
    masses."""
    for wait_name in ("w1",):
        for batch in ("a", "b"):
            for reading in ("amount", "amplitude"):
                name = f"clock_m256_{wait_name}_{reading}_{batch}"
                yield (
                    name,
                    clock_world(name, mass="m256", wait_name=wait_name, reading=reading, batch=batch),
                )
    for impacts in BENDING_PAIRS:
        tail = f"b{impacts[0]}_{impacts[1]}"
        for reading in ("amount", "amplitude"):
            name = f"bend_m256_w1_{reading}_{tail}"
            yield (
                name,
                bending_world(name, mass="m256", wait_name="w1", reading=reading, impacts=impacts),
            )
    for impacts in BENDING_PAIRS:
        tail = f"b{impacts[0]}_{impacts[1]}"
        name = f"bend_control_{tail}"
        yield (
            name,
            bending_world(
                name, mass="m256", wait_name="w1", reading="amount", impacts=impacts, star_on=False
            ),
        )
    for batch in ("a", "b"):
        name = f"clock_control_{batch}"
        yield (
            name,
            clock_world(name, mass="m256", wait_name="w1", reading="amount", batch=batch, star_on=False),
        )
    for option in ("law", "thing", "field"):
        yield f"sep_{option}", separating_world(f"sep_{option}", option=option)
    yield "sep_nomass", separating_world("sep_nomass", option="law", mass_on=False)
    for batch in ("a", "b"):
        for reading in ("amount", "amplitude"):
            name = f"clock_m256_wgr_{reading}_{batch}"
            yield name, clock_world(name, mass="m256", wait_name="wgr", reading=reading, batch=batch)
    for impacts in BENDING_PAIRS:
        tail = f"b{impacts[0]}_{impacts[1]}"
        for mass in ("m64", "m16"):
            name = f"bend_{mass}_w1_amount_{tail}"
            yield name, bending_world(name, mass=mass, wait_name="w1", reading="amount", impacts=impacts)
    for batch in ("a", "b"):
        for reading in ("amount", "amplitude"):
            name = f"clock_m64_w1_{reading}_{batch}"
            yield name, clock_world(name, mass="m64", wait_name="w1", reading=reading, batch=batch)
    for impacts in BENDING_PAIRS:
        tail = f"b{impacts[0]}_{impacts[1]}"
        for reading in ("amount", "amplitude"):
            name = f"bend_m256_wgr_{reading}_{tail}"
            yield (
                name,
                bending_world(name, mass="m256", wait_name="wgr", reading=reading, impacts=impacts),
            )
    for option in ("law", "thing", "field"):
        yield f"sep_{option}_m256", separating_world(f"sep_{option}_m256", option=option, mass="m256")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(migrate(document), indent=1) + "\n", encoding="utf-8")
        print(path.name, document["shape"], document["ticks"], document["wait_per_quantum"])


if __name__ == "__main__":
    main()
