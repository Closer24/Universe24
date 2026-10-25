"""The nineteen gates of tools/record_gates.py (the owner's phenomena, 2026-10-25; the two blind hands' table agreed cold on PR #2187) on the committed record of examples/events/universe24, every verdict asserted by name so that a record losing a SHOWN gate or gaining a NOT SHOWN one fails by that name (a gain is a finding, and the list is rewritten on purpose), with the existence counts the gates read; and three predicates on a record of a few lines written by hand."""

from tests.laws import ROOT, load_file
from tests.laws_universe import FOLDER

GATES = load_file("record_gates", ROOT / "tools" / "record_gates.py")
SHOWN = {
    "links_lengthening",
    "links_cycle",
    "era_of_matter",
    "acceleration",
    "contraction",
    "light.present_absorbed",
    "families_forming",
    "gravitational_time_dilation",
    "horizon.links_and_silence",
    "conservation.identity",
    "charge_conservation",
    "arrow_of_time",
    "mass_ratios.fit",
}
NOT_SHOWN = {
    "recurring_bangs",
    "light.redshift",
    "collisions",
    "gravitational_redshift",
    "light_path",
    "free_fall",
    "horizon.stopped_clock",
    "conservation.exact",
    "uncertainty",
    "mass_ratios.from_clicks",
}
BOARD = {"recurring_bangs", "links_cycle", "acceleration", "contraction", "horizon"}


def test_the_committed_record_shows_the_agreed_gates_by_name():
    """The record of c60804dc7: the thirteen verdicts SHOWN and the ten NOT SHOWN by name, the board's view at the five gates whose quantity is the whole board, the lack named exactly where a verdict is NOT SHOWN, the summary's last line the count, and the counts that are existence claims: returns above one, black holes above zero, the bodies' credits above light's, births in the first cycle alone."""
    results = GATES.gates(GATES.read_record(FOLDER))
    verdicts = GATES.verdicts(results)
    assert {k for k, v in verdicts.items() if v == "SHOWN"} == SHOWN
    assert {k for k, v in verdicts.items() if v == "NOT SHOWN"} == NOT_SHOWN
    assert [r["gate"] for r in results] == [name for name, _f in GATES.GATES]
    assert {r["gate"] for r in results if r["view"] == "board"} == BOARD
    for r in results:
        shown = all(v == "SHOWN" for v in GATES.verdicts([r]).values())
        assert (r["missing"] is None) == shown, r["gate"]
        assert set(r) == {"gate", "verdict", "view", "reads", "numbers", "missing"}
    numbers = {r["gate"]: r["numbers"] for r in results}
    assert len(numbers["recurring_bangs"]["returns"]) > 1
    assert numbers["recurring_bangs"]["births_per_cycle"][0] > 0
    assert set(numbers["recurring_bangs"]["births_per_cycle"][1:]) == {0}
    assert len(numbers["horizon"]["holes"]) > 0 and len(numbers["horizon"]["silent_wall_runs"]) > 0
    assert numbers["era_of_matter"]["body_credits"] > numbers["era_of_matter"]["light_credits"] > 0
    assert (
        numbers["gravitational_time_dilation"]["birthed_slower"]
        > numbers["gravitational_time_dilation"]["other_slower"]
    )
    assert numbers["conservation"]["identity_holds"] == numbers["conservation"]["lines"] > 0
    assert numbers["conservation"]["excess_zero"] == 0
    assert (
        GATES.summary(results).splitlines()[-1] == f"{len(SHOWN)} of {len(SHOWN) + len(NOT_SHOWN)} shown"
    )


def hand_record(births_at):  # type: ignore[no-untyped-def]
    """A record of a few lines by hand on the 3-cube: the volume rising to a top at 4 with one fire, falling to its return at 7 and rising again; a birth at each interval of `births_at` at the Node A, light's credit and a body's credit there and the same body's credit at the Node B at 3 and 9, A's clock advancing 3 proper intervals between the two closes and B's 4; every take exact; one Node turned at 5."""
    volumes = [100, 110, 120, 130, 120, 110, 100, 110, 120, 130, 140, 150]
    header = {"shape": [3, 3, 3], "held": ["volume"], "seed": "light", "primes": [[5, 1], [13, 1]]}
    header.update(families=["volume", "sign", "light", "point 2 0", "point 0 2"])
    header.update(points={"point 2 0": [3, 5], "point 0 2": [5, 13]})
    eras, nodes = [], []
    for t, volume in enumerate(volumes, start=1):
        row = {"volume": volume, "velocity": volume - volumes[max(t - 2, 0)], "writes": {"light": 1}}
        quanta = {"light": {"quanta": 27}, "sign": {"quanta": 0}}
        eras.append(
            {
                "interval": t,
                "fires": int(t == 4),
                "horizon": 0,
                "rows": {"volume": row},
                "quanta": quanta,
            }
        )
        turned = [0] if t == 5 else []
        nodes.append(
            {"interval": t, "length": [1.0] * 27, "turned": turned, "direction": [1] * 27, "horizon": []}
        )
    take = {"taken": 10, "walls": 10, "excess": 0, "step": 10}
    births, credits, lays = [], [], []
    for n, t in enumerate(births_at):
        birth = {
            "event": "birth",
            "interval": t,
            "family": "light",
            "children": ["point 2 0", "point 2 0"],
        }
        births.append(
            {
                **birth,
                "senses": [-1, 1],
                "nodes": [[0, 0, 1]],
                "records": [n, n + 1],
                "points": [[3, 5]] * 2,
                **take,
            }
        )
        lays.append(
            {
                "event": "lay",
                "interval": t,
                "family": "light",
                "node": {"at": [0, 0, 1]},
                "before": [2, 1, 0],
                "after": [1, 1, 0],
            }
        )
    for t, where, proper, identity, kind in (
        (3, (0, 0, 1), 2, [2, 0], 1),
        (3, (0, 0, 1), 2, [3, 0], 2),
        (9, (0, 0, 1), 5, [3, 0], 2),
    ):
        credit = {
            "event": "credit",
            "interval": t,
            "family": "light",
            "node_detector": where[2],
            "window": [t, t],
            "proper": proper,
        }
        credit.update(
            count=1,
            absorbed="light",
            emitted="point 2 0",
            point=[3, 5],
            kind=kind,
            sense=kind - 1,
            beat=None,
        )
        credits.append({**credit, "support": list(where), "identity": identity, **take})
    for t, proper in ((3, 2), (9, 6)):
        credit = {
            **credits[-1],
            "interval": t,
            "window": [t, t],
            "proper": proper,
            "node_detector": 13,
            "support": [1, 1, 1],
        }
        credits.append(credit)
    return GATES.record_of(header, eras, nodes, GATES.READER.Lines(credits, births, lays, []))


def test_three_predicates_on_a_record_by_hand():
    """By hand: two returns (1 and 7) with a birth after the second make the recurring bangs SHOWN, and the same record with both births before the return NOT SHOWN with the lack named; the birthed Node A counting 3 proper intervals against B's 4 between the shared closes 3 and 9 makes the dilation SHOWN with the births as matter; every line's taken equal to its walls makes the conservation SHOWN as the identity and as exact."""
    record = hand_record([3, 9])
    bangs = GATES.gate_recurring_bangs(record)
    assert bangs["verdict"] == "SHOWN" and bangs["numbers"] == {
        "returns": [1, 7],
        "tops": [4],
        "births_per_cycle": [1, 1],
    }
    assert bangs["view"] == "board" and bangs["missing"] is None
    stopped = GATES.gate_recurring_bangs(hand_record([3, 5]))
    assert stopped["verdict"] == "NOT SHOWN" and stopped["numbers"]["births_per_cycle"] == [2, 0]
    assert stopped["missing"] == "a birth after a return (the lay lock)"
    dilation = GATES.gate_gravitational_time_dilation(record)
    assert dilation["verdict"] == "SHOWN" and dilation["view"] == "clicks"
    assert dilation["numbers"] == {
        "node_pairs_unequal_proper": 1,
        "pairs_one_birthed": 1,
        "birthed_slower": 1,
        "other_slower": 0,
    }
    conservation = GATES.gate_conservation(record)
    assert (
        conservation["verdict"] == {"identity": "SHOWN", "exact": "SHOWN"}
        and conservation["missing"] is None
    )
    assert conservation["numbers"]["lines"] == conservation["numbers"]["identity_holds"] == 7
    assert GATES.verdicts([bangs, conservation]) == {
        "recurring_bangs": "SHOWN",
        "conservation.identity": "SHOWN",
        "conservation.exact": "SHOWN",
    }
    assert all(
        r["verdict"] in ("SHOWN", "NOT SHOWN") or isinstance(r["verdict"], dict)
        for r in GATES.gates(record)
    )
