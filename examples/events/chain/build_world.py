"""The chain world's builder (the click's plan of 2026-10-18, the chain world at M = 3 with the six blinds; the owner's word: the files on the branch, the readings the owner's alone): from `design.json` it writes the six worlds, one chain under each of the six signed permutations of the axes that carry a chain to a chain (`chain_x_minus.json` the original, the light along x toward the axis's lower side; `chain_x_plus.json` its mirror image, every coordinate c to 95 - c; the same along y and z), each a chain of 96 Nodes open on its axis with both faces receding, two records of two parts (g at the count 1, e at 0) declared NodeDetectors over three Nodes each, the transition g to e by the light at the declared weight and resonance over a window of 48 from the first lit interval (C2) and the rate e to g as a source in time at the lifetime 48 (C5: dark to its own source), and one packet of the light at k = pi / 4, one whole quantum in the record's own unit (C1), from the Node 84 toward the bodies at 60 to 62 and 20 to 22; the seventh world `chain_detuned.json` (C9 (b), the packet's length: the chain along x with the second body alone and one packet at k = pi / 8 of one quantum, a flat top of 48 Nodes with the raised cosine of 8 beyond it, monochromatic within the window and detuned from the transition, with its eight trial seeds in `detuned_trials.json`), and the blind `expectation.json`, the blinds B1 to B7 as text with no measured number inside them, written before any run and never edited after but for B7's bound, moved by derivation on 2026-10-19 and again under (D) the same day, each move dated inside its row with the former bound kept. With `--modes` it lays the original's light by the generator (tools/pixel_mode.py) and writes the five images' mode files as the original's levels carried by the permutation (`image_mode`), so the six lays are exact images of one another, B5's premise (the carried levels equal the generator's own lay of the mirror packet index by index, the cold reader's check on main of 2026-10-19; the mirror packet's wave is declared with the phase that describes the levels, `mirror_phase`). Every number is the design's; the engine reads none of it.

PYTHONPATH=src python examples/events/chain/build_world.py --modes [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
AXES = ("x", "y", "z")
MINUS, PLUS = "minus", "plus"  # the light toward the axis's lower side (the original) or its upper side


def placed(design: dict, axis: str, toward: str, along: int) -> list[int]:
    """A coordinate along the chain as a Node of the world: on the chain's axis, itself for the light toward the lower side and its mirror image 95 - c for the light toward the upper side, 0 on the two folded axes."""
    node = [0, 0, 0]
    node[AXES.index(axis)] = along if toward == MINUS else design["length"] - 1 - along
    return node


def body(design: dict, number: int, axis: str, toward: str) -> dict:
    """One record of two parts declared a NodeDetector over its Nodes, in the original's order (B5's one exception, the draw's order): g at the count 1, the transition into e by the light, the rate back as a source in time, its own generator seeded by the design."""
    rows, light = design["bodies"], design["light"]["family"]
    first = rows["first"][number]
    return {
        "family": rows["family"],
        "nodes": [
            {"node": placed(design, axis, toward, first + i), "weight": 1} for i in range(rows["nodes"])
        ],
        "parts": [
            {"part": 0, "name": "g", "count": 1},
            {"part": 1, "name": "e", "count": 0},
        ],
        "transitions": [
            {
                "from": "g",
                "to": "e",
                "drive": light,
                "weight": rows["weight"],
                "resonance": design["resonance"],
            }
        ],
        "rates": [{"from": "e", "to": "g", "lifetime": rows["lifetime"], "gives_to": light}],
        "node_detector": {
            **design["generator"],
            "seed": rows["seeds"][number],
        },  # the window derived at load
    }


def mirror_phase(design: dict, toward: str) -> list[int]:
    """The packet's phase as a fraction of the turn: 0 for the original, and for the mirror image the phase at which cos(k c' + phi) at the image Node c' = L - 1 - c equals the original's cos(k c), phi = -(L - 1) k, so the declared wave describes the levels the image carries."""
    if toward == MINUS:
        return [0, 1]
    turns = Fraction(-(design["length"] - 1), 2 * design["light"]["quarters"]) % 1
    return [turns.numerator, turns.denominator]


def packet(design: dict, axis: str, toward: str) -> dict:
    """The one packet of the light: k = pi / quarters toward the bodies, one wavelength of raised cosine beyond its top, the amplitude of one whole quantum in the record's unit."""
    light, top = design["light"], placed(design, axis, toward, design["light"]["top"])
    return {
        "family": light["family"],
        "along": axis,
        "wave": [-1 if toward == MINUS else 1, light["quarters"]],
        "phase": mirror_phase(design, toward),
        "amplitude": light["amplitude"],
        "top": {name: [top[k], top[k]] for k, name in enumerate(AXES)},
        "edge": {name: light["edge"] if name == axis else 0 for name in AXES},
    }


def world_of(design: dict, name: str) -> dict:
    """One world of the design: the chain of the design's length along its axis, open there with both faces receding and folded to one Node on the two other axes, the two bodies and the one packet."""
    axis, toward = design["worlds"][name]
    return {
        "shape": [design["length"] if a == axis else 1 for a in AXES],
        "boundary": {a: "open" if a == axis else "periodic" for a in AXES},
        "face_depth": design["face_depth"],
        "intervals": design["intervals"],
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [
            body(design, number, axis, toward) for number in range(len(design["bodies"]["first"]))
        ],
        "packets": [packet(design, axis, toward)],
        "node_detectors": [],
        "receding": {
            axis: {"sides": ["low", "high"], "largest": design["largest"], "layers": design["layers"]}
        },
    }


def detuned_world(design: dict) -> dict:
    """The detuned packet's world (C9 (b)): the chain along x toward the lower side with the design's one body (`detuned.body`, three Nodes as the others) and one packet of the light at k = pi / `quarters`, a flat top of `top` Nodes with the raised cosine of `edge` beyond, at the amplitude of one quantum in the record's unit at that wave: monochromatic within the window, its passage over the body longer than the window, detuned from the transition's resonance by the dispersion."""
    row, light = design["detuned"], design["light"]
    world = world_of(design, next(iter(design["worlds"])))
    world["bodies"] = [body(design, row["body"], AXES[0], MINUS)]
    world["packets"] = [
        {
            "family": light["family"],
            "along": AXES[0],
            "wave": [-1, row["quarters"]],
            "phase": [0, 1],
            "amplitude": row["amplitude"],
            "top": {"x": list(row["top"]), "y": [0, 0], "z": [0, 0]},
            "edge": {"x": row["edge"], "y": 0, "z": 0},
        }
    ]
    return world


def expectation(design: dict) -> dict:
    """The blind: the seven blinds of the click's plan as text, no measured number inside them (the bounds named by their formulas, D4's number read at the lay into lay_bounds.json before any run)."""
    sides, row = {MINUS: "the axis's lower side", PLUS: "the axis's upper side"}, design["detuned"]
    return {
        "verdict": "NODEDETECTOR",
        "comment": "The chain world of the click's plan: one law-quantum of light at k = pi / 4 on two bodies of three Nodes along a chain of 96 with receding faces, each body taking the light into e over a window of 48 from the first lit interval and giving it back as a source in time at the lifetime 48; the six worlds the chain under the six signed permutations that carry a chain to a chain. The six blinds below are the conservation section's, each a conservation to the remainder's bound and bit for bit under the inverse, written before any run and never edited after; the readings are the owner's, appended to blind_and_reading.md after the runs (tools/run_inputs.py on each world, tools/meeting_trials.py on the design's seeds, tools/back_in_time.py over the inverse's intervals).",
        "worlds": {
            name: {"axis": axis, "light_toward": sides[toward]}
            for name, (axis, toward) in design["worlds"].items()
        },
        "detuned_world": {
            "name": row["name"],
            "axis": AXES[0],
            "light_toward": sides[MINUS],
            "wave": f"pi / {row['quarters']}",
            "trials": len(row["seeds"]),
            "seeds": "detuned_trials.json, for tools/meeting_trials.py",
        },
        "trials": len(design["seeds"]),
        "intervals": design["trial_intervals"],
        "inverse_intervals": design["inverse_intervals"],
        "lay_bounds": "lay_bounds.json, the lay's numbers read from the loaded worlds before any run (lay_bounds.py): the light's unit W_rec and its count, each body's amplitudes and D4's bound per axis",
        "blind": {
            "B1 count": {
                "reading": "at every credit line labelled NODEDETECTOR (an absorption naming `absorbed`, an emission naming `emitted`) the change of the light's count, `left` against the line before, and of the body's parts' counts, `kept`; the light's share in whole quanta over the board at every interval, Q_light over W_rec (the books' `quanta`), against its count c_light (the books' `count`)",
                "blind": "dc_light = -1 at every absorption and +1 at every emission, dc_e = -dc_g = +1 at an absorption and -1 at an emission, exactly, at every click of the run; Q_light / W_rec within 1 / 2 of c_light at every interval outside the front's span (the erasing front after a count reaches 0, D6) and outside a source's span (the lay's increments, D7)",
                "status": "the books' integers (D2, D3, D4 and D7 of the conservation section); derived, no measurement inside",
                "fence": "clicks and the books",
            },
            "B2 energy": {
                "reading": "the board's form Q summed over every family (the books' `share` in the current's unit) before and after the pair of one absorption and one emission; the light's invariant I = Q_light / W_rec at the lay and after the source's span",
                "blind": "under C1 the form after the pair stands within D7's bound of its value before, one unit W_rec exchanged each way and the label carrying no form (D4); I_light = 1 within D7's bound at the lay (the books' count 1 read from the loaded world, lay_bounds.json) and again after the span of the emission",
                "status": "C1 with D4 and D7; the bound 3 den SUM_t (|a_t| + 1 / 4) over the laid form, read on the source's increments",
                "fence": "lattice (the books' share), beside the clicks",
            },
            "B3 momentum": {
                "reading": "at every absorption the credit line's `momentum` (the piece p_a, C4), `twist` (n_a) and `shortfall` (s_a, C3); the body's own P_a, its record's momentum terms over its Nodes in T's unit (`readings.momentum_of`, `twist.scaled`), at the click and after its emission; the light's P_a over the board before and after the source's span",
                "blind": "p_a = gain_a + s_a exactly at every absorption, the probe's integers (D5); P_body kept through the emission within D4's bound computed at the lay and written in lay_bounds.json before the run (C3); the source's residue, the light's P after the span against its value before, within D7's bound named to the source's asymmetry; the open board's identity D8 holds term by term in the packet_emission folder's kind and is not this folder's",
                "status": "D4, D5, D7 and D8 with C3 and C4",
                "fence": "clicks (the credit line's three readings) and a lattice reading (P over the body's Nodes)",
            },
            "B4 the inverse": {
                "reading": "tools/back_in_time.py over 40 intervals of chain_x_minus through its first absorption and the emission that follows, the verdict",
                "blind": "MATCH bit for bit: every array returns through the click's two writes, the fold and the lay lines, the inverse of the one act",
                "status": "the lay act's inverse (`lay.written`, one `lay` line per Node changed; tools/back_in_time, `crossed`)",
                "fence": "the tool's verdict, LATTICE",
            },
            "B5 the 48": {
                "reading": "the six worlds run over their intervals (tools/run_inputs.py), each output's click lines, every level and every remainder brought back by the inverse of its signed permutation: the coordinate on the chain's axis to itself for a world toward the lower side and to 95 less itself for a world toward the upper side, the vector components with the axis's sign",
                "blind": "every click line, level and remainder equal under the six signed permutations, with the draw's order the one named exception: `drawn` takes the first index whose cumulative weight exceeds the pick in the list's order and a tie the lower index (the law's L812, untouched), so the image worlds carry the declaration's lists, the Nodes, the directions and the outcomes, as the images in the original's order, and with that the comparison is exact",
                "status": "equivariance under the 48 to the bit (L408's acts; the face on a Port set, the lay a scalar per line, the fold about the click's Node: C6)",
                "fence": "the output lines and the arrays",
            },
            "B6 anticoincidence": {
                "reading": "the anticoincidence folder's trials (tools/meeting_trials.py on examples/events/anticoincidence/one_photon.json over its design's seeds): P(A only), P(B only), P(both) and alpha",
                "blind": "P(both) = 0 exactly, alpha = 0, |P(A only) - P(B only)| <= 2 sqrt(s (1 - s) / N) with s the anticoincidence folder's blind and N its trials; the identities D3 (the hole) and D6 (the front) per click",
                "status": "S.57 (b), the credit's one draw per record; D3 and D6",
                "fence": "clicks (the anticoincidence folder's own)",
            },
            "B7 the line shape": {
                "reading": "chain_detuned over its intervals for each seed of detuned_trials.json (tools/meeting_trials.py with that file as the design): the trials with an absorption at the body, the credit lines naming `absorbed`",
                "blind": "absorbed in at most 1 of the 8 trials (the bound moved with the rule on 2026-10-19 under (D), the atom branch, as the first correction was moved, by derivation and no fit to a reading: the body's window is the packet's passage derived at load, W = 116 over its three Nodes, so the detuned turn is the envelope's spectral weight at the detuning over the whole passage, Delta = 0.2198 per interval, v_g 0.570, the envelope read at kappa = 0.3857 per Node, the weight 0.0657 over the three Nodes, the resonant turn 1.115 rad at the declared weight 6 over three Nodes and the detuned turn 0.073 rad, the chance sin^2 = 5.4 x 10^-3 per trial, 0.043 absorptions expected in eight and P(2 or more) 8.0 x 10^-4; the record of the declared window 48: at most 4 of the 8 trials, the bound corrected by derivation on 2026-10-19 from at most 1 of 8 after the first run had read 3 of 8, the correction the derivation's and no fit to a reading, the sinc weighing the turn and not the chance, the turn per flat window 1.27 rad at one Node at the declared weight 6, 0.206 rad under the sinc's 0.162, sin^2 0.042 at one Node and 0.111 with the body's projection over its three Nodes, two windows per passage, 0.19 per trial, 1.5 of 8 expected, P(at most 4 of 8) = 0.99, under the first bound a lawful engine failing about half the time, and the reading 3 of 8 at the declared 48 the narrower line's record): the packet at k = pi / 8 stands detuned from the transition at [5414, 6000] (k = pi / 4) by Delta = omega(pi / 4) - omega(pi / 8) per interval, and the window's sinc at Delta W / 2 weighs each window's turn by sinc^2 (C9: the line shape is the window's own, the width 1 / W; at the declared 48 Delta W / 2 = 5.3 and sinc^2 below 1 / 30); the packet's flat top of 48 Nodes with the raised cosine of 8 beyond is monochromatic within the window, its passage over the body at the group velocity 116 intervals, the one window under (D) where the declared 48 opened two or three; a packet of one wavelength at pi / 8, the 17-Node kind of the other worlds, would reach the transition with its spectrum and be absorbed at the weight's sin^2, so a detuning claim needs the packet's length W Nodes or more (C9 (b), the declaration)",
                "status": "C9, the window's sinc; the declaration (b) on the packet's length; written before any run; the bound moved with the rule on 2026-10-19 ((D), the window the passage derived at load), the engine's reading at W 116 none of eight pinned in tests/test_the_chain_world.py",
                "fence": "clicks",
            },
        },
        "status": design["status"],
    }


def image_mode(design: dict, name: str, world: dict, original: dict) -> dict:
    """An image world's mode file from the original's: the same levels at the image Nodes, each flat x-major index of the original chain (its coordinate along x) carried to the image Node's flat index by the permutation, the entries sorted by index; the digest the image world's own (`world_files.input_digest`)."""
    from event_universe.world_files import input_digest

    axis, toward = design["worlds"][name]
    shape = world["shape"]

    def carried(level: dict) -> dict:
        pairs = []
        for at, value in zip(level["at"], level["values"], strict=True):
            x, y, z = placed(design, axis, toward, int(at))
            pairs.append((x * shape[1] * shape[2] + y * shape[2] + z, value))
        pairs.sort()
        return {"at": [at for at, _ in pairs], "values": [value for _, value in pairs]}

    packets = [
        {**entry, "moving": {key: carried(level) for key, level in entry["moving"].items()}}
        for entry in original["packets"]
    ]
    return {"world_digest": input_digest(world), "bodies": [], "packets": packets}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument(
        "--modes",
        action="store_true",
        help="lay the original by the generator, the images by the permutation",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    original, first = None, next(iter(design["worlds"]))
    for name in design["worlds"]:
        path, world = args.folder / f"{name}.json", world_of(design, name)
        path.write_text(json.dumps(world) + "\n", encoding="utf-8")
        if args.modes and name == first:
            import pixel_mode

            pixel_mode.main(["--input", str(path)])
            original = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
        elif args.modes:
            assert original is not None
            mode = json.dumps(image_mode(design, name, world, original), separators=(",", ":"))
            path.with_suffix(".mode.json").write_text(mode + "\n", encoding="utf-8")
    row, path = design["detuned"], args.folder / f"{design['detuned']['name']}.json"
    path.write_text(json.dumps(detuned_world(design)) + "\n", encoding="utf-8")
    if args.modes:
        import pixel_mode

        pixel_mode.main(["--input", str(path)])
    trials = {"seeds": row["seeds"], "trial_intervals": design["trial_intervals"]}
    (args.folder / "detuned_trials.json").write_text(json.dumps(trials) + "\n", encoding="utf-8")
    (args.folder / "expectation.json").write_text(
        json.dumps(expectation(design), indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
