"""The readings of the point emitter's first row (ALGEBRA.md 9.71 (1); BUILD.md section 26
item 50) from the one command's outputs (`tools/run_inputs.py --out DIR ...`): on the chain
the counts at the two sides and the wait at each side from its record's open (the click
line's `giving`, the record's giving click, the window's open; the file's `window_read` the
window's typical length); on the light clock the wait from the open to the click at the
seat's own set (the tick), its mean, rms and standard error. DETECTOR unless marked; no pin,
no verdict. `--wavelength WORLD.json [INTERVAL]` reads the light's rows on the chain after the
first window as a GAMEBOARD diagnostic: the mean spacing of the zero crossings along x, twice
the half wavelength, on the segment 100 to 500 Links beyond the seat on each side."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


def stats(values: list[float]) -> tuple[float, float, float]:
    n = len(values)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    mean = sum(values) / n
    rms = math.sqrt(sum((v - mean) ** 2 for v in values) / n)
    return mean, rms, rms / math.sqrt(n)


def report(clicks: list[dict], detector: str, what: str) -> None:
    waits = sorted(c["interval"] - c["giving"] for c in clicks if c["detector"] == detector)
    mean, rms, se = stats([float(w) for w in waits])
    print(
        f"DETECTOR {detector}: {len(waits)} clicks; {what} from the open: mean {mean:.1f}, rms {rms:.1f}, "
        f"standard error {se:.1f}, least {waits[0] if waits else None}"
    )


def chain(out: Path) -> None:
    data = json.loads((out / "point_chain.output.json").read_text(encoding="utf-8"))
    clicks = data.get("clicks", [])
    print("== THE POINT EMITTER ON THE CHAIN (9.71 (1) (i) to (iii))")
    print(f"DETECTOR counts {data.get('counts')}; {len({c['record'] for c in clicks})} records clicked")
    for side in ("left", "right", "face"):
        report(clicks, side, "the wait")
    print(
        "COMPUTATION set beside (9.71 (1)): the two sides alike, 32 +- 4 each of 64 with face receivers "
        "taking all; the first click at a side at 500 / c_l = 873 after the open plus the window's share "
        "(the sets of three Nodes at 500 take part and pass the rest to the faces)"
    )


def light_clock(out: Path) -> None:
    data = json.loads((out / "point_light_clock.output.json").read_text(encoding="utf-8"))
    clicks = data.get("clicks", [])
    print("== THE LIGHT CLOCK WITH A POINT EMITTER (9.71 (1) (iv))")
    print(f"DETECTOR counts {data.get('counts')}")
    report(clicks, "at_well", "the tick")
    print(
        "COMPUTATION set beside (9.71 (1) (iv)): from the open 2 x 60 / 0.573 = 209 plus the window's "
        "centroid n / 2 (n the world file's window_read; 961 at n = 1503), every tick within sqrt(n) "
        "= 39 of it with the rung's draw as now"
    )


def wavelength(path: Path, at: int | None = None) -> None:
    """GAMEBOARD: the light's rows on the chain read after the first window."""
    import numpy as np

    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.events.world import parse_nature_beam_world

    document = json.loads(path.read_text(encoding="utf-8"))
    window = int(document["measured"][0]["emitter"]["window_read"])
    at = at if at is not None else window + 400
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    for _ in range(at):
        simulation.step()
    rows = np.zeros(simulation.shape[0], dtype=np.int64)
    for live in simulation.records.values():
        if live.family == 0:
            rows += live.now[:, 0, 0]
    seat = int(document["measured"][0]["position"][0])
    for low, high, side in ((seat + 100, seat + 500, "+x"), (seat - 500, seat - 100, "-x")):
        segment = rows[max(low, 0) : min(high, len(rows))]
        crossings = [
            x
            for x in range(len(segment) - 1)
            if (segment[x] > 0 > segment[x + 1]) or (segment[x] < 0 < segment[x + 1])
        ]
        spacings = [b - a for a, b in zip(crossings, crossings[1:], strict=False)]
        mean = sum(spacings) / len(spacings) if spacings else float("nan")
        print(
            f"GAMEBOARD at interval {at}, {side} 100 to 500 Links from the seat: {len(crossings)} zero "
            f"crossings, the wavelength {2 * mean:.1f} Links (light's dispersion at the seat's rotation "
            "0.178: 20.4)"
        )


if __name__ == "__main__":
    if sys.argv[1] == "--wavelength":
        wavelength(Path(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else None)
    else:
        folder = Path(sys.argv[1])
        if (folder / "point_chain.output.json").exists():
            chain(folder)
        if (folder / "point_light_clock.output.json").exists():
            light_clock(folder)
