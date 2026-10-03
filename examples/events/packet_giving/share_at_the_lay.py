"""The share at the lay, the one diagnostic of the advisor's second on the packet lay (examples/events/packet_giving, blind_and_reading.md, "The share at the lay"; #1572 comment 5967374097; the mathematician's 242, 5967687794, section 1, and the advisor's second, 5967838095): the same packet (tau 48, w 4, [2, 3]) at T = 2^22, where the floor is far, and at the shipped T, laid by the engine's own `laid_packet` (both time levels at the carrier's phase) in three rows, the old root S = T / (2 sin Omega), the one-line root T / sin Omega and the branch's lay as it is (the scratch substitutes a row's root in its own process at run time and reads the laid a_0 back; nothing in src changes), its share over the board read at the lay's interval and the nine after in the top's unit W_c = 3 den T, in the own unit at [2, 3] W_d = W_c sin Omega and in W_rec where the books hold it, beside the invariant 2 SUM a^2 sin Omega / T of each envelope; against it the guide's source in time at the same T (the resonance world's chain with the giver alone, `laid_increment` over the lifetime), read at the lay's interval, at the span's end and nine intervals after. A scratch: it writes a universe with the quantum action T beside the run in a temporary folder and ships nothing; every share is a GameBoard reading and is labelled so; the blind stands in blind_and_reading.md, written before any run.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/packet_giving/share_at_the_lay.py [--action 4194304] [--seed 1] [--after 9] [--lifetime 48] [--width 4]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from event_universe import giving
from event_universe.core.rule3 import division_fixed_point, division_forward
from event_universe.features.click import envelope
from event_universe.game_board import GameBoard
from event_universe.loader.derived import count_wall
from event_universe.world_files import input_digest, load_world

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))  # the folder's builder, the same world and the same numbers
from build_world import numbers, world  # noqa: E402

LABEL = "every share a GameBoard reading; the jump's interval the giver's own draw"


def plane_line_root(action: int, resonance: tuple[int, int]) -> int:
    """The root the branch laid before the mathematician's 242, S = T / (2 sin Omega) = isqrt((T den div 2)^2 div (den^2 - num^2)), one line's share of a plane's quantum (the ledger's line 16), kept here by its own formula so that the reading of the old root stands whatever root the engine lays."""
    num, den = resonance
    half = int(division_forward(action * den, 2, 0)[0])
    return division_fixed_point(int(division_forward(half * half, den * den - num * num, 0)[0]))


def one_line_root(action: int, resonance: tuple[int, int]) -> int:
    """The root of a packet on one real line, SUM a^2 = T / sin Omega = isqrt(T^2 den^2 div (den^2 - num^2)), twice the plane's S of one line (the mathematician's 242, section 1), one root of the whole product by the fixed point of the division act."""
    num, den = resonance
    square = int(division_forward(action * action * den * den, den * den - num * num, 0)[0])
    return division_fixed_point(square)


def scratch_universe(design: dict[str, Any], action: int, folder: Path) -> Path:
    """The design's universe with the quantum action `action` in place of the file's, written beside the run and named by its absolute path (the loader joins a repository path, an absolute one stands)."""
    universe = json.loads((ROOT / design["universe"]).read_text(encoding="utf-8"))
    universe["integers"]["quantum_action"] = action
    path = folder / f"universe_{action}.json"
    path.write_text(json.dumps(universe) + "\n", encoding="utf-8")
    return path


def written(document: dict[str, Any], path: Path) -> Path:
    """A world written with the generator's empty mode file beside it (an instrument body takes no mode entry), the mode file carrying the world's digest."""
    path.write_text(json.dumps(document) + "\n", encoding="utf-8")
    mode = {"world_digest": input_digest(document), "bodies": [], "messages": []}
    path.with_suffix(".mode.json").write_text(json.dumps(mode) + "\n", encoding="utf-8")
    return path


def units_of(board: GameBoard, index: int, resonance: tuple[int, int]) -> dict[str, int]:
    """The three units a share is read in: W_c = 3 den T, the top's; W_d = isqrt(W_c^2 (den^2 - num^2)) div den, the own unit at the resonance (the resonance world's and the dedicated test's line); W_rec where the credit's books hold a unit per record (the engine after #1717), else the top's."""
    num, den = resonance
    top = count_wall(board.families[index], board.world.quantum_action)
    own = int(division_forward(division_fixed_point(top * top * (den * den - num * num)), den, 0)[0])
    held = getattr(board.credit, "units", None)
    return {"W_c": top, "W_d": own, "W_rec": int(held[index]) if held else top}


def reading(board: GameBoard, index: int, units: dict[str, int]) -> dict[str, Any]:
    """One interval's share of the family over the board, a GameBoard reading: in the top's unit and in the own unit as fractions, and in whole quanta by the count's line, (share + W div 2) div W, in each unit."""
    total, frozen = board.total_share(index)
    if total is None:
        return {"tick": board.tick, "share": None, "frozen": frozen}
    quanta = {
        name: int(division_forward(total, wall, division_forward(wall, 2, 0)[0])[0])
        for name, wall in units.items()
    }
    return {
        "tick": board.tick,
        "over_W_c": round(total / units["W_c"], 4),
        "over_W_d": round(total / units["W_d"], 4),
        "quanta": quanta,
    }


def run(path: Path, light: str, seed: int, span: int, after: int, resonance: tuple[int, int]) -> dict:
    """One world from its file to the giving and `span` - 1 + `after` intervals beyond it: the giver's generator at the trial's seed as the builder's reading sets it; the share at the lay's interval, at the span's end and at every one of the `after` intervals after it, with the sparse trail in between; the largest level laid, the body's slice at z = 0 carrying a_0, the root laid read back."""
    lines: list[dict[str, Any]] = []
    board = GameBoard(load_world(path), lines.append)
    for books in board.credit.bodies:
        books.state = seed * len(board.credit.bodies) + books.number
    index = [f.name for f in board.families].index(light)
    units = units_of(board, index, resonance)
    given: int | None = None
    trail: list[dict[str, Any]] = []
    for _ in range(int(json.loads(path.read_text(encoding="utf-8"))["ticks"])):
        board.step()
        if given is None:
            jumps = [c for c in lines if c["event"] == "jump" and c.get("given") == light]
            if jumps:
                given = int(jumps[0]["tick"])
                trail.append({"at": "the lay's interval", **reading(board, index, units)})
            continue
        since = board.tick - given
        if since == span - 1:
            trail.append({"at": "the span's end", **reading(board, index, units)})
        elif since < span - 1 and since % 8 == 0:
            trail.append({"at": "inside the span", **reading(board, index, units)})
        elif span - 1 < since <= span - 1 + after:
            trail.append({"at": f"{since - span + 1} after", **reading(board, index, units)})
        if since >= span - 1 + after:
            break
    lays = [c for c in lines if c["event"] == "lay" and c["family"] == light]
    both = sum(1 for c in lays if c["before"][0] != c["after"][0] and c["before"][1] != c["after"][1])
    return {
        "world": path.name,
        "given_at": given,
        "lay_lines": len(lays),
        "lay_lines_changing_both_levels": both,
        "largest_level_laid": max((abs(c["after"][0] - c["before"][0]) for c in lays), default=0),
        "count_in_books": board.credit.counts[index],
        "units": units,
        "units_over_W_c": {k: round(v / units["W_c"], 4) for k, v in units.items()},
        "trail": trail,
    }


def envelope_numbers(total: int, span: int, across: int, action: int, sine: float) -> dict[str, Any]:
    """A root's envelope: a_0, the length, the slices at one level, the deficit, the invariant 2 SUM a^2 sin Omega / T and the form of an infinite plane wave of the mode at these squares, sin Omega over 2 times the invariant (3 den a^2 sin^2 Omega per Node, pointwise)."""
    amplitudes = envelope(total, span, across)
    squares = across * sum(a * a for a in amplitudes)
    return {
        "root": total,
        "a_0": amplitudes[0],
        "length": len(amplitudes),
        "slices_at_one_level": sum(1 for a in amplitudes if a == 1),
        "deficit": total - squares,
        "invariant_2_sum_a2_sin_omega_over_T": round(2 * squares * sine / action, 5),
        "plane_wave_form_over_W_c": round(squares * sine * sine / action, 4),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--action", type=int, default=2**22, help="the quantum action T of the scratch")
    parser.add_argument("--seed", type=int, default=1, help="the trial's seed, as the builder's reading")
    parser.add_argument("--after", type=int, default=9, help="the intervals read after the lay")
    parser.add_argument(
        "--lifetime", type=int, default=None, help="another lifetime tau (the design's 48)"
    )
    parser.add_argument("--width", type=int, default=None, help="another width w (the design's 4)")
    args = parser.parse_args(argv)
    started = time.time()
    design = json.loads((HERE / "design.json").read_text(encoding="utf-8"))
    if args.lifetime is not None:  # the advisor's scratch packet, tau 2 and w 3, read for its residue
        design["giver"] = {**design["giver"], "lifetime": args.lifetime, "window": args.lifetime}
    if args.width is not None:
        design["width"] = args.width
    num, den = design["giver"]["resonance"]
    lifetime, width, light = int(design["giver"]["lifetime"]), int(design["width"]), design["light"]
    sine = math.sqrt(den * den - num * num) / den
    laid = (
        giving.exact_total
    )  # the engine's root as the branch lays it, restored after every substitution
    roots = {
        "old root, S = T / (2 sin Omega)": plane_line_root(args.action, (num, den)),
        "one-line root, T / sin Omega": one_line_root(args.action, (num, den)),
        "the branch's lay as it is": laid(args.action, (num, den)),
    }
    longest = max(len(envelope(r, lifetime, width * width)) for r in roots.values())
    out: dict[str, Any] = {
        "label": LABEL,
        "quantum_action": args.action,
        "lifetime": lifetime,
        "width": width,
        "sin_omega": round(sine, 4),
    }
    with tempfile.TemporaryDirectory(prefix="share_at_the_lay_") as scratch:
        folder = Path(scratch)
        universe = scratch_universe(design, args.action, folder)
        design = {**design, "quantum_action": args.action, "universe": str(universe)}
        found = numbers(design)
        design["margin"] = int(design["margin"]) + longest - found["length"]  # one board for every root
        found = numbers(design)
        packet = {**world(design), "ticks": 40 * lifetime}
        packet[
            "detectors"
        ] = [  # the design's reach falls beyond a short train's board; no region enters the form
            d for d in packet["detectors"] if all(0 <= p[0] < found["shape"][0] for p in d["positions"])
        ]
        packet_path = written(packet, folder / "packet.json")
        chain = json.loads((HERE.parent / "resonance" / "resonant.json").read_text(encoding="utf-8"))
        giver = {**chain["measured"][0], "instrument": {**chain["measured"][0]["instrument"]}}
        giver["rates"] = [{**giver["rates"][0], "lifetime": lifetime}]
        giver["instrument"]["window"] = lifetime
        chain = {**chain, "universe": str(universe), "measured": [giver], "ticks": 40 * lifetime}
        chain_path = written(chain, folder / "chain.json")
        out["board"] = {"shape": found["shape"], "body": found["body"]}
        source_total = roots["the branch's lay as it is"]
        out["source_in_time"] = {
            "A_t_flat": division_fixed_point(int(division_forward(source_total, lifetime, 0)[0])),
            "span": lifetime,
            "chain": chain["shape"],
            "run": run(chain_path, light, args.seed, lifetime, args.after, (num, den)),
        }
        try:
            for name, root in roots.items():
                if name.startswith("the branch"):
                    giving.exact_total = laid
                else:  # the row's root substituted in this process alone, nothing in src changed
                    giving.exact_total = lambda action, resonance, root=root: root
                row = {
                    "envelope": envelope_numbers(root, lifetime, width * width, args.action, sine),
                    "run": run(packet_path, light, args.seed, 1, args.after, (num, den)),
                }
                row["root_laid_as_read_back"] = (
                    row["run"]["largest_level_laid"] == row["envelope"]["a_0"]
                )
                out[name] = row
        finally:
            giving.exact_total = laid
    out["seconds"] = round(time.time() - started, 1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
