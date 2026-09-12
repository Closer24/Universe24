"""A disposable live preview of copied state, separate from authoritative run output."""

import base64
import html
import multiprocessing
import os
import pickle
import time
import warnings
from collections import deque
from io import BytesIO
from multiprocessing.process import BaseProcess
from multiprocessing.queues import Queue
from multiprocessing.synchronize import Event
from pathlib import Path
from queue import Empty, Full
from urllib.parse import quote
from uuid import uuid4

from PIL import Image

from .frames import Frame, Slice, VolumeFrame


def _write_page(
    output: Path,
    *,
    title: str,
    phase: str,
    tick: int,
    total_ticks: int,
    png: bytes | None = None,
    detail: str = "",
    error: str | None = None,
    destination: str | None = None,
    refresh: bool = True,
) -> None:
    """Publish one complete standalone page, never a partially written image or document."""
    refresh_tag = '<meta http-equiv="refresh" content="1">' if refresh else ""
    if destination is not None:
        refresh_tag = (
            f'<meta http-equiv="refresh" content="0; url={html.escape(destination, quote=True)}">'
        )
    picture = (
        '<img id="frame" alt="Live simulation snapshot" src="data:image/png;base64,'
        + base64.b64encode(png).decode("ascii")
        + '">'
        if png is not None
        else '<p id="waiting">The first image is being prepared.</p>'
        if refresh and destination is None
        else ""
    )
    link = (
        f'<p><a href="{html.escape(destination, quote=True)}">Open the recorded replay</a></p>'
        if destination is not None
        else ""
    )
    warning = f'<p class="warning">Live preview: {html.escape(error)}</p>' if error else ""
    progress = min(100, max(0, round(100 * tick / max(1, total_ticks))))
    document = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{refresh_tag}
<title>{html.escape(title)} — Live</title><style>
body{{margin:0;background:#080f1c;color:#edf5ff;font:16px system-ui}}
main{{max-width:1050px;margin:auto;padding:24px}}h1{{font-size:24px}}
img{{display:block;width:100%;height:auto;border-radius:12px}}
progress{{width:100%;accent-color:#4cc9ff}}p{{color:#c2d5ed}}a{{color:#4cc9ff}}
.warning{{color:#ffd166}}#phase{{font-size:20px;color:#74ffac}}
</style></head><body><main><h1>{html.escape(title)}</h1>
<p id="phase">{html.escape(phase)}</p>
<p id="tick" data-tick="{tick}">Tick {tick} / {total_ticks}</p>
<progress value="{progress}" max="100"></progress>
<p id="detail">{html.escape(detail)}</p>{warning}{link}{picture}
</main></body></html>"""
    temporary = output / f".live-{uuid4().hex}.tmp"
    try:
        temporary.write_text(document, encoding="utf-8")
        os.replace(temporary, output / "live.html")
    finally:
        temporary.unlink(missing_ok=True)


def _preview_worker(
    incoming: Queue[bytes],
    stopping: Event,
    errors: Queue[str],
    output: Path,
    title: str,
    total_ticks: int,
    view: Slice,
    volume: bool,
) -> None:
    """Consume only copied snapshots; the child never receives a ScalarEngine or a callback."""
    picture = output / f".live-frame-{os.getpid()}.png"
    volume_history: deque[VolumeFrame] = deque(maxlen=8)
    slice_history: deque[Frame] = deque(maxlen=8)
    try:
        while not stopping.is_set():
            try:
                packet = incoming.get(timeout=0.2)
            except Empty:
                continue
            for _ in range(8):
                try:
                    packet = incoming.get_nowait()
                except Empty:
                    break
            if stopping.is_set():
                break
            # These bytes originate only from this run's own snapshot producer.
            frame = pickle.loads(packet)
            from .render import render_run_preview, render_volume_preview

            if volume:
                if not isinstance(frame, VolumeFrame):
                    raise TypeError("a volume preview requires a VolumeFrame")
                volume_history.append(frame)
                render_volume_preview(tuple(volume_history), picture)
            else:
                if not isinstance(frame, Frame):
                    raise TypeError("a slice preview requires a Frame")
                slice_history.append(frame)
                render_run_preview(tuple(slice_history), view, picture)
            if stopping.is_set():
                break
            _write_page(
                output,
                title=title,
                phase="Simulation running",
                tick=frame.tick,
                total_ticks=total_ticks,
                png=picture.read_bytes(),
                detail=(
                    "Live snapshots may skip intermediate frames. Framing and color scale "
                    "follow the available history. The image counter ends at the latest preview "
                    "tick; the page counter shows the requested run. The recorded replay uses one fixed scale."
                ),
            )
    except Exception as error:
        try:
            errors.put_nowait(f"{type(error).__name__}: {error}")
        except Full:
            pass
    finally:
        picture.unlink(missing_ok=True)


class LiveDisplay:
    """Keep preview work bounded and disposable while every canonical frame is retained."""

    def __init__(self, output: Path, *, title: str, total_ticks: int, view: Slice, volume: bool) -> None:
        self.output = output
        self.title = title
        self.total_ticks = total_ticks
        self.view = view
        self.volume = volume
        self.error: str | None = None
        self._process: BaseProcess | None = None
        self._incoming: Queue[bytes] | None = None
        self._errors: Queue[str] | None = None
        self._stopping: Event | None = None
        self._ticks: list[int] = []
        self._last_publish = float("-inf")
        self._artifact: Path | None = None
        self._failure: str | None = None
        self._started = False
        self._publish_failed = False

    def _record_error(self, error: Exception | str) -> None:
        if self.error is None:
            self.error = str(error)
            try:
                warnings.warn(
                    f"Live preview unavailable: {self.error}. Recorded output is still being generated.",
                    RuntimeWarning,
                    stacklevel=2,
                )
            except RuntimeWarning:
                # A warning-as-error policy must not change physical stepping or saved output.
                pass

    def start(self) -> None:
        if self._started:
            return
        self._started = True
        try:
            self.output = self.output.resolve()
            self.output.mkdir(parents=True, exist_ok=True)
            _write_page(
                self.output,
                title=self.title,
                phase="Starting simulation",
                tick=0,
                total_ticks=self.total_ticks,
                detail="This page updates automatically while the run and replay are prepared.",
            )
            context = multiprocessing.get_context("spawn")
            self._incoming = context.Queue(maxsize=1)
            self._errors = context.Queue(maxsize=1)
            self._stopping = context.Event()
            self._process = context.Process(
                target=_preview_worker,
                args=(
                    self._incoming,
                    self._stopping,
                    self._errors,
                    self.output,
                    self.title,
                    self.total_ticks,
                    self.view,
                    self.volume,
                ),
                name="Universe24LivePreview",
                daemon=True,
            )
            self._process.start()
        except Exception as error:
            self._record_error(error)
            self.close()

    def submit(self, frame: Frame | VolumeFrame) -> None:
        """Serialize before returning so later caller mutation cannot reach the consumer."""
        self._ticks.append(frame.tick)
        if self._incoming is None:
            return
        try:
            self._check_worker()
            packet = pickle.dumps(frame, protocol=pickle.HIGHEST_PROTOCOL)
            try:
                self._incoming.put_nowait(packet)
            except Full:
                try:
                    self._incoming.get_nowait()
                except Empty:
                    return
                try:
                    self._incoming.put_nowait(packet)
                except Full:
                    pass
        except Exception as error:
            self._record_error(error)
            self.close()

    def _check_worker(self) -> None:
        if self._errors is not None:
            try:
                raise RuntimeError(self._errors.get_nowait())
            except Empty:
                pass
        if self._process is not None and self._process.exitcode is not None:
            raise RuntimeError(f"preview process exited with code {self._process.exitcode}")

    def stop_preview(self) -> None:
        """Reap the sole preview writer before the parent publishes canonical export progress."""
        process = self._process
        terminated = False
        try:
            if self._stopping is not None:
                self._stopping.set()
            if process is not None and process.pid is not None:
                process.join(timeout=2)
                if process.is_alive():
                    terminated = True
                    process.terminate()
                    process.join(timeout=2)
                if process.is_alive():
                    process.kill()
                    process.join(timeout=2)
                if process.is_alive():
                    raise RuntimeError("preview process did not stop")
                if not terminated and process.exitcode not in (None, 0):
                    self._record_error(f"preview process exited with code {process.exitcode}")
            if self._errors is not None:
                try:
                    self._record_error(self._errors.get_nowait())
                except Empty:
                    pass
        except Exception as error:
            self._record_error(error)
            # Do not race a surviving worker's page writes in the final export callback.
            self._publish_failed = True
        finally:
            for channel in (self._incoming, self._errors):
                if channel is not None:
                    channel.cancel_join_thread()
                    channel.close()
            self._incoming = None
            self._errors = None
            self._stopping = None
            if process is None or not process.is_alive():
                self._process = None

    def rendered(self, index: int, image: Image.Image) -> None:
        """Publish selected already-rendered rasters without slowing every GIF frame."""
        if self._publish_failed:
            return
        now = time.monotonic()
        if now - self._last_publish < 0.75 and index != len(self._ticks) - 1:
            return
        try:
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            tick = self._ticks[index]
            _write_page(
                self.output,
                title=self.title,
                phase="Building recorded replay",
                tick=tick,
                total_ticks=self.total_ticks,
                png=buffer.getvalue(),
                detail=f"Rendering frame {index + 1} of {len(self._ticks)}. All saved frames are retained.",
                error=self.error,
            )
            self._last_publish = now
        except Exception as error:
            self._record_error(error)
            self._publish_failed = True

    def finish(self, artifact: Path) -> None:
        self.close()
        try:
            self._artifact = artifact.resolve()
            self._terminal_page(
                "Run stopped" if self._failure is not None else "Run complete",
                self._failure or "Opening the complete recorded replay.",
            )
        except Exception as error:
            self._record_error(error)

    def fail(self, error: BaseException) -> None:
        self._failure = str(error)
        self.close()
        self._terminal_page("Run stopped", str(error))

    def _terminal_page(self, phase: str, detail: str) -> None:
        if self._process is not None and self._process.is_alive():
            return
        destination = None
        if self._artifact is not None:
            try:
                destination = quote(self._artifact.relative_to(self.output).as_posix())
            except ValueError:
                destination = self._artifact.as_uri()
        try:
            _write_page(
                self.output,
                title=self.title,
                phase=phase,
                tick=self._ticks[-1] if self._ticks else 0,
                total_ticks=self.total_ticks,
                detail=detail,
                error=self.error,
                destination=destination,
                refresh=False,
            )
        except Exception as error:
            self._record_error(error)

    def close(self) -> None:
        self.stop_preview()
