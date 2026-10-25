"""Hand N2: the entropy of the clicks on a fresh 300-interval run of the hole seed at den 697,786 (the 3-cube torus, Gamma 1,000, T 36,000; the world declares nothing, so seed.uniform_seed lays the sea with the hole at the origin and the board reads itself). The lattice is stepped in-process as tools/eras.py steps it, every output line kept (credit, birth, lay, refused, click, density), and the birth's selector `meeting_board.drawn_among` is watched from outside (a wrapper in this script; src/ untouched) so that every draw's room, the count of affordable lists at the meeting Node, is read with the quotient `left` it drew by. The readings, integers only, per interval t: the credits, births, lays and refusals; the click records N(t) (credits and births, history kept and never run back) with bit_length(N); the distinct click records D(t); the draws and their rooms; the law's quantity H(t) = SUM over the draws to t of bit_length(room - 1), the bits the clicks wrote (a certain draw of one list writes 0 bits; a draw among 2^k lists writes k), and Omega(t) = PRODUCT of the rooms, the number of records consistent with the clicks, with bit_length(Omega - 1) = H(t) exactly where every room is a power of two; monotone by construction, shown non-decreasing at every interval. Then tools/back_in_time.py on the same world (the run back's verdict) by subprocess.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/n2/hole_seed_entropy.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import event_universe.meeting_board as meeting_board
from event_universe.lattice import Lattice
from event_universe.world_files import load_world

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
OUT = HERE.with_name("out")
DEN, GAMMA, T = 697786, 1000, 36000
SHAPE, INTERVALS = [3, 3, 3], 300
EVERY = 25
PYTHON = sys.executable


def write_world() -> Path:
    OUT.mkdir(exist_ok=True)
    universe = OUT / "u697786.json"
    universe.write_text(json.dumps({"integers": {"den": DEN, "node_clock": GAMMA, "quantum_action": T}}) + "\n", encoding="utf-8")
    world = OUT / "hole300.json"
    world.write_text(json.dumps({"universe": str(universe.relative_to(ROOT)), "shape": SHAPE, "intervals": INTERVALS}) + "\n", encoding="utf-8")
    return world


def run(world: Path) -> tuple[list[dict], list[tuple[int, int, int | None]], float]:
    rooms: list[tuple[int, int, int | None]] = []
    lines: list[dict] = []
    holder: dict = {}
    original = meeting_board.drawn_among

    def watched(tables, left):  # the draw watched from outside: the room and the quotient, nothing changed
        rooms.append((int(holder["board"].interval), len(tables), None if left is None else int(left)))
        return original(tables, left)

    def keep(line: dict) -> None:
        if line.get("event") in ("click", "density", "credit", "lay", "birth", "refused"):
            lines.append(dict(line))

    meeting_board.drawn_among = watched
    began = time.perf_counter()
    try:
        board = Lattice(load_world(world), output=keep)
        holder["board"] = board
        for _ in range(INTERVALS):
            board.step()
    finally:
        meeting_board.drawn_among = original
    return lines, rooms, time.perf_counter() - began


def record_key(line: dict) -> tuple:
    if line["event"] == "credit":
        return ("credit", line.get("family"), line.get("realised"), line.get("kind"), line.get("sense"), json.dumps(line.get("support")), json.dumps(line.get("identity")), json.dumps(line.get("point")), json.dumps(line.get("momentum")))
    return ("birth", line.get("family"), json.dumps(line.get("children")), json.dumps(line.get("senses")), json.dumps(line.get("nodes")), json.dumps(line.get("points")))


def readings(lines: list[dict], rooms: list[tuple[int, int, int | None]]) -> dict:
    per_interval: dict[int, Counter] = {t: Counter() for t in range(1, INTERVALS + 1)}
    for line in lines:
        per_interval[int(line["interval"])][line["event"]] += 1
    rooms_at: dict[int, list[tuple[int, int | None]]] = {t: [] for t in range(1, INTERVALS + 1)}
    for t, room, left in rooms:
        rooms_at[t].append((room, left))
    seen: set[tuple] = set()
    n = d = h = 0
    omega = 1
    table = []
    monotone = True
    last = (0, 0, 0, 1)
    by_interval_lines: dict[int, list[dict]] = {t: [] for t in range(1, INTERVALS + 1)}
    for line in lines:
        if line["event"] in ("credit", "birth"):
            by_interval_lines[int(line["interval"])].append(line)
    for t in range(1, INTERVALS + 1):
        for line in by_interval_lines[t]:
            n += 1
            key = record_key(line)
            if key not in seen:
                seen.add(key)
                d += 1
        for room, _left in rooms_at[t]:
            h += (room - 1).bit_length()
            omega *= room
        if not (n >= last[0] and d >= last[1] and h >= last[2] and omega >= last[3]):
            monotone = False
        last = (n, d, h, omega)
        c = per_interval[t]
        table.append(
            {
                "interval": t,
                "credits": c["credit"],
                "births": c["birth"],
                "lays": c["lay"],
                "refused": c["refused"],
                "draws": len(rooms_at[t]),
                "rooms": [room for room, _l in rooms_at[t]],
                "N_click_records": n,
                "bits_N": n.bit_length(),
                "D_distinct_records": d,
                "bits_D": d.bit_length(),
                "H_bits_written_by_the_draws": h,
                "bits_Omega_minus_1": (omega - 1).bit_length(),
            }
        )
    return {"table": table, "monotone_at_every_interval": monotone, "Omega_final": omega}


def summary(lines: list[dict], rooms: list[tuple[int, int, int | None]], seconds: float) -> dict:
    events = Counter(line["event"] for line in lines)
    births = [line for line in lines if line["event"] == "birth"]
    credits = [line for line in lines if line["event"] == "credit"]
    refused = Counter(line.get("cause") for line in lines if line["event"] == "refused")
    children = Counter(child for line in births for child in line["children"])
    senses = Counter(s for line in births for s in line["senses"])
    room_counts = Counter(room for _t, room, _l in rooms)
    found = {
        "den": DEN,
        "gamma": GAMMA,
        "T": T,
        "shape": SHAPE,
        "intervals": INTERVALS,
        "seconds_integer": int(seconds),
        "events": dict(events),
        "first_birth_interval": births[0]["interval"] if births else None,
        "first_credit_interval": credits[0]["interval"] if credits else None,
        "children_born_by_family": dict(children),
        "children_senses": {str(k): v for k, v in senses.items()},
        "quanta_absorbed_in_credits_sum_count": sum(int(line.get("count") or 0) for line in credits),
        "credit_kinds": dict(Counter(line.get("kind") for line in credits)),
        "credit_beats_none": sum(1 for line in credits if line.get("beat") is None),
        "credit_families": dict(Counter(line.get("family") for line in credits)),
        "refused_by_cause": {str(k): v for k, v in refused.items()},
        "draws": len(rooms),
        "draw_rooms": {str(k): v for k, v in sorted(room_counts.items())},
        "draws_certain_room_1": room_counts.get(1, 0),
        "draws_with_a_choice": sum(v for k, v in room_counts.items() if k > 1),
        "births_excess_sum": sum(int(line.get("excess") or 0) for line in births),
        "births_walls_sum": sum(int(line.get("walls") or 0) for line in births),
        "births_taken_sum": sum(int(line.get("taken") or 0) for line in births),
        "births_exact_take_identity_taken_equals_walls_plus_excess": all(int(line["taken"]) == int(line["walls"]) + int(line["excess"]) for line in births if "taken" in line),
        "births_with_excess_0": sum(1 for line in births if "excess" in line and int(line["excess"]) == 0),
    }
    return found


def run_back(world: Path) -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    env.setdefault("TMPDIR", "/dev/shm/tmp")
    began = time.perf_counter()
    done = subprocess.run(
        [PYTHON, str(ROOT / "tools" / "back_in_time.py"), str(world), "--intervals", str(INTERVALS)],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    out = done.stdout.strip().splitlines()
    verdict = json.loads(out[-1]) if out else {"verdict": "NO OUTPUT", "stderr": done.stderr[-2000:]}
    verdict["seconds_integer"] = int(time.perf_counter() - began)
    verdict["returncode"] = done.returncode
    return verdict


def main() -> None:
    world = write_world()
    lines, rooms, seconds = run(world)
    (OUT / "hole300.clicks.jsonl").write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    found = summary(lines, rooms, seconds)
    read = readings(lines, rooms)
    found["monotone_at_every_interval"] = read["monotone_at_every_interval"]
    found["Omega_final"] = read["Omega_final"]
    found["final"] = read["table"][-1]
    found["every_25"] = [row for row in read["table"] if row["interval"] % EVERY == 0 or row["interval"] == 1]
    found["run_back"] = run_back(world)
    (OUT / "hole_seed_entropy.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
    (OUT / "hole_seed_entropy_table.json").write_text(json.dumps(read["table"]), encoding="utf-8")
    text = []
    text.append(f"hole seed at den {DEN}, Gamma {GAMMA}, T {T}, shape {SHAPE}, {INTERVALS} intervals, {found['seconds_integer']} s forward")
    text.append(f"events {found['events']}; first birth at interval {found['first_birth_interval']}; first credit at {found['first_credit_interval']}")
    text.append(f"children {found['children_born_by_family']} senses {found['children_senses']}; credits by family {found['credit_families']} kinds {found['credit_kinds']} beat None {found['credit_beats_none']}; quanta absorbed {found['quanta_absorbed_in_credits_sum_count']}")
    text.append(f"refused by cause {found['refused_by_cause']}; draws {found['draws']} rooms {found['draw_rooms']} (certain {found['draws_certain_room_1']}, with a choice {found['draws_with_a_choice']})")
    text.append(f"births: taken {found['births_taken_sum']} = walls {found['births_walls_sum']} + excess {found['births_excess_sum']}: identity {found['births_exact_take_identity_taken_equals_walls_plus_excess']}; births with excess 0: {found['births_with_excess_0']}")
    text.append(f"monotone at every interval (N, D, H, Omega): {found['monotone_at_every_interval']}; Omega final {found['Omega_final']}")
    text.append("t | credits | births | lays | refused | draws | N | bits N | D | bits D | H bits | bits(Omega-1)")
    for row in found["every_25"]:
        text.append(f"{row['interval']} | {row['credits']} | {row['births']} | {row['lays']} | {row['refused']} | {row['draws']} | {row['N_click_records']} | {row['bits_N']} | {row['D_distinct_records']} | {row['bits_D']} | {row['H_bits_written_by_the_draws']} | {row['bits_Omega_minus_1']}")
    text.append(f"run back: {found['run_back']}")
    body = "\n".join(text) + "\n"
    (OUT / "hole_seed_entropy.txt").write_text(body, encoding="utf-8")
    sys.stdout.write(body)


if __name__ == "__main__":
    main()
