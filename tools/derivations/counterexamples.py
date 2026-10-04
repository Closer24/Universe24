"""The breaker of the paper's claims (the method of 2026-10-04): every row of paper/claims_breakers.json of the kind (a) whose breaker is pure algebra of Rule3's line, tried inside the claim's stated condition and outside it, on the smallest configuration. The rows are in counterexample_rows.py (the step's theorems), counterexample_forms.py (the conserved form, the Wronskian, the share and the flux) and counterexample_derived.py (the derived rows of the abstract and the tables); this module holds the registry keyed exactly by the JSON's keys and the report.

The state of a row: `green` where the claim holds inside and breaks outside (or states no condition to step outside of), `BROKE` where it fails inside, `FENCE` where it holds inside and nothing breaks outside (a condition the claim does not need). A red row changes nothing of the paper: it is reported for the hands. Every number of the law is rule3.py's, every step the derivation modules'; floats stand only where the claim itself is a float (a series, an arctan, a root).

Usage: `python tools/derivations/counterexamples.py` prints the Markdown table (key, state, witness) and exits non-zero if any row is BROKE or FENCE.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import counterexample_derived as derived  # noqa: E402
import counterexample_forms as forms  # noqa: E402
import counterexample_rows as rows  # noqa: E402
import rule3  # noqa: E402, F401  (the derivations' root; tests/test_derivations_lean_on_rule3_alone.py)
from counterexample_rows import Row  # noqa: E402

REGISTRY: tuple[tuple[str, Callable[[], Row]], ...] = (
    (
        "So Lorentzs group and the continuums rotations are no symmet",
        rows.cube_group_commutes_with_rule3,
    ),
    (
        "Beyond P the extreme mode grows without bound the mode at wa",
        rows.guard_bounds_the_pi_mode_at_fixed_coefficients,
    ),
    (
        "In the clicks there are conservations other than the GameBoa",
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
        "The total share of any GameBoard whose Links read the same f",
        forms.total_share_nonnegative_inside_the_guard,
    ),
    ("The direction of time belongs to the clicks and not to the G", rows.the_step_is_a_bijection),
    (
        "The line without its division conserves it exactly with the",
        forms.wronskian_conserved_by_the_line_at_static_paces,
    ),
    (
        "Its total over the GameBoard is invariant under any change o",
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
        "tab:adds: The postNewtonian parameters with the gap for 0 num le den g",
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


def state_of(row: Row) -> str:
    if not row.holds_inside:
        return "BROKE"
    if row.breaks_outside is False:
        return "FENCE"
    return "green"


def run() -> list[tuple[str, str, str]]:
    """Every row of the registry under its JSON key: (key, state, witness)."""
    found = []
    for key, function in REGISTRY:
        row = function()
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
