"""The counts table in prose from bell_setting.py's JSON lines: per record and per (outcome, setting) the pairs used, the four cells [n, same, opposite], the settings' agreement through the root, and S = num / den with S^2 against 4 and 8 under the first labelling (a = 0, b = 0) and the band of every labelling. Usage: python summarize.py <out.json> [...]"""

import json
import sys

sys.set_int_max_str_digits(0)

for path in sys.argv[1:]:
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        print("RECORD", r["record"].split("/")[-1], "intervals", r["intervals"], "cube", r["cube"])
        for k in (
            "births",
            "credits",
            "pairs clicked at both ends",
            "twin one Link away at both ends",
            "the two ends clicking in one interval",
            "credit's sense equal to the laid sense (- end, + end)",
            "credit's sense 0 (ends)",
            "run_back",
        ):
            print("  ", k, r[k])
        for rd in r["readings"]:
            cells = rd["cells (- end, + end): [n, same, opposite]"]
            first = rd["labellings"]["a=0 b=0"]
            bands = sorted({v["band"] for v in rd["labellings"].values() if v.get("S")})
            s = "no S (a cell empty)" if first.get("S") is None else f"S = {first['S'][0]} / {first['S'][1]}, S^2 = {first['S^2'][0]} / {first['S^2'][1]}"
            print(
                "  ",
                f"outcome {rd['outcome']:8s} setting {rd['setting']:13s}",
                "used",
                rd["pairs used"],
                "dropped",
                rd["pairs dropped (a setting or an outcome undefined)"],
                "agree/differ",
                rd["settings agree / differ through the root"],
                "cells ab,ab',a'b,a'b'",
                [cells["00"], cells["01"], cells["10"], cells["11"]],
                s,
                "; ".join(bands) if bands else "every labelling has an empty cell",
            )
