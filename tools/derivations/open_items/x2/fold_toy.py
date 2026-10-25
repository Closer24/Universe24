"""Hand X2: the toy's functions mapped to their fold target, and the folded toy's line estimate from measured ranges.

The estimate's rule, every number a measured line range of lean_full.py / decoder_full.py (ast end_lineno):
  kept   : a function kept whole at its measured size;
  drop   : a function dropped whole (the inverse written again by hand, a dead helper, a probe of the engine);
  minus  : a function kept less the named line ranges (the switches on os.environ, the modes on link_birth, the
           former clauses kept by name, the credit's frame the decoder re-runs the Node from, the write lines that
           move into write(rows), the detectors' reading that moves into the writer);
  split  : a range of a function counted under another target (named).
Usage: python fold_toy.py toy_functions.json fold_toy.json
"""
import json
import sys
from pathlib import Path

LEAN = "lean/lean_full.py"
DEC = "lean/decoder_full.py"

# function -> (target, rule, drops: list of (start, end) ranges removed, note)
SPEC = {
    "roll": ("PRIM", "kept", [], "the shift through a Port"),
    "gcd_arr": ("OUT", "drop", [], "defined, never called"),
    "Line": ("PRIM", "kept", [], "the line's three integers"),
    "load_world": ("LOADER", "kept", [], "the two files in"),
    "Lean.from_files": ("LOADER", "kept", [], ""),
    "Lean.__init__": ("LOADER", "minus", [(89, 101), (110, 115)],
                      "the state from the rows; the seed's lays (89-101 by the row's kind, 110-115 the plane lays) become calls of lay(row, at, quanta, sense): one loop, counted under CLICK's lay as 3 lines"),
    "Lean.content": ("ROTATE", "kept", [], "the content read c = level_of(X)"),
    "Lean.pair_angle": ("LOADER", "kept", [], "the orbit table of (cos, sin) at the count n: a function of (Gamma, X) alone, derived once"),
    "Lean.tensions": ("WRITE", "minus", [(134, 135)], "the stress parts of every line of quanta; the switch LEAN_FORMER_TENSION and the former reading out"),
    "Lean.link_factors": ("ROTATE", "minus", [(141, 142)], "the Link factor from the two ends' axis lines; the switch LEAN_FLAT_FACTORS out"),
    "Lean.rule": ("ROTATE", "kept", [], "Rule3's integers from the pair and the paces"),
    "Lean.step_line": ("ROTATE", "kept", [], "rotate(row) for a line (the riding line the same with the wall w X as an input, no line added)"),
    "Lean.frames": ("ROTATE", "kept", [], "the frame sign per Port"),
    "Lean.step_plane": ("ROTATE", "kept", [], "rotate(row) for a plane: the two lines with the phase as an input"),
    "Lean.centred_count": ("ROTATE", "kept", [], "K = 2 (Phi_now - Phi_before) + c"),
    "Lean.link_phases": ("ROTATE", "kept", [], "the Link's count and its (cos, sin)"),
    "Lean.share": ("CLICK", "minus", [(210, 212)], "the share at the Node (the read of whole quanta, the lay's refusal, the standing); the switch LEAN_NODE_SHARE out"),
    "Lean.step": ("LOOP", "minus", [(230, 233), (246, 251), (260, 275)],
                  "the interval's order; 230-233 the three switches out; 246-251 the forms, W and J accumulated inside the rotate loop move into write(rows) (counted there as 6); 260-275 the held writes move into write(rows) (counted there as 15, the switch line 270 out)"),
    "Lean.snapshot": ("LOOP", "kept", [], "the start kept for the swap and the close"),
    "Lean.is_im": ("SWAP", "kept", [], "which lines are a plane's im line: becomes the row's shape (2) read, no list by position"),
    "Lean.floor": ("SWAP", "kept", [], "X_f = volume_of(Gamma, -Gamma)"),
    "Lean.write_walls": ("LOADER", "kept", [], "the write walls per line, derived once from den, Gamma, T"),
    "Lean.all_lines": ("LOOP", "kept", [], "the rows list"),
    "Lean.swap": ("SWAP", "kept", [], "the trigger on the volume row's triple"),
    "Lean.exchange": ("SWAP", "kept", [], "every line exchanged and complemented at its own wall (the wall a property of the line, not `line is self.phi`)"),
    "Lean.frame_nodes": ("PRIM", "kept", [], "the Node and its six neighbours"),
    "Lean.read_number": ("CLICK", "kept", [], "the one-Link read on the digit lattices, the two refusals origin and coarse"),
    "Lean.take": ("CLICK", "kept", [], "the exact take by the quadratic root"),
    "Lean.close": ("CLICK", "minus", [(407, 419), (469, 476)],
                   "the click: the Link close (391-406), the lay's refusal, the take per Node, the lay, the bodies' closing; 407-419 the two former modes (link, node) out; 469-476 the detectors' light credits move to the writer (counted there as 8)"),
    "Lean.lay_amplitude": ("CLICK", "minus", [(480, 480)], "the lay of one quantum of the child's unit; the switch LEAN_FIXED_A out"),
    "Lean.credit": ("WRITER", "minus", [(495, 501)], "the credit line; 495-501 the frame (the Node's phases, odd lines, factors, neighbours) out: the decoder reads the seven readings alone"),
    "Lean.back_line": ("ROTATE", "drop", [], "the inverse written again: rotate(row, direction=-1) is the same function (carried_division takes the direction)"),
    "Lean.back_plane": ("ROTATE", "drop", [], "the inverse written again: rotate(row, direction=-1)"),
    "Lean.step_back": ("LOOP", "minus", [(546, 624)],
                       "533-545 the close undone from the log (13 lines) kept as click(rows, direction=-1); 546-624 the step written again backward out: step(direction=-1) is the same function"),
    "Lean.census": ("WRITER", "kept", [], "the integers per Node and the bits"),
    "Lean.state_bytes": ("WRITER", "kept", [], "the run back's hash"),
}
MAIN_BLOCK = (635, 667)  # the __main__ run: the loop called, the rows' cadence, the record dumped: WRITER (host)
EXTRA_LINES = {"CLICK": [("the seed's lays and the click's lays as one lay(row, at, quanta, sense): one loop in the loader calling it", 3)],
               "WRITE": [("the forms, W and J accumulated over the rows (from step 246-251)", 6), ("the held writes, one carried division per line (from step 260-275 less 270)", 15)],
               "WRITER": [("the detectors' light credits (from close 469-476)", 8), ("the __main__ block 635-667", MAIN_BLOCK[1] - MAIN_BLOCK[0] + 1)]}
DECODER = {"solve": (31, "drop: the species solve re-runs the Node's fold from the frame; the decoder reads the credit's point and beat instead"),
           "rest": (200 - 31, "kept: the gates from the credit lines, in integers")}
TESTS = {"lean/cube48_test.py": ("TEST", "the 48 on the toy, kept"), "lean/runback_test.py": ("TEST", "the run back, kept"),
         "lean/mirror_diag.py": ("TOOL", "a diagnostic, out of the toy's module or kept under tools"),
         "lean/residuals.py": ("TOOL", "a diagnostic of the former decoder's solve: falls with solve"),
         "lean/freeze_diag.py": ("TOOL", "a diagnostic, kept under tools or out")}
PROBES = ("probes/refusals_probe.py", "probes/stability_probe.py", "probes/write_probe.py")


def main():
    report = json.load(open(sys.argv[1], encoding="utf-8"))
    lean = {f["name"]: f for f in report["files"][LEAN]["functions"]}
    out = {}
    rows = []
    for name, (target, rule, drops, note) in SPEC.items():
        f = lean[name]
        if rule == "drop":
            kept = 0
        else:
            removed = sum(e - s + 1 for s, e in drops)
            for s, e in drops:
                assert f["start"] <= s <= e <= f["end"], (name, s, e)
            kept = f["lines"] - removed
        out.setdefault(target, {"measured": 0, "kept": 0, "functions": 0})
        out[target]["measured"] += f["lines"]
        out[target]["kept"] += kept
        out[target]["functions"] += 1
        rows.append({"function": name, "range": f"{f['start']}-{f['end']}", "measured": f["lines"], "target": target, "rule": rule,
                     "dropped_ranges": drops, "kept": kept, "note": note})
    for target, extras in EXTRA_LINES.items():
        out.setdefault(target, {"measured": 0, "kept": 0, "functions": 0})
        for note, n in extras:
            out[target]["kept"] += n
            rows.append({"function": "(moved)", "target": target, "rule": "split", "kept": n, "note": note})
    lean_lines = report["files"][LEAN]["lines"]
    in_functions = sum(f["lines"] for f in lean.values() if "." in f["name"] or not f["name"][0].isupper() or f["name"] == "Line")
    class_header = lean["Lean"]["lines"] - sum(f["lines"] for f in lean.values() if f["name"].startswith("Lean."))
    module_level = lean_lines - in_functions - class_header - (MAIN_BLOCK[1] - MAIN_BLOCK[0] + 1)
    node_targets = ("ROTATE", "WRITE", "SWAP", "CLICK", "PRIM", "LOOP")
    node_kept = sum(out[t]["kept"] for t in node_targets if t in out)
    decoder_kept = DECODER["rest"][0]
    tests_kept = sum(report["files"][p]["lines"] for p, (kind, _n) in TESTS.items() if kind == "TEST")
    tools_lines = sum(report["files"][p]["lines"] for p, (kind, _n) in TESTS.items() if kind == "TOOL")
    probes_lines = sum(report["files"][p]["lines"] for p in PROBES)
    toy_lean_total = sum(report["files"][p]["lines"] for p in report["files"] if p.startswith("lean/"))
    summary = {
        "lean_full.py measured": lean_lines,
        "module level (docstring, imports, constants, module functions' headers)": module_level,
        "Lean class header lines (docstring, blank)": class_header,
        "by target (measured lines of the functions mapped; kept lines after the fold)": out,
        "folded Node file (rotate, write, swap, click, the primitives, the loop)": node_kept,
        "folded loader": out["LOADER"]["kept"],
        "folded writer (the lines out, the census, the __main__ run)": out["WRITER"]["kept"],
        "folded decoder (decoder_full.py 200 less solve 31)": decoder_kept,
        "folded tests kept (cube48_test, runback_test)": tests_kept,
        "diagnostics (mirror_diag, residuals, freeze_diag) kept under tools or out": tools_lines,
        "probes of the 4.0 engine (out of the toy)": probes_lines,
        "module level and imports carried over (estimate: the same 20 lines of imports and constants)": 20,
        "folded toy total (Node + loader + writer + decoder + the two tests + imports)": node_kept + out["LOADER"]["kept"] + out["WRITER"]["kept"] + decoder_kept + tests_kept + 20,
        "toy lean/ measured": toy_lean_total,
        "toy lean/ + probes measured": report["totals"]["lines"],
    }
    Path(sys.argv[2]).write_text(json.dumps({"summary": summary, "rows": rows, "decoder": DECODER, "tests": TESTS}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    for r in rows:
        print(r["target"], r["function"], r.get("range", ""), r.get("measured", ""), "->", r["kept"], r["rule"])


if __name__ == "__main__":
    main()
