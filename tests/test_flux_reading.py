"""The flux reading (ALGEBRA.md 9.19 (3), the mathematician's derivation of 2026-09-24 from
8.2; the model owner's word, "plant board values and check everything works as expected"):
(a) the local identity e_i(t) - e_i(t - 1) = SUM over the reads j of i of G_ij, with G_ij =
(1 / 3) A_ij (now_i before_j - before_i now_j) the flux into i from j, holds EXACTLY on the
engine's integer rule up to the remainders' own term of 8.2 at the Node, (a_next,i -
a_before,i) (r_i - r'_i) / (3 num_i), on planted random rows (light's pair [1, 1] and the
matter kind [800, 809]), the flux antisymmetric and pair-free; (b) a packet's one-way inward
flux into one detector, SUM over intervals and Ports of max(G, 0), over its passage is the
packet's conserved form I to a part in a hundred (the backward part of a planted packet
returns through the open face's mirror and passes the detector too, the excess the lattice's
counter-flow), the signed sum below a part in a million of I. Every number here is a
COMPUTATION on the rule's integers; no pin."""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation, LiveRecord
from event_universe.events.rule import rule_coefficients
from event_universe.events.world import parse_nature_beam_world
from tests.test_emitter import NODE_CLOCK
from tests.test_emitter import reads as family_reads
from tests.test_massive_record import massive_world

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md 9.57 (2);
# the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}


def planted(simulation: DetectorLawSimulation, family: int, now, before, remainder) -> LiveRecord:
    """A record's rows given to the rule directly (no Ports: the flux reads the rows, not a take)."""
    return LiveRecord(
        1,
        0,
        family,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        now.astype(np.int64),
        before.astype(np.int64),
        remainder.astype(np.int64),
        pointers=[0] * len(simulation.detector_names),
        first_rung=[None] * len(simulation.detector_names),
        age=10,
    )


def reads(simulation: DetectorLawSimulation, family: int, length: int) -> dict[tuple[int, int], int]:
    """The read matrix A of a chain (y and z of extent 1): (i, j) with the multiplicity of the
    reads of j among the six reads of i; the self-reads of the folded axes."""
    wrap = simulation.kind_wrap[family]
    out: dict[tuple[int, int], int] = {}
    for x in range(length):
        for axis in range(3):
            for sign in (1, -1):
                if axis > 0:
                    if wrap[axis]:
                        out[(x, x)] = out.get((x, x), 0) + 1
                    continue
                j = x + sign
                if 0 <= j < length:
                    out[(x, j)] = out.get((x, j), 0) + 1
                elif wrap[0]:
                    out[(x, j % length)] = out.get((x, j % length), 0) + 1
    return out


def chain_world(pair: list[int] | None, length: int, boundary: dict[str, str]) -> DetectorLawSimulation:
    document = massive_world([length, 1, 1], boundary, [800, 809])
    document["detectors"] = []
    document["age_bound"] = 100000
    return DetectorLawSimulation(parse_nature_beam_world(document))


def test_the_local_flux_identity_is_exact_on_the_rules_integers():
    """(a) on a periodic chain of 60, five intervals, random rows and remainders."""
    for family, (num, den) in ((0, (1, 1)), (1, (800, 809))):
        simulation = chain_world(None, 60, PERIODIC)
        matrix = reads(simulation, family, 60)
        rng = np.random.default_rng(3)
        now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        remainder = rng.integers(0, 3 * den, size=(60, 1, 1), dtype=np.int64)
        live = planted(simulation, family, now, before, remainder)
        if family == 1:
            live.driven = None  # a massive record advanced by the rule alone

        def level(rows, i):
            return Fraction(int(rows[i, 0, 0]))

        def share(a_next, a_now, matrix=matrix, num=num, den=den):
            found = []
            for i in range(60):
                total = sum(Fraction(m) * level(a_now, j) for (ii, j), m in matrix.items() if ii == i)
                found.append(
                    Fraction(den, num) * (level(a_next, i) ** 2 + level(a_now, i) ** 2)
                    - Fraction(1, 3) * level(a_next, i) * total
                )
            return found

        for _ in range(5):
            a_before, a_now, r_old = live.before.copy(), live.now.copy(), live.remainder.copy()
            simulation._advance(live)
            a_next, r_new = live.now.copy(), live.remainder.copy()
            old, new = share(a_now, a_before), share(a_next, a_now)
            for i in range(60):
                flux = sum(
                    Fraction(m, 3)
                    * (level(a_now, i) * level(a_before, j) - level(a_before, i) * level(a_now, j))
                    for (ii, j), m in matrix.items()
                    if ii == i
                )
                # the remainders' term under the weak-field rule, (a_next - a_before) (r -
                # r') / (3 R) at a Node without content, R = 2 Gamma^2 num (ALGEBRA.md 9.57 (1))
                remainder_term = (level(a_next, i) - level(a_before, i)) * Fraction(
                    int(r_old[i, 0, 0]) - int(r_new[i, 0, 0]), 3 * 2 * NODE_CLOCK**2 * num
                )
                assert new[i] - old[i] - flux == remainder_term, (family, i)
        # antisymmetry and the pair-free form: G_ij = -G_ji on every Link
        for (i, j), m in matrix.items():
            if i != j:
                g_ij = Fraction(m, 3) * (
                    level(live.now, i) * level(live.before, j)
                    - level(live.before, i) * level(live.now, j)
                )
                g_ji = Fraction(matrix[(j, i)], 3) * (
                    level(live.now, j) * level(live.before, i)
                    - level(live.before, j) * level(live.now, i)
                )
                assert g_ij == -g_ji


def test_a_packets_one_way_inward_flux_into_one_cell_is_its_conserved_form():
    """(b) a Gaussian packet of 40 Links at k = 0.3024 on light's open chain of 400, read at the
    Node 200 over 600 intervals: the one-way inward flux 1.0017 of I (the backward part of the
    planted packet, 1.35 percent, returns through the -x face, no Node beyond the board, and
    passes the Node too; the excess the lattice's counter-flow on the passage; before the
    take retired the sponge took that part and the reading was 0.9865), the signed sum
    7 x 10^4 against I 5.9 x 10^11 (COMPUTATION)."""
    simulation = chain_world(None, 400, {"x": "open", "y": "periodic", "z": "periodic"})
    matrix = reads(simulation, 0, 400)
    k = 0.3024
    omega = math.acos((math.cos(k) + 2) / 3)  # the chain's band at light's pair
    x = np.arange(400)
    envelope = np.exp(-(((x - 60) / 14.0) ** 2))
    now = np.rint(UNIT * envelope * np.cos(k * (x - 60))).astype(np.int64).reshape(400, 1, 1)
    before = np.rint(UNIT * envelope * np.cos(k * (x - 60) + omega)).astype(np.int64).reshape(400, 1, 1)
    live = planted(simulation, 0, now, before, np.zeros((400, 1, 1), dtype=np.int64))

    def form(a_next, a_now) -> Fraction:
        total = Fraction(0)
        for i in range(400):
            read = sum(
                Fraction(m) * Fraction(int(a_now[j, 0, 0])) for (ii, j), m in matrix.items() if ii == i
            )
            total += (
                Fraction(int(a_next[i, 0, 0]) ** 2 + int(a_now[i, 0, 0]) ** 2)
                - Fraction(1, 3) * Fraction(int(a_next[i, 0, 0])) * read
            )
        return total

    start = form(live.now, live.before)
    node = 200
    one_way = Fraction(0)
    signed = Fraction(0)
    for _ in range(600):
        a_now, a_before = live.now.copy(), live.before.copy()
        simulation._advance(live)
        for j in (node - 1, node + 1):
            g = Fraction(1, 3) * (
                int(a_now[node, 0, 0]) * int(a_before[j, 0, 0])
                - int(a_before[node, 0, 0]) * int(a_now[j, 0, 0])
            )
            one_way += max(g, Fraction(0))
            signed += g
    ratio = one_way / start
    assert Fraction(99, 100) < ratio < Fraction(101, 100), float(ratio)
    assert abs(signed) * 1_000_000 < start, (float(signed), float(start))


def test_the_conserved_form_and_the_detectors_inflow_tally_are_the_engines_integers():
    """(c) the engine's `conserved_form` is 3 I times the family's wall times Gamma (the Node
    clock, ALGEBRA.md 9.35 (2); BUILD.md section 26 item 31: I with the clock's weights (den f
    / (Gamma num)) on the squares and (2 den M / (Gamma num)) on now x before at the seven
    Nodes with content, the well at 20 and the six receiver bodies, M = 1) on planted rows,
    exact against the Fraction form, for light (the wall 1) and for a massive family with a well
    ([8, 7] on the kind [7, 8]: the wall 56); (d) the engine's `detector_inflow_tally` into a set of
    three Nodes (a detector cube cut by the chain, record 1899) counts the two outer Ports
    only (the Links inside the set are no Ports), exact against the Fraction fluxes, and 0
    into a set the record does not reach."""
    document = massive_world([40, 1, 1], PERIODIC, [800, 809])
    document["age_bound"] = 100000
    document["universe"].append(
        {"name": "source", "quantum": 1, "pair": [7, 8], "charge": 0, "reads": family_reads()}
    )
    document["measured"] = [
        {
            "position": [20, 0, 0],
            "family": "source",
            "amount": 1,
            "stocks": {},
            "ramp": 0,
            "start": 0,
            "margin": "control",
            "momentum": [0, 0, 0],
            "side": 1,
            "q": 0,
            "spin": [0, 0, 0],
            "moment": [0, 0, 0],
            "pair": [8, 7],
            "seed": 0,
        },
        {
            "position": [5, 0, 0],
            "family": "light",
            "amount": 1,
            "stocks": {},
            "momentum": [0, 0, 0],
        },
        *(
            {
                "position": [x, 0, 0],
                "family": "light",
                "amount": 1,
                "stocks": {},
                "momentum": [0, 0, 0],
            }
            for x in (6, 7, 30, 31, 32)
        ),
    ]
    document["detectors"] = [
        {"name": "pair", "positions": [[5, 0, 0], [6, 0, 0], [7, 0, 0]]},
        {"name": "far", "positions": [[30, 0, 0], [31, 0, 0], [32, 0, 0]]},
    ]
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    source = [family.name for family in simulation.families].index("source")
    assert simulation.kind_wall(0) == 1 and simulation.kind_wall(source) == 56
    rng = np.random.default_rng(5)
    for family in (0, source):
        matrix = reads(simulation, family, 40)
        now = rng.integers(-UNIT, UNIT, size=(40, 1, 1), dtype=np.int64)
        before = rng.integers(-UNIT, UNIT, size=(40, 1, 1), dtype=np.int64)
        now[25:] = 0
        before[25:] = 0  # nothing at the far set's Node 30 nor beside it
        live = planted(simulation, family, now, before, np.zeros((40, 1, 1), dtype=np.int64))
        wall = simulation.kind_wall(family)
        expected = Fraction(0)
        for i in range(40):
            num = int(simulation.kind_num[family][i, 0, 0])
            den = int(simulation.kind_den[family][i, 0, 0])
            content = int(simulation.level_of("content")[i, 0, 0])
            assert content == (1 if i in (5, 6, 7, 20, 30, 31, 32) else 0)
            read_i, self_i, wall_i = rule_coefficients(num, den, NODE_CLOCK, content, True)
            # the six reads plain, the Node's terms [w (a^2 + b^2) - S a b] / (3 R) (item 44)
            read = sum(Fraction(m) * int(before[j, 0, 0]) for (ii, j), m in matrix.items() if ii == i)
            a, b = int(now[i, 0, 0]), int(before[i, 0, 0])
            expected += Fraction(wall_i * (a * a + b * b) - self_i * a * b, 3 * read_i)
            expected -= Fraction(1, 3) * a * read
        assert Fraction(*simulation.conserved_form(live)) == 3 * wall * expected
        pair = simulation.detector_names.index("pair")
        far = simulation.detector_names.index("far")
        offers = simulation.detector_inflow_tally(live)
        inward = Fraction(0)
        for i, j in ((5, 4), (7, 8)):
            g = Fraction(
                int(now[i, 0, 0]) * int(before[j, 0, 0]) - int(before[i, 0, 0]) * int(now[j, 0, 0])
            )
            inward += max(g, Fraction(0))
        # the tally in the form's units: the wall times the plain current, unweighted
        # (ALGEBRA.md 9.50 (13); item 36; the pace at both ends, item 34, HISTORY)
        assert offers.get(pair, 0) == inward * wall
        assert offers.get(far, 0) == 0


def test_the_tally_over_the_ports_is_the_board_wide_reading_and_costs_the_ports_alone(capsys):
    """THE CLICK'S COST (the model owner's record 1934; BUILD.md section 26 item 26): the
    detectors' inflow per record is read at the Port pairs alone. On the emitter world
    (the chain of 80 with the cube screen at [70, 72] and the closed faces) and on the
    detector-law layer (24 x 9 with three cubes of side 3), after every interval of a run
    the tally per detector equals the board-wide reading `inward_flux` into that detector's Nodes,
    bit for bit, for every live record; the Port pairs are listed once per family; and the
    HOST cost printed is the Ports read per record per interval against the board's Nodes
    (4 Ports of 80 Nodes on the chain, the screen cube's two and the emitter body's two; 40
    of 216 on the layer; the two slits' placement reported when the given train lands)."""
    from tests.test_detector_law import layer_world
    from tests.test_emitter import emitter_world

    for name, document, intervals in (
        ("the emitter chain", emitter_world(stock=2), 120),
        ("the detector-law layer", layer_world(), 60),
    ):
        world = parse_nature_beam_world(document)
        simulation = DetectorLawSimulation(world)
        checked = 0
        for _ in range(intervals):
            simulation.step()
            for live in simulation.records.values():
                tally = simulation.detector_inflow_tally(live)
                for detector in range(len(simulation.detector_names)):
                    mask = simulation.detector_at_node == detector
                    assert tally.get(detector, 0) == simulation.inward_flux(live, mask), (
                        name,
                        simulation.tick,
                        detector,
                    )
                checked += 1
        assert checked > 0
        families = sorted({live.family for live in simulation.records.values()} | {0})
        for family in families:
            port_i, port_j, port_detector = simulation._inflow_ports(family)
            assert port_i.shape == port_j.shape == port_detector.shape
            assert simulation._inflow_ports(family) is simulation._inflow_ports(family)
            print(
                f"click cost (HOST): {name}: family {family}: {int(port_i.size)} Ports read per "
                f"record per interval against {int(np.prod(simulation.shape))} Nodes"
            )
