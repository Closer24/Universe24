"""Headless JavaScript consumers preserve boundary, accounting and field references."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from event_universe.initialization import parse_initial_state
from tests.test_spatial_coupling import document

ASSETS = Path(__file__).resolve().parents[1] / "src/event_universe/ui_assets"


def javascript(asset, start, end, setup, expression, payload):
    executable = shutil.which("node")
    if executable is None:
        pytest.skip("headless JavaScript consumer checks require Node; simulation does not")
    source = (ASSETS / asset).read_text(encoding="utf-8")
    function = source[source.index(start) : source.index(end, source.index(start))]
    script = (
        "const input=JSON.parse(require('node:fs').readFileSync(0,'utf8'));\n"
        + setup
        + "\n"
        + function
        + "\n"
        + expression
    )
    result = subprocess.run(
        [executable, "-e", script],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        timeout=10,
    )
    return json.loads(result.stdout)


@pytest.mark.parametrize("port", range(6))
def test_terminal_playback_preserves_outward_direction_without_wrapping_or_mutation(port):
    origin = [2, 2, 2]
    origin[port // 2] = 4 if port % 2 == 0 else 0
    frame = {
        "tick": 2,
        "boundary": "open",
        "cells": [],
        "transfers": [
            {
                "origin": origin,
                "target": None,
                "port": port,
                "arrival_tick": 3,
                "type": "carrier",
                "values": {"stock": [-3]},
            }
        ],
    }
    result = javascript(
        "playback.html",
        "function visibleRecords(",
        "let pan=",
        "const metadata={shape:[5,5,5],link_ticks:3,boundary:'open'},shape=metadata.shape;",
        "const before=JSON.stringify(input); const records=visibleRecords(input);"
        "console.log(JSON.stringify({records,unchanged:JSON.stringify(input)===before}));",
        frame,
    )
    expected = list(origin)
    expected[port // 2] += (1 if port % 2 == 0 else -1) * 2 / 3
    record = result["records"][0]
    assert record["position"] == pytest.approx(expected)
    assert record["values"] == {"stock": [-3]}
    assert "Exit" in record["owner"] and "3" in record["owner"]
    assert result["unchanged"] is True


@pytest.mark.parametrize("boundary", [None, "periodic"])
def test_legacy_periodic_movie_keeps_wrapped_transfer_positions(boundary):
    frame = {
        "tick": 2,
        "cells": [],
        "transfers": [
            {
                "origin": [0, 2, 2],
                "target": [4, 2, 2],
                "port": 1,
                "arrival_tick": 3,
                "type": "carrier",
                "values": {},
            }
        ],
    }
    if boundary is not None:
        frame["boundary"] = boundary
    records = javascript(
        "playback.html",
        "function visibleRecords(",
        "let pan=",
        "const metadata={shape:[5,5,5],link_ticks:3},shape=metadata.shape;",
        "console.log(JSON.stringify(visibleRecords(input)));",
        frame,
    )
    assert records[0]["position"] == pytest.approx([5 - 2 / 3, 2, 2])
    assert records[0]["owner"] == "Link → 4, 2, 2; arrives 3"


def test_field_rename_preserves_nested_flux_coupling_and_valid_configuration():
    raw = document()
    raw["fields"][1]["components"] = 1
    raw["spatial_fields"][1]["baseline"] = 2
    raw["spatial_couplings"][0]["rotation"] = {
        "op": "mul",
        "args": [{"field": "polarity"}, {"flux": "control"}],
    }
    parse_initial_state(raw)
    renamed = javascript(
        "app.js",
        "function renameReferences(",
        "function check(",
        "",
        "renameReferences(input,'field','control','renamed_signal');"
        "input.fields[1].name='renamed_signal'; console.log(JSON.stringify(input));",
        raw,
    )
    assert renamed["spatial_couplings"][0]["rotation"]["args"][1] == {"flux": "renamed_signal"}
    assert renamed["spatial_fields"][1]["field"] == "renamed_signal"
    assert renamed["spatial_couplings"][0]["rotation"]["args"][0] == {"field": "polarity"}
    initial = parse_initial_state(renamed)
    assert initial.fields[1].name == "renamed_signal"


def result_view(metadata):
    return javascript(
        "app.js",
        "function renderResults()",
        "async function poll()",
        "function node(tag,text='',className=''){return {tag,text,className,children:[],"
        "append(...items){this.children.push(...items)},replaceChildren(...items){this.children=items}}}"
        "const elements=new Map(),$=selector=>{if(!elements.has(selector))elements.set(selector,node('div'));"
        "return elements.get(selector)};"
        "let busy=false,loading=false,configuration={},moviePath=null,selectedRun='sample';"
        "const runs=[{id:'sample',status:'completed',model:'generic',requested_ticks:3,elapsed_seconds:0.1,"
        "artifacts:{},metadata:input}];",
        "renderResults();console.log(JSON.stringify($('#results')));",
        metadata,
    )


def descendants(node):
    yield node
    for child in node.get("children", []):
        yield from descendants(child)


@pytest.mark.parametrize("loss,escaped", [([5, -2, 0], [0, 0, 0]), ([0, 0, 0], [5, -2, 0])])
def test_successful_loss_or_escape_is_displayed_as_balanced_with_signed_ledger(loss, escaped):
    metadata = {
        "completed_ticks": 3,
        "initial_totals": {"stock": [5, -2, 0]},
        "final_totals": {"stock": [0, 0, 0]},
        "source_totals": {"stock": [0, 0, 0]},
        "dissipation_totals": {"stock": loss},
        "escaped_totals": {"stock": escaped},
        "conserved_at_every_completed_tick": False,
        "accounting_balanced_at_every_completed_tick": True,
    }
    nodes = list(descendants(result_view(metadata)))
    paragraphs = [item["text"] for item in nodes if item["tag"] == "p"]
    assert any("accounting balances" in text for text in paragraphs)
    assert not any("failed" in text for text in paragraphs)
    headers = [item["text"] for item in nodes if item["tag"] == "th"]
    assert headers == ["TRACKED FIELD", "INITIAL", "FINAL", "SOURCE CHANGE", "DISSIPATED", "ESCAPED"]
    rows = [item for item in nodes if item["tag"] == "tr"]
    assert [item["text"] for item in rows[1]["children"]][-2:] == [
        json.dumps(loss, separators=(",", ":")),
        json.dumps(escaped, separators=(",", ":")),
    ]


def test_explicit_accounting_failure_overrides_unchanged_inventory_flag():
    nodes = descendants(
        result_view(
            {
                "completed_ticks": 3,
                "conserved_at_every_completed_tick": True,
                "accounting_balanced_at_every_completed_tick": False,
            }
        )
    )
    assert any(item["text"] == "Quantity accounting failed." for item in nodes)


def test_old_conservative_metadata_still_reports_success():
    nodes = descendants(result_view({"completed_ticks": 3, "conserved_at_every_completed_tick": True}))
    assert any(
        item["text"] == "Declared quantities conserved at every completed tick." for item in nodes
    )
