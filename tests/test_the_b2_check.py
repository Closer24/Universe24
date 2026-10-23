"""The law's row (b2) on the engine, the sign holder's odd line read by the Link with the sign opposite to the time line's (ALGEBRA.md #the-rows-against-nature (b2); The sign holder rotates the two-part record; The odd line's source is the sign's own current; `FamilyRule.link_read` (-1, -1), `plane.link_levels`): a charged plane record moving along x at the group velocity v of its band past a static time line and a static odd line L_x standing with one gradient along y, the odd line at + v / c_s^2 of the time line, the ratio the engine's own booking writes for a moving record (the law's line, the odd level over the time level + v / c_s^2, read on main 2026-10-21: L_x / L_0 climbing toward 0.6056 at beta_s = 0.2855 from the first write 10 of 17.3 x 0.606). The check's premise stands outside the step: the two lines are laid in the free row 0 of the holder of the sign (read by the record, owned by no record) and restored after every interval, so the record reads one static field, as the law's reader does; the record's own row is written and read by nothing on this board. The force is the change per interval of the record's kinetic wave number along y, arg SUM conj(z_i) z_(i+y) e^(i theta_y(i)) with theta_y the row's y-Link phase pair's angle (the time line moves the kinetic wave number through the Link phase growing by k_r (L_0(i) - L_0(i + y)) / Gamma per interval, the odd line's static Link angle moves the canonical one): E the time line alone, -k_r G_0 / Gamma; M the odd line alone, -v d theta_x / dy; E + M the two together, gamma_s (1 - beta_s^2) = 1 / gamma_s of the static force for a co-moving reader, nature's Coulomb over gamma. The world is declared here and ships nowhere."""

import json
import math
from pathlib import Path

import numpy as np

from event_universe import records, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world

NUM, DEN, GAMMA, T, K_R = 4000, 6000, 6000, 36_000_000, 3
K_W = (
    T * NUM // (GAMMA * DEN)
)  # the law's alpha E_h T num / (Gamma den) at E_h 1, derived by the loader: 4,000
SHAPE, N, SIGMA, G_0, INTERVALS, A = (
    (26, 31, 1),
    2,
    3.0,
    12,
    40,
    260,
)  # the lump's amplitude 260 levels: W total 0.20 T on the one layer
C_S2 = NUM / (3 * DEN)  # the family's own light speed squared, R / w at the vacuum's paces
K = 2 * math.pi * N / SHAPE[0]
OMEGA = math.acos(
    1 - (DEN - NUM) / DEN - C_S2 * (1 - math.cos(K))
)  # 2 cos omega = 2 - 2 (den - num) / den - (2 num / 3 den)(1 - cos k)
V = C_S2 * math.sin(K) / math.sin(OMEGA)  # d omega / dk, the group velocity
BETA2 = V * V / C_S2
GAMMA_S = 1 / math.sqrt(1 - BETA2)
YC = (SHAPE[1] - 1) // 2
Y = np.indices(SHAPE)[1]


def board_of(tmp_path: Path) -> Lattice:
    """hydrogen_read3's integers and its charge holder (no `form`) with the electron alone, on a board periodic in x and z and open in y, the electron laid by a mode file as the plane wave A g(y) e^(i k x), g a Gaussian of sigma 3 about the centre, 0 on the face layers, its before level the same wave turned by the band's omega(k), the clockwise record (W > 0) moving toward +x at v."""
    universe = {
        "integers": {"node_clock": GAMMA, "quantum_action": T, "width": 63, "link_unit": 16},
        "families": [
            {
                "name": "charge",
                "pair": [6000, 6000],
                "reads": {},
                "held": {"sources": ["wronskian"], "level_weight": 1},
            },
            {"name": "electron", "pair": [NUM, DEN], "reads": {"charge": K_R}, "dimension": 2},
        ],
    }
    g = np.exp(-((np.arange(SHAPE[1]) - YC) ** 2) / (2 * SIGMA * SIGMA))
    g[0] = g[-1] = 0.0
    x = np.indices(SHAPE)[0]
    amplitude, phase = A * g[Y], K * x
    levels = [
        np.rint(amplitude * f(phase + turn)).astype(int)
        for turn in (0.0, OMEGA)
        for f in (np.cos, np.sin)
    ]
    now_re, now_im, before_re, before_im = levels
    assert (now_re * before_im - now_im * before_re).sum() > 0.19 * T  # W > 0, the clockwise record
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    world = dict(shape=list(SHAPE), boundary=dict(x="periodic", y="open", z="periodic"), face_depth=1)
    world.update(intervals=INTERVALS, universe="u.json", node_detectors=[])
    world.update(bodies=[{"family": "electron", "nodes": [{"node": [0, YC, 0], "count": 1}]}])
    (path := tmp_path / "beam.json").write_text(json.dumps(world), encoding="utf-8")
    moving = {
        key: [int(v) for v in level.ravel()]
        for key, level in zip(("now", "im_now", "before", "im_before"), levels, strict=True)
    }
    mode = {"family": "electron", "pair": [NUM, DEN], "moving": moving}
    beside = {"world_digest": input_digest(world), "bodies": [mode]}
    path.with_suffix(".mode.json").write_text(json.dumps(beside), encoding="utf-8")
    world_files.REPOSITORY_ROOT = tmp_path
    return Lattice(load_world(path))


def force_of(board: Lattice, time_line: bool, odd_line: bool) -> float:
    """The change per interval of the record's kinetic wave number along y over the run, by a linear fit, with the free row's time line G_0 (y - yc) and/or its odd line L_x = round((v / c_s^2) G_0 (y - yc)) held static."""
    charge = [f.name for f in board.families].index("charge")
    electron = [f.name for f in board.families].index("electron")
    width = board.families[charge].width
    profiles = [np.zeros(SHAPE, dtype=np.int64) for _ in range(width)]
    if time_line:
        profiles[0][:] = G_0 * (Y - YC)
    if odd_line:
        profiles[1][:] = np.rint((V / C_S2) * G_0 * (Y - YC)).astype(np.int64)

    def restore() -> None:
        for line, profile in enumerate(profiles):
            old = board.states[charge].lines[line]
            level = profile.astype(old.now.dtype)
            board.states[charge].lines[line] = records.Record(level, level.copy(), old.remainder)

    def kinetic() -> float:
        re, im = board.states[electron].lines
        z = re.now.astype(float) + 1j * im.now.astype(float)
        cosine, sine, count = (
            board.states[charge].phases[1][2],
            board.states[charge].phases[1][3],
            board.states[charge].phases[1][7],
        )  # the record's row, the y axis: its pair and its count line, the sine read with the count's sign (2026-10-21)
        sense = np.where(np.asarray(count.now) < 0, -1.0, 1.0)
        theta = np.arctan2(
            sense * np.asarray(sine.now, dtype=float), np.asarray(cosine.now, dtype=float)
        )
        return float(np.angle((np.conj(z[:, :-1]) * z[:, 1:] * np.exp(1j * theta[:, :-1])).sum()))

    restore()
    found = [kinetic()]
    for _ in range(INTERVALS):
        board.step()
        restore()
        found.append(kinetic())
    slope, _ = np.polyfit(np.arange(INTERVALS + 1), np.unwrap(np.array(found)), 1)
    return float(slope)


def test_the_co_moving_reader_reads_coulomb_over_gamma(tmp_path: Path) -> None:
    """(b2) At beta_s = 0.2855 (k = 2 pi 2 / 26 of the pair [4000, 6000], v = 0.1346, c_s^2 = 2 / 9): E within 2 percent of -k_r G_0 / Gamma (-0.00592 against -0.00600: the Link phase grows by the law's number exactly and the record's phase-gradient estimator drifts 1.3 percent on the dispersing lump); M negative, M / (-k_r G_0 / Gamma) within 1 percent of -beta_s^2 = -0.0815 (0.2 percent) and M / E within 2 percent of it (the estimator's drift again); gamma_s (E + M) / E within 0.5 percent of 1 / gamma_s = 0.9584 (0.9578); the read's sign (-1, -1) pinned by the law's own row."""
    assert abs(BETA2 - 0.08150) < 0.0001 and abs(V - 0.1346) < 0.0001
    electric_law = -K_R * G_0 / GAMMA
    holder = board_of(tmp_path).families[0]
    assert holder.link_read == (-1, -1) and (holder.write_weight, holder.write_wall) == (K_W, 1)
    electric = force_of(board_of(tmp_path), True, False)
    magnetic = force_of(board_of(tmp_path), False, True)
    both = force_of(board_of(tmp_path), True, True)
    assert abs(electric / electric_law - 1) < 0.02, (electric, electric_law)
    assert magnetic / electric < 0 and abs(magnetic / electric + BETA2) < 0.02 * BETA2, (
        magnetic / electric,
        -BETA2,
    )
    assert abs(magnetic / electric_law + BETA2) < 0.01 * BETA2, (
        magnetic / electric_law,
        -BETA2,
    )  # against the law's electric, the Link phase's exact growth
    reading = GAMMA_S * both / electric
    assert abs(reading * GAMMA_S - 1) < 0.005, (
        reading,
        1 / GAMMA_S,
    )  # gamma_s (1 - beta_s^2) = 1 / gamma_s
    print(
        f"(b2) at beta_s = {math.sqrt(BETA2):.4f}: E {electric:.7f} (the law's {electric_law:.6f}), M / E {magnetic / electric:+.5f} "
        f"(-beta_s^2 = {-BETA2:.5f}), gamma_s (E + M) / E {reading:.4f} (1 / gamma_s = {1 / GAMMA_S:.4f})"
    )
