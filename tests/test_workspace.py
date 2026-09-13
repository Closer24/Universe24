"""A real local HTTP workspace must run edited JSON through the existing engine."""

import hashlib
import http.client
import json
import math
import threading
import time
from pathlib import Path

import pytest

from event_universe.runner import run_initialization
from event_universe.ui import Workspace, WorkspaceServer

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def server(tmp_path):
    server = WorkspaceServer(Workspace(ROOT / "examples", tmp_path / "workspace"), 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server
    server.shutdown()
    thread.join(timeout=3)
    server.server_close()


def request(server, path, data=None, headers=None, method=None):
    connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=10)
    defaults = {"X-Workspace-Token": server.token, "Content-Type": "application/json"}
    defaults.update(headers or {})
    connection.request(
        method or ("GET" if data is None else "POST"),
        path,
        body=json.dumps(data) if data is not None else None,
        headers=defaults,
    )
    response = connection.getresponse()
    status, payload, kind = response.status, response.read(), response.getheader("Content-Type", "")
    connection.close()
    return status, json.loads(payload) if kind.startswith("application/json") else payload


def wait_for_run(server, identifier):
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        status, result = request(server, f"/api/runs/{identifier}")
        assert status == 200
        if result["status"] != "running":
            return result
        time.sleep(0.03)
    pytest.fail("Workspace child did not complete")


def without_elapsed(metadata):
    comparable = dict(metadata)
    elapsed = comparable.pop("elapsed_seconds")
    assert type(elapsed) in (int, float) and math.isfinite(elapsed) and elapsed >= 0
    return comparable


def test_workspace_serves_assets_and_current_example_data(server):
    status, page = request(server, "/")
    assert status == 200
    assert server.token.encode() in page and b"__WORKSPACE_TOKEN__" not in page
    assert b"Simulation workspace" in page
    assert request(server, "/app.js")[0] == request(server, "/style.css")[0] == 200
    status, payload = request(server, "/api/templates")
    assert status == 200
    assert {item["id"] for item in payload["templates"]} == {
        "01-two-approaching-particles",
        "02-parallel-particle-beams",
        "03-spreading-pulse",
        "04-unequal-mass-collision",
        "basic",
        "exchange",
        "finite_fields",
        "local_field_rules",
        "local_lorentz_field",
        "moving_source",
        "open_world",
        "spatial_causal_events",
        "spatial_computation_delay",
        "spatial_turning",
        "three_mass_finite",
    }
    for template in payload["templates"]:
        assert template["source"] == (ROOT / "examples" / f"{template['id']}.json").read_text(
            encoding="utf-8"
        )
    assert request(server, "/api/runs")[1] == {"runs": []}


@pytest.mark.parametrize("source", ['{"ticks":1,"ticks":2}', '{"schema_version":1}', "not JSON"])
def test_invalid_configuration_is_rejected_before_start(server, source):
    for endpoint in ("/api/validate", "/api/runs"):
        status, payload = request(server, endpoint, {"source": source})
        assert status == 400 and payload["error"]
    assert not server.workspace.output.exists()
    assert not server.workspace.jobs


@pytest.mark.parametrize(
    "headers",
    [
        {"X-Workspace-Token": "wrong"},
        {"Origin": "https://another.example"},
        {"Host": "another.example"},
        {"Sec-Fetch-Site": "cross-site"},
    ],
)
def test_other_origins_cannot_launch_a_local_process(server, headers):
    source = (ROOT / "examples/basic.json").read_text(encoding="utf-8")
    assert request(server, "/api/runs", {"source": source}, headers)[0] == 403
    assert not server.workspace.jobs


def test_routes_do_not_expose_arbitrary_files(server):
    for path in (
        "/../pyproject.toml",
        "/runs/../../pyproject.toml",
        "/%2e%2e/pyproject.toml",
        "/api/runs/" + "0" * 32,
        "/runs/" + "0" * 32 + "/state.json",
    ):
        assert request(server, path)[0] == 404
    assert request(server, "/api/templates", headers={"Host": "other.example"})[0] == 403


def test_editor_fragments_keep_the_strict_json_key_policy(server):
    status, payload = request(server, "/api/json", {"source": '{"amount":1,"amount":2}'})
    assert status == 400 and "duplicate JSON key" in payload["error"]
    assert request(server, "/api/json", {"source": '{"amount":2}'}) == (200, {"value": {"amount": 2}})


def test_export_saves_a_validated_download_with_the_exact_input(server):
    source = (ROOT / "examples/basic.json").read_text(encoding="utf-8")
    status, exported = request(server, "/api/export", {"source": source})
    assert status == 200
    connection = http.client.HTTPConnection("127.0.0.1", server.server_port)
    connection.request("GET", exported["url"])
    response = connection.getresponse()
    assert response.status == 200
    assert response.getheader("Content-Disposition") == f'attachment; filename="{exported["name"]}"'
    assert response.read().decode("utf-8") == source
    connection.close()
    assert request(server, "/api/export", {"source": "{}"})[0] == 400
    assert request(server, "/exports/" + "0" * 32 + ".json")[0] == 404


def test_changed_configuration_is_loaded_without_build_and_runs_match_cli(server, tmp_path):
    files = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "src").rglob("*.py")}
    document = json.loads((ROOT / "examples/exchange.json").read_bytes())
    identities = []
    for ticks in (2, 5):
        document["ticks"] = ticks
        document["model_id"] = f"edited-config-{ticks}"
        document["seeds"][0]["values"] = {"balance": 16 + ticks}
        source = json.dumps(document)
        status, checked = request(server, "/api/validate", {"source": source})
        assert status == 200 and checked["summary"]["ticks"] == ticks
        status, started = request(server, "/api/runs", {"source": source})
        assert status == 202
        job = wait_for_run(server, started["id"])
        assert job["status"] == "completed"
        metadata = job["metadata"]
        assert metadata["tick"] == metadata["completed_ticks"] == ticks
        assert metadata["display"] == "none"
        assert metadata["model"] == document["model_id"]
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["initial_totals"]["balance"] == [16 + ticks]
        saved = Path(job["output"])
        assert (saved / "initialization.json").read_bytes() == source.encode("utf-8")
        assert "run.html" not in job["artifacts"]
        initial = tmp_path / f"input-{ticks}.json"
        initial.write_bytes(source.encode("utf-8"))
        direct = tmp_path / f"direct-{ticks}"
        run_initialization(initial, direct)
        for name in ("run.json", "state.json", "events.jsonl", "initialization.json"):
            saved_bytes, direct_bytes = (saved / name).read_bytes(), (direct / name).read_bytes()
            if name == "run.json":
                assert without_elapsed(json.loads(saved_bytes)) == without_elapsed(
                    json.loads(direct_bytes)
                )
            else:
                assert saved_bytes == direct_bytes
            assert request(server, job["artifacts"][name]) == (200, (saved / name).read_bytes())
        identities.append(job["id"])
    assert len(set(identities)) == 2
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in files.items())


def test_workspace_runs_open_finite_example_headlessly_with_exact_escape_accounting(server):
    source = (ROOT / "examples/open_world.json").read_text(encoding="utf-8")
    status, checked = request(server, "/api/validate", {"source": source})
    assert status == 200 and checked["valid"]
    assert checked["summary"]["ticks"] == 12
    status, started = request(server, "/api/runs", {"source": source})
    assert status == 202
    job = wait_for_run(server, started["id"])
    assert job["status"] == "completed"
    metadata = job["metadata"]
    without_elapsed(metadata)
    assert metadata["schema_version"] == 2
    assert metadata["boundary"] == "open"
    assert metadata["display"] == "none"
    assert metadata["completed_ticks"] == metadata["tick"] == 12
    assert metadata["initial_totals"] == {"strength": [72], "radiation": [0]}
    assert metadata["source_totals"] == {"strength": [0], "radiation": [72]}
    assert metadata["escaped_totals"] == {"strength": [72], "radiation": [20]}
    assert metadata["dissipation_totals"] == {"strength": [0], "radiation": [0]}
    assert metadata["localized_totals"] == {"strength": [0], "radiation": [52]}
    assert metadata["final_totals"] == {"strength": [0], "radiation": [52]}
    assert metadata["accounting_balanced_at_every_completed_tick"]
    assert not metadata["conserved_at_every_completed_tick"]
    assert all(field["balanced"] for field in metadata["spatial_accounting"].values())
    assert set(job["artifacts"]) == {"initialization.json", "run.json", "state.json", "events.jsonl"}
    saved = Path(job["output"])
    assert (saved / "initialization.json").read_bytes() == source.encode("utf-8")
    state = json.loads((saved / "state.json").read_bytes())
    assert state["transfers"] == state["spatial_transfers"] == []
    assert all(not node["disturbances"] for node in state["nodes"])
    events = [json.loads(line) for line in (saved / "events.jsonl").read_bytes().splitlines()]
    assert any(event["event"] == "escaped" for event in events)
    assert any(event["event"] == "spatial_escaped" for event in events)
    assert {path.name for path in saved.iterdir()} == set(job["artifacts"])


def test_failed_engine_run_keeps_its_failure_metadata(server):
    document = json.loads((ROOT / "examples/exchange.json").read_bytes())
    document["couplings"][0]["amount"] = {"op": "exact_div", "args": [1, 0]}
    status, started = request(server, "/api/runs", {"source": json.dumps(document)})
    assert status == 202
    job = wait_for_run(server, started["id"])
    assert job["status"] == job["metadata"]["status"] == "failed"
    assert job["metadata"]["error"]
    assert "run.json" in job["artifacts"] and "state.json" in job["artifacts"]


def test_stop_and_duplicate_run_requests_are_explicit(server):
    document = json.loads((ROOT / "examples/exchange.json").read_bytes())
    document["ticks"] = 1000000000
    payload = {"source": json.dumps(document)}
    status, started = request(server, "/api/runs", payload)
    assert status == 202
    assert request(server, "/api/runs", payload)[0] == 409
    assert request(server, "/api/templates")[0] == 200  # HTTP remains responsive during physical work.
    status, stopped = request(server, f"/api/runs/{started['id']}/stop", {})
    assert status == 200 and stopped["status"] == "cancelled"
    assert server.workspace.jobs[started["id"]].process.poll() is not None
    assert request(server, f"/api/runs/{started['id']}/stop", {})[1]["status"] == "cancelled"


@pytest.mark.parametrize(
    "settings", [{"visualize": "false"}, {"frame_stride": 0}, {"frame_stride": True}]
)
def test_run_options_are_validated_before_spawning(server, settings):
    source = (ROOT / "examples/basic.json").read_text(encoding="utf-8")
    assert request(server, "/api/runs", {"source": source, **settings})[0] == 400
    assert not server.workspace.jobs


def test_workspace_shutdown_reaps_active_children(tmp_path):
    workspace = Workspace(ROOT / "examples", tmp_path)
    document = json.loads((ROOT / "examples/exchange.json").read_bytes())
    document["ticks"] = 1000000000
    started = workspace.start(json.dumps(document), False, 1)
    workspace.close()
    assert workspace.jobs[started["id"]].process.poll() is not None
    assert workspace.jobs[started["id"]].state == "cancelled"
