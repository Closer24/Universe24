"""Read the records of experiment A6 (docs/EXPERIMENTS.md) and evaluate its criterion
clause by clause, per form of the coupling (`turn`, the momentum register;
`delay`, the pre-registered delay table): the ray's momentum register at the end
of its pass (from the `ray_push` records and the ray's `spatial_escaped` record),
the deflection alpha = atan2(|transverse|, p_x) in radians, the log-log
least-squares exponent of alpha over the five b with its standard error, the
linearity in M, G_eff(N) = alpha b / (4 M) and its products with N and N^2 over the
N scan, the diagonal passes against the axis fit at equal Euclidean b, the ratio
of the light's alpha to the slow ray's, the control, the ledger, the star's
momentum line, and the mean field's prediction beside every case
(`predictions.json`). A Renderer of records in the sense of Highlights 3.29: it
reads only what the runner wrote (``run.json``, ``events.jsonl``,
``initialization.json``) and never the engine.

Run:  python examples/nature/a6_bending/analyze.py RUN [RUN ...] [--out summary.json] [--record record.json]
where RUN is a run directory (``run.json`` beside ``events.jsonl``) of one world
of ``make_worlds.py``. The per-run lines and the clause table are printed;
``--out`` writes the full summary and ``--record`` the small committed record the
test reads.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDICTIONS = HERE / "predictions.json"
EXPONENT_BAND = (-1.1, -0.9)
LINEARITY_TOLERANCE = 1 / 16
SCALING_TOLERANCE = 1 / 16
DIAGONAL_TOLERANCE = 1 / 8
AXIS_B = (4, 6, 8, 12, 16)
SCAN_B = 8
SCAN_BITS = (8, 10, 12, 14, 16)
BASE_BITS = 12
CUBE_AXIS_B = (4, 6, 8)
CUBE_DIAGONAL_D = (3, 4, 6)


def load(run):
    directory = Path(run)
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    return directory, metadata, world


def case_of(model):
    """`a6-bending-turn-c-d3` -> ('turn', 'c_d3')."""
    tail = model.removeprefix("a6-bending-")
    form, _, rest = tail.partition("-")
    return form, rest.replace("-", "_")


def geometry(world):
    """The star, the launcher, the ray's line, the ray's family and width."""
    bodies = {body["family"]: body for body in world["external_bodies"]}
    star = bodies.get("neutron")
    launcher = bodies["launcher"]
    ray = world["emissions"][0]["field"]
    definitions = {entry["field"]: entry for entry in world["spatial_fields"]}
    launch = next(rule for rule in world["ray_interactions"] if rule["name"] == "launch")
    gravity = next(rule for rule in world["ray_interactions"] if rule["name"] != "launch")
    line = tuple(launcher["position"])
    offset = (0, 0, 0)
    if star is not None:
        offset = (0, line[1] - star["position"][1], line[2] - star["position"][2])
    return {
        "shape": list(world["shape"]),
        "star": None if star is None else list(star["position"]),
        "amount": None if star is None else star["amount"],
        "line": list(line),
        "offset": list(offset),
        "b": math.hypot(offset[1], offset[2]),
        "ray": ray,
        "bits": definitions[ray]["phase_bits"],
        "modulus": 1 << definitions[ray]["phase_bits"],
        "rate": definitions[ray]["kerengonen"]["phase_advance"],
        "light": world["emissions"][0]["amount"],
        "launch_delay": launch["outputs"][0]["delay"],
        "release": definitions["mass_field"]["release"],
        "rule": gravity["name"],
        "table": gravity["outputs"][0]["delay"] if "outputs" in gravity else gravity["momentum_table"],
    }


def alpha_of(register):
    px, py, pz = (float(v) for v in register)
    return math.atan2(math.hypot(py, pz), px)


def analyze(run):
    directory, metadata, world = load(run)
    form, case = case_of(metadata["model"])
    geo = geometry(world)
    ray = geo["ray"]
    pushes = []
    escape = None
    star_series = {}
    meetings_on_line = 0
    cycles_on_line = {}
    line = tuple(geo["line"])
    with (directory / "events.jsonl").open(encoding="utf-8") as stream:
        for text in stream:
            event = json.loads(text)
            kind = event["event"]
            if kind == "ray_push" and event["family"] == ray:
                pushes.append(event)
            elif kind == "spatial_escaped" and ray in event["escaped"]:
                escape = event
            elif kind == "external_body_absorbed" and event["body"] == 0 and geo["star"] is not None:
                star_series[event["tick"]] = list(event["momentum"])
            elif kind == "spatial_cycle" and tuple(event["position"][1:]) == line[1:]:
                x = event["position"][0]
                cycles_on_line.setdefault(x, []).append(event["tick"])
                if event.get("source_delta", {}).get("momentum"):
                    meetings_on_line += 1
    # The ray's register at the end: its escape record's momentum less the field
    # content that left in the same packet (field rays carry amount x heading, +X
    # through Port 0; a field ray carries no register).
    register = None
    straight = None
    escape_tick = None
    if escape is not None:
        momentum = list(escape["escaped"]["momentum"])
        field = escape["escaped"].get("mass_field", [0])[0]
        heading = [1, 0, 0] if escape["port"] == 0 else None
        if heading is not None:
            momentum = [momentum[i] - field * heading[i] for i in range(3)]
        register = momentum
        escape_tick = escape["tick"]
        expected_tick = geo["launch_delay"] + geo["shape"][0] + 1
        straight = (
            escape["port"] == 0
            and list(escape["position"]) == [geo["shape"][0] - 1, line[1], line[2]]
            and escape["tick"] == expected_tick
        )
    push_sum = [0, 0, 0]
    register_series = {}
    for event in pushes:
        for axis in range(3):
            push_sum[axis] += event["after"][axis] - event["before"][axis]
        register_series[event["tick"]] = list(event["after"])
    audit = metadata["audit"]
    star_final = None
    if geo["star"] is not None:
        star_final = metadata["external_bodies"][0]["final"]["momentum"]
    predicted = None
    if PREDICTIONS.is_file():
        predictions = json.loads(PREDICTIONS.read_text(encoding="utf-8"))
        predicted = predictions["cases"].get(case)
    alpha = None if register is None else alpha_of(register)
    result = {
        "run": str(directory),
        "model": metadata["model"],
        "form": form,
        "case": case,
        **geo,
        "status": metadata["status"],
        "error": metadata.get("error"),
        "ticks": metadata["completed_ticks"],
        "elapsed_seconds": metadata["elapsed_seconds"],
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "all_balanced": all(entry["balanced"] for entry in audit),
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "momentum_turn": metadata.get("ray_momentum_turn"),
        "dense": metadata.get("dense_field"),
        "pushes": len(pushes),
        "first_push": None if not pushes else [pushes[0]["tick"], list(pushes[0]["position"])],
        "push_sum": push_sum,
        "register": register,
        "alpha": alpha,
        "escape_tick": escape_tick,
        "escape_position": None if escape is None else list(escape["position"]),
        "straight": straight,
        "meetings_on_line": meetings_on_line,
        "line_nodes_cycled": len(cycles_on_line),
        "star_final_momentum": star_final,
        "star_absorbed": None
        if geo["star"] is None
        else metadata["external_body_totals"]["mass_field"][0],
        "bodies_momentum_line": metadata["external_body_momentum"],
        "star_series": star_series,
        "register_series": register_series,
        "predicted_push": None if predicted is None else predicted["push"],
        "predicted_alpha": None if predicted is None else predicted["alpha"],
        "predicted_steady_alpha": None if predicted is None else predicted.get("steady_alpha"),
    }
    if predicted is not None and register is not None and predicted["push"][1] != 0:
        result["push_ratio"] = (register[1]) / predicted["push"][1]
    else:
        result["push_ratio"] = None
    return result


def fit(points):
    """Least-squares slope of ln alpha over ln b with its standard error; None when
    an alpha is 0 (no logarithm) or fewer than three points remain."""
    usable = [(r, v) for r, v in points if v is not None and v > 0]
    n = len(usable)
    if n < 3 or n != len(points):
        return {
            "exponent": None,
            "standard_error": None,
            "intercept": None,
            "points": n,
            "zeros": len(points) - n,
        }
    xs = [math.log(r) for r, _ in usable]
    ys = [math.log(v) for _, v in usable]
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    slope = sxy / sxx
    intercept = my - slope * mx
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys, strict=True))
    se = math.sqrt(residual / (n - 2) / sxx) if n > 2 else None
    return {"exponent": slope, "standard_error": se, "intercept": intercept, "points": n, "zeros": 0}


def power_law(fitted, r):
    if fitted["exponent"] is None:
        return None
    return math.exp(fitted["intercept"]) * r ** fitted["exponent"]


def beam_fractions(runs):
    """The unscattered beam 8192 (6/11)^(b-1), which meets the ray once at the
    star's x, as a fraction of the mean field's transverse push, per axis case."""
    if not PREDICTIONS.is_file():
        return None
    predictions = json.loads(PREDICTIONS.read_text(encoding="utf-8"))
    result = {}
    for b in AXIS_B:
        row = predictions["cases"].get(f"b{b}")
        if row is None or not row.get("push") or row["push"][1] == 0:
            continue
        result[f"b{b}"] = {"beam": row["beam"], "fraction": row["beam"] / abs(row["push"][1])}
    return result


def clauses(results, form):
    """The criterion of A6 for one form, each clause with its verdict and numbers;
    a clause whose worlds did not run is reported as not run (pass None)."""
    runs = {r["case"]: r for r in results if r["form"] == form}
    table = []

    def alpha(case):
        r = runs.get(case)
        return None if r is None or r["alpha"] is None else r["alpha"]

    # 1. Momentum exact at every tick: every ledger line balanced and conserved.
    table.append(
        {
            "clause": "momentum exact at every tick (ledger balanced, conserved_at_every_completed_tick, the bodies' line)",
            "pass": bool(runs)
            and all(
                r["all_balanced"]
                and r["conserved_at_every_completed_tick"]
                and r["status"] == "completed"
                for r in runs.values()
            ),
            "numbers": {
                case: {
                    "balanced": r["all_balanced"],
                    "conserved": r["conserved_at_every_completed_tick"],
                    "status": r["status"],
                    "bodies_momentum_line": r["bodies_momentum_line"],
                }
                for case, r in runs.items()
            },
        }
    )
    # 2. The control goes straight.
    control = runs.get("control")
    table.append(
        {
            "clause": "control goes straight (no star: the register unchanged, the escape on the line at the straight tick)",
            "pass": None
            if control is None
            else bool(
                control["straight"]
                and control["pushes"] == 0
                and control["register"] == [control["light"], 0, 0]
            ),
            "numbers": None
            if control is None
            else {
                "register": control["register"],
                "escape": control["escape_position"],
                "tick": control["escape_tick"],
                "pushes": control["pushes"],
            },
        }
    )
    # 3. The ray bends toward the body on both sides.
    sides = {}
    for b in AXIS_B:
        for case, sign in ((f"b{b}", -1), (f"m{b}", 1)):
            r = runs.get(case)
            if r is None or r["register"] is None:
                continue
            sides[case] = {
                "register": r["register"],
                "toward": sign * r["register"][1] > 0 and r["register"][2] == 0,
            }
    both = all(f"b{b}" in sides and f"m{b}" in sides for b in AXIS_B)
    table.append(
        {
            "clause": "bends toward the body on both sides (p_y < 0 above the star, > 0 below, p_z = 0)",
            "pass": None if not sides else (all(v["toward"] for v in sides.values()) and both),
            "numbers": {"sides": sides, "both_sides_run": both},
        }
    )
    # 4. The log-log exponent of alpha over the five b.
    points = [(float(b), alpha(f"b{b}")) for b in AXIS_B if f"b{b}" in runs]
    fitted = fit(points) if len(points) == len(AXIS_B) else None
    table.append(
        {
            "clause": f"log-log exponent of alpha over b = {list(AXIS_B)} within {EXPONENT_BAND}",
            "pass": None
            if fitted is None
            else (
                fitted["exponent"] is not None
                and EXPONENT_BAND[0] <= fitted["exponent"] <= EXPONENT_BAND[1]
            ),
            "numbers": {
                "points": points,
                "fit": fitted,
                "predicted_fit": fit(
                    [(float(b), runs[f"b{b}"]["predicted_alpha"]) for b in AXIS_B if f"b{b}" in runs]
                )
                if len(points) == len(AXIS_B)
                else None,
                "beam_fraction": beam_fractions(runs),
            },
        }
    )
    # 5. alpha at 2M is 2 alpha at M within 1/16.
    a_m, a_2m = alpha(f"b{SCAN_B}"), alpha("2m")
    ratio = None if a_m in (None, 0) or a_2m is None else a_2m / a_m
    table.append(
        {
            "clause": f"alpha at 2M equals 2 alpha at M within {LINEARITY_TOLERANCE} relative (b = {SCAN_B})",
            "pass": None
            if ratio is None and ("2m" not in runs or f"b{SCAN_B}" not in runs)
            else (ratio is not None and abs(ratio / 2 - 1) <= LINEARITY_TOLERANCE),
            "numbers": {"alpha_M": a_m, "alpha_2M": a_2m, "ratio": ratio},
        }
    )
    # 6. G_eff(N) N^2 constant over the five N within 1/16 of its value at N = 2^12.
    scan = {}
    for bits in SCAN_BITS:
        case = f"b{SCAN_B}" if bits == BASE_BITS else f"n{bits}"
        r = runs.get(case)
        if r is None or r["alpha"] is None:
            continue
        n = 1 << bits
        g = r["alpha"] * r["b"] / (4 * r["amount"])
        scan[str(bits)] = {
            "N": n,
            "alpha": r["alpha"],
            "register": r["register"],
            "G_eff": g,
            "G_eff_N": g * n,
            "G_eff_N2": g * n * n,
        }
    complete = all(str(bits) in scan for bits in SCAN_BITS)
    base = scan.get(str(BASE_BITS))
    n2_pass = None
    if complete and base is not None and base["G_eff_N2"] > 0:
        n2_pass = all(
            abs(row["G_eff_N2"] / base["G_eff_N2"] - 1) <= SCALING_TOLERANCE for row in scan.values()
        )
    elif complete:
        n2_pass = False
    n1_constant = None
    if complete and base is not None and base["G_eff_N"] > 0:
        n1_constant = all(
            abs(row["G_eff_N"] / base["G_eff_N"] - 1) <= SCALING_TOLERANCE for row in scan.values()
        )
    n0_constant = None
    if complete and base is not None and base["G_eff"] > 0:
        n0_constant = all(
            abs(row["G_eff"] / base["G_eff"] - 1) <= SCALING_TOLERANCE for row in scan.values()
        )
    table.append(
        {
            "clause": f"G_eff(N) N^2 constant over N = 2^{list(SCAN_BITS)} within {SCALING_TOLERANCE} of its value at N = 2^{BASE_BITS} (b = {SCAN_B})",
            "pass": n2_pass,
            "numbers": {"scan": scan, "G_eff_N_constant": n1_constant, "G_eff_constant": n0_constant},
        }
    )
    # 7. The diagonal alpha at equal Euclidean b within 1/8 of the axial (the cube).
    cube_points = [(runs[f"c_b{b}"]["b"], alpha(f"c_b{b}")) for b in CUBE_AXIS_B if f"c_b{b}" in runs]
    cube_fit = fit(cube_points) if len(cube_points) == len(CUBE_AXIS_B) else None
    diagonal = {}
    for d in CUBE_DIAGONAL_D:
        r = runs.get(f"c_d{d}")
        if r is None or r["alpha"] is None or cube_fit is None:
            continue
        axial = power_law(cube_fit, r["b"])
        diagonal[f"c_d{d}"] = {
            "b": r["b"],
            "alpha": r["alpha"],
            "register": r["register"],
            "axis_fit": axial,
            "ratio": None if not axial else r["alpha"] / axial,
        }
    diagonal_pass = None
    if len(diagonal) == len(CUBE_DIAGONAL_D):
        diagonal_pass = all(
            v["ratio"] is not None and abs(v["ratio"] - 1) <= DIAGONAL_TOLERANCE
            for v in diagonal.values()
        )
    table.append(
        {
            "clause": f"diagonal alpha at equal Euclidean b within {DIAGONAL_TOLERANCE} of the axial (the cube's axis fit)",
            "pass": diagonal_pass,
            "numbers": {"cube_axis": cube_points, "cube_fit": cube_fit, "diagonal": diagonal},
        }
    )
    # 8. Reported, not pinned: the light's alpha over the slow ray's, against 2.
    a_slow = alpha("slow")
    table.append(
        {
            "clause": "reported: alpha(light) / alpha(slow ray) at equal b and M, against 2",
            "pass": None,
            "numbers": {
                "alpha_light": a_m,
                "alpha_slow": a_slow,
                "ratio": None if a_slow in (None, 0) or a_m is None else a_m / a_slow,
                "registers": {
                    "light": None if f"b{SCAN_B}" not in runs else runs[f"b{SCAN_B}"]["register"],
                    "slow": None if "slow" not in runs else runs["slow"]["register"],
                },
            },
        }
    )
    # 9. Reported: the engine against the mean field's prediction (the expectation of its integers).
    ratios = {case: r["push_ratio"] for case, r in runs.items() if r["push_ratio"] is not None}
    table.append(
        {
            "clause": "reported: the ray's transverse push over the mean field's prediction, per case",
            "pass": None,
            "numbers": {
                "ratios": ratios,
                "max_deviation": None if not ratios else max(abs(v - 1) for v in ratios.values()),
            },
        }
    )
    return table


def print_run(r):
    print(
        f"== {r['model']}  form={r['form']} case={r['case']} b={r['b']:.3f} offset={r['offset']} shape={r['shape']}"
        f" ray={r['ray']} bits={r['bits']} amount={r['amount']} ticks={r['ticks']} status={r['status']} elapsed={r['elapsed_seconds']:.0f}s"
    )
    print(f"   source {r['source_sha256']}  init {r['initialization_sha256']}")
    print(
        f"   pushes {r['pushes']} first {r['first_push']} sum {r['push_sum']} register {r['register']}"
        f" alpha {None if r['alpha'] is None else round(r['alpha'], 7)} escape {r['escape_position']} at tick {r['escape_tick']} straight {r['straight']}"
    )
    print(
        f"   predicted push {None if r['predicted_push'] is None else [round(v, 1) for v in r['predicted_push']]}"
        f" alpha {None if r['predicted_alpha'] is None else round(r['predicted_alpha'], 7)}"
        f" ratio {None if r['push_ratio'] is None else round(r['push_ratio'], 4)}"
        f" | star final {r['star_final_momentum']} absorbed {r['star_absorbed']} bodies' line {r['bodies_momentum_line']}"
        f" | balanced {r['all_balanced']} conserved {r['conserved_at_every_completed_tick']} meetings on line {r['meetings_on_line']}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    results = [analyze(run) for run in args.runs]
    results.sort(key=lambda r: (r["form"], r["run"]))
    for r in results:
        print_run(r)
    tables = {}
    for form in ("turn", "delay"):
        if not any(r["form"] == form for r in results):
            continue
        table = clauses(results, form)
        tables[form] = table
        print(f"\n== Criterion of A6, clause by clause, the {form} form")
        for entry in table:
            verdict = "----" if entry["pass"] is None else ("PASS" if entry["pass"] else "FAIL")
            print(f"   {verdict}  {entry['clause']}")
            print("         " + json.dumps(entry["numbers"], default=str)[:1500])
    if args.out:
        args.out.write_text(
            json.dumps({"runs": results, "clauses": tables}, indent=1) + "\n", encoding="utf-8"
        )
    if args.record:
        record = {
            "runs": [
                {k: r[k] for k in r if k not in ("star_series", "register_series")} for r in results
            ],
            "clauses": tables,
        }
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
