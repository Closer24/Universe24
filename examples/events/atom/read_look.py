"""The atom level's reading from a look file (tools/look/record.py's `<world>.look.json`), a lattice reading: per interval, from the electron's two lines z = now + i second, Q = SUM |z|^2 and its radial profile within the folder's radii about the proton's Node, |z| along +x every two Nodes, the share of the plane x = centre (the 2p_x's node plane), the peak Node and its level, the rotation less the well's angle at r = 0 to 8 along +x from the centre, Omega_i = -arg(z_i(t) / z_i(t - 1)) - U_i with U_i = -k_r h_i / Gamma from the holder's row the proton sources as tools/standing_lay.py read it off the engine's start (`<world>.standing.json` beside the look, `well_along_axis`; the look's own charge row is light, the sum of the holder's rows, the electron's own row among them, and not the row the electron reads), and the look's share over the family's wall beside them (the engine's share_of, the reading that is not conserved under the sign's Link phases); the means of Omega over the intervals after the first sixth of the run; and the checks against the blind (`expectation.json`, the world's entry): the share within the named radius at the named interval within its tolerance, the peak Node the centre at every interval where the blind names it, the profile within its tolerance of the lay's at every radius through the run, Omega within its tolerance at the named radii, the node plane at 0 and the peak on the x axis at the named |x| where the blind names them, the peak level's band beside the lay's. Written to `<world>.reading.json`; every number the look's, the script summing and comparing and inventing none.

python examples/events/atom/read_look.py examples/events/atom/atom.look.json [--expectation expectation.json] [--standing atom.standing.json]
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

ALONG = tuple(range(9))  # the Nodes r = 0..8 along +x from the centre the rotation is read at


def array_of(value: Any, shape: tuple[int, int, int]) -> np.ndarray:
    """A frame's array, dense nested lists or the nonzero Nodes alone, as a dense array over the frame's shape."""
    out = np.zeros(int(np.prod(shape)), dtype=np.float64)
    if value is None:
        return out.reshape(shape)
    if isinstance(value, dict):
        out[np.asarray(value["at"], dtype=np.int64)] = np.asarray(value["values"], dtype=np.float64)
        return out.reshape(shape)
    return np.asarray(value, dtype=np.float64).reshape(shape)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("look", type=Path, help="the look file")
    parser.add_argument(
        "--expectation", type=Path, default=Path(__file__).resolve().parent / "expectation.json"
    )
    parser.add_argument("--record", default="electron", help="the record's family")
    parser.add_argument(
        "--standing",
        type=Path,
        default=None,
        help="the tool's readings beside the world (<world>.standing.json), the well along +x",
    )
    parser.add_argument(
        "--out", type=Path, default=None, help="the reading's file (<world>.reading.json)"
    )
    args = parser.parse_args(argv)
    look = json.loads(args.look.read_text(encoding="utf-8"))
    stem = str(look["world"]).rsplit(".", 1)[0]
    shape = tuple(int(v) for v in look["shape"])
    gamma = int(look["node_clock"])
    centre = tuple(int(v) for v in look["bodies"][0]["nodes"][0])  # the proton's Node
    wall = next(int(f["wall"]) for f in look["families"] if f["name"] == args.record)
    expectation = (
        json.loads(args.expectation.read_text(encoding="utf-8")) if args.expectation.exists() else {}
    )
    radii = [int(v) for v in (expectation.get("radii", {}).get(stem) or (1, 2, 3, 4, 6, 8, 10))]
    blind = (expectation.get("worlds") or {}).get(stem, {})
    grids = np.meshgrid(*(np.arange(e) - c for e, c in zip(shape, centre, strict=True)), indexing="ij")
    radius = np.sqrt(sum(g.astype(float) ** 2 for g in grids))
    frames = look["frames"]
    after = max(
        1, (len(frames) - 1) // 6
    )  # the rotation's mean over the intervals after the first sixth
    # the well along +x from the tool's readings: h_i the holder's row the proton sources, U_i = -k_r h_i / Gamma
    standing_path = args.standing or args.look.with_name(
        args.look.name.replace(".look.json", ".standing.json")
    )
    tool = json.loads(standing_path.read_text(encoding="utf-8"))
    h_along = [int(v) for v in tool["well_along_axis"]][: len(ALONG)]
    along = [tuple(c + (d if axis == 0 else 0) for axis, c in enumerate(centre)) for d in ALONG]
    well = np.zeros(shape, dtype=np.float64)
    for node, value in zip(along, h_along, strict=True):
        well[node] = -int(tool["k_r"]) * value / gamma
    every_two = list(range(0, shape[0] // 2 + 1, 2))
    rows: list[dict[str, Any]] = []
    previous = None
    for frame in frames:
        row = frame["families"][args.record]
        z = array_of(row["now"], shape) + 1j * array_of(row["second"], shape)
        q = np.abs(z) ** 2
        total = float(q.sum())
        peak = np.unravel_index(int(np.argmax(q)), shape)
        rates: list[float | None] = []
        if previous is not None:
            for node in along:
                if z[node] != 0 and previous[node] != 0:
                    rates.append(float(-np.angle(z[node] / previous[node]) - well[node]))
                else:
                    rates.append(None)
        rows.append(
            {
                "interval": int(frame["interval"]),
                "Q": total,
                "profile": [float(q[radius <= r].sum()) / total for r in radii],
                "size_along_x": [
                    math.sqrt(float(q[centre[0] + d, centre[1], centre[2]])) for d in every_two
                ],
                "node_plane_share": float(q[centre[0], :, :].sum()) / total,
                "peak_node": [int(v) for v in peak],
                "peak_level": math.sqrt(float(q.max())),
                "centre_level": math.sqrt(float(q[centre])),
                "share_over_wall": (None if row.get("share") is None else row["share"] / wall),
                "Omega_along_x": rates,
            }
        )
        previous = z
    q0 = rows[0]["Q"]
    means: list[float | None] = []
    for k in range(len(ALONG)):
        values = [
            r["Omega_along_x"][k]
            for r in rows
            if r["interval"] > after and r["Omega_along_x"] and r["Omega_along_x"][k] is not None
        ]
        means.append(float(np.mean(values)) if values else None)
    checks: dict[str, Any] = {}
    if "share" in blind:
        at, r_at = int(blind["read_at_interval"]), int(blind["share_within_r"])
        read_at = next(r for r in rows if r["interval"] == at)
        read = read_at["profile"][radii.index(r_at)]
        checks["share_within_r_at_interval"] = {
            "r": r_at,
            "interval": at,
            "read": read,
            "blind": blind["share"],
            "tolerance": blind["tolerance"],
            "pass": abs(read - blind["share"]) <= blind["tolerance"],
        }
    if "peak_node" in blind:
        want = [int(v) for v in blind["peak_node"]]
        misses = [r["interval"] for r in rows if r["peak_node"] != want]
        checks["peak_node_at_every_interval"] = {"blind": want, "pass": not misses, "misses": misses}
    if "profile_at_the_lay" in blind and "profile_tolerance" in blind:
        lay_profile = [float(v) for v in blind["profile_at_the_lay"]]
        worst = max(abs(r["profile"][i] - lay_profile[i]) for r in rows for i in range(len(lay_profile)))
        checks["profile_within_tolerance_of_the_lay"] = {
            "radii": radii[: len(lay_profile)],
            "worst_deviation": worst,
            "tolerance": blind["profile_tolerance"],
            "pass": worst <= blind["profile_tolerance"],
        }
    if "profile_at_the_lay" in blind and "absolute_share_in_units_of_Q0_within" in blind:
        # the moved blind (2026-10-19): the absolute share within each radius in units of the lay's Q_0, profile x Q / Q_0, against the lay's, up to the named radius; the total Q within the walk's budget
        lay_profile = [float(v) for v in blind["profile_at_the_lay"]]
        up_to = int(blind["absolute_share_radii_up_to"])
        tolerance = float(blind["absolute_share_in_units_of_Q0_within"])
        worst_per_radius = {}
        for i, r_i in enumerate(radii[: len(lay_profile)]):
            if r_i > up_to:
                continue
            deviations = [
                (abs(r["profile"][i] * r["Q"] / q0 - lay_profile[i]), r["interval"]) for r in rows
            ]
            worst_per_radius[str(r_i)] = max(deviations)
        worst = max(v[0] for v in worst_per_radius.values())
        checks["absolute_share_in_units_of_Q0_within_tolerance"] = {
            "radii_up_to": up_to,
            "worst_deviation_and_interval_per_radius": worst_per_radius,
            "worst_deviation": worst,
            "tolerance": tolerance,
            "pass": worst <= tolerance,
        }
        budget = blind.get("Q_budget", {})
        one_signed, either = (
            float(budget.get("one_signed_over_120", 0)) * (len(rows) - 1) / 120,
            float(budget.get("either_sign", 0)),
        )
        at_end = rows[-1]["Q"] / q0
        checks["Q_within_the_walks_budget"] = {
            "Q_over_Q0_at_end": at_end,
            "least": 1 - either,
            "most": 1 + one_signed + either,
            "pass": 1 - either <= at_end <= 1 + one_signed + either,
        }
    if "Omega" in blind:
        at_r = [int(v) for v in blind["Omega_read_at_r"]]
        read = [means[k] for k in at_r]
        checks["Omega_at_r"] = {
            "r": at_r,
            "read": read,
            "blind": blind["Omega"],
            "tolerance": blind["Omega_tolerance"],
            "pass": all(
                v is not None and abs(v - blind["Omega"]) <= blind["Omega_tolerance"] for v in read
            ),
        }
    if "node_plane" in blind:
        worst = max(r["node_plane_share"] for r in rows)
        checks["node_plane_share"] = {
            "largest_over_the_run": worst,
            "blind": blind["node_plane"],
            "pass": worst == float(blind["node_plane"]),
        }
    if "peak_on_axis_x_at" in blind:
        allowed = {int(v) for v in blind["peak_on_axis_x_at"]}
        misses = [
            r["interval"]
            for r in rows
            if not (
                abs(r["peak_node"][0] - centre[0]) in allowed
                and r["peak_node"][1] == centre[1]
                and r["peak_node"][2] == centre[2]
            )
        ]
        checks["peak_on_the_x_axis_at"] = {
            "abs_x": sorted(allowed),
            "pass": not misses,
            "misses": misses,
            "peak_nodes": sorted({tuple(r["peak_node"]) for r in rows}),
        }
    if "peak_level_at_the_lay" in blind:
        levels = [r["peak_level"] for r in rows]
        checks["peak_level_band"] = {
            "lay": blind["peak_level_at_the_lay"],
            "read_least": min(levels),
            "read_most": max(levels),
            "at_interval_1": levels[1] if len(levels) > 1 else None,
            "largest_relative_deviation": max(abs(v - blind["peak_level_at_the_lay"]) for v in levels)
            / blind["peak_level_at_the_lay"],
        }
    marks = sorted({0, 1, after, 20, 40, 60, 80, 100, 120} & {r["interval"] for r in rows})
    reading = {
        "label": "lattice reading",
        "world": look["world"],
        "verdict": look["verdict"],
        "intervals": look["intervals"],
        "centre": list(centre),
        "radii": radii,
        "well_along_x": h_along,
        "U_along_x": [float(well[node]) for node in along],
        "Omega_mean_after": after,
        "Omega_mean_along_x": means,
        "Q_over_Q0": {str(t): rows[t]["Q"] / q0 for t in marks},
        "profile_at": {str(t): [round(v, 4) for v in rows[t]["profile"]] for t in marks},
        "size_along_x_at": {str(t): [round(v, 1) for v in rows[t]["size_along_x"]] for t in marks},
        "node_plane_share_at": {str(t): rows[t]["node_plane_share"] for t in marks},
        "peak_at": {str(t): [rows[t]["peak_node"], round(rows[t]["peak_level"], 1)] for t in marks},
        "centre_level_at": {str(t): round(rows[t]["centre_level"], 1) for t in marks},
        "share_over_wall_at": {str(t): rows[t]["share_over_wall"] for t in marks},
        "share_over_wall_relative_to_0": {
            str(t): (
                None
                if rows[t]["share_over_wall"] is None or rows[0]["share_over_wall"] is None
                else rows[t]["share_over_wall"] / rows[0]["share_over_wall"]
            )
            for t in marks
        },
        "checks": checks,
        "per_interval": rows,
    }
    target = args.out or args.look.with_name(args.look.name.replace(".look.json", ".reading.json"))
    target.write_text(json.dumps(reading, indent=1) + "\n", encoding="utf-8")
    summary = {
        k: reading[k]
        for k in (
            "world",
            "verdict",
            "intervals",
            "Omega_mean_along_x",
            "Q_over_Q0",
            "profile_at",
            "peak_at",
            "centre_level_at",
            "node_plane_share_at",
            "share_over_wall_relative_to_0",
        )
    }
    summary["checks"] = {k: (v.get("pass") if "pass" in v else v) for k, v in checks.items()}
    print(json.dumps(summary, default=str))


if __name__ == "__main__":
    main()
