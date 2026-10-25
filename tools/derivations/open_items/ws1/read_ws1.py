"""ws1's reader of an out.json of run_ws1.py: the swap's counts at the turned Nodes; the board's W of the planes with a gap decomposed
over the run into the step's part SUM (W1 - W0), the swap's part SUM (W2 - W1) (the discard of the step's output at the turned Nodes, whose
own exchange keeps W) and the click's part SUM (W3 - W2) (the births' lays; a credit takes on the gap-0 line alone); the identity
SUM (W2 - W1) = sum_pre - sum_post over the turned sites; W at the marks 0, T/4, T/2, 3T/4, T over the board and per half mask;
every reading an integer. Usage: python read_ws1.py <out.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
d = json.load(open(sys.argv[1]))
print("world", d["world"], "intervals", d["intervals"], "cube", d["cube"], "seconds", d["seconds"])
print("counts", d["counts"])
print("run back", d["run_back"], "census", d["census"], "end_hash", d["end_hash"][:16])
c = d["wcounts"]
print("swap at the turned Nodes: sites (Node x plane with a gap)", c["sites"], "kept", c["kept"], "negated", c["negated"], "changed", c["changed"],
      "| of the kept, W = 0 at", c["kept_zero"], "so W != 0 kept", c["kept"] - c["kept_zero"], "| turned Nodes", c["nodes"], "with the Node's W sum kept", c["node_sum_kept"])
print("at the turned sites: W_pre (held) summed", c["sum_pre"], "W_post (the step's output, discarded) summed", c["sum_post"], "W_after (exchanged) summed", c["sum_after"],
      "| sites where the step left W unchanged", c["post_equal_pre"])
log = d["wlog"]
step = sum(r[2] - r[1] for r in log)
swap = sum(r[3] - r[2] for r in log)
click = sum(r[4] - r[3] for r in log)
print("the board's W of the planes with a gap: at the seed", log[0][1], "at the end", log[-1][4], "the change", log[-1][4] - log[0][1])
print("  decomposed: the step SUM (W1 - W0) =", step, "| the swap SUM (W2 - W1) =", swap, "| the click SUM (W3 - W2) =", click, "| sum", step + swap + click)
print("  identity: SUM (W2 - W1) against sum_pre - sum_post at the turned sites:", swap, "against", c["sum_pre"] - c["sum_post"], "equal" if swap == c["sum_pre"] - c["sum_post"] else "NOT EQUAL")
nz = [r for r in log if r[3] != r[2]]
print("  intervals where the swap's part is not 0:", len(nz), "of", len(log), "| intervals with turns:", sum(1 for r in log if r[5] > 0), "| turns", sum(r[5] for r in log), "births", sum(r[6] for r in log), "credits", sum(r[7] for r in log), "frozen Node-intervals", sum(r[8] for r in log))
# the step's part split: intervals with no turn and no birth against the rest
quiet = [r for r in log if r[5] == 0 and r[6] == 0]
print("  the step's part on intervals with no turn and no birth:", sum(r[2] - r[1] for r in quiet), "over", len(quiet), "intervals")
# per-interval table at marks
n = d["intervals"]
marks = sorted({0, n // 4, n // 2, 3 * n // 4, n})
wr = d["wread"]
print("W at the marks [i, W of the planes with a gap over the board, W of every plane over the board, W per half mask...]:")
for m in marks:
    print("  ", wr[m])
if len(wr[0]) > 3:
    off = [r[0] for r in wr if r[1] != r[3] + r[4]]
    print("  mask sums against the board: intervals where mask A + mask B != board:", len(off), "of", len(wr), "(the tie plane's W where the cube is odd)")
# the largest single-interval steps
big = sorted(log, key=lambda r: -abs(r[2] - r[1]))[:5]
print("the five largest step parts [i, w0 pre, w1 step, w2 swap, w3 click, turned, births, credits, frozen]:")
for r in big:
    print("  ", r, "step", r[2] - r[1], "swap", r[3] - r[2], "click", r[4] - r[3])
bigs = sorted(log, key=lambda r: -abs(r[3] - r[2]))[:5]
print("the five largest swap parts:")
for r in bigs:
    print("  ", r, "step", r[2] - r[1], "swap", r[3] - r[2], "click", r[4] - r[3])
print("the first ten intervals:")
for r in log[:10]:
    print("  ", r, "step", r[2] - r[1], "swap", r[3] - r[2], "click", r[4] - r[3])
