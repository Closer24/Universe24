"""Recorded configured links, selected sites and local receipt directions agree."""

import json
from itertools import product

import pytest

from event_universe.diagnostics.local_observer import LocalObserver, ObserverDefinition
from event_universe.runner import run_initialization
from tests.test_initialization import _document
from tests.test_observer_playback import player, recording


def topology_recording(kind="bcc"):
    data = recording()
    if kind == "bcc":
        offsets = list(product((-1, 1), repeat=3))
        residues = [[0, 0, 0], [1, 1, 1]]
    else:
        offsets = [p for p in product((-1, 0, 1), repeat=3) if sum(v != 0 for v in p) == 2]
        residues = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    data["metadata"].update(
        shape=[8, 8, 8],
        link_ticks=2,
        topology={
            "model_id": "configured-ports-v1",
            "offsets": offsets,
            "site_modulus": 2,
            "site_residues": residues,
        },
    )
    data["observation"]["receipts"][0]["port"] = 6
    data["observation"]["receipts"][1]["port"] = len(offsets) - 1
    return data


@pytest.mark.parametrize(
    ("kind", "degree", "last_label"), [("bcc", 8, "+X +Y +Z"), ("fcc", 12, "+X +Y")]
)
def test_observer_replay_uses_configured_receiver_directions_without_future_receipts(
    kind, degree, last_label
):
    result = player(
        topology_recording(kind),
        r"""
const initial={cards:$('#receivers').children.length,unknown:textTree($('#receivers'))};
selectFrame(1);const first=textTree($('#observer-records'));
selectFrame(2);const last=$('#receivers').children.at(-1);
console.log(JSON.stringify({initial,first,last:textTree(last),worldInitialized,
  direction:last.children[0].textContent,unchanged:JSON.stringify({frames,metadata,observation})===JSON.stringify(input)}));
""",
    )
    assert result["initial"]["cards"] == degree
    assert result["initial"]["unknown"].count("Unknown") == degree
    assert "later arrival" not in result["first"]
    assert result["direction"] == last_label
    assert "later arrival" in result["last"]
    assert result["worldInitialized"] is False
    assert result["unchanged"] is True


def test_recorded_diagonal_link_moves_in_all_axes_and_splits_periodic_seam():
    result = player(
        topology_recording(),
        r"""
initializeWorldView();
const transfer={origin:[7,7,7],target:[0,0,0],port:7,arrival_tick:2};
const diagonal=transferView(transfer,{tick:1});
const segments=linkSegments(transfer.origin,portOffset(7),'periodic');
const exiting=transferView({...transfer,target:null},{tick:1,boundary:'open'});
let rejected=false;try{portOffset(8)}catch(error){rejected=true}
console.log(JSON.stringify({position:diagonal.position,segments,exit:exiting.owner,rejected}));
""",
    )
    assert result["position"] == [7.5, 7.5, 7.5]
    assert result["segments"] == [
        [[7, 7, 7], [7.5, 7.5, 7.5]],
        [[-0.5, -0.5, -0.5], [0, 0, 0]],
    ]
    assert result["exit"] == "Exit through +X +Y +Z; leaves 2"
    assert result["rejected"] is True


@pytest.mark.parametrize(("kind", "projected_count"), [("bcc", 32), ("fcc", 64)])
def test_projection_draws_only_selected_sites_and_actual_configured_links(kind, projected_count):
    result = player(
        topology_recording(kind),
        r"""
initializeWorldView();
const lattice=projectedLattice([0,1],[0,7,0,7],'periodic');
console.log(JSON.stringify({nodes:lattice.nodes,segments:lattice.segments,
  excluded:selectedSite([0,0,1]),origin:selectedSite([0,0,0])}));
""",
    )
    assert len(result["nodes"]) == projected_count
    assert result["excluded"] is False and result["origin"] is True
    if kind == "bcc":
        assert all(x % 2 == y % 2 for x, y in result["nodes"])
        assert [[0, 0], [1, 1]] in result["segments"] or [[1, 1], [0, 0]] in result["segments"]
        assert all(a[0] != b[0] and a[1] != b[1] for a, b in result["segments"])
    assert all(abs(a[axis] - b[axis]) <= 1 for a, b in result["segments"] for axis in (0, 1))


def test_observer_accepts_configured_port_count_and_rejects_wrong_width_atomically():
    probe = LocalObserver(ObserverDefinition((0, 0, 0)), port_count=8)
    event = {
        "event": "spatial_received",
        "position": (0, 0, 0),
        "received_fields": [{}, {}, {}, {}, {}, {}, {}, {"inventory": [7]}],
    }
    probe.receive(event)
    assert probe.receipts[0]["port"] == 7
    assert probe.receipts[0]["values"] == {"inventory": (7,)}
    with pytest.raises(ValueError, match="configured receiver-port"):
        probe.receive({**event, "received_fields": event["received_fields"][:6]})
    assert len(probe.receipts) == 1
    with pytest.raises(ValueError, match="configured receiver sides"):
        probe.receive(
            {
                "event": "received",
                "position": (0, 0, 0),
                "port": 8,
                "disturbance": "test",
                "values": {"inventory": [1]},
            }
        )
    assert len(probe.receipts) == 1


@pytest.mark.parametrize("count", [True, 1, 27])
def test_observer_port_count_has_a_fixed_supported_bound(count):
    with pytest.raises(ValueError, match="observer port_count"):
        LocalObserver(ObserverDefinition((0, 0, 0)), port_count=count)


def configured_run():
    raw = _document()
    raw.update(shape=[8, 8, 8], ticks=2, link_ticks=2)
    raw["topology"] = topology_recording()["metadata"]["topology"]
    raw["disturbance_types"] = [raw["disturbance_types"][0]]
    raw["disturbance_types"][0]["transport"] = {"mode": "move", "weights": [1] + [0] * 7}
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    return raw


def test_runner_preserves_explicit_topology_and_high_port_receipts_without_changing_state(tmp_path):
    raw = configured_run()
    initialization, placement = tmp_path / "input.json", tmp_path / "probe.json"
    initialization.write_text(json.dumps(raw))
    placement.write_text(json.dumps({"position": [1, 1, 1]}))
    for name, probe in (("observed", placement), ("plain", None)):
        run_initialization(initialization, tmp_path / name, observer=probe)
    metadata = json.loads((tmp_path / "observed/run.json").read_text())
    assert metadata["topology"] == json.loads(json.dumps(raw["topology"]))
    assert metadata["status"] == "completed"
    observations = json.loads((tmp_path / "observed/observations.json").read_text())
    assert len(observations["receipts"]) == 1
    assert observations["receipts"][0]["port"] == 7
    assert observations["receipts"][0]["values"]["mass"] == [2]
    for name in ("events.jsonl", "state.json"):
        assert (tmp_path / "observed" / name).read_bytes() == (tmp_path / "plain" / name).read_bytes()
    assert not (tmp_path / "observed/run.html").exists()


def test_runner_rejects_observer_outside_selected_sites_before_creating_output(tmp_path):
    initialization, placement = tmp_path / "input.json", tmp_path / "probe.json"
    initialization.write_text(json.dumps(configured_run()))
    placement.write_text(json.dumps({"position": [2, 2, 3]}))
    with pytest.raises(ValueError, match="not a site"):
        run_initialization(initialization, tmp_path / "output", observer=placement)
    assert not (tmp_path / "output").exists()


def test_legacy_runner_metadata_keeps_implicit_six_port_topology(tmp_path):
    initialization = tmp_path / "input.json"
    initialization.write_text(json.dumps(_document()))
    run_initialization(initialization, tmp_path / "output", ticks=0)
    metadata = json.loads((tmp_path / "output/run.json").read_text())
    assert "topology" not in metadata
    assert metadata["shape"] == [17, 17, 17]
    assert metadata["link_ticks"] == 1
