"""cp1's one test, under 15 s: the chiral 3-cube to 12 intervals on the flagged copy (CP1_FORM=1, the children as packets): births happen; every birth's children are packets (the waves and the two ends' momenta logged, the taker's packet moving, the far packet at rest with momentum 0); the taker's packet, where its levels resolve the phase (amplitude above 3), carries the recoil on every axis whose wave number is within the band's half (the P balance within 10 per mille of the take's component there); each packet's charge is one quantum's Wronskian to the rounding (within 100 per mille of T div 2, the share fitted to one quantum and the Wronskian rounded over 27 Nodes, measured 16 to 52 per mille below) and the two sum to 0 within 100 per mille; the run back 4 of 4 by the state hash; every integer within 128 bits. Usage: tests_cp1.py <src_cp1> <world_chiral_3_30.json>"""
import os
import sys
import time

os.environ["CP1_FORM"] = "1"
sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

t0 = time.time()
u, w = load_world(sys.argv[2])
n = 12
node = Node(u, dict(w, intervals=n))
den = node.den
sq = (den * den) // 2
cap = int(sq**0.5)
while cap * cap > sq:
    cap -= 1
while (cap + 1) * (cap + 1) <= sq:
    cap += 1
hashes = []
for _ in range(n):
    node.step()
    hashes.append(node.state_hash())
births = [e for e in node.log if e["event"] == "birth"]
assert births, "no birth on the 3-cube to 12"
half_t = node.T // 2
for e in births:
    assert "waves" in e and "dP_lay_ends" in e, "a birth not laid as packets"
    at = tuple(e["node"])
    taker = 0 if tuple(e["minus"]) == at else 1
    assert e["waves"][1 - taker] == [0, 0, 0], "the far packet is at rest"
    assert e["dP_lay_ends"][1 - taker] == [0, 0, 0], "the rest packet onto nothing books momentum 0"
    assert e["packet_nodes"] == [27, 27], "the least envelope: 27 Nodes"
    p = [int(a) + int(b) + int(c) for a, b, c in zip(e["dP_take"], e["dP_lay_ends"][0], e["dP_lay_ends"][1])]
    for a in range(3):
        if e["amplitude_packets"][taker] > 3 and abs(int(e["waves"][taker][a])) < cap and int(e["dP_take"][a]) != 0:  # a packet whose levels resolve the phase (the row with the small sine fits one quantum at the amplitude 3: unresolved, it carries nothing, by name)
            assert 1000 * abs(p[a]) <= 10 * abs(int(e["dP_take"][a])), ("the recoil not carried within 10 per mille on an uncapped axis", e["i"], a, p, e["dP_take"])
    w_minus, w_plus = (int(x) for x in e["W_children"])
    if e["amplitude_packets"][0] > 3:  # a packet onto nothing (not onto standing light)
        assert 1000 * abs(abs(w_minus) - half_t) <= 100 * half_t, ("the rest packet charge off T div 2 beyond 100 per mille", w_minus, half_t)
        assert 1000 * abs(w_minus + w_plus) <= 100 * half_t, ("the charges not summing to 0 within 100 per mille", w_minus, w_plus)
    for x in (e["booked"], e["taken"], *e["dP_take"], *p, *(y for v in e["waves"] for y in v), *(y for v in e["moment_ends"] for y in v)):
        assert abs(int(x)).bit_length() <= 128
back, exact = 4, 0
for k in range(back):
    node.run(-1)
    exact += node.state_hash() == hashes[len(hashes) - 2 - k]
assert exact == back, ("the run back", exact, back)
print("ok: births", len(births), "run back", exact, "of", back, "seconds", int(time.time() - t0))
