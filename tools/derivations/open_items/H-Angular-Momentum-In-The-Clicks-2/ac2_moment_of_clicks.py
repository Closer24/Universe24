"""The angular momentum read in the clicks alone (the hand H-Angular-Momentum-In-The-Clicks-2): a reader over a record's log, integers only, one Link's reach (it reads credit and birth lines, no Node).

For every credit line the moment (2 r - 2 c) x dP_take about the centre c (doubled, so a centre at a half-integer stays an integer; 2J is what is summed, as the board hands' 2L); for every birth line the taker's moment (2 r_at - 2 c) x dP_take plus the lay's moment at the Link (2 r_plus - 2 c) x dP_lay (dP_lay along the Link's axis, so either end reads the same, checked); a merger's two ends each at their own Node. The spin part: the credit's sense (the plane's one scalar) and the born children's senses summed. The identities read per line: a laid-back credit books dP_take 0 (EQ-S1); a birth's dP_lay is 0 (the children at the quarter turn carry no current); the senses of a born pair sum to 0; and J about a second centre c' is J(c) - (c' - c) x P_clicks exactly."""
import json
import sys
from typing import Any

sys.set_int_max_str_digits(0)


def cross(u: list[int], v: list[int]) -> list[int]:
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def add(u: list[int], v: list[int]) -> list[int]:
    return [a + b for a, b in zip(u, v, strict=True)]


def arm(r: list[int], centre2: list[int]) -> list[int]:
    return [2 * x - c for x, c in zip(r, centre2, strict=True)]


def axis_of(minus: list[int], plus: list[int], cube: int) -> int | None:
    """The Link's axis from its two ends (one coordinate apart, the torus's wrap included)."""
    axes = [a for a in range(3) if (plus[a] - minus[a]) % cube != 0]
    return axes[0] if len(axes) == 1 else None


def moment_of_clicks(record: dict[str, Any], centre2: list[int]) -> dict[str, Any]:
    """The clicks' J (doubled) about the centre (doubled coordinates), per record, with the per-line identities and the per-interval running sum."""
    log = record["log"]
    cube = record.get("cube") or (max(max(e["node"]) for e in log if e.get("node")) + 1)
    J2 = [0, 0, 0]
    P = [0, 0, 0]
    per_interval: dict[int, list[int]] = {}
    out: dict[str, Any] = {
        "credits": 0, "credits laid back": 0, "laid back with dP_take 0": 0, "laid back with dP_take not 0": 0,
        "credits standing (dP_take booked)": 0, "credits with dP_take 0 and not laid back": 0,
        "births": 0, "births with dP_lay 0": 0, "births with dP_lay along the Link's axis": 0,
        "births with senses summing to 0": 0, "births with W_children summing to 0": 0,
        "births with dP_take along the Link's axis only": 0, "mergers (two ends' takes)": 0,
        "sense sum over credits": 0, "credits by sense": {"-1": 0, "0": 0, "1": 0},
        "J2 of the takes' along-axis part at births": [0, 0, 0], "J2 of the takes' transverse part at births": [0, 0, 0],
        "J2 of the credits": [0, 0, 0], "J2 of the births' takes": [0, 0, 0], "J2 of the births' lays": [0, 0, 0],
    }
    for e in log:
        kind = e.get("event")
        if kind == "credit":
            out["credits"] += 1
            dp = [int(x) for x in e["dP_take"]]
            m = cross(arm(e["node"], centre2), dp)
            if "laid_back" in e:
                out["credits laid back"] += 1
                out["laid back with dP_take 0" if dp == [0, 0, 0] else "laid back with dP_take not 0"] += 1
            else:
                out["credits standing (dP_take booked)"] += 1
                if dp == [0, 0, 0]:
                    out["credits with dP_take 0 and not laid back"] += 1
            out["sense sum over credits"] += int(e.get("sense", 0))
            out["credits by sense"][str(int(e.get("sense", 0)))] += 1
            out["J2 of the credits"] = add(out["J2 of the credits"], m)
        elif kind == "birth":
            out["births"] += 1
            dp_lay = [int(x) for x in e["dP_lay"]]
            ax = axis_of(e["minus"], e["plus"], cube)
            if dp_lay == [0, 0, 0]:
                out["births with dP_lay 0"] += 1
            if ax is not None and all(dp_lay[b] == 0 for b in range(3) if b != ax):
                out["births with dP_lay along the Link's axis"] += 1
            if sum(e["senses"]) == 0:
                out["births with senses summing to 0"] += 1
            if sum(int(w) for w in e["W_children"]) == 0:
                out["births with W_children summing to 0"] += 1
            lay_m = cross(arm(e["plus"], centre2), dp_lay)
            if "takes" in e:
                out["mergers (two ends' takes)"] += 1
                takes = [(t["node"], [int(x) for x in t["dP_take"]]) for t in e["takes"]]
            else:
                takes = [(e["node"], [int(x) for x in e["dP_take"]])]
            m = [0, 0, 0]
            dp = [0, 0, 0]
            for where, dpt in takes:
                a = arm(where, centre2)
                m = add(m, cross(a, dpt))
                dp = add(dp, dpt)
                if ax is not None:
                    along = [dpt[b] if b == ax else 0 for b in range(3)]
                    trans = [0 if b == ax else dpt[b] for b in range(3)]
                    out["J2 of the takes' along-axis part at births"] = add(out["J2 of the takes' along-axis part at births"], cross(a, along))
                    out["J2 of the takes' transverse part at births"] = add(out["J2 of the takes' transverse part at births"], cross(a, trans))
            if ax is not None and all(dp[b] == 0 for b in range(3) if b != ax):
                out["births with dP_take along the Link's axis only"] += 1
            out["J2 of the births' takes"] = add(out["J2 of the births' takes"], m)
            out["J2 of the births' lays"] = add(out["J2 of the births' lays"], lay_m)
            m = add(m, lay_m)
            dp = add(dp, dp_lay)
        else:
            continue
        J2 = add(J2, m)
        P = add(P, dp)
        per_interval[int(e["i"])] = add(per_interval.get(int(e["i"]), [0, 0, 0]), m)
    out["cube"] = cube
    out["centre2"] = centre2
    out["J2 clicks"] = J2
    out["P clicks"] = P
    out["intervals with a click moment not 0"] = sum(1 for v in per_interval.values() if v != [0, 0, 0])
    out["max abs J2 per interval"] = max((max(abs(x) for x in v) for v in per_interval.values()), default=0)
    out["per_interval"] = {str(k): v for k, v in sorted(per_interval.items())}
    return out


def shift_identity(record: dict[str, Any], centre2: list[int], other2: list[int]) -> bool:
    """J2(c') = J2(c) - (2c' - 2c) x P exactly (the moment's one centre law)."""
    a, b = moment_of_clicks(record, centre2), moment_of_clicks(record, other2)
    d = [o - c for o, c in zip(other2, centre2, strict=True)]
    return b["J2 clicks"] == add(a["J2 clicks"], [-x for x in cross(d, a["P clicks"])])


def against_board(reading: dict[str, Any], am1_path: str) -> dict[str, Any]:
    """The clicks' J2 per interval against the board's 2L change per interval (am1's per-interval reading, the same doubled centre): the board's change less the clicks' moment is the torque of the step and the swap."""
    am1 = json.load(open(am1_path))
    rows = am1["rows"]
    centre = am1["centre"]
    if [2 * c for c in centre] != reading["centre2"]:
        return {"am1": am1_path, "centre mismatch": [centre, reading["centre2"]]}
    prev = None
    sum_abs_board = [0, 0, 0]
    sum_abs_clicks = [0, 0, 0]
    sum_abs_rest = [0, 0, 0]
    at_click_intervals = [0, 0, 0]
    board_at_click = [0, 0, 0]
    n_click_intervals = 0
    for row in rows:
        l2 = [int(x) for x in row["2L"]]
        if prev is not None:
            d = [x - y for x, y in zip(l2, prev, strict=True)]
            m = reading["per_interval"].get(str(row["i"]), [0, 0, 0])
            rest = [x - y for x, y in zip(d, m, strict=True)]
            for a in range(3):
                sum_abs_board[a] += abs(d[a])
                sum_abs_clicks[a] += abs(m[a])
                sum_abs_rest[a] += abs(rest[a])
            if m != [0, 0, 0]:
                n_click_intervals += 1
                for a in range(3):
                    at_click_intervals[a] += abs(m[a])
                    board_at_click[a] += abs(d[a])
        prev = l2
    end = [int(x) for x in rows[-1]["2L"]]
    start = [int(x) for x in rows[0]["2L"]]
    return {
        "am1": am1_path.split("/")[-1], "intervals": len(rows) - 1,
        "board 2L end - start": [e - s for e, s in zip(end, start, strict=True)],
        "clicks J2 summed": reading["J2 clicks"],
        "board change less clicks (the torque of the step and the swap)": [e - s - j for e, s, j in zip(end, start, reading["J2 clicks"], strict=True)],
        "sum |board d2L| per interval": sum_abs_board, "sum |clicks J2| per interval": sum_abs_clicks, "sum |rest| per interval": sum_abs_rest,
        "intervals with a click moment": n_click_intervals,
        "at those intervals: sum |clicks J2|": at_click_intervals, "at those intervals: sum |board d2L|": board_at_click,
    }


if __name__ == "__main__":
    path = sys.argv[1]
    record = json.load(open(path))
    cube = record.get("cube") or (max(max(e["node"]) for e in record["log"] if e.get("node")) + 1)
    centre2 = [cube - 1] * 3 if len(sys.argv) < 3 or not sys.argv[2] else [int(x) for x in sys.argv[2].split(",")]
    reading = moment_of_clicks(record, centre2)
    reading["centre shift identity (J2(c') = J2(c) - (2c'-2c) x P) at c' = 0"] = shift_identity(record, centre2, [0, 0, 0])
    per = reading.pop("per_interval")
    if len(sys.argv) > 3:
        reading["against the board"] = against_board({**reading, "per_interval": per}, sys.argv[3])
    reading["record"] = path.split("/")[-1]
    print(json.dumps(reading, indent=1))
