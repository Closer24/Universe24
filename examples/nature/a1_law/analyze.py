"""Read the records of A1 repeated under the law of the bit (docs/EXPERIMENTS.md,
2026-09-18): the two worlds of `make_worlds.py` (`two_slits`, `one_slit`) run
through the runner and replayed by `record_screen.py`. A Renderer of records
(Highlights 3.29): it reads `run.json`, `events.jsonl`, `initialization.json`
and `screen.json` and never the engine. Prints the readings and writes
`record.json`.

What it reads per world: the things counted (the clicks per mark, on the
screen and on the wall) and the emissions made; per screen mark the shadows
returned over the run (n summed over ticks, the intensity a mark returned),
their peak and its tick, the push J_x summed over ticks and its peak, the
phases and owners of what arrived; the amount at the probe Nodes behind the
slits (the peak per tick, against the 256 quanta per owner of DERIVATIONS.md
section 30); the ledger at the end. Then the fringe reading: the local maxima
and minima of the returned amount and of the push along the screen, their
spacing against the optical spacing lambda_w L / d, and the depth
(max - min) / (max + min) between the central maximum and the nearest
minimum; and the control: the two-slit profile against the one-slit profile
and its mirror image (the world is symmetric under y -> 64 - y, so the closed
slit's own pattern is the open slit's mirrored), whose sum is the incoherent
sum of the two slits, the difference being the cross term.

Run:  python examples/nature/a1_law/analyze.py RUNS_DIR [--record record.json]
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORLDS = (
    "two_slits",
    "one_slit",
    "two_slits_big",
    "one_slit_big",
    "two_slits_periodic",
    "one_slit_periodic",
)
SQRT3 = math.sqrt(3.0)


def components(value):
    return [value] if isinstance(value, int) else list(value)


def ledger_line(entry: dict, family: str) -> dict:
    line = entry["fields"][family]
    return {key: (components(v) if key != "balanced" else v) for key, v in line.items()}


def extrema(profile: list[float], ys: list[int], margin: int = 2) -> dict:
    """Local maxima and minima of a profile along y, away from the ends."""
    maxima, minima = [], []
    for i in range(margin, len(profile) - margin):
        left, here, right = profile[i - 1], profile[i], profile[i + 1]
        if here > left and here >= right:
            maxima.append((ys[i], here))
        if here < left and here <= right:
            minima.append((ys[i], here))
    spacings = [b[0] - a[0] for a, b in zip(maxima, maxima[1:], strict=False)]
    return {
        "maxima": maxima,
        "minima": minima,
        "spacings": spacings,
        "mean_spacing": (sum(spacings) / len(spacings)) if spacings else None,
    }


def depth(profile: list[float], ys: list[int], centre: int) -> dict:
    """The central value against the nearest local minimum on either side."""
    index = ys.index(centre)
    central = profile[index]
    found = None
    for step in range(1, len(profile)):
        for i in (index - step, index + step):
            if (
                1 <= i < len(profile) - 1
                and profile[i] < profile[i - 1]
                and profile[i] <= profile[i + 1]
            ):
                found = (ys[i], profile[i])
                break
        if found:
            break
    if found is None or central + found[1] == 0:
        return {"central": central, "nearest_minimum": found, "depth": None}
    return {
        "central": central,
        "nearest_minimum": found,
        "depth": (central - found[1]) / (central + found[1]),
    }


def analyze(directory: Path) -> dict:
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    screen = json.loads((directory / "screen.json").read_text(encoding="utf-8"))
    events = [
        json.loads(line)
        for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    kinds = Counter(event["event"] for event in events)
    screen_x = screen["screen_x"]
    clicks_by_mark: Counter[tuple[int, ...]] = Counter()
    quanta_by_mark: Counter[tuple[int, ...]] = Counter()
    click_ticks: dict[tuple[int, ...], list[int]] = {}
    for event in events:
        if event["event"] == "detector_click":
            key = tuple(event["position"])
            clicks_by_mark[key] += 1
            quanta_by_mark[key] += event["amount"]
            click_ticks.setdefault(key, []).append(event["tick"])
    screen_clicks = {k: v for k, v in clicks_by_mark.items() if k[0] == screen_x}
    wall_clicks = {k: v for k, v in clicks_by_mark.items() if k[0] != screen_x}
    # The lamp emits one thing every interval while its stock lasts (2^22 or
    # more against 4 per interval): the emissions are the ticks, and the photons
    # still in flight at the end are the ticks less the wall's clicks.
    emissions = int(metadata["completed_ticks"])
    (light,) = world["spatial_fields"]
    (emission,) = world["emissions"]
    lamp = world["disturbance_types"][0]["defaults"]["light"]
    ticks = screen["ticks"]
    positions = [tuple(p) for p in screen["screen"]]
    ys = [p[1] for p in positions]
    n = screen["n"]
    j = screen["j"]
    returned = [sum(n[t][k] for t in range(1, ticks + 1)) for k in range(len(positions))]
    peak = [max(n[t][k] for t in range(1, ticks + 1)) for k in range(len(positions))]
    peak_tick = [
        max(range(1, ticks + 1), key=lambda t, k=k: (n[t][k], -t)) for k in range(len(positions))
    ]
    push_x = [sum(j[t][k][0] for t in range(1, ticks + 1)) for k in range(len(positions))]
    push_y = [sum(j[t][k][1] for t in range(1, ticks + 1)) for k in range(len(positions))]
    peak_push_x = [
        max((j[t][k][0] for t in range(1, ticks + 1)), key=abs) for k in range(len(positions))
    ]
    first_arrival = [
        next((t for t in range(1, ticks + 1) if n[t][k]), None) for k in range(len(positions))
    ]
    phases_total: Counter[str] = Counter()
    for row in screen["phases"]:
        phases_total.update(row)
    owners_total: Counter[str] = Counter()
    for row in screen["owners"]:
        owners_total.update(row)
    audit = metadata["audit"]
    last = audit[-1]
    photon = emission["amount"]
    K = metadata["K"]
    # The width: the world's N (the cleanup of 2026-09-18) or, in a record made
    # before it, the family's phase_bits.
    modulus = int(world.get("N", 1 << int(light.get("phase_bits", 6))))
    # lambda_w = K_der / (sqrt(3) M) with K_der the content per turn, N x K (DERIVATIONS.md 27 (v), 29).
    lambda_w = modulus * K / (SQRT3 * photon)
    wall_x = screen["wall_x"]
    walled = {m["position"][1] for m in world["detectors"] if m["position"][0] == wall_x}
    slits = sorted(y for y in range(world["shape"][1]) if y not in walled)
    d = (slits[-1] - slits[0]) if len(slits) > 1 else None
    L = screen_x - wall_x
    optical = (lambda_w * L / d) if d else None
    centre = world["shape"][1] // 2
    centre = min(ys, key=lambda y: abs(y - centre))
    return {
        "model": metadata["model"],
        "status": metadata["status"],
        "error": metadata.get("error"),
        "completed_ticks": metadata["completed_ticks"],
        "elapsed_seconds": round(float(metadata["elapsed_seconds"]), 1),
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "dense_field": metadata.get("dense_field"),
        "K": K,
        "phase_width": modulus,
        "clock": bool(light.get("clock")),
        "photon_amount": photon,
        "lamp_stock": lamp,
        "fill": world["initial_field"]["light"]["fill"],
        "slits": slits,
        "d": d,
        "L": L,
        "lambda_w_links": lambda_w,
        "optical_spacing_links": optical,
        "emissions": emissions,
        "photons_in_flight_at_end": emissions
        - sum(clicks_by_mark[k] for k in clicks_by_mark if k[0] != screen_x),
        "events": dict(sorted(kinds.items())),
        "screen_clicks": {str(list(k)): v for k, v in sorted(screen_clicks.items())},
        "wall_clicks": {str(list(k)): v for k, v in sorted(wall_clicks.items())},
        "wall_click_quanta": sum(v for k, v in quanta_by_mark.items() if k[0] != screen_x),
        "wall_first_click": min(
            (t[0] for k, t in click_ticks.items() if k[0] != screen_x), default=None
        ),
        "things_resident_on_screen": sum(sum(row) for row in screen["things_resident"]),
        "screen_y": ys,
        "returned": returned,
        "peak": peak,
        "peak_tick": peak_tick,
        "first_arrival": first_arrival,
        "push_x": push_x,
        "push_y": push_y,
        "peak_push_x": peak_push_x,
        "phases": dict(sorted(phases_total.items(), key=lambda kv: int(kv[0]))),
        "owners": dict(owners_total),
        "wall_returned_peak": max(screen["wall_returned"]),
        "wall_returned_total": sum(screen["wall_returned"]),
        "probes": {
            key: {"peak": max(row), "peak_tick": row.index(max(row)), "last": row[-1]}
            for key, row in screen["probes"].items()
        },
        "beyond_wall_peak": max(screen["beyond_wall"]),
        "beyond_wall_peak_tick": screen["beyond_wall"].index(max(screen["beyond_wall"])),
        "beyond_wall_last": screen["beyond_wall"][-1],
        "ledger_last": {
            "tick": last["tick"],
            "light": ledger_line(last, "light"),
            "momentum": ledger_line(last, "momentum"),
            "real": last.get("real"),
            "shadow": last.get("shadow"),
        },
        "initial_totals": metadata["initial_totals"],
        "final_totals": metadata["final_totals"],
        "escaped_totals": metadata["escaped_totals"],
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "real_conserved": metadata.get("real_conserved"),
        "lamp_momentum_last": (metadata["momentum"][-1] if metadata.get("momentum") else None),
        "extrema_returned": extrema(returned, ys),
        "extrema_push": extrema(push_x, ys),
        "depth_returned": depth(returned, ys, centre),
        "depth_push": depth(push_x, ys, centre),
    }


def control(two: dict, one: dict) -> dict:
    """The two-slit profile against the incoherent sum of the one-slit profile and
    its mirror image, per mark."""
    ys = two["screen_y"]
    size = max(ys) + min(ys)
    rows = []
    for k, y in enumerate(ys):
        mirror = ys.index(size - y)
        incoherent = one["returned"][k] + one["returned"][mirror]
        incoherent_push = one["push_x"][k] + one["push_x"][mirror]
        rows.append(
            {
                "y": y,
                "two": two["returned"][k],
                "one": one["returned"][k],
                "one_mirror": one["returned"][mirror],
                "incoherent": incoherent,
                "cross": two["returned"][k] - incoherent,
                "two_push": two["push_x"][k],
                "one_push": one["push_x"][k],
                "incoherent_push": incoherent_push,
                "cross_push": two["push_x"][k] - incoherent_push,
            }
        )
    cross = [r["cross"] for r in rows]
    cross_push = [r["cross_push"] for r in rows]
    sign_changes = sum(1 for a, b in zip(cross, cross[1:], strict=False) if a * b < 0)
    sign_changes_push = sum(1 for a, b in zip(cross_push, cross_push[1:], strict=False) if a * b < 0)
    return {
        "rows": rows,
        "cross_max": max(cross),
        "cross_min": min(cross),
        "cross_sign_changes": sign_changes,
        "cross_push_max": max(cross_push),
        "cross_push_min": min(cross_push),
        "cross_push_sign_changes": sign_changes_push,
        "two_total": sum(two["returned"]),
        "incoherent_total": sum(r["incoherent"] for r in rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path)
    parser.add_argument("--record", type=Path, default=HERE / "record.json")
    args = parser.parse_args()
    record: dict = {"worlds": {}}
    for name in WORLDS:
        directory = args.runs / name / "run"
        if (directory / "screen.json").exists():
            record["worlds"][name] = analyze(directory)
    for suffix in ("", "_big", "_periodic"):
        two, one = "two_slits" + suffix, "one_slit" + suffix
        if two in record["worlds"] and one in record["worlds"]:
            record["control" + suffix] = control(record["worlds"][two], record["worlds"][one])
    for name, row in record["worlds"].items():
        print(f"## {name}: {row['status']}, {row['completed_ticks']} ticks, {row['elapsed_seconds']} s")
        print(
            f"emissions {row['emissions']}, screen clicks {sum(row['screen_clicks'].values())}, "
            f"wall clicks {sum(row['wall_clicks'].values())} at {list(row['wall_clicks'])}, "
            f"first at tick {row['wall_first_click']}; phases at the screen {row['phases']}; "
            f"owners {row['owners']}; lambda_w {row['lambda_w_links']:.2f}, optical spacing "
            f"{row['optical_spacing_links']}"
        )
        print(
            f"probes {row['probes']}; beyond the wall peak {row['beyond_wall_peak']} at tick {row['beyond_wall_peak_tick']}"
        )
        print(f"ledger {json.dumps(row['ledger_last'])}")
        print(f"extrema of the returned amount {row['extrema_returned']}")
        print(f"extrema of the push {row['extrema_push']}")
        print(f"depth returned {row['depth_returned']}, push {row['depth_push']}")
        print("| y | returned | peak (tick) | first | push_x | peak push_x |")
        print("| ---: | ---: | ---: | ---: | ---: | ---: |")
        for k, y in enumerate(row["screen_y"]):
            print(
                f"| {y} | {row['returned'][k]} | {row['peak'][k]} ({row['peak_tick'][k]}) | "
                f"{row['first_arrival'][k]} | {row['push_x'][k]} | {row['peak_push_x'][k]} |"
            )
        print()
    for key in ("control", "control_big", "control_periodic"):
        if key not in record:
            continue
        c = record[key]
        print(
            f"## {key}: cross term of the returned amount {c['cross_min']} to {c['cross_max']} "
            f"({c['cross_sign_changes']} sign changes), of the push {c['cross_push_min']} to "
            f"{c['cross_push_max']} ({c['cross_push_sign_changes']} sign changes); two-slit total "
            f"{c['two_total']} against the incoherent sum {c['incoherent_total']}"
        )
    args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(args.record)


if __name__ == "__main__":
    main()
