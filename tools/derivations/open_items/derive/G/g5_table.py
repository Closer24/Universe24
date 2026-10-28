"""G5 (drafter G): the table of the g1 outputs (no engine run): per run the world, ticks, rule, the driven
carries and their exact ties (S1), the impulse's u ties (S2), the tension's live ties (S3), the carried
carries' remainders at 0 (S4, the regulator's turn and the drives, the ratchet's pawl bit left out), the
turned driven gears at fine 0 (S6), the coupled charge SUM c_T Q_T at tick 0 and at the end, the births,
the rewind, and the final state hash's first twelve digits. argv: none; reads g1_*.txt beside it."""
import glob
import os
import re

G = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/derive/G'


def grab(text, pattern, default='-'):
    m = re.search(pattern, text, re.M)
    return m.group(1) if m else default


rows = []
for path in sorted(glob.glob(G + '/g1_*.txt')):
    name = os.path.basename(path)
    if name.startswith('g1_first'):
        continue
    text = open(path, encoding='ascii').read()
    if 'forward done' not in text:
        rows.append((name, 'incomplete'))
        continue
    head = grab(text, r'^(world_\S+), (\d+) ticks')
    ticks = grab(text, r'^world_\S+, (\d+) ticks')
    rule = grab(text, r'ticks, rule (\w+)')
    mirror = grab(text, r'mirror (\w+)')
    urule = grab(text, r'the impulse rounding u at its tie: (\w+)', 'head')
    couplings = [int(x) for x in grab(text, r'couplings \[([^\]]*)\]', '').split(',') if x.strip()]
    q0 = [int(x) for x in grab(text, r'^tick 0: plain charges \[([^\]]*)\]', '').split(',') if x.strip()]
    c0 = sum(c * q for c, q in zip(couplings, q0))
    c1 = grab(text, r'coupled total SUM c_T Q_T: (-?\d+)')
    s1 = grab(text, r'S1 driven carries: (\d+)')
    t1 = grab(text, r'S1 ties: (\d+)')
    t2 = grab(text, r'S2 u ties \(2p = tX mod 2tX\): (\d+)')
    t3 = grab(text, r'S3 tension ties inside 0\.\.Gamma: (\d+)')
    t4a = grab(text, r'S4 turn remainder at 0, even teeth: (\d+)')
    t4b = grab(text, r'S4 drive remainder at 0, even teeth: (\d+)')
    t4c = grab(text, r'S4 drive \(tick\.py\) remainder at 0, even teeth: (\d+)')
    t6 = grab(text, r'S6 turned driven gears at fine 0 \(the mirror misses -P by W\): (\d+)')
    births = grab(text, r'^fittings: (\d+ pairs, \d+ unspringings)')
    rewind = grab(text, r'^the rewind: (\d+ of \d+)')
    final = grab(text, r'final state hash (\w{12})')
    rows.append((name, f'{head} {ticks} rule {rule}/{urule} mirror {mirror} | S1 {t1} of {s1} | S2 {t2} | S3 {t3}'
                       f' | S4 {t4a}+{t4b}+{t4c} | S6 {t6} | coupled charge {c0} -> {c1} | {births}'
                       f' | rewind {rewind} | hash {final}'))
for name, line in rows:
    print(f'{name}: {line}')
