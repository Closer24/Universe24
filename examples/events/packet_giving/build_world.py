"""The packet giving world's builder (examples/events/packet_giving; the open board's giving as a packet along a drawn axis, the mathematician's 224 (1) and 229 with the advisor's seconds, two hands): one world from the design, its board's length, the detector's place and the blind `expectation.json` derived from the design's numbers by the engine's own pure functions (the one-line packet's root T / sin Omega, the envelope, the band's line with the transverse mode; `features/click`) and the reach's line, written before any lay and byte for byte the same on every run of this script; `--modes` writes the mode file by the generator; `--read` runs the world over the design's seeds and prints the readings beside the blind (the detector's clicks, the drawn directions from the lay lines, the far Node's cosine, a GameBoard reading labelled so).

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/packet_giving/build_world.py [--design <design>.json] [--folder <folder>] [--modes] [--read]
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

from event_universe.features.click import along_cosine, envelope, line_total
from event_universe.loader.derived import count_wall

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def numbers(design: dict[str, Any]) -> dict[str, Any]:
    """The derived numbers of the design: the one-line packet's root T / sin Omega (`line_total`; the mathematician's 242 section 1, #1572 comment 5967687794, and the advisor's second, 5967838095 section 1, two hands), the envelope's amplitudes and length L, cos k_x and the wavelength along x, the reach, the board's length and the body's and the detector's Nodes."""
    num, den = design["giver"]["resonance"]
    action, width, lifetime = (
        int(design["quantum_action"]),
        int(design["width"]),
        int(design["giver"]["lifetime"]),
    )
    total = line_total(action, (num, den))
    amplitudes = envelope(total, lifetime, width * width)
    length = len(amplitudes)
    light = tuple(design["light_pair"])
    unit = (
        3 * light[1] * action
    ) ** 2  # the count's wall squared, the lay's reference scale (the register)
    doubled = along_cosine((light[0], light[1]), (num, den), width, unit)
    assert doubled is not None, "the width cannot carry the resonance"
    cosine = doubled / (2 * unit)
    wave_number = math.acos(cosine)
    wavelength = 2 * math.pi / wave_number
    reach = (math.pi * width / wavelength) * math.sqrt(total / length)
    margin = int(design["margin"])
    centre = length + margin
    shape = [2 * (length + margin) + 1, width, width]
    across = width // 2
    return {
        "total": total,
        "amplitudes": amplitudes,
        "length": length,
        "deficit": total - width * width * sum(a * a for a in amplitudes),
        "cos_k_x": cosine,
        "k_x": wave_number,
        "k_x_over_pi": wave_number / math.pi,
        "wavelength": wavelength,
        "reach": reach,
        "reach_node": int(round(reach)),
        "shape": shape,
        "body": [centre, across, across],
        "detector_x": centre + int(round(reach)),
        "reading_node": [centre + int(round(reach)) // 2, across, across],
        "group_pace": math.sin(wave_number) / (3 * math.sqrt(1 - (num / den) ** 2)),
        "directions_held": ["+x", "-x"],
        "directions_meeting_the_detector": ["+x"],
    }


def world(design: dict[str, Any]) -> dict[str, object]:
    """The world of the design: the board long on x and `width` across, the giver at the centre with its packet's width, the region detector of the band's top across x at the reach on the +x side, the instrument's window the run."""
    found, row, light = numbers(design), design["giver"], design["light"]
    ticks = int(row["window"]) + int(design["passage_intervals"])
    giver = {
        "family": row["family"],
        "nodes": [{"node": found["body"], "count": 1}],
        "parts": [{"part": 0, "name": "g", "count": 0}, {"part": 1, "name": "e", "count": 1}],
        "transitions": [
            {
                "from": "g",
                "to": "e",
                "drive": light,
                "weight": int(row["weight"]),
                "resonance": list(row["resonance"]),
            }
        ],
        "rates": [
            {
                "from": "e",
                "to": "g",
                "lifetime": int(row["lifetime"]),
                "gives_to": light,
                "width": int(design["width"]),
            }
        ],
        "instrument": {**design["generator"], "window": int(row["window"]), "seed": int(row["seed"])},
    }
    width = int(design["width"])
    positions = [[found["detector_x"], y, z] for y in range(width) for z in range(width)]
    detector = {
        "name": design["detector"]["name"],
        "positions": positions,
    }
    return {
        "shape": found["shape"],
        "boundary": dict(design["boundary"]),
        "face_depth": int(design["face_depth"]),
        "ticks": ticks,
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [giver],
        "messages": [],
        "detectors": [detector],
        "instrument": {**design["generator"], "window": ticks, "seed": int(design["detector"]["seed"])},
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind, from the design alone: the count 1 read by the detector in its own unit within the window of the passage, the share at the lay in the top's unit (sin Omega times the top-hat's excess, the hands' derivation), the far reading of cos Omega within 2 / A_far of the resonance over the window after the giving's tick, and the fraction of seeds whose drawn direction meets the detector; written before any lay, rewritten at two hands on the one-line root (the mathematician's 242 section 1, #1572 comment 5967687794, and the advisor's second, 5967838095 section 1, two hands) before the re-run."""
    found = numbers(design)
    num, den = design["giver"]["resonance"]
    first, last = design["reading_window_after_giving"]
    sine, excess = math.sqrt(1 - (num / den) ** 2), float(design["top_hat_excess"])
    held, meeting = found["directions_held"], found["directions_meeting_the_detector"]
    return {
        "verdict": "DETECTOR",
        "comment": design["comment"],
        "family": design["light"],
        "lay": {
            "lifetime": int(design["giver"]["lifetime"]),
            "giving": "drawn per interval at the hazard 1 / lifetime in the dark, the jump line's tick",
            "width": int(design["width"]),
            "total": found["total"],
            "total_formula": "T / sin Omega = isqrt(T^2 den^2 div (den^2 - num^2)), the one-line packet's root, twice S = T / (2 sin Omega), the plane's share per line (the mathematician's 242 section 1, #1572 comment 5967687794; the advisor's second, 5967838095 section 1)",
            "length": found["length"],
            "length_formula": "the envelope in the energy form from tau and T, a_t = isqrt((R_t div tau) div w^2), R_(t+1) = R_t - w^2 a_t^2, ending where a_t falls below 1",
            "first_amplitude": found["amplitudes"][0],
            "deficit": found["deficit"],
            "lay_lines_at_most": found["length"] * int(design["width"]) ** 2,
            "cos_k_x": found["cos_k_x"],
            "k_x_over_pi": found["k_x_over_pi"],
            "wavelength": found["wavelength"],
            "reach": found["reach"],
            "shape": found["shape"],
            "body": found["body"],
            "detector_x": found["detector_x"],
        },
        "share": {
            "value": sine * excess,
            "sine_mode": sine,
            "top_hat_excess": excess,
            "reading": "the light's share over the board in the top's unit W_c at the giving's interval, the jump line's tick, a GameBoard reading",
            "status": "sin Omega of the top's unit with the sine mode across, times the top-hat's excess at its edges (the hands' derivation at T = 2^22, the mathematician's 242 section 1 and the advisor's second); at the shipped T the rounded levels' residue is a finding by name",
        },
        "count": {
            "value": 1,
            "reading": "the detector's credit lines (DETECTOR) in its own unit, the record's own share per quantum read from the books, over its window, the run, the packet's passage",
            "status": "one quantum one click by the count's line (the advisor's clause (iii)); read over the seeds whose drawn direction meets the detector; re-read on the one-line root, half of the detector's inflow at the half root having been the lay's (242 section 1)",
        },
        "cos_omega": {
            "value": num / den,
            "pair": [num, den],
            "node": found["reading_node"],
            "window_after_giving": [first, last],
            "estimator": "SUM_t n_t (n_(t+1) + n_(t-1)) / (2 SUM_t n_t^2)",
            "gate": "|cos Omega_read - num / den| <= 2 / A_far with A_far = max |n_t| over the window at the reading Node (the mathematician's 220, the advisor's second); a GameBoard reading",
        },
        "direction": {
            "fraction": [len(meeting), len(held)],
            "held": held,
            "meeting": meeting,
            "reading": "the fraction of seeds whose lay lines extend from the body toward the detector (the equivalent directions the board holds, each at the giving's weight)",
            "gate": "within sqrt(N p (1 - p)) of N p over the seeds",
        },
        "seeds": len(design["seeds"]),
        "status": "the two hands' lines (224, 229, the advisor's seconds; the root 242 section 1, the advisor's second); fence: clicks for the count, a GameBoard reading for the cosine, the lay lines for the direction",
    }


def reading(design: dict[str, Any], folder: Path) -> dict[str, object]:
    """The readings over the design's seeds (the giver's generator at the trial's seed as `tools/meeting_trials.py` sets it, the region's untouched): per seed the giving's tick from the jump line, the drawn direction from the lay lines, the detector's clicks, the light's count in the books, its share in the top's unit at the giving's tick and the far Node's cosine over the blind's window after the giving; the blind's numbers computed from the design beside them."""
    from event_universe.game_board import GameBoard
    from event_universe.world_files import load_world

    blind = expectation(design)
    path = folder / "packet_giving.json"
    world_file = json.loads(path.read_text(encoding="utf-8"))
    node = tuple(blind["cos_omega"]["node"])  # type: ignore[index]
    first, last = blind["cos_omega"]["window_after_giving"]  # type: ignore[index]
    trials = []
    for seed in design["seeds"]:
        lines: list[dict[str, Any]] = []
        board = GameBoard(load_world(path), lines.append)
        for books in board.credit.bodies:
            books.state = int(seed) * len(board.credit.bodies) + books.number
        pulse = [f.name for f in board.families].index(design["light"])
        wall = count_wall(board.families[pulse], board.world.quantum_action)
        series: dict[int, int] = {}
        given_at, share_at_lay = None, None
        for _ in range(int(world_file["ticks"])):
            board.step()
            series[board.tick] = int(board.states[pulse].lines[0].now[node])
            if given_at is None and any(c["event"] == "jump" for c in lines):
                given_at, laid = board.tick, board.total_share(pulse)[0]
                share_at_lay = None if laid is None else laid / wall
            if board.ended is not None:
                break
        lays = [c for c in lines if c["event"] == "lay" and c["family"] == design["light"]]
        xs = sorted({c["node"]["at"][0] for c in lays})
        body_x = blind["lay"]["body"][0]  # type: ignore[index]
        direction = "+x" if xs and xs[-1] > body_x else "-x" if xs and xs[0] < body_x else None
        credits = [c for c in lines if c["event"] == "credit"]
        window = [
            t
            for t in (range(given_at + first, given_at + last + 1) if given_at is not None else ())
            if t - 1 in series and t + 1 in series
        ]
        squares = sum(series[t] ** 2 for t in window)
        far = max((abs(series[t]) for t in window), default=0)
        cosine = (
            sum(series[t] * (series[t + 1] + series[t - 1]) for t in window) / (2 * squares)
            if squares
            else None
        )
        total = board.total_share(pulse)[0]
        trials.append(
            {
                "seed": seed,
                "given_at": given_at,
                "direction": direction,
                "share_at_lay": share_at_lay,
                "lay_lines": len(lays),
                "clicks": len(credits),
                "click_ticks": [c["tick"] for c in credits],
                "count_in_books": board.credit.counts[pulse],
                "share_over_wall": None if total is None else total / wall,
                "cos_omega_read": cosine,
                "far_level": far,
                "levels": [series[t] for t in window],
            }
        )
    meeting = [t for t in trials if t["direction"] in blind["direction"]["meeting"]]  # type: ignore[index]
    return {
        "world": path.name,
        "trials": trials,
        "directions": {d: sum(1 for t in trials if t["direction"] == d) for d in ("+x", "-x", None)},
        "clicks_where_meeting": [t["clicks"] for t in meeting],
        "share_at_lay": [t["share_at_lay"] for t in trials],
        "cos_omega_where_meeting": [t["cos_omega_read"] for t in meeting],
        "blind": blind,
        "label": "clicks DETECTOR; the cosine, the share and the directions GAMEBOARD readings",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--modes", action="store_true", help="write the mode file by the generator")
    parser.add_argument("--read", action="store_true", help="run the seeds and print the readings")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    blind = json.dumps(expectation(design), indent=1, ensure_ascii=False) + "\n"
    (args.folder / "expectation.json").write_text(blind, encoding="utf-8")
    path = args.folder / "packet_giving.json"
    path.write_text(json.dumps(world(design)) + "\n", encoding="utf-8")
    if args.modes:
        command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)]
        subprocess.run(command, check=True, cwd=ROOT)
    print(json.dumps({"world": str(path), "laid": bool(args.modes)}))
    if args.read:
        print(json.dumps(reading(design, args.folder), indent=1))


if __name__ == "__main__":
    main()
