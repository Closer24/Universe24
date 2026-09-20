"""The detector under the law of the ray (docs/RAY_LAW.md, section 5): the
wave is a reading of a crowd of rays at a detector and lives nowhere else.
A detector is a SET of Nodes with ONE record (the model owner, 2026-09-19:
"a detector measuring three Nodes sees one electron that can be on any of
the three"): per interval and family, under the reading `wave`, the
clicked rays' amplitudes A_u = 32 x amount_u at their phases (the 1/256
tables) are summed over the whole set by the one decomposition, the record
is X^2 + Y^2 of its scalar and the set's phase (the pointer's nearest step)
is returned to every measured event of the set; under the reading `beam`
(the default) the arriving rays are paired by opposite phase over the set,
a paired couple passes on and the rest click, the record the plain count;
the threshold gates every response of a detector over the amount summed
over the set, a receiver's and a re-emitter's alike, a smaller set passing
with a `pass` record; a release reads no threshold. What an arrival does
stays at its Node (the content joins the measured event it reached, the
push, the label). The expected integers of docs/TEST_EXPECTATIONS.md ("The
detector's record"), written down first. K 2^20, `suspension` 0, `release`
[0, 1], the families `m` (free) and `light` (paid), every measured event
`fixed`, the detector `d` declared `wave` in (a) to (e):

(a) two rays of amount 1 arriving in one interval at a counter of threshold
    1, in phase (0 and 0): the record 4 x 32^2 x 256^2 = 268435456, the
    amount 2 and two clicks; in antiphase (0 and 32): the record 0, the
    amount 2 and two clicks; one ray alone: 32^2 x 256^2 = 67108864; the
    `record` line of `events.jsonl` carries the pointer (X, Y) and the
    square; the run's detector report carries the cumulative record;
(b) a receiver (a measured event of `m`, content 4, measuring light) at
    threshold 3 (from `test_detector_sensitivity` (a), re-pinned): 2 rays of
    another number pass with a `pass` record (`threshold` 3), no click, no
    push, the rays going on whole; 3 rays are measured: 3 clicks, `held`
    [4, 3], the momentum (192, 0, 0) (three labels of 64 along +X: since
    2026-09-19 the label of a unit along a heading is Q e_d, Q = 64,
    RAY_LAW section 2 and note 23), nothing left in the store, the report
    3 measured, 3 clicks, the record (3 x 32)^2 x 256^2 = 9 x 32^2 x 256^2
    (a row of three identical rays is one coherent amplitude);
(c) a re-emitter at threshold 3 (from (b) there): 2 rays pass; 3 rays are
    taken (re-released 3, no click, the push (192, 0, 0), the recoil at
    the re-emission -(64, 64, 64) leaving the momentum (128, -64, -64))
    and created again at the same interval's self-creation, one per
    declared direction (+X, +Y, +Z), with the re-emitter's number, the
    arriving phase 20, content 1, age 0;
(d) an emitter inside a detector reads no threshold: a lamp of light
    (content 24, K 24, rate [1, 1]) in a detector of threshold 5 releases
    one unit per heading per interval, its content 18 then 12; a reader of
    `m` (content 4) at threshold 4 passes 3 rays and reads 4, pushed by
    -M x 64 c = (-1024, 0, 0);
(e) the record is exact and never refused (2026-09-19, after the night's
    bound refused `two_contents`): every entry (C, S) of the 1/256 tables
    is shorter than 257 for every N from 2 through 4096 (the largest
    C^2 + S^2 is 65897), so each component of the pointer is within
    32 x 257 x the clicked amount and the int64 register holds it up to
    the amount (2^62 - 1) // (32 x 257) = 560759486676481
    (`POINTER_AMOUNT_BOUND`, 2^48 inside, 2^49 beyond); beyond it the
    pointer is summed in Python integers, and the square and the record
    are Python integers always. Every case is compared with the Python-int
    computation X = sum 32 x amount x C[phase], Y = sum 32 x amount x
    S[phase] over the clicked rows of the record (the `click` lines)
    through the tables: a row of 261123 (the old bound) records
    2139119616^2 with the pointer (2139119616, 0); a row of 261124 (one
    past the old bound) records 2139127808^2; a row of 2^18 (what
    `two_contents` sends to a face) records 2^62 exactly, one past the
    law's bound 2^62 - 1; two rows of 130561 and 130563 (two numbers, +X
    and -X, a quarter turn apart) record (2^13 x 130561)^2 + (2^13 x
    130563)^2; a row of 2^49 (beyond the pointer's register bound, as the
    reviewer's silent int64 wrap at 2^52 was; since the label along the
    unit vector, 2026-09-19, a row above 2^50 is refused by the reading's
    second-moment bound, amount x 64^2 x rows, before any record) records
    2^124 with the pointer (2^62, 0); two rows of 2^18
    clicking in the intervals 1 and 3 accumulate 2^63, beyond int64, in
    the detector's record and the report, round-tripped through JSON; a
    ray of 2^18 stepping off the open face +x records 2^62 on `face:+x`;
(f) the set (the model owner's principle, 2026-09-19): a `wave` detector
    `d3` of three Nodes, (4, 0, 1), (4, 1, 1) and (4, 2, 1), each a counter
    of `m` (content 4) measuring light: one ray of amount 1 arriving at
    any one of the three gives one `record` line naming `d3` (its `node`
    and `measured` None: the click says "here, in one of these"), the
    record 32^2 x 256^2 the same whichever Node it reached, and the click
    at the Node it reached (that counter holds [4, 1], the other two
    [4, 0]); at threshold 2 one ray of amount 1 at one Node passes
    (`threshold` 2) while two rays of amount 1 at two different Nodes in
    the same interval both click and record 4 x 32^2 x 256^2 (one pointer
    over the set); the window reads the set's phase: two rays at the
    phases 0 and 16 at two Nodes have the set's phase 8, and with the
    window 20 on every counter both click (the phase 0 alone would be
    outside) while with the window 56 both pass with `window` 56 (the
    phase 0 alone would be inside);
(g) the phase returned (the model owner, 2026-09-19: the detector returns
    to the board the information it received): a click of one ray of
    phase 40 at a one-Node `wave` detector whose counter is at phase 0
    leaves the counter at phase 40 (the report's `phase` 40, the `record`
    line's `phase` 40), the turn of K 2^20 being 0; a lamp of light
    (content 24, K 24, rate [1, 1]) in a `wave` detector that clicks a
    ray of phase 40 at tick 1 releases its six rays of that tick at the
    received phase 40 and is at phase 41 after the interval (the frame's
    turn 1 added after the click), at 42 after the next with its rays at
    41; the set of three Nodes of (f) with the rays at 0 and 16 puts all
    three counters at phase 8; a ray below the threshold leaves the
    counter at phase 0, and a `read` of `m` (a ray of phase 40) leaves the
    reader at phase 0;
(h) the reading `beam` (the model owner, 2026-09-19, "only events"; the
    default): at a one-Node beam detector, two rays of amount 1 in phase
    (0 and 0, +X and -X) both click, the record (the count) 2, the
    `record` line without a pointer and with `phase` 0 (the last clicked
    ray's); opposite (0 and 32) both pass with `cancelled` true, no
    click, the two rays going on whole, the record 0 and no `record`
    line; a quarter turn apart (0 and 16) with the window 16 on the
    counter both are admitted by the gate and paired (the arc the half
    circle centred on the opposite phase), both pass cancelled; without a
    window they are not paired and both click; three rays at the phases
    0 (+X), 32 (-X) and 0 (+Y) in the order of their numbers: the first
    pairs with the second, the third clicks alone (1 click, record 1);
    rows of 3 (phase 0) and 2 (phase 32): 2 units pair and pass, 1 unit
    clicks (the click line's amount 1, the two `cancelled` lines 2 and 2,
    the rows of 2 and 2 in the store); the books balanced in every case;
    the refusal of `"reading": "field"` names the key.
"""

from __future__ import annotations

import json

import pytest

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import RaySimulation, parse_ray_world
from event_universe.events.nature_beam import POINTER_AMOUNT_BOUND
from event_universe.events.world import MOMENTUM_BOUND

M, LIGHT = 0, 1
NODE = [4, 1, 1]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
FAMILIES = [{"name": "m", "quantum": 0}, {"name": "light", "quantum": 1}]
SOURCE = {"position": [0, 1, 1], "family": "light", "amount": 4, "fixed": True}
UNIT_RECORD = 32 * 32 * 256 * 256


def world(
    measured: list[dict[str, object]],
    in_transit: list[dict[str, object]],
    threshold: int,
    clock: int = 1 << 20,
    reading: str = "wave",
    positions: list[list[int]] | None = None,
) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": "ray-detector-test",
        "shape": [9, 3, 3],
        "boundary": "open",
        "ticks": 2,
        "K": clock,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit,
        "detectors": [
            {
                "name": "d",
                "positions": positions or [NODE],
                "threshold": threshold,
                "reading": reading,
            }
        ],
    }


def arrival(
    amount: int,
    family: str = "light",
    number: int = 2,
    phase: int = 0,
    direction: list[int] | None = None,
) -> dict[str, object]:
    """Rays one Link before the detector's Node, arriving in interval 1."""
    heading = direction or [1, 0, 0]
    return {
        "position": [NODE[0] - heading[0], NODE[1] - heading[1], NODE[2] - heading[2]],
        "family": family,
        "number": number,
        "direction": heading,
        "amount": amount,
        "phase": phase,
    }


def test_two_rays_in_phase_record_four_units_and_in_antiphase_nothing():
    """(a)."""
    counter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    other = {"position": [8, 1, 1], "family": "light", "amount": 4, "fixed": True}
    for phases, expected in (((0, 0), 4 * UNIT_RECORD), ((0, 32), 0), ((0,), UNIT_RECORD)):
        rays = [arrival(1, number=2, phase=phases[0])]
        if len(phases) == 2:
            rays.append(arrival(1, number=3, phase=phases[1], direction=[-1, 0, 0]))
        records: list[dict[str, object]] = []
        simulation = RaySimulation(
            parse_ray_world(world([counter, SOURCE, other], rays, 1)), records.append
        )
        entry = simulation.measured[1]
        simulation.step()
        assert simulation.books()["balanced"]
        assert entry.events == [0, len(phases)], phases
        assert entry.detector_set.record == [0, expected], phases
        assert simulation.detectors()[0]["families"]["light"] == {
            "measured": len(phases),
            "clicks": len(phases),
            "record": expected,
            "phase": None if expected == 0 else 0,
        }
        assert simulation.detectors()[0]["reading"] == "wave"
        lines = [r for r in records if r["event"] == "record"]
        assert len(lines) == 1 and lines[0]["record"] == expected and lines[0]["detector"] == "d"
        pointer = lines[0]["pointer"]
        assert pointer[0] ** 2 + pointer[1] ** 2 == expected
        assert lines[0]["node"] == NODE and lines[0]["measured"] == 1


def test_a_receiver_measures_only_a_set_at_its_threshold_and_a_smaller_one_passes():
    """(b)."""
    receiver = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    records: list[dict[str, object]] = []
    simulation = RaySimulation(
        parse_ray_world(world([receiver, SOURCE], [arrival(2)], 3)), records.append
    )
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    assert entry.detector == 0 and entry.threshold == 3
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 0] and entry.held == [4, 0] and entry.momentum == [0, 0, 0]
    assert entry.measured[LIGHT] == NO_RESPONSE
    assert light.size == 1 and int(light.amount[0]) == 2 and int(light.node[0]) == light.flat((4, 1, 1))
    assert [(r["event"], r["amount"], r["threshold"]) for r in records] == [("pass", 2, 3)]
    simulation.step()
    assert simulation.books()["balanced"] and light.size == 1 and int(light.amount[0]) == 2

    records.clear()
    simulation = RaySimulation(
        parse_ray_world(world([receiver, SOURCE], [arrival(3)], 3)), records.append
    )
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 3] and entry.held == [4, 3] and entry.momentum == [192, 0, 0]
    assert entry.pushed == [192, 0, 0] and entry.measured[LIGHT] == {**NO_RESPONSE, "measure": 3}
    assert light.size == 0
    assert simulation.detectors()[0]["families"]["light"] == {
        "measured": 3,
        "clicks": 3,
        "record": 9 * UNIT_RECORD,
        "phase": 0,
    }
    assert [r["event"] for r in records] == ["click", "record"]


def test_a_re_emitter_takes_only_a_set_at_its_threshold_and_creates_it_again_as_its_own():
    """(c)."""
    emitter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "phase": 9,
        "fixed": True,
        "directions": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "table": {"light": "rerelease"},
    }
    simulation = RaySimulation(parse_ray_world(world([emitter, SOURCE], [arrival(2, phase=20)], 3)))
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert (
        entry.measured[LIGHT] == NO_RESPONSE
        and entry.pending == [[], []]
        and entry.momentum == [0, 0, 0]
    )
    assert light.size == 1 and int(light.amount[0]) == 2 and int(light.number[0]) == 2

    records: list[dict[str, object]] = []
    simulation = RaySimulation(
        parse_ray_world(world([emitter, SOURCE], [arrival(3, phase=20)], 3)), records.append
    )
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert [(r["event"], r["amount"], r["push"]) for r in records] == [("rerelease", 3, [192, 0, 0])]
    assert entry.measured[LIGHT] == {**NO_RESPONSE, "rerelease": 3} and entry.events == [0, 0]
    assert entry.held == [4, 0] and entry.pending == [[], []]
    assert entry.pushed == [192, 0, 0] and entry.momentum == [128, -64, -64]
    assert (
        simulation.ledger.transit_absorbed[LIGHT] == 3 and simulation.ledger.transit_released[LIGHT] == 3
    )
    rows = sorted(
        (
            int(light.direction[i]),
            int(light.amount[i]),
            int(light.phase[i]),
            int(light.age[i]),
            int(light.number[i]),
            int(light.content[i]),
        )
        for i in range(light.size)
    )
    assert rows == [(2, 1, 20, 0, 1, 1), (4, 1, 20, 0, 1, 1), (6, 1, 20, 0, 1, 1)]
    assert set(light.node.tolist()) == {light.flat((4, 1, 1))}
    simulation.step()
    assert simulation.books()["balanced"]
    assert sorted(light.node.tolist()) == sorted(
        light.flat(p) for p in ((5, 1, 1), (4, 2, 1), (4, 1, 2))
    )


def test_a_release_reads_no_threshold_and_a_reading_is_gated_like_a_measurement():
    """(d)."""
    lamp = {"position": NODE, "family": "light", "amount": 24, "fixed": True, "lamp": {"rate": [1, 1]}}
    simulation = RaySimulation(parse_ray_world(world([lamp], [], 5, clock=24)))
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    assert entry.detector == 0 and entry.threshold == 5
    for tick in (1, 2):
        simulation.step()
        assert simulation.books()["balanced"], tick
        fresh = light.age == 0
        assert sorted(light.direction[fresh].tolist()) == [2, 3, 4, 5, 6, 7], tick
        assert (light.content[fresh] == 1).all() and (light.amount[fresh] == 1).all()
        assert entry.held == [0, 24 - 6 * tick] and simulation.ledger.held_spent[LIGHT] == 6 * tick, tick
        assert simulation.ledger.transit_released[LIGHT] == 6 * tick and entry.momentum == [0, 0, 0], (
            tick
        )
    assert simulation.detectors()[0]["families"]["light"] == {
        "measured": 0,
        "clicks": 0,
        "record": 0,
        "phase": None,
    }

    source = {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True}
    reader = {"position": NODE, "family": "m", "amount": 4, "fixed": True, "table": {"m": "read"}}
    for amount, push, read in ((3, [0, 0, 0], 0), (4, [-1024, 0, 0], 4)):
        simulation = RaySimulation(
            parse_ray_world(world([source, reader], [arrival(amount, family="m", number=1)], 4))
        )
        entry, m = simulation.measured[2], simulation.stores[M]
        simulation.step()
        assert simulation.books()["balanced"], amount
        assert entry.momentum == push and entry.pushed == push, amount
        assert entry.measured[M] == {**NO_RESPONSE, "read": read}, amount
        assert entry.held == [4, 0] and entry.events == [0, 0], amount
        assert m.size == 1 and int(m.amount[0]) == amount and int(m.number[0]) == 1, amount
        assert simulation.detectors()[0]["families"]["m"] == {
            "measured": 0,
            "clicks": 0,
            "record": 0,
            "phase": None,
        }, amount


def test_the_record_is_exact_and_never_refused():
    """(e)."""
    counter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    other = {"position": [8, 1, 1], "family": "light", "amount": 4, "fixed": True}
    for k in range(1, 13):
        cosines, sines = phase_cosines(1 << k), phase_sines(1 << k)
        assert max(c * c + s * s for c, s in zip(cosines, sines, strict=True)) < 257 * 257
    assert POINTER_AMOUNT_BOUND == MOMENTUM_BOUND // (32 * 257) == 560759486676481
    assert (1 << 48) < POINTER_AMOUNT_BOUND < (1 << 49)
    cosines, sines = phase_cosines(64), phase_sines(64)

    def expected(records: list[dict[str, object]], detector: str) -> tuple[int, int, int]:
        """The Python-int pointer and square of the rows that clicked at `detector`."""
        rows = [
            (int(r["amount"]), int(r["phase"]))
            for r in records
            if r["event"] == "click" and r["detector"] == detector
        ]
        x = sum(32 * amount * cosines[phase] for amount, phase in rows)
        y = sum(32 * amount * sines[phase] for amount, phase in rows)
        return x, y, x * x + y * y

    quarter = arrival(130563, number=3, direction=[-1, 0, 0], phase=16)
    for rays, pointer, square in (
        ([arrival(261123)], (2139119616, 0), 2139119616**2),
        ([arrival(261124)], (2139127808, 0), 2139127808**2),
        ([arrival(1 << 18)], (1 << 31, 0), 1 << 62),
        (
            [arrival(130561), quarter],
            (8192 * 130561, 8192 * 130563),
            8192**2 * (130561**2 + 130563**2),
        ),
        ([arrival(1 << 49)], (1 << 62, 0), 1 << 124),
    ):
        records: list[dict[str, object]] = []
        simulation = RaySimulation(
            parse_ray_world(world([counter, SOURCE, other], rays, 1)), records.append
        )
        simulation.step()
        assert simulation.books()["balanced"], rays
        assert expected(records, "d") == (*pointer, square), rays
        assert simulation.measured[1].detector_set.record == [0, square], rays
        lines = [r for r in records if r["event"] == "record"]
        assert len(lines) == 1 and lines[0]["pointer"] == list(pointer), rays
        assert lines[0]["record"] == square, rays
        amount = sum(int(ray["amount"]) for ray in rays)
        report = simulation.detectors()[0]["families"]["light"]
        phase = report.pop("phase")
        assert report == {"measured": amount, "clicks": amount, "record": square}, rays
        assert phase == (0 if len(rays) == 1 else 8), rays
        assert json.loads(json.dumps(report))["record"] == square, rays
    assert 2139119616**2 < MOMENTUM_BOUND < (1 << 62) < (1 << 63) < (1 << 124)
    # The accumulation: two rows of 2^18, one Link and two Links before the
    # detector (the intervals 1 and 3), record 2^63 in total, beyond int64.
    later = {**arrival(1 << 18, number=3), "position": [NODE[0] - 2, 1, 1]}
    records = []
    simulation = RaySimulation(
        parse_ray_world(world([counter, SOURCE, other], [arrival(1 << 18), later], 1)), records.append
    )
    for _ in range(3):
        simulation.step()
        assert simulation.books()["balanced"]
    assert [r["tick"] for r in records if r["event"] == "record"] == [1, 3]
    entry = simulation.measured[1]
    assert entry.detector_set.record == [0, 1 << 63] and "record" not in entry.state()
    report = json.loads(json.dumps(simulation.detectors()))[0]["families"]["light"]
    assert report["record"] == 1 << 63 and report["clicks"] == 1 << 19
    # A face click: a ray of 2^18 stepping off the open face +x.
    off = {
        "position": [8, 1, 1],
        "family": "light",
        "number": 2,
        "direction": [1, 0, 0],
        "amount": 1 << 18,
        "phase": 0,
    }
    records = []
    simulation = RaySimulation(
        parse_ray_world(world([counter, SOURCE, other], [off], 1)), records.append
    )
    simulation.step()
    assert simulation.books()["balanced"]
    faces = {d["name"]: d["families"]["light"] for d in simulation.face_detectors()}
    assert expected(records, "face:+x") == (1 << 31, 0, 1 << 62)
    assert faces["face:+x"]["record"] == 1 << 62 and faces["face:+x"]["clicks"] == 1 << 18
    assert simulation.detectors()[1:] == simulation.face_detectors()


SET_NODES = [[4, 0, 1], [4, 1, 1], [4, 2, 1]]


def counters(table: dict[str, object] | None = None) -> list[dict[str, object]]:
    """Three counters of `m` measuring light at the set's Nodes, numbers 1 to 3."""
    return [
        {
            "position": node,
            "family": "m",
            "amount": 4,
            "fixed": True,
            "table": table or {"light": "measure"},
        }
        for node in SET_NODES
    ]


def at_node(node: list[int], phase: int = 0, number: int = 4, direction: list[int] | None = None):
    """A ray of light one Link before `node`, arriving in interval 1."""
    heading = direction or [1, 0, 0]
    return {
        "position": [node[0] - heading[0], node[1] - heading[1], node[2] - heading[2]],
        "family": "light",
        "number": number,
        "direction": heading,
        "amount": 1,
        "phase": phase,
    }


def set_world(
    rays: list[dict[str, object]], threshold: int = 1, table: dict[str, object] | None = None
) -> dict[str, object]:
    sources = [SOURCE, {"position": [8, 1, 1], "family": "light", "amount": 4, "fixed": True}]
    document = world([*counters(table), *sources], rays, threshold, positions=SET_NODES)
    document["detectors"][0]["name"] = "d3"
    return document


def test_a_detector_is_a_set_of_nodes_with_one_record():
    """(f)."""
    for reached in range(3):
        records: list[dict[str, object]] = []
        simulation = RaySimulation(
            parse_ray_world(set_world([at_node(SET_NODES[reached], phase=0)])), records.append
        )
        simulation.step()
        assert simulation.books()["balanced"], reached
        lines = [r for r in records if r["event"] == "record"]
        assert len(lines) == 1, reached
        assert lines[0]["detector"] == "d3" and lines[0]["record"] == UNIT_RECORD, reached
        assert lines[0]["node"] is None and lines[0]["measured"] is None, reached
        assert simulation.detectors()[0]["families"]["light"]["record"] == UNIT_RECORD, reached
        assert simulation.detectors()[0]["nodes"] == 3
        clicks = [r for r in records if r["event"] == "click"]
        assert [(c["node"], c["detector"], c["amount"]) for c in clicks] == [
            (SET_NODES[reached], "d3", 1)
        ]
        for k in range(3):
            entry = simulation.measured[k + 1]
            assert entry.held == ([4, 1] if k == reached else [4, 0]), (reached, k)
            assert entry.detector_set is simulation.detector_sets[0]
    # The threshold on the amount summed over the set.
    records = []
    simulation = RaySimulation(parse_ray_world(set_world([at_node(SET_NODES[0])], 2)), records.append)
    simulation.step()
    assert simulation.books()["balanced"]
    assert [(r["event"], r["amount"], r["threshold"]) for r in records] == [("pass", 1, 2)]
    assert simulation.detectors()[0]["families"]["light"]["record"] == 0
    records = []
    two = [at_node(SET_NODES[0], number=4), at_node(SET_NODES[2], number=5, direction=[-1, 0, 0])]
    simulation = RaySimulation(parse_ray_world(set_world(two, 2)), records.append)
    simulation.step()
    assert simulation.books()["balanced"]
    assert [r["event"] for r in records] == ["click", "click", "record"]
    assert simulation.detectors()[0]["families"]["light"] == {
        "measured": 2,
        "clicks": 2,
        "record": 4 * UNIT_RECORD,
        "phase": 0,
    }
    # The window reads the set's phase: the rays at 0 and 16, the set at 8.
    quarter = [at_node(SET_NODES[0], phase=0), at_node(SET_NODES[2], phase=16, number=5)]
    for setting, expected in ((20, ["click", "click", "record"]), (56, ["pass", "pass"])):
        records = []
        table = {"light": {"rule": "measure", "phase_window": setting}}
        simulation = RaySimulation(parse_ray_world(set_world(quarter, 1, table)), records.append)
        simulation.step()
        assert simulation.books()["balanced"], setting
        assert [r["event"] for r in records] == expected, setting
        if setting == 56:
            assert all(r["window"] == 56 for r in records)
        else:
            assert records[-1]["phase"] == 8 and records[-1]["detector"] == "d3"


def test_a_click_returns_the_sets_phase_to_its_measured_events():
    """(g)."""
    counter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    records: list[dict[str, object]] = []
    simulation = RaySimulation(
        parse_ray_world(world([counter, SOURCE], [arrival(1, phase=40)], 1)), records.append
    )
    entry = simulation.measured[1]
    assert entry.phase == 0
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.phase == 40 and entry.turn == 0
    assert simulation.detectors()[0]["families"]["light"]["phase"] == 40
    assert [r["phase"] for r in records if r["event"] == "record"] == [40]
    # A lamp that clicked releases at the received phase; the turn follows.
    lamp = {"position": NODE, "family": "light", "amount": 24, "fixed": True, "lamp": {"rate": [1, 1]}}
    simulation = RaySimulation(
        parse_ray_world(world([lamp, SOURCE], [arrival(1, phase=40)], 1, clock=24))
    )
    entry, light = simulation.measured[1], simulation.stores[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.phase == 41 and entry.events == [0, 1] and entry.held == [0, 24 - 6 + 1]
    fresh = light.age == 0
    assert int(fresh.sum()) == 6 and (light.phase[fresh] == 40).all()
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.phase == 42
    assert (light.phase[light.age == 0] == 41).all()
    # The set of three Nodes: every measured event of the set takes the phase.
    quarter = [at_node(SET_NODES[0], phase=0), at_node(SET_NODES[2], phase=16, number=5)]
    simulation = RaySimulation(parse_ray_world(set_world(quarter)))
    simulation.step()
    assert simulation.books()["balanced"]
    assert [simulation.measured[k].phase for k in (1, 2, 3)] == [8, 8, 8]
    # A pass and a read leave the phase alone.
    simulation = RaySimulation(parse_ray_world(world([counter, SOURCE], [arrival(1, phase=40)], 2)))
    simulation.step()
    assert simulation.books()["balanced"] and simulation.measured[1].phase == 0
    source = {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True}
    reader = {"position": NODE, "family": "m", "amount": 4, "fixed": True, "table": {"m": "read"}}
    simulation = RaySimulation(
        parse_ray_world(world([source, reader], [arrival(4, family="m", number=1, phase=40)], 1))
    )
    simulation.step()
    assert simulation.books()["balanced"]
    assert simulation.measured[2].measured[M]["read"] == 4 and simulation.measured[2].phase == 0


def test_the_beam_reading_pairs_opposite_rays_and_counts_the_rest():
    """(h)."""
    counter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    other = {"position": [8, 1, 1], "family": "light", "amount": 4, "fixed": True}
    below = {"position": [4, 0, 1], "family": "light", "amount": 4, "fixed": True}
    measured = [counter, SOURCE, other, below]

    def run(rays, table=None, threshold=1):
        document = world(
            [{**counter, "table": table or counter["table"]}, SOURCE, other, below],
            rays,
            threshold,
            reading="beam",
        )
        records: list[dict[str, object]] = []
        simulation = RaySimulation(parse_ray_world(document), records.append)
        simulation.step()
        assert simulation.books()["balanced"]
        return simulation, records

    first = arrival(1, number=2, phase=0)
    simulation, records = run([first, arrival(1, number=3, phase=0, direction=[-1, 0, 0])])
    assert [r["event"] for r in records] == ["click", "click", "record"]
    assert records[-1]["record"] == 2 and "pointer" not in records[-1] and records[-1]["phase"] == 0
    assert simulation.detectors()[0]["families"]["light"] == {
        "measured": 2,
        "clicks": 2,
        "record": 2,
        "phase": 0,
    }
    assert simulation.detectors()[0]["reading"] == "beam"
    assert simulation.measured[1].events == [0, 2]
    simulation, records = run([first, arrival(1, number=3, phase=32, direction=[-1, 0, 0])])
    assert [(r["event"], r["number"], r["amount"], r["phase"], r["cancelled"]) for r in records] == [
        ("pass", 2, 1, 0, True),
        ("pass", 3, 1, 32, True),
    ]
    light = simulation.stores[LIGHT]
    assert (
        light.size == 2 and light.amount.tolist() == [1, 1] and simulation.measured[1].events == [0, 0]
    )
    assert simulation.detectors()[0]["families"]["light"]["record"] == 0
    assert simulation.measured[1].held == [4, 0]
    quarter = [first, arrival(1, number=3, phase=16, direction=[-1, 0, 0])]
    simulation, records = run(quarter, {"light": {"rule": "measure", "phase_window": 16}})
    assert [(r["event"], r["phase"]) for r in records] == [("pass", 0), ("pass", 16)]
    assert all(r["cancelled"] for r in records)
    simulation, records = run(quarter)
    assert [r["event"] for r in records] == ["click", "click", "record"] and records[-1]["record"] == 2
    three = [
        first,
        arrival(1, number=3, phase=32, direction=[-1, 0, 0]),
        arrival(1, number=4, phase=0, direction=[0, 1, 0]),
    ]
    simulation, records = run(three)
    assert [(r["event"], r["number"]) for r in records] == [
        ("pass", 2),
        ("pass", 3),
        ("click", 4),
        ("record", 0),
    ]
    assert records[-1]["record"] == 1 and records[-1]["phase"] == 0
    assert simulation.measured[1].events == [0, 1] and simulation.stores[LIGHT].size == 2
    rows = [arrival(3, number=2, phase=0), arrival(2, number=3, phase=32, direction=[-1, 0, 0])]
    simulation, records = run(rows)
    assert [(r["event"], r["number"], r.get("amount", r.get("record"))) for r in records] == [
        ("pass", 2, 2),
        ("pass", 3, 2),
        ("click", 2, 1),
        ("record", 0, 1),
    ]
    light = simulation.stores[LIGHT]
    assert sorted(light.amount.tolist()) == [2, 2] and simulation.measured[1].held == [4, 1]
    assert simulation.ledger.transit_absorbed[LIGHT] == 1
    with pytest.raises(ValueError, match="reading"):
        parse_ray_world(world(measured, [], 1, reading="field"))
