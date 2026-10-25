"""The run back through tops, births and clicks: N intervals forward with the state's bytes kept, N back, each state compared bit for bit.
Usage: python runback_test.py <den> <intervals> [link]"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lean_full import Lean
den, n, link = int(sys.argv[1]), int(sys.argv[2]), len(sys.argv) > 3 and sys.argv[3] == 'link'
b = Lean(den, 5, link_birth=link)
def h(): return hashlib.sha256(b.state_bytes() + str(b.interval).encode()).hexdigest()
kept = [h()]
for _ in range(n): b.step(); kept.append(h())
turns = b.counts['turns']; births = b.counts['births']; clicks = b.counts['body_clicks']
ok = 0; first_bad = None
for k in range(n):
    b.step_back()
    if h() == kept[n - 1 - k]: ok += 1
    elif first_bad is None: first_bad = n - 1 - k
print({'intervals': n, 'link': link, 'turns': turns, 'births': births, 'clicks': clicks, 'exact': ok, 'first mismatch at interval': first_bad})
