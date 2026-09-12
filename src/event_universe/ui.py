"""Local, build-free configuration workspace for the initialization-driven runner."""

import argparse
import hmac
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from pathlib import Path
from typing import BinaryIO, cast
from urllib.parse import urlsplit
from uuid import uuid4

from event_universe.configuration_validation import validate_configuration
from event_universe.initialization import parse_json_document
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path

if sys.platform == "win32":
    _creation_flags = subprocess.CREATE_NO_WINDOW
else:
    _creation_flags = 0

MAX_REQUEST = 1_048_576
ARTIFACTS = {"initialization.json", "run.json", "state.json", "events.jsonl", "run.html"}
RUN_ROUTE = re.compile(r"/api/runs/([a-f0-9]{32})(?:/(stop))?")
FILE_ROUTE = re.compile(r"/runs/([a-f0-9]{32})/([a-z.]+)")
EXPORT_ROUTE = re.compile(r"/exports/([a-f0-9]{32})\.json")
CLEANUP_INTERVAL_SECONDS = 30


def validate_source(source: object) -> dict[str, object]:
    """Use the same strict data validator as the CLI, without executing a simulation."""
    if not isinstance(source, str) or len(source.encode("utf-8")) > MAX_REQUEST:
        raise ValueError("configuration must be JSON text no larger than 1 MiB")
    report = validate_configuration(source, kind="initialization")
    if not report.valid:
        raise ValueError(report.issues[0].message)
    return report.summary


def default_configs() -> Path:
    source = Path(__file__).resolve().parents[2] / "examples"
    return source if source.is_dir() else Path(sys.prefix) / "share/event-universe/examples"


@dataclass
class Job:
    identifier: str
    model: str
    requested_ticks: int
    output: Path
    process: subprocess.Popen[bytes]
    log: BinaryIO
    started: float
    initialization: Path
    lease: ArtifactLease
    state: str = "running"
    elapsed: float = 0

    def refresh(self) -> None:
        code = self.process.poll()
        if code is not None:
            if self.state == "running":
                self.state = "completed" if code == 0 else "failed"
                self.elapsed = time.monotonic() - self.started
            self._finish()

    def _finish(self) -> None:
        try:
            self.log.close()
        finally:
            if self.log.closed:
                self.lease.finish()

    def describe(self) -> dict[str, object]:
        self.refresh()
        metadata: object = None
        path = self.output / "run.json"
        if self.state != "running" and path.is_file():
            try:
                metadata = json.loads(path.read_bytes())
            except ValueError, OSError:
                pass
        return {
            "id": self.identifier,
            "model": self.model,
            "status": self.state,
            "requested_ticks": self.requested_ticks,
            "elapsed_seconds": time.monotonic() - self.started
            if self.state == "running"
            else self.elapsed,
            "metadata": metadata,
            "artifacts": {
                name: f"/runs/{self.identifier}/{name}"
                for name in sorted(ARTIFACTS)
                if (self.output / name).is_file() and self.state != "running"
            },
            "output": str(self.output),
        }

    def stop(self) -> None:
        self.refresh()
        if self.state != "running":
            return
        try:
            self.process.terminate()
        except OSError:
            if self.process.poll() is None:
                raise
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=3)
        self.state = "cancelled"
        self.elapsed = time.monotonic() - self.started
        self._finish()


class Workspace:
    """Own host jobs and immutable inputs; never implement or modify physical laws."""

    def __init__(self, configs: Path, output: Path) -> None:
        validate_output_path(output)
        self.configs = configs.resolve()
        self.output = output.resolve()
        self.jobs: dict[str, Job] = {}
        self.exports: dict[str, tuple[Path, str]] = {}
        self.lock = threading.Lock()

    def export(self, source: object) -> dict[str, str]:
        summary = validate_source(source)
        assert isinstance(source, str)
        identifier = uuid4().hex
        directory = self.output / "exports"
        path = directory / f"{identifier}.json"
        validate_output_path(path)
        directory.mkdir(parents=True, exist_ok=True)
        with path.open("xb"):
            pass
        with ArtifactLease(self.output, [path]):
            path.write_bytes(source.encode("utf-8"))
        name = re.sub(r"[^a-zA-Z0-9_-]", "_", str(summary["model"]))[:80] + ".json"
        with self.lock:
            self.exports[identifier] = (path, name)
        return {"url": f"/exports/{identifier}.json", "name": name}

    def templates(self) -> list[dict[str, object]]:
        result: list[dict[str, object]] = []
        for path in sorted(self.configs.glob("*.json")):
            if path.stat().st_size > MAX_REQUEST:
                continue
            try:
                source = path.read_text(encoding="utf-8")
                summary = validate_source(source)
            except ValueError, OSError, RecursionError:
                continue
            result.append(
                {
                    "id": path.stem,
                    "name": re.sub(r"^\d+-", "", path.stem).replace("-", " ").title(),
                    "source": source,
                    "summary": summary,
                }
            )
        return result

    def start(self, source: object, visualize: object, stride: object) -> dict[str, object]:
        summary = validate_source(source)
        if type(visualize) is not bool or type(stride) is not int or stride < 1:
            raise ValueError("visualize must be a boolean and frame_stride a positive integer")
        assert isinstance(source, str)
        with self.lock:
            for job in self.jobs.values():
                job.refresh()
                if job.state == "running":
                    raise RuntimeError(
                        "A simulation is already running. Stop it or wait for completion."
                    )
            identifier = uuid4().hex
            inputs = self.output / "inputs"
            initialization = inputs / f"{identifier}.json"
            log_path = inputs / f"{identifier}.log"
            destination = self.output / "runs" / identifier
            for path in (initialization, log_path, destination):
                validate_output_path(path)
            inputs.mkdir(parents=True, exist_ok=True)
            with initialization.open("xb"):
                pass
            command = [
                sys.executable,
                "-m",
                "event_universe",
                "--init",
                str(initialization),
                "--output",
                str(destination),
                "--frame-stride",
                str(stride),
            ]
            if visualize:
                command.append("--visualize")
            environment = os.environ.copy()
            package_root = str(Path(__file__).resolve().parent.parent)
            environment["PYTHONPATH"] = package_root + os.pathsep + environment.get("PYTHONPATH", "")
            environment["PYTHONUTF8"] = "1"
            log = log_path.open("xb")
            lease: ArtifactLease | None = None
            try:
                lease = ArtifactLease(
                    self.output, [initialization, Path(log.name)], keep_alive_with=[destination]
                )
                initialization.write_bytes(source.encode("utf-8"))
                process = subprocess.Popen(
                    command,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    env=environment,
                    creationflags=_creation_flags,
                )
            except BaseException:
                try:
                    log.close()
                finally:
                    if lease is not None and log.closed:
                        lease.finish()
                raise
            job = Job(
                identifier,
                str(summary["model"]),
                int(cast(int, summary["ticks"])),
                destination,
                process,
                log,
                time.monotonic(),
                initialization,
                lease,
            )
            self.jobs[identifier] = job
            return job.describe()

    def cleanup(self, *, now: float | None = None) -> dict[str, object]:
        """Refresh host ownership before expiring generated files and their links."""
        with self.lock:
            for job in self.jobs.values():
                job.refresh()
            report = cleanup_expired(self.output, now=now)
            self.jobs = {
                identifier: job
                for identifier, job in self.jobs.items()
                if job.state == "running"
                or any(path.exists() for path in (job.output, job.initialization, Path(job.log.name)))
            }
            self.exports = {
                identifier: exported
                for identifier, exported in self.exports.items()
                if exported[0].is_file()
            }
            return report

    def close(self) -> None:
        with self.lock:
            for job in self.jobs.values():
                job.stop()


class WorkspaceServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, workspace: Workspace, port: int = 8765) -> None:
        self.workspace = workspace
        self.token = secrets.token_urlsafe(32)
        self._last_cleanup = float("-inf")
        super().__init__(("127.0.0.1", port), WorkspaceHandler)
        self.origin = f"http://127.0.0.1:{self.server_port}"

    def server_close(self) -> None:
        try:
            self.workspace.close()
        finally:
            super().server_close()

    def service_actions(self) -> None:
        now = time.monotonic()
        if now - self._last_cleanup >= CLEANUP_INTERVAL_SECONDS:
            self.workspace.cleanup()
            self._last_cleanup = now


class WorkspaceHandler(BaseHTTPRequestHandler):
    server: WorkspaceServer

    def log_message(self, format: str, *args: object) -> None:
        pass

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(10)

    def _local_request(self) -> bool:
        return (
            self.headers.get("Host") == self.server.origin.removeprefix("http://")
            and self.headers.get("Origin", self.server.origin) == self.server.origin
            and self.headers.get("Sec-Fetch-Site", "same-origin") in {"same-origin", "none"}
        )

    def _send(self, content: bytes, kind: str, status: int = 200, download: str | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(content)))
        if download is not None:
            self.send_header("Content-Disposition", f'attachment; filename="{download}"')
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        # Recorded renderer documents contain their own inline script and styles.
        policy = "default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'"
        if self.path.startswith("/runs/"):
            policy += "; script-src 'unsafe-inline'; style-src 'unsafe-inline'"
        self.send_header("Content-Security-Policy", policy)
        self.end_headers()
        self.wfile.write(content)

    def _json(self, value: object, status: int = 200) -> None:
        self._send(json.dumps(value).encode(), "application/json; charset=utf-8", status)

    def do_GET(self) -> None:
        if not self._local_request():
            self._json({"error": "Only this local workspace may access the server."}, 403)
            return
        path = urlsplit(self.path).path
        if path.startswith(("/api/runs", "/runs/", "/exports/")):
            self.server.workspace.cleanup()
        if path in {"/", "/app.js", "/style.css"}:
            name = "index.html" if path == "/" else path[1:]
            content = files("event_universe").joinpath("ui_assets", name).read_bytes()
            if path == "/":
                content = content.replace(b"__WORKSPACE_TOKEN__", self.server.token.encode())
            kind = {"/": "text/html", "/app.js": "text/javascript", "/style.css": "text/css"}[path]
            self._send(content, kind + "; charset=utf-8")
        elif path == "/api/templates":
            self._json({"templates": self.server.workspace.templates()})
        elif path == "/api/runs":
            with self.server.workspace.lock:
                self._json(
                    {
                        "runs": [
                            job.describe() for job in reversed(list(self.server.workspace.jobs.values()))
                        ][:20]
                    }
                )
        elif match := RUN_ROUTE.fullmatch(path):
            with self.server.workspace.lock:
                job = self.server.workspace.jobs.get(match[1])
                self._json(job.describe() if job else {"error": "Run not found"}, 200 if job else 404)
        elif match := EXPORT_ROUTE.fullmatch(path):
            with self.server.workspace.lock:
                exported = self.server.workspace.exports.get(match[1])
                try:
                    download_content = exported[0].read_bytes() if exported else None
                except FileNotFoundError:
                    download_content = None
            if download_content is None or exported is None:
                self._json({"error": "Export not found"}, 404)
            else:
                self._send(download_content, "application/json; charset=utf-8", download=exported[1])
        elif match := FILE_ROUTE.fullmatch(path):
            with self.server.workspace.lock:
                job = self.server.workspace.jobs.get(match[1])
                try:
                    download_content = (
                        (job.output / match[2]).read_bytes()
                        if job is not None and match[2] in ARTIFACTS
                        else None
                    )
                except FileNotFoundError:
                    download_content = None
            if download_content is None:
                self._json({"error": "Artifact not found"}, 404)
                return
            kind = "text/html" if match[2].endswith(".html") else "text/plain"
            self._send(download_content, kind + "; charset=utf-8")
        else:
            self._json({"error": "Not found"}, 404)

    def do_POST(self) -> None:
        if not self._local_request() or not hmac.compare_digest(
            self.headers.get("X-Workspace-Token", ""), self.server.token
        ):
            self._json({"error": "Reload the local workspace before submitting changes."}, 403)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_REQUEST or self.headers.get("Transfer-Encoding"):
                raise ValueError("request must contain at most 1 MiB of JSON")
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError("request must be a JSON object")
            path = urlsplit(self.path).path
            if path == "/api/json":
                fragment = body.get("source")
                if not isinstance(fragment, str):
                    raise ValueError("JSON fragment must be text")
                self._json({"value": parse_json_document(fragment)})
            elif path == "/api/export":
                self._json(self.server.workspace.export(body.get("source")))
            elif path == "/api/validate":
                self._json({"valid": True, "summary": validate_source(body.get("source"))})
            elif path == "/api/runs":
                self._json(
                    self.server.workspace.start(
                        body.get("source"), body.get("visualize", False), body.get("frame_stride", 1)
                    ),
                    HTTPStatus.ACCEPTED,
                )
            elif (match := RUN_ROUTE.fullmatch(path)) and match[2] == "stop":
                with self.server.workspace.lock:
                    job = self.server.workspace.jobs.get(match[1])
                    if job is None:
                        self._json({"error": "Run not found"}, 404)
                    else:
                        job.stop()
                        self._json(job.describe())
            else:
                self._json({"error": "Not found"}, 404)
        except (ValueError, RecursionError) as error:
            self._json({"error": str(error)}, 400)
        except RuntimeError as error:
            self._json({"error": str(error)}, 409)
        except OSError as error:
            self._json({"error": f"Could not access run files or start the runner: {error}"}, 500)


def main() -> None:
    parser = argparse.ArgumentParser(description="Open the local Universe24 configuration workspace.")
    parser.add_argument(
        "--port", type=int, default=8765, help="Local HTTP port; 0 chooses an unused port"
    )
    parser.add_argument(
        "--configs", type=Path, default=default_configs(), help="Folder of JSON templates"
    )
    parser.add_argument("--output", type=Path, default=Path("artifacts/workspace"))
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("port must be between 0 and 65535")
    try:
        server = WorkspaceServer(Workspace(args.configs, args.output), args.port)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot start workspace: {error}\n")
    print(
        f"Universe24 workspace: {server.origin}\nKeep this terminal open. Press Ctrl+C to stop.",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
