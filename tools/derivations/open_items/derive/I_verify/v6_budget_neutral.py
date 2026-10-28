"""I_verify v6: are i4's budget wrappers (carry, turnover, click, standard_rate) neutral to the dynamics?
Runs i4_head.py's budget for N ticks (it ticks N + 1 times), snapshots the clock, then restores the head's
carry/turnover/click/standard_rate (keeping the variant's fix patches), ticks a fresh clock N + 1 times, and compares
every gear, the slack, the dial, the clicks, the tick count and the log length bit for bit.
Run: venv314/bin/python -I v6_budget_neutral.py <world> <ticks> <variant>"""
import io
import contextlib
import sys
S = '/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad'
world, ticks, variant = sys.argv[1], sys.argv[2], sys.argv[3]
sys.argv = ['i4_head.py', world, ticks, variant]
sys.path.insert(0, S + '/derive/I_verify/run')
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import i4_head as M
with_budget = M.snapshot(M.clock)
M.T.Tick.carry, M.T.Tick.turnover, M.T.Tick.click = M.orig_carry, M.orig_turnover, M.orig_click
M.T.Tick.standard_rate = M.orig_standard_rate if not M.FIX1 else M.standard_rate   # fix1 needs e recorded
clk = M.new_clock()
for _ in range(int(ticks) + 1):
    clk.tick()
plain = M.snapshot(clk)
print(f"V6 {world} {variant}: {int(ticks) + 1} ticks with the budget wrappers against without: bit for bit equal: "
      f"{M.same(with_budget, plain)}; turns {M.clock.counts['turns']} against {clk.counts['turns']}")
