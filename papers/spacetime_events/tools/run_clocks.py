"""The two clocks of Section 5 counted on the board with the program's own functions (core/paces for the clock and the Link's pace from the content, core/rule3 for the integers and the step), in exact whole numbers, and written to run_clocks.json beside the paper: (rest) one Node of the pair 2 and 3 whose six neighbours hold its own number, stepped 6,000 ticks at content 0 and at content 600, its swings counted (a swing is the number going up, down and back; counted as the sign changes of now, two per swing); (moving) a row of 400 Nodes, ends holding zero, the neighbours across the row holding each Node's own number, a pattern eight Nodes from crest to crest laid at Node 70 and stepped 1,200 ticks, the number at the pattern's middle read each tick and its swings counted against the same count at rest; (light) a long pattern of light, forty Nodes from crest to crest, on a row of 4,000 Nodes at content 600 and at none, stepped 1,500 ticks with light's integers at that content, its middle's speed counted and compared with the form c (rate/q_0)^2. Deterministic; no toss. Usage: python3 -I run_clocks.py [src directory, ../../src unless given]."""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parents[2] / "src"
sys.path.insert(0, str(SRC))
import numpy as np  # noqa: E402
from event_universe.core import paces, rule3  # noqa: E402

GAMMA = 6000
NUM, DEN = 2, 3
OUT = HERE.parent / "run_clocks.json"


def integers(content: int, num: int = NUM, den: int = DEN) -> tuple[int, int, tuple[int, ...], int, int]:
    """(clock, the Link's pace, the six reads, S, w) at one content from the program's functions, for the pair num and den."""
    clock = int(paces.clock_of(GAMMA, content))
    pace = int(paces.link_pace_of(GAMMA, content))
    reads, s, w = rule3.coefficients(num, den, GAMMA, clock, pace)
    return clock, pace, tuple(int(x) for x in reads), int(s), int(w)


def swings(series: list[int]) -> float:
    s = np.sign(np.array(series, dtype=np.int64))
    s = s[s != 0]
    return float(int(np.sum(s[1:] * s[:-1] < 0)) / 2)


def rest(content: int, ticks: int, height: int = 10**6) -> float:
    """One Node whose six arrivals are its own number, started at the top of a swing, stepped `ticks` times."""
    clock, pace, reads, s, w = integers(content)
    cos_turn = (sum(reads) + s) / (2 * w)
    now, before, rem = height, int(round(height * cos_turn)), 0
    series = [now]
    for _ in range(ticks):
        nxt, rem = rule3.rule3(reads, (now,) * 6, s, w, now, before, rem)
        before, now = now, nxt
        series.append(now)
    return swings(series), max(abs(x) for x in series)


def moving(crest: int, ticks: int, row: int = 400, start: float = 70.0, width: float = 18.0, height: int = 10**7) -> dict:
    """A pattern `crest` Nodes from crest to crest on a row of `row` Nodes, each Node an equal part of a swing behind the one before; the middle followed by the pattern's weight; its number's swings counted."""
    clock, pace, reads, s, w = integers(0)
    part = 2 * math.pi / crest  # the part of a swing between neighbours, as an angle
    cos_turn = (s + 4 * reads[0] + 2 * reads[0] * math.cos(part)) / (2 * w)  # the two row neighbours a part behind and ahead, the four across holding the own number
    turn = math.acos(cos_turn)
    x = np.arange(row, dtype=float)
    shape = height * np.exp(-((x - start) ** 2) / (2 * width ** 2))
    now = np.rint(shape * np.cos(part * (x - start))).astype(np.int64)
    before = np.rint(shape * np.cos(part * (x - start) + turn)).astype(np.int64)
    rem = np.zeros(row, dtype=np.int64)
    r64, s64, w64 = np.int64(reads[0]), np.int64(s), np.int64(w)
    middles, at_middle = [], []
    for t in range(ticks + 1):
        weight = now.astype(float) ** 2 + before.astype(float) ** 2
        middle = float((x * weight).sum() / weight.sum())
        middles.append(middle)
        at_middle.append(int(now[int(round(middle))]))
        if t == ticks:
            break
        left, right = np.roll(now, 1), np.roll(now, -1)
        left[0] = 0
        right[-1] = 0  # the ends hold zero
        nxt, rem = rule3.rule3((r64,) * 6, (right, left, now, now, now, now), s64, w64, now, before, rem)
        before, now = now, nxt
    return {"row": row, "crest": crest, "ticks": ticks, "middle_start": round(middles[0], 1), "middle_end": round(middles[-1], 1), "middle_speed": round((middles[-1] - middles[0]) / ticks, 4), "swings_moving": swings(at_middle), "swings_rest": rest(0, ticks)[0], "largest_number": int(np.abs(now).max())}


def light(content: int, ticks: int = 1500, row: int = 4000, start: float = 800.0, crest: float = 40.0, width: float = 60.0, height: int = 10**7) -> dict:
    """A long pattern of light (the pair 1 and 1) on a row of `row` Nodes at one content, the neighbours across the row holding each Node's own number; its middle followed by the pattern's weight, its speed in Nodes per tick, against the form sqrt(R/w) of its integers."""
    clock, pace, reads, s, w = integers(content, 1, 1)
    c_form = math.sqrt(reads[0] / w)
    x = np.arange(row, dtype=float)
    part = 2 * math.pi / crest
    laid = lambda t: np.rint(height * np.exp(-((x - start - c_form * t) ** 2) / (2 * width ** 2)) * np.cos(part * (x - start - c_form * t))).astype(np.int64)
    now, before, rem = laid(0), laid(-1), np.zeros(row, dtype=np.int64)
    r64, s64, w64 = np.int64(reads[0]), np.int64(s), np.int64(w)
    centre = lambda a: float(((a.astype(float) ** 2) * x).sum() / (a.astype(float) ** 2).sum())
    c0 = centre(now)
    for _ in range(ticks):
        left, right = np.roll(now, 1), np.roll(now, -1)
        left[0] = 0
        right[-1] = 0
        nxt, rem = rule3.rule3((r64,) * 6, (right, left, now, now, now, now), s64, w64, now, before, rem)
        before, now = now, nxt
    return {"content": content, "clock": clock, "row": row, "crest": crest, "ticks": ticks, "speed_form": round(c_form, 4), "speed_counted": round((centre(now) - c0) / ticks, 4), "largest_number": int(np.abs(now).max())}


def main() -> int:
    ticks = 6000
    (s0, big0), (s600, big600) = rest(0, ticks), rest(600, ticks)
    clock600 = integers(600)[0]
    out = {
        "pair": [NUM, DEN],
        "rest": {"ticks": ticks, "content_0": {"clock": integers(0)[0], "swings": s0, "largest_number": big0}, "content_600": {"clock": clock600, "swings": s600, "largest_number": big600}, "ratio": round(s600 / s0, 4)},
        "moving": moving(8, 1200),
        "light": {"content_0": light(0), "content_600": light(600)},
    }
    out["moving"]["ratio"] = round(out["moving"]["swings_moving"] / out["moving"]["swings_rest"], 4)
    lt = out["light"]
    lt["ratio_counted"] = round(lt["content_600"]["speed_counted"] / lt["content_0"]["speed_counted"], 3)
    lt["ratio_form"] = round(lt["content_600"]["speed_form"] / lt["content_0"]["speed_form"], 3)
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    r, m = out["rest"], out["moving"]
    print(f"run_clocks: at rest, pair {NUM} and {DEN}, {r['ticks']} ticks: {r['content_0']['swings']} swings at content 0 (clock {r['content_0']['clock']}), {r['content_600']['swings']} at content 600 (clock {r['content_600']['clock']}), ratio {r['ratio']}")
    print(f"run_clocks: moving, row {m['row']}, crest {m['crest']}, {m['ticks']} ticks: the middle from {m['middle_start']} to {m['middle_end']}, {m['middle_speed']} Node per tick; {m['swings_moving']} swings at the moving middle against {m['swings_rest']} at rest, ratio {m['ratio']}")
    print(f"run_clocks: light, row {lt['content_0']['row']}, crest {lt['content_0']['crest']}, {lt['content_0']['ticks']} ticks: {lt['content_600']['speed_counted']} Node per tick at content 600 against {lt['content_0']['speed_counted']} at none, ratio {lt['ratio_counted']} counted, {lt['ratio_form']} by the form")
    print(f"written to {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
