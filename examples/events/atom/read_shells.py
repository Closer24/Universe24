"""The shells' reading (the design verdict of 2026-10-19, section 4; tests/test_the_exchange_sign.py, the shell of two quanta): each shells world is loaded and stepped by the engine's own step with a spy on `lists.absorption`, the test's, which keeps each close's list as the engine builds it (the board's interval, the transitions out of the standing part by their parts' names, the weight of each outcome and of nothing, and beside them the weights the same list carries without the sign, each transition's transfer share over the closing norms by the credit's own `unabsorbed_in` read, the identity) and returns it untouched; from the run's lines the credit lines of the body (the interval, the part before and the part realised at each absorption), the body's counts at the end and the photon's count. The checks against the blind (`expectation.json`, the world's entry): the two closes at the blind's intervals, the first close's weights into either excited part and the rest, the second close's weights into the populated and the empty excited part, no count above the blind's bound for the antisymmetric record, the piling for the symmetric control. Written to `atom_shells.reading.json` for both worlds; every number the engine's, the script comparing and inventing none. With `--rule` the blind's seed rule is run before the folder's run: the antisymmetric world is built at each candidate seed into a scratch folder by build_world.py (`--seed`) and read, and the first seed at which the second photon enters the empty part is named.

PYTHONPATH=src python examples/events/atom/read_shells.py [--worlds atom_shells.json atom_shells_symmetric.json] [--expectation expectation.json] [--out atom_shells.reading.json]
PYTHONPATH=src python examples/events/atom/read_shells.py --rule [--scratch <folder>]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from event_universe import lists
from event_universe.core.rule3 import division_forward
from event_universe.lattice import Lattice
from event_universe.world_files import load_world

HERE = Path(__file__).resolve().parent


def run(path: Path) -> dict[str, Any]:
    """One world run with the spy: the closes, the credit lines, the counts at the end."""
    closes: list[dict[str, Any]] = []
    original = lists.absorption

    def kept(board: Lattice, drive: int, outcomes: list[Any]) -> list[Any]:
        norms = [sum(label * label for label in books.labels) for books, _transition in outcomes]
        unit, _unabsorbed = board.credit.unabsorbed_in(drive, norms)  # the list's own read, the identity
        unsigned = [
            int(b.shares[t] * division_forward(unit, norm, 0)[0])
            for (b, t), norm in zip(outcomes, norms, strict=True)
        ]
        found = original(board, drive, outcomes)
        names = tuple(outcomes[0][0].declared.names) if outcomes else ()
        closes.append(
            {
                "interval": int(board.interval),
                "standing_part": names[outcomes[0][0].part] if outcomes else None,
                "transitions": [[names[t.leaves], names[t.enters]] for _b, t in outcomes],
                "weights": [int(a.weight) for a in found[:-1]],
                "rest": int(found[-1].weight),
                "weights_without_the_sign": unsigned,
                "unit": int(unit),
            }
        )
        return found

    lists.absorption = kept
    try:
        lines: list[dict[str, Any]] = []
        board = Lattice(load_world(path), lines.append)
        books = board.credit.bodies[0]
        names = list(books.declared.names)
        photon = [f.name for f in board.families].index("photon")
        start = {
            "part": names[books.part],
            "counts": list(books.counts),
            "capacities": list(books.declared.capacities),
        }
        exchange = int(board.families[books.index].exchange)
        for _ in range(board.world.intervals):
            board.step()
            if board.ended is not None:
                break
    finally:
        lists.absorption = original
    credits = [
        {
            k: line.get(k)
            for k in ("interval", "before", "realised", "count", "left", "absorbed", "window")
        }
        for line in lines
        if line.get("event") == "credit"
    ]
    taken = [c for c in credits if c["absorbed"]]
    return {
        "world": path.name,
        "exchange": {-1: "antisymmetric", 1: "symmetric"}.get(exchange, "undeclared"),
        "parts": names,
        "start": start,
        "intervals": int(board.interval),
        "closes": closes,
        "credit_lines": credits,
        "absorptions": taken,
        "counts_at_the_end": list(books.counts),
        "photon_count_at_the_end": int(board.credit.counts[photon]),
        "entered_the_empty_part": len(taken) == 2 and taken[1]["realised"] != taken[0]["realised"],
        "piled": len(taken) == 2 and taken[1]["realised"] == taken[0]["realised"],
    }


def checked(reading: dict[str, Any], blind: dict[str, Any]) -> dict[str, Any]:
    """The reading against the world's blind: the closes' intervals, the first close's weights and rest, the second close's weights into the populated and the empty part, the counts' bound, the piling."""
    names, closes = reading["parts"], reading["closes"]
    checks: dict[str, Any] = {}
    want = [int(v) for v in blind["closes"]]
    checks["closes_at"] = {
        "read": [c["interval"] for c in closes],
        "blind": want,
        "pass": [c["interval"] for c in closes] == want,
    }
    first = blind["first_close"]
    if closes:
        c = closes[0]
        checks["first_close_weights"] = {
            "read": dict(zip(["->".join(t) for t in c["transitions"]], c["weights"], strict=True)),
            "rest": c["rest"],
            "blind": {"into_each_excited_part": first["into_each_excited_part"], "rest": first["rest"]},
            "pass": all(w == int(first["into_each_excited_part"]) for w in c["weights"])
            and c["rest"] == int(first["rest"]),
        }
    second = blind["second_close"]
    if len(closes) > 1 and reading["absorptions"]:
        c = closes[1]
        populated = reading["absorptions"][0]["realised"]
        into = {t[1]: w for t, w in zip(c["transitions"], c["weights"], strict=True)}
        unsigned = {
            t[1]: w for t, w in zip(c["transitions"], c["weights_without_the_sign"], strict=True)
        }
        empty = [n for n in into if n != populated]
        read_populated, read_empty = into.get(populated), [into[n] for n in empty]
        checks["second_close_weights"] = {
            "populated_part": populated,
            "into_the_populated_part": read_populated,
            "unsigned_into_the_populated_part": unsigned.get(populated),
            "into_the_empty_part": read_empty,
            "rest": c["rest"],
            "blind": {
                "into_the_populated_part": second["into_the_populated_part"],
                "into_the_empty_part": second["into_the_empty_part"],
            },
            "pass": read_populated == int(second["into_the_populated_part"])
            and all(w == int(second["into_the_empty_part"]) for w in read_empty),
        }
    if "counts_never_above" in blind:
        bound = int(blind["counts_never_above"])
        checks["counts_never_above"] = {
            "bound": bound,
            "read": reading["counts_at_the_end"],
            "pass": max(reading["counts_at_the_end"]) <= bound,
        }
    checks["at_the_seed"] = {
        "blind": blind["at_the_seed"],
        "counts_at_the_end": reading["counts_at_the_end"],
        "photon_count_at_the_end": reading["photon_count_at_the_end"],
        "entered_the_empty_part": reading["entered_the_empty_part"],
        "piled": reading["piled"],
    }
    assert isinstance(names, list)
    return checks


def rule(expectation: dict[str, Any], scratch: Path) -> dict[str, Any]:
    """The blind's seed rule run: the antisymmetric world built at each candidate seed into the scratch folder and read; the first seed at which the second photon enters the empty part."""
    blind = expectation["worlds"]["atom_shells"]
    found: dict[str, Any] = {"candidates": {}, "seed": None, "rule": blind["seed_rule"]}
    for seed in blind["seed_candidates"]:
        folder = scratch / f"seed_{seed}"
        subprocess.run(
            [
                sys.executable,
                str(HERE / "build_world.py"),
                "--folder",
                str(folder),
                "--only",
                "atom_shells",
                "--modes",
                "--seed",
                str(seed),
            ],
            check=True,
            cwd=HERE.parents[2],
            stdout=subprocess.DEVNULL,
        )
        reading = run(folder / "atom_shells.json")
        found["candidates"][str(seed)] = {
            "absorptions": [[c["interval"], c["before"], c["realised"]] for c in reading["absorptions"]],
            "counts_at_the_end": reading["counts_at_the_end"],
            "entered_the_empty_part": reading["entered_the_empty_part"],
        }
        if reading["entered_the_empty_part"] and found["seed"] is None:
            found["seed"] = int(seed)
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--worlds",
        type=Path,
        nargs="*",
        default=[HERE / "atom_shells.json", HERE / "atom_shells_symmetric.json"],
    )
    parser.add_argument("--expectation", type=Path, default=HERE / "expectation.json")
    parser.add_argument("--out", type=Path, default=HERE / "atom_shells.reading.json")
    parser.add_argument(
        "--rule",
        action="store_true",
        help="run the blind's seed rule over the candidates and name the seed",
    )
    parser.add_argument(
        "--scratch", type=Path, default=None, help="the rule's scratch folder (a temporary one)"
    )
    args = parser.parse_args(argv)
    expectation = json.loads(args.expectation.read_text(encoding="utf-8"))
    if args.rule:
        scratch = args.scratch or Path(tempfile.mkdtemp(prefix="shells_rule_"))
        print(json.dumps(rule(expectation, scratch), indent=1))
        return
    worlds = {}
    for path in args.worlds:
        reading = run(path)
        stem = path.name.rsplit(".", 1)[0]
        blind = expectation["worlds"].get(stem, {})
        reading["checks"] = checked(reading, blind) if blind else {}
        reading["seed_declared"] = blind.get("seed")
        worlds[stem] = reading
    document = {
        "label": "NODEDETECTOR",
        "comment": "the shells' reading: each close's absorption list as the engine built it (the spy of the branch's test), the credit lines, the counts at the end, checked against the blind; two quanta, one standing part at a time (the one-part convention: the body stands in gu, then in gd after the first click, so the second close's list is gd's)",
        "worlds": worlds,
    }
    args.out.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    summary = {
        stem: {
            "exchange": r["exchange"],
            "absorptions": [[c["interval"], c["before"], c["realised"]] for c in r["absorptions"]],
            "counts_at_the_end": r["counts_at_the_end"],
            "photon_count_at_the_end": r["photon_count_at_the_end"],
            "checks": {k: v.get("pass", v) for k, v in r["checks"].items()},
        }
        for stem, r in worlds.items()
    }
    print(json.dumps(summary, default=str))


if __name__ == "__main__":
    main()
