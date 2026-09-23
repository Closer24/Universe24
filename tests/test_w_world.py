"""The W world: the exchange form of the weak force at one Link (docs/BEAM_LAW.md,
section 10 note 36 (iv); the model owner, 2026-09-20, "go on everything",
item (3): the W world after the transformation; the physicist's design,
WEAK.md 1.1 and 4.5). The W is a paid family with a whole charge per unit
of amount (D-1) and the family key `lifetime` 1, no column: a row born at
a self-creation makes its one step at the age 1 (m(1) = 1 on every
direction), is read by the table of the measured event it arrives at, and
is booked on the border `lifetime` at the end of that interval where no
table took it; it exists on the neighbours of its emitter and nowhere
else. Nothing is added to the law: the W world composes `become` (note 36
(iii)), D-1 (note 36 (ii)) and the lifetime (note 31 (vii)); L = 0 is no family
at all (the parser refuses a lifetime of 0), the contact form being the
`become` entry itself with its products released by the measured event
(Fermi's form, series J1 and J3); no Z family (a neutral current is the
neutrino's own row met by a `rerelease` within a window). The expected
integers of docs/TEST_EXPECTATIONS.md ("The W world"), written down
before the first run.

The bar 7 x 1 x 1, `"law": "beam"`, K 2^20, N 64, `release` [1, 2^20]
(no free release of a content of 1839 before the age 570), `suspension` 0;
the register's scale of series I: `n` (free, no phase circle, content
1839, charge 0), `p` (free, no phase circle, charge 4 per unit of content:
7344 on 1836), `w` (paid, quantum 1, a phase circle, charge -7344 per unit
of amount, `lifetime` 1), `beta` (paid, quantum 1, charge -7344) and
`positron` (paid, quantum 1, charge +7344); the neutron `n` of content
1839 fixed at x = 2 with `become` at 3 into `p` with the one product
`[["w", 1, 3]]` (the charges: 4 x 1836 = 7344 on the proton left against
-7344 on the W unit: 0, the neutron's) and `directions` `[[1, 0, 0]]`,
the proton `p` of content 1836 fixed at x = 3, one Link on +x; the
label of the W row 64 x 1 x 3 = 192 along its direction.

(a) the exchange: at tick 3 the neutron becomes `p` (`held` [0, 1836, 0,
    0, 0], the charge (7344, 1)) and throws the W on +x (the `become`
    record with the products [["w", 1, 3, [1, 0, 0]]], the recoil
    [-192, 0, 0], its momentum (-192, 0, 0)); at tick 4 the W row (age 1)
    is at x = 3 and the proton measures it by the keys' rule for a paid
    arrival (a `click` record naming the measured event 2, the family
    `w`, amount 1, content 3, the push (192, 0, 0)): the proton's `held`
    [0, 1836, 3, 0, 0], its content 1839, its clicks [0, 0, 1, 0, 0], its
    charge (0, 1) (7344 on its 1836 less 7344 on the W unit held: a
    neutron's content and a neutron's charge in the detector's terms), its
    momentum (192, 0, 0); the store empty after tick 4 and no click on the
    border `lifetime`; the books' charge line [7344, 1] at every tick of 8
    (7344 on the proton; then 7344 on each proton and -7344 on the W in
    transit; then 7344 and 0), the `w` lines released 1 (the transit
    line's units), measured 3 (the content line), current 0, the lifetime
    line 0; the run's `hypotheses` ["columns-v1",
    "weak-v1"] (the lifetime's identity and the transformation's);
(b) the W into empty space: the neutron's `directions` `[[-1, 0, 0]]`
    (x = 1 holds nothing): at tick 4 the W row at x = 1 (age 1) is booked
    on the border `lifetime` (a `click` record naming the detector
    `lifetime`, amount 1, content 3, momentum [-192, 0, 0]); the proton
    untouched (`held` [0, 1836, 0, 0, 0], momentum (0, 0, 0)); the
    escaped amount of `w` 1; the charge line [7344, 1] at every tick
    (the escaped unit's -7344 against the two protons' 14688);
(c) the click trigger on the proton: the design's sketch, the entry `w:
    {rule become, phase_window 0, phase_width 64, into n, products
    [["beta", 1, 3]]}`, is refused at load (the charges do not balance:
    -7344 on the beta unit against 7344 on the proton's 1836, the W unit
    held keeping its own -7344); the balanced form, the product
    `[["positron", 1, 3]]`, is accepted: at tick 4 the W clicks (the push
    (192, 0, 0)) and the proton becomes `n`, the positron born in step 5
    of tick 4 on -y (the clock age 3, the heading 3 in Port order), label
    (0, -192, 0), the recoil (0, 192, 0), the momentum (192, 192, 0); the
    `become` record at tick 4 with the trigger "click", triggered 4, from
    `p`, into `n`, the products [["positron", 1, 3, [0, -1, 0]]], the
    recoil [0, 192, 0], counted 1 (the W row's amount); the event's
    `held` [1833, 0, 3, 0, 0], content 1836, charge (-7344, 1); the
    positron through `face:-y` at tick 5 (the bar one Node thick); the
    charge line [7344, 1] at every tick (7344 on the first proton, -7344
    on the neutron holding the W unit, +7344 on the positron in transit
    and then escaped); the `became` lines `p` 0 (+1836 at tick 3, -1836 at
    tick 4) and `n` -6 (-1839 then +1833), the `w` line measured 3, the
    `positron` line released 1; the entry consumed;
(d) the refusals, naming the key: `lifetime` 0 on `w` (L = 0 is no
    family at all); the W's charge as a fraction ([-7344, 2]).
"""

from __future__ import annotations

import json

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.world import COLUMNS_RULE, WEAK_RULE
from event_universe.runner import run_initialization

N_, P_, W_, BETA_, POSITRON_ = 0, 1, 2, 3, 4
PROTON, NEUTRON, CHARGE = 1836, 1839, 4
W_CHARGE = -CHARGE * PROTON
W_CONTENT = 3
LABEL = 64 * W_CONTENT


def families(w_lifetime: object = 1, w_charge: object = W_CHARGE) -> list[dict[str, object]]:
    return [
        {"name": "n", "quantum": 0, "phase": False},
        {"name": "p", "quantum": 0, "phase": False, "charge": CHARGE},
        {"name": "w", "quantum": 1, "charge": w_charge, "lifetime": w_lifetime},
        {"name": "beta", "quantum": 1, "charge": W_CHARGE},
        {"name": "positron", "quantum": 1, "charge": -W_CHARGE},
    ]


def neutron(direction: list[int]) -> dict[str, object]:
    return {
        "position": [2, 0, 0],
        "family": "n",
        "amount": NEUTRON,
        "fixed": True,
        "directions": [direction],
        "become": {"at": 3, "into": "p", "products": [["w", 1, W_CONTENT]]},
    }


def proton(table: dict[str, object] | None = None) -> dict[str, object]:
    found: dict[str, object] = {"position": [3, 0, 0], "family": "p", "amount": PROTON, "fixed": True}
    if table is not None:
        found["table"] = table
    return found


def world(measured: list[dict[str, object]], ticks: int = 8, **keys: object) -> dict[str, object]:
    document: dict[str, object] = {
        "law": "beam",
        "model_id": "w-world-test",
        "shape": [7, 1, 1],
        "boundary": "open",
        "ticks": ticks,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1 << 20],
        "suspension": 0,
        "families": families(),
        "measured": measured,
    }
    document.update(keys)
    return document


def run(
    document: dict[str, object], ticks: int
) -> tuple[NatureBeamSimulation, list[dict[str, object]], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(
        parse_nature_beam_world(document), records.append, keep_row_clicks=True
    )
    books: list[dict[str, object]] = []
    for tick in range(1, ticks + 1):
        simulation.step()
        found = simulation.books()
        assert found["balanced"], tick
        books.append(found)
    return simulation, records, books


def line(books: dict[str, object], family: str, kind: str) -> dict[str, object]:
    families_ = books["families"]
    assert isinstance(families_, dict)
    found = families_[family][kind]
    assert isinstance(found, dict)
    return found


def clicks(records: list[dict[str, object]]) -> list[tuple[object, ...]]:
    return [
        (r["tick"], r["measured"], r["detector"], r["family"], r["amount"], r["content"])
        for r in records
        if r["event"] == "click"
    ]


# -- (a) ---------------------------------------------------------------------------


def test_the_exchange_at_one_link(tmp_path):
    """(a)."""
    document = world([neutron([1, 0, 0]), proton()])
    parsed = parse_nature_beam_world(document)
    assert parsed.hypotheses == [COLUMNS_RULE, WEAK_RULE] and parsed.families[W_].lifetime == 1
    simulation, records, books = run(document, 8)
    first, second = simulation.measured[1], simulation.measured[2]
    assert first.family == P_ and first.held == [0, PROTON, 0, 0, 0]
    assert first.charge == (CHARGE * PROTON, 1) and first.momentum == [-LABEL, 0, 0]
    assert second.family == P_ and second.held == [0, PROTON, W_CONTENT, 0, 0]
    assert second.content == NEUTRON and second.clicks == [0, 0, 1, 0, 0]
    assert second.charge == (0, 1) and second.momentum == [LABEL, 0, 0]
    become = [r for r in records if r["event"] == "become"]
    assert become == [
        {
            "event": "become",
            "tick": 3,
            "node": [2, 0, 0],
            "measured": 1,
            "trigger": "clock",
            "triggered": 3,
            "from": "n",
            "into": "p",
            "products": [["w", 1, W_CONTENT, [1, 0, 0]]],
            "recoil": [-LABEL, 0, 0],
            "counted": 0,
        }
    ]
    assert clicks(records) == [(4, 2, None, "w", 1, W_CONTENT)]
    click = next(r for r in records if r["event"] == "click")
    assert click["node"] == [3, 0, 0] and click["push"] == [LABEL, 0, 0]
    assert all(store.size == 0 for store in simulation.stores)
    for tick, found in enumerate(books, start=1):
        assert found["charge"] == [CHARGE * PROTON, 1], tick
        w_transit, w_measured = line(found, "w", "transit"), line(found, "w", "measured")
        if tick >= 4:
            assert w_transit["released"] == 1 and w_transit["current"] == 0
            assert w_measured["measured"] == W_CONTENT
        elif tick == 3:
            assert w_transit["released"] == 1 and w_transit["current"] == 1
        else:
            assert w_transit["released"] == 0
    assert simulation.ledger.lifetime_amount[W_] == 0 and simulation.ledger.escaped_amount(W_) == 0
    path = tmp_path / "world.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    record = json.loads(
        run_initialization(path, tmp_path / "run", keep_row_clicks=True).read_text(encoding="utf-8")
    )
    assert record["status"] == "completed" and record["hypotheses"] == [COLUMNS_RULE, WEAK_RULE]
    assert record["conserved_at_every_completed_tick"]
    states = {int(s["number"]): s for s in record["measured"]}
    assert states[2]["charge"] == [0, 1] and states[2]["content"] == NEUTRON
    assert states[2]["held"] == [0, PROTON, W_CONTENT, 0, 0] and states[2]["became"] == 0
    assert states[1]["charge"] == [CHARGE * PROTON, 1] and states[1]["became"] == 1
    assert record["families"][W_]["lifetime"] == 1 and record["families"][W_]["charge"] == [W_CHARGE, 1]
    border = next(d for d in record["detectors"] if d["name"] == "lifetime")
    assert border["families"]["w"]["clicks"] == 0


# -- (b) ---------------------------------------------------------------------------


def test_the_w_into_empty_space_dies_on_the_border():
    """(b)."""
    simulation, records, books = run(world([neutron([-1, 0, 0]), proton()]), 8)
    assert clicks(records) == [(4, None, "lifetime", "w", 1, W_CONTENT)]
    border = next(r for r in records if r["event"] == "click")
    assert border["node"] == [1, 0, 0] and border["momentum"] == [-LABEL, 0, 0]
    second = simulation.measured[2]
    assert second.held == [0, PROTON, 0, 0, 0] and second.momentum == [0, 0, 0]
    assert simulation.measured[1].momentum == [LABEL, 0, 0]
    assert simulation.ledger.lifetime_amount[W_] == 1 and simulation.ledger.escaped_amount(W_) == 1
    for tick, found in enumerate(books, start=1):
        assert found["charge"] == [CHARGE * PROTON, 1], tick
    assert all(store.size == 0 for store in simulation.stores)


# -- (c) ---------------------------------------------------------------------------


def entry(products: list[list[object]]) -> dict[str, object]:
    return {
        "w": {
            "rule": "become",
            "phase_window": 0,
            "phase_width": 64,
            "into": "n",
            "products": products,
        }
    }


def test_the_click_trigger_on_the_proton_balances_with_a_positive_product():
    """(c)."""
    sketch = world([neutron([1, 0, 0]), proton(entry([["beta", 1, W_CONTENT]]))])
    with pytest.raises(ValueError, match="charges do not balance"):
        parse_nature_beam_world(sketch)
    document = world([neutron([1, 0, 0]), proton(entry([["positron", 1, W_CONTENT]]))])
    simulation, records, books = run(document, 8)
    second = simulation.measured[2]
    assert second.family == N_ and second.held == [PROTON - W_CONTENT, 0, W_CONTENT, 0, 0]
    assert second.content == PROTON and second.charge == (W_CHARGE, 1)
    assert second.momentum == [LABEL, LABEL, 0] and second.became == 1
    assert second.transforms == [None] * 5 and second.table[W_] == "measure"
    become = [r for r in records if r["event"] == "become"]
    assert become[0]["trigger"] == "clock" and become[0]["measured"] == 1
    assert become[1] == {
        "event": "become",
        "tick": 4,
        "node": [3, 0, 0],
        "measured": 2,
        "trigger": "click",
        "triggered": 4,
        "from": "p",
        "into": "n",
        "products": [["positron", 1, W_CONTENT, [0, -1, 0]]],
        "recoil": [0, LABEL, 0],
        "counted": 1,
    }
    assert clicks(records) == [
        (4, 2, None, "w", 1, W_CONTENT),
        (5, None, "face:-y", "positron", 1, W_CONTENT),
    ]
    for tick, found in enumerate(books, start=1):
        assert found["charge"] == [CHARGE * PROTON, 1], tick
        if tick >= 4:
            assert line(found, "p", "measured")["became"] == 0
            assert line(found, "n", "measured")["became"] == -NEUTRON + PROTON - W_CONTENT
            assert line(found, "w", "measured")["measured"] == W_CONTENT
            assert line(found, "positron", "transit")["released"] == 1
    assert all(store.size == 0 for store in simulation.stores)


# -- (d) ---------------------------------------------------------------------------


def test_the_refusals():
    """(d)."""
    document = world([neutron([1, 0, 0]), proton()])
    document["families"] = families(w_lifetime=0)
    with pytest.raises(ValueError, match="lifetime"):
        parse_nature_beam_world(document)
    document["families"] = families(w_charge=[W_CHARGE, 2])
    with pytest.raises(ValueError, match="per unit of amount and whole"):
        parse_nature_beam_world(document)
