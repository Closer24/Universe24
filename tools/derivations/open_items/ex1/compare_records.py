"""ex1: two records compared bit for bit but for the clock (the milliseconds of the reader's rows). Usage: compare_records.py <a.json> <b.json>"""
import json
import sys


def strip(rec):
    for row in rec.get("rows", []):
        row.pop("milliseconds", None)
    return rec


def main(a, b):
    sys.set_int_max_str_digits(0)
    ra, rb = strip(json.load(open(a))), strip(json.load(open(b)))
    same = json.dumps(ra, sort_keys=True) == json.dumps(rb, sort_keys=True)
    keys = [k for k in ra if json.dumps(ra[k], sort_keys=True) != json.dumps(rb.get(k), sort_keys=True)]
    print(json.dumps({"a": a, "b": b, "bit_for_bit": same, "keys_apart": keys}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
