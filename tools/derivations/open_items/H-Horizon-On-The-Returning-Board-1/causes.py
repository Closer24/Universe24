"""The causes of the refusals at one interval (sb1): the refusal events of the record's log counted by their cause, and the Nodes that bore a child, so an uneven birth round on an alike board is read by cause and not guessed."""
import json
import sys
from collections import Counter


def main(path, interval):
    r = json.load(open(path))
    cause = Counter()
    nodes = set()
    born = set()
    for e in r["log"]:
        if int(e.get("i", -1)) != interval:
            continue
        if e.get("event") == "refused":
            cause[str(e.get("why") or e.get("cause") or e.get("kind"))] += 1
            nodes.add(str(e.get("node")))
        if e.get("event") == "birth":
            born.add(str(e.get("node")))
    print(path, "interval", interval)
    print("  the refusals by cause", dict(cause))
    print("  the Nodes with a refusal", len(nodes), "the Nodes that bore", len(born))
    keys = sorted({k for e in r["log"] if e.get("event") == "refused" for k in e})
    print("  the refusal event's own fields", keys)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
