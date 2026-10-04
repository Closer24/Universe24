"""The generator is Rule3 (ALGEBRA.md #the-generator): the generator lays a body as the fixed point of the row it reads, its declared count the weighted share its record lays, a body rotating in a sense beside its record, refusing a cloud, a body that fits no positive pace, a universe without T and two bodies sharing a region by name; it lays a message as the wave under its envelope by the rotation act, and an inner face of the board (the face rule inside it) reflects the wave but for its gap, the gate MATCH."""

import json
import math

import numpy as np

import event_universe.world_files as world_files
from event_universe.core import paces
from event_universe.game_board import GameBoard
from event_universe.loader.faces import faces_of
from event_universe.world_files import input_digest, load_world
from tests.laws import BACK, CHAIN, EVENTS, PACKET, SLIT, TOOL, chain_body_world, refused, slit_world


def dense(levels: dict[str, list[int]], shape: tuple[int, ...] = (24, 9, 1)) -> np.ndarray:
    """A level of the mode file's sparse form as the board's array, the slit board's without a shape."""
    found = np.bincount(levels["at"], levels["values"], int(np.prod(shape))).astype(np.int64)
    return found.reshape(shape)


def test_a_message_is_the_wave_under_its_envelope_and_the_inner_face_reflects_it(tmp_path, monkeypatch):
    """The message lay: now_i = b e_i cos(k x_i) at k = pi / 4 along x, b = 1,328, the raised cosine of half-width 4 about x = 5, and the before level the exact lay's, the real part of the packet z = b e e^(i k x) with every component advanced by its own omega(q) (ALGEBRA.md, The message lay), each level within two units of the test's own transform over the board's shape with the uniform content out in proportion to the envelope (the rounding and the division act's leftover units; the rotation act and no table); the loader admits the folded board and refuses by name a node_reader Node, a body Node and a laid level beyond the inner face, faces that leave no Node, a node_reader's `remainder` key (no count stands at a Node: the count is the record's share) and a message's `whole` Node without its `tick` (a lay whole by the count is at a declared tick of the run, `loader/messages.py`); a packet toward -x at the phase pi / 2 with the transverse wave number pi / 8 along y (`wave` [-1, 4], `phase` [1, 4], `transverse` {y: [1, 8]}) is laid as its mirror at that slant within two units of the same transform (the band cos omega(q) over x and y), and a transverse wave number on the along axis is refused by name; the screen's click lines are its report, the net inflow into its column through its front boundary Ports, never 0 and never a Node, beside the field's readings; in the run the Nodes beyond the board stay 0 in every family and the charge's share in quanta over the board stays above 0, the wave passes the gap (the light's levels beyond the wall, more in the gap's row than at the board's edge) and reflects elsewhere (more of its form before the wall than on the same board without the wall); the back-in-time gate says MATCH over the run. One Node declaring six quanta on the chain becomes a body of several Nodes, each carrying a quantum, their counts within the rounding of the declaration (one lay of the body of 6 at the integer fixed point serves every reading of the body: a test runs under 30 seconds, the owner's word of 2026-10-03; the lays of 10, 50 and 100 quanta are the generator's scaling, a run of tools/pixel_mode.py by name); its standing reading rotates above the matter band's top and below 2, its peak at the centre, its period read whole; the mode file stands for the world by its digest and the GameBoard loads its levels as written; a body laid with a sense carries its second level pair beside them, a neutral one none; the body of the charged family is one quantum of count 1 (the law's count per charged record, the loader's gate; ALGEBRA.md, No record reads its own write of the sign), laid by the generator as the one-Node record of its quantum (`--pixel`: the level now (A, 0) and the level before the band's rest rotation in its sense, so the first pair's second level is 0 at every Node and the second pair's level before carries the sense). Two quanta on the tests' chain of 24 are refused by name as a cloud, the top mode of the board as declared rotating at [230, 173] = 1.3295, under the band's top 1.3333 (in one dimension every well binds on a board that holds its mode, the board's length entering the lightest body's binding: on a chain of 28 the two quanta bind as two Nodes carrying a quantum each, a run of tools/pixel_mode.py by name; the cloud is otherwise a three-dimensional body's refusal by name); the body's well stands far below the Link's zero (no finite count collapses under the composed paces, the write per proper volume, ALGEBRA.md #the-paces, The paces compose); two bodies of ten quanta two Links apart at the centre are refused by name (no mode stands in the region left to the first body by the second's, or their regions share a Node), a universe without T and a sense other than +1 or -1 are refused by name. The lay at the integer fixed point (the world's `lay` of the kind `fixed_point`, loader/lay.py): the body of 7 quanta (6 under the bolometer's unit; 7 the least that binds at the fixed point in the family's quantum, a quantum carrying sin omega_0 = 0.745 of the form it carried in W_c) re-laid in the content it returns until the record's two levels and the content repeat within the declared stop of 1 unit at every Node, the mode file's trajectory ending within it after more than one pass, the loader reading the lay; the compact seed's lay by name at the stop of 8 units; the budget's gate refuses by name a tolerance whose least T is above the universe's. The aslant message toward -x at the phase pi / 2 with k_y = pi / 8 is the real pair of z = b e e^(i (-k x + k_y y + pi / 2)); the screen's lines are the region's report and the field's reading alone, no Node named."""
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
        assert not np.any([a[beyond] for s in walled.states for r in s.lines for a in (r.now, r.before)])
        assert walled.books()["charge"]["quanta"] > 0
    level = np.abs(walled.states[charge].lines[0].now[:, :, 0])
    passed, free = level[13:].sum(axis=0), np.abs(open_board.states[charge].lines[0].now[:12]).sum()
    assert passed[4] > passed[0] > 0 and level[:12].sum() > free and open_board.wrap.beyond is None
    assert BACK.verdict(GameBoard(load_world(path)), 24)["verdict"] == "MATCH"
    turned = chain_body_world(tmp_path, TOOL, senses=(1,))  # the rotating lay: one quantum of charge
    rotating = json.loads(turned.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert rotating["count"] == 1 and not any(rotating["moving"]["im_now"])  # the one-Node record (A, 0)
    assert any(rotating["moving"]["im_before"]) and len(rotating["moving"]["im_before"]) == CHAIN
    refused("is a cloud", lambda: chain_body_world(tmp_path, TOOL, 2))  # two quanta on the chain of 24
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
    """The generator's `count` of a message is the books' count of its record at the lay (`GameBoard.credit.counts`; the mathematician's finding of 2026-10-03): the lines the books count summed over the board and the total read in quanta once, never per Node, so the shipped two slits' 1,998 and the Zeno world's 667 are the books' own, and a dilute wave below half a quantum at every Node reads its one quantum over the board while the per-Node reading sums to 0."""
    for folder, name in (("two_slits", "two_slits"), ("zeno", "zeno_1")):
        world = EVENTS / folder / f"{name}.json"
        entries = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"]
        board = GameBoard(load_world(world))
        names = [family.name for family in board.families]
        assert [entry["count"] for entry in entries] == [
            board.credit.counts[names.index(e["family"])] for e in entries
        ]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    dilute = slit_world(tmp_path, TOOL, "dilute", messages=[{**PACKET, "amplitude": 80}])
    entry = json.loads(dilute.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"][0]
    board = GameBoard(load_world(dilute))
    charge = [family.name for family in board.families].index("charge")
    assert entry["count"] == board.credit.counts[charge] == 1 and not board.quanta(charge)[0].any()


def test_the_exact_before_level_puts_no_form_in_the_backward_root_beyond_the_rounding():
    """The exact message lay (ALGEBRA.md, The message lay; the hands' route, #1793 comments 5978111549 (c) and 5978208136 (3)) on the shipped worlds whose messages carry an envelope, the two slits, the which-way, the GHZ and Bell worlds (the anticoincidence's photons at the amplitudes 116 and 112 are left out: their rounding bound is 7 x 10^-2, above the bound that means something): each message laid by the generator as the mode file holds it (`pixel_mode`, through the division act) and read mode by mode against the law's exact lay in real numbers, the test's own floats from the file's keys (a_i = b e_i cos(k x_i + phi) and s_i = b e_i sin(k x_i + phi), the band cos omega(q) = (cos q_x + cos q_y + cos q_z) / 3 at the board's wave numbers, the before level the real part of the packet z = a + i s with every component advanced by its own omega(q), the uniform content of each level out in proportion to the envelope). The roots per bin, N_q = fftn(now) and B_q = fftn(before), u_q = (B_q - N_q e^(-i omega_q)) / (2 i sin omega_q) forward in time and v_q = (N_q e^(i omega_q) - B_q) / (2 i sin omega_q) backward, the bins with sin omega_q = 0 skipped (the uniform mode the division act removed, the staggered mode); a real pair's mirror bins carry the conjugate roots, u_(-q) = conj(v_q), so the backward root is read over the carrier's half-space, 0 < sign(p) q_along < pi, as its departure from the exact lay's own v*_q (the packet's mirror content, 0 beyond it before the rounding): misplaced = SUM_q |v_q - v*_q|^2 sin omega_q over the exact lay's forward form F* = SUM_q |u*_q|^2 sin omega_q. The same number for the plain lay's pair, before_i = b e_i cos(k x_i + phi + omega_k) from the same a and s (the engine's lay before this commit, the law's beta per component), rounded the same way. The bound from the rounding alone, from the file's own numbers: every laid level is off the real line by at most one half at every Node (the exact before level's tails reach every Node of the board, sqrt(1 - **L**^2) being no local read), so each level's error has the form at most N^2 / 4 over the bins (Parseval, N the board's Nodes) and the two levels' errors add in amplitude, SUM_q |R_q e^(i omega_q) - T_q|^2 <= N^2, the backward form from the error at most N^2 / (4 sin omega_min), sin omega_min the board's smallest nonzero sin omega_q: bound = N^2 / (4 sin omega_min F*). Printed per file, the plain lay's share, the exact lay's and the bound: the two slits 6.2 x 10^-2, 5.0 x 10^-6 and 2.0 x 10^-4, the which-way 6.2 x 10^-2, 6.5 x 10^-6 and 2.0 x 10^-4, the GHZ's three beams 2.8 x 10^-2, 4.3 x 10^-6 and 3.4 x 10^-4, Bell's two 7.2 x 10^-2, 1.2 x 10^-5 and 1.3 x 10^-5 and 3.1 x 10^-4 (the law's first-order estimate of the plain lay's share, 3.4 percent at the top 1 and the edge 6, is the band's narrow-width line; the exact per-component share at the shipped widths is larger); asserted: the exact lay's share below the bound and below the plain lay's by two orders, the bound below 10^-3. A single plane wave over a whole periodic box (the shipped Zeno drive, no edge, the top the whole axis) has one component, so its before level is the plain lay's, b cos(k x + phi + omega_k) by the same rounding, at every Node exactly."""

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

    def laid_by(document):
        """The world's messages as the generator lays them, dense over the board, with omega(q) and the bins."""
        shape = tuple(document["shape"])
        bins = [
            2 * np.pi * np.fft.fftfreq(n).reshape([-1 if a == axis else 1 for a in range(3)])
            for axis, n in enumerate(shape)
        ]
        omega = np.arccos(np.clip(sum(np.cos(q) for q in bins) / 3, -1, 1))
        entries = TOOL.pixel_mode(document)["messages"]
        pairs = [
            tuple(dense(entry["moving"][word], shape) for word in ("now", "before")) for entry in entries
        ]
        return pairs, omega, bins

    worlds = (
        ("two_slits", "two_slits"),
        ("which_way", "which_way"),
        ("ghz", "ghz_x_x_x"),
        ("bell", "bell_a_b"),
    )
    for folder, name in worlds:
        document = json.loads((EVENTS / folder / f"{name}.json").read_text(encoding="utf-8"))
        pairs, omega, bins = laid_by(document)
        for number, (message, pair) in enumerate(zip(document["messages"], pairs, strict=True)):
            a, s, envelope, omega_k = real_line(document, message)
            q_along = bins["xyz".index(message["along"])]
            half = np.broadcast_to(
                (np.sign(message["wave"][0]) * q_along > 0) & (np.abs(q_along) < np.pi), a.shape
            )
            advanced = np.real(np.fft.ifftn(np.fft.fftn(a + 1j * s) * np.exp(1j * omega)))
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
