"""Print the validation tables of a results file as Markdown.

    python -m research.click_decoder_v1.validation.table [results_v1.0.json]
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def fmt(v):
    if isinstance(v, dict) and "n" in v:
        return f"{v['n']}/{v['of']}" + (f" = {v['rate']:.3f}" if v["rate"] is not None else "")
    return str(v)


def main(path=None):
    r = json.loads(Path(path or HERE / "results_v1.0.json").read_text())
    print(f"decoder {r['decoder']['version']}, frozen {r['frozen']['frozen_utc'] if r['frozen'] else '-'}\n")
    print("| set A metric | value |\n|---|---|")
    for k, v in r["set_A"]["metrics"].items():
        print(f"| {k} | {fmt(v)} |")
    for name, key in (("set B (r08 test set, r08 reference truth)", "set_B"), ("set C (l = 0 layer)", "set_C")):
        print(f"\n{name}\n\n| family | truth (dark) | found | TP | FP | FN | precision | recall all | recall visible |")
        print("|---|---|---|---|---|---|---|---|---|")
        for fam, d in r[key]["totals"].items():
            if isinstance(d, dict) and "tp" in d:
                print(f"| {fam} | {d['truth']} ({d['truth_dark']}) | {d['found']} | {d['tp']} | {d['fp']} | {d['fn']} | "
                      f"{d['precision']} | {d['recall_all']} | {d['recall_visible']} |")
        if "dark_recall" in r[key]["totals"]:
            print(f"\ndark objects at rest found in this layer: {fmt(r[key]['totals']['dark_recall'])}")
    print("\nset A by group\n\n| group | blocks | with sources | composite sources | lamps | light tracks | "
          "matter tracks | created |\n|---|---|---|---|---|---|---|---|")
    for g, d in r["set_A"]["by_group"].items():
        print(f"| {g} | {d.get('blocks', 0)} | {d.get('with sources', 0)} | {d.get('composite sources', 0)} | "
              f"{d.get('lamps', 0)} | {d.get('light tracks', 0)} | {d.get('matter tracks', 0)} | "
              f"{d.get('created objects', 0)} |")


if __name__ == "__main__":
    main(*sys.argv[1:])
