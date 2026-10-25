"""em2's probe of W-S1's algebra on the engine (section 3 of the report): the interval's writes are wrapped so that at every interval, at every Node, the engine's emission numerator over W_div is read beside the EXACT change of the planes' Wronskian over the interval (W after the divisions less W at the start, the engine's own w_after and w_end), with the carrier's term (W_in - W_out) W_start over W_out beside it; integers only. Printed: per record the count of Node-intervals, the max |exact change|, the max |engine's read + exact change| (the residual, 0 where the algebra is exact), the residual's bound by the remainders (2 per line: the kick's rounding), the max |cumulative exact change| per Node against T div 2 and against T, the board's total change per interval (max abs), the count of Node-intervals where |exact change| >= T div 2, the laid levels under the letter (the engine's count). Usage: python probe_emission.py <world.json> <intervals> [flag]"""
import json
import os
import sys

sys.set_int_max_str_digits(0)
import numpy as np

from event_universe import interval as itv
from event_universe.core.rule3 import quotient
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import zeros

universe, world = load_world(sys.argv[1])
n_int = int(sys.argv[2])
world["intervals"] = n_int
node = Node(universe, world)
T = node.T
stats = {
    "node_intervals": 0, "max_abs_exact": 0, "max_abs_residual": 0, "residual_nonzero": 0,
    "max_abs_cumulative": 0, "max_abs_board_total": 0, "nodes_intervals_change_ge_half_T": 0,
    "max_abs_carrier_term": 0, "max_abs_engine_read": 0, "max_abs_W_start": 0,
}
cumulative = zeros(node.shape)
series = []  # per interval: (i, sum |exact|, board total, max |W_start|)
orig_writes = itv.Interval.writes


def probed_writes(self):
    exact = self.w_after - self.w_end  # the planes' Wronskian after the step less at the start, exact integers
    read = quotient(self.emission, self.w_div)  # the engine's numerator (W-S1 as built), floor
    w_in = self.mean_wall()  # forward: the pre carrier's mean wall... (the rows still hold the pre carrier here? no: set_rows comes after; carrier line is the pre one)
    w_out = self.w_div
    carrier_term = quotient((w_in - w_out) * self.w_end, w_out)
    residual = read + exact - carrier_term
    cumulative[...] = cumulative + exact
    ex = [abs(int(x)) for x in exact.reshape(-1)]
    stats["node_intervals"] += len(ex)
    stats["max_abs_exact"] = max(stats["max_abs_exact"], max(ex))
    stats["max_abs_residual"] = max(stats["max_abs_residual"], max(abs(int(x)) for x in residual.reshape(-1)))
    stats["residual_nonzero"] += sum(1 for x in residual.reshape(-1) if int(x) != 0)
    stats["max_abs_cumulative"] = max(stats["max_abs_cumulative"], max(abs(int(x)) for x in cumulative.reshape(-1)))
    stats["max_abs_board_total"] = max(stats["max_abs_board_total"], abs(int(sum(int(x) for x in exact.reshape(-1)))))
    stats["nodes_intervals_change_ge_half_T"] += sum(1 for x in ex if x >= T // 2)
    stats["max_abs_carrier_term"] = max(stats["max_abs_carrier_term"], max(abs(int(x)) for x in carrier_term.reshape(-1)))
    stats["max_abs_engine_read"] = max(stats["max_abs_engine_read"], max(abs(int(x)) for x in read.reshape(-1)))
    stats["max_abs_W_start"] = max(stats["max_abs_W_start"], max(abs(int(x)) for x in self.w_end.reshape(-1)))
    series.append((self.node.interval, sum(ex), int(sum(int(x) for x in exact.reshape(-1))), max(abs(int(x)) for x in self.w_end.reshape(-1))))
    orig_writes(self)


itv.Interval.writes = probed_writes
for _ in range(n_int):
    node.step()
stats["T"] = T
stats["T_half"] = T // 2
stats["drift"] = node.drift
stats["laid (engine count)"] = node.counts["laid"]
stats["laid_nodes"] = node.counts["laid_nodes"]
stats["births"] = node.counts["births"]
stats["body_clicks"] = node.counts["body_clicks"]
stats["cumulative over T_half (nodes)"] = sum(1 for x in cumulative.reshape(-1) if abs(int(x)) >= T // 2)
stats["cumulative over T (nodes)"] = sum(1 for x in cumulative.reshape(-1) if abs(int(x)) >= T)
stats["census (integers, bits)"] = list(node.census())
stats["max transient bits"] = node.max_transient
print(json.dumps(stats))
step = max(1, len(series) // 12)
print(json.dumps({"series (i, sum|exact|, board total, max|W_start|) every " + str(step): series[::step]}))
