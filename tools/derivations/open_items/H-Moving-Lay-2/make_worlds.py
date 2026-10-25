"""mv2's worlds for the moving lay, written here so that every integer in them is on record (the universe David's universe_middle.json, den 1655909141;
the row index 2 the heavy lift [506298091, den], num/den 0.3057, David's bodies' row; the row index 1 the light lift [1655880909, den]; the row index 0 light).
The wave number h_a = den sin(k_a / 2) per axis: h = den div 2 is k = pi / 3 exactly; h = isqrt(den^2 div 2) is k = pi / 2 to the unit; h = den div 4 is
k = 2 asin(1 / 4); h = den is the band's edge k = pi."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
U = "../toy/universe_middle.json"
den = 1655909141
H_PI3 = den // 2
H_PI2 = math.isqrt(den * den // 2)
H_Q = den // 4
H_PI = den
SEA = {"lay": "sea", "row": 0}


def world(name, shape, intervals, seed, **extra):
    doc = {"universe": U, "shape": [shape] * 3, "intervals": intervals, "seed": seed}
    doc.update(extra)
    json.dump(doc, open(os.path.join(HERE, 'worlds', name + '.json'), 'w'))


def at(row, centre, quanta, h=None, width=2):
    lay = {"lay": "at", "row": row, "centre": list(centre), "width": width, "quanta": quanta}
    if h is not None: lay["wave"] = list(h)
    return lay


os.makedirs(os.path.join(HERE, 'worlds'), exist_ok=True)
# (c) the control: the same packet with no wave key (David's lay, bit for bit) and with wave [0, 0, 0]
world('c_rest_david', 9, 20, [SEA, at(2, (4, 4, 4), 100)])
world('c_rest_wave0', 9, 20, [SEA, at(2, (4, 4, 4), 100, (0, 0, 0))])
# (a) the electron packet moving along +x: the law's run (the sea laid, the volume written by the law)
world('a_e_pi3', 9, 60, [SEA, at(2, (1, 4, 4), 100, (H_PI3, 0, 0))])
world('a_e_pi2', 9, 60, [SEA, at(2, (1, 4, 4), 100, (H_PI2, 0, 0))])
world('a_e_q', 9, 60, [SEA, at(2, (1, 4, 4), 100, (H_Q, 0, 0))])
world('a_e_edge', 9, 60, [SEA, at(2, (4, 4, 4), 100, (H_PI, 0, 0))])
world('a_e_pi3_w3', 9, 60, [SEA, at(2, (1, 4, 4), 100, (H_PI3, 0, 0), width=3)])
# the same packets on the held vacuum (the toy's `control` key, no lay of the law: the metric's row held, the paces the vacuum's; the kinematics alone)
HELD = {"well": {"at": [4, 4, 4], "levels": 0, "radius": 1, "held": True}}
world('k_e_pi3_held', 9, 60, [at(2, (1, 4, 4), 100, (H_PI3, 0, 0))], control=HELD)
world('k_e_pi2_held', 9, 60, [at(2, (1, 4, 4), 100, (H_PI2, 0, 0))], control=HELD)
world('k_e_q_held', 9, 60, [at(2, (1, 4, 4), 100, (H_Q, 0, 0))], control=HELD)
world('k_e_pi3_w3_held', 9, 60, [at(2, (1, 4, 4), 100, (H_PI3, 0, 0), width=3)], control=HELD)
world('k_e_edge_held', 9, 60, [at(2, (4, 4, 4), 100, (H_PI, 0, 0))], control=HELD)
# the light lift (row 1) moving: nearly light's band
world('k_l1_pi3_held', 9, 20, [at(1, (1, 4, 4), 100, (H_PI3, 0, 0))], control=HELD)
# (b) light with a direction: the massless row (row 0) with a wave number, on the held vacuum (the kinematics) and over the sea (the law's run, the clicks)
world('k_light_pi2_held', 9, 20, [at(0, (1, 4, 4), 20, (H_PI2, 0, 0))], control=HELD)
world('k_light_pi3_held', 9, 20, [at(0, (1, 4, 4), 20, (H_PI3, 0, 0))], control=HELD)
world('b_light_pi2', 9, 30, [SEA, at(0, (1, 4, 4), 20, (H_PI2, 0, 0))])
# (d) the collision: two electron packets 4 Links apart laid toward each other (100 against 50 quanta so that the total momentum is not 0 by symmetry), the law's run and the held vacuum
world('d_collide', 9, 60, [SEA, at(2, (2, 4, 4), 100, (H_PI2, 0, 0)), at(2, (6, 4, 4), 50, (-H_PI2, 0, 0))])
world('d_collide_held', 9, 60, [at(2, (2, 4, 4), 100, (H_PI2, 0, 0)), at(2, (6, 4, 4), 50, (-H_PI2, 0, 0))], control=HELD)
world('d_collide_equal', 9, 60, [SEA, at(2, (2, 4, 4), 100, (H_PI2, 0, 0)), at(2, (6, 4, 4), 100, (-H_PI2, 0, 0))])
# the refusal by name: a wave number beyond the band's edge
world('r_beyond_edge', 5, 1, [SEA, at(2, (2, 2, 2), 10, (den + 1, 0, 0))])
# the 48: the 5-cube seed for the images (the sea with the moving packet off the centre)
world('s48_e_pi3', 5, 6, [SEA, at(2, (1, 2, 3), 60, (H_PI3, 0, 0))])
world('s48_e_oblique', 5, 6, [SEA, at(2, (1, 2, 3), 60, (H_PI3, -H_Q, 0))])
print('h values:', {'pi/3': H_PI3, 'pi/2': H_PI2, '2 asin(1/4)': H_Q, 'pi': H_PI})
print(sorted(os.listdir(os.path.join(HERE, 'worlds'))))
