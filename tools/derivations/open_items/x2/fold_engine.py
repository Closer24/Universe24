"""Hand X2: every function of src/event_universe mapped to the place it folds into, summed by target.

Targets: ROTATE (rotate(row)), WRITE (write(rows)), SWAP (swap(row)), CLICK (click(rows): the read, the pick, the
take, the lay, the credit, the refusals), PRIM (the Node's integer primitives the four share: the carried division,
the roundings, the root search, the paces, the Port's shift, the line's three integers), LOOP (the interval's order
and the state), LOADER (the two files in and the numbers derived once), WRITER (the lines out), DECODER (names, den's
circle, species: tools/), OUT (dead under the laws, or the host's). The mapping is the hand's reading of every function
(the report names the reason per group); the counts are the syntax tree's (functions.py).

Usage: python fold_engine.py engine_functions.json fold_engine.json
"""
import json
import sys
from pathlib import Path

SPEC = {
    "act.py": {"click": "CLICK", "written": "CLICK", "affordable": "CLICK", "born_table": "OUT", "list_walls": "LOADER",
               "born_list": "OUT", "born_items": "CLICK"},
    "board_readings.py": {"UniformMode": "WRITER", "horizon_ports": "OUT", "stresses": "WRITE", "sense_currents": "WRITE",
                          "sense_fluxes": "WRITE", "uniform_mode": "WRITER", "Eras": "WRITER", "volume_sums": "WRITER",
                          "eras": "WRITER", "row_level": "ROTATE"},
    "bookings.py": {"sources_of": "OUT", "record_lines": "OUT", "booked_of": "WRITE", "booked_sources": "OUT"},
    "bound_body.py": {"beats_of": "CLICK", "body_records": "OUT", "bodies_closing": "CLICK"},
    "conversion.py": {"sine_of": "LOADER", "gaussian": "OUT", "candidates": "LOADER", "baryons": "OUT", "kept": "OUT",
                      "conjugate_exact": "OUT", "times": "OUT", "lists_of": "OUT", "walls_of": "LOADER",
                      "meeting_reducible": "OUT", "birth_of": "LOADER"},
    "core/paces.py": {"rounded": "PRIM", "odd_rounded": "PRIM", "sine_den": "LOADER", "clock_alone": "PRIM", "Side": "PRIM",
                      "Side.reach": "PRIM", "sides": "PRIM", "side_of": "PRIM", "clock": "PRIM", "link_pace": "PRIM",
                      "frozen_content": "LOADER", "looked_up": "PRIM", "clock_of": "PRIM", "link_pace_of": "PRIM",
                      "node_paces": "PRIM", "axis_pace": "WRITE", "write_factor": "WRITE", "write_factor_terms": "WRITE",
                      "at_nodes": "PRIM", "within_width": "WRITE", "exponent_products": "WRITER", "turn_factor": "WRITE",
                      "clear_memo": "LOOP"},
    "core/ports.py": {"shifted": "PRIM", "arrival": "PRIM"},
    "core/rule3.py": {"Rule": "ROTATE", "wall_of": "ROTATE", "mass": "ROTATE", "rule_integers": "ROTATE", "coefficients": "ROTATE",
                      "link_factor": "ROTATE", "carried_division": "PRIM", "flux_total": "ROTATE", "rule3": "ROTATE",
                      "division_forward": "PRIM", "division_back": "PRIM", "largest_below": "PRIM", "form_term": "CLICK",
                      "partial_rooms": "LOADER"},
    "credit.py": {"Books": "OUT", "Books.of": "OUT", "born": "OUT", "counted": "OUT", "count_of": "OUT", "record_unit": "LOADER",
                  "support_of": "OUT"},
    "digits.py": {"ported": "PRIM", "frame_of": "PRIM", "ports_of": "PRIM", "opposite": "PRIM", "picked": "PRIM", "ruled": "OUT",
                  "rule_and_pairs": "OUT", "digits_of": "CLICK", "odd_line": "CLICK", "at_origin": "CLICK", "lattice_of": "CLICK",
                  "read_of": "CLICK"},
    "emission.py": {"emitted_lines": "CLICK", "laid_by_count": "CLICK", "born_point": "OUT", "unborn_point": "OUT"},
    "features/click/__init__.py": {"Refused": "CLICK", "Refused.__init__": "CLICK", "read_number": "CLICK", "drawn_from": "CLICK",
                                   "squared": "CLICK", "amplitude": "CLICK"},
    "features/currents/__init__.py": {"Levels": "PRIM", "Neighbours": "PRIM", "current": "PRIM", "momentum_terms": "CLICK",
                                      "tension": "WRITE", "stress": "WRITE"},
    "features/held_write/__init__.py": {"held_write": "WRITE"},
    "features/phase/__init__.py": {"unit": "ROTATE", "D": "ROTATE", "K0": "ROTATE", "half_wall": "ROTATE", "seed": "LOADER",
                                   "act": "ROTATE", "chosen": "ROTATE", "iterate": "ROTATE", "Orbit": "LOADER",
                                   "Orbit.__init__": "LOADER", "Orbit.carried_to": "LOADER", "Orbit.pairs_at": "LOADER",
                                   "seeded": "OUT", "orbit_of": "OUT", "read": "ROTATE", "signed_read": "ROTATE",
                                   "signed_rounded": "PRIM", "fold": "ROTATE", "amplitude": "LOADER", "quarter_turn": "OUT"},
    "features/read/__init__.py": {"read_again": "OUT", "plain": "OUT", "content_of": "ROTATE", "link_tension": "ROTATE",
                                  "link_tensions": "ROTATE", "link_factors": "ROTATE", "axis_paces": "WRITE",
                                  "stability_bound": "LOADER", "edge_squared": "LOADER", "edge_of": "LOADER",
                                  "at_the_node": "LOADER", "paces_guard": "LOADER"},
    "features/start/__init__.py": "OUT",
    "features/start/rests.py": "OUT",
    "features/volume/__init__.py": {"clock_zero": "LOADER", "volume_of": "LOADER", "bounds_of": "LOADER", "fill_of": "OUT",
                                    "level_of": "ROTATE", "searched_levels": "ROTATE", "at_start": "OUT", "resting": "OUT",
                                    "started": "OUT", "levels_read": "ROTATE"},
    "flux.py": {"link_fluxes": "ROTATE", "turned_link_fluxes": "ROTATE", "gathered_line": "ROTATE", "step_line": "ROTATE",
                "step_momentum": "ROTATE", "gathered_plane": "ROTATE", "step_plane": "ROTATE", "step_family": "ROTATE",
                "pairs_of": "ROTATE", "step_records": "LOOP"},
    "frames.py": {"frames_of": "ROTATE"},
    "hole.py": {"Take": "CLICK", "walls_of": "CLICK", "moved": "CLICK", "taken_at": "CLICK", "take_of": "CLICK"},
    "lattice.py": {"Lattice": "LOOP", "Lattice.__init__": "LOADER", "Lattice.half_wall": "PRIM", "Lattice.walls": "WRITE",
                   "Lattice.mask": "PRIM", "Lattice.start": "OUT", "Lattice.born_point": "OUT", "Lattice.unborn_point": "OUT",
                   "Lattice.lines_of": "OUT", "Lattice.read": "ROTATE", "Lattice.rulers": "WRITE", "Lattice.share_of": "CLICK",
                   "Lattice.quanta": "CLICK", "Lattice.total_share": "OUT", "Lattice.books": "OUT", "Lattice.stepped": "LOOP",
                   "Lattice.record": "OUT", "Lattice.advanced_to_the_close": "LOOP", "Lattice.closed_after": "LOOP",
                   "Lattice.step": "LOOP", "Lattice.held_write": "WRITE", "Lattice.bounded": "OUT", "Lattice.booked_back": "WRITE",
                   "Lattice.step_inverse": "LOOP"},
    "lay.py": {"shares_of": "OUT", "division_act": "OUT", "guarded": "OUT", "corrected": "OUT", "written": "CLICK", "laid": "CLICK"},
    "loader/charge.py": {"pythagorean_readers": "LOADER"},
    "loader/circle.py": "DECODER",
    "loader/derived.py": {"Row": "LOADER", "Read": "OUT", "FamilyRule": "OUT", "FamilyRule.held": "OUT", "FamilyRule.write": "OUT",
                          "FamilyRule.quanta": "OUT", "FamilyRule.width": "OUT", "FamilyRule.planes": "OUT", "FamilyRule.laid": "OUT",
                          "FamilyRule.power": "OUT", "FamilyRule.exponent": "OUT", "FamilyRule.axes": "OUT", "FamilyRule.record": "OUT",
                          "FamilyRule.link_read": "OUT", "exponent_of": "WRITER", "turns": "OUT", "charged": "OUT",
                          "children_of": "OUT", "with_records": "OUT", "HeldWrite": "LOADER", "with_reads": "OUT",
                          "family_rules": "OUT", "alpha_of": "LOADER", "shared_clock": "OUT", "weight_of": "OUT",
                          "readers_of": "OUT", "count_wall": "LOADER", "held_write_of": "LOADER", "largest_of": "LOADER",
                          "amplitude_bound": "LOADER", "bound_under_rooms": "LOADER"},
    "loader/interval.py": {"volume_rows": "OUT"},
    "loader/keys.py": "LOADER",
    "loader/rooms.py": "LOADER",
    "loader/seed.py": {"seed_of": "LOADER"},
    "loader/universe.py": {"gone_refused": "LOADER", "sign_holder": "LOADER", "volume_holder": "LOADER", "volume_pair": "LOADER",
                           "rows_of": "LOADER", "resolved": "OUT", "universe_of": "LOADER"},
    "loader/world.py": "LOADER",
    "meeting.py": {"stepped": "LOOP"},
    "meeting_back.py": {"named": "OUT", "arrays_of": "OUT", "snapshot": "OUT", "first_difference": "OUT", "node_of": "CLICK",
                        "same_lay": "CLICK", "crossed": "CLICK", "logged": "CLICK"},
    "meeting_board.py": {"child_of": "CLICK", "drawn_among": "CLICK", "meetings": "CLICK", "closed": "CLICK", "holes_of": "CLICK",
                         "refused_by": "CLICK", "Clock": "CLICK", "agreed": "CLICK", "readings_at": "CLICK"},
    "node.py": {"read_key": "OUT", "read_lines": "ROTATE", "read": "ROTATE", "rulers": "WRITE", "rulers_of": "WRITE",
                "turning": "ROTATE", "sign_holder": "OUT", "clocked_potentials": "WRITE", "phase_counts": "ROTATE",
                "phase_carried": "ROTATE", "phase_rows": "WRITE", "phased": "LOOP", "guarded": "LOADER", "least_pace": "OUT",
                "rule_of": "ROTATE", "held_write_at": "WRITE", "seed_phases": "LOADER", "phase_act": "LOOP"},
    "plane.py": {"link_levels": "ROTATE", "link_wall": "ROTATE", "link_guard": "LOADER", "frame_signs": "ROTATE",
                 "phase_links": "ROTATE", "sign_pairs": "ROTATE", "link_pairs": "ROTATE", "turned_room": "LOADER"},
    "readings.py": {"framed": "ROTATE", "at": "PRIM", "slices": "PRIM", "ports": "PRIM", "sense_current_of": "WRITE",
                    "currents_of": "WRITE", "momentum_of": "CLICK", "stresses_of": "WRITE", "axis_sources_of": "WRITE",
                    "axis_neighbours": "WRITE"},
    "records.py": {"NodeState": "LOOP", "Record": "PRIM", "level_at": "PRIM", "record_slice": "OUT", "rows_total": "OUT",
                   "row_levels": "OUT", "form": "WRITE", "wronskian": "WRITE", "well": "WRITER", "rulers_write_factor": "WRITE",
                   "reads_content": "OUT", "wall_rulers": "OUT", "scaled_sum": "WRITE", "write_sources": "WRITE",
                   "divided_walls": "LOADER", "exact": "PRIM", "walls_at": "LOADER", "pressure_term": "WRITE",
                   "axis_positions": "OUT", "largest": "OUT", "zeros": "PRIM", "full": "PRIM", "empty_record": "LOADER",
                   "phase_row": "LOADER", "phase_lines": "LOADER", "born_lines": "OUT", "complement": "SWAP",
                   "write_origins": "LOADER", "empty_state": "LOADER"},
    "registry.py": "OUT",
    "reports.py": {"credit": "WRITER", "lay": "WRITER", "book": "WRITER", "point_of": "CLICK", "birth_line": "WRITER",
                   "refused_line": "WRITER"},
    "seed.py": {"drift_of": "LOADER", "uniform_seed": "LOADER"},
    "share.py": {"frozen": "PRIM", "over_pace": "CLICK", "share": "CLICK", "family_share": "CLICK", "board_share": "CLICK",
                 "quanta_of": "CLICK", "half_action": "OUT", "charge_of": "OUT", "charged": "OUT", "by_charge": "OUT",
                 "count_read": "OUT"},
    "shear.py": {"carried": "OUT", "shear_lines": "OUT", "written": "WRITE", "stepped": "ROTATE", "inverted": "ROTATE", "born": "LOADER"},
    "slabs.py": "OUT",
    "swap.py": {"kept": "LOOP", "at_top": "SWAP", "floor_of": "SWAP", "at_floor": "SWAP", "swapped": "SWAP", "swapped_phases": "SWAP",
                "acted": "SWAP", "stepped": "LOOP", "inverted": "LOOP"},
    "take.py": {"Item": "CLICK", "below_quantum": "CLICK"},
    "walls.py": {"sourced": "OUT"},
    "world_files.py": "LOADER",
}
TARGETS = ("ROTATE", "WRITE", "SWAP", "CLICK", "PRIM", "LOOP", "LOADER", "WRITER", "DECODER", "OUT")


def main():
    report = json.load(open(sys.argv[1], encoding="utf-8"))
    out = {t: {"functions": 0, "lines": 0, "kind_branches": 0, "extra_branches": 0, "places": []} for t in TARGETS}
    unmapped = []
    for rel, entry in report["files"].items():
        spec = SPEC.get(rel)
        for fn in entry["functions"]:
            name = fn["name"]
            if spec is None:
                if entry["functions"]:
                    unmapped.append((rel, name))
                continue
            target = spec if isinstance(spec, str) else spec.get(name)
            if target is None:
                unmapped.append((rel, name))
                continue
            is_class = "." not in name and name[0].isupper()
            # a class's lines are its methods' lines: count the class once (its own lines beyond its methods are the header)
            methods = [f for f in entry["functions"] if f["name"].startswith(name + ".")]
            lines = fn["lines"] - sum(m["lines"] for m in methods) if is_class and methods else fn["lines"]
            kind = len(fn["kind_branches"]) - sum(len(m["kind_branches"]) for m in methods) if is_class and methods else len(fn["kind_branches"])
            extra = len(fn["extra_branches"]) - sum(len(m["extra_branches"]) for m in methods) if is_class and methods else len(fn["extra_branches"])
            o = out[target]
            o["functions"] += 1
            o["lines"] += lines
            o["kind_branches"] += kind
            o["extra_branches"] += extra
            o["places"].append(f"{rel}:{name} {fn['start']}-{fn['end']} ({lines}) K{kind} X{extra}")
    # the module-level lines outside any function (docstrings, imports, constants)
    in_functions = sum(o["lines"] for o in out.values())
    total = report["totals"]["lines"]
    summary = {t: {k: v for k, v in o.items() if k != "places"} for t, o in out.items()}
    summary["module level (docstrings, imports, constants)"] = {"lines": total - in_functions}
    summary["total lines"] = total
    summary["unmapped"] = unmapped
    four = {t: summary[t]["functions"] for t in ("ROTATE", "WRITE", "SWAP", "CLICK")}
    summary["places folding into the four"] = {**four, "sum": sum(four.values())}
    summary["kind branches by target"] = {t: summary[t]["kind_branches"] for t in TARGETS}
    Path(sys.argv[2]).write_text(json.dumps({"summary": summary, "places": {t: o["places"] for t, o in out.items()}}, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
