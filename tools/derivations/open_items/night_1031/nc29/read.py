"""NC29's reader: the decoder's own functions (wt/src/tensor24/decoder) on a record, shadow.clock_lines by its own
logic with places.keys() - meeting taken once (shadow.py:136 takes it per line), plus the clicks per 100 rounds per
train and the end line. Usage: python -I read.py <record .jsonl>"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("wt", "src")))
sys.set_int_max_str_digits(0)

from tensor24.decoder import clicks, measure, records, shadow  # noqa: E402


def clock_lines(record):
    lines = clicks.listed(record)
    gaps, _ = shadow.lacking(lines, ("q", "train"), "its meeting is")
    places = shadow.placed(lines, gaps)
    meeting = {p for p, h in places.items() if shadow.met(h)}
    outside = places.keys() - meeting  # taken once
    own = {}
    for line in sorted([x for x in lines if records.whole(x.get("train"))], key=lambda x: x["round"]):
        own.setdefault((line["site"], line["train"]), []).append(line)
    astray = {at for at, held in own.items() for e in held if (e["round"], e["site"]) in outside}
    return len(astray), len(own)


def main():
    record, cause = records.read(sys.argv[1])
    if record is None:
        print("not read:", cause)
        return
    held = clicks.counted(record)
    labels = {t.get("index"): t.get("label") for t in record.header.get("trains", [])}
    print("end:", record.end)
    print("click lines:", len(held.lines))
    for t, tally in held.trains.items():
        print(f"train {t} ({labels.get(t)}): {tally.lines} lines, given {tally.given}, taken {tally.taken}, net {tally.net}")
    b = shadow.books(record)
    print("books:", b["kind"], "|", b["cause"])
    m = shadow.meetings(record)
    print("meetings:", m["kind"], "|", m["cause"][:300])
    astray, clocks = clock_lines(record)
    print(f"each clock's line: {'SHOWN' if not astray else 'NOT SHOWN'}: {astray} of {clocks} clocks click outside a meeting")
    rounds = record.end.get("rounds", 0)
    per = {}
    for line in held.lines:
        per.setdefault(line["train"], {}).setdefault((line["round"] - 1) // 100, 0)
        per[line["train"]][(line["round"] - 1) // 100] += abs(line["q"])
    for t in sorted(per):
        print(f"clicks |q| per 100 rounds, train {t} ({labels.get(t)}):",
              [per[t].get(i, 0) for i in range((rounds + 99) // 100)])


main()
