"""ca1's FLAGGED COPY of the engine's src under /dev/shm/tmp/ca1/src_ca1 (never the worktree's src), written by exact text replacements, each named; every replacement must match once or the script refuses. The flag: the environment variable CA1_ODD_TAKE; empty, the copy is the head's path bit for bit.
The form under the flag (the derivation, DERIVATION.md section 3): the take's lay on the odd part of the taken line's record alone, now += t s and before -= t s (the even part now + before fixed), so that X T X = T(-1) as for Rule3; the fall read exactly from the board (the share before and after the lay, as walls_of reads the children's walls), the least s in [1, dist] by a scan; the take's momentum booked on both slots. The undo and the lay-back are the same lay act with the count's sign (CR-S1), restoring both slots."""
import os, shutil, sys
SRC = sys.argv[1]
DST = '/dev/shm/tmp/ca1/src_ca1'
if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
R = {
 'event_universe/take.py': [
  ("from event_universe.rows import PLANE, Line, Row\n",
   "from event_universe.rows import PLANE, Line, Row\nimport os\n\nCA1_ODD = bool(os.environ.get('CA1_ODD_TAKE', ''))  # ca1's flag: the take laid on the odd part of the record (now - before) alone\n"),
  ("        levels = tuple(levels if j == PLANE * line else 0 for j in range(PLANE * len(lines)))\n",
   "        levels = tuple(levels if j == PLANE * line else (-levels if (CA1_ODD and j == PLANE * line + 1) else 0) for j in range(PLANE * len(lines)))  # ca1: the odd lay, before -= the count\n"),
  ("    def fall(s: int) -> int:\n        moved = now + t * s\n",
   "    def fall(s: int) -> int:\n        if CA1_ODD:  # ca1: the fall read from the board exactly, the share before and after the odd lay (as walls_of reads the walls)\n            rec_ = node.records().index(row)\n            stood = int(sum(int(v) for v in node.share(row.lines, r).reshape(-1)))\n            lay(node, rec_, at, t * s, line=k)\n            after = int(sum(int(v) for v in node.share(row.lines, r).reshape(-1)))\n            lay(node, rec_, at, t * s, -1, line=k)\n            return stood - after\n        moved = now + t * s\n"),
  ("    full = fall(dist := abs(now - before))\n",
   "    full = fall(dist := abs(now - before)) if not CA1_ODD else fall(max(1, half(dist := abs(now - before))))  # ca1: the odd lay's full move is the exchange X itself (the form even, the fall 0); the guard reads the fall at the half move, the odd fall's peak\n"),
  ("    for s in rule3.least_root(-w * x, -((w + w) * now + pull) * t * x, walls * weight, dist):\n",
   "    for s in ([] if CA1_ODD else rule3.least_root(-w * x, -((w + w) * now + pull) * t * x, walls * weight, dist)):  # ca1: under the flag the least s by the scan below\n"),
  ("    node.last_dp = momentum_of(node, z.now, z.before, at, d_now=toward * levels, num=row.pair[0])\n",
   "    node.last_dp = momentum_of(node, z.now, z.before, at, d_now=toward * levels, d_before=(-toward * levels if CA1_ODD else 0), num=row.pair[0])  # ca1: both slots' momentum\n"),
 ],
}
for rel, reps in R.items():
    path = os.path.join(DST, rel)
    text = open(path).read()
    for old, new in reps:
        n = text.count(old)
        if n != 1:
            sys.exit(f'REFUSED: {rel}: the text occurs {n} times: {old[:60]!r}')
        text = text.replace(old, new)
    open(path, 'w').write(text)
    print('written', path, len(reps), 'replacements')
