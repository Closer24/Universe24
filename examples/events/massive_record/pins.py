"""The pins of the massive record kind's check worlds, computed and written into
`expectations.json` BEFORE any world runs and never moved after (BUILD.md section 5;
MASSIVE_RECORD.md sections 4, 8, 11). Every number is a COMPUTATION: copied from a
script beside the design (its name and the SHA of its output file recorded) or from the
closed form the design states, and recomputed on the world's own board by the margin
module of the package (`diagnostics/massive_record_margin`), the world's own being the
pin where the two differ (BUILD.md section 10 (b)). A world's kind (CONTROL, PIN,
PREDICTION) is written with its pin.

- (i) the block at rest: omega_b and the extent on the world's own 48^3 board; the
  design's 96^3 numbers beside them; the clock's count over the run 3000 omega_b / 2 pi.
- (ii) the block pushed to k = 3: section 8's one formula per world on its own 64^3 box,
  f / f_0 = omega_b(gamma_m s, g) / (gamma_m omega_b(s, g)), the moving block a resting
  well of width gamma_m s along the motion and s across, the non-integer width
  interpolated between its two integer neighbours (`massive_moving_pins.py`), a
  PREDICTION of the block form's residual; the first-order 1 / gamma_m (1 - eps
  (gamma_m^2 - 1) / 2) beside it as the band's second term only.
- (iii) the cavity: the exact separable form cos omega = (num / den) cos(pi / (s + 1)) at
  rest; 1 / gamma_m^2 in motion (section 8's cavity limit).
- (v) the index block at rest: the closed form n^2 = 1 + G g / (omega_0^2 - omega^2) at
  the declared integers, and the phase delay (n - 1) k s it predicts at the probe.
- (v-m) the index in motion: the design's same-Node ratios of the covariant dielectric's
  delay (`massive_moving_index.out` at the design's head), the drive's pair carried; at
  K = 4 no number is declared (read beside K = 3 to say how much of the same-Node
  numbers is the degenerate resonance's); the covariant expectation itself is formed at
  read time from the engine's own rest readings at omega', as the script forms it.

Run from the repository root:

    PYTHONPATH=src python examples/events/massive_record/pins.py
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import numpy as np

from event_universe.diagnostics.massive_record_margin import (
    block_cells,
    block_margin,
    largest_eigenvalue,
)
from event_universe.events.world import parse_nature_beam_world

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DESIGN = ROOT / "docs" / "designs" / "detector_law"
C = 1.0 / math.sqrt(3.0)
N_PHASE = 64
SCRIPTS = (
    "massive_board_margin",
    "massive_moving_pins",
    "massive_block_clock_motion",
    "massive_dielectric_index",
    "massive_moving_index",
    "massive_light_clock_relay",
    "massive_conserved_form",
    "massive_layer_pins",
)


def blob(path: Path) -> str:
    """The Git blob SHA of a file beside the design (the name and the SHA of the script
    copied, BUILD.md section 5)."""
    return subprocess.run(
        ["git", "hash-object", str(path)], capture_output=True, text=True, check=True, cwd=ROOT
    ).stdout.strip()


def load(name: str):
    return parse_nature_beam_world(json.loads((HERE / f"{name}.json").read_text(encoding="utf-8")))


def gamma_of(k: int, omega_0: float | None = None, cone: str = "exact") -> tuple[float, float]:
    """beta and gamma_m of a drive of one Link every k intervals: at the massive kind's EXACT
    CONE c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2 (MASSIVE_RECORD.md section 8 at the
    design's 14e3657e, the pin's gamma), at its second order c_m^2 = cos omega_0 c^2 (`cone`
    "second"), or at light's c = 1 / sqrt 3 (`cone` "light"); the two others are the design's
    CONTROLS beside the pin."""
    pace = 1.0 / k
    if omega_0 is None or cone == "light":
        c_cone = C
    elif cone == "second":
        c_cone = C * math.sqrt(math.cos(omega_0))
    else:
        c_cone = C * math.sqrt(math.cos(omega_0) * omega_0 / math.sin(omega_0))
    beta = pace / c_cone
    return beta, 1.0 / math.sqrt(1.0 - beta * beta)


def rectangular_mode(world, number: int, width: int) -> float:
    """omega_b of the block's well widened to `width` cells along x (s across) on the
    world's own board: the one formula's resting well of width gamma_m s."""
    entry = world.measured[number]
    definition = entry.block
    family = world.families[entry.family]
    shape = (int(world.shape[0]), int(world.shape[1]), int(world.shape[2]))
    wrap = world.kind_periodic(entry.family)
    corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
    cube = block_cells(shape, corner, definition.side, wrap)
    along = np.zeros(shape, dtype=bool)
    start = corner[0] - (width - definition.side) // 2
    for offset in range(width):
        along[(start + offset) % shape[0], :, :] = True
    across = np.any(cube, axis=0)
    cells = along & across[np.newaxis, :, :]
    ratio = np.where(cells, definition.pair[1] / definition.pair[0], family.pair[1] / family.pair[0])
    seed = np.where(cells, 1.0, 0.0) + 1e-3 * np.random.default_rng(0).standard_normal(shape)
    lambda_max, _ = largest_eigenvalue(ratio, wrap, seed)
    return math.acos(max(-1.0, min(1.0, lambda_max / 2.0)))


def one_formula(world, number: int, k: int, cone: str = "exact") -> dict[str, float]:
    """Section 8's one formula on the world's own box (`massive_moving_pins.py`) with gamma at
    the named cone (the exact cone the pin; the second order and light's the controls)."""
    reading = block_margin(world, number)
    _, gamma = gamma_of(k, reading.omega_0, cone)
    width = gamma * reading.side
    low, high = int(math.floor(width)), int(math.ceil(width))
    omega_low = rectangular_mode(world, number, low)
    omega_high = rectangular_mode(world, number, high) if high != low else omega_low
    omega_wide = omega_low + (omega_high - omega_low) * (width - low)
    return {
        "cone": cone,
        "omega_b_rest": reading.omega_b,
        "eps": reading.eps,
        "extent": reading.extent,
        "gamma_m": gamma,
        "width": width,
        "omega_b_low": omega_low,
        "omega_b_high": omega_high,
        "omega_b_wide": omega_wide,
        "pin_f_over_f0": omega_wide / (gamma * reading.omega_b),
        "first_order": (1.0 / gamma) * (1.0 - reading.eps * (gamma * gamma - 1.0) / 2.0),
    }


def clock_omega(clock: tuple[int, int]) -> float:
    """omega of a light clock `phase_per_link` [a, b] on the circle of N = 64."""
    return 2.0 * math.pi * clock[0] / (clock[1] * N_PHASE)


def main() -> None:
    pins: dict[str, object] = {
        "format": "massive-record-expectations-v1",
        "identity": "massive-record-v1",
        "design": "docs/designs/detector_law/MASSIVE_RECORD.md sections 4, 8, 11 and the build's plan BUILD.md section 5; every number written before its world runs and never moved after",
        "scripts": {
            name: {"py": blob(DESIGN / f"{name}.py"), "out": blob(DESIGN / f"{name}.out")}
            for name in SCRIPTS
            if (DESIGN / f"{name}.out").exists()
        },
        "worlds": {},
    }
    worlds: dict[str, object] = pins["worlds"]  # type: ignore[assignment]
    # (i) at rest, CONTROL
    for name, design in (("rest_20", (0.11066, 5.7, 0.451)), ("rest_28", (0.13184, 8.2, 0.220))):
        world = load(name)
        reading = block_margin(world, 0)
        worlds[name] = {
            "kind": "CONTROL",
            "reads": "the block's own clock at rest: its count over the run and the spectral peak of its record's sum (GAMEBOARD) against omega_b",
            "pin": {
                "omega_b": reading.omega_b,
                "period_intervals": 2.0 * math.pi / reading.omega_b,
                "count_over_run": world.ticks * reading.omega_b / (2.0 * math.pi),
                "eps": reading.eps,
                "extent": reading.extent,
            },
            "design": {
                "omega_b": design[0],
                "extent": design[1],
                "eps": design[2],
                "source": "massive_board_margin.out on a 96^3 box; the world's own 48^3 number is the pin (the periodic image's shift)",
            },
        }
    # (ii) pushed to k = 3, PREDICTION
    for name, design in (
        ("moving_20", (0.7814, 0.7805, 0.7831)),
        ("moving_28", (0.8032, 0.8024, 0.8048)),
    ):
        world = load(name)
        formula = one_formula(world, 0, 3, "exact")
        worlds[name] = {
            "kind": "PREDICTION",
            "reads": "THE CLICKS (DETECTOR, the reader of record): the count between clicks on the block's own record over the hold [1500, 9500] against the rest world's; the spectral peak of the record's sum over the hold a GAMEBOARD diagnostic beside; light's energy drift and the mode k = 2 pi / 3 on x (the pump's signature; no light and no coupling declared, so both read 0)",
            "pin": formula,
            "controls": {
                "second_order_c_m": one_formula(world, 0, 3, "second"),
                "light_c": one_formula(world, 0, 3, "light"),
            },
            "design": {
                "pin_f_over_f0_exact_cone": design[0],
                "control_second_order": design[1],
                "control_light": design[2],
                "source": "MASSIVE_RECORD.md section 8 at the design's 14e3657e (main e821129a): the one formula with gamma at the exact cone c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2, the second order (c_m) and light's gamma the CONTROLS beside; massive_moving_pins.out the light-gamma numbers",
            },
        }
    # (i-L), (ii-L): the layer pin world of section 11 item 7 (mu = 0.15, s = 14, g = mu^2 / 4
    # on a periodic 200^2 layer, the seed the bound mode's integer profile): the rest world's
    # pin the mode's period, the moving world's the one formula at the exact cone
    if (HERE / "layer_pin_rest_14.json").exists():
        world = load("layer_pin_rest_14")
        reading = block_margin(world, 0)
        worlds["layer_pin_rest_14"] = {
            "kind": "PIN (layer)",
            "reads": "THE CLICKS (DETECTOR, the reader of record): the count between clicks on the block's own record over [200, 3500] against the mode's period; the clicks' own spectrum the finer COMPUTATION; the summed record's and the centre cell's spectral peaks GAMEBOARD diagnostics beside",
            "pin": {
                "omega_b": reading.omega_b,
                "period_intervals": 2.0 * math.pi / reading.omega_b,
                "eps": reading.eps,
                "extent": reading.extent,
                "seed": "the bound mode's integer profile at 2^20 over the whole layer, the same at both levels (the generator's integers in the world file; the load-time check against the module's mode printed)",
            },
            "design": {
                "omega_b": 0.14846,
                "extent": 36.2,
                "source": "massive_layer_pins.out (a 256^2 layer)",
            },
        }
        world = load("layer_pin_k3_14")
        worlds["layer_pin_k3_14"] = {
            "kind": "PIN (layer)",
            "reads": "THE CLICKS (DETECTOR): the count between clicks over the hold [10200, 18200] after the ramp of 10000 (DECLARATIONS.md section 8) against the rest world's, f / f_0; the peaks GAMEBOARD diagnostics beside; a row whose clicks still beat after the ramp is a diagnostic until they read the mode (then a longer ramp)",
            "pin": one_formula(world, 0, 3, "exact"),
            "controls": {
                "second_order_c_m": one_formula(world, 0, 3, "second"),
                "light_c": one_formula(world, 0, 3, "light"),
            },
            "design": {
                "pin_f_over_f0_exact_cone": 0.8116,
                "control_second_order": 0.8108,
                "control_light": 0.8132,
                "script_layer_reading": 0.8113,
                "source": "MASSIVE_RECORD.md section 11 item 7 and SCHEDULE.md row 4a (the exact cone; the second order and light's beside; massive_layer_pins.out the script's own reading)",
            },
        }
    # (iii) the cavity, CONTROL
    world = load("cavity_24")
    num, den = world.families[1].pair
    side = world.measured[0].block.side
    omega = math.acos((num / den) * math.cos(math.pi / (side + 1)))
    worlds["cavity_24"] = {
        "kind": "CONTROL",
        "reads": "the cavity's count over the run and its spectral peak (GAMEBOARD) against the separable form",
        "pin": {
            "omega": omega,
            "period_intervals": 2.0 * math.pi / omega,
            "count_over_run": world.ticks * omega / (2.0 * math.pi),
            "form": "cos omega = (num / den) cos(pi / (s + 1)) with the pair [800, 809] and s = 24",
        },
        "design": {
            "omega": 0.19503,
            "source": "MASSIVE_RECORD.md section 4's table, the quadrature 0.19515 to the lattice's residual",
        },
    }
    _, gamma3 = gamma_of(3, math.acos(num / den), "exact")
    worlds["cavity_24_moving"] = {
        "kind": "CONTROL",
        "reads": "the cavity's count per interval over the hold against the rest cavity's rate (GAMEBOARD); the pump's signature (0, no light declared)",
        "pin": {
            "f_over_f0": 1.0 / (gamma3 * gamma3),
            "form": "1 / gamma_m^2 at the exact cone, section 8's cavity limit (the medium's clock); as built the moving cavity is a hard mirror stepping (BUILD_READINGS.md), its number never read against this until the physicist redeclares it",
        },
        "design": {"f_over_f0": 0.6667, "source": "massive_block_clock_motion.out"},
    }
    # (v) the index at rest, CONTROL of the coupling
    world = load("index_50")
    clock = world.families[0].phase_per_age
    assert clock is not None
    omega = clock_omega(clock)
    omega_0 = math.acos(7.0 / 8.0)
    for name, g, design in (
        ("index_50", 1 / 50, 1.0430),
        ("index_20", 1 / 20, 1.1044),
        ("index_10", 1 / 10, 1.1998),
    ):
        n = math.sqrt(1.0 + g / (omega_0 * omega_0 - omega * omega))
        worlds[name] = {
            "kind": "CONTROL",
            "reads": "light's phase delay at the probe against index_reference over the block's 12 cells (GAMEBOARD): n = 1 + delay / (k s), k = omega / c",
            "pin": {
                "omega": omega,
                "omega_0": omega_0,
                "n": n,
                "delay_rad": (n - 1.0) * (omega / C) * 12,
                "form": "n^2 = 1 + G g / (omega_0^2 - omega^2) at G = 1, omega_0 = acos(7 / 8), omega = 2 pi (153 / 100) / 64",
            },
            "design": {
                "n": design,
                "source": "massive_dielectric_index.out at its omega_0 = 0.5000; the chain's own 1.034, 1.083, 1.159 the lattice's band, 0.8 to 3.4 percent below the closed form",
            },
        }
    # (v-m) the index in motion, PREDICTION
    for k in (3, 4):
        beta, gamma = gamma_of(k)
        for direction, sign in (("toward", 1.0), ("away", -1.0)):
            omega_prime = gamma * clock_omega((3565, 10000)) * (1.0 + sign * beta)
            entry: dict[str, object] = {
                "kind": "PREDICTION",
                "reads": "light's phase delay at the probe over the window [3400, 4300] against the reference at omega (GAMEBOARD), as the ratio to the covariant expectation (n(omega') - 1) omega' gamma_m s / c with n(omega') from the engine's own rest world at omega' (index_moving_rest_k"
                + str(k)
                + "_"
                + direction
                + " against its reference); light's energy drift and the mode k = 2 pi / 3 on x over the window (the pump's signature)",
                "pin": {
                    "k": k,
                    "beta_c": beta,
                    "gamma_m": gamma,
                    "omega": clock_omega((3565, 10000)),
                    "omega_prime": omega_prime,
                    "drive_pair": [k * k, k * k - 3],
                },
            }
            if k == 3:
                # the same-Node form's ratios on this chain of 2200 (the design's .out:
                # head-on 0.500 and 0.399; from behind 2.569 and 1.582, the window's two
                # halves unequal there); the design's pin FROM BEHIND, 6.8 and 4.3, is
                # read on the longer chain below
                entry["pin"]["ratio_read_over_expected"] = 0.500 if direction == "toward" else 2.569  # type: ignore[index]
                entry["design"] = {
                    "ratio_drive_pair": 0.500 if direction == "toward" else 2.569,
                    "ratio_G_g_unchanged": 0.399 if direction == "toward" else 1.582,
                    "source": "massive_moving_index.out at the design's head (the same-Node form on the chain of 2200, the rows re-forming); the engine carries the drive's pair, so the pin is the drive-pair ratio; a PREDICTION of the model as built, never Fizeau's",
                }
            else:
                entry["design"] = {
                    "source": "no number declared at K = 4 (MASSIVE_RECORD.md section 11 item 4: read beside K = 3 to say how much of the same-Node numbers is the degenerate resonance's, exact at K = 3)",
                }
            worlds[f"index_moving_k{k}_{direction}"] = entry
        omega_away = gamma * clock_omega((3565, 10000)) * (1.0 - beta)
        long_entry: dict[str, object] = {
            "kind": "PREDICTION",
            "reads": "the receding case on the longer chain (n = 4000, the source at 300, the probe at 2500, the block from x = 1500 from interval 2600, the window [5000, 6000]): the ratio of the delay to the covariant expectation with n(omega') from index_moving_long_rest_k"
            + str(k)
            + "_away against its reference; the pump's signature over the window",
            "pin": {
                "k": k,
                "beta_c": beta,
                "gamma_m": gamma,
                "omega": clock_omega((3565, 10000)),
                "omega_prime": omega_away,
                "drive_pair": [k * k, k * k - 3],
            },
        }
        if k == 3:
            long_entry["pin"]["ratio_read_over_expected"] = 6.740  # type: ignore[index]
            long_entry["design"] = {
                "ratio_drive_pair": 6.740,
                "ratio_G_g_unchanged": 4.277,
                "source": "massive_moving_index.out at the design's head, the receding case on the longer chain (the same-Node form; the Boss's 16:13Z: 4.3 and 6.8 from behind); the engine carries the drive's pair, so the pin is 6.74",
            }
        else:
            long_entry["design"] = {"source": "no number declared at K = 4 (read beside K = 3)"}
        worlds[f"index_moving_long_k{k}_away"] = long_entry
    (HERE / "expectations.json").write_text(json.dumps(pins, indent=1) + "\n", encoding="utf-8")
    for name, entry in worlds.items():
        print(name, entry["kind"], json.dumps(entry["pin"])[:160])


if __name__ == "__main__":
    main()
