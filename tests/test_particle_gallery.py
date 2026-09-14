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
