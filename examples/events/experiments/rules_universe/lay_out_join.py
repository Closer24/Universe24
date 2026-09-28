"""WORLD (d) OF THE RULE'S OWN UNIVERSE: THE CLICK JOINS AND PARTS (ALGEBRA.md #the-rows-against-nature, THE RULE'S OWN UNIVERSE, THE BOUND BODY IS ONE NODE, THE CLICK JOINS AND PARTS, THE ALGEBRA OF CLUSTERS; the owner's decision of 2026-09-28, 13:02 Israel time, through the Closer: the rule's universe is the finish line, world (d) to the de Broglie Experimenter; the owner's word of 15:11: Gamma in the rule's universe file is 24, a whole universe in small). Two worlds on the rule's universe of record (`examples/events/planck.json`; Gamma read from the file): THE JOIN, two bound bodies of one Node each, the smaller and the deeper, so close that their tails overlap: the law's row is a run of clicks from the smaller to the deeper whose last ends the smaller's record, one record for the joined cluster (the one non-local act); THE PARTING (the world named `part`), the same two bodies beyond the click's reach ln(b_1 b_2 / T) / kappa (Cheshbon's line of 15:22 Israel time), so that no click passes and both records stand. The counts, the clock pairs, the tails, the edge, the reach and the distances are Cheshbon's per Gamma and per engine (the engine of today reads the level once; the corrected term reads it twice, the law's form): at Gamma = 24 (15:22) the pixels are the counts 6 to 11 under the law and 9 to 14 on the engine of today, the join at three Links and the parting at six (the reach about three to four Links); at Gamma = 12,000 (13:03, 13:18, 14:12, 14:47) the join at two Links and, the reach being about eighteen Links, the far world at five Links is the slow join and no parting (the older run; the second run of record is Gamma = 6,000 by the owner's word of 15:44, laid out when Cheshbon gives its table). Cheshbon's table from the generator run as Rule3 in integers (15:43) enters the expectation as the record's amplitude b, its count D bar and its period P per body, the reading of the run (the Closer 15:47). The mode files come from the generator of the rule's universe, `tools/pixel_mode.py` (the owner's word of 14:32: no seed, profile or mode written by hand; THE GENERATOR IS RULE3, the owner's word of 15:28: the mode files are regenerated when the tool derives the record by Rule3 alone). Every number is the law's; no number of a run enters here. THE HIERARCHY IS RECURSIVE (the world named `hierarchy`, where Cheshbon's number is given): two equal pixels two Links apart are a cluster one level up, and the breathing period of the pair's total count against the pixel's period is the ratio of the ticks between levels, about e^(kappa d) (Cheshbon 16:35: at 6,000, 2,000 and 2,000 at two Links, P_2 about 73 against P_1 9.55, the ratio 7.6 in 5 to 11). Run from the repository root: python examples/events/experiments/rules_universe/lay_out_join.py [--out <folder>] [--engine today|term] [--universe <file>] [--suffix _6000]; the files are written under the folder and nothing else."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from event_universe.world_files import (
    input_digest,  # noqa: E402  (the loader's own digest, the mode file's stamp)
)

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent

UNIVERSE_OF_RECORD = "examples/events/planck.json"  # the rule's own universe of record (#1411, #1419, #1425, #1430): three rows in pairs over Gamma, T = 1; Gamma is read from the file
ENGINE = "examples/events/engine_start.json"
EDGE_FRACTION = {  # the edge of the bound body as a fraction of Gamma (Cheshbon 14:12 and 15:22 Israel time): under the corrected term (the law, the level read twice) 0.2255 Gamma; on the engine of today (the level read once) 0.3444 Gamma
    "today": 0.3444,
    "term": 0.2255,
}
COUNTS = {  # the smaller and the deeper body's counts per engine and Gamma (Cheshbon 15:22 for 24; 15:50 for 6,000, the run of record after 24 by the owner's word of 15:44; 14:47 and 13:03 for 12,000, the older run)
    "today": {24: (10, 12), 6_000: (2_200, 2_350), 12_000: (4_400, 4_700)},
    "term": {24: (8, 10), 6_000: (1_500, 2_000), 12_000: (3_000, 4_000)},
}
DISTANCES = {  # Links between the two Nodes per Gamma: the join within the click's reach, the far world beyond it (24: the reach about three to four Links, Cheshbon 15:22, so six Links part; 6,000: the join at three Links, Cheshbon 15:50, the reach ln(b_1 b_2 / T) / kappa about eight to eighteen Links by the two tails, so twenty Links part; 12,000: the reach about eighteen Links, Cheshbon 13:18, so five Links is the slow join and no parting)
    24: {"join": 3, "part": 6, "reach": 4},
    6_000: {"join": 3, "part": 20, "reach": 18},
    12_000: {"join": 2, "part": 5, "reach": 18},
}
DISSOLUTION = {  # the smaller dissolved within these intervals (blind): 24 about two bound periods (Cheshbon 15:22); 6,000 at three Links about two bound periods, 15 to 25 intervals (Cheshbon 16:37); 12,000 at two Links 3 to 10 and at five Links 30 to 70 (Cheshbon 13:18)
    24: {"join": (10, 20), "part": None},
    6_000: {"join": (15, 25), "part": None},
    12_000: {"join": (3, 10), "part": (30, 70)},
}
TICKS = 300  # the run's length in intervals: the Experimenter's proposal until Cheshbon's blind number of clicks
STEPS = 1024  # N, the phase's steps
PIXELS: dict[
    str, dict[int, dict[str, float | int]]
] = {  # Cheshbon's numbers per engine and count: the bound rotation omega_b, its period in intervals, the tail's kappa per Link, the clock pair's numerator a over 2^16 and the tail's factor t over 2^16 (15:22 Israel time for Gamma = 24, the law's table and the level-once table; 15:50 for 6,000 with the amplitude b of the form; 14:12, 14:47 and 13:39 for 12,000)
    "term": {
        6: {"omega_b": 0.8105, "period": 7.75, "kappa": 0.446, "a": 90_329, "t": 41_948},
        7: {"omega_b": 0.7358, "period": 8.54, "kappa": 0.798, "a": 97_161, "t": 29_503},
        8: {"omega_b": 0.6578, "period": 9.55, "kappa": 1.015, "a": 103_723, "t": 23_747},
        9: {"omega_b": 0.5826, "period": 10.79, "kappa": 1.164, "a": 109_453, "t": 20_458},
        10: {"omega_b": 0.5137, "period": 12.23, "kappa": 1.269, "a": 114_155, "t": 18_423},
        11: {"omega_b": 0.4550, "period": 13.81, "kappa": 1.341, "a": 117_736, "t": 17_144},
        1_500: {"omega_b": 0.8105, "period": 7.75, "kappa": 0.446, "a": 90_329, "t": 41_948, "b": 49},
        2_000: {"omega_b": 0.6578, "period": 9.55, "kappa": 1.015, "a": 103_723, "t": 23_747, "b": 69},
        2_200: {"omega_b": 0.5972, "period": 10.52, "kappa": 1.138, "a": 108_385, "t": 20_992, "b": 79},
        2_500: {"omega_b": 0.5137, "period": 12.23, "kappa": 1.269, "a": 114_155, "t": 18_423, "b": 98},
        3_000: {"omega_b": 0.8105, "period": 7.75, "kappa": 0.446, "a": 90_326, "t": 41_943},
        4_000: {"omega_b": 0.6578, "period": 9.55, "kappa": 1.02, "a": 103_722, "t": 23_724},
    },
    "today": {
        9: {"omega_b": 0.8218, "period": 7.65, "kappa": 0.356, "a": 89_243, "t": 45_922},
        10: {"omega_b": 0.7779, "period": 8.08, "kappa": 0.631, "a": 93_378, "t": 34_863},
        11: {"omega_b": 0.7274, "period": 8.64, "kappa": 0.826, "a": 97_899, "t": 28_688},
        12: {"omega_b": 0.6741, "period": 9.32, "kappa": 0.976, "a": 102_403, "t": 24_686},
        13: {"omega_b": 0.6193, "period": 10.15, "kappa": 1.097, "a": 106_729, "t": 21_885},
        14: {"omega_b": 0.5637, "period": 11.15, "kappa": 1.195, "a": 110_792, "t": 19_830},
        2_200: {"omega_b": 0.8290, "period": 7.58, "kappa": 0.283, "a": 88_553, "t": 49_395, "b": 58},
        2_350: {"omega_b": 0.8055, "period": 7.80, "kappa": 0.480, "a": 90_801, "t": 40_554, "b": 61},
        2_500: {"omega_b": 0.7779, "period": 8.08, "kappa": 0.631, "a": 93_378, "t": 34_863, "b": 65},
        3_000: {"omega_b": 0.6741, "period": 9.32, "kappa": 0.976, "a": 102_403, "t": 24_686, "b": 82},
        4_400: {"omega_b": 0.8290, "period": 7.58, "kappa": 0.283, "a": 88_553, "t": 49_395},
        4_700: {"omega_b": 0.8055, "period": 7.80, "kappa": 0.480, "a": 90_801, "t": 40_554},
        5_000: {"omega_b": 0.778, "period": 8.08, "kappa": 0.63, "a": 93_270, "t": 34_734},
        6_000: {"omega_b": 0.674, "period": 9.32, "kappa": 0.98, "a": 102_340, "t": 24_904},
    },
}
RECORDS: dict[
    str, dict[int, dict[str, list[float]]]
] = {  # Cheshbon's table from the generator run as Rule3 in integers at Gamma = 24 (15:43 Israel time; the Closer 15:47: the blind expectation of every look at 24): per engine and per amplitude b at the Node, the counts the record carries (D bar = the sum of D over the record's period div P T, THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD), the period P in intervals and the window of declared counts that seed it; the count of a run is read against D bar and P, not against the file's count
    "term": {
        5: {"counts": [8, 9], "record_count": [8.4, 10.0], "period": [9.2, 11.0]},
        8: {"counts": [10, 11], "record_count": [12.4, 14.9], "period": [12.0, 13.3]},
    },
    "today": {
        5: {"counts": [9, 11], "record_count": [9.6, 9.9], "period": [6.9, 8.0]},
        6: {"counts": [12, 12], "record_count": [9.2, 9.2], "period": [9.2, 9.2]},
    },
}
RECORD_PAIR = {  # the two bodies of (d) by their amplitude b (Cheshbon 15:43 item 3(d), the Closer 15:47): the smaller and the deeper
    "term": (5, 8),
    "today": (5, 6),
}
HIERARCHY = {  # THE HIERARCHY IS RECURSIVE (Cheshbon 16:35 Israel time, the Closer 16:42): two equal pixels close enough that their tails overlap are a cluster of one level up, and the cluster's own tick is the breathing period P_2 of the pair's total count; P_2 / P_1 is about e^(kappa d) with P_1 the pixel's period; per engine and Gamma the pair's count, the distance and the blind numbers (P_2 in intervals, the ratio and its band)
    "term": {
        6_000: {
            "count": 2_000,
            "distance": 2,
            "pair_period": 73,
            "ratio": 7.6,
            "ratio_band": (5, 11),
            "others": "at 3 Links P_2 about 201 (the ratio 21); 1,500 at 2 Links 19 (2.4); 2,500 at 2 Links 155 (12.7)",
        },
    },
}
STEPPING_GAMMA = {  # GAMMA IS NOT CONSTANT (the owner's word of 15:44 Israel time; Cheshbon 15:50 and 17:25): under node_clock [Gamma_0, 6] the edge 0.2255 Gamma_t rises by 1.353 quanta per interval, so a pixel that does not accumulate dissolves after (c / 0.2255 - Gamma_0) / 6 intervals; at a constant Gamma never. The blind number of the parting world, where no click passes: per engine and Gamma the smaller's count, the node_clock pair and the interval of its dissolution with its band; it enters the expectation under its name before the file takes the pair (Nature24's loader line)
    "term": {
        6_000: {"count": 1_500, "node_clock": [6_000, 6], "dissolution_interval": 109, "band": 15},
    },
}
RECORD_RATIO_BAND = (
    0.15  # the band on the clocks' ratio deep over small (Cheshbon 15:43: 1.2, 1.05 to 1.35)
)
CLOCK_UNIT = 1 << 16  # den of the clock pair [a, den], 2 cos omega_b = a / den (Cheshbon 13:51)
DENOMINATOR = 1024  # every body's phase denominator
FACE_DEPTH = 3
SHAPE = [32, 9, 1]
AXIS_Y = 4  # the bodies' row
LEFT_X = 7  # the smaller body's Node; the deeper at LEFT_X + the distance


class Layout:
    """The numbers of one layout: the universe file's Gamma, the engine's edge and counts, the distances and Cheshbon's numbers per count."""

    def __init__(self, universe: str, engine: str) -> None:
        document = json.loads((ROOT / universe).read_text(encoding="utf-8"))
        self.universe = universe
        self.engine = engine
        self.gamma = int(document["integers"]["node_clock"])
        self.action = int(document["integers"]["quantum_action"])
        if self.gamma not in COUNTS[engine]:
            raise ValueError(
                f"{universe} carries Gamma = {self.gamma:,}: Cheshbon's numbers for world (d) are held for Gamma in {sorted(COUNTS[engine])} alone"
            )
        self.small, self.deep = COUNTS[engine][self.gamma]
        self.edge = EDGE_FRACTION[engine] * self.gamma
        self.horizon = self.gamma // 2
        self.distances = DISTANCES[self.gamma]
        self.dissolution = DISSOLUTION[self.gamma]
        self.stepping = STEPPING_GAMMA.get(engine, {}).get(
            self.gamma
        )  # the rising Gamma's blind number where Cheshbon gives it
        self.hierarchy = HIERARCHY.get(engine, {}).get(
            self.gamma
        )  # the cluster's breathing where Cheshbon's number is given
        self.records = (
            RECORDS[engine] if self.gamma == 24 else None
        )  # the integer generator's table exists for 24 alone

    def numbers(self, count: int) -> dict[str, float | int]:
        """Cheshbon's numbers for one count on this engine; a count without them is refused by name."""
        try:
            return PIXELS[self.engine][count]
        except KeyError:
            raise ValueError(
                f"no clock pair and tail of Cheshbon for the count {count:,} on the engine '{self.engine}'"
            ) from None


def pixel(x: int, count: int) -> dict[str, Any]:
    """A bound body of one Node at rest: the count in the Node, no momentum."""
    return {
        "family": "matter",
        "nodes": [{"node": [x, AXIS_Y, 0], "count": count}],
        "q": 1,  # THE SIGN IS THE BODY'S: a body of the rule's universe is its count at its Node and its q (the owner's word of 14:32 Israel time)
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "phase_denominator": DENOMINATOR,
    }


def world(layout: Layout, distance: int, counts: tuple[int, int] | None = None) -> dict[str, Any]:
    """Two bound bodies of one Node on the row, the smaller at the left and the deeper `distance` Links to its right (or the two counts given, the hierarchy's equal pair); the readings: the matter level at both Nodes every interval, its support and total, both bodies' momentum, the records alive."""
    small, deep = counts or (layout.small, layout.deep)
    right = LEFT_X + distance
    readings: list[dict[str, Any]] = [
        {"name": f"matter_x{x}", "kind": "level", "family": "matter", "node": [x, AXIS_Y, 0], "every": 1}
        for x in (LEFT_X, right)
    ] + [
        {"name": "matter_support", "kind": "support", "family": "matter", "every": 5},
        {"name": "matter_total", "kind": "total", "family": "matter", "every": 5},
        {"name": "left_momentum", "kind": "momentum", "body": 0, "every": 10},
        {"name": "right_momentum", "kind": "momentum", "body": 1, "every": 10},
        {"name": "records_alive", "kind": "alive", "every": 10},
    ]
    return {
        "shape": SHAPE,
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "ticks": TICKS,
        "N": STEPS,
        "engine": ENGINE,
        "universe": layout.universe,
        "measured": [pixel(LEFT_X, small), pixel(right, deep)],
        "detectors": [],
        "readings": readings,
        "face_depth": FACE_DEPTH,
    }


def write_mode(layout: Layout, world_path: Path, document: dict[str, Any]) -> None:
    """The mode file beside the world by the generator of the rule's universe, `tools/pixel_mode.py` (#1417; the owner's word of 14:32 Israel time: the input a count at a Node with the clock pair and the tail's ratio per count, the output the bound state; no mode written by hand)."""
    command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(world_path)]
    for c in sorted({body["nodes"][0]["count"] for body in document["measured"]}):
        numbers = layout.numbers(c)
        command += [
            "--clock",
            str(c),
            str(numbers["a"]),
            str(CLOCK_UNIT),
            "--tail",
            str(c),
            str(numbers["t"]),
        ]
    subprocess.run(command, check=True, cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")})


def amplitudes(layout: Layout, counts: tuple[int, int]) -> dict[str, Any]:
    """The amplitude b of the form per count where Cheshbon's table gives it (6,000: b = isqrt(c T den div (2 den - a)) as the tool writes it); nothing where it does not."""
    given = {str(c): layout.numbers(c)["b"] for c in counts if "b" in layout.numbers(c)}
    return {"amplitude_b_of_the_form": given} if given else {}


def record_expectation(layout: Layout) -> dict[str, Any] | None:
    """Cheshbon's record table for the two bodies (15:43 Israel time): the amplitude b of each, the count the standing record carries (D bar) and its period P, and the clocks' ratio with its band; the run's counts and periods are read against these, not against the file's counts. None where the table is not given (Gamma other than 24)."""
    if layout.records is None:
        return None
    small, deep = RECORD_PAIR[layout.engine]
    rows = {str(b): {"amplitude_b": b, **layout.records[b]} for b in (small, deep)}
    mid = [sum(layout.records[b]["period"]) / 2 for b in (small, deep)]
    ratio = round(mid[1] / mid[0], 2)
    return {
        "row": "THE COUNT IS THE RECORD'S FORM OVER ITS PERIOD (Cheshbon 15:41, the Closer 15:46): the file declares the record by its amplitude b, the count is (the sum of D over the period) div (P T), read once per period; the realisable pixels at 24 are b = 5 (the counts about 8 to 10) and b = 8 (about 12 to 15) under the law; the run's count at each Node over the last period and the period from the level's sign changes are read against this table",
        "bodies": {"small": rows[str(small)], "deep": rows[str(deep)]},
        "clock_ratio_deep_over_small": [
            round(ratio - RECORD_RATIO_BAND, 2),
            ratio,
            round(ratio + RECORD_RATIO_BAND, 2),
        ],
        "band": "one quantum on every count, 10 to 15 percent; the period to one interval",
    }


def stepping_expectation(layout: Layout, parts: bool) -> dict[str, Any]:
    """GAMMA IS NOT CONSTANT, the blind number of the parting world (Cheshbon 17:25 Israel time): with the universe file's node_clock the pair [Gamma_0, 6] the smaller pixel, which no click reaches, dissolves as the edge rises, at the interval given with its band; at a constant Gamma never. Nothing where the table is not given or the world is not the parting."""
    table = layout.stepping
    if table is None or not parts or int(table["count"]) != layout.small:
        return {}
    return {
        "stepping_gamma": {
            "name": "GAMMA IS NOT CONSTANT",
            "row": (
                f"with node_clock {table['node_clock']} the edge 0.2255 Gamma_t rises by about one quantum every interval and the smaller pixel ({layout.small:,}), which no click reaches, "
                f"dissolves at about interval {table['dissolution_interval']} ({table['dissolution_interval'] - table['band']} to {table['dissolution_interval'] + table['band']}); "
                "at a constant Gamma it never dissolves: the one reading that tells a rising Gamma from a constant one (Cheshbon 17:25); the file takes the pair by Nature24's loader line"
            ),
            "node_clock": list(table["node_clock"]),
            "dissolution_interval_of_the_smaller": [
                table["dissolution_interval"] - table["band"],
                table["dissolution_interval"],
                table["dissolution_interval"] + table["band"],
            ],
            "at_constant_gamma": "never",
        }
    }


WORLD_INTEGERS = (
    "momentum_unit",
    "twist_table",
    "quantum_action",
    "least_residues",
    "most_families",
)  # the universe's integers a world carries at its top level when its universe is inline (the loader's keys); width and most_steps are the engine's


def stepping_world(layout: Layout, document: dict[str, Any], step: int) -> dict[str, Any]:
    """The parting under a rising Gamma (GAMMA IS NOT CONSTANT, #1463): the same world with the universe file's rows inline and `node_clock` the pair [Gamma_0, step], the pair living in that key alone (the loader refuses a world-level clock beside a universe file); the rows and the integers copied from the file of record, nothing written by hand."""
    universe = json.loads((ROOT / layout.universe).read_text(encoding="utf-8"))
    stepping = {key: value for key, value in document.items() if key != "universe"}
    stepping["universe"] = universe["families"]
    for key in WORLD_INTEGERS:
        stepping[key] = universe["integers"][key]
    stepping["node_clock"] = [layout.gamma, step]
    return stepping


def write_stepping_mode(
    layout: Layout, world_path: Path, document: dict[str, Any], twin: dict[str, Any]
) -> None:
    """The stepping world's mode file: the bodies by the tool on the twin world that names the universe file (the tool reads the family's pair from the file), stamped with the stepping world's own digest by the loader's `input_digest`; the bodies are the same bodies at the same Nodes."""
    twin_path = world_path.with_name(f"{world_path.stem}.twin.json")
    twin_path.write_text(json.dumps(twin, indent=1) + "\n", encoding="utf-8")
    try:
        write_mode(layout, twin_path, twin)
        mode = json.loads(twin_path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    finally:
        twin_path.unlink(missing_ok=True)
        twin_path.with_suffix(".mode.json").unlink(missing_ok=True)
    mode["world_digest"] = input_digest(document)
    world_path.with_suffix(".mode.json").write_text(json.dumps(mode, indent=1) + "\n", encoding="utf-8")


def stepping_parting_expectation(layout: Layout, step: int, blind: dict[str, Any]) -> dict[str, Any]:
    """The parting's expectation under the rising Gamma: Cheshbon's number (17:25) is the dissolution row itself, the smaller pixel dissolving at the interval given as the edge rises, one record at the end; at a constant Gamma never (the sibling world `part`)."""
    table = layout.stepping
    assert table is not None and int(table["node_clock"][1]) == step
    low = table["dissolution_interval"] - table["band"]
    high = table["dissolution_interval"] + table["band"]
    changed = dict(blind)
    changed["row"] = (
        f"ALGEBRA.md GAMMA IS NOT CONSTANT (Cheshbon 17:25 Israel time): the parting of {layout.small:,} and {layout.deep:,} at {layout.distances['part']} Links "
        f"under node_clock [{layout.gamma:,}, {step}]: no click passes, and the edge 0.2255 Gamma_t rises by about one quantum every interval, so the smaller pixel dissolves "
        f"at about interval {table['dissolution_interval']} ({low} to {high}) with no transfer; at a constant Gamma (the world `part`) it never dissolves"
    )
    changed["blind"] = {
        **blind["blind"],
        "dissolution_intervals": [low, high],
        "records_at_the_end": 1,
        "clicks_expected": "no click: the bodies stand apart beyond the reach; the smaller dissolves under the rising edge alone",
    }
    return changed


def hierarchy_expectation(layout: Layout) -> dict[str, Any]:
    """THE HIERARCHY IS RECURSIVE, the blind expectation of the equal pair (Cheshbon 16:35 Israel time): the breathing period of the pair's total count P_2 against the pixel's period P_1, the ratio about e^(kappa d) with its band; no number of a run."""
    table = layout.hierarchy
    assert table is not None
    count, distance = int(table["count"]), int(table["distance"])
    numbers = layout.numbers(count)
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: THE HIERARCHY IS RECURSIVE; Cheshbon's numbers before the run; no number of a run here",
        "row": (
            f"ALGEBRA.md THE HIERARCHY IS RECURSIVE (Cheshbon 16:35 Israel time): two equal bound bodies of one Node, the counts {count:,} and {count:,}, "
            f"{distance} Links apart on the rule's own universe (Gamma = {layout.gamma:,}, T = {layout.action}): their tails overlap and the clicks run both ways, "
            "so the pair is a cluster one level up whose own tick is the breathing period of its total count; the ratio of that period to the pixel's is the ratio of the ticks between two levels, about e^(kappa d)"
        ),
        "DETECTOR": [],
        "faces": "a face is no body and a click at an open face is no click (Cheshbon 14:55, the Closer 15:02 Israel time)",
        "blind": {
            "row": (
                "Cheshbon's numbers of 16:35 Israel time (2026-09-28): the pixel's period P_1 from its table, the pair's breathing period P_2 about e^(kappa d) times P_1; "
                f"other pairs for the reading: {table['others']}; the band of the ratio is Cheshbon's, one quantum on every count"
            ),
            "name": "THE HIERARCHY IS RECURSIVE",
            "gamma": layout.gamma,
            "edge_quanta_per_node": round(layout.edge, 2),
            "horizon_quanta_per_node": layout.horizon,
            "counts": [count, count],
            "distance_links": distance,
            "tail_kappa_per_link": {str(count): numbers["kappa"]},
            "bound_rotation": {str(count): numbers["omega_b"]},
            "pixel_period_intervals": numbers["period"],
            "pair_breathing_period_intervals": table["pair_period"],
            "period_ratio_pair_over_pixel": table["ratio"],
            "period_ratio_band": list(table["ratio_band"]),
            **amplitudes(layout, (count, count)),
            "first_click_interval": 1,
            "dissolution_intervals": None,
            "clicks_expected": "clicks both ways between two equal pixels; neither dissolves; the pair's total count breathes with the period P_2",
            "records_at_the_end": 2,
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the clicks keep the clicks; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
    }


def expectation(layout: Layout, name: str, distance: int) -> dict[str, Any]:
    """The blind expectation: the law's row in words (THE CLICK JOINS AND PARTS), the numbers Cheshbon gives before the run, the reversible row over the whole run; no number of a run."""
    parts = name == "part" and layout.dissolution["part"] is None
    dissolution = layout.dissolution[name]
    counts = (layout.small, layout.deep)
    periods = [layout.numbers(c)["period"] for c in counts]
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: the row of THE CLICK JOINS AND PARTS; Cheshbon's numbers before the run; no number of a run here",
        "row": (
            f"ALGEBRA.md THE CLICK JOINS AND PARTS: two bound bodies of one Node, the counts {layout.small:,} and {layout.deep:,} "
            f"(the edge {layout.edge:.2f} = {EDGE_FRACTION[layout.engine]} Gamma on the engine '{layout.engine}'), on the rule's own universe "
            f"(Gamma = {layout.gamma:,}, T = {layout.action}, the divisors of the file), {distance} Links apart: "
            + (
                f"beyond the click's reach ln(b_1 b_2 / T) / kappa (about {layout.distances['reach']} Links), so no click passes between them: "
                "THE PARTING, the two records stand and neither count falls under the edge"
                if parts
                else (
                    "their tails overlap (kappa per Link in the blind numbers), the count's line reads the overlap and clicks, "
                    "the tail biased toward the deeper, so the smaller gives quantum by quantum to the deeper until its count falls under the edge "
                    "and dissolves; one record for the joined cluster (the one non-local act)"
                    if name == "join"
                    else f"the tails still overlap (the click's reach under T = 1 is about {layout.distances['reach']} Links), so there is no parting: the slow join, the smaller dissolved within the blind intervals, one record"
                )
            )
        ),
        "DETECTOR": [],
        "faces": "a face is no body and a click at an open face is no click (Cheshbon 14:55, the Closer 15:02 Israel time): a record that reaches a face ends and is not counted; the reading of (d) is the two Nodes' counts and the count's line's moves between them",
        "blind": {
            "row": (
                "Cheshbon's numbers before the run (2026-09-28, 13:03, 13:18 and 15:22 Israel time): under T = 1 every remainder crosses, the first click at interval 1 where the tails overlap; "
                "the smaller dissolves within about two bound periods once the clicks run; the click's reach is ln(b_1 b_2 / T) / kappa Links; "
                "at Gamma = 24 the count is quantised in tenths of the pixel, so every blind number carries a band of one quantum, 10 to 15 percent, "
                "the count breathes by one quantum and a pixel of 6 or 7 is not realisable under the law (Cheshbon 15:22, item 5)"
            ),
            "gamma": layout.gamma,
            "edge_quanta_per_node": round(layout.edge, 2),
            "horizon_quanta_per_node": layout.horizon,
            "counts": list(counts),
            "tail_kappa_per_link": {str(c): layout.numbers(c)["kappa"] for c in counts},
            "bound_rotation": {str(c): layout.numbers(c)["omega_b"] for c in counts},
            "bound_period_intervals": {str(c): layout.numbers(c)["period"] for c in counts},
            **amplitudes(layout, counts),
            "clock_ratio_deep_over_small": round(periods[1] / periods[0], 3),
            "click_reach_links": layout.distances["reach"],
            "first_click_interval": None if parts else 1,
            "dissolution_intervals": None if dissolution is None else list(dissolution),
            "record": record_expectation(layout),
            "clicks_expected": "no click: the bodies stand apart beyond the reach"
            if parts
            else "a run of clicks from the smaller to the deeper until the smaller's record ends",
            "records_at_the_end": 2 if parts else 1,
            **stepping_expectation(layout, parts),
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the clicks keep the clicks; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="the folder the files are written into")
    parser.add_argument(
        "--engine",
        choices=sorted(COUNTS),
        default="today",
        help="the counts and the edge: today (the level read once) or term (the corrected term, the law's form)",
    )
    parser.add_argument(
        "--suffix",
        default="",
        help="a suffix on the world names (join, part, hierarchy), e.g. _6000, so that the files of another Gamma stand beside the files at 24",
    )
    parser.add_argument(
        "--stepping",
        type=int,
        default=0,
        help="with a step above 0, also the parting under a rising Gamma: the world `part<suffix>_stepping` with node_clock [Gamma_0, step] and the universe's rows inline (Cheshbon's blind number in its expectation where the table gives it)",
    )
    parser.add_argument(
        "--universe",
        default=UNIVERSE_OF_RECORD,
        help="the universe file the worlds name, relative to the repository root; Gamma is read from it",
    )
    args = parser.parse_args()
    layout = Layout(args.universe, args.engine)
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    worlds = []
    for name in ("join", "part"):
        distance = layout.distances[name]
        worlds.append(
            (f"{name}{args.suffix}", world(layout, distance), expectation(layout, name, distance))
        )
    if layout.hierarchy is not None:
        pair = (int(layout.hierarchy["count"]), int(layout.hierarchy["count"]))
        document = world(layout, int(layout.hierarchy["distance"]), pair)
        worlds.append((f"hierarchy{args.suffix}", document, hierarchy_expectation(layout)))
    for file_name, document, blind in worlds:
        (folder / f"{file_name}.json").write_text(
            json.dumps(document, indent=1) + "\n", encoding="utf-8"
        )
        write_mode(layout, folder / f"{file_name}.json", document)
        (folder / f"{file_name}.expectation.json").write_text(
            json.dumps(blind, indent=1) + "\n", encoding="utf-8"
        )
    if args.stepping:
        if layout.stepping is None or int(layout.stepping["node_clock"][1]) != args.stepping:
            raise ValueError(
                f"no blind number of Cheshbon for a step of {args.stepping} at Gamma = {layout.gamma:,}"
            )
        twin = world(layout, layout.distances["part"])
        document = stepping_world(layout, twin, args.stepping)
        file_name = f"part{args.suffix}_stepping"
        (folder / f"{file_name}.json").write_text(
            json.dumps(document, indent=1) + "\n", encoding="utf-8"
        )
        write_stepping_mode(layout, folder / f"{file_name}.json", document, twin)
        blind = stepping_parting_expectation(
            layout, args.stepping, expectation(layout, "part", layout.distances["part"])
        )
        (folder / f"{file_name}.expectation.json").write_text(
            json.dumps(blind, indent=1) + "\n", encoding="utf-8"
        )
        worlds.append((file_name, document, blind))
    print(
        json.dumps(
            {
                "universe": layout.universe,
                "gamma": layout.gamma,
                "engine": layout.engine,
                "worlds": [file_name for file_name, _document, _blind in worlds],
                "counts": [layout.small, layout.deep],
                "distances": [layout.distances["join"], layout.distances["part"]],
            }
        )
    )


if __name__ == "__main__":
    main()
