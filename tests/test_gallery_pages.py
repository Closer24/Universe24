"""The gallery's page tool (`tools/gallery_pages.py`) reads the engine and
draws; it replays no rule. Its capture is checked against the engine's own
stores on a minimal GameBoard and its page against the page convention
(the frame player, the GIF inside the HTML), headless, in seconds.

The world: an open cube of 7 x 7 x 7 with no measured event and two
declared rows of a paid family of one number and content, head-on on the
x axis from (1, 3, 3) on +x and (5, 3, 3) on -x, age 0. The expected
integers, written down first, from the flight table and the collision
table ([BEAM_LAW section 3 and section 4](../docs/BEAM_LAW.md)): a heading
crosses 32 Links in 55 intervals, its first two Links at the intervals 1
and 3, so the rows are at x = 2 and 4 after the interval 1, at x = 3 and 3
after the interval 3: they meet at (3, 3, 3) at the interval 3 and the
head-on pair parks on the rest slots (the class "+x -x" of four members,
the forward map the cyclic shift), so after the interval 3 both rows are at
the meeting Node with the rest direction (0, 0, 0); the capture reads the
same columns as the store, and the frames requested at the intervals 1 and
3 carry those ticks.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gallery_pages", ROOT / "tools" / "gallery_pages.py")
assert SPEC is not None and SPEC.loader is not None
gallery_pages = importlib.util.module_from_spec(SPEC)
sys.modules["gallery_pages"] = gallery_pages
SPEC.loader.exec_module(gallery_pages)


def head_on_world() -> dict[str, object]:
    def row(position: list[int], direction: list[int]) -> dict[str, object]:
        return {
            "position": position,
            "family": "light",
            "number": 1,
            "direction": direction,
            "amount": 1,
            "phase": 5,
            "age": 0,
        }

    return {
        "law": "beam",
        "model_id": "gallery-pages-test-v1",
        "shape": [7, 7, 7],
        "boundary": "open",
        "ticks": 6,
        "K": 1 << 20,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "measured": [],
        "in_transit": [row([1, 3, 3], [1, 0, 0]), row([5, 3, 3], [-1, 0, 0])],
    }


@pytest.fixture
def world_path(tmp_path: Path) -> Path:
    path = tmp_path / "head_on.json"
    path.write_text(json.dumps(head_on_world()), encoding="utf-8")
    return path


def test_capture_reads_the_stores_at_the_requested_intervals(world_path: Path) -> None:
    replay = gallery_pages.Replay(world_path)
    frames = replay.run([1, 3])
    assert [frame.tick for frame in frames] == [1, 3]
    first, meeting = frames
    rows = first.rows[0]
    assert rows.family == "light"
    assert sorted(zip(rows.x.tolist(), rows.y.tolist(), rows.z.tolist(), strict=True)) == [
        (2, 3, 3),
        (4, 3, 3),
    ]
    assert rows.phase.tolist() == [5, 5] and rows.amount.tolist() == [1, 1]
    # The frame is a copy of the store at that interval, not a view of the
    # store as it is now.
    store = replay.simulation.stores[0]
    x, _, _ = store.coordinates(store.node)
    assert x.tolist() == [3, 3]
    rows = meeting.rows[0]
    assert sorted(zip(rows.x.tolist(), rows.y.tolist(), rows.z.tolist(), strict=True)) == [
        (3, 3, 3),
        (3, 3, 3),
    ]
    rest = [replay.directions[int(d)] for d in rows.direction]
    assert rest == [(0, 0, 0), (0, 0, 0)]
    assert meeting.bodies == [] and [s.name for s in meeting.sets] == []


def test_frame_ticks_keeps_the_ends_and_the_bound() -> None:
    assert gallery_pages.frame_ticks(5) == [0, 1, 2, 3, 4, 5]
    ticks = gallery_pages.frame_ticks(3000, count=120)
    assert ticks[0] == 0 and ticks[-1] == 3000 and len(ticks) == 120
    assert all(b > a for a, b in zip(ticks[:-1], ticks[1:], strict=True))


def test_plane_and_cube_draw_every_row(world_path: Path) -> None:
    replay = gallery_pages.Replay(world_path)
    frames = replay.run([1, 3])
    plane = gallery_pages.plane_for(replay, scale=4)
    plane.largest = gallery_pages.largest_amounts(frames)
    assert plane.largest == {"light": 2.0}
    image = plane.image(frames[0])
    assert image.size == (7 * 4 + 12, 7 * 4 + 12)
    pixels = np.asarray(image)
    # Two lit Nodes at (2, 3) and (4, 3), y upward: rows 3 from the bottom.
    lit = {
        (x, y)
        for x in range(7)
        for y in range(7)
        if pixels[plane.pixel(x, y)[1].__int__(), plane.pixel(x, y)[0].__int__()].sum() > 60
    }
    assert lit == {(2, 3), (4, 3)}
    cube = gallery_pages.Cube(tuple(replay.world.shape), 12, replay.world.phase_steps, replay.directions)
    assert cube.image(frames[1], highlight=(3, 3, 3)).size == cube.size


def test_player_embeds_the_frames_the_gif_and_the_intervals(world_path: Path) -> None:
    replay = gallery_pages.Replay(world_path)
    frames = replay.run([0, 1, 2, 3])
    plane = gallery_pages.plane_for(replay, scale=3)
    images = [plane.image(frame) for frame in frames]
    player = gallery_pages.Player(
        "test", images, [f.tick for f in frames], [{"rows": "2"}] * 4, "A caption."
    )
    document = gallery_pages.page("A test page", "The lead.", player.html())
    assert "<title>A test page</title>" in document
    assert 'class="player" id="test"' in document
    assert "data:image/gif;base64," in document and "data:image/png;base64," in document
    assert '"ticks": [0, 1, 2, 3]' in document and '"count": 4' in document
    assert '<button class="play"' in document and 'input class="slider"' in document
    # The GIF is a visible image of the page: the picture moves without scripts.
    assert '<img class="gif" alt="the moving picture" src="data:image/gif;base64,' in document
    gif = gallery_pages.gif_bytes(images, 100)
    assert gif[:6] in (b"GIF87a", b"GIF89a")


def test_a_body_is_drawn_with_its_momentum_arrow_and_its_copies(tmp_path: Path) -> None:
    """A body of momentum (64, 0, 0) on a 9 x 9 x 1 plane releasing on +x:
    its arrow (accent-green pixels to its right, none at a momentum of zero) and
    its copies (translucent discs of its colour at its rows' Nodes, absent
    with `copies` off)."""
    world = {
        "law": "beam",
        "model_id": "gallery-pages-test-arrow-v1",
        "shape": [9, 9, 1],
        "boundary": {"z": "periodic"},
        "ticks": 4,
        "K": 4,
        "N": 64,
        "release": [1, 1],
        "suspension": 0,
        "families": [{"name": "m", "quantum": 0, "phase": False}],
        "measured": [
            {"position": [4, 4, 0], "family": "m", "amount": 8, "fixed": True, "directions": [[1, 0, 0]]}
        ],
    }
    path = tmp_path / "arrow.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    replay = gallery_pages.Replay(path)
    frames = replay.run([3])
    frame = frames[0]
    assert frame.rows[0].amount.size >= 1  # the body's own rows on +x
    plane = gallery_pages.plane_for(replay, scale=8)
    plane.largest = gallery_pages.largest_amounts(frames)
    still = np.asarray(plane.image(frame)).astype(int)
    moving = gallery_pages.Frame(
        frame.tick,
        frame.rows,
        [
            gallery_pages.Body(b.number, b.family, b.position, b.content, (64, 0, 0), b.phase)
            for b in frame.bodies
        ],
        frame.sets,
    )
    with_arrow = np.asarray(plane.image(moving)).astype(int)
    cx, cy = plane.pixel(4, 4)
    right = (slice(int(cy) - 2, int(cy) + 3), slice(int(cx) + 8, int(cx) + 20))
    white = lambda a: int(((a[right][:, :, 1] > 170) & (a[right][:, :, 0] < 130)).sum())  # noqa: E731  # the accent green
    assert white(still) == 0 and white(with_arrow) > 0
    plane.copies = False
    without = np.asarray(plane.image(frame)).astype(int)
    rx, ry = plane.pixel(5, 4)
    assert tuple(still[int(ry), int(rx)]) != tuple(without[int(ry), int(rx)])


def test_the_volume_draws_the_cube_and_every_lit_node(world_path: Path) -> None:
    """The three-dimensional view of the head-on world at the interval 1:
    the image has the projection's size, and the two rows' Nodes project
    to lit pixels (their family colour) where the projection says."""
    replay = gallery_pages.Replay(world_path)
    frames = replay.run([1])
    volume = gallery_pages.volume_for(replay, scale=10)
    volume.largest = gallery_pages.largest_amounts(frames)
    image = volume.image(frames[0])
    assert image.size == volume.size
    pixels = np.asarray(image).astype(int)
    for node in ((2, 3, 3), (4, 3, 3)):
        u, v = volume.project(*node)
        assert pixels[int(v), int(u)].sum() > 120
    u, v = volume.project(3, 5, 2)  # an unlit Node away from the cube's edges
    assert pixels[int(v), int(u)].sum() < 120
