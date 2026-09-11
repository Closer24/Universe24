import base64
import multiprocessing
import re
import time
from io import BytesIO

import pytest
from PIL import Image

from event_universe.diagnostics.frames import Slice, VolumeFrame
from event_universe.diagnostics.live import LiveDisplay


def snapshot(tick=0):
    return VolumeFrame(tick, {(2, 3, 4): 1}, [(0, 2, 3, 4, 1, 0, 0)], (1, 0, 0), 10, (8, 8, 8))


def display_at(path):
    return LiveDisplay(path, title="Live <example>", total_ticks=4, view=Slice("XY", 4), volume=True)


@pytest.mark.visualization
def test_spawn_preview_is_available_before_finish_and_owns_a_copied_snapshot(tmp_path):
    display = display_at(tmp_path / "live output")
    try:
        display.start()
        page = display.output / "live.html"
        assert "Starting simulation" in page.read_text(encoding="utf-8")
        assert not (display.output / "run.html").exists()
        frame = snapshot()
        display.submit(frame)
        frame.tick = 99
        frame.field.clear()
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            text = page.read_text(encoding="utf-8")
            if 'id="frame"' in text:
                break
            assert display.error is None
            time.sleep(0.05)
        else:
            pytest.fail("the spawned consumer never published its initial snapshot")
        assert 'data-tick="0"' in text
        assert "99" not in text.split('id="tick"')[1].split("</p>")[0]
        assert "Simulation running" in text
        assert "may skip intermediate frames" in text
        assert '<meta http-equiv="refresh" content="1">' in text
        assert "Live &lt;example&gt;" in text
        assert not (display.output / "run.html").exists()
        encoded = re.search(r"data:image/png;base64,([^\"]+)", text).group(1)
        with Image.open(BytesIO(base64.b64decode(encoded))) as image:
            assert image.size == (1500, 1275)
        assert any(child.name == "Universe24LivePreview" for child in multiprocessing.active_children())
    finally:
        display.close()
    assert not any(child.name == "Universe24LivePreview" for child in multiprocessing.active_children())


@pytest.mark.visualization
def test_pending_large_preview_can_be_cancelled_without_queue_shutdown_deadlock(tmp_path):
    display = display_at(tmp_path)
    try:
        display.start()
        frame = snapshot()
        frame.field = {(index, 0, 0): index for index in range(20_000)}
        for tick in range(5):
            frame.tick = tick
            display.submit(frame)
        display.stop_preview()
        display.close()
        assert not any(
            child.name == "Universe24LivePreview" for child in multiprocessing.active_children()
        )
    finally:
        display.close()


@pytest.mark.visualization
def test_worker_start_failure_does_not_prevent_export_progress_or_failed_replay(tmp_path, monkeypatch):
    def denied_start(self):
        raise OSError("preview worker could not start")

    monkeypatch.setattr(multiprocessing.get_context("spawn").Process, "start", denied_start)
    display = display_at(tmp_path)
    with pytest.warns(RuntimeWarning, match="preview worker could not start"):
        display.start()
    display.submit(snapshot())
    display.stop_preview()
    display.rendered(0, Image.new("RGB", (20, 10), "blue"))
    text = (tmp_path / "live.html").read_text(encoding="utf-8")
    assert "Building recorded replay" in text
    assert "preview worker could not start" in text
    assert "data:image/png;base64," in text
    display.fail(ValueError("physical acceptance failed"))
    artifact = tmp_path / "failed replay #1.html"
    artifact.write_text("FAILED RUN", encoding="utf-8")
    display.finish(artifact)
    text = (tmp_path / "live.html").read_text(encoding="utf-8")
    assert "Run stopped" in text and "physical acceptance failed" in text
    assert "Run complete" not in text
    assert 'id="waiting"' not in text
    assert 'content="0; url=failed%20replay%20%231.html"' in text
    display.close()


def test_failure_does_not_redirect_to_a_stale_previous_run(tmp_path):
    (tmp_path / "run.html").write_text("An earlier run", encoding="utf-8")
    display = display_at(tmp_path)
    display.fail(RuntimeError("new export failed"))
    text = (tmp_path / "live.html").read_text(encoding="utf-8")
    assert "Run stopped" in text and "new export failed" in text
    assert 'id="waiting"' not in text
    assert "refresh" not in text
    assert 'href="run.html"' not in text


@pytest.mark.visualization
def test_worker_crash_after_the_last_submission_is_reported_at_shutdown(tmp_path):
    display = display_at(tmp_path)
    try:
        display.start()
        display.submit(snapshot())
        process = display._process
        assert process is not None
        process.kill()
        process.join(timeout=5)
        with pytest.warns(RuntimeWarning, match="preview process exited with code"):
            display.stop_preview()
        assert display.error is not None
        display.rendered(0, Image.new("RGB", (20, 10)))
        assert "Building recorded replay" in (tmp_path / "live.html").read_text(encoding="utf-8")
    finally:
        display.close()


def test_preview_publication_error_remains_diagnostic(tmp_path, monkeypatch):
    display = display_at(tmp_path)
    display.submit(snapshot())

    def unavailable(*args, **kwargs):
        raise PermissionError("preview page is unavailable")

    monkeypatch.setattr("event_universe.diagnostics.live._write_page", unavailable)
    with pytest.warns(RuntimeWarning, match="preview page is unavailable"):
        display.rendered(0, Image.new("RGB", (20, 10)))
    display.rendered(0, Image.new("RGB", (20, 10)))
    display.finish(tmp_path / "run.html")
    display.close()
    assert display.error == "preview page is unavailable"
