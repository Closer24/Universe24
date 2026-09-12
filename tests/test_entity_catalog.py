"""Descriptive reference coverage and rejection boundaries, without physical laws."""

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe.entity_catalog import validate_catalog

CATALOG = Path(__file__).resolve().parents[1] / "examples/known-entities/catalog.json"


def _property(**values):
    return {"status": "measured", "sources": ["reference"], **values}


def _particle(identity, charge, partner, properties, *, field="matter_field", spin=1):
    return {
        "id": identity,
        "label": identity,
        "physical_status": "test_fixture",
        "sources": ["reference"],
        "field_ids": [field],
        "interaction_ids": ["pair_conversion"],
        "antiparticle_id": partner,
        "electric_charge_thirds": charge,
        "twice_spin": spin,
        "rest_mass_relation": "equal_positive_pair" if charge else "massless",
        "physical_properties": properties,
    }


@pytest.fixture
def catalog():
    """Small synthetic values isolate validation from changing reference tables."""
    return {
        "catalog_version": 2,
        "purpose": "physical_reference",
        "scope": {"coverage": "A synthetic validation fixture, not a physics table."},
        "notes": ["No dynamic rule is selected by these descriptive records."],
        "sources": {"reference": {"title": "Fixture source", "url": "https://example.org/data"}},
        "field_entities": [
            {
                "id": identity,
                "label": identity,
                "physical_status": "test_fixture",
                "sources": ["reference"],
                "excitation_ids": excitations,
                "interaction_ids": ["pair_conversion"],
                "physical_properties": {"category": _property(value="reference field")},
            }
            for identity, excitations in (
                ("matter_field", ["negative", "positive"]),
                ("radiation_field", ["radiation"]),
            )
        ],
        "particle_entities": [
            _particle(
                "negative",
                -3,
                "positive",
                {
                    "mass": _property(
                        value_decimal="1.25",
                        unit="MeV/c^2",
                        context="Synthetic rest mass.",
                        uncertainty_decimal="0.05",
                        uncertainty_kind="standard uncertainty",
                    ),
                    "charge": _property(metadata_key="electric_charge_thirds"),
                },
            ),
            _particle(
                "positive",
                3,
                "negative",
                {
                    "mass": _property(status="reference", entity_id="negative"),
                    "charge": _property(metadata_key="electric_charge_thirds"),
                },
            ),
            _particle(
                "radiation",
                0,
                "radiation",
                {
                    "mass": _property(value_decimal="0", unit="MeV/c^2", context="Massless fixture."),
                },
                field="radiation_field",
                spin=2,
            ),
        ],
        "disturbance_families": [
            {
                "id": "bound_states",
                "label": "Bound states",
                "physical_status": "test_fixture",
                "sources": ["reference"],
                "field_ids": ["matter_field", "radiation_field"],
                "interaction_ids": ["pair_conversion"],
                "physical_properties": {
                    "composition": _property(
                        status="context_dependent",
                        context="State-dependent composition.",
                        constituent_ids=["negative", "positive"],
                    )
                },
            }
        ],
        "interaction_families": [
            {
                "id": "pair_conversion",
                "label": "Pair conversion",
                "physical_status": "test_fixture",
                "claim_level": "descriptive_only",
                "participant_ids": [
                    "negative",
                    "positive",
                    "radiation",
                    "matter_field",
                    "radiation_field",
                    "bound_states",
                ],
                "mediator_ids": ["radiation"],
                "conditions": ["The interaction requires a permitted initial state."],
                "sources": ["reference"],
            }
        ],
        "representative_channels": [
            {
                "id": "pair_to_radiation",
                "interaction_id": "pair_conversion",
                "physical_status": "test_fixture",
                "claim_level": "descriptive_only",
                "incoming_ids": ["negative", "positive"],
                "outgoing_ids": ["radiation", "radiation"],
                "conditions": ["Available energy and all conserved quantities must permit it."],
                "sources": ["reference"],
            }
        ],
        "examples": [],
    }


def _replace(document, path, value):
    target = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def test_descriptive_validation_preserves_data_and_channel_multiplicity(catalog):
    before = deepcopy(catalog)
    assert validate_catalog(catalog) is None
    assert catalog == before
    assert catalog["representative_channels"][0]["outgoing_ids"] == ["radiation", "radiation"]


@pytest.mark.parametrize(
    "path",
    [
        ("field_entities", 0, "sources"),
        ("particle_entities", 0, "physical_properties", "mass", "sources"),
        ("field_entities", 0, "excitation_ids"),
        ("particle_entities", 0, "field_ids"),
        ("disturbance_families", 0, "field_ids"),
        ("particle_entities", 0, "interaction_ids"),
        ("interaction_families", 0, "participant_ids"),
        ("interaction_families", 0, "mediator_ids"),
        ("representative_channels", 0, "incoming_ids"),
        ("representative_channels", 0, "outgoing_ids"),
        ("representative_channels", 0, "sources"),
        ("disturbance_families", 0, "physical_properties", "composition", "constituent_ids"),
    ],
)
def test_unknown_reference_is_rejected_at_each_relation_boundary(catalog, path):
    _replace(catalog, path, ["missing"])
    with pytest.raises(ValueError, match="unknown reference|reciprocal"):
        validate_catalog(catalog)


@pytest.mark.parametrize("section", ["field_entities", "particle_entities", "disturbance_families"])
def test_duplicate_entity_identity_is_rejected(catalog, section):
    catalog[section].append(deepcopy(catalog[section][0]))
    with pytest.raises(ValueError, match="duplicate"):
        validate_catalog(catalog)


def test_identity_cannot_be_shared_between_fields_and_particles(catalog):
    catalog["field_entities"][0]["id"] = "negative"
    with pytest.raises(ValueError, match="unique across"):
        validate_catalog(catalog)


@pytest.mark.parametrize(
    "path",
    [
        ("field_entities", 0, "excitation_ids"),
        ("particle_entities", 0, "field_ids"),
        ("particle_entities", 0, "interaction_ids"),
    ],
)
def test_one_way_entity_relationship_is_rejected(catalog, path):
    _replace(catalog, path, [])
    with pytest.raises(ValueError, match="reciprocal"):
        validate_catalog(catalog)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("electric_charge_thirds", 0),
        ("twice_spin", 2),
        ("rest_mass_relation", "different_mass"),
        ("antiparticle_id", "radiation"),
    ],
)
def test_conjugate_identity_cannot_silently_change_charge_spin_or_mass(catalog, key, value):
    catalog["particle_entities"][0][key] = value
    with pytest.raises(ValueError):
        validate_catalog(catalog)


@pytest.mark.parametrize("key", ["electric_charge_thirds", "twice_spin"])
def test_intrinsic_integer_attributes_reject_boolean_values(catalog, key):
    catalog["particle_entities"][0][key] = True
    with pytest.raises(ValueError, match="integer"):
        validate_catalog(catalog)


@pytest.mark.parametrize("value", [1.25, True, "NaN", "Infinity", "1e-3", " 1.25", "01.25"])
def test_measurements_require_unambiguous_finite_decimal_strings(catalog, value):
    catalog["particle_entities"][0]["physical_properties"]["mass"]["value_decimal"] = value
    with pytest.raises(ValueError, match="finite decimal string"):
        validate_catalog(catalog)


@pytest.mark.parametrize("key", ["unit", "context", "uncertainty_kind"])
def test_measurement_requires_units_context_and_uncertainty_interpretation(catalog, key):
    del catalog["particle_entities"][0]["physical_properties"]["mass"][key]
    with pytest.raises(ValueError, match="measurement"):
        validate_catalog(catalog)


@pytest.mark.parametrize("status", ["unknown", "not_applicable"])
def test_unknown_property_cannot_be_replaced_by_numerical_zero(catalog, status):
    catalog["particle_entities"][0]["physical_properties"]["mass"].update(
        status=status,
        value_decimal="0",
    )
    with pytest.raises(ValueError, match="cannot invent numerical"):
        validate_catalog(catalog)


@pytest.mark.parametrize("change", ["negative_uncertainty", "missing_value", "reversed_bounds"])
def test_measurement_uncertainty_and_bounds_are_consistent(catalog, change):
    mass = catalog["particle_entities"][0]["physical_properties"]["mass"]
    if change == "negative_uncertainty":
        mass["uncertainty_decimal"] = "-0.05"
    elif change == "missing_value":
        del mass["value_decimal"]
    else:
        mass.update(lower_bound_decimal="2", upper_bound_decimal="1")
    with pytest.raises(ValueError, match="uncertainty|bounds"):
        validate_catalog(catalog)


def test_an_upper_limit_does_not_require_an_invented_central_measurement(catalog):
    catalog["particle_entities"][0]["physical_properties"]["mass"] = _property(
        status="upper_limit",
        upper_bound_decimal="2",
        unit="MeV/c^2",
        context="Synthetic bound at the stated confidence level.",
        confidence_level_percent=90,
    )
    validate_catalog(catalog)


@pytest.mark.parametrize("value", [-1, 0, 100, 101, True, "ninety", [90]])
def test_confidence_level_must_be_a_valid_percentage(catalog, value):
    catalog["particle_entities"][0]["physical_properties"]["mass"]["confidence_level_percent"] = value
    with pytest.raises(ValueError, match="confidence"):
        validate_catalog(catalog)


def test_alias_must_target_the_same_existing_property(catalog):
    catalog["particle_entities"][1]["physical_properties"]["mass"]["entity_id"] = "matter_field"
    with pytest.raises(ValueError, match="same property"):
        validate_catalog(catalog)


def test_mass_aliases_cannot_form_a_cycle(catalog):
    catalog["particle_entities"][0]["physical_properties"]["mass"] = _property(
        status="reference",
        entity_id="positive",
    )
    with pytest.raises(ValueError, match="cyclic"):
        validate_catalog(catalog)


def test_alias_cannot_override_its_canonical_value(catalog):
    catalog["particle_entities"][1]["physical_properties"]["mass"]["value"] = "different mass"
    with pytest.raises(ValueError, match="cannot override"):
        validate_catalog(catalog)


def test_intrinsic_metadata_reference_has_only_one_value(catalog):
    catalog["particle_entities"][0]["physical_properties"]["charge"]["value"] = 3
    with pytest.raises(ValueError, match="one canonical value"):
        validate_catalog(catalog)


@pytest.mark.parametrize(
    "path",
    [
        ("particle_entities", 0, "physical_properties", "mass", "status"),
        ("particle_entities", 0, "antiparticle_id"),
        ("representative_channels", 0, "interaction_id"),
    ],
)
def test_nontext_discriminators_are_reported_as_validation_errors(catalog, path):
    _replace(catalog, path, [])
    with pytest.raises(ValueError):
        validate_catalog(catalog)


def test_channel_charge_must_balance_even_when_all_participants_are_known(catalog):
    catalog["representative_channels"][0]["incoming_ids"] = ["negative"]
    with pytest.raises(ValueError, match="charge is not balanced"):
        validate_catalog(catalog)


def test_declared_interaction_does_not_allow_channels_outside_its_participants(catalog):
    catalog["interaction_families"][0]["participant_ids"].remove("bound_states")
    catalog["disturbance_families"][0]["interaction_ids"] = []
    catalog["representative_channels"][0]["incoming_ids"] = ["bound_states"]
    with pytest.raises(ValueError, match="outside its interaction family"):
        validate_catalog(catalog)


@pytest.mark.parametrize("section", ["interaction_families", "representative_channels"])
@pytest.mark.parametrize(("key", "value"), [("conditions", []), ("claim_level", "derived_law")])
def test_possible_interactions_require_conditions_and_no_claim_of_a_derived_law(
    catalog,
    section,
    key,
    value,
):
    catalog[section][0][key] = value
    with pytest.raises(ValueError, match="descriptive_only"):
        validate_catalog(catalog)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("expression", {"field": "charge"}),
        ("formula", "a supplied physical update"),
        ("op", "add"),
        ("updates", []),
        ("transport", {"rate": 1}),
        ("hamiltonian", [[0, 1], [1, 0]]),
        ("rates", {"decay": 1}),
        ("executable_profile", {}),
        ("quantum_profile", {}),
    ],
)
def test_executable_content_is_rejected_even_when_nested_in_descriptive_scope(catalog, key, value):
    catalog["scope"]["extra"] = [{"nested": {key: value}}]
    with pytest.raises(ValueError, match="executable rules or formulas"):
        validate_catalog(catalog)


def test_cli_rejects_duplicate_json_keys_before_validation(tmp_path):
    invalid = tmp_path / "duplicate.json"
    invalid.write_text('{"catalog_version": 2, "catalog_version": 2}', encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "event_universe.entity_catalog", str(invalid)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "duplicate" in result.stderr.lower()


def test_shipped_catalog_is_a_valid_descriptive_reference():
    validate_catalog(json.loads(CATALOG.read_text(encoding="utf-8")))


def test_cli_validates_the_shipped_reference_without_loading_laws():
    result = subprocess.run(
        [sys.executable, "-m", "event_universe.entity_catalog", str(CATALOG)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "no simulation laws were loaded" in result.stdout


@pytest.fixture
def shipped():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_shipped_inventory_covers_standard_model_species_and_distinct_conjugates(shipped):
    fields = {row["id"] for row in shipped["field_entities"]}
    assert {
        "electromagnetic_field",
        "strong_field",
        "weak_field",
        "higgs_field",
        "quark_fields",
        "charged_lepton_fields",
        "neutrino_fields",
        "gravity_metric",
    } <= fields
    particles = {row["id"]: row for row in shipped["particle_entities"]}
    for flavor in ("up", "down", "charm", "strange", "top", "bottom"):
        assert {f"{flavor}_quark", f"anti{flavor}_quark"} <= particles.keys()
    assert {
        "electron",
        "positron",
        "muon",
        "antimuon",
        "tau",
        "antitau",
        "photon",
        "gluon_multiplet",
        "w_plus",
        "w_minus",
        "z_boson",
        "higgs_boson",
        "proton",
        "antiproton",
        "neutron",
        "antineutron",
    } <= particles.keys()
    for flavor in ("electron", "muon", "tau"):
        assert {f"{flavor}_neutrino", f"{flavor}_antineutrino"} <= particles.keys()
    assert particles["neutron"]["antiparticle_id"] == "antineutron"
    assert particles["photon"]["antiparticle_id"] == "photon"
    assert particles["gluon_multiplet"]["antiparticle_id"] == "gluon_multiplet"


def test_composite_collective_and_gravitational_disturbances_have_explicit_family_coverage(shipped):
    families = {row["id"] for row in shipped["disturbance_families"]}
    assert {
        "mesons",
        "baryons_and_resonances",
        "exotic_hadrons",
        "nuclei_and_isotopes",
        "atoms_and_ions",
        "molecules",
        "antimatter_composites",
        "bulk_matter",
        "acoustic_and_elastic_waves",
        "plasma_waves",
        "condensed_matter_quasiparticles",
        "coherent_condensates",
        "gravitational_waves",
        "compact_gravitating_bodies",
    } <= families
    for section in ("field_entities", "particle_entities", "disturbance_families"):
        for row in shipped[section]:
            assert row["physical_properties"]
            assert row["sources"]
            assert row["interaction_ids"] or row["physical_status"] == "project_hypothesis"
            for prop in row["physical_properties"].values():
                assert prop["status"] and prop["sources"]


def test_neutrino_flavor_records_do_not_invent_definite_masses_or_dirac_identity(shipped):
    neutrinos = [row for row in shipped["particle_entities"] if "neutrino" in row["id"]]
    assert len(neutrinos) == 6
    for row in neutrinos:
        assert row["conjugacy_status"] == "dirac_majorana_unresolved"
        assert row["rest_mass_relation"] == "flavor_state_not_definite_mass"
        mass = row["physical_properties"]["mass"]
        assert mass["status"] == "not_applicable"
        assert "value_decimal" not in mass
        assert "flavor" in mass["context"].lower()


@pytest.mark.parametrize("name", ["mass", "lifetime", "decay_width", "width", "mass_upper_limit"])
def test_mass_lifetime_width_and_mass_limit_cannot_be_negative(catalog, name):
    catalog["particle_entities"][0]["physical_properties"][name] = _property(
        value_decimal="-1",
        unit="reference units",
        context="Invalid nonnegative quantity.",
    )
    with pytest.raises(ValueError, match="nonnegative"):
        validate_catalog(catalog)


def test_generic_signed_measurements_remain_possible(catalog):
    catalog["particle_entities"][0]["physical_properties"]["magnetic_moment"] = _property(
        value_decimal="-1.25",
        unit="reference units",
        context="Synthetic signed measurement.",
    )
    validate_catalog(catalog)


@pytest.mark.parametrize("bound", ["lower_bound_decimal", "upper_bound_decimal"])
def test_mass_bounds_cannot_be_negative(catalog, bound):
    catalog["particle_entities"][0]["physical_properties"]["mass"] = _property(
        status="upper_limit",
        unit="MeV/c^2",
        context="Invalid mass limit.",
        **{bound: "-1"},
    )
    with pytest.raises(ValueError, match="nonnegative"):
        validate_catalog(catalog)


@pytest.mark.parametrize(
    ("identity", "value", "uncertainty", "unit"),
    [
        ("electron", "0.51099895000", "0.00000000015", "MeV/c^2"),
        ("muon", "105.6583755", "0.0000023", "MeV/c^2"),
        ("tau", "1776.93", "0.09", "MeV/c^2"),
        ("up_quark", "2.16", "0.07", "MeV/c^2"),
        ("down_quark", "4.70", "0.07", "MeV/c^2"),
        ("strange_quark", "93.5", "0.8", "MeV/c^2"),
        ("charm_quark", "1.2730", "0.0046", "GeV/c^2"),
        ("bottom_quark", "4.183", "0.007", "GeV/c^2"),
        ("top_quark", "172.56", "0.31", "GeV/c^2"),
        ("w_plus", "80.3692", "0.0133", "GeV/c^2"),
        ("z_boson", "91.1880", "0.0020", "GeV/c^2"),
        ("higgs_boson", "125.20", "0.11", "GeV/c^2"),
        ("proton", "938.27208816", "0.00000029", "MeV/c^2"),
        ("neutron", "939.5654205", "0.0000005", "MeV/c^2"),
    ],
)
def test_pdg_2025_mass_snapshot_matches_independently_reviewed_tables(
    shipped,
    identity,
    value,
    uncertainty,
    unit,
):
    # PDG 2025 summary tables: leptons pp. 1-2, quarks p. 1,
    # gauge/Higgs bosons pp. 1-4 and baryons pp. 1 and 4.
    particles = {row["id"]: row for row in shipped["particle_entities"]}
    mass = particles[identity]["physical_properties"]["mass"]
    assert mass["value_decimal"] == value
    assert mass["uncertainty_decimal"] == uncertainty
    assert mass["unit"].replace("^", "") == unit.replace("^", "")
    assert mass["status"] == "measured"
    assert any("pdg.lbl.gov/2025/" in shipped["sources"][source]["url"] for source in mass["sources"])


@pytest.mark.parametrize(
    ("identity", "value", "uncertainty"),
    [
        ("muon", "0.0000021969811", "0.0000000000022"),
        ("tau", "0.0000000000002903", "0.0000000000000005"),
        ("neutron", "878.4", "0.5"),
    ],
)
def test_free_particle_lifetimes_match_pdg_mean_life_units(shipped, identity, value, uncertainty):
    particles = {row["id"]: row for row in shipped["particle_entities"]}
    lifetime = particles[identity]["physical_properties"]["lifetime"]
    assert lifetime["value_decimal"] == value
    assert lifetime["uncertainty_decimal"] == uncertainty
    assert lifetime["unit"] == "s"
    assert "free" in lifetime["context"].lower()


def test_quark_mass_scheme_and_scale_are_not_free_particle_masses(shipped):
    particles = {row["id"]: row for row in shipped["particle_entities"]}
    for identity in ("up_quark", "down_quark", "strange_quark", "charm_quark", "bottom_quark"):
        properties = particles[identity]["physical_properties"]
        context = properties["mass"]["context"].lower()
        assert "modified minimal subtraction" in context
        assert "2 gev" in context or "own running-mass scale" in context
        assert "free-quark" in properties["lifetime"]["context"].lower()
        assert "value_decimal" not in properties["lifetime"]
    assert "event-kinematics" in particles["top_quark"]["physical_properties"]["mass"]["context"]


def test_physical_polarizations_distinguish_massless_and_massive_vector_bosons(shipped):
    particles = {row["id"]: row for row in shipped["particle_entities"]}
    for identity in ("photon", "gluon_multiplet"):
        assert particles[identity]["physical_properties"]["polarization"]["value"] == [
            "positive helicity",
            "negative helicity",
        ]
        assert particles[identity]["physical_properties"]["mass"]["status"] == "theoretical"
    for identity in ("w_plus", "w_minus", "z_boson"):
        assert particles[identity]["physical_properties"]["polarization"]["value"] == [
            "two transverse polarizations",
            "one longitudinal polarization",
        ]
    assert particles["higgs_boson"]["twice_spin"] == 0
    assert particles["gluon_multiplet"]["physical_properties"]["color_representation"]["value"] == (
        "adjoint color octet"
    )


def test_observed_gravity_does_not_promote_dark_identity_or_gravitons_to_measurements(shipped):
    rows = {
        row["id"]: row
        for section in ("field_entities", "particle_entities", "disturbance_families")
        for row in shipped[section]
    }
    assert rows["gravitational_waves"]["physical_status"] == "established"
    assert rows["graviton"]["physical_status"] == "hypothetical"
    assert rows["computational_field"]["physical_status"] == "project_hypothesis"
    for identity in ("dark_matter", "dark_energy"):
        assert rows[identity]["physical_properties"]["mass"]["status"] == "unknown"
        assert "value_decimal" not in rows[identity]["physical_properties"]["mass"]
    assert "value_decimal" not in rows["graviton"]["physical_properties"]["mass"]
    gravity = next(
        row for row in shipped["interaction_families"] if row["id"] == "gravitational_interaction"
    )
    assert gravity["mediator_ids"] == []
    assert "graviton" not in gravity["participant_ids"]


@pytest.mark.parametrize(
    ("channel", "incoming", "outgoing"),
    [
        ("muon_decay", ["muon"], ["electron", "electron_antineutrino", "muon_neutrino"]),
        ("antimuon_decay", ["antimuon"], ["positron", "electron_neutrino", "muon_antineutrino"]),
        ("free_neutron_beta_decay", ["neutron"], ["proton", "electron", "electron_antineutrino"]),
        ("inverse_beta_scattering", ["electron_antineutrino", "proton"], ["positron", "neutron"]),
        ("top_bottom_decay", ["top_quark"], ["w_plus", "bottom_quark"]),
        ("w_plus_leptonic_decay", ["w_plus"], ["positron", "electron_neutrino"]),
        ("two_photon_pair_creation", ["photon", "photon"], ["electron", "positron"]),
        ("electron_positron_two_photon_annihilation", ["electron", "positron"], ["photon", "photon"]),
    ],
)
def test_representative_channels_keep_flavor_conjugacy_and_product_multiplicity(
    shipped,
    channel,
    incoming,
    outgoing,
):
    channels = {row["id"]: row for row in shipped["representative_channels"]}
    assert sorted(channels[channel]["incoming_ids"]) == sorted(incoming)
    assert sorted(channels[channel]["outgoing_ids"]) == sorted(outgoing)
    assert channels[channel]["claim_level"] == "descriptive_only"
    assert channels[channel]["conditions"]


def test_neutrino_and_gauge_interactions_do_not_become_generic_charge_only_rules(shipped):
    interactions = {row["id"]: row for row in shipped["interaction_families"]}
    assert interactions["strong_color_interactions"]["mediator_ids"] == ["gluon_multiplet"]
    assert interactions["weak_charged_current"]["mediator_ids"] == ["w_plus", "w_minus"]
    assert interactions["weak_neutral_current"]["mediator_ids"] == ["z_boson"]
    assert interactions["electromagnetic_scattering"]["mediator_ids"] == ["photon"]
    for flavor in ("electron", "muon", "tau"):
        for suffix in ("neutrino", "antineutrino"):
            identity = f"{flavor}_{suffix}"
            assert identity in interactions["weak_neutral_current"]["participant_ids"]
            assert identity in interactions["weak_charged_current"]["participant_ids"]
            assert identity in interactions["neutrino_flavor_mixing"]["participant_ids"]
            assert identity not in interactions["strong_color_interactions"]["participant_ids"]
    pair_conditions = " ".join(interactions["pair_creation_annihilation"]["conditions"])
    assert "one real photon cannot create a massive pair in empty space" in pair_conditions
    for channel in shipped["representative_channels"]:
        assert not (
            channel["incoming_ids"] == ["photon"]
            and sorted(channel["outgoing_ids"]) == ["electron", "positron"]
        )


@pytest.mark.parametrize(
    ("identity", "constituents", "baryon_number"),
    [
        ("proton", ["up_quark", "up_quark", "down_quark"], 1),
        ("neutron", ["up_quark", "down_quark", "down_quark"], 1),
        ("antiproton", ["antiup_quark", "antiup_quark", "antidown_quark"], -1),
        ("antineutron", ["antiup_quark", "antidown_quark", "antidown_quark"], -1),
    ],
)
def test_nucleon_composition_is_valence_metadata_with_distinct_antimatter(
    shipped,
    identity,
    constituents,
    baryon_number,
):
    particle = next(row for row in shipped["particle_entities"] if row["id"] == identity)
    properties = particle["physical_properties"]
    assert sorted(properties["composition"]["constituent_ids"]) == sorted(constituents)
    assert properties["baryon_number"]["value"] == baryon_number
    assert "sea components" in properties["composition"]["context"]
    assert particle["field_ids"] == []
