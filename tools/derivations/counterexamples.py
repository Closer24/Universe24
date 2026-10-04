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
        "So Lorentzs group and the continuums rotations are no symmet",
        rows.cube_group_commutes_with_rule3,
    ),
    (
        "Beyond P the mode at wave number pi on every axis grows with",
        rows.guard_bounds_the_pi_mode_at_fixed_coefficients,
    ),
    (
        "In the clicks there are conservations other than the boards",
        forms.boards_conservations_are_the_form_and_the_wronskian,
    ),
    (
        "The change is 0 at paces fixed in time uniform or not for th",
        forms.weighted_form_is_exact_at_static_paces,
    ),
    (
        "The integer step subtracts the remainder term deltaiDeltaai",
        forms.integer_step_subtracts_the_remainder_term,
    ),
    (
        "Over one step of Rule3 the shares rational value before its",
        forms.shares_change_is_the_six_weighted_currents,
    ),
    (
        "So over any region the total share changes only by the weigh",
        forms.regions_share_changes_by_boundary_currents,
    ),
    (
        "The total share of a closed or periodic lattice is nonnega",
        forms.total_share_nonnegative_inside_the_guard,
    ),
    ("The direction of time belongs to the clicks and not to the b", rows.the_step_is_a_bijection),
    (
        "The line without its division conserves it exactly with the",
        forms.wronskian_conserved_by_the_line_at_static_paces,
    ),
    (
        "Its total over the lattice is invariant under any change o",
        forms.wronskian_total_under_a_change_of_paces,
    ),
    ("The exact angle of the shears is 2arctanL p0 2Gamma2 which i", rows.shears_exact_angle),
    (
        "And a pair is one laid record its phase a shared classical v",
        rows.chsh_of_local_responses_at_most_two,
    ),
    ("So the rule carries exactly three exact massive rotations 2c", rows.three_exact_massive_rotations),
    (
        "itemm A free record keeps its wave number Rule3 is invariant",
        rows.plane_wave_keeps_its_wave_number,
    ),
    ("tab:results: The rules acts form no product of levels", forms.acts_form_no_product_of_levels),
    (
        "tab:results: A conserved form at static paces with the weights 1 pi2 its",
        forms.weighted_form_is_exact_at_static_paces,
    ),
    (
        "tab:results: The count is the records share the rational total share is n",
        derived.count_is_the_share,
    ),
    ("tab:results: Three exact massive rotations", rows.three_exact_massive_rotations),
    (
        "tab:adds: The bands inertia and kinetic scale m 3tanomega0 cm2 omega0",
        derived.bands_inertia_and_kinetic_scale,
    ),
    (
        "What the clicks structure derives of the masses is in S53 th",
        derived.bands_inertia_and_kinetic_scale,
    ),
    (
        "tab:adds: The postNewtonian parameters with the gap gammaK den num bet",
        derived.ppn_parameters_against_kepler,
    ),
    (
        "tab:results: The same forms against Keplers potential gammaK betaK and al",
        derived.ppn_parameters_against_kepler,
    ),
    (
        "tab:adds: Yilmazs exponential metric N2 e2U h2 e2U gamma beta 1 exactl",
        derived.exponential_metric_ppn,
    ),
    (
        "Lights index e2U places the photon sphere at r 2m with U m r",
        derived.shadow_capture_radius_is_2em,
    ),
    (
        "tab:adds: The shadows capture radius b 2em against Schwarzschilds 3sqr",
        derived.shadow_capture_radius_is_2em,
    ),
    (
        "tab:results: De Broglie the fall Newtons pull the contents index for ever",
        derived.fall_coefficient_and_de_broglie,
    ),
    (
        "itemh De Broglies relation for the band for the fringe spaci",
        derived.fall_coefficient_and_de_broglie,
    ),
    ("The declared pairs 478 169 sits below 2sqrt 2 because the an", derived.bells_478_over_169),
    ("The same credit on four lines gives the threequantum GHZ cor", derived.ghz_mermin_minus_four),
    ("tab:clicks: GHZ three quanta", derived.ghz_mermin_minus_four),
    (
        "The level slows the clock by the potential Phi ell Gamma U w",
        derived.clock_pace_is_the_exponential,
    ),
    ("tab:results: A holders reach from its gap Yukawas form", derived.yukawa_reach_from_the_gap),
    (
        "tab:results: Lights speed 1 sqrt 3 Links per interval its dispersion and",
        derived.light_speed_and_dispersion,
    ),
    (
        "tab:adds: The moving clocks fourth order omega0suma na4tanomega0 cotom",
        derived.moving_clock_fourth_order,
    ),
    (
        "tab:results: The moving clock its fourth order and its kinetic scale cm L",
        derived.moving_clock_fourth_order,
    ),
    ("iteme The moving clock the bands kinetic scale and the fourt", derived.moving_clock_fourth_order),
    (
        "tab:adds: The frozen content Uf tfrac12ln2Gamma Gamma 2ln 2Gamma level",
        derived.frozen_content_level,
    ),
    (
        "tab:adds: The clicks booking identity Delta Q wx vx b with the records",
        derived.booking_identity_delta_q,
    ),
    ("tab:results: The gravitational redshift z fomega0U", derived.redshift_f_omega0),
)

# the second set (the main text's and the tables' rows left without a function, the supplement's S.n rows: a new
# function where the claim is new, the existing function where an S.n row states its claim)
REGISTRY_TWO: tuple[tuple[str, Callable[[], Row]], ...] = (
    ("The record is the top mode of Rule3s symmetric form at the p", rows_two.record_is_the_top_mode),
    ("S.13", rows_two.record_is_the_top_mode),
    ("S.1", rows_two.plane_wave_exact_at_the_paces),
    ("S.2", rows_two.lights_index_at_the_composed_paces),
    ("S.7", rows_two.stress_reading_of_a_plane_wave),
    ("S.14", rows_two.adiabatic_invariant_and_the_drift),
    ("S.17", rows_two.cross_current_of_two_standing_records),
    (
        "A body with two bound modes omegai omegaj transfers between",
        rows_two.rabi_transfer_and_the_resonance,
    ),
    ("S.16", rows_two.rabi_transfer_and_the_resonance),
    ("S.43", rows_two.rabi_transfer_and_the_resonance),
    ("tab:clicks: The absorption line", rows_two.rabi_transfer_and_the_resonance),
    (
        "tab:results: A bodys clicks no light from a steady rotation light at a br",
        rows_two.steady_rotation_writes_no_light,
    ),
    ("S.42", rows_two.steady_rotation_writes_no_light),
    ("tab:clicks: Emission", rows_two.guides_lay_of_one_quantum),
    (
        "tab:results: The stability of a body under the dilation to first order in",
        rows_two.stability_under_the_dilation,
    ),
    ("S.48", rows_two.proofs_of_the_theorems),
    (
        "So the odd lines are sourced by the halved current over the",
        forms_two.odd_lines_sourced_by_the_halved_current,
    ),
    (
        "tab:results: The force between moving charges Coulombs over gamma",
        forms_two.force_between_moving_charges,
    ),
    ("tab:clicks: Magnetism", forms_two.force_between_moving_charges),
    ("S.33", forms_two.force_between_moving_charges),
    ("tab:clicks: A bodys count in clicks", forms_two.counts_inflow_with_the_factor_squared),
    ("tab:clicks: No signalling", forms_two.no_signalling_marginals),
    ("tab:clicks: The whichway sum", forms_two.which_way_sum),
    ("S.57", forms_two.one_photon_on_two_bodies),
    ("S.8", forms_two.regions_reading_factor_and_the_draws_scatter),
    (
        "The three are one as the gap closes Its slow limit at small",
        derived_two.three_are_one_as_the_gap_closes,
    ),
    ("S.63", derived_two.three_are_one_as_the_gap_closes),
    (
        "Its bending is exact in the gap while the orbits second orde",
        derived_two.bending_exact_in_the_gap,
    ),
    (
        "tab:results: The bending which fixed the one assumption the perihelion th",
        derived_two.bending_exact_in_the_gap,
    ),
    ("tab:clicks: The bendings clicks", derived_two.bending_exact_in_the_gap),
    ("S.20", derived_two.bending_exact_in_the_gap),
    (
        "itemp The lens a content bends light and matter alike by one",
        derived_two.lens_one_formula_for_light_and_matter,
    ),
    (
        "tab:adds: The lens Eq one formula for light and matter for light exact",
        derived_two.lens_one_formula_for_light_and_matter,
    ),
    ("S.28", derived_two.lens_one_formula_for_light_and_matter),
    (
        "tab:adds: The gravity of light a light packet pulls at 1 times E c2 ag",
        derived_two.gravity_of_light_factor_one,
    ),
    (
        "tab:adds: The finestructure constants form alpha 3sqrt 3 8pik Gamma Es",
        derived_two.alpha_laws_form_from_the_write_weight,
    ),
    (
        "tab:results: alpha 3sqrt 3 8pik Gamma Es between two quanta k the sign ho",
        derived_two.alpha_laws_form_from_the_write_weight,
    ),
    ("S.26", derived_two.alpha_laws_form_from_the_write_weight),
    ("S.54", derived_two.alpha_laws_form_from_the_write_weight),
    (
        "tab:adds: The clusters deceleration q0 Omegam 2 0 at z ll 1 bound or f",
        derived_two.clusters_deceleration,
    ),
    ("S.29", derived_two.clusters_deceleration),
    (
        "tab:adds: A bodys binding per quantum bounded by 076CW Gamma E at one",
        derived_two.binding_bound_by_watsons_integral,
    ),
    ("S.38", derived_two.binding_bound_by_watsons_integral),
    ("tab:results: Newtons pull the clocks G and Keplers G", derived_two.newtons_pull_and_the_two_g),
    ("S.25", derived_two.newtons_pull_and_the_two_g),
    (
        "tab:results: The two clocks shift alike the findings against nature of Se",
        derived_two.two_clocks_shift_alike,
    ),
    ("tab:clicks: The clocks click rate", derived_two.two_clocks_shift_alike),
    ("S.31", derived_two.two_clocks_shift_alike),
    ("S.41", derived_two.two_clocks_shift_alike),
    ("S.58", derived_two.push_on_a_moving_record),
    ("S.23", derived_two.near_field_minima_of_the_two_slits),
    ("S.24", derived_two.links_bound_from_the_dispersion),
    ("S.27", derived_two.electron_as_the_free_matter_quantum),
    ("S.35", derived_two.preferred_frame_parameter),
    ("S.39", derived_two.gapped_holders_kernel),
    ("S.36", derived_two.five_carrier_forms),
    ("S.44", derived_two.two_forces_between_quanta),
    ("S.45", derived_two.nuclear_holders_threshold),
    ("S.46", derived_two.atom_with_the_nucleus_angle),
    ("S.59", derived_two.zeno_curve),
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
    ("S.40", derived.ghz_mermin_minus_four),
    ("S.47", derived.fall_coefficient_and_de_broglie),
    ("S.50", derived.booking_identity_delta_q),
    ("S.51", rows.chsh_of_local_responses_at_most_two),
    ("S.53", derived.bands_inertia_and_kinetic_scale),
    ("S.55", forms.boards_conservations_are_the_form_and_the_wronskian),
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
