"""Verifier's probe (integers only): on an A1 board every Node-clock holds the same hand z, so the Meshes' wind of a
coupled hand is SUM over the six Spokes of R (|z|^2 - z . U_j z), U_j the Mesh's turn (meshes.through_mesh: the
offset pair over the standard length, then the odd gear's and the flow's tangent triple, each part rounded once);
the +a and -a Spokes turn by opposite angles. The exact turn gives 2 |z|^2 (1 - cos theta) >= 0 per axis; the
rounding can give less. Counts the draws where the per-axis sum is below 0 (the draft's 'G >= 0 on the A1 course'
needs it never below 0). Also the offset pair at a count n != 0 (the standard circle's (cos, sin)).
Usage: python -I transport_rounding.py ENGINE_ROOT DRAWS SEED"""
import sys, random, json
root, draws, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path[:0] = [root + "/src", root]
from tests.laws import world_of  # noqa: E402
from event_universe.clock import Clock  # noqa: E402
from event_universe.meshes import Mesh, through_mesh  # noqa: E402
from event_universe.readings import standard_angle  # noqa: E402
calibre, piece = world_of("world_bang.json")
piece = json.loads(json.dumps(piece)); piece["seed"][0]["quanta"] = 1
clock = Clock(calibre, piece)
L, GAM = clock.standard_length, clock.full_rate
rng = random.Random(seed)
neg = 0; worst = (0, None)
neg_n = 0
for i in range(draws):
    amp = rng.choice([3, 30, 1000, 10**5, 10**7, 10**9])
    z = [rng.randint(-amp, amp), rng.randint(-amp, amp)]
    A = rng.choice([0, 1, 2, 3, 7, 50, 300]) * rng.choice([1, -1])
    m = rng.choice([0, 0, 1, 5, 100, 4000]) * rng.choice([1, -1])
    count = rng.choice([0, 0, 0, 1, 2, 5, 40])
    if count:
        c1, s1 = standard_angle(clock, count); c2, s2 = standard_angle(clock, -count)
    else:
        c1, s1, c2, s2 = L, 0, L, 0
    tot = 0
    for (c, s, sign) in ((c1, s1, 1), (c2, s2, -1)):
        at = Mesh(1, 1, c, s, sign * 2 * A, (GAM * GAM, sign * m))
        u = through_mesh(list(z), at, L, GAM)
        tot += z[0] * z[0] + z[1] * z[1] - (z[0] * int(u[0]) + z[1] * int(u[1]))
    if tot < 0:
        neg += 1
        neg_n += count != 0
        if tot < worst[0]:
            worst = (tot, (z, A, m, count))
print(f"{draws} draws: the per-axis wind 2|z|^2 - z.U+z - z.U-z below 0 in {neg} (of them with an offset count: {neg_n});"
      f" the most negative {worst}")
