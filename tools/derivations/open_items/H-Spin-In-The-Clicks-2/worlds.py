"""sp2: writes the world files of the two measurement sets into worlds/ (David's universe_middle.json, den 1,655,909,141,
Gamma 1,000, T 36,000, G 16; its row 2 the heavy lift (506,298,091, den), cos omega_0 = 0.3058, g = 0.69).

Set SG (Stern-Gerlach in the clicks): the 9-cube, 60 intervals, David's packet (row 2, width 3, 218 quanta at the
centre [4, 4, 4]) laid at one sense, in a hand-held field of the shape-4 row's odd line A_x:
A_x(y, z) = -(y - 4) (B0 + b (z - 4)), so the curl B_z = B0 + b (z - 4) stands along z with the gradient b along z
(the Stern-Gerlach magnet: the field and its gradient along one axis), B_y = -b (y - 4) its return; held constant.
Controls: the same packet with no field; David's conjugate-pair lay (both senses) with and without the field.
The electric contrast: the shape-4 row's time line A_0 held at a uniform gradient E along z (the potential's
gradient: the two charges should part, the clicks showing the sense as the charge and not as a spin).

Set Q (two quanta at one Node): the 7-cube, 60 intervals, row 2, width 2 (the raised cosine 2, 1: the centre Node
holds 64 / 216 of the packet's share), centre [3, 3, 3]: one lay of 4 quanta (the centre at one unit and above), one
lay of 8, two lays of 4 at one centre (like senses), one lay of 4 at each sense at one centre, two lays of 4 three
Links apart, one lay of 4 on row 2 and one on row 1 at one centre.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'worlds'); os.makedirs(OUT, exist_ok=True)
UNIVERSE = os.path.join('..', 'toy', 'universe_middle.json')

SG_CUBE, SG_INTERVALS, SG_CENTRE, SG_ROW, SG_WIDTH, SG_QUANTA = 9, 60, [4, 4, 4], 2, 3, 218
B0, B_GRAD, E_GRAD = 200, 100, 10
Q_CUBE, Q_INTERVALS, Q_CENTRE, Q_ROW, Q_WIDTH, Q_N = 7, 60, [3, 3, 3], 2, 2, 40  # 40 quanta over the width-2 packet: the centre Node at about 11 units, standing through its beat (4 quanta left the centre at 1.15 units and no close in 60 intervals)


def sg_lay(sense=None, quanta=SG_QUANTA, centre=SG_CENTRE):
    lay = {'lay': 'at', 'row': SG_ROW, 'centre': centre, 'width': SG_WIDTH, 'quanta': quanta}
    if sense is not None: lay['sense'] = sense
    return lay


def magnet(b0=B0, b=B_GRAD):
    # the odd line A_x is line 1 of the shape-4 row; across = y (axis 1), along = z (axis 2)
    return {'held_potential': [{'line': 1, 'field': 'sg', 'at': SG_CENTRE, 'across': 1, 'along': 2, 'B0': b0, 'b': b}]}


def electric(e=E_GRAD):
    return {'held_potential': [{'line': 0, 'field': 'linear', 'at': SG_CENTRE, 'along': 2, 'E': e}]}


def world(shape, intervals, seed, control=None):
    # the sea first (the massless row's drift at every Node, David's world_bodies form): the clicks' take is paid by the light at the Node, refused by name where none stands
    w = {'universe': UNIVERSE, 'shape': [shape] * 3, 'intervals': intervals, 'seed': [{'lay': 'sea', 'row': 0}] + seed}
    if control: w['control'] = control
    return w


WORLDS = {
    # SG set
    'sg_plus_B': world(SG_CUBE, SG_INTERVALS, [sg_lay(1)], magnet()),
    'sg_minus_B': world(SG_CUBE, SG_INTERVALS, [sg_lay(-1)], magnet()),
    'sg_plus_0': world(SG_CUBE, SG_INTERVALS, [sg_lay(1)]),
    'sg_minus_0': world(SG_CUBE, SG_INTERVALS, [sg_lay(-1)]),
    'sg_pair_B': world(SG_CUBE, SG_INTERVALS, [sg_lay(None)], magnet()),
    'sg_pair_0': world(SG_CUBE, SG_INTERVALS, [sg_lay(None)]),
    'sg_plus_uniformB': world(SG_CUBE, SG_INTERVALS, [sg_lay(1)], magnet(B0, 0)),
    'sg_minus_uniformB': world(SG_CUBE, SG_INTERVALS, [sg_lay(-1)], magnet(B0, 0)),
    'e_plus': world(SG_CUBE, SG_INTERVALS, [sg_lay(1)], electric()),
    'e_minus': world(SG_CUBE, SG_INTERVALS, [sg_lay(-1)], electric()),
    # Q set
    'q_one_4': world(Q_CUBE, Q_INTERVALS, [{'lay': 'at', 'row': Q_ROW, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': Q_N, 'sense': 1}]),
    'q_one_8': world(Q_CUBE, Q_INTERVALS, [{'lay': 'at', 'row': Q_ROW, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': 2 * Q_N, 'sense': 1}]),
    'q_two_like': world(Q_CUBE, Q_INTERVALS, [{'lay': 'at', 'row': Q_ROW, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': Q_N, 'sense': 1}] * 2),
    'q_two_opposite': world(Q_CUBE, Q_INTERVALS, [{'lay': 'at', 'row': Q_ROW, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': Q_N, 'sense': 1}, {'lay': 'at', 'row': Q_ROW, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': Q_N, 'sense': -1}]),
    'q_two_apart': world(Q_CUBE, Q_INTERVALS, [{'lay': 'at', 'row': Q_ROW, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': Q_N, 'sense': 1}, {'lay': 'at', 'row': Q_ROW, 'centre': [3, 3, 6], 'width': Q_WIDTH, 'quanta': Q_N, 'sense': 1}]),
    'q_two_rows': world(Q_CUBE, Q_INTERVALS, [{'lay': 'at', 'row': Q_ROW, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': Q_N, 'sense': 1}, {'lay': 'at', 'row': 1, 'centre': Q_CENTRE, 'width': Q_WIDTH, 'quanta': Q_N, 'sense': 1}]),
}

if __name__ == '__main__':
    for name, w in WORLDS.items():
        json.dump(w, open(os.path.join(OUT, name + '.json'), 'w'))
    print('wrote', len(WORLDS), 'worlds to', OUT)
