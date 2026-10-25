"""The shape-8 row (SR-S1 to SR-S4, the Boss's order 6398593790 (3) of 2026-10-25): the row enters from the universe file alone as {"shape": 8, "pair": [num, den]}, its algebra derived at the load; the tests sr1's five on the toy's copies, run here on the engine's Node with the toy's controls: the Zeeman doublet (the one-interval shifts of the two spins opposite and within one level of the derived num B0 x_now div (3 den Gamma)), the negated vector's lay (the lay negated, the share, the charge and the credits equal line for line), the reach (an odd line changed two Links away leaves the row bit for bit), the exclusion at the lay per full state (the pile 1x refused like, 2x opposite spins, 4x by hand), and the Stern-Gerlach gate read from the toy's committed records (the credits' centroids per spin sign along the gradient, the verdict asserted by name)."""

from __future__ import annotations

import copy
import json
from typing import Any

from event_universe import gram
from event_universe.core.rule3 import signed_quotient
from event_universe.rows import POTENTIAL, QUARTET
from tests.laws import ROOT, load_file, refused, run_back_exact, world_of

TOY = load_file("lean_toy", ROOT / "tools" / "derivations" / "toys" / "lean" / "toy.py")
RECORDS = ROOT / "tools" / "derivations" / "toys" / "lean" / "records"
CENTRE, UP, DOWN = (
    (2, 2, 2),
    [1, -1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
)  # Gamma_z's eigenvectors


def toy_of(
    spin: list[int], sense: int | None = 1, seed: list[dict[str, Any]] | None = None, **control: Any
) -> Any:
    """The toy on the middle universe with the shape-8 row: the sea and one packet of 100 quanta at the 5-cube's centre along the spin (or the seed given), with the controls."""
    universe, world = world_of("world_quartet.json")
    lay = dict(world["seed"][1], vector=spin, **({} if sense is None else {"sense": sense}))
    return TOY.Toy(
        universe, dict(world, seed=[world["seed"][0], lay] if seed is None else seed, control=control)
    )


def lines_of(node: Any) -> list[Any]:
    """The shape-8 row's lines."""
    return next(r for r in node.records() if r.shape == QUARTET).lines


def test_the_zeeman_doublet_is_the_derived_shift_with_the_two_spins_opposite_sr_s3() -> None:
    """sr1's T2: the packet of 100 quanta (the amplitude 369) stepped once in the held A_x = -B0 (y - c), B0 = 400 (Phi_z = 2 B0), with the Node term on and off: per line at the centre x_next(on) - x_next(off) is the derived num B0 x_now div (3 den Gamma) to one level, the spin up shifted with its lines and the spin down against them (g = 2, the doublet), 0 on the lines at 0."""
    field = [{"line": 1, "at": list(CENTRE), "across": 1, "along": 2, "B0": 400, "b": 0}]
    for spin, sign in ((UP, 1), (DOWN, -1)):
        on, off = toy_of(spin, held_potential=field), toy_of(spin, held_potential=field, pauli=False)
        now = [int(line.now[CENTRE]) for line in lines_of(on)]
        assert now == [369 * v for v in spin]
        on.step()
        off.step()
        shifts = [
            int(a.now[CENTRE]) - int(b.now[CENTRE])
            for a, b in zip(lines_of(on), lines_of(off), strict=True)
        ]
        num, den, gamma = on.records()[2].pair[0], on.den, on.gamma
        derived = [sign * int(signed_quotient(num * 400 * x, 3 * den * gamma)) for x in now]
        assert all(abs(s - d) <= 1 for s, d in zip(shifts, derived, strict=True)), (shifts, derived)
        assert all(
            (s == 0) == (x == 0) and (s > 0) == (sign * x > 0) for s, x in zip(shifts, now, strict=True)
        )


def test_the_negated_vector_lays_the_lay_negated_with_the_charge_the_share_and_the_credits_equal_sr_s2() -> (
    None
):
    """The double cover's -I (the 2 pi turn): the lay along -v is the lay along v with every level negated, its share and its charge equal (the bilinears even), and the run's credits equal line for line but for the levels, which are the negation; the run back exact on both."""
    a, b = toy_of(UP, ride="symmetric"), toy_of([-v for v in UP], ride="symmetric")
    la, lb = lines_of(a), lines_of(b)
    for slot in ("now", "before"):
        assert [getattr(x, slot).tolist() for x in lb] == [(-getattr(x, slot)).tolist() for x in la]
    assert a.log[-1]["share"] == b.log[-1]["share"] > 0
    assert gram.charge(QUARTET, la).tolist() == gram.charge(QUARTET, lb).tolist()
    kept = copy.deepcopy(a), copy.deepcopy(b)
    for _ in range(10):
        a.step()
        b.step()
    credits = [[e for e in node.log if e["event"] == "credit"] for node in (a, b)]
    assert len(credits[0]) == len(credits[1]) > 0
    for ca, cb in zip(*credits, strict=True):
        fa, fb = ca.pop("frame"), cb.pop("frame")
        assert ca == cb and fb["levels_now"] == [-x for x in fa["levels_now"]]
        assert {k: v for k, v in fa.items() if "levels" not in k} == {
            k: v for k, v in fb.items() if "levels" not in k
        }
    assert [run_back_exact(k, 10) for k in kept] == [10, 10]


def test_the_quartet_sees_one_link_sr() -> None:
    """sr1's T5: the shape-4 row's odd line changed by 500 at a Node two Links from the row's centre leaves the centre's eight lines (now, before, remainder) bit for bit after one interval, and changes the row one Link away."""
    a = toy_of(UP, ride="symmetric")
    b = copy.deepcopy(a)
    odd = b.row(POTENTIAL).lines[1]
    odd.now[2, 2, 4], odd.before[2, 2, 4] = odd.now[2, 2, 4] + 500, odd.before[2, 2, 4] + 500
    a.step()
    b.step()
    centre = [[[int(s[CENTRE]) for s in (x.now, x.before, x.rem)] for x in lines_of(n)] for n in (a, b)]
    assert centre[0] == centre[1]
    assert [int(x.now[2, 2, 3]) for x in lines_of(a)] != [int(x.now[2, 2, 3]) for x in lines_of(b)]


def test_the_exclusion_at_the_lay_reads_the_full_state_and_the_pile_is_gone_sr_s4() -> None:
    """sr1's pile: one quantum laid (1x its share, the amplitude 37); a second lay of the same spin and sense at the Node refused by state, the share 1x; a second lay of the opposite spin laid, the share 2x exactly (the G-orthogonal vectors add with no cross term); the same spin at the opposite sense laid, the pair neutral (W = 0 at the centre); the doubled lines' share by hand 4x (the pile the rule is for); the refusals by name: a quartet's lay with no vector, a lay onto the shape-4 row."""
    sea, one = world_of("world_quartet.json")[1]["seed"]
    one = dict(one, quanta=1, sense=1)
    single = toy_of(UP, seed=[sea, one])
    share = single.log[-1]["share"]
    rule = single.rule(single.records()[2].pair, single.content(), single.link_factors())
    assert share > 0 and single.log[-1]["amplitude"] == 37
    like = toy_of(UP, seed=[sea, one, one])
    assert like.counts["refused_lay"] == 1 and like.log[1]["cause"] == "state"
    assert int(like.share(lines_of(like), rule).sum()) == share
    opposite = toy_of(UP, seed=[sea, one, dict(one, vector=DOWN)])
    assert opposite.counts["refused_lay"] == 0
    assert int(opposite.share(lines_of(opposite), rule).sum()) == 2 * share
    neutral = toy_of(UP, seed=[sea, one, dict(one, sense=-1)])
    assert (
        neutral.counts["refused_lay"] == 0 and int(gram.charge(QUARTET, lines_of(neutral))[CENTRE]) == 0
    )
    doubled = [copy.copy(line) for line in lines_of(single)]
    for line in doubled:
        line.now, line.before = 2 * line.now, 2 * line.before
    assert int(single.share(doubled, rule).sum()) == 4 * share
    refused("names its vector", toy_of, UP, seed=[sea, {k: v for k, v in one.items() if k != "vector"}])
    refused("onto a record", toy_of, UP, seed=[sea, dict(one, row=4)])


def test_stern_gerlach_reads_the_credits_centroids_per_spin_sign_along_the_gradient_sr() -> None:
    """The gate the Boss read from sr2 (The-Spinor-Row_COMPARISON.md): on the toy's committed records of the 9-cube at 60 intervals on the former loop (an eigenvector of Gamma_x laid at the centre, 400 quanta, the held A_x = -(y - c)(B0 + b (z - c)), B0 = 200, b = 100), the credits with the spin sign + and - along z have their centroids on opposite sides of the centre along the gradient's axis, SHOWN where by 150 milli each with the control's within 150 of the centre; the verdict asserted by name (NOT SHOWN at these parameters: 119 / -118 milli, the control 112 / -51 on 62 / 59 credits), the run back exact on both records."""
    found = {}
    for name in ("on", "off"):
        record = json.loads((RECORDS / f"stern_gerlach_{name}.json").read_text(encoding="utf-8"))
        assert record["run_back"] == [10, 10] and record["world"]["intervals"] == 60
        middle = (record["world"]["shape"][2] // 2) * 1000
        places: dict[int, list[int]] = {1: [], -1: []}
        for credit in (e for e in record["log"] if e["event"] == "credit"):
            if credit["frame"]["axial_sign"][2]:
                places[credit["frame"]["axial_sign"][2]].append(credit["node"][2])
        found[name] = {sign: sum(xs) * 1000 // len(xs) - middle for sign, xs in places.items()}
    split, control = found["on"], found["off"]
    assert split[1] > 0 > split[-1]
    shown = min(split[1], -split[-1]) >= 150 and all(abs(c) < 150 for c in control.values())
    verdict = (
        "SHOWN"
        if shown
        else f"NOT SHOWN: {split[1]} / {split[-1]} against 150, the control {control[1]} / {control[-1]}"
    )
    assert verdict == "NOT SHOWN: 119 / -118 against 150, the control 112 / -51"
