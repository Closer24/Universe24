"""The breaker of the paper's claims (the method of 2026-10-04): every row of paper/claims_breakers.json of the kind (a) whose breaker is pure algebra of Rule3's line, tried inside the claim's stated condition and outside it, on the smallest configuration. The rows are in counterexample_rows.py (the step's theorems), counterexample_forms.py (the conserved form, the Wronskian, the share and the flux), counterexample_derived.py (the derived rows of the abstract and the tables) and the second set, counterexample_rows_two.py (the top mode, the plane wave at the paces, the bodies' lines), counterexample_forms_two.py (the currents, the credit and the screen) and counterexample_derived_two.py (the weak field and the constants); this module holds the registry keyed exactly by the JSON's keys, one function serving every key that states its claim, and the report.

The state of a row: `green` where the claim holds inside and breaks outside (or states no condition to step outside of), `BROKE` where it fails inside, `FENCE` where it holds inside and nothing breaks outside (a condition the claim does not need). A red row changes nothing of the paper: it is reported for the hands. Every number of the law is rule3.py's, every step the derivation modules'; floats stand only where the claim itself is a float (a series, an arctan, a root).

Usage: `python tools/derivations/counterexamples.py` prints the Markdown table (key, state, witness) and exits non-zero if any row is BROKE or FENCE.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import counterexample_derived as derived  # noqa: E402
import counterexample_derived_two as derived_two  # noqa: E402
import counterexample_forms as forms  # noqa: E402
import counterexample_forms_two as forms_two  # noqa: E402
import counterexample_rows as rows  # noqa: E402
import counterexample_rows_two as rows_two  # noqa: E402
import rule3  # noqa: E402, F401  (the derivations' root; tests/test_derivations_lean_on_rule3_alone.py)
from counterexample_rows import Row  # noqa: E402

REGISTRY_ONE: tuple[tuple[str, Callable[[], Row]], ...] = (
    (
        "No boost no rotation beyond the cubes 24 and no scaling is i",
        rows.cube_group_commutes_with_rule3,
    ),
    (
        "tab:claims: The guard is the CourantFriedrichsLewy condition under the c",
        rows.guard_bounds_the_pi_mode_at_fixed_coefficients,
    ),
    (
        "long:In the clicks there are conservations other than the lattice",
        forms.boards_conservations_are_the_form_and_the_wronskian,
    ),
    (
        "long:The change is 0 at paces fixed in time uniform or not for th",
        forms.weighted_form_is_exact_at_static_paces,
    ),
    (
        "With the rounding each Nodes remainder adds the term r r wpi",
        forms.integer_step_subtracts_the_remainder_term,
    ),
    (
        "Over one step of Rule3 the rational quantum share at a Node",
        forms.shares_change_is_the_six_weighted_currents,
    ),
    (
        "long:So over any region the total share changes only by the weigh",
        forms.regions_share_changes_by_boundary_currents,
    ),
    (
        "The total quantum share of any lattice whose Links read the",
        forms.total_share_nonnegative_inside_the_guard,
    ),
    ("The lattice holds only the future and has no arrow Rule3 bei", rows.the_step_is_a_bijection),
    (
        "long:The line without its division conserves it exactly with the",
        forms.wronskian_conserved_by_the_line_at_static_paces,
    ),
    (
        "long:Its total over the lattice is invariant under any change of",
        forms.wronskian_total_under_a_change_of_paces,
    ),
    ("long:The exact angle of the shears is 2arctanL p0 2Gamma2 which i", rows.shears_exact_angle),
    (
        "long:And a pair is one laid record its phase a shared classical v",
        rows.chsh_of_local_responses_at_most_two,
    ),
    ("The line of one Node at rest anext 2cosomega0anow abefore is", rows.three_exact_massive_rotations),
    (
        "long:itemm A free record keeps its wave number Rule3 is invariant",
        rows.plane_wave_keeps_its_wave_number,
    ),
    (
        "what the acts can form on the infinite lattice for one field",
        forms.acts_form_no_product_of_levels,
    ),
    (
        "tab:claims: A conserved form at static paces with the weights 1 pi2 its",
        forms.weighted_form_is_exact_at_static_paces,
    ),
    (
        "tab:claims: The count is the configurations quantum share the rational t",
        derived.count_is_the_share,
    ),
    ("long:tab:results: Three exact massive rotations", rows.three_exact_massive_rotations),
    (
        "item The bands inertia and kinetic scale m 3tanomega0 cm2 om",
        derived.bands_inertia_and_kinetic_scale,
    ),
    (
        "long:What the clicks structure derives of the masses is in S53 th",
        derived.bands_inertia_and_kinetic_scale,
    ),
    (
        "item The postNewtonian parameters with the gap for 0 num le",
        derived.ppn_parameters_against_kepler,
    ),
    (
        "tab:claims: The two potentials and the Kepler map the moving clock at cm",
        derived.ppn_parameters_against_kepler,
    ),
    (
        "item The exponential metric reached from the composed paces",
        derived.exponential_metric_ppn,
    ),
    (
        "long:Lights index e2U places the photon sphere at r 2m with U m r",
        derived.shadow_capture_radius_is_2em,
    ),
    (
        "item The shadows capture radius b 2em against Schwarzschilds",
        derived.shadow_capture_radius_is_2em,
    ),
    (
        "long:tab:results: De Broglie the fall Newtons pull the contents index for ever",
        derived.fall_coefficient_and_de_broglie,
    ),
    (
        "long:itemh De Broglies relation for the band for the fringe spaci",
        derived.fall_coefficient_and_de_broglie,
    ),
    (
        "tab:claims: Bells E cos 2a b S 478 169 Tsirelsons 2 GreenbergerHorneZeil",
        derived.bells_478_over_169,
    ),
    ("The same counting rule on four lines gives the threequantum", derived.ghz_mermin_minus_four),
    ("long:tab:clicks: GHZ three quanta", derived.ghz_mermin_minus_four),
    (
        "long:The level slows the clock by the potential Phi ell Gamma U w",
        derived.clock_pace_is_the_exponential,
    ),
    (
        "tab:claims: A potential fields reach from its gap Yukawas form Poissons",
        derived.yukawa_reach_from_the_gap,
    ),
    (
        "tab:claims: An event spreads by Rule3 at one Link per interval the causa",
        derived.light_speed_and_dispersion,
    ),
    (
        "item The moving clocks fourth order omega0suma na4tanomega0",
        derived.moving_clock_fourth_order,
    ),
    (
        "long:tab:results: The moving clock its fourth order and its kinetic scale cm L",
        derived.moving_clock_fourth_order,
    ),
    ("item The moving clock fv 1 v2 2cm2 2omega0 sin 2omega0v4 8cm", derived.moving_clock_fourth_order),
    (
        "long:tab:adds: The frozen content Uf tfrac12ln2Gamma Gamma 2ln 2Gamma level",
        derived.frozen_content_level,
    ),
    (
        "item The clicks identity under a write the long versions boo",
        derived.booking_identity_delta_q,
    ),
    ("item The clocks rate 1 fomega0U f 21 cosomega0 omega0sinomeg", derived.redshift_f_omega0),
)

# the second set (the main text's and the tables' rows left without a function, the supplement's S.n rows: a new
# function where the claim is new, the existing function where an S.n row states its claim)
REGISTRY_TWO: tuple[tuple[str, Callable[[], Row]], ...] = (
    (
        "long:The record is the top mode of Rule3s symmetric form at the p",
        rows_two.record_is_the_top_mode,
    ),
    ("S.13", rows_two.record_is_the_top_mode),
    ("S.1", rows_two.plane_wave_exact_at_the_paces),
    ("S.2", rows_two.lights_index_at_the_composed_paces),
    ("S.7", rows_two.stress_reading_of_a_plane_wave),
    ("S.14", rows_two.adiabatic_invariant_and_the_drift),
    ("S.17", rows_two.cross_current_of_two_standing_records),
    (
        "long:A body with two bound modes omegai omegaj transfers between",
        rows_two.rabi_transfer_and_the_resonance,
    ),
    ("S.16", rows_two.rabi_transfer_and_the_resonance),
    ("S.41", rows_two.rabi_transfer_and_the_resonance),
    ("long:tab:clicks: The absorption line", rows_two.rabi_transfer_and_the_resonance),
    (
        "item A steady rotation writes no light a breathing bound sta",
        rows_two.steady_rotation_writes_no_light,
    ),
    ("S.40", rows_two.steady_rotation_writes_no_light),
    ("long:tab:clicks: Emission", rows_two.guides_lay_of_one_quantum),
    (
        "the stable bound state under the dilation and to first order",
        rows_two.stability_under_the_dilation,
    ),
    ("S.45", rows_two.proofs_of_the_theorems),
    (
        "long:So the odd lines are sourced by the halved current over the",
        forms_two.odd_lines_sourced_by_the_halved_current,
    ),
    (
        "item Coulombs force over gammaL the Lorentz factor between m",
        forms_two.force_between_moving_charges,
    ),
    ("long:tab:clicks: Magnetism", forms_two.force_between_moving_charges),
    ("S.33", forms_two.force_between_moving_charges),
    ("long:tab:clicks: A bodys count in clicks", forms_two.counts_inflow_with_the_factor_squared),
    ("long:tab:clicks: No signalling", forms_two.no_signalling_marginals),
    ("long:tab:clicks: The whichway sum", forms_two.which_way_sum),
    ("long:S.57", forms_two.one_photon_on_two_bodies),
    ("S.8", forms_two.regions_reading_factor_and_the_draws_scatter),
    (
        "long:The three are one as the gap closes Its slow limit at small",
        derived_two.three_are_one_as_the_gap_closes,
    ),
    ("S.53", derived_two.three_are_one_as_the_gap_closes),
    (
        "long:Its bending is exact in the gap while the orbits second orde",
        derived_two.bending_exact_in_the_gap,
    ),
    (
        "tab:claims: The exponential metric gamma beta 1 in U the bending 4Ub Sha",
        derived_two.bending_exact_in_the_gap,
    ),
    ("long:tab:clicks: The bendings clicks", derived_two.bending_exact_in_the_gap),
    ("S.20", derived_two.bending_exact_in_the_gap),
    (
        "item The lens Eq with the chromatic term k2 e6U e2U 24 S28 i",
        derived_two.lens_one_formula_for_light_and_matter,
    ),
    (
        "item The lens Eq one formula for light and matter natures fo",
        derived_two.lens_one_formula_for_light_and_matter,
    ),
    ("S.28", derived_two.lens_one_formula_for_light_and_matter),
    (
        "item The gravity of light a light packets integrated write a",
        derived_two.gravity_of_light_factor_one,
    ),
    (
        "item The finestructure constants form alpha 3sqrt 3 8pik Gam",
        derived_two.alpha_laws_form_from_the_write_weight,
    ),
    (
        "item alpha 3sqrt 3 8pik Gamma Es k declared charge universal",
        derived_two.alpha_laws_form_from_the_write_weight,
    ),
    ("S.26", derived_two.alpha_laws_form_from_the_write_weight),
    ("S.48", derived_two.alpha_laws_form_from_the_write_weight),
    (
        "item The clusters deceleration q0 Omegam 2 0 at z ll 1 bound",
        derived_two.clusters_deceleration,
    ),
    ("S.29", derived_two.clusters_deceleration),
    (
        "long:tab:adds: A bodys binding per quantum bounded by 076CW Gamma E at one",
        derived_two.binding_bound_by_watsons_integral,
    ),
    ("S.36", derived_two.binding_bound_by_watsons_integral),
    (
        "item Newtons pull 1 r2 and G as a reading Eq Keplers G at 08",
        derived_two.newtons_pull_and_the_two_g,
    ),
    ("S.25", derived_two.newtons_pull_and_the_two_g),
    (
        "long:tab:results: The two clocks shift alike the findings against nature of Se",
        derived_two.two_clocks_shift_alike,
    ),
    ("long:tab:clicks: The clocks click rate", derived_two.two_clocks_shift_alike),
    ("S.31", derived_two.two_clocks_shift_alike),
    ("S.39", derived_two.two_clocks_shift_alike),
    ("S.51", derived_two.push_on_a_moving_record),
    ("S.23", derived_two.near_field_minima_of_the_two_slits),
    ("S.24", derived_two.links_bound_from_the_dispersion),
    ("S.27", derived_two.electron_as_the_free_matter_quantum),
    ("S.35", derived_two.preferred_frame_parameter),
    ("S.37", derived_two.gapped_holders_kernel),
    ("long:S.36", derived_two.five_carrier_forms),
    ("S.42", derived_two.two_forces_between_quanta),
    ("long:S.45", derived_two.nuclear_holders_threshold),
    ("S.43", derived_two.atom_with_the_nucleus_angle),
    ("long:S.59", derived_two.zeno_curve),
    ("S.54", derived_two.lattice_scale_quartic_coefficient),
    ("S.3", rows.guard_bounds_the_pi_mode_at_fixed_coefficients),
    ("S.4", rows.cube_group_commutes_with_rule3),
    ("S.5", forms.shares_change_is_the_six_weighted_currents),
    ("S.6", forms.total_share_nonnegative_inside_the_guard),
    ("S.9", forms.wronskian_conserved_by_the_line_at_static_paces),
    ("S.10", derived.bells_478_over_169),
    ("S.11", derived.yukawa_reach_from_the_gap),
    ("S.12", derived.light_speed_and_dispersion),
    ("S.15", derived.redshift_f_omega0),
    ("S.18", derived.fall_coefficient_and_de_broglie),
    ("S.19", derived.ppn_parameters_against_kepler),
    ("S.21", derived.moving_clock_fourth_order),
    ("S.22", derived.fall_coefficient_and_de_broglie),
    ("S.30", derived.shadow_capture_radius_is_2em),
    ("S.32", forms.weighted_form_is_exact_at_static_paces),
    ("S.34", derived.exponential_metric_ppn),
    ("S.38", derived.ghz_mermin_minus_four),
    ("S.44", derived.fall_coefficient_and_de_broglie),
    ("S.46", derived.booking_identity_delta_q),
    ("S.47", rows.chsh_of_local_responses_at_most_two),
    ("long:S.53", derived.bands_inertia_and_kinetic_scale),
    ("S.49", forms.boards_conservations_are_the_form_and_the_wronskian),
)
REGISTRY = REGISTRY_ONE + REGISTRY_TWO


def state_of(row: Row) -> str:
    if not row.holds_inside:
        return "BROKE"
    if row.breaks_outside is False:
        return "FENCE"
    return "green"


def run() -> list[tuple[str, str, str]]:
    """Every row of the registry under its JSON key: (key, state, witness); a function serving several keys runs once."""
    found, computed = [], {}
    for key, function in REGISTRY:
        if function not in computed:  # one function serves every key that states its claim, run once
            computed[function] = function()
        row = computed[function]
        found.append((key, state_of(row), row.witness))
    return found


def main() -> int:
    results = run()
    print("| key | state | witness |")
    print("|---|---|---|")
    for key, state, witness in results:
        print(f"| {key} | {state} | {witness.replace('|', '/')} |")
    red = [key for key, state, _ in results if state != "green"]
    print(f"\n{len(results)} rows, {len(results) - len(red)} green" + (f", red: {red}" if red else ""))
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
