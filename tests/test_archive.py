"""Complete disk histories, bounded streaming, and deterministic resource cleanup."""

import io
import json
from importlib.resources import files
from pathlib import Path

import pytest

from event_universe import archive, runner
from event_universe.archive import JsonArchive, write_json
from event_universe.diagnostics.disturbance_render import render_disturbances

from .test_disturbance_engine import document, kind


def test_archive_copies_json_values_and_supports_indexed_prefixes(tmp_path):
    with JsonArchive(tmp_path) as history:
        original = {"tick": 0, "values": [1, -2], "vector": (3, 4, 5)}
        history.append(original)
        original["values"].append(99)
        history.append({"tick": 0, "count": 1})
        history.append({"tick": 2, "count": 2})
        assert len(history) == 3
        assert history[0] == {"tick": 0, "values": [1, -2], "vector": [3, 4, 5]}
        assert history[-1] == {"tick": 2, "count": 2}
        assert history[1:] == [{"tick": 0, "count": 1}, {"tick": 2, "count": 2}]
        assert list(history)[0] == history[0]
        with pytest.raises(IndexError):
            _ = history[3]
    assert history.closed
    assert list(tmp_path.iterdir()) == []


def test_partial_encoding_rolls_back_without_changing_the_saved_prefix(tmp_path):
    with JsonArchive(tmp_path) as history:
        history.append({"sequence": 1})
        with pytest.raises(TypeError):
            history.append({"encoded_first": [2, 3], "invalid": object()})
        assert len(history) == 1
        history.append({"sequence": 2})
        assert json.loads("".join(history.json_chunks())) == [{"sequence": 1}, {"sequence": 2}]


def test_nested_archive_export_matches_json_without_loading_items(tmp_path, monkeypatch):
    values = [{"label": "<signal> \N{SNOWMAN}", "payload": "x" * 170000}, {"tick": 3}]
    with JsonArchive(tmp_path) as history:
        for value in values:
            history.append(value)

        def cannot_materialize(self, index):
            pytest.fail("stream export must not read whole history items")

        monkeypatch.setattr(JsonArchive, "__getitem__", cannot_materialize)
        assert max(map(len, history.json_chunks())) <= 65536
        output = io.StringIO()
        write_json(output, {"history": history, "other": [True, None, (1, 2)]}, escape_html=True)
        expected = json.dumps({"history": values, "other": [True, None, (1, 2)]})
        assert output.getvalue() == expected.replace("<", "\\u003c")


def test_second_file_creation_failure_closes_the_first(tmp_path, monkeypatch):
    opened = []
    original = archive.TemporaryFile

    def open_file(**options):
        if opened:
            raise OSError("index creation failed")
        handle = original(**options)
        opened.append(handle)
        return handle

    monkeypatch.setattr(archive, "TemporaryFile", open_file)
    with pytest.raises(OSError, match="index creation"):
        JsonArchive(tmp_path)
    assert opened[0].closed
    assert list(tmp_path.iterdir()) == []


def test_indexed_reads_can_interleave_with_a_streaming_export(tmp_path):
    with JsonArchive(tmp_path) as history:
        history.append({"payload": "x" * 140000})
        history.append({"tick": 2})
        chunks = history.json_chunks()
        saved = [next(chunks), next(chunks)]
        assert history[-1] == {"tick": 2}
        saved.extend(chunks)
        assert json.loads("".join(saved)) == [{"payload": "x" * 140000}, {"tick": 2}]


def test_history_context_closes_both_files_after_a_consumer_failure(tmp_path):
    with pytest.raises(ValueError, match="consumer failed"):
        with JsonArchive(tmp_path) as history:
            history.append({"sequence": 1})
            raise ValueError("consumer failed")
    assert history.closed
    assert history._index.closed
    assert list(tmp_path.iterdir()) == []


def test_streamed_playback_is_byte_equivalent_to_the_previous_json_embedding(tmp_path):
    frames = [{"tick": 0, "cells": [], "transfers": []}, {"tick": 2, "cells": []}]
    metadata = {"model": "<configured>", "shape": (3, 3, 3)}
    observation = {"samples": [{"audit_tick": 0, "received_count": 0}], "receipts": []}
    with JsonArchive(tmp_path) as history:
        for frame in frames:
            history.append(frame)
        output = render_disturbances(history, tmp_path / "movie.html", metadata, observation=observation)
    template = files("event_universe").joinpath("ui_assets", "playback.html").read_text("utf-8")
    encoded = json.dumps({"frames": frames, "metadata": metadata, "observation": observation})
    expected = template.replace("__RECORDING__", encoded.replace("<", "\\u003c"))
    assert output.read_text(encoding="utf-8") == expected


@pytest.mark.parametrize("fail_export", [False, True])
def test_runner_closes_spooled_observer_histories_even_when_export_fails(
    tmp_path, monkeypatch, fail_export
):
    created = []

    class TrackedArchive(JsonArchive):
        def __init__(self):
            super().__init__(tmp_path)
            created.append(self)

    monkeypatch.setattr(runner, "JsonArchive", TrackedArchive)
    raw = document([kind("resident")], [((0, 0, 0), "resident")])
    raw.update(ticks=3, observer={"position": [0, 0, 0], "max_receipts": 1})
    source = tmp_path / "initial.json"
    source.write_text(json.dumps(raw))
    if fail_export:
        original = Path.open

        def open_file(path, *args, **kwargs):
            if path.name == "observations.json":
                raise OSError("observer export failed")
            return original(path, *args, **kwargs)

        monkeypatch.setattr(Path, "open", open_file)
        with pytest.raises(OSError, match="observer export"):
            runner.run_initialization(source, tmp_path / "output")
    else:
        runner.run_initialization(source, tmp_path / "output")
        saved = json.loads((tmp_path / "output/observations.json").read_text())
        assert [item["audit_tick"] for item in saved["samples"]] == [0, 1, 2, 3]
        assert saved["receipts"] == []
    assert len(created) == 2
    assert all(history.closed and history._index.closed for history in created)
