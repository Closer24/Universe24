"""H-Click-Beyond-Rule3-2: the report's rows from the readers' summaries (one JSON line per clicks file). Usage: python cx2_rows.py <clicks.json> ..."""
import json
import sys

for path in sys.argv[1:]:
    try:
        s = json.load(open(path))["summary"]
    except Exception as e:  # noqa: BLE001
        print(path, "unreadable", e)
        continue
    k = s["kinds"]
    row = "| {name} | {read} | {light} | {merg} | {cand} | {rest} | {cred} | {lb} | {stops} | {lays} | {turns} | {sg} | {pl} | {rf} | {rb} |".format(
        name=path.split("/")[-1],
        read=s["births_read"], light=k["light_taken_births"], merg=k["pair_taken_mergers"],
        cand=s["inverse_kept_with_standing"], rest=k["rest_births"], cred=k["credits"], lb=k["laid_back"],
        stops=k["stops"], lays=k["lay_refusals"], turns=k["turns"],
        sg="%d of %d" % tuple(s["sign_from_odd_bilinear"]), pl="%d of %d" % tuple(s["plane_from_digit"]),
        rf="%d of %d (%d crowded)" % (s["refusal_from_quotient"][0], s["refusal_from_quotient"][1], s["refused_crowded"]),
        rb="%s" % (s["run_back"] and "%d of %d" % (s["run_back"]["exact"], s["run_back"]["intervals"])),
    )
    print(row)
    c = s["credits"]
    print("  credits: levels <= dist %d of %d; exact take %d; turned %d; line0 %d line1 %d; birth exact take %s; stops fall<walls %d" % (
        c["levels_le_dist"], k["credits"], c["exact_take"], c["turned"], c["taken_line_0"], c["taken_line_1"], s["birth_exact_take"], c["stops_fall_below_walls"]))
