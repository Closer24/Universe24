"""The generator is Rule3 (ALGEBRA.md #the-generator): the generator lays a body as the fixed point of the row it reads, its declared count the weighted share its record lays, a body rotating in a sense beside its record, refusing a cloud, a body that fits no positive pace, a universe without T and two bodies sharing a region by name; it lays a message as the wave under its envelope by the rotation act, and an inner face of the board (the face rule inside it) reflects the wave but for its gap, the gate MATCH."""

import json
import math
from dataclasses import replace

import numpy as np

import event_universe.world_files as world_files
from event_universe.core import paces
from event_universe.game_board import GameBoard
from event_universe.loader.faces import faces_of
from event_universe.world_files import input_digest, load_world
from tests.laws import (
    BACK,
    CHAIN,
    EVENTS,
    PACKET,
    SLIT,
    TOOL,
    chain_body_world,
    design_beside,
    refused,
    slit_world,
)


def dense(levels: dict[str, list[int]], shape: tuple[int, ...] = (24, 9, 1)) -> np.ndarray:
    """A level of the mode file's sparse form as the board's array, the slit board's without a shape."""
    found = np.bincount(levels["at"], levels["values"], int(np.prod(shape))).astype(np.int64)
    return found.reshape(shape)


def test_a_message_is_the_wave_under_its_envelope_and_the_inner_face_reflects_it(tmp_path, monkeypatch):
    """The message lay: now_i = b e_i cos(k x_i) at k = pi / 4 along x, b = 1,328, the raised cosine of half-width 4 about x = 5, and the before level the exact lay's, the real part of the packet z = b e e^(i k x) with every component advanced by its own omega(q) (ALGEBRA.md, The message lay), each level within two units of the test's own transform over the board's shape with the uniform content out in proportion to the envelope (the rounding and the division act's leftover units; the rotation act and no table); the loader admits the folded board and refuses by name a node_reader Node, a body Node and a laid level beyond the inner face, faces that leave no Node, a node_reader's `remainder` key (no count stands at a Node: the count is the record's share) and a message's `whole` Node without its `tick` (a lay whole by the count is at a declared tick of the run, `loader/messages.py`); a packet toward -x at the phase pi / 2 with the transverse wave number pi / 8 along y (`wave` [-1, 4], `phase` [1, 4], `transverse` {y: [1, 8]}) is laid as its mirror at that slant within two units of the same transform (the band cos omega(q) over x and y), and a transverse wave number on the along axis is refused by name; the screen's click lines are its report, the net inflow into its column through its front boundary Ports, never 0 and never a Node, beside the field's readings; in the run the Nodes beyond the board stay at the vacuum, 0 or the massless row's declared rest, in every family and the charge's share in quanta over the board stays above 0, the wave passes the gap (the light's levels beyond the wall, more in the gap's row than at the board's edge) and reflects elsewhere (more of its form before the wall than on the same board without the wall); the back-in-time gate says MATCH over the run. One Node declaring six quanta on the chain becomes a body of several Nodes, each carrying a quantum, their counts within the rounding of the declaration (one lay of the body of 6 at the integer fixed point serves every reading of the body: a test runs under 30 seconds, the owner's word of 2026-10-03; the lays of 10, 50 and 100 quanta are the generator's scaling, a run of tools/pixel_mode.py by name); its standing reading rotates above the matter band's top and below 2, its peak at the centre, its period read whole; the mode file stands for the world by its digest and the GameBoard loads its levels as written; a body laid with a sense carries its second level pair beside them, a neutral one none; the body of the charged family is one quantum of count 1 (the law's count per charged record, the loader's gate; ALGEBRA.md, No record reads its own write of the sign), laid by the generator as the one-Node record of its quantum (the design's `pixels`: the level now (A, 0) and the level before the band's rest rotation in its sense, so the first pair's second level is 0 at every Node and the second pair's level before carries the sense). Two quanta on a chain of 12 are refused by name as a cloud, the top mode of the board as declared rotating at [196, 147] = 1.3333, not above the band's top 1.3333 (in one dimension every well binds on a board that holds its mode, the board's length entering the lightest body's binding: at the declared vacuum content 60 the two quanta bind on the tests' chain of 24 at [196, 146] = 1.3425, as they bound on a chain of 28 at the content 0, where the chain of 24 refused them at [230, 173] = 1.3295, runs of tools/pixel_mode.py by name; the cloud is otherwise a three-dimensional body's refusal by name); the body's well stands far below the Link's zero (no finite count collapses under the composed paces, the write per proper volume, ALGEBRA.md #the-paces, The paces compose); two bodies of ten quanta two Links apart at the centre are refused by name (no mode stands in the region left to the first body by the second's, or their regions share a Node), a universe without T and a sense other than +1 or -1 are refused by name. The lay at the integer fixed point (the world's `lay` of the kind `fixed_point`, loader/lay.py): the body of 7 quanta (6 under the bolometer's unit; 7 the least that binds at the fixed point in the family's quantum, a quantum carrying sin omega_0 = 0.745 of the form it carried in W_c) re-laid in the content it returns until the record's two levels and the content repeat within the declared stop of 1 unit at every Node, the mode file's trajectory ending within it after more than one pass, the loader reading the lay; the compact seed's lay by name at the stop of 8 units; the budget's gate refuses by name a tolerance whose least T is above the universe's. The aslant message toward -x at the phase pi / 2 with k_y = pi / 8 is the real pair of z = b e e^(i (-k x + k_y y + pi / 2)); the screen's lines are the region's report and the field's reading alone, no Node named."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    screen = {"name": "screen", "positions": [[20, y, 0] for y in range(9)]}
    path = slit_world(tmp_path, TOOL, node_readers=[screen])
    mode = json.loads((mode_file := path.with_suffix(".mode.json")).read_text())["messages"][0]
    now, before = (dense(mode["moving"][word]) for word in ("now", "before"))
    k, x, y = math.pi / 4, np.arange(24)[:, None], np.arange(9)[None, :]
    away = np.abs(x - 5)
    envelope = np.where(away <= 4, (1 + np.cos(np.pi * away / 4)) / 2, 0.0)  # the raised cosine along x

    def exact(packet: np.ndarray) -> tuple[np.ndarray, np.ndarray]:  # the law's lay in the test's floats
        """The real pair of the packet z = b e e^(i k x) over the board's shape: now its real part, before the real part of z with every component advanced by its own omega(q), the uniform content of each out in proportion to the envelope (ALGEBRA.md, The message lay)."""
        bins = [2 * np.pi * np.fft.fftfreq(n) for n in packet.shape]
        omega = np.arccos((np.cos(bins[0])[:, None] + np.cos(bins[1])[None, :] + 1) / 3)
        advanced = np.real(np.fft.ifft2(np.fft.fft2(packet) * np.exp(1j * omega)))
        weights, beyond = np.broadcast_to(envelope, packet.shape), (x == 12) & (y != 4)  # the inner face
        now_line, before_line = (
            level - weights * level.sum() / weights.sum()
            for level in (np.where(beyond, 0.0, packet.real), np.where(beyond, 0.0, advanced))
        )
        return now_line, before_line

    straight = np.broadcast_to(1328 * envelope * np.exp(1j * k * x), (24, 9))  # z along x, flat over y
    for level, line in zip(
        (now, before), exact(straight), strict=True
    ):  # the gap's column, on the board
        assert (
            np.abs(level[:, 4, 0] - line[:, 4]).max() <= 2
        )  # within the rounding and the act's leftover
    assert (now[:, 4:5, :] == now).all() and mode["count"] > 0 and not now[12].any()
    assert int(now.sum()) == 0 and int(before.sum()) == 0
    inner, at = "beyond the board's inner face", {"node": [12, 0, 0], "count": 50}
    for change, reason in (
        (
            {"node_readers": [{"name": "d", "positions": [[12, 0, 0]]}]},
            f"{inner}: nothing stands there",
        ),
        ({"messages": [{**PACKET, "wave": [0, 4]}]}, "wave's p is 0"),
        ({"faces": [{"axis": "z", "at": 0, "gaps": []}]}, "faces leave no Node"),
        ({"messages": [{**PACKET, "whole": [5, 4, 0]}]}, "holds `whole` or `count` without `tick`"),
        (
            {"node_readers": [{**screen, "remainder": {"charge": 1}}]},
            "unknown key 'remainder'",
        ),  # no count
        ({"messages": [{**PACKET, "transverse": {"x": [1, 8]}}]}, "transverse holds the unknown key"),
    ):
        refused(reason, lambda c=change: load_world(slit_world(tmp_path, TOOL, "r", **c)))
    aslant = {**PACKET, "wave": [-1, 4], "phase": [1, 4], "transverse": {"y": [1, 8]}}
    turned = slit_world(tmp_path, TOOL, "turned", messages=[aslant])
    before = json.loads(turned.with_suffix(".mode.json").read_text())["messages"][0]["moving"]["before"]
    slanted = 1328 * envelope * np.exp(1j * (-k * x + math.pi / 2 + math.pi * y / 8))  # z at the slant
    assert np.abs(dense(before)[:, 4, 0] - exact(slanted)[1][:, 4]).max() <= 2
    body = {"family": "matter", "nodes": [at]}
    refused(f"{inner}: nothing stands there", TOOL.pixel_mode, {**SLIT, "bodies": [body]})
    tampered = json.loads(mode_file.read_text(encoding="utf-8"))
    tampered["messages"][0]["moving"]["now"]["at"].append(12 * 9)
    tampered["messages"][0]["moving"]["now"]["values"].append(5)
    mode_file.write_text(json.dumps(tampered), encoding="utf-8")
    refused(f"is 5 at the Node \\[12, 0, 0\\], {inner}", lambda: load_world(path))
    mode_file.write_text(json.dumps({**tampered, "messages": [mode]}), encoding="utf-8")
    walled = GameBoard(load_world(path), (lines := []).append)
    open_board = GameBoard(load_world(slit_world(tmp_path, TOOL, "open", faces=[])))
    charge, beyond = [family.name for family in walled.families].index("charge"), walled.wrap.beyond
    assert beyond is not None and beyond.sum() == 8 and not beyond[12, 4, 0]
    walled.step()
    assert not [x for x in lines if x["event"] == "click"] and not walled.quanta(charge)[0][beyond].any()
    for _ in range(23):
        walled.step(), open_board.step()
        risen = [x for x in lines if x["tick"] == walled.tick and x["node_reader"] == "screen"]
        assert all(
            x["event"] in ("click", "density") and not {"node", "ports"} & x.keys() for x in risen
        )
        assert all(x["inflow"] != 0 for x in risen if x["event"] == "click")
        levels = [a[beyond] for s in walled.states for r in s.lines for a in (r.now, r.before)]
        assert {int(v) for level in levels for v in level} <= {0, *(f.rest for f in walled.families)}
        assert walled.books()["charge"]["quanta"] > 0
    level = np.abs(walled.states[charge].lines[0].now[:, :, 0])
    passed, free = level[13:].sum(axis=0), np.abs(open_board.states[charge].lines[0].now[:12]).sum()
    assert passed[4] > passed[0] > 0 and level[:12].sum() > free and open_board.wrap.beyond is None
    assert BACK.verdict(GameBoard(load_world(path)), 24)["verdict"] == "MATCH"
    turned = chain_body_world(tmp_path, TOOL, senses=(1,))  # the rotating lay: one quantum of charge
    rotating = json.loads(turned.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert rotating["count"] == 1 and not any(rotating["moving"]["im_now"])  # the one-Node record (A, 0)
    assert any(rotating["moving"]["im_before"]) and len(rotating["moving"]["im_before"]) == CHAIN
    refused(
        "is a cloud", lambda: chain_body_world(tmp_path, TOOL, 2, chain=12)
    )  # two quanta, a chain of 12
    plain = json.loads(chain_body_world(tmp_path, TOOL, mode=False).read_text(encoding="utf-8"))
    refused("a sense is \\+1 or -1", lambda: TOOL.pixel_mode(json.loads(json.dumps(plain)), [2]))
    near = [{"family": "matter", "nodes": [{"node": [x, 0, 0], "count": 10}]} for x in (12, 14)]
    refused("share a Node|does not stand", TOOL.pixel_mode, {**plain, "bodies": near})
    fixed = json.loads((world := chain_body_world(tmp_path, TOOL, 7, mode=False)).read_text())
    fixed["lay"] = {"kind": "fixed_point", "stop": 1, "passes": 30, "seed": "one_node"}
    fixed["lay"].update(tolerance=[1, 4], confidence=[32, 1])
    world.write_text(json.dumps(fixed), encoding="utf-8"), TOOL.main(["--input", str(world)])
    mode_path = world.with_suffix(".mode.json")
    document, mode = (json.loads(p.read_text(encoding="utf-8")) for p in (world, mode_path))
    nodes = document["bodies"][0]["nodes"]  # the one declared Node became the body's Nodes
    laid = sum(entry["count"] for entry in nodes)
    assert len(nodes) > 1 and all(entry["count"] >= 1 for entry in nodes)
    assert (abs(laid - 7) - (abs(laid - 7) & 1)) ** 2 <= 4 * 7  # within the rounding
    entry, (a, den) = mode["bodies"][0], mode["bodies"][0]["clock"]
    assert TOOL.agree(entry["carried"], 7) and entry["count"] == 7 and entry["seed"] >= 1
    assert 2 * 4000 * den < a * 6000 and a < 2 * den  # above the band's top 2 x 4000 / 6000, below 2
    profile, peak, moving = entry["profile"], entry["amplitude"], entry["moving"]
    assert max(map(abs, profile)) == abs(profile[CHAIN // 2]) == peak > 0  # the peak at the centre
    assert entry["period"][1] == 2 and entry["period"][0] >= 4 and "im_now" not in moving
    assert moving["now"] == profile and len(moving["before"]) == len(profile) == CHAIN
    assert (entry["pair"], entry["family"]) == ([4000, 6000], "matter")
    assert mode["world_digest"] == input_digest(document)
    passes = entry["lay"]["trajectory"]  # the integer fixed point's passes, the last within the stop
    assert len(passes) > 1 and max(passes[-1][1:3]) <= 1 and load_world(world).lay.stop == 1
    board = GameBoard(load_world(world))  # lawful, the family's two levels
    matter = board.states[[family.name for family in board.families].index("matter")].lines[0]
    assert matter is not None and matter.now[CHAIN // 2, 0, 0] == peak
    assert matter.before.ravel().tolist() == entry["moving"]["before"]
    held = [s for f, s in zip(board.families, board.states, strict=True) if f.held and not f.wronskian]
    deep = int(sum(s.lines[0].now for s in held).max())
    assert 0 < deep < paces.frozen_content(board.world.node_clock)  # the well below the Link's zero
    compact = dict(fixed, lay=dict(fixed["lay"], seed="compact", profile=[76, 4], stop=8))
    world.write_text(json.dumps(compact), encoding="utf-8"), TOOL.main(["--input", str(world)])
    seeded = json.loads(mode_path.read_text(encoding="utf-8"))["bodies"][0]
    assert seeded["lay"]["seed"] == "compact" and load_world(world).lay.profile == (76, 4)
    first = TOOL.compact_seed(100, (12, 0, 0), (24, 1, 1), TOOL.Wrap(False, True, True), (76, 4))
    assert first[11:14, 0, 0].tolist() == [4, 92, 4] and first.sum() == 100  # folded Ports: the centre
    for words, lay in (("seed is one", {"seed": "wide"}), ("profile .* seed", {"seed": "compact"})):
        refused(words, TOOL.lay_of, {"kind": "repeat", **lay}, "lay")
    document["lay"]["tolerance"] = [1, 1000]  # a tolerance T cannot meet: the budget's gate
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path.write_text(json.dumps({**mode, "world_digest": input_digest(document)}))
    refused("below the least T", lambda: load_world(world))
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    del universe["integers"]["quantum_action"]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    refused("declares no quantum_action T", lambda: TOOL.pixel_mode(plain))


def test_a_messages_mode_count_is_the_books_count_read_once_over_the_board(tmp_path, monkeypatch):
    """The generator's `count` of a message is the books' count of its record at the lay (`GameBoard.credit.counts`; the mathematician's finding of 2026-10-03): the lines the books count summed over the board and the total read in quanta once, never per Node, so the shipped two slits' 1,804 and the Zeno world's 833 are the books' own at the content the generator counts at, 0 (`message_entry` reads no rest: at the declared rest 60 the engine's books read the same lay at 1,844, the share at the paces Gamma - 2 c_vac), and a dilute wave below half a quantum at every Node reads its one quantum over the board while the per-Node reading sums to 0."""
    for folder, name in (("two_slits", "two_slits"), ("zeno", "zeno_1")):
        world = EVENTS / folder / f"{name}.json"
        entries = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"]
        loaded = load_world(world)  # the generator counts at the content 0, no rest read
        board = GameBoard(replace(loaded, families=tuple(replace(f, rest=0) for f in loaded.families)))
        names, books = [family.name for family in board.families], board.credit.counts  # the lay's paces
        assert [e["count"] for e in entries] == [books[names.index(e["family"])] for e in entries]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    dilute = slit_world(tmp_path, TOOL, "dilute", messages=[{**PACKET, "amplitude": 80}])
    entry = json.loads(dilute.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"][0]
    board = GameBoard(load_world(dilute))
    charge = [family.name for family in board.families].index("charge")
    assert entry["count"] == board.credit.counts[charge] == 1 and not board.quanta(charge)[0].any()


def test_the_exact_before_level_puts_no_form_in_the_backward_root_beyond_the_rounding():
    """The exact message lay (ALGEBRA.md, The message lay; the hands' route, #1793 comments 5978111549 (c) and 5978208136 (3)) on the shipped worlds whose messages carry an envelope, the two slits, the which-way, the GHZ and Bell worlds (the anticoincidence's photons at the amplitudes 116 and 112 are left out: their rounding bound is 7 x 10^-2, above the bound that means something): each message laid by the generator as the mode file holds it (`pixel_mode`, through the division act) and read mode by mode against the law's exact lay in real numbers, the test's own floats from the file's keys (a_i = b e_i cos(k x_i + phi) and s_i = b e_i sin(k x_i + phi), the band cos omega(q) = (cos q_x + cos q_y + cos q_z) / 3 at the board's wave numbers, the before level the real part of the packet z = a + i s with every component advanced by its own omega(q), the uniform content of each level out in proportion to the envelope). The roots per bin, N_q = fftn(now) and B_q = fftn(before), u_q = (B_q - N_q e^(-i omega_q)) / (2 i sin omega_q) forward in time and v_q = (N_q e^(i omega_q) - B_q) / (2 i sin omega_q) backward, the bins with sin omega_q = 0 skipped (the uniform mode the division act removed, the staggered mode); a real pair's mirror bins carry the conjugate roots, u_(-q) = conj(v_q), so the backward root is read over the carrier's half-space, 0 < sign(p) q_along < pi, as its departure from the exact lay's own v*_q (the packet's mirror content, 0 beyond it before the rounding): misplaced = SUM_q |v_q - v*_q|^2 sin omega_q over the exact lay's forward form F* = SUM_q |u*_q|^2 sin omega_q. The backward root's absolute share, SUM_q |v_q|^2 sin omega_q over F*, stays at the analytic packet's own leakage into the mirror bins (a + i s of a finite envelope is not one-sided; the advisor's remark, #1793 comment 5980093560 (2)), 3.6 x 10^-4 of the form at the two slits at the weight sin omega and 2.3 x 10^-4 at sin^2 omega (Bell's 3.1 x 10^-4 and 2.7 x 10^-4, the GHZ's 6.8 x 10^-3 with its envelope across the beam), and the misplaced share is the integer lay's departure from it, the rounding's. The same number for the plain lay's pair, before_i = b e_i cos(k x_i + phi + omega_k) from the same a and s (the engine's lay before this commit, the law's beta per component), rounded the same way. The bound from the rounding alone, from the file's own numbers: every laid level is off the real line by at most one half at every Node (the exact before level's tails reach every Node of the board, sqrt(1 - **L**^2) being no local read), so each level's error has the form at most N^2 / 4 over the bins (Parseval, N the board's Nodes) and the two levels' errors add in amplitude, SUM_q |R_q e^(i omega_q) - T_q|^2 <= N^2, the backward form from the error at most N^2 / (4 sin omega_min), sin omega_min the board's smallest nonzero sin omega_q: bound = N^2 / (4 sin omega_min F*). The transform runs over the board at its largest declared extents (a receding axis's `largest`, the packet at its coordinates, the before level cropped to the board), as the generator's does. Printed per file, the plain lay's share, the exact lay's and the bound (a GameBoard diagnostic read at this commit, re-read at the frozen hash): the two slits 6.6 x 10^-2, 6.8 x 10^-6 and 2.3 x 10^-4, the which-way 6.6 x 10^-2, 6.2 x 10^-6 and 2.3 x 10^-4, the GHZ's three beams 2.8 x 10^-2, 4.3 x 10^-6 and 3.4 x 10^-4, Bell's two 7.6 x 10^-2, 9.5 x 10^-6 and 6.5 x 10^-6 and 3.1 x 10^-4 (the law's first-order estimate of the plain lay's share, 3.4 percent at the top 1 and the edge 6, is the band's narrow-width line; the exact per-component share at the shipped widths is larger); asserted: the exact lay's share below the bound and below the plain lay's by two orders, the bound below 10^-3. A single plane wave over a whole periodic box (the shipped Zeno drive, no edge, the top the whole axis) has one component, so its before level is the plain lay's, b cos(k x + phi + omega_k) by the same rounding, at every Node exactly."""

    def real_line(document, message):
        """The law's a and s in the test's floats from the file's keys, the envelope b e_i and the carrier's omega_k."""
        shape = tuple(document["shape"])
        numbers = {name: (0, 1) for name in "xyz"}
        numbers.update({n: tuple(v) for n, v in message.get("transverse", {}).items()})
        numbers[message["along"]] = tuple(message["wave"])
        k = [math.pi * p / q for p, q in (numbers[name] for name in "xyz")]
        envelope = message["amplitude"] * np.ones(shape)
        for axis, name in enumerate("xyz"):
            (first, last), h, at = message["top"][name], message["edge"][name], np.arange(shape[axis])
            away = np.maximum(np.maximum(first - at, at - last), 0)
            taper = np.where(away <= h, (1 + np.cos(np.pi * away / (h or 1))) / 2, 0.0)
            envelope = envelope * taper.reshape([-1 if a == axis else 1 for a in range(3)])
        turned, whole = message["phase"]
        phase = sum(k[a] * np.indices(shape)[a] for a in range(3)) + 2 * math.pi * turned / whole
        carrier = math.acos(sum(map(math.cos, k)) / 3)
        return envelope * np.cos(phase), envelope * np.sin(phase), envelope, carrier

    def roots(now, before, omega):
        """The pair's forward and backward roots per bin, 0 where sin omega_q is 0."""
        n_q, b_q = (np.fft.fftn(np.asarray(level, dtype=float)) for level in (now, before))
        kept = np.sin(omega) > 1e-9
        sine = 2j * np.where(kept, np.sin(omega), 1.0)
        forward, backward = (
            (b_q - n_q * np.exp(-1j * omega)) / sine,
            (n_q * np.exp(1j * omega) - b_q) / sine,
        )
        return np.where(kept, forward, 0), np.where(kept, backward, 0)

    def rounded(level):
        return np.floor(level + 0.5)

    def band(shape):
        """The board's bins per axis and omega(q) over a shape."""
        bins = [
            2 * np.pi * np.fft.fftfreq(n).reshape([-1 if a == axis else 1 for a in range(3)])
            for axis, n in enumerate(shape)
        ]
        return bins, np.arccos(np.clip(sum(np.cos(q) for q in bins) / 3, -1, 1))

    def laid_by(document):
        """The world's messages as the generator lays them, dense over the board, with omega(q), the bins and the largest extents (a receding axis's `largest`, else the shape's)."""
        shape = tuple(document["shape"])
        receding = document.get("receding", {})
        largest = tuple(receding.get(n, {}).get("largest", k) for n, k in zip("xyz", shape, strict=True))
        entries = TOOL.pixel_mode(document)["messages"]
        pairs = [
            tuple(dense(entry["moving"][word], shape) for word in ("now", "before")) for entry in entries
        ]
        return pairs, *band(shape), largest

    worlds = (
        ("two_slits", "two_slits"),
        ("which_way", "which_way"),
        ("ghz", "ghz_x_x_x"),
        ("bell", "bell_a_b"),
    )
    for folder, name in worlds:
        document = json.loads((EVENTS / folder / f"{name}.json").read_text(encoding="utf-8"))
        pairs, bins, omega, largest = laid_by(document)
        for number, (message, pair) in enumerate(zip(document["messages"], pairs, strict=True)):
            a, s, envelope, omega_k = real_line(document, message)
            q_along = bins["xyz".index(message["along"])]
            half = np.broadcast_to(
                (np.sign(message["wave"][0]) * q_along > 0) & (np.abs(q_along) < np.pi), a.shape
            )
            packet, within = np.zeros(largest, dtype=complex), tuple(slice(0, n) for n in a.shape)
            packet[within] = (
                a + 1j * s
            )  # the packet at its coordinates on the board at its largest extents
            advanced = np.real(np.fft.ifftn(np.fft.fftn(packet) * np.exp(1j * band(largest)[1])))[within]
            beyond = np.zeros(a.shape, dtype=bool)  # the Nodes beyond an inner face, 0 before the act
            for at in faces_of(document["faces"], a.shape) if "faces" in document else ():
                beyond[at] = True
            ideal = [
                np.where(beyond, 0.0, level)
                - envelope * np.where(beyond, 0.0, level).sum() / envelope.sum()
                for level in (a, advanced)
            ]  # the law's lay in reals, the division act last
            plain = (rounded(a), rounded(a * math.cos(omega_k) - s * math.sin(omega_k)))
            sine, (u_star, v_star) = np.sin(omega)[half], roots(*ideal, omega)
            forward = float((np.abs(u_star[half]) ** 2 * sine).sum())
            shares = {
                word: float((np.abs(roots(*laid, omega)[1] - v_star)[half] ** 2 * sine).sum() / forward)
                for word, laid in (("plain", plain), ("exact", pair))
            }
            bound = a.size**2 / (4 * float(np.sin(omega)[np.sin(omega) > 1e-9].min()) * forward)
            print(
                f"{folder}/{name} messages[{number}]: the plain lay's misplaced share {shares['plain']:.3e}, "
                f"the exact lay's {shares['exact']:.3e}, the rounding's bound {bound:.3e}"
            )
            assert shares["exact"] < bound < 1e-3 and 100 * shares["exact"] < shares["plain"]
    document = json.loads(
        (EVENTS / "zeno" / "zeno_1.json").read_text(encoding="utf-8")
    )  # one plane wave
    a, s, _envelope, omega_k = real_line(document, document["messages"][0])
    assert (laid_by(document)[0][0][1] == rounded(a * math.cos(omega_k) - s * math.sin(omega_k))).all()


def test_the_generators_count_is_the_designs_and_a_re_lay_without_the_designs_key_is_refused(
    tmp_path, monkeypatch
):
    """The generator's input count (`designed_quanta`, `declared`; the advisor's breaker and the mathematician's audit, #1793 comments 5981736108 K6, 5982140872 B3; the Boss's 5981734131 item 6; two hands): a body declared on its Nodes, a body laid before, is re-laid at the design file's `quanta` and never at its Nodes' sum, the engine's reading of the lay before (the shipped pixel's design names its count where its Nodes' sum is the reading); the tool refuses such a world by name, naming the folder, the world and the key, with no design file beside it, with the mode file beside it alone (a mode file written elsewhere stands for no design) and with a design file naming no `quanta` for its world; a direct call of `pixel_mode` without the count is refused by name too; with the key the design's count is the lay's input, the mode entry's `count`, its share and the re-laid Nodes' sum within the rounding, and a new body on one Node keeps its declared count beside a design's."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, mode=False)  # one Node carrying 6, a new body
    document = json.loads(world.read_text(encoding="utf-8"))
    nodes = [{"node": [x, 0, 0], "count": c} for x, c in ((11, 1), (12, 3), (13, 1))]  # a lay before, 5
    document["bodies"][0]["nodes"] = nodes
    world.write_text(json.dumps(document), encoding="utf-8")
    named = f"{tmp_path.name}/chain.json bodies\\[0\\] is declared on 3 Nodes, a body laid before, and "
    design = tmp_path / "design.json"  # the chain's design beside it: its lay's keys and no `quanta`
    refused(named + f"the design file {design} names no `quanta`", TOOL.main, ["--input", str(world)])
    design.unlink()
    refused(named + "no design.json in .* names no `quanta`", TOOL.main, ["--input", str(world)])
    world.with_suffix(".mode.json").write_text(json.dumps({"bodies": [{"count": 5}]}), encoding="utf-8")
    refused(named + "no design.json", TOOL.main, ["--input", str(world)])  # the mode file is no design
    refused("bodies\\[0\\] is declared on 3 Nodes.*design file's `quanta`", TOOL.pixel_mode, document)
    pixel = EVENTS / "matter_alone" / "pixel.json"
    shipped = json.loads((pixel.parent / "design.json").read_text(encoding="utf-8"))["worlds"]["pixel"]
    assert TOOL.designed_quanta(pixel, json.loads(pixel.read_text(encoding="utf-8"))) == [
        shipped["quanta"]
    ]
    design.write_text(json.dumps({"worlds": {"chain": {"quanta": 6}}}), encoding="utf-8")
    one = {"family": "matter", "nodes": [{"node": [12, 0, 0], "count": 5}]}
    assert (
        TOOL.designed_quanta(world, document) == [6]
        and TOOL.declared(one, (CHAIN, 1, 1), 6, "b")[2] == 5
    )
    TOOL.main(["--input", str(world)])
    entry = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    laid = sum(n["count"] for n in json.loads(world.read_text(encoding="utf-8"))["bodies"][0]["nodes"])
    print(f"the body declared on 3 Nodes summing to 5 re-laid at the design's {entry['count']}: {entry}")
    assert entry["count"] == 6 and TOOL.agree(entry["carried"], 6) and TOOL.agree(laid, 6)


def test_the_generator_refuses_a_wave_at_p_0_by_name_before_any_lay(tmp_path, monkeypatch, capsys):
    """The generator's own refusal of a wave at p = 0 (`wave_of`; the advisor's breaker and the mathematician's audit, #1793 comments 5981736108 K6, 5982140872 B3; the Boss's 5981734131 item 6; two hands): the tool laid the wave [0, q] as any, the now level 0 at every Node of a massless family and the before level nonzero, a lay the loader alone refused; a world with the wave [0, 4] is refused by the tool by name, naming the message and the wave, through its command (no mode file written) and through `pixel_mode` with a body declared beside the message (nothing laid, no round printed); the loader's own refusal stands on a world file carrying the wave under its mode file's digest; the shipped two slits' world lays as its mode file holds it."""
    two_slits = EVENTS / "two_slits" / "two_slits.json"
    shipped = json.loads(two_slits.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"]
    entries = TOOL.pixel_mode(json.loads(two_slits.read_text(encoding="utf-8")))["messages"]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    still, words = {**PACKET, "wave": [0, 4]}, "messages\\[0\\].wave's p is 0 in the wave \\[0, 4\\]"
    refused(words, slit_world, tmp_path, TOOL, "still", messages=[still])
    assert not (tmp_path / "still.mode.json").exists()
    body, _ = {"family": "matter", "nodes": [{"node": [5, 4, 0], "count": 6}]}, capsys.readouterr()
    refusal = refused(words, TOOL.pixel_mode, {**SLIT, "messages": [still], "bodies": [body]})
    assert capsys.readouterr().err == ""  # no lay and no round printed before the refusal
    path = slit_world(tmp_path, TOOL)  # the wave [1, 4] laid, then the file turned to p = 0 by hand
    document = {**json.loads(path.read_text(encoding="utf-8")), "messages": [still]}
    path.write_text(json.dumps(document), encoding="utf-8")
    mode = json.loads((mode_path := path.with_suffix(".mode.json")).read_text(encoding="utf-8"))
    mode_path.write_text(json.dumps({**mode, "world_digest": input_digest(document)}), encoding="utf-8")
    refused("messages\\[0\\].wave's p is 0: a message has", lambda: load_world(path))  # the loader's own
    print(f"the tool's refusal: {refusal}; the two slits' message laid as shipped: {entries == shipped}")
    assert entries == shipped


def test_the_generators_sense_and_one_node_declaration_are_the_design_files_and_the_flags_are_refused(
    tmp_path, monkeypatch
):
    """The generator's two inputs beside the count are the design file's (the owner's decision C2, #1793 comment 5982379080; `design_entry`, `designed_lay`): `senses`, the rotation sense per body in the world's order, and `pixels`, the bodies laid as the one-Node record of their quanta, read from the folder's design.json beside the world, its world's entry or the design's own, and never from the command line: `--sense` and `--pixel` on the command line are refused by name with the words "the design file's" before the world is read (no mode file written); a design naming a body in `pixels` without its sense is refused by name naming the design file's `senses`; with both keys the chain's one quantum of the charged family is laid as the one-Node record in its sense, as the flags laid it, the design's own keys standing where the design has no entry for the world; the pair atom's shipped design carries the keys its builder passed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, senses=(1,), mode=False)  # its design entry written beside
    for flags in (["--sense", "1"], ["--pixel", "0"], ["--sense=1", "--pixel=0"]):
        refusal = refused("the design file's", TOOL.main, ["--input", str(world), *flags])
    assert not world.with_suffix(".mode.json").exists() and str(refusal).startswith("--sense=1 on the")
    design_beside(tmp_path, "chain", senses=[], pixels=[0])
    refused(
        "one-Node record with no sense.*the design file's `senses`", TOOL.main, ["--input", str(world)]
    )
    (tmp_path / "design.json").write_text(json.dumps({"senses": [1], "pixels": [0]}), encoding="utf-8")
    assert TOOL.designed_lay(world) == ([1], (0,)) and TOOL.design_entry(world) == {
        "senses": [1],
        "pixels": [0],
    }
    TOOL.main(["--input", str(world)])
    entry = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert entry["count"] == 1 and entry["lay"]["kind"] == TOOL.DECLARATION
    assert not any(entry["moving"]["im_now"]) and any(
        entry["moving"]["im_before"]
    )  # the one-Node record
    pair = json.loads((EVENTS / "pair_atom" / "design.json").read_text(encoding="utf-8"))
    print(
        f"the flags' refusal: {refusal}; the chain's one-Node record {entry['clock']}; the pair atom's design {pair['senses']} {pair['pixels']}"
    )
    assert (pair["senses"], pair["pixels"]) == ([1, -1], [0, 1]) and TOOL.designed_lay(
        EVENTS / "a.json"
    ) == ([], ())


def test_a_packet_of_a_gapped_family_is_advanced_by_its_own_band_and_a_massless_one_by_the_vacuums(
    tmp_path, monkeypatch
):
    """R370 (the reviewer's #1793 comment 5984295586 section C, the advisor's 5984314233 (3); the law's (h), **L** the line's own read of the message's family): the generator's exact before level advances every component of a packet by its family's own band, cos omega(q) = (num / den) (cos q_x + cos q_y + cos q_z) / 3, the massless band its case at num = den; a plane wave cos(k x) at k = pi / 4 over a periodic box of 8 Nodes has one component, so its before level is A cos(k x + omega) rounded once half up, omega from that formula in the test's own floats, at matter's pair [4000, 6000] and at the charge's [6000, 6000]."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    plane = {**PACKET, "top": {"x": [0, 7], "y": [0, 0], "z": [0, 0]}, "edge": {"x": 0, "y": 0, "z": 0}}
    box = {"shape": [8, 1, 1], "boundary": {axis: "periodic" for axis in "xyz"}, "faces": []}
    for family, (num, den) in (("matter", (4000, 6000)), ("charge", (6000, 6000))):
        path = slit_world(tmp_path, TOOL, family, messages=[{**plane, "family": family}], **box)
        entry = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"][0]
        omega = math.acos(num / den * (math.cos(math.pi / 4) + 2) / 3)  # the family's own band
        before = np.floor(1328 * np.cos(math.pi / 4 * np.arange(8) + omega) + 0.5).astype(int)
        assert dense(entry["moving"]["before"], (8, 1, 1)).ravel().tolist() == before.tolist()
