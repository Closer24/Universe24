"""ex1: the take read from a record's log alone (the credit lines: births and body credits), in integers.
Prints the counts, taken and booked summed over the births and over the credits, the quotient in hundredths with its
remainder, the excess per line (min, max, the count at 0), the run back, the Node's integer count and bits, and under the
flag the paid identity (taken + remainder_was - remainder == booked) per line and the remainders' net change.
Usage: read_take.py <record.json>"""
import json
import sys


def quot(a, b, scale):
    return (a * scale // b, a * scale % b) if b else (None, None)


def main(path):
    sys.set_int_max_str_digits(0)
    rec = json.load(open(path))
    log = rec["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    counts = rec["counts"]
    out = {"file": path, "counts": counts, "run_back": rec["run_back"]}
    last = rec["rows"][-1] if rec["rows"] else {}
    out["integers"] = last.get("integers")
    out["max_bits"] = last.get("max bits")
    for name, lines, book in (("births", births, "booked"), ("credits", credits, None)):
        taken = sum(int(e["taken"]) for e in lines)
        booked = sum(int(e["booked"]) for e in lines) if book else None
        d = {"lines": len(lines), "taken": taken}
        if book:
            d["booked"] = booked
            d["taken_per_booked_hundredths_rem"] = quot(taken, booked, 100)
            exc = [int(e["taken"]) - int(e["booked"]) for e in lines]
            d["excess_min_max"] = [min(exc), max(exc)] if exc else None
            d["excess_zero_count"] = sum(1 for x in exc if x == 0)
            d["excess_sum"] = sum(exc)
            if lines and "remainder_was" in lines[0]:
                paid = [int(e["taken"]) + int(e["remainder_was"]) - int(e["remainder"]) for e in lines]
                d["paid_eq_booked_count"] = sum(1 for p, e in zip(paid, lines) if p == int(e["booked"]))
                d["paid_per_booked_hundredths_rem"] = quot(sum(paid), booked, 100)
                d["remainder_net_change"] = sum(int(e["remainder"]) - int(e["remainder_was"]) for e in lines)
                d["remainder_max"] = max(int(e["remainder"]) for e in lines)
        else:
            if lines and "booked" not in lines[0]:
                sys.path.insert(0, sys.argv[2] if len(sys.argv) > 2 else "")
                from event_universe.core.paces import sine_den
                from event_universe.core.rule3 import unit_of

                den, T = int(rec["den"]), int(rec["T"])
                units = [unit_of(sine_den(int(p_), den) if int(p_) != den else den, T) for p_ in rec["planes"]]
                for e in lines:
                    e["booked"] = units[int(e["line"])]
                d["booked_from_units"] = True
                d["booked"] = sum(int(e["booked"]) for e in lines)
                d["taken_per_booked_hundredths_rem"] = quot(taken, d["booked"], 100)
                exc = [int(e["taken"]) - int(e["booked"]) for e in lines]
                d["excess_min_max"] = [min(exc), max(exc)] if exc else None
                d["excess_per_booked_max_hundredths"] = max(quot(x, int(e["booked"]), 100)[0] for x, e in zip(exc, lines)) if exc else None
            if lines and "remainder_was" in lines[0]:
                paid = [int(e["taken"]) + int(e["remainder_was"]) - int(e["remainder"]) for e in lines]
                d["paid_eq_owed_unit_count"] = sum(1 for p, e in zip(paid, lines) if p == int(e["booked"]))
                d["booked"] = sum(int(e["booked"]) for e in lines)
                d["taken_per_booked_hundredths_rem"] = quot(taken, d["booked"], 100)
                d["remainder_net_change"] = sum(int(e["remainder"]) - int(e["remainder_was"]) for e in lines)
                d["remainder_max"] = max(int(e["remainder"]) for e in lines)
            levels = [int(e["levels"]) for e in lines]
            d["levels_min_max"] = [min(levels), max(levels)] if levels else None
        out[name] = d
    senses = [sum(e["senses"]) for e in births]
    out["charge_sum_over_births"] = sum(senses)
    out["W_children_sum"] = sum(sum(e["W_children"]) for e in births)
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main(sys.argv[1])
