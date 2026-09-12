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


def test_field_only_movie_draws_node_vectors_and_separate_transfer_values_without_mutation():
    frame = {
        "tick": 0,
        "cells": [],
        "transfers": [],
        "spatial_baselines": {"a": [2, 0, 0], "b": [0, 0, 0]},
        "spatial_fields": [
            {
                "position": [2, 2, 2],
                "fields": {
                    "a": {
                        "baseline": [2, 0, 0],
                        "value": [3, 4, 0],
                        "populations": [[1, 4, 0]] + [[0, 0, 0]] * 7,
                        "directions": [[90, 80, 0]] * 6,
                    },
                    "b": {"baseline": [0, 0, 0], "value": [0, 0, 0]},
                },
            }
        ],
        "spatial_transfers": [
            {
                "origin": [0, 2, 2],
                "target": [1, 2, 2],
                "port": 0,
                "arrival_tick": 2,
                "fields": {"a": [[2, 0, 0], [-1, 0, 0]] + [[0, 0, 0]] * 6},
            }
        ],
    }
    recording = {
        "frames": [frame],
        "metadata": {"model": "field-only", "shape": [5, 5, 5], "link_ticks": 2},
    }
    result = javascript(
        "playback.html",
        '"use strict";',
        "</script></body>",
        "const calls=[];const context=new Proxy({}, {get(target,key){return target[key]||"
        "((...args)=>calls.push([key,...args]));}});"
        "function element(){return {children:[],style:{},value:'',textContent:'',"
        "append(...children){this.children.push(...children)},replaceChildren(){this.children=[]}}}"
        "const elements=new Map();const document={querySelector(id){if(!elements.has(id))"
        "elements.set(id,element());return elements.get(id)},createElement:element,"
        "createTextNode(text){return {textContent:text}},addEventListener(){}};"
        "document.querySelector('#recording').textContent=JSON.stringify(input);"
        "document.querySelector('#plane').value='0,1';"
        "document.querySelector('#zoom').value='1';"
        "Object.assign(document.querySelector('#scene'),{getContext(){return context},"
        "getBoundingClientRect(){return {width:640,height:360}}});"
        "const window={devicePixelRatio:1},location={search:''};"
        "class ResizeObserver{observe(){}}function requestAnimationFrame(){}",
        "console.log(JSON.stringify({rows:elements.get('#records').children.map(row=>"
        "row.children.map(cell=>cell.textContent)),labels:calls.filter(call=>call[0]==='fillText'),"
        "rectangles:calls.filter(call=>call[0]==='rect').length,"
        "values:visibleSpatialFields(frames[0]).map(record=>record.value),"
        "unchanged:JSON.stringify({frames,metadata})===JSON.stringify(input)}));",
        recording,
    )
    assert result["values"] == [[3, 4, 0], [0, 0, 0], [1, 0, 0]]
    assert [row[0] for row in result["rows"]] == ["Field: a", "Field: b", "Field: a"]
    assert result["rows"][0][2:] == ["[3,4,0]", "Node field; value includes baseline"]
    assert result["rows"][2][2:] == ["[1,0,0]", "Field Link → 1, 2, 2; arrives 2"]
    assert any(label[1] == "a: 3, 4, 0" for label in result["labels"])
    assert result["rectangles"] >= 3  # Two node squares and the existing clip rectangle.
    assert result["unchanged"] is True


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


def test_editor_rename_preserves_group_port_and_joint_rule_references():
    from tests.test_spatial_interactions import exchange

    raw = exchange()
    raw["field_groups"] = [{"name": "joint_group", "fields": ["quantity"]}]
    raw["field_rules"] = [
        {
            "name": "retain",
            "when": {"received": "quantity", "port": 0},
            "assignments": [{"field": "quantity", "expression": {"field": "quantity", "side": "right"}}],
            "invariants": [
                {"name": "unchanged_output", "expression": {"outgoing": "quantity", "port": 0}}
            ],
        }
    ]
    parse_initial_state(raw)
    renamed = javascript(
        "app.js",
        "function renameReferences(",
        "function check(",
        "",
        "renameReferences(input,'field','quantity','inventory');"
        "renameReferences(input,'type','held','probe');"
        "input.fields[0].name='inventory'; input.disturbance_types[0].name='probe';"
        "console.log(JSON.stringify(input));",
        raw,
    )
    assert renamed["field_groups"][0]["fields"] == ["inventory"]
    assert renamed["field_rules"][0]["when"] == {"received": "inventory", "port": 0}
    assert renamed["field_rules"][0]["invariants"][0]["expression"] == {
        "outgoing": "inventory",
        "port": 0,
    }
    assert renamed["spatial_interactions"][0]["type"] == "probe"
    assert renamed["spatial_interactions"][0]["assignments"][0]["field"] == "inventory"
    assert renamed["disturbance_types"][0]["defaults"] == {"inventory": 5}
    parse_initial_state(renamed)


@pytest.mark.parametrize(
    "stored",
    [
        "{}",
        json.dumps({"__proto__": "older draft", "keep": "unchanged draft"}),
        "null",
        "[]",
        "invalid JSON",
    ],
)
def test_drafts_save_arbitrary_template_names_and_preserve_loaded_drafts(stored):
    updates = {name: f"draft for {name}" for name in ("__proto__", "constructor", "toString")}
    saved = javascript(
        "app.js",
        "let drafts =",
        "function changed()",
        "let selected='',source='',saved='';const localStorage={"
        "getItem(){return input.stored},setItem(key,value){saved=value}};",
        "for(const [key,value] of Object.entries(input.updates)){"
        "selected=key;source=value;remember();}console.log(saved);",
        {"stored": stored, "updates": updates},
    )
    expected = dict(updates)
    if "unchanged draft" in stored:
        expected["keep"] = "unchanged draft"
    assert saved == expected


def add_editor_item(raw, tab):
    return javascript(
        "app.js",
        "function addButton(",
        "function $$(",
        "const configuration=input.document,tab=input.tab,buttons=[];"
        "function node(tag,text=''){const value={text,children:[],classList:{add(){}},"
        "append(...items){this.children.push(...items);this.lastChild=items.at(-1)},"
        "replaceChildren(){this.children=[]},querySelector(){return {}},"
        "addEventListener(event,callback){if(event==='click')this.click=callback}};"
        "if(tag==='button')buttons.push(value);return value;}"
        "const editor=node('form');editor.reportValidity=()=>true;"
        "const $=()=>editor,$$=()=>[];function card(){return node('section')}"
        "function inputControl(parent){parent.append(node('label'))}"
        "function check(){}function jsonField(){}function changed(){}"
        "{const input=inputControl;",
        "renderEditor();buttons[0].click();console.log(JSON.stringify(configuration));}",
        {"document": raw, "tab": tab},
    )


@pytest.mark.parametrize(
    "tab,names,expected",
    [
        ("fields", ["field_4", "heading", "radiation"], "field_5"),
        ("fields", ["field_4", "field_5", "constructor"], "field_6"),
        ("fields", ["constructor", "__proto__", "toString"], "field_4"),
        ("types", ["type_2"], "type_3"),
        ("types", ["type_3", "type_4"], "type_5"),
        ("types", ["__proto__"], "type_2"),
    ],
)
def test_add_editor_item_uses_an_unused_name_without_changing_existing_defaults(tab, names, expected):
    field_names = names if tab == "fields" else ["stock"]
    type_names = names if tab == "types" else ["carrier"]
    raw = {
        "schema_version": 1,
        "model_id": "editor-name-check",
        "shape": [3, 3, 3],
        "slots_per_cell": 4,
        "link_ticks": 1,
        "normal_budget": 1000,
        "ticks": 0,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {"name": name, "components": 1, "units": "unit", "signed": False, "conserved": False}
            for name in field_names
        ],
        "disturbance_types": [
            {"name": name, "fields": [field_names[0]], "transport": {"mode": "hold"}}
            for name in type_names
        ],
        "seeds": [],
    }
    parse_initial_state(raw)
    added = add_editor_item(raw, tab)
    collection = "fields" if tab == "fields" else "disturbance_types"
    assert added[collection][:-1] == raw[collection]
    assert added[collection][-1]["name"] == expected
    if tab == "types":
        assert added[collection][-1]["fields"] == [field_names[0]]
        assert added[collection][-1]["transport"] == {"mode": "hold"}
    parse_initial_state(added)


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
