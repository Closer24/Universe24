"""Every integer the paper states about the run is read from the run's data and checked in arrow.tex: the board's shape, the ticks, the click's tick and Nodes, the detectors' Nodes, the counting stretch, the toss's starting number, the coupling, the light's place, the shares at the first close, the shells, the wiped Nodes, the record's values, the rewriting lines, the first wrong Node and the first wrong sets, and the clocks' four counts from run_clocks.json. Each must appear in Section 4, the run, and nowhere else (the owner's order: the run's numbers in Section 4 alone; the Abstract, the click and the Conclusion in formulas), and no integer of an older run may remain. Usage: python3 check_numbers.py <run directory> (with report_e3.json, figure_data.json, the world file and shares_diagnostic.json)."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import abstract_of, plain, read_tex, sections_of


def load(run_dir: Path) -> dict:
    """The run's facts from its report (report_e4.json, or report_e3.json for the earlier run) and figure_data.json."""
    rep_file = run_dir / "report_e4.json" if (run_dir / "report_e4.json").exists() else run_dir / "report_e3.json"
    report = json.load(open(rep_file))
    figure = json.load(open(run_dir / "figure_data.json"))
    world = report["world"]
    shape = world["shape"]
    bodies = world["bodies"]
    detectors = [[n["node"] for n in b["nodes"]] for b in bodies]
    coupling = sorted({t["weight"] for b in bodies for t in b["transitions"]})
    stretch = sorted({b["node_detector"]["window"] for b in bodies})
    seed = sorted({b["node_detector"]["seed"] for b in bodies})
    packets = world["packets"]
    light_x = sorted({p["top"]["x"][0] for p in packets})
    light_yz = sorted({(p["top"]["y"][1] - p["top"]["y"][0] + 1) for p in packets} | {(p["top"]["z"][1] - p["top"]["z"][0] + 1) for p in packets})
    iv = report["iv_two_detectors"]
    shells_rows = report.get("a_erased_nodes_per_shell") or report["erased_nodes_per_shell"]
    shells = [row[2] for row in shells_rows]
    wrong = report["iii_b_no_faces_lays_crossed"]
    faces = report.get("b_faces") or report["faces_in_books"]
    facts = {
        "shape": shape,
        "nodes": shape[0] * shape[1] * shape[2],
        "fixed": not world.get("receding"),
        "ticks": world["intervals"],
        "stretch": stretch,
        "seed": seed,
        "coupling": coupling,
        "detectors": detectors,
        "light_x": light_x,
        "light_across": light_yz,
        "click_tick": iv["click_tick"],
        "click_node": iv["hole_nodes_file_coordinates"][0],
        "shell_counts_first_nine": shells[:9],
        "shells": len(shells),
        "wiped_nodes": report.get("a_erased_nodes_total_to_end", report.get("erased_nodes_total")),
        "record_values": faces["count"],
        "record_nonzero": faces.get("nonzero_value_count"),
        "record_written": faces.get("count_keyed_to_%d" % world["intervals"]),
        "nodes_touched": faces.get("distinct_nodes"),
        "nodes_nonzero": faces.get("nodes_with_at_least_one_nonzero_wiped_value"),
        "largest_value": faces.get("largest_abs_value"),
        "lay_lines": iv["lay_lines"]["count"],
        "first_wrong_tick": wrong["first_mismatch"][0],
        "first_wrong_count": wrong["rows_first3"][0][2],
        "wrong_sets_first_three": [row[2] for row in wrong["rows_first3"]],
        "wrong_at_tick_0": (report["iii_no_books"].get("g_wrong_at_tick_0") or [None, None, None])[2],
        "back_to": wrong["back_to"],
        "second_click": iv["second_click"],
        "twist": ((iv.get("credit_lines") or [{}])[0].get("twist") or [None])[0],
        "piece_momentum": [int(p) for p in ((iv.get("credit_lines") or [{}])[0].get("momentum") or [])],
        "resonance": (world["bodies"][0].get("transitions") or [{}])[0].get("resonance", [None])[0],
        "resonance_den": (world["bodies"][0].get("transitions") or [{}])[0].get("resonance", [None, None])[1],
        "twin_first_difference_tick": report["i_twin"]["first_difference"][0],
    }
    closes = iv.get("c_closes")
    if closes:
        sh = {t: [closes[t]["shares"][k]["share_over_unit"][0] for k in sorted(closes[t]["shares"]) if k.startswith("body") and closes[t]["shares"][k]["share_over_unit"]] for t in closes}
        facts["shares_first_close"] = sh[str(stretch[0])]
        facts["shares_second_close"] = sh[str(2 * stretch[0])]
        # the paper's no-click weight is the draw's rule: what is left of one piece after the earlier closes' shares, less the shares now, never below zero (0.811 at tick 48 = 1 - 0.080 - 0.109); the report's field no_click_weight_over_unit_as_engine (0.621) is another bookkeeping of the engine and is not the number the draw used
        facts["no_click_first_close"] = round(1 - sum(sh[str(stretch[0])]), 3)
        a2, b2 = sh[str(2 * stretch[0])]
        facts["chance_of_the_taker"] = round(max(a2, b2) / (a2 + b2), 2)
    else:
        shares_file = run_dir / "shares_diagnostic.json"
        if shares_file.exists():
            shx = json.load(open(shares_file))
            first = str(stretch[0])
            facts["shares_first_close"] = [shx["closes"][k]["share_over_unit"][0] for k in sorted(shx["closes"]) if k.startswith(first + " body")]
    return facts


# the run's numbers, allowed in Section 4 alone
RUN_ONLY = ["9,279", "18,560", "18,176", "16,111", "13,673", "0.536", "0.678", "0.558", "0.811", "0.080", "0.109", "722.5", "803.0", "147.5", "160.5", "60 and 8", "6, 18, 38", "25,600", "400 by 8 by 8", "172 ticks", "tick 96", "tick 171", "tick 48", "(223, 4, 4)", "(175, 4, 4)", "0.56", "9,424", "31,560", "33,812", "2,252", "34,349", "13,418", "174 runs", "226", "0.435", "0.565", "0.025", "0.438", "0.562", "324 clicks", "182", "326 runs", "0.815", "0.019", "0.812", "0.658", "0.024", "1.21", "0.81 left", "83 ticks", "4,280", "3,480", "872 at tick 172", "26,406", "46,774", "14,842", "263 of 400", "384 named", "39,272", "37,952", "38,584", "36,640", "5,154", "2,936", "5,414", "4,096", "2,168", "1,400", "0.80 of", "0.86 of", "1,124", "1,312", "9.1 \\times 10^6", "1.0 \\times 10^7", "1.0 \\times 10^6"]
# nature's numbers of Section 5's tick bound (the measurement's scale and what follows from it), not this board's: allowed outside Section 4
NATURE_NUMBERS = ["3.8 \\times 10^{-16}", "6.3 \\times 10^{10}", "1.3 \\times 10^{11}", "1.24 \\times 10^{-18}", "1.3 \\times 10^{-26}", "1.1 \\times 10^{-25}", "10^{-25}", "2.6 \\times 10^{-35}", "2.2 \\times 10^{-34}", "2 \\times 10^{-34}", "1.24 \\times 10^{20}", "1.8 \\times 10^{-13}", "5 \\times 10^{-16}", "2 \\times 10^{-16}", "3 \\times 10^{-17}", "10^{-17}", "2 \\times 10^{-15}", "10^{-15}", "6.9 \\times 10^{11}", "2 \\times 10^{-36}", "64^\\circ", "71^\\circ", "130^\\circ", "180^\\circ", "2 \\times 10^{-26}", "10^{-26}", "3 \\times 10^{-27}", "4 \\times 10^{-27}", "6 \\times 10^{25}", "6 \\times 10^{-20}", "2 \\times 10^{-20}", "10^{-20}"]
# this board's example numbers, allowed in Section 4 alone (the owner: Sections 2 and 5 in symbols and generic statements; a specific board's numbers only in the run)
EXAMPLE_ONLY = ["6,000", "5,429", "0.900", "0.905", "1.06", "an eighth", "0.1967", "0.1965", "0.916", "0.251", "0.50", "the pair 2 and 3", "the pair 1 and 1", "n = 600", "216,000,000", "72,000,000", "648,000,000", "144,000,000", "4,912", "96,510,976", "363,245,652", "864,000,000", "0.818", "0.819"]


def half_up(x: float) -> str:
    """A frequency to three places, a half rounded up (263/400 = 0.6575 prints as 0.658)."""
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(str(x)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def normalise(text: str) -> str:
    """Thousands commas removed inside numbers, so 8,127 reads 8127; the Node brackets kept."""
    return re.sub(r"(?<=\d),(?=\d{3}\b)", "", text)


def has(text: str, token: str) -> bool:
    return re.search(r"(?<![\d.])" + re.escape(token) + r"(?![\d])", text) is not None


def node_text(node: list[int]) -> str:
    return "(" + ", ".join(str(v) for v in node) + ")"


def expectations(f: dict) -> list[tuple[str, str, set[str]]]:
    """(what, the token to find, the parts it must appear in): A the Abstract, R the run section, C the Conclusion, K the click section."""
    e = []
    e.append(("the board's shape", f"{f['shape'][0]} by {f['shape'][1]} by {f['shape'][2]}", {"R"}))
    e.append(("the board's Nodes", str(f["nodes"]), {"R"}))
    e.append(("the ticks", str(f["ticks"]), {"R"}))
    e.append(("the counting stretch", str(f["stretch"][0]), {"R"}))
    e.append(("the toss's seed", str(f["seed"][0]), {"R"}))
    e.append(("the strength", str(f["coupling"][0]), {"R"}))
    for det in f["detectors"]:
        for node in det:
            e.append(("a detector's Node", node_text(node), {"R"}))
    e.append(("the click's tick", f"tick {f['click_tick']}", {"R"}))
    e.append(("the click's Node", node_text(f["click_node"]), {"R"}))
    if f.get("twist"):
        e.append(("the taker's turn, the angle 1/q_0 taken so many times", f"taken {f['twist']:,} times", {"R"}))
    for p in f.get("piece_momentum", []):
        e.append(("the piece's momentum per axis", f"{abs(p):,}", {"R"}))
    if f.get("gained"):
        e.append(("the momentum written into the taker", f"written {f['gained']:,}", {"R"}))
        e.append(("what the quarter swing could not hold", f"held back {f['short']:,} more", {"R"}))
    if f.get("halves"):
        h96, h0, o96, o0, lt120, tw120 = f["halves"]
        for what, token in (("the taken half alone at tick 96", f"carried {h96:,} at tick 96"), ("at the start", f"({h0:,} at the start)"), ("the other half alone", f"{-o96:,}"), ("the other half at the start", f"{-o0:,}"), ("light and taker at tick 120", f"together {lt120:,} against {tw120:,} without a click")):
            e.append((what, token, {"R"}))
        e.append(("the references' scale", f"M = {f['scale']:,}", {"R"}))
        e.append(("the resonance's cosine", f"{f['resonance']:,}/{f['resonance_den']:,}", {"R"}))
    if f.get("cross"):
        cr, drift, frac, frac_read, fan_y, fan_z, halves_sum0 = f["cross"]
        for what, token in (("the halves' cross terms", f"their cross terms, {cr:,}, add"), ("the remainder's drift at the click", f"about {round(drift, -2):,}, is the remainder's drift"), ("the taker over its half", f"{frac:.2f} of its half's momentum"), ("the two-Node reading over the half", f"{frac_read:.2f} of its half's momentum"), ("the whole light across the tube", f"carried {fan_y:,} and {fan_z} across the tube"), ("the halves' sum at the start", f"not their sum {halves_sum0:,}")):
            e.append((what, token, {"R"}))
    if f.get("board_sums"):
        s0, s96, s120, s172, twin172, both172, fan0 = f["board_sums"]
        for what, token in (("the light's sum at tick 96", f"{s96:,} at tick 96"), ("at tick 0", f"{s0:,} at tick 0"), ("without a click at tick 172", f"{twin172:,} at tick 172 without a click"), ("at tick 120 with the click", f"the light stood at {s120:,}"), ("at the run's end", f"stood at {s172:,}"), ("light and atoms together at the end", f"{-both172:,} against {fan0:,} before")):
            e.append((what, token, {"R"}))
    for what, token in f.get("ensemble", []):
        e.append((what, token, {"R"}))
    e.append(("the wiped Nodes", str(f["wiped_nodes"]), {"R"}))
    e.append(("the record's named values", str(f["record_values"]), {"R"}))
    if f.get("record_written"):
        e.append(("the record's written values", str(f["record_written"]), {"R"}))
    if f.get("record_nonzero"):
        e.append(("the record's nonzero values", str(f["record_nonzero"]), {"R"}))
    e.append(("the first wrong tick", f"tick {f['first_wrong_tick']}", {"R"}))
    if f.get("wrong_at_tick_0"):
        e.append(("the wrong Nodes at tick 0", f"{f['wrong_at_tick_0']} of the {f['nodes']} Nodes", {"R"}))
    e.append(("the backward run's end", f"{f['first_wrong_tick']} down to {f['back_to']}", {"R"}))
    e.append(("the twin's first difference", f"tick {f['twin_first_difference_tick']}", {"R"}))
    if "shares_first_close" in f:
        e.append(("the shares at the first close", " and ".join(f"{x:.3f}" for x in f["shares_first_close"]), {"R"}))
    if "shares_second_close" in f:
        e.append(("the shares at the second close", " and ".join(f"{x:.3f}" for x in f["shares_second_close"]), {"R"}))
        e.append(("no click at the first close", f"{f['no_click_first_close']:.3f}", {"R"}))
        e.append(("the taker's chance", f"{f['chance_of_the_taker']:.2f}", {"R"}))
    return e


def main(argv: list[str]) -> int:
    run_dir = Path(argv[1]) if len(argv) > 1 else Path(".")
    f = load(run_dir)
    tex = read_tex()
    secs = sections_of(tex)
    parts = {
        "A": normalise(plain(abstract_of(tex))),
        "R": normalise(plain(secs["The run"])),
        "C": normalise(plain(secs["Conclusion"])),
        "K": normalise(plain(secs["The click"])),
    }
    problems_outside = []
    names = {"A": "the Abstract", "R": "Section 4 (the run)", "C": "the Conclusion", "K": "Section 3 (the click)", "T": "Section 5 (time)"}
    parts["T"] = normalise(plain(secs["What time is on the board"]))
    # the run's numbers belong to Section 4 alone (the owner's order): nowhere else in the paper, the Abstract and the captions included
    outside = normalise(plain(tex.replace(secs["The run"], " ")))
    for token in RUN_ONLY:
        if has(outside, normalise(token)):
            problems_outside.append(token)
    for token in EXAMPLE_ONLY:
        if has(outside, normalise(token)):
            problems_outside.append(token + " (this board's number outside Section 4)")
    problems = []
    # every file run_e4.py reads or writes must be in the committed folder: the world, its mode file and design.json beside it, and its outputs
    script = run_dir / "run_e4.py"
    needed = {"one_piece_3d_fixed.json", "one_piece_3d_fixed.mode.json", "design.json", "run_e4.py"}
    if script.exists():
        needed |= set(re.findall(r'OUT / "([^"]+)"', script.read_text(encoding="utf-8")))
    missing = sorted(n for n in needed if not (run_dir / n).exists())
    print(f"  the run's folder holds {len(needed) - len(missing)} of the {len(needed)} files run_e4.py reads or writes")
    if missing:
        problems.append("missing from the run's folder: " + ", ".join(missing))
    clocks_file = Path(__file__).resolve().parent.parent / "run_clocks.json"
    if clocks_file.exists():
        rc = json.load(open(clocks_file))
        f["clock_swings_rest"] = [rc["rest"]["content_0"]["swings"], rc["rest"]["content_600"]["swings"], rc["rest"]["ticks"]]
        f["clock_swings_moving"] = [rc["moving"]["swings_moving"], rc["moving"]["swings_rest"], rc["moving"]["ticks"], rc["moving"]["row"]]
        for what, big, token in (("the rest Node's largest number", rc["rest"]["content_0"]["largest_number"], "1.0 \\times 10^6"), ("the moving row's largest number", rc["moving"]["largest_number"], "9.1 \\times 10^6"), ("the light row's largest number", rc["light"]["content_600"]["largest_number"], "1.0 \\times 10^7")):
            mant, expo = f"{big:.1e}".split("e")
            if f"{mant} \\times 10^{int(expo)}" != token or f"${token}$" not in secs["The run"]:
                problems.append(f"{what}: {big} is not printed as {token} in Section 4")
        for what, token in (("the swings at rest, content 600", f"{rc['rest']['content_600']['swings']} swings in {rc['rest']['ticks']} ticks"), ("the swings at rest, content 0", f"against {rc['rest']['content_0']['swings']} at none"), ("the moving middle's swings", f"{rc['moving']['swings_moving']} swings in {rc['moving']['ticks']} ticks against {rc['moving']['swings_rest']} at rest"), ("the row", f"row of {rc['moving']['row']} Nodes")):
            if not has(parts["R"], normalise(token)):
                problems.append(f"{what}: '{token}' not found in {names['R']}")
    else:
        problems.append("run_clocks.json is missing (tools/run_clocks.py writes it)")
    momentum_file = Path(__file__).resolve().parent.parent / "run_momentum.json"
    if momentum_file.exists():
        rm = json.load(open(momentum_file))
        f["gained"], f["short"] = rm["gained_along_board"], rm["short_of_the_piece"]
        f["board_sums"] = [rm["light_along_board"]["0"], rm["light_along_board"]["96"], rm["light_along_board"]["120"], rm["light_along_board"]["172"], rm["twin_light_along_board"]["172"], rm["light_and_atoms_along_board_at_end"], rm["fan"][0]]
        hv = rm["halves_alone_along_board"]
        f["halves"] = [hv[rm["taken_half"]]["96"], hv[rm["taken_half"]]["0"], hv[[k for k in hv if k != rm["taken_half"]][0]]["96"], hv[[k for k in hv if k != rm["taken_half"]][0]]["0"], rm["light_and_taker_at_120"], rm["twin_light_along_board"]["120"]]
        f["scale"] = rm["reference_scale"]
        f["cross"] = [rm["cross_terms_at_start"], rm["gap_at_click_tick"] - rm["cross_terms_at_start"], round(rm["taker_along_board"] / hv[rm["taken_half"]]["96"], 2), round(abs(rm["piece_momentum_read_at_the_taker"][0]) / hv[rm["taken_half"]]["96"], 2), rm["fan"][1], rm["fan"][2], sum(h["0"] for h in hv.values())]
        if rm["light_along_board"]["96"] != rm["fan"][0] or rm["taker_along_board"] != rm["gained_along_board"]:
            problems.append("run_momentum.json: the light's sum at the click's tick is not the credit line's fan, or the taker's lines do not sum to what the twist gained")
        if rm["twist"][0] != f.get("twist") or rm["piece_momentum_read_at_the_taker"] != f.get("piece_momentum") or rm["quarter_turn_acts"] != rm["twist"][0]:
            problems.append("run_momentum.json disagrees with the report's credit line (the twist, the piece's momentum) or the twist is not the quarter turn")
    else:
        problems.append("run_momentum.json is missing (tools/run_momentum.py writes it)")
    ensemble_file = run_dir / "ensemble" / "summary.json"
    if ensemble_file.exists():
        es = json.load(open(ensemble_file))["summary"]
        both, alone_a, alone_b = es["both"], es["A"], es["B"]
        n = both["seeds"]
        at96 = both["clicks_by_detector_and_tick"]
        pw = both["prediction_from_the_weights"]
        f["ensemble"] = [("the seeds", f"1 to {n}"), ("the near detector's clicks, both present", f"in {both['A_clicks']} runs"), ("the far detector's clicks, both present", f"in {both['B_clicks']}"),
                         ("the near frequency", half_up(both["A_frequency"][0])), ("the far frequency", half_up(both["B_frequency"][0])), ("the frequencies' uncertainty", half_up(both["A_frequency"][1])),
                         ("the chained chances", f"{pw['predicted']['A']:.3f} and {pw['predicted']['B']:.3f}"),
                         ("the clicks at tick 96", f"{at96['A at 96'] + at96['B at 96']} clicks at tick 96, {at96['B at 96']} were"), ("the far share at tick 96", f"{at96['B at 96'] / (at96['A at 96'] + at96['B at 96']):.3f}"),
                         ("the far detector alone", f"in {alone_b['B_clicks']} runs of {alone_b['seeds']}"), ("the far detector alone, its frequency", half_up(alone_b["B_frequency"][0])), ("its uncertainty", half_up(alone_b["B_frequency"][1])), ("the far detector alone, chained", f"{alone_b['prediction_from_the_weights']['predicted']['B']:.3f} by"),
                         ("the near detector alone", half_up(alone_a["A_frequency"][0])), ("the near detector alone, its uncertainty", half_up(alone_a["A_frequency"][1])), ("the near detector alone, chained", f"{alone_a['prediction_from_the_weights']['predicted']['A']:.3f} by the same"),
                         ("the two weights at tick 96 together", f"{sum(pw['weights_read']['96'].values()):.2f}, exceed the {pw['chain']['96']['reached_with_no_click']:.2f} left")]
        if both["two_clicks_in_one_run"] or both["no_click"]:
            problems.append("the ensemble with both detectors had a run with two clicks or with none; the paper says neither happened")
    else:
        problems.append("run3d_fixed/ensemble/summary.json is missing")
    if problems_outside:
        problems.append("a run number outside Section 4: " + ", ".join(problems_outside))
    print(f"  run numbers outside Section 4: {len(problems_outside)}")
    for what, token, where in expectations(f):
        token_n = normalise(token)
        for p in sorted(where):
            if not has(parts[p], token_n):
                problems.append(f"{what}: '{token}' not found in {names[p]}")
    if f["second_click"]:
        problems.append("the data show a second click; the paper says none came")
    if f["fixed"] and not re.search(r"The board (is|was) fixed", parts["R"]):
        problems.append("the run's board is fixed but section 5 does not say so")
    # no integer of another run: every number of four or more digits in the three parts must be a fact
    allowed = {str(f["wiped_nodes"]), str(f["record_values"]), str(f["record_values"] - 2), str(f.get("record_nonzero")), str(f.get("record_written")), str(f.get("nodes_touched")), str(f.get("nodes_nonzero")), str(f["nodes"]), str(f.get("wrong_at_tick_0")), "6000", "5429", "1299", "72000000", "216000000", "144000000", "648000000", "864000000", "1728000000", "1080000000", "432000000", "48255488", "142467072", "1836", str(f.get("twist"))} | {str(abs(p)) for p in f.get("piece_momentum", [])} | {str(f.get("gained")), str(f.get("short"))} | {str(abs(x)) for x in f.get("board_sums", [])} | {str(abs(x)) for x in f.get("halves", [])} | {str(f.get("resonance")), str(f.get("scale"))} | {str(abs(x)) for x in f.get("cross", []) if isinstance(x, int)} | ({str(int(round(f["cross"][1], -2)))} if f.get("cross") else set()) | {str(rc["rest"]["ticks"]), str(rc["moving"]["ticks"])} if clocks_file.exists() else set()
    for p in ("A", "R", "C"):
        for m in re.findall(r"(?<![\d.])\d{4,}(?![\d])", parts[p]):
            if m not in allowed and not (1800 <= int(m) <= 2100):
                problems.append(f"a number not of this run in {names[p]}: {m}")
    # the same value everywhere: the wiped Nodes and the record's values stated nowhere with another figure
    for what, val, alt in (("wiped Nodes", f["wiped_nodes"], r"(\d{3,}) (?:wiped )?Nodes wiped|(\d{3,}) wiped Nodes"), ("record's written values", f.get("record_written") or f["record_values"], r"(\d{3,}) whole numbers overwritten"), ("record's named values", f["record_values"], r"(\d{3,}) values, two per Node")):
        for p in ("A", "R", "C"):
            for m in re.finditer(alt, parts[p]):
                num = next(g for g in m.groups() if g)
                if int(num) != val:
                    problems.append(f"{what} stated as {num} in {names[p]}, the data say {val}")
    print(f"check_numbers: the run at {run_dir}; {len(expectations(f)) + 4} facts checked")
    for k, v in f.items():
        print(f"  {k}: {v}")
    if problems:
        print("MISMATCHES:")
        for pr in problems:
            print("  " + pr)
        return 1
    print("every integer of the paper matches the run's data, and every run number sits in Section 4 alone")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
