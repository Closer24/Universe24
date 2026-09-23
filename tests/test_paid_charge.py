"""A paid family's charge per unit of amount, D-1 (docs/BEAM_LAW.md, section
2 and section 10 note 36 (ii); the model owner, 2026-09-20, "go on
everything", item (2): a paid family may declare a whole charge per unit of
amount, read on the charge line of the books only, the push untouched; the
physicist's design, WEAK.md 1.5): the charge of a measured event is rho
times its content for a free family and the declared whole charge times
the amount (the units it clicked, and the units waiting to be created
again) for a paid family; the books' charge line is that sum over the
measured events plus the paid rows in transit and the paid units escaped,
conserved exactly through the flight of a charged paid row, its click, its
home, its escape and the escape of the body that holds it; the push of a
paid ray stays its label and a paid family's electric column stays 0, so
no push reads the charge. The expected integers of
docs/TEST_EXPECTATIONS.md ("A paid family's charge"), written down before
the first run. Bars of 7 x 1 x 1, K 2^20, N 64, `release` [0, 1],
`suspension` 0; the families `p` (free, no phase circle, charge [1, 5]:
+1 on a content of 5), `beta` (paid, quantum 1, charge -1 per unit of
amount) and `w` (free, no phase circle, charge 0, the absorber); a row of
`beta` of amount 1 declared at x = 1 on +x walks by the flight table's
m(tau) = (128 tau + 110) // 220: x = 2 at the ages 1, 2; 3 at 3, 4; 4 at 5,
6; 5 at 7; 6 at 8, 9; off the bar at 10.

(a) the click of a charged paid row: `p` of content 5 fixed at x = 0, the
    absorber `w` (content 1) fixed at x = 4, the beta row of number 1 at
    x = 1: the books' charge line is [0, 1] at every tick (p +1 and the
    row in transit -1, then p +1 and the absorber's unit -1); the row
    clicks at tick 5: the absorber's `held` [0, 1, 1] (the beta content 1,
    the quantum), its content 2, its `clicks` [0, 1, 0], its `units` of
    beta 1, its charge (-1, 1), its `charges()` [(2, 1), (-1, 1)] and, for
    the push, `charges(for_push=True)` [(2, 1), (0, 1)]; its momentum
    (64, 0, 0), the paid ray's label; the same world with the beta charge
    0 gives the same momentum (64, 0, 0) and the charge line [1, 1] (the
    push untouched by the charge, the line changed by it); a charged free
    reader (`p`, charge [1, 5]) reading a charged beta row takes the
    label alone, (64, 0, 0), no electric term (the paid family's column
    value is (0, 1));
(b) the escape through a face: the world of (a) without the absorber: the
    row leaves through `face:+x` at tick 10; the charge line [0, 1] at
    every tick of 12 (p +1, the escaped unit -1), the escaped amount 1;
(c) the home: the absorber `w` fixed at x = 3 releasing on +x alone and the
    row of ITS number (2) at x = 1: at tick 3 the row is home (pending),
    created again on +x in the same interval, and leaves through `face:+x`
    at tick 10; the charge line [-1, 1] at every tick of 12 (the one unit
    in transit, at home, in transit, escaped); the absorber's momentum
    (0, 0, 0) after tick 3 (the home's +64 and the re-creation's -64);
(d) a body that holds clicked units leaves the GameBoard: the world of (a)
    with the absorber free (not fixed): after the click its content is 2
    and its momentum (64, 0, 0), so it steps one Link per (64 x 2 + 64) /
    64 = 3 self-creations off its drive (the step drive of 2026-09-20,
    advanced since the crossing rule of 2026-09-21 by the momentum after
    the previous interval, the step preceding the law: the drive 64 at the
    interval after the click, 6, and 192 = D at 8): the steps at the
    ticks 8, 11 and 14 (x = 5, 6, off the bar), the click on `face:+x` at
    tick 14 with its `held` [0, 1, 1] (7, 10, 13 under the order as it
    was; the rule as it was, the count off the clock `by_clock(age - 1,
    64, 192)`, stepped at 6, 9, 12); the
    ledger's `units_escaped` [0, 1, 0]; the charge line [0, 1] at every
    tick of 15;
(e) the refusals and the record: `charge` [-1, 2] on a paid family
    refused (whole per unit of amount); a lamp on a measured event of a
    charged paid family refused (it would release charge from nothing);
    `charge` -1 on a paid family accepted: the family's `charge` (-1, 1),
    its `charge` column value (0, 1), the run's record `charge` [-1, 1]
    and the column's value [0, 1], `hypotheses` [] (a report of the books,
    no identity).
"""

from __future__ import annotations

import json

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.runner import run_initialization

P, BETA, W = 0, 1, 2
PLUS_X = [1, 0, 0]


def families(beta_charge: int | list[int] = -1) -> list[dict[str, object]]:
    return [
        {"name": "p", "quantum": 0, "phase": False, "charge": [1, 5]},
        {"name": "beta", "quantum": 1, "charge": beta_charge},
        {"name": "w", "quantum": 0, "phase": False},
    ]


def world(
    measured: list[dict[str, object]],
    number: int = 1,
    beta_charge: int | list[int] = -1,
    ticks: int = 12,
) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": "paid-charge-test",
        "shape": [7, 1, 1],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": families(beta_charge),
        "measured": measured,
        "in_transit": [
            {
                "position": [1, 0, 0],
                "family": "beta",
                "number": number,
                "direction": PLUS_X,
                "amount": 1,
                "phase": 0,
            }
        ],
    }


PROTON: dict[str, object] = {"position": [0, 0, 0], "family": "p", "amount": 5, "fixed": True}
ABSORBER: dict[str, object] = {"position": [4, 0, 0], "family": "w", "amount": 1, "fixed": True}


def run(
    document: dict[str, object], ticks: int
) -> tuple[NatureBeamSimulation, list[dict[str, object]], list[list[int]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(document), records.append, keep_row_clicks=True
    )
    lines: list[list[int]] = []
    for tick in range(1, ticks + 1):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        lines.append(list(books["charge"]))  # type: ignore[call-overload]
    return simulation, records, lines


def test_the_charge_line_through_a_click_of_a_charged_paid_row():
    """(a)."""
    simulation, records, lines = run(world([PROTON, ABSORBER]), 6)
    assert lines == [[0, 1]] * 6
    absorber = simulation.measured[2]
    clicks = [r for r in records if r["event"] == "click"]
    assert [(r["tick"], r["measured"], r["family"]) for r in clicks] == [(5, 2, "beta")]
    assert absorber.held == [0, 1, 1] and absorber.content == 2 and absorber.clicks == [0, 1, 0]
    assert absorber.units(BETA) == 1 and absorber.charge == (-1, 1)
    assert absorber.charges() == [(2, 1), (-1, 1)] and absorber.charges(for_push=True) == [
        (2, 1),
        (0, 1),
    ]
    assert absorber.momentum == [64, 0, 0] and absorber.state()["charge"] == [-1, 1]
    # The push untouched by the charge: the same integers with the charge 0.
    neutral, _, neutral_lines = run(world([PROTON, ABSORBER], beta_charge=0), 6)
    assert neutral.measured[2].momentum == [64, 0, 0] and neutral_lines == [[1, 1]] * 6
    assert neutral.measured[2].charge == (0, 1)
    # A charged free reader reads a charged paid row: the label alone.
    reader: dict[str, object] = {
        "position": [4, 0, 0],
        "family": "p",
        "amount": 5,
        "fixed": True,
        "table": {"beta": "read"},
    }
    read, read_records, _ = run(world([PROTON, reader]), 6)
    reads = [r for r in read_records if r["event"] == "read"]
    assert [(r["tick"], r["push"]) for r in reads] == [(5, [64, 0, 0])]
    assert read.measured[2].momentum == [64, 0, 0] and read.measured[2].charge == (1, 1)


def test_the_charge_line_through_an_escape_and_a_home():
    """(b), (c)."""
    simulation, records, lines = run(world([PROTON]), 12)
    assert lines == [[0, 1]] * 12
    escapes = [(r["tick"], r["detector"]) for r in records if r["event"] == "click"]
    assert escapes == [(10, "face:+x")] and simulation.ledger.escaped_amount(BETA) == 1
    assert simulation.ledger.units_escaped == [0, 0, 0]
    mirror: dict[str, object] = {
        "position": [3, 0, 0],
        "family": "w",
        "amount": 1,
        "fixed": True,
        "directions": [PLUS_X],
    }
    simulation, records, lines = run(world([mirror], number=1), 12)
    assert lines == [[-1, 1]] * 12
    kinds = [(r["event"], r["tick"], r.get("detector")) for r in records]
    assert kinds == [("home", 3, None), ("click", 10, "face:+x")]
    assert simulation.measured[1].momentum == [0, 0, 0] and simulation.measured[1].units(BETA) == 0
    assert (
        simulation.ledger.transit_released == [0, 1, 0] and simulation.ledger.escaped_amount(BETA) == 1
    )


def test_a_body_that_holds_clicked_units_leaves_the_game_board():
    """(d)."""
    body = {**ABSORBER, "fixed": False}
    simulation, records, lines = run(world([PROTON, body], ticks=15), 15)
    assert lines == [[0, 1]] * 15
    steps = [(r["tick"], r["to"]) for r in records if r["event"] == "step"]
    assert steps == [(8, [5, 0, 0]), (11, [6, 0, 0])]
    escapes = [r for r in records if r["event"] == "click" and r["detector"] == "face:+x"]
    assert [(r["tick"], r["measured"], r["held"]) for r in escapes] == [(14, 2, [0, 1, 1])]
    assert 2 not in simulation.measured and simulation.ledger.units_escaped == [0, 1, 0]
    assert simulation.ledger.held_escaped == [0, 1, 1]


def refused(document: dict[str, object], text: str) -> None:
    with pytest.raises(ValueError, match=text):
        parse_nature_beam_world(document)


def test_the_refusals_and_the_record(tmp_path):
    """(e)."""
    refused(
        world([PROTON, ABSORBER], beta_charge=[-1, 2]),
        r"families\[1\]\.charge: a paid family's charge is per unit of amount and whole",
    )
    lamp: dict[str, object] = {
        "position": [4, 0, 0],
        "family": "beta",
        "amount": 4,
        "fixed": True,
        "lamp": {"wheel": [1, 64], "rate": [1, 1], "directions": [PLUS_X]},
    }
    refused(world([PROTON, lamp]), r"measured\[1\]: a lamp of the charged paid family 'beta'")
    parsed = parse_nature_beam_world(world([PROTON, ABSORBER]))
    assert parsed.families[BETA].charge == (-1, 1) and parsed.families[BETA].columns[1].value == (0, 1)
    assert parsed.families[BETA].values == ((1, 1), (0, 1)) and parsed.hypotheses == []
    path = tmp_path / "world.json"
    path.write_text(json.dumps(world([PROTON, ABSORBER], ticks=6)), encoding="utf-8")
    record = json.loads(
        run_initialization(path, tmp_path / "run", keep_row_clicks=True).read_text(encoding="utf-8")
    )
    assert record["status"] == "completed" and record["hypotheses"] == []
    assert record["families"][BETA]["charge"] == [-1, 1]
    assert record["families"][BETA]["columns"][1] == {"name": "charge", "value": [0, 1], "sign": 1}
    assert [entry["charge"] for entry in record["audit"]] == [[0, 1]] * 6
    assert record["measured"][1]["charge"] == [-1, 1] and record["measured"][1]["charges"]["charge"] == [
        -1,
        1,
    ]
