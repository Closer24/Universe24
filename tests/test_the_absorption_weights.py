"""The absorption's weights at one denominator (ALGEBRA.md, The absorption, the draw (a) and (b): where the shares of the bodies closing one drive's interval sum above the unit the rest is 0 and the drive's one quantum goes to one of them in the proportion of their shares; each body's weight is its own transfer share, its entered label squared over its own norm, the weights of bodies of different counts brought to one denominator, the norms' least common multiple, bodies of one count read as before; the mathematician's line, #1793 comment 5981866600 K4, the advisor's second 5981976271 (3), two hands; `lists.absorption`, `credit.Books.unabsorbed_in`)."""

import json
import math
from fractions import Fraction

from event_universe import lists, meeting, world_files
from event_universe.features.phase import quarter_turn
from event_universe.lattice import Lattice
from event_universe.resonance import unit_weight
from event_universe.world_files import load_world
from tests.laws import TOOL
from tests.laws_content import (
    ONE_PHOTON,
    TWO_ATOMS,
    TWO_PHOTONS,
    ZENO_1,
    ZENO_ATOM,
    content_world,
    with_content,
)
from tests.laws_read import redeclared


def test_bodies_of_different_counts_take_by_their_own_transfer_shares(tmp_path):
    """Two atoms reading one photon, A of count 1 and B of count 2 (the anticoincidence world's two atoms, B's ground part declared at the count 2; B's norm the engine's own, read from the books and not assumed), closing one interval: the absorption's list at one denominator (ALGEBRA.md, The absorption, the draw (a) and (b); `lists.absorption`): the unit the norms' least common multiple, each body's weight its transfer share scaled by the unit over its own norm, and the rest the record's unabsorbed share less the weights, 0 where they sum above the unit (both turned whole: the two weights the unit each and nothing to the rest, one quantum one taker; A half turned and B untouched: A's weight half the unit and B's 0; A closing alone: its share in its own norm); the realised frequencies over an ensemble of worlds are the trials tool's reading (tools/meeting_trials.py) and no test's."""
    world = json.loads(json.dumps(ONE_PHOTON))  # the deleted anticoincidence world's declaration
    redeclared(world)["bodies"][1]["parts"][0]["count"] = (
        2  # the second atom's ground part at the count 2
    )
    (path := tmp_path / "two_counts.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    board = Lattice(load_world(path))
    a, b = board.credit.bodies
    drive = a.declared.transitions[0].drive
    n_a, n_b = (sum(label * label for label in books.labels) for books in (a, b))
    assert a.counts == [1, 0] and b.counts == [2, 0] and 0 < n_a < n_b  # the engine's own norms
    unit = n_a * n_b // math.gcd(n_a, n_b)

    def weights(closing, shares):  # the list's weights with the record's count 1 and no earlier window
        board.credit.counts[drive] = 1
        board.credit.account_ended(drive)
        for books, share in zip(closing, shares, strict=True):
            books.shares = {books.declared.transitions[0]: share}
        outcomes = [(books, books.declared.transitions[0]) for books in closing]
        return [alternative.weight for alternative in lists.absorption(board, drive, outcomes)]

    half = n_a // 2
    assert weights([a, b], [n_a, n_b]) == [unit, unit, 0]  # one quantum, one taker, nothing to the rest
    assert weights([a, b], [half, 0]) == [half * (unit // n_a), 0, unit - half * (unit // n_a)]
    assert weights([a], [half]) == [half, n_a - half]  # A alone: its own norm the unit
    print(f"the norms {n_a} and {n_b}, the unit {unit}: the absorption's weights at one denominator")


def test_the_weight_from_the_unit_is_checked_on_the_zeno_calibration(tmp_path):
    """C9 (a) of the click's plan, the transition's weight from the unit (`resonance.unit_weight`): the weight at which one quantum of the drive at resonance, spread over the window as it passes the Node, turns the quarter turn, the ratio of the phase line's quarter turn (9424 acts at Gamma 6000) over S_1 = sqrt(3 W T / (4 sin k)), the plane's size one quantum makes over the window; at W = 48 and T = 32768 S_1 reads 1086 at the Zeno transition [2, 3] (k = pi / 2) and 1291 at the atoms' [5414, 6000] (k = pi / 4), the ratios 8.68 and 7.30 where the files declare 1 and 6. The check on the Zeno calibration (the drive 392 at the weight 1, Itano's pi pulse): the drive carries A^2 W sin k / (3 T) = 75 + 1 / 32 quanta past the body per window, and the declared weight times the root of that count is the derived weight within one part in four hundred, the pi pulse being the derived weight's quarter turn at one quantum per window scaled by the root of the quanta, an identity of the model; so the replacement of the files' weights keeps Itano's column only with the drive re-declared at one quantum per window, 392 over the root, about 45, the owner's call, and the derivation stands beside the declared weight. None for a massive drive and for a resonance outside the massless band ([1, 3], the resonance folder's detuned taker, stands at cos k = -1). The cold reader's line of 2026-10-19 on this identity: A_1 cancels in it, so it tests neither S_1 nor the premise of one quantum turning the quarter; it says that 392 is the quarter-turn amplitude at the weight 1 over the window 48 (pi Gamma / W = 392.7) and that the derived weight is that amplitude over the one-quantum amplitude, the calibration identity by name; the unit's weight carries 1 / sqrt(W) of its window and is no coupling's constant (the check of the same day: the declared weight stands)."""
    board = Lattice(
        load_world(content_world(tmp_path, "zeno_1", ZENO_1, ZENO_ATOM, content=False))
    )  # the deleted zeno_1, inlined; a load, no run
    body, action = board.credit.bodies[0], board.world.quantum_action
    quarter = quarter_turn(board.amplitude, board.world.node_clock)
    transition, window = (
        body.declared.transitions[0],
        48,
    )  # the Zeno calibration's window, the derivation's own parameter (C9 (a)); the world's window is derived at the load since 2026-10-23 (8, the body's beat) and enters the calibration nowhere
    light, amplitude = board.families[transition.drive].pair, board.world.packets[0].amplitude
    zeno = unit_weight(quarter, window, action, light, transition.resonance)
    atom = unit_weight(quarter, window, action, light, (5414, 6000))
    assert (
        zeno is not None and atom is not None and zeno[0] == atom[0] == 9424
    )  # the unit's part from the quarter turn, the window entering the second part alone (1086 and 1291 at the declared window 48 before the derived window of 2026-10-23)
    assert (light, amplitude) == ((6000, 6000), 392)
    quanta = Fraction(amplitude**2 * window, 3 * action)  # A^2 W sin k / (3 T), sin k = 1 at pi / 2
    derived = Fraction(*zeno)
    assert (
        transition.weight == 1
    )  # the quanta per window A^2 W sin k / (3 T) follow the derived window (2401 / 32 at the declared window 48 before 2026-10-23); the weight's relation to them is the clause below
    assert abs(float(derived) / math.sqrt(quanta) - transition.weight) < 1 / 400
    assert unit_weight(quarter, window, action, (1, 1299), (2, 3)) is None  # a massive drive
    assert unit_weight(quarter, window, action, light, (1, 3)) is None  # cos k = -1, no travelling wave
    print(
        f"C9 (a): the weight from the unit {float(derived):.3f} at [2, 3] and {float(Fraction(*atom)):.3f} at "
        f"[5414, 6000] over the window {window}; the Zeno drive {amplitude} carries {float(quanta):.2f} quanta per "
        f"window, its one-quantum amplitude {amplitude / math.sqrt(quanta):.1f}"
    )


def test_a_body_among_several_drives_takes_each_by_its_own_transfer_share(tmp_path, monkeypatch):
    """The absorption among several drives (ALGEBRA.md, The click writes on the lattice (f); The two-mode line; `meeting.turned_labels`, `absorbed`): two atoms, each with the transitions g to e by `photon` and by `photon_b`, one packet of each laid at the centre toward one atom, the left atom's window closing first while `photon`'s count stands (the windows derived from the packets' passage, 37 each under the content of the born universe, the left atom closing at 45 and the right at 50 in the two drives' world, 49 and 50 with `photon` alone; re-pinned 2026-10-20 under the content, 33 each and the closes 45 and 46 before it): a drive's weight at a body is its own transfer share, so the left atom takes `photon_b`, the drive that passed it, and the right `photon`; with `photon_b` removed the one drive's share is the composed label squared bit for bit at both atoms, and `photon`'s share at each atom is the same number in both worlds."""
    seen, turned = [], meeting.turned_labels

    def kept(board, books):  # the labels and the shares at the window's close, before the click
        turned(board, books)
        shares = getattr(books, "shares", {})  # none before the fix: the clicks' assertion fails
        seen.append(
            (
                books.number,
                list(books.labels),
                {board.families[t.drive].name: s for t, s in shares.items()},
            )
        )

    monkeypatch.setattr(meeting, "turned_labels", kept)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    clicks = {}
    for drives in (("photon", "photon_b"), ("photon",)):
        universe = json.loads(json.dumps(TWO_ATOMS))
        universe["families"] += [{**universe["families"][1], "name": d} for d in drives[1:]]
        (tmp_path / "u.json").write_text(
            json.dumps(with_content(universe)), encoding="utf-8"
        )  # the content, 2026-10-20
        world = json.loads(json.dumps(TWO_PHOTONS))
        world.update(shape=[64, 1, 1], universe="u.json")
        for body, at in zip(world["bodies"], (15, 47), strict=True):
            body["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in range(at, at + 4)]  # 4 Nodes
            body["node_detector"] = {k: v for k, v in body["node_detector"].items() if k != "window"}
            body["transitions"] = [{**body["transitions"][0], "drive": d} for d in drives]
        for packet, x, family in zip(world["packets"], (32, 31), ("photon", "photon_b"), strict=True):
            packet.update(top={**packet["top"], "x": [x, x]}, family=family)
        world["packets"] = [m for m in world["packets"] if m["family"] in drives]
        (path := tmp_path / f"{len(drives)}.json").write_text(json.dumps(world), encoding="utf-8")
        TOOL.main(["--input", str(path)])
        board = Lattice(load_world(path), (lines := []).append)
        while board.interval < 70:
            board.step()
        hits = [c for c in lines if c.get("absorbed")]
        clicks[drives] = [(c["interval"], c["node_detector"], c["absorbed"]) for c in hits]
    by_share = {("body 0", "photon_b"), ("body 1", "photon")}  # each atom's drive of the larger share
    assert all((c[1], c[2]) in by_share and 40 <= c[0] <= 52 for c in clicks["photon", "photon_b"])
    assert all(c[1:] == ("body 1", "photon") and 40 <= c[0] <= 52 for c in clicks[("photon",)])
    two, one = ({n: (lab, s) for n, lab, s in part} for part in (seen[:2], seen[2:]))  # per body
    print(f"by the drives' shares {clicks['photon', 'photon_b']}; the left atom's {two[0][1]}")
    assert all(labels[1] ** 2 == shares["photon"] for labels, shares in one.values())  # one drive
    assert (
        two[1][1]["photon"] == one[1][1]["photon"]
    )  # photon's share at the right atom's close, 50 in both
    assert (
        two[0][1]["photon"] * 1000 < two[0][1]["photon_b"]
        and two[1][1]["photon_b"] * 1000 < two[1][1]["photon"]
    )
