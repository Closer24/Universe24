"""Held-out test H10 of the sign_split_v1 layer with decoder v1.1 (pre-registered: validation/PREREGISTRATION.md, addendum 3).

    nice -n 10 python -m research.click_decoder_v1.validation.heldout_sign

For each of r20's 34 settings (runs/matter_light_v1/r20/phase_element/, truth: r20's phase_element.json)
and the official CLI log (phase_element_cli/, truth 280 / 0 / 3): split the native log into the P and M
layers, compare them with r20's files, decode each layer with v1.1 and r20's detector declaration, and
count the comparators exactly as r20 does. Writes runs/click_decoder_v1/heldout/heldout_sign_split_v1.json (never
into the package) and compares it with the recorded validation/heldout_sign_split_v1.json (release 1.0.4).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from research.click_decoder_v1 import decoder_v11 as D
from research.click_decoder_v1.sign_layer import sign_split
from research.click_decoder_v1.validation.run import report_recorded

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
R20 = ROOT / "runs/matter_light_v1/r20"
OUT = ROOT / "runs/click_decoder_v1/heldout/r20"


def counts(base, det, side, prefix):
    if not Path(f"{prefix}.P.jsonl").exists():
        sign_split(base, prefix)
    spec = json.loads(Path(det).read_text())
    names = sorted(spec["detectors"])
    fired, same = {}, {}
    for tag in ("P", "M"):
        mine = Path(f"{prefix}.{tag}.jsonl")
        theirs = Path(str(base).replace(".jsonl", f".{tag}.jsonl"))
        same[tag] = theirs.exists() and mine.read_bytes() == theirs.read_bytes()
        ev, info = D.read_log(mine)
        rep = D.decode(ev, side=side, horizon=1, detectors=spec, layer=f"sign_split_v1:{tag}", log_info=info)
        fired[tag] = {k for k, v in rep["correlations"]["detectors"].items() if v["bins_fired"] > 0}
    return {"+": len(fired["P"]), "-": len(fired["M"]),
            "0": sum(1 for k in names if k not in fired["P"] and k not in fired["M"]),
            "both": sum(1 for k in names if k in fired["P"] and k in fired["M"])}, same


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    truth = json.loads((ROOT / "research/matter_light_v1/r20/phase_element.json").read_text())
    rows, ok = [], 0
    for r in truth["rows"]:
        name = f"{r['family']}_{r['setting']}"
        base = R20 / "phase_element" / f"{name}.jsonl"
        got, same = counts(base, R20 / "phase_element" / f"{name}.detectors.json", r["side"], OUT / name)
        want = {k: r["decoder_counts"][k] for k in ("+", "-", "0", "both")}
        rows.append({"setting": name, "truth": want, "v1.1": got, "equal": got == want, "layers_equal_r20": same,
                     "log_sha256": hashlib.sha256(base.read_bytes()).hexdigest()})
        ok += got == want
        print(name, got == want, same, flush=True)
    cli_base = R20 / "phase_element_cli" / "Falpha_1_1.cli.jsonl"
    side = next(r["side"] for r in truth["rows"] if f"{r['family']}_{r['setting']}" == "Falpha_1_1")
    got, same = counts(cli_base, R20 / "phase_element_cli" / "Falpha_1_1.cli.detectors.json", side, OUT / "Falpha_1_1.cli")
    cli = {"truth": {"+": 280, "-": 0, "0": 3}, "v1.1": got, "layers_equal_r20": same,
           "equal": [got["+"], got["-"], got["0"]] == [280, 0, 3]}
    out = {"layer": "sign_split_v1", "decoder": D.VERSION, "settings_equal": [ok, len(rows)], "cli": cli, "rows": rows,
           "layer_files_equal": sum(1 for x in rows if all(x["layers_equal_r20"].values()))}
    written = OUT.parent / "heldout_sign_split_v1.json"
    written.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"settings_equal": out["settings_equal"], "layer_files_equal": out["layer_files_equal"], "cli": cli}))
    return report_recorded(out, HERE / "heldout_sign_split_v1.json", written)


if __name__ == "__main__":
    main()
