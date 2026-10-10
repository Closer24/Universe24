"""The paper's results against its assumptions, for a human to read: every sentence that states a result (we show, so, therefore, because, here is why) and every sentence that states an assumption (we declare, we put in, assumed, placed by us, declared, taken from). A result is flagged when its own reason is one of the paper's declared things, and the three parts of the arrow are traced: the speed must follow from the step rule's locality, the place from the record's absence, the size from a count. Usage: python3 check_circularity.py."""
from __future__ import annotations
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import body_of, plain, read_tex, sentences

RESULT = [r"\bwe show\b", r"\bso\b", r"\btherefore\b", r"\bbecause\b", r"\bhere is why\b", r"\bit follows\b", r"\bthat is why\b"]
ASSUMPTION = [r"\bwe declare\b", r"\bwe put it in\b", r"\bwe put in\b", r"\bassum", r"\bplaced by us\b", r"\bdeclared\b", r"\btaken from the first paper\b", r"\bwe propose\b", r"\bchosen\b"]


def matches(sentence: str, patterns: list[str]) -> list[str]:
    return [p.strip("\\b") for p in patterns if re.search(p, sentence, flags=re.I)]


def main() -> int:
    body = plain(body_of(read_tex()))
    sents = sentences(body)
    results = [(s, matches(s, RESULT)) for s in sents if matches(s, RESULT)]
    assumptions = [(s, matches(s, ASSUMPTION)) for s in sents if matches(s, ASSUMPTION)]
    print("RESULTS (%d sentences):" % len(results))
    for s, m in results:
        print("  [%s] %s" % (", ".join(m), s))
    print("\nASSUMPTIONS (%d sentences):" % len(assumptions))
    for s, m in assumptions:
        print("  [%s] %s" % (", ".join(m), s))
    flags = []
    # a result whose reason is a declaration of the same thing
    for s, m in results:
        if matches(s, ASSUMPTION) and re.search(r"\b(so|therefore|because)\b", s, re.I) and re.search(r"\b(declare|put in|declared)\b", s, re.I):
            flags.append("a result reasoned from a declaration in one sentence: " + s)
    # the three parts of the arrow and their reasons
    text = body
    speed_ok = re.search(r"reads only its neighbours.*?one step per tick|speaks only to its six neighbours.*?one step per tick|one neighbour per tick, because|Nothing moves faster than one step per tick|counted in steps along the connections, nothing moves faster", text, re.I | re.S) is not None
    place_ok = re.search(r"backward run fails where the record is missing|goes wrong where the wiping had reached|starts where the wiping last reached", text, re.I) is not None
    size_ok = re.search(r"count(ed)? of whole numbers|whole numbers, each|values, plus two|16,254 values", text, re.I) is not None
    print("\nTHE ARROW'S THREE PARTS:")
    print("  the speed from the step rule's locality: %s" % ("found" if speed_ok else "MISSING"))
    print("  the place from the record's absence: %s" % ("found" if place_ok else "MISSING"))
    print("  the size as a count: %s" % ("found" if size_ok else "MISSING"))
    # the click is declared, and the paper must say so before claiming the arrow's place
    if not re.search(r"the click, which we declare", text):
        flags.append("the paper does not say that the click is declared")
    if not re.search(r"not our result|proposal", text):
        flags.append("the paper does not separate the proposal about nature from the result on the board")
    for part, ok in (("speed", speed_ok), ("place", place_ok), ("size", size_ok)):
        if not ok:
            flags.append("the arrow's %s has no stated reason of the right kind" % part)
    if flags:
        print("\nFLAGS:")
        for f in flags:
            print("  " + f)
        return 1
    print("\nno circularity flagged; the lists above are for a human to read")
    return 0


if __name__ == "__main__":
    sys.exit(main())
