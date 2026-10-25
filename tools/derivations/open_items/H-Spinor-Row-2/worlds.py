"""sr2: the universe files with the spinor row and the worlds measured (written under worlds/; integers only).

The universe: David's universe_middle.json (den 1,655,909,141, Gamma 1,000, T 36,000, G 16) with one row more, by number:
{"shape": 8, "pair": [506298091, 1655909141]}, the heavy lift's pair (the plane row 2 and the spinor row 6 share the
pair: two rows of the file, the shape deciding how the lines turn together). The big universe (universe_toy.json, the
54-bit den) with the spinor row at its heavy lift's pair, for the births.
"""
import json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'worlds'); os.makedirs(OUT, exist_ok=True)
middle = json.load(open(os.path.join(HERE, 'toy', 'universe_middle.json')))
big = json.load(open(os.path.join(HERE, 'toy', 'universe_toy.json')))
u_mid = copy.deepcopy(middle); u_mid['rows'].append({'shape': 8, 'pair': [506298091, 1655909141]})
u_big = copy.deepcopy(big); u_big['rows'].append({'shape': 8, 'pair': [2458210083751875, 15162856759112389]})
json.dump(u_mid, open(os.path.join(OUT, 'universe_sr2.json'), 'w'), indent=1)
json.dump(u_big, open(os.path.join(OUT, 'universe_sr2_big.json'), 'w'), indent=1)
SPIN_ROW = len(u_mid['rows']) - 1  # the spinor row's index in the file (6)
UP_X = [1, 0, 0, 0, 1, 0, 0, 0]; UP_Y = [1, 0, 0, 0, 0, 1, 0, 0]; UP_Z = [1, 0, 0, 0, 0, 0, 0, 0]; DOWN_Z = [0, 0, 0, 0, 1, 0, 0, 0]


def sg(line, across, along, B0, b, at=(4, 4, 4)):
    return {'line': line, 'at': list(at), 'field': 'sg', 'across': across, 'along': along, 'B0': B0, 'b': b}


def world(name, cube, intervals, seed, control=None):
    w = {'universe': 'universe_sr2.json', 'shape': [cube] * 3, 'intervals': intervals, 'seed': seed}
    if control: w['control'] = control
    json.dump(w, open(os.path.join(OUT, name + '.json'), 'w'))


packet = lambda spin, quanta=218, width=3, at=(4, 4, 4), sense=None: dict({'lay': 'at', 'row': SPIN_ROW, 'centre': list(at), 'width': width, 'quanta': quanta, 'spin': spin}, **({} if sense is None else {'sense': sense}))
sea = {'lay': 'sea', 'row': 0}
# (a) the Zeeman doublet at one place: the 7-cube, a width-2 packet of 40 quanta spin-up along x (both z components populated), a uniform B_z = B0 / Gamma held (A_x = -(y - 3) B0), 150 intervals; the control B0 = 0; the same for a plane (row 2) in the same field
c5 = (2, 2, 2); c7 = (3, 3, 3)
for B0 in (0, 800, 1600):
    world('zeeman_spinor_B%d' % B0, 7, 150, [sea, packet(UP_X, 40, 2, c7)], {'held_potential': [sg(1, 1, 2, B0, 0, c7)]} if B0 else None)
    if B0 in (0, 1600): world('zeeman_plane_B%d' % B0, 7, 150, [sea, {'lay': 'at', 'row': 2, 'centre': list(c7), 'width': 2, 'quanta': 40}], {'held_potential': [sg(1, 1, 2, B0, 0, c7)]} if B0 else None)
# (a') the Zeeman doublet on the 9-cube (no turns there in 60 intervals): the SG packet spin-up along x in a uniform B_z = B0 / Gamma, the two components' crossings at the centre read
for B0 in (1600, 3200):
    world('zeeman9_B%d' % B0, 9, 60, [sea, packet(UP_X)], {'held_potential': [sg(1, 1, 2, B0, 0)]})
world('zeeman9_plane_B3200', 9, 60, [sea, {'lay': 'at', 'row': 2, 'centre': [4, 4, 4], 'width': 3, 'quanta': 218}], {'held_potential': [sg(1, 1, 2, 3200, 0)]})
# (b) Stern-Gerlach: the 9-cube, the neutral spinor packet (218 quanta, width 3, both senses) spin-up along x, 60 intervals
world('sg_control', 9, 60, [sea, packet(UP_X)])
world('sg_uniform', 9, 60, [sea, packet(UP_X)], {'held_potential': [sg(1, 1, 2, 200, 0)]})  # B_z = 200 / Gamma uniform: no gradient
world('sg_grad_z', 9, 60, [sea, packet(UP_X)], {'held_potential': [sg(1, 1, 2, 200, 100)]})  # A_x = -(y - 4)(200 + 100 (z - 4)): B_z with its gradient along z
world('sg_grad_y', 9, 60, [sea, packet(UP_X)], {'held_potential': [sg(2, 0, 1, 200, 100)]})  # A_y = -(x - 4)(200 + 100 (y - 4)): B_z (reversed) with its gradient along y
world('sg_second_axis', 9, 60, [sea, packet(UP_Z)], {'held_potential': [sg(3, 1, 1, 200, 100)]})  # a z-up packet (one region selected) in A_z = -(y - 4)(200 + 100 (y - 4)): B_x with its gradient along y: the x components part along y
world('sg_grad_z_plane', 9, 60, [sea, {'lay': 'at', 'row': 2, 'centre': [4, 4, 4], 'width': 3, 'quanta': 218}], {'held_potential': [sg(1, 1, 2, 200, 100)]})  # the plane in the same gradient (sp2's control)
# (c) the births: the big universe on the 5-cube, David's emergence seed, 120 intervals
wb = {'universe': 'universe_sr2_big.json', 'shape': [5, 5, 5], 'intervals': 300, 'seed': [{'lay': 'sea', 'row': 0}, {'lay': 'hole', 'at': [0, 0, 0]}, {'lay': 'at', 'row': 0, 'centre': [1, 0, 0], 'quanta': 1}]}
json.dump(wb, open(os.path.join(OUT, 'births_big.json'), 'w'))
# (d) the pile: the 7-cube, 30 intervals, lays at the centre of width 2
c7 = (3, 3, 3)
world('pile_one_up', 7, 30, [sea, packet(UP_Z, 40, 2, c7, 1)])
world('pile_two_up', 7, 30, [sea, packet(UP_Z, 40, 2, c7, 1), packet(UP_Z, 40, 2, c7, 1)])
world('pile_up_down', 7, 30, [sea, packet(UP_Z, 40, 2, c7, 1), packet(DOWN_Z, 40, 2, c7, 1)])
world('pile_one_80', 7, 30, [sea, packet(UP_Z, 80, 2, c7, 1)])
# (e) the 48: the 5-cube, 20 intervals, a spinor packet of 40 quanta width 2 spin-up along x in the gradient field
world('cube48_base', 5, 20, [sea, packet(UP_X, 40, 2, c5)], {'held_potential': [sg(1, 1, 2, 200, 100, c5)]})
print('written under', OUT, 'spinor row index', SPIN_ROW)
