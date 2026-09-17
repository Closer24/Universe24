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
    w_frame = results["beta_decay"]["frames"][5]
    assert any(d["type"] == "w_minus" for node in w_frame["nodes"] for d in node["disturbances"])


@pytest.mark.visualization
def test_gallery_renders_the_animations_and_stills(tmp_path):
    pytest.importorskip("matplotlib")
    pytest.importorskip("PIL")
    from PIL import Image

    output = tmp_path / "gallery"
    backscatter = GALLERY.run_backscatter(output)
    saved = GALLERY.render(output, backscatter)
    assert [p.name for p in saved] == [
        "electron_positron_backscatter.gif",
        "electron_positron_backscatter_contact.png",
    ]
    assert all(p.stat().st_size for p in saved)
    assert Image.open(saved[0]).n_frames >= 9
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
