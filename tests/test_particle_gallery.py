"""Named-particle gallery: derived inputs, recorded facts and optional rendering."""

import importlib.util
import json
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "particle_gallery", ROOT / "examples/gallery/particle_gallery.py"
)
GALLERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GALLERY)


def test_derived_configurations_are_valid_and_keep_their_source_contracts():
    backscatter = GALLERY.backscatter_configuration()
    template = json.loads(GALLERY.BACKSCATTER_TEMPLATE.read_text(encoding="utf-8"))
    assert backscatter["model_id"] == template["model_id"]
    assert backscatter["interactions"] == template["interactions"]
    assert backscatter["seeds"] == GALLERY.BACKSCATTER_SEEDS and backscatter["ticks"] == 96
    assert validate_configuration(json.dumps(backscatter).encode()).valid
    catalog = GALLERY.catalog_configuration()
    names = {t["name"] for t in catalog["disturbance_types"]}
    assert {"source_electron", "source_positron", "contact_probe", "localized_charge"} <= names
    assert catalog["event_program"]["model"] == "causal-contact-fields-v1"
    assert validate_configuration(json.dumps(catalog).encode()).valid


def test_separated_pair_meets_at_tick_36_and_exchanges_momenta(tmp_path):
    result = GALLERY.run_backscatter(tmp_path / "gallery")
    assert result["contact_ticks"] == [36]
    assert result["momenta_before"] == {"electron": ["1000", "0", "0"], "positron": ["-1000", "0", "0"]}
    assert result["momenta_after"] == {"electron": ["-1000", "0", "0"], "positron": ["1000", "0", "0"]}
    assert result["final_totals"] == {"mass": [2000], "charge": [0]} and result["conserved"]
    timeline = result["timeline"]
    assert timeline["ticks"] == list(range(0, 97, 12))
    assert timeline["records"][96]["electron"]["position"] == [3, 8, 8]
    assert timeline["records"][96]["positron"]["position"] == [13, 8, 8]


def test_catalog_pair_records_opposite_fields_and_two_captures(tmp_path):
    result = GALLERY.run_contact_fields(tmp_path / "gallery")
    summary = result["summary"]
    assert [d["weights"] for d in summary["decisions"]] == [[9, 16], [9, 16]]
    assert [c["address"] for c in summary["captures"]] == [[3, 1, 1], [3, 3, 1]]
    assert summary["final_totals"]["charge"] == [0] and summary["final_totals"]["mass"] == [1022]
    frames = result["frames"]
    assert [f["tick"] for f in frames] == list(range(17))
    signs = {
        (n["position"][1], GALLERY._field_value(n) > 0)
        for n in frames[2]["spatial_fields"]
        if GALLERY._field_value(n) != 0
    }
    assert (1, False) in signs and (3, True) in signs
    assert not any((1, True) == s or (3, False) == s for s in signs)


def test_reaction_laws_validate_and_conserve_every_declared_inventory():
    raw = json.loads(GALLERY.REACTIONS_TEMPLATE.read_text(encoding="utf-8"))
    assert raw["model_id"] == "configured-lepton-reactions-v1"
    assert [f["name"] for f in raw["fields"] if f["conserved"]] == [
        "energy",
        "momentum",
        "charge",
        "lepton_e",
        "lepton_mu",
        "baryon",
    ]
    assert [r["name"] for r in raw["interactions"]] == [
        "pair_to_muons",
        "annihilation",
        "w_minus_decay",
        "w_plus_decay",
        "muon_decay_step_1",
        "antimuon_decay_step_1",
        "beta_decay_step_1",
    ]
    for name in GALLERY.REACTION_SCENARIOS:
        assert validate_configuration(json.dumps(GALLERY.reaction_configuration(name)).encode()).valid


def test_reactions_record_annihilation_muon_chain_and_beta_decay(tmp_path):
    results = GALLERY.run_reactions(tmp_path / "gallery")
    annihilation = results["annihilation"]["summary"]
    assert annihilation["events"] == [{"tick": 5, "position": [7, 7, 1], "rule": "annihilation"}]
    assert [list(r[1:3]) for r in annihilation["final_records"]] == [["photon", 13], ["photon", 13]]
    assert annihilation["final_totals"] == annihilation["initial_totals"]
    muon = results["muon_pair"]["summary"]
    assert [(e["tick"], e["rule"]) for e in muon["events"]] == [
        (5, "pair_to_muons"),
        (8, "antimuon_decay_step_1"),
        (8, "muon_decay_step_1"),
        (9, "w_plus_decay"),
        (9, "w_minus_decay"),
    ]
    kinds = sorted(r[1] for r in muon["final_records"])
    assert kinds == [
        "electron",
        "electron_antineutrino",
        "electron_neutrino",
        "muon_antineutrino",
        "muon_neutrino",
        "positron",
    ]
    assert muon["final_totals"]["energy"] == [2200] and muon["final_totals"]["lepton_mu"] == [0]
    assert muon["final_totals"]["lepton_e"] == [0] and muon["final_totals"]["charge"] == [0]
    beta = results["beta_decay"]["summary"]
    assert [(e["tick"], e["rule"]) for e in beta["events"]] == [
        (4, "beta_decay_step_1"),
        (5, "w_minus_decay"),
    ]
    assert sorted(r[1] for r in beta["final_records"]) == ["electron", "electron_antineutrino", "proton"]
    assert beta["final_totals"] == beta["initial_totals"]
    assert beta["final_totals"]["baryon"] == [1] and beta["final_totals"]["charge"] == [0]
    shell = beta["charged_lepton_mass_shell"]
    assert shell["status"] == "failed"
    electrons = [row for row in shell["failures"] if row["type"] == "electron"]
    assert electrons and all(row["energy_squared_minus_momentum_squared"] == 0 for row in electrons)
    w_frame = results["beta_decay"]["frames"][5]
    assert any(d["type"] == "w_minus" for node in w_frame["nodes"] for d in node["disturbances"])


@pytest.mark.parametrize("owner", ["node", "held_output", "link"])
def test_shell_screen_reports_massless_electron_at_each_owner_without_mutation(owner):
    record = {"type": "electron", "values": {"energy": [7], "momentum": [7, 0, 0]}}
    frame = {"tick": 3, "nodes": [], "transfers": []}
    if owner == "link":
        frame["transfers"] = [{**record, "origin": [2, 2, 2]}]
    else:
        bank = "disturbances" if owner == "node" else "held_outputs"
        frame["nodes"] = [{"position": [2, 2, 2], bank: [record]}]
    before = json.dumps(frame, sort_keys=True)
    audit = GALLERY.charged_lepton_shell_screen([frame])
    assert audit["sample_count"] == 1 and audit["status"] == "failed"
    assert audit["failures"][0]["owner"] == owner
    assert audit["failures"][0]["energy_squared_minus_momentum_squared"] == 0
    assert json.dumps(frame, sort_keys=True) == before


def test_positive_shell_is_not_reported_as_a_validated_species_mass():
    frame = {
        "tick": 0,
        "nodes": [
            {
                "position": [1, 1, 1],
                "disturbances": [
                    {"type": "electron", "values": {"energy": [13], "momentum": [12, 0, 0]}}
                ],
            }
        ],
    }
    audit = GALLERY.charged_lepton_shell_screen([frame])
    assert audit["sample_count"] == 1 and audit["status"] == "not_established"
    assert audit["failures"] == []
    assert GALLERY.charged_lepton_shell_screen([])["status"] == "not_established"


@pytest.mark.parametrize(
    "energy,momentum,expected_shell",
    [(-13, [12, 0, 0], 25), (0, [0, 0, 0], 0), (3, [2, 3, 6], -40)],
)
def test_massive_screen_rejects_negative_energy_zero_energy_and_spacelike_products(
    energy, momentum, expected_shell
):
    frame = {
        "tick": 0,
        "nodes": [
            {
                "position": [1, 1, 1],
                "disturbances": [
                    {"type": "electron", "values": {"energy": [energy], "momentum": momentum}}
                ],
            }
        ],
    }
    audit = GALLERY.charged_lepton_shell_screen([frame])
    assert audit["status"] == "failed" and audit["sample_count"] == 1
    assert audit["failures"][0]["energy_squared_minus_momentum_squared"] == expected_shell


@pytest.mark.visualization
def test_gallery_renders_two_animations_and_two_stills(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("PIL")
    from PIL import Image

    output = tmp_path / "gallery"
    backscatter = GALLERY.run_backscatter(output)
    contact = GALLERY.run_contact_fields(output)
    saved = GALLERY.render(output, backscatter, contact)
    assert [p.name for p in saved] == [
        "electron_positron_backscatter.gif",
        "electron_positron_backscatter_contact.png",
        "electron_positron_contact_fields.gif",
        "electron_positron_contact_fields_tick03.png",
    ]
    assert all(p.stat().st_size for p in saved)
    assert Image.open(saved[0]).n_frames >= 9 and Image.open(saved[2]).n_frames >= 17
    reactions = GALLERY.run_reactions(output)
    rendered = GALLERY.render_reactions(output, reactions)
    assert [p.name for p in rendered] == [
        "reaction_annihilation.gif",
        "reaction_annihilation_event.png",
        "reaction_muon_pair.gif",
        "reaction_muon_pair_event.png",
        "reaction_beta_decay.gif",
        "reaction_beta_decay_event.png",
    ]
    assert all(p.stat().st_size for p in rendered)
