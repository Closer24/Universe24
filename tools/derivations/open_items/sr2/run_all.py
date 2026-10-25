"""sr2: the driver: every measurement run in order through the flagged copy, each a subprocess, its output under outputs/ and its log under logs/ (no shell loop; one script).
Usage: python run_all.py [set]   (set: sg, zeeman, pile, births, reach, cube48; default all)
"""
import os, sys, subprocess, time, json

HERE = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
os.makedirs(os.path.join(HERE, 'outputs'), exist_ok=True); os.makedirs(os.path.join(HERE, 'logs'), exist_ok=True)
W = lambda name: os.path.join(HERE, 'worlds', name + '.json')
O = lambda name: os.path.join(HERE, 'outputs', name + '.json')
RUN = os.path.join(HERE, 'sr2_run.py')
SETS = {
    'sg': [('sg_control', [PY, RUN, W('sg_control'), O('sg_control'), 'back', '10', 'axis', '2', 'comp', '2']),
           ('sg_uniform', [PY, RUN, W('sg_uniform'), O('sg_uniform'), 'back', '10', 'axis', '2', 'comp', '2']),
           ('sg_grad_z', [PY, RUN, W('sg_grad_z'), O('sg_grad_z'), 'back', '10', 'axis', '2', 'comp', '2']),
           ('sg_grad_y', [PY, RUN, W('sg_grad_y'), O('sg_grad_y'), 'back', '10', 'axis', '1', 'comp', '2']),
           ('sg_second_axis', [PY, RUN, W('sg_second_axis'), O('sg_second_axis'), 'back', '10', 'axis', '1', 'comp', '0']),
           ('sg_grad_z_plane', [PY, RUN, W('sg_grad_z_plane'), O('sg_grad_z_plane'), 'back', '10', 'axis', '2', 'comp', '2'])],
    'zeeman': [(n, [PY, RUN, W(n), O(n), 'back', '5']) for n in ('zeeman_spinor_B0', 'zeeman_spinor_B800', 'zeeman_spinor_B1600', 'zeeman_plane_B0', 'zeeman_plane_B1600')],
    'zeeman9': [(n, [PY, RUN, W(n), O(n), 'back', '10']) for n in ('zeeman9_B1600', 'zeeman9_B3200', 'zeeman9_plane_B3200')],
    'pile': [(n, [PY, RUN, W(n), O(n), 'back', '5']) for n in ('pile_one_up', 'pile_two_up', 'pile_up_down', 'pile_one_80')],
    'births': [('births_big', [PY, RUN, W('births_big'), O('births_big'), 'back', '10'])],
    'reach': [('reach', [PY, os.path.join(HERE, 'sr2_reach.py'), W('sg_grad_z'), '3', '4,4,4'])],
    'cube48': [('cube48', [PY, os.path.join(HERE, 'sr2_cube48.py'), W('cube48_base'), O('cube48'), '20'])],
}


def main():
    which = sys.argv[1:] or ['sg', 'zeeman', 'pile', 'births', 'reach', 'cube48']
    for s in which:
        for name, cmd in SETS[s]:
            t0 = time.monotonic_ns()
            with open(os.path.join(HERE, 'logs', name + '.log'), 'w') as log:
                code = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=HERE).returncode
            print(json.dumps({'run': name, 'exit': code, 'seconds': (time.monotonic_ns() - t0) // 10 ** 9}), flush=True)


if __name__ == '__main__':
    main()
