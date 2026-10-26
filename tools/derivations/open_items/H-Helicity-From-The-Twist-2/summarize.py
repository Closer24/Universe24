"""The summary of the helicity reader's outputs: per record the reading's checks, the carriage counts, hd2's integer counts, the Bell cells and S per outcome and setting (integers only). Usage: python summarize.py <out.json> ..."""
import json
import sys

OUTCOMES = ("sense", "lambda_birth*lambda_arrival", "Hbirth.Htwin", "lambda_birth*lambda_twin", "lambda_twin*lambda_arrival", "sign_h_arrival", "int_arrival", "Hbirth.Int_arrival", "lambda_birth*int_arrival_inward", "Hbirth.Int_twin")
SETTINGS = ("arrival_side", "arrival_twin", "taken_line", "turned", "link_frame", "proper_parity")
for path in sys.argv[1:]:
    o = json.load(open(path))
    print("==", o["record"], "cube", o["cube"], "intervals", o["intervals"], "run back", o["run_back"])
    for k in ("births", "births with the twist read from the Node line", "births read from the log alone", "into matches the log (the take's Node the end the current flows into)", "h's sign matches the log (the + child's end by the twist's sign)", "births by the helicity's sign (h e_a along +a: +, -)", "births by axis", "children by lambda (the scalar along the arm: +, -)", "one hand row (every birth's h e_a of one sign)"):
        print(k, ":", o[k])
    for k, v in o["carriage"].items():
        print("carriage", k, v)
    u = o["unit"]
    print("unit", {k: u[k] for k in u if not k.startswith("|h|")})
    print("bell pairs", o["bell"]["pairs clicked at both ends"])
    for r in o["bell"]["readings"]:
        if r["outcome"] in OUTCOMES and r["setting"] in SETTINGS:
            best = r["largest S^2 over the labellings"]
            lab = None if best is None else r["labellings"][best["labelling"]]
            print("bell", r["outcome"], "|", r["setting"], "| used", r["pairs used"], "dropped", r["pairs dropped"], "| cells", r["cells (- end, + end): [n, same, opposite]"], "| S", None if lab is None else lab["S"], "q,r", None if lab is None else lab["S quotient, remainder"], "S^2", None if lab is None else lab["S^2"], "|", None if lab is None else lab["band"])
