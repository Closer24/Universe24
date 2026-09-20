"""The world file of the Beam Law refuses by name (docs/BEAM_LAW.md,
sections 2 and 7) and the runner records a run; the integer bounds of the
measured line (re-pinned from `test_event_worlds` (e) and
`test_integer_bounds_of_measured_and_emission` (a) under the Beam Law). The
expected results of docs/TEST_EXPECTATIONS.md ("The world file of the Beam
Law"), written down first:

(a) refused, naming the key: `"law": "events"` (naming the Beam Law
    and MIGRATION), `"law": "rays"` (the law's name before 2026-09-20,
    naming the migration; a world without `law` names `"beam"`), `dynamics`, `max_active_owners`, `headings` on a lamp,
    `heading` on a ray, `port_map`, `groups` on a detector, a non-primitive
    direction (2, 2, 0), a component beyond P (65 at the default bound), a
    direction the world does not declare, a rest direction on a lamp, a
    repeated direction, a momentum label beyond 2^62 - 1 on a declared ray
    and on a lamp's release, `phase_per_link` outside 0 .. N - 1 or on a
    family without a phase circle, the earlier engines' keys, `phase_turn`,
    a closed GameBoard, an unknown key, a content at K x N / 2, a lamp on a free
    family, two measured events at one Node, an unknown table rule, N not a
    power of two, a detector on a Node without a measured event, a Node in
    two detectors, `kind` on a family (naming MIGRATION: the quantum decides
    the kind), a family without `quantum`, a negative quantum, a charge on a
    paid family (a fraction, since 2026-09-20, D-1: whole per unit of amount), `charge` on a measured event (naming MIGRATION: since
    2026-09-20 the charge is the family's per unit of content), a family
    charge with a denominator of 0 or a part that is not an integer, a
    detector named `face:+x` (a face detector's name), a `suspension`
    denominator of 0, a window for a family without a phase circle;
(b) accepted: the direction table of a world with `directions` [[1, 1, 0]]
    is the two rest vectors, the six headings and (1, 1, 0); a measured
    event's `directions` by vector or by index; a ray at rest (index 0);
    `suspension` 1 as (1, 1), [1, 4], [0, 4] as (0, 1); `reads` per entry;
    a family `charge` -3 as (-3, 1) and [1, 2] as (1, 2), the measured
    event's `charge` then [-3 x 2^24, 1] and [2^23, 1] (rho x content,
    reduced), the books' `charge` the same pair;
(c) the runner: a 4-interval world into `run.json` (`law` "beam-v1",
    completed, four ticks, four books, conserved, the measured events, the
    six face detectors of the open GameBoard with their `record`, the
    directions table, `suspension` [1, 1]), `state.json` (the law, tick 4,
    the Nodes with rays) and `events.jsonl`; a negative tick count and a
    used output directory refused;
(d) the bounds (re-pinned on 2026-09-19 at 1/64 of their amounts, the
    label of a unit along a heading being 64 e_d since the label along the
    unit vector, BEAM_LAW section 2 and note 23): two measured events of
    content 1 one Link apart at `release` [1, 1] read each other's one ray
    from interval 2 on and are pushed by 1 x 64 x 1 = 64 toward each
    other; the second, declared with the momentum -(2^62 - 1) + 64 on x,
    reaches the bound exactly and is accepted; one unit nearer it is
    refused with `OverflowError` naming the measured event, its Node and
    the momentum; a reader of content 2^56 - 1 met by one ray takes the
    push -(2^56 - 1) x 64 = -(2^62 - 64), and at 2^56 the push -2^62 is
    refused naming the push.
"""

from __future__ import annotations

import json

import pytest

from event_universe.events import BEAM_LAW, NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.world import MOMENTUM_BOUND
from event_universe.runner import run_initialization

CONTENT = 1 << 24


def base(**keys: object) -> dict[str, object]:
    world: dict[str, object] = {
        "law": "beam",
        "model_id": "ray-parsing-test",
        "shape": [11, 11, 11],
        "boundary": "open",
        "ticks": 4,
        "K": 1 << 22,
        "N": 64,
        "release": [1, 128],
        "suspension": 1,
        "families": [{"name": "m", "quantum": 0, "charge": 0, "phase": False}],
        "measured": [{"position": [5, 5, 5], "family": "m", "amount": CONTENT, "fixed": True}],
    }
    world.update(keys)
    return world


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_nature_beam_world(document)


def test_the_world_refuses_by_name():
    """(a)."""
    world = base()
    light = {"name": "light", "quantum": 1}
    lamp = {"position": [1, 1, 1], "family": "light", "amount": 4, "fixed": True}
    refused({**world, "law": "events"}, '"law": "events" names the law of events.*MIGRATION')
    # The law's name before 2026-09-20 is refused naming the migration (rays-v1
    # is beam-v1, the same law); the edge: no law at all names the one value.
    refused(
        {**world, "law": "rays"}, '"law": "rays" is the Beam Law.s name before 2026-09-20.*MIGRATION'
    )
    refused({key: value for key, value in world.items() if key != "law"}, '"law": "beam"')
    refused({**world, "dynamics": "reversible-detector-v1"}, "law of events' keys \\(dynamics\\)")
    refused({**world, "max_active_owners": 1}, "max_active_owners")
    refused(
        {
            **world,
            "families": [light],
            "measured": [{**lamp, "lamp": {"rate": 1, "headings": [[1, 0, 0]]}}],
        },
        "declares headings",
    )
    refused(
        {
            **world,
            "in_transit": [
                {"position": [1, 1, 1], "family": "m", "number": 1, "heading": [1, 0, 0], "amount": 1}
            ],
        },
        "declares heading",
    )
    refused(
        {**world, "measured": [{**world["measured"][0], "port_map": [0, 1, 2, 3, 4, 5]}]},
        "declares port_map",
    )  # type: ignore[index]
    refused(
        {**world, "detectors": [{"name": "d", "positions": [[5, 5, 5]], "groups": []}]},
        "declares groups",
    )
    refused({**world, "directions": [[2, 2, 0]]}, "primitive vector")
    refused({**world, "directions": [[65, 1, 0]]}, "from -64 through 64")
    refused(
        {**world, "measured": [{**world["measured"][0], "directions": [[1, 1, 0]]}]}, "does not declare"
    )  # type: ignore[index]
    refused(
        {**world, "families": [light], "measured": [{**lamp, "lamp": {"rate": 1, "directions": [0]}}]},
        "must not be a rest direction",
    )
    refused(
        {**world, "measured": [{**world["measured"][0], "directions": [[1, 0, 0], [1, 0, 0]]}]},
        "repeats a direction",
    )  # type: ignore[index]
    refused(
        {
            **world,
            "families": [{**light, "quantum": (1 << 30) - 1}],
            "measured": [lamp],
            "in_transit": [
                {
                    "position": [1, 1, 1],
                    "family": "light",
                    "number": 1,
                    "direction": [1, 0, 0],
                    "amount": 1 << 33,
                }
            ],
        },
        "exceeds the integer bound",
    )
    refused(
        {
            **world,
            "K": 1,
            "N": 4096,
            "families": [{**light, "quantum": (1 << 30) - 1}],
            "measured": [{**lamp, "amount": 2000, "lamp": {"rate": [1 << 33, 1]}}],
        },
        "exceeds the integer bound",
    )
    refused(
        {**world, "families": [{**light, "phase_per_link": 64}]},
        "phase_per_link must be an integer from 0 through 63",
    )
    refused(
        {**world, "families": [{"name": "m", "quantum": 0, "phase": False, "phase_per_link": 3}]},
        "refused for a family without a phase circle",
    )
    refused({**world, "contents": []}, "earlier engines' keys")
    for key in ("initial_shadows", "wait_per_quantum", "schema_version", "dense_field"):
        refused({**world, key: 1}, key)
    refused(
        {**world, "families": [{"name": "m", "quantum": 0, "phase_turn": "none"}]},
        "unknown keys: phase_turn",
    )
    refused({**world, "boundary": "periodic"}, "closed GameBoard is refused")
    refused({**world, "prefill": 3}, "unknown keys: prefill")
    phased = {**world, "families": [{"name": "m", "quantum": 0, "charge": 0}]}
    refused(
        {**phased, "measured": [{"position": [1, 1, 1], "family": "m", "amount": 1 << 28}]},
        "below K x N",
    )
    parse_nature_beam_world(
        {**world, "measured": [{"position": [1, 1, 1], "family": "m", "amount": 1 << 28}]}
    )
    refused(
        {
            **world,
            "measured": [{"position": [1, 1, 1], "family": "m", "amount": 4, "lamp": {"rate": 1}}],
        },
        "a lamp is a measured event of a paid family",
    )
    refused(
        {**world, "measured": [{"position": [1, 1, 1], "family": "m", "amount": 4}] * 2},
        "two measured events at one Node",
    )
    refused(
        {
            **world,
            "measured": [{"position": [1, 1, 1], "family": "m", "amount": 4, "table": {"m": "keep"}}],
        },
        "must be one of",
    )
    refused({**world, "N": 48}, "power of two")
    refused(
        {**world, "detectors": [{"name": "d", "positions": [[0, 0, 0]]}]}, "without a measured event"
    )
    refused(
        {
            **world,
            "detectors": [
                {"name": "d", "positions": [[5, 5, 5]]},
                {"name": "e", "positions": [[5, 5, 5]]},
            ],
        },
        "a Node in two detectors",
    )
    refused(
        {**world, "families": [{"name": "m", "kind": "free", "quantum": 0}]},
        "declares kind, a key removed on 2026-09-19.*MIGRATION",
    )
    refused({**world, "families": [{"name": "m"}]}, "lacks keys: quantum")
    refused({**world, "families": [{"name": "m", "quantum": -1}]}, "quantum must be an integer from 0")
    refused(
        {**world, "families": [{"name": "light", "quantum": 3, "charge": [1, 3]}]},
        "a paid family's charge is per unit of amount and whole",
    )
    refused(
        {**world, "measured": [{**world["measured"][0], "charge": 2}]},
        "measured\\[0\\] declares charge, a key removed on 2026-09-20.*docs/MIGRATION.md",
    )
    for value, text in (
        ([1, 0], "families\\[0\\].charge denominator must be an integer from 1"),
        ([1.5, 2], "families\\[0\\].charge numerator must be an integer"),
        ("1/2", "families\\[0\\].charge must be an integer or \\[numerator, denominator\\]"),
        ([1, 2, 3], "families\\[0\\].charge must be an integer or \\[numerator, denominator\\]"),
    ):
        refused({**world, "families": [{"name": "m", "quantum": 0, "charge": value}]}, text)
    refused(
        {**world, "detectors": [{"name": "face:+x", "positions": [[5, 5, 5]]}]},
        "detectors\\[0\\].name 'face:\\+x' is the name of a face detector",
    )
    refused({**world, "suspension": [1, 0]}, "suspension denominator")
    refused(
        {
            **world,
            "measured": [
                {
                    "position": [1, 1, 1],
                    "family": "m",
                    "amount": 4,
                    "table": {"m": {"rule": "read", "phase_window": 3}},
                }
            ],
        },
        "refused for a family without a phase circle",
    )


def test_the_world_accepts_the_direction_table_and_the_keys():
    """(b)."""
    world = base(directions=[[1, 1, 0]])
    parsed = parse_nature_beam_world(world)
    assert parsed.directions == (
        (0, 0, 0),
        (0, 0, 0),
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
        (1, 1, 0),
    )
    by_vector = parse_nature_beam_world(
        {**world, "measured": [{**world["measured"][0], "directions": [[1, 1, 0], [0, 0, 1]]}]}
    )  # type: ignore[index]
    by_index = parse_nature_beam_world(
        {**world, "measured": [{**world["measured"][0], "directions": [8, 6]}]}
    )  # type: ignore[index]
    assert by_vector.measured[0].directions == by_index.measured[0].directions == (8, 6)
    rest = parse_nature_beam_world(
        {
            **world,
            "in_transit": [
                {"position": [1, 1, 1], "family": "m", "number": 1, "direction": 0, "amount": 2}
            ],
        }
    )
    assert rest.in_transit[0].direction == 0 and rest.in_transit[0].age == 0
    assert parsed.suspension == (1, 1) and parsed.release == (1, 128) and parsed.owners(0) == (1,)
    assert parse_nature_beam_world({**world, "suspension": [1, 4]}).suspension == (1, 4)
    assert parse_nature_beam_world({**world, "suspension": [0, 4]}).suspension == (0, 1)
    reads = parse_nature_beam_world(
        {
            **world,
            "measured": [{**world["measured"][0], "table": {"m": {"rule": "read", "reads": "tensor"}}}],
        }
    )  # type: ignore[index]
    assert reads.measured[0].reads == ("tensor",) and parsed.measured[0].reads == ("vector",)
    detector = parse_nature_beam_world(
        {**world, "detectors": [{"name": "d", "positions": [[5, 5, 5]], "threshold": 3}]}
    )
    assert detector.detector_of((5, 5, 5)) == 0 and detector.detectors[0].threshold == 3


def test_the_runner_records_a_run(tmp_path):
    """(c)."""
    world = base()
    path = tmp_path / "world.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    record = json.loads(run_initialization(path, tmp_path / "run").read_text(encoding="utf-8"))
    assert record["law"] == BEAM_LAW and record["status"] == "completed"
    assert record["completed_ticks"] == 4 and record["conserved_at_every_completed_tick"] is True
    assert len(record["audit"]) == 4 and record["measured"][0]["content"] == CONTENT
    assert [entry["name"] for entry in record["detectors"]] == [
        "face:+x",
        "face:-x",
        "face:+y",
        "face:-y",
        "face:+z",
        "face:-z",
    ]
    assert all("record" in entry["families"]["m"] for entry in record["detectors"])
    assert record["suspension"] == [1, 1] and record["directions"][2] == [1, 0, 0]
    assert record["families"][0]["phase"] is False and record["families"][0]["phase_per_link"] == 0
    state = json.loads((tmp_path / "run" / "state.json").read_text(encoding="utf-8"))
    assert state["law"] == BEAM_LAW and state["tick"] == 4 and state["nodes"] and "measured" in state
    assert (tmp_path / "run" / "events.jsonl").exists()
    with pytest.raises(ValueError, match="ticks must be nonnegative"):
        run_initialization(path, tmp_path / "negative", ticks=-1)
    with pytest.raises(ValueError, match="empty output directory"):
        run_initialization(path, tmp_path / "run")
    assert (tmp_path / "run" / "initialization.json").read_bytes() == path.read_bytes()


def pair(momentum: int) -> dict[str, object]:
    return base(
        shape=[2, 1, 1],
        K=1024,
        release=[1, 1],
        suspension=0,
        families=[{"name": "m", "quantum": 0}],
        measured=[
            {"position": [0, 0, 0], "family": "m", "amount": 1, "fixed": True},
            {
                "position": [1, 0, 0],
                "family": "m",
                "amount": 1,
                "fixed": True,
                "momentum": [momentum, 0, 0],
            },
        ],
    )


def test_the_measured_line_is_bounded_before_assignment():
    """(d)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(pair(-MOMENTUM_BOUND + 64)))
    simulation.step()
    simulation.step()
    assert simulation.books()["balanced"]
    assert simulation.measured[2].momentum == [-MOMENTUM_BOUND, 0, 0]
    assert simulation.measured[2].pushed == [-64, 0, 0] and simulation.measured[1].pushed == [64, 0, 0]
    simulation = NatureBeamSimulation(parse_nature_beam_world(pair(-MOMENTUM_BOUND + 63)))
    simulation.step()
    with pytest.raises(OverflowError, match=r"the momentum of measured event 2 at \[1, 0, 0\]"):
        simulation.step()
    for content, push in (((1 << 56) - 1, -((1 << 62) - 64)), (1 << 56, None)):
        world = base(
            shape=[3, 1, 1],
            K=1 << 60,
            release=[0, 1],
            suspension=0,
            families=[{"name": "m", "quantum": 0, "phase": False}],
            measured=[
                {"position": [2, 0, 0], "family": "m", "amount": 4, "fixed": True},
                {"position": [1, 0, 0], "family": "m", "amount": content, "fixed": True},
            ],
            in_transit=[
                {"position": [0, 0, 0], "family": "m", "number": 1, "direction": [1, 0, 0], "amount": 1}
            ],
        )
        simulation = NatureBeamSimulation(parse_nature_beam_world(world))
        if push is None:
            with pytest.raises(OverflowError, match=r"the push of measured event 2 at \[1, 0, 0\]"):
                simulation.step()
        else:
            simulation.step()
            assert simulation.measured[2].momentum == [push, 0, 0]


def test_the_phase_circle_reaches_65536_steps():
    """(a) and (b), the bound of N raised on 2026-09-20 by the model owner
    ("raise the bound"): a world declares N up to 65536, the tables' one
    bound `core.phase.MAX_PHASE_STEPS`; above it the world is refused naming
    N, and a non-power of two stays refused. The tables at 65536 steps have
    65536 entries, the quarter turn exact (S[p + N/4] = C[p], read as
    C[p - N/4]), the eighth turn 181 as at every N, and every entry within
    256; the edge: 131072 is refused by the tables and by the world."""
    from event_universe.core.phase import MAX_PHASE_STEPS, phase_cosines, phase_sines

    assert MAX_PHASE_STEPS == 65536
    steps = 65536
    cosines, sines = phase_cosines(steps), phase_sines(steps)
    assert len(cosines) == steps and len(sines) == steps
    assert cosines[0] == 256 and cosines[steps // 2] == -256 and cosines[steps // 4] == 0
    assert cosines[steps // 8] == 181 and sines[steps // 8] == 181
    assert all(sines[(p + steps // 4) % steps] == cosines[p] for p in range(0, steps, 977))
    assert max(max(map(abs, cosines)), max(map(abs, sines))) == 256
    with pytest.raises(ValueError, match="between 2 and 65536"):
        phase_cosines(2 * steps)
    world = base(N=steps, families=[{"name": "m", "quantum": 0, "charge": 0}])
    assert parse_nature_beam_world(world).phase_steps == steps
    refused({**world, "N": 2 * steps}, "N")
    refused({**world, "N": 3 * 4096}, "power of two")
