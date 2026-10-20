"""The singlet's four worlds under the family's sign (ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange, 2026-10-19, and The click is the meeting; tests/test_the_spin.py, the singlet's test built as files, and tests/test_the_exchange_sign.py, the singlet under the sign) from the design file beside this script: four chain worlds, one per pair of settings, the two-plane family's parts laid alike as two packets from the centre toward the two ends, half a quantum each, two beams to the two declared regions at the chain's ends, each region's `axis` the side's setting (c, s) and both regions' `pattern` the plain identity, the family's sign under exchange declared `antisymmetric` in the universe file (the crossed pattern [[0, 1], [-1, 0]] on one side the declaration of 3.0.0 the sign supersedes, its numbers identical by the determinant's identity at two parts); their mode files by the packet lay (tools/pixel_mode.py, with --modes); and the blind expectation file, derived from the settings in exact fractions before any run and never touched after, by the reader's own algebra on equal parts in the sign's form (tools/spin_gate.py, `at_equal_parts` with the family's sign read from the universe file, the ports by the loader's `ports_of` on the axis and the pattern): E(a, b) = -cos(theta_a - theta_b), -119 / 169, 119 / 169, -120 / 169, -120 / 169, S = -478 / 169 with the CHSH signs, the marginal 1 / 2, and the three local credits as the fence, every one with |S| at most 2. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell_singlet/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import bell_gate  # noqa: E402  # the reader's arithmetic: E, the marginals, the combination, the file's form
import spin_gate  # noqa: E402  # the reader in the plane's form with the family's sign: the blind is what it gives on equal parts

from event_universe.loader.universe import EXCHANGE  # noqa: E402  # the key's two words

ORDER = (
    ("a", "b"),
    ("a", "b_prime"),
    ("a_prime", "b"),
    ("a_prime", "b_prime"),
)  # CHSH, minus on the second
COMBINATION = {"name": "S", "signs": [1, -1, 1, 1]}  # S = E(a, b) - E(a, b') + E(a', b) + E(a', b')


def world(design: dict[str, Any], a: str, b: str) -> dict[str, object]:
    """One world: the chain, the pair laid as one event at the centre toward both sides, the two regions at the ends with their settings as their axes and their patterns, the receding faces, the intervals, the draw."""
    source, depth, length = int(design["source"]), int(design["screen"]), int(design["length"])
    p, q = (int(v) for v in design["wave"])
    packets = [
        {
            "family": design["family"],
            "along": "x",
            "wave": [sign * p, q],
            "phase": [0, 1],
            "amplitude": int(design["amplitude"]),
            "top": {"x": [source, source], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": int(design["edge_along"]), "y": 0, "z": 0},
        }
        for sign in (-1, 1)
    ]
    node_detectors = [
        {
            "name": design["sides"]["a"],
            "positions": [[x, 0, 0] for x in range(depth)],
            "axis": [int(v) for v in design["settings"][a]],
            "pattern": design["patterns"]["a"],
        },
        {
            "name": design["sides"]["b"],
            "positions": [[x, 0, 0] for x in range(length - depth, length)],
            "axis": [int(v) for v in design["settings"][b]],
            "pattern": design["patterns"]["b"],
        },
    ]
    return {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": int(design["intervals"]),
        "universe": design["universe"],
        "bodies": [],
        "packets": packets,
        "node_detectors": node_detectors,
        "receding": design["receding"],
        "draw": design["draw"],
    }


def ports(design: dict[str, Any], settings: tuple[str, ...]) -> list[dict[str, tuple[int, ...]]]:
    """The sides' ports for one combination of settings, each side's from its axis and its pattern (the loader's one arithmetic for an axis and a basis)."""
    return [
        bell_gate.ports_of(
            tuple(int(v) for v in design["settings"][setting]),
            tuple((int(a), int(b)) for a, b in design["patterns"][label]),
        )
        for label, setting in zip(design["sides"], settings, strict=True)
    ]


def exchange_of(design: dict[str, Any]) -> int:
    """The family's sign under exchange as the universe file the design names declares it (the key `exchange`, its two words the loader's), -1 antisymmetric, 1 symmetric, 0 undeclared."""
    universe = json.loads((ROOT / str(design["universe"])).read_text(encoding="utf-8"))
    row = next(f for f in universe["families"] if f["name"] == design["family"])
    return EXCHANGE[row["exchange"]] if "exchange" in row else 0


def blind_of(
    worlds: dict[str, list[Any]], labels: list[str], name: str, signs: list[int], exchange: int
) -> dict[str, Any]:
    """The blind's numbers from the settings alone in the sign's form (bell_gate's `blind_of` with spin_gate's `at_equal_parts`): per combination of settings the reader's numbers at equal parts under the family's sign, and the combination `name` of the four E by the meeting and by each local credit with the signs given."""
    numbers = {
        key: bell_gate.written(spin_gate.at_equal_parts(ports, exchange), labels)
        for key, ports in worlds.items()
    }

    def combined(entry: str) -> list[int] | None:
        return bell_gate.pair(
            bell_gate.combination((bell_gate.fraction(numbers[key][entry]) for key in worlds), signs)
        )

    found: dict[str, Any] = {
        entry: {key: numbers[key][entry] for key in worlds}
        for entry in ("correlation", "marginals", "sub_correlations", "shares", "joint")
    }
    found[name] = combined("correlation")
    for entry in ("by_the_parts_shares", "by_the_local_sums", "by_the_sign"):
        found[entry] = {
            "correlation": {key: numbers[key][entry] for key in worlds},
            name: combined(entry),
        }
    return found


def blind(design: dict[str, Any]) -> dict[str, Any]:
    """The blind numbers from the settings alone, exact, by the reader's algebra on equal parts in the sign's form: E per pair of settings and S by the meeting, the marginals, the shares, the three local credits with their S, and the status and fence of each."""
    found = blind_of(
        {" ".join(pair): ports(design, pair) for pair in ORDER},
        list(design["sides"]),
        COMBINATION["name"],
        COMBINATION["signs"],
        exchange_of(design),
    )
    found.update(
        efficiency="1, closed by construction: every pair is credited by the draw",
        status="theorem under the declared credit (the one form of the click, the meeting, the pair's amplitude the determinant of the two sides' parts under the family's antisymmetric sign, the plain identity pattern on both sides): E(a, b) = -cos(theta_a - theta_b) exact in the integers' rationals at equal parts, the parts laid alike stepping alike by the determinism of Rule3; S = -478 / 169 with the CHSH signs, |S| = 478 / 169 = 2.8284, above 2 and below 2 sqrt 2 by 2.5 x 10^-5; every marginal 1 / 2 whatever the partner's axis; at equal axes the shares of (+, +) and (-, -) are 0 exactly, the anticorrelation; the numbers the crossed pattern's of 3.0.0 exactly, the determinant at two parts equal to the symmetric form with [[0, 1], [-1, 0]] on one side term by term; a gate of the engine and never a result (HIGHLIGHTS.md, One experiment and one gate)",
        fence="clicks",
    )
    found["by_the_parts_shares"].update(
        status="theorem: each part's share credited alone is a product form, |S| at most 2; the lower fence (read over the parts with the identity patterns: its sign against the crossed pattern's flips, the magnitude 238 / 169 unchanged)",
        fence="clicks",
    )
    found["by_the_local_sums"].update(
        status="theorem: the square of each side's own sum is a product form, |S| at most 2; each side drawing alone on its own local share lands here (the probe's arm B1, 240 / 169; under the identity patterns its sign against the crossed pattern's flips, the magnitude unchanged)",
        fence="clicks",
    )
    found["by_the_sign"].update(
        status="theorem: the larger port on each side, every outcome the same, |S| at most 2, 2 exactly where neither side ties (the probe's arm B3); the upper fence of a local credit (under the identity patterns its sign against the crossed pattern's flips, the magnitude 2 unchanged)",
        fence="clicks",
    )
    return found


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/spin_gate.py (bell_gate's reading) reads it: the family with its sign under exchange, the window, the sides' regions, the settings as axes and the patterns (the identity on both, the superseded crossed pattern named), the four worlds in CHSH order with the combination's name and signs, the credit's rule named in the sign's form, the seed, the probe's four arms and the blind."""
    return {
        "verdict": "NODEDETECTOR",
        "comment": design["comment"],
        "family": design["family"],
        "window": [int(v) for v in design["window"]],
        "sides": design["sides"],
        "settings": design["settings"],
        "settings_declared_as": "axis",
        "patterns": design["patterns"],
        "exchange": design["exchange"],
        "superseded_pattern": design["superseded_pattern"],
        "order": [" ".join(pair) for pair in ORDER],
        "runs": {" ".join(pair): "singlet_" + "_".join(pair) for pair in ORDER},
        "combination": COMBINATION,
        "rule": "the joint share accumulated over the window on both members of the level pair in the sign's form: J(p_A, p_B) = SUM over the window and both members of |SUM_{k != l} sign(l - k) e_k^A(p_A) psi_k^A e_l^B(p_B) psi_l^B|^2, the determinant of the two sides' parts for the family's antisymmetric sign, psi_k the part's (re, im) sums at the side and e_k(+) = alpha_k c + beta_k s and e_k(-) = alpha_k (-s) + beta_k c from the declared axis (c, s) under the side's pattern, the identity on both sides (at two parts the same term by term as the symmetric form SUM_k c_k psi_k^A psi_k^B with the crossed pattern [[0, 1], [-1, 0]] on one side, the 3.0.0 declaration); E = (J_++ + J_-- - J_+- - J_-+) over the four summed; the window the whole passage, the credit's interval the window's close, the two ports drawn one after another by the sides on their own reads with the write at the birth, the realised pair the gate's; J is a sum of norms and never negative, so no floor is needed",
        "arms": design["arms"],
        "blind": blind(design),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode files too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for a, b in ORDER:
        path = args.folder / f"singlet_{a}_{b}.json"
        document = world(design, a, b)
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        if args.modes:
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        print(json.dumps({"world": str(path), "settings": [a, b]}))
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": str(args.folder / "expectation.json"), "blind": written["blind"]["S"]}
        )
    )


if __name__ == "__main__":
    main()
