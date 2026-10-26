"""rl1 (H-Rule3-Link-Record-1): the Link coupling's symmetry by the integers on the flagged copy (PYTHONPATH the copy; RL1_FORM read by the copy's node.py, the forms called here by name). The head's reach R_ij = 2 num p_i^2 Q_ij is not symmetric where the paces differ but p_j^2 R_ij = p_i^2 R_ji at every Link (D M symmetric, D = diag(1 / p_i^2): the law's weighted conserved form, ALGEBRA.md #the-conserved-form); every symmetric form (sum, geo, link) has R_ij = R_ji at every Link and loses the weighted symmetry at every Link whose paces differ (no symmetric form keeps the law's weight: f symmetric and f / p_i^2 symmetric forces p_i = p_j or f = 0). Under 15 s."""
import os
import sys

import numpy as np

sys.path.insert(0, os.environ.get("RL1_SRC", "/dev/shm/tmp/rl1/src"))
from event_universe.core import rule3  # noqa: E402
from event_universe.core.ports import PORTS, across  # noqa: E402

NUM, DEN, GAMMA, G = 999, 1000, 1000, 16


def board(seed):
    rng = np.random.default_rng(seed)
    pace = np.array([int(x) for x in rng.integers(1, GAMMA + 1, 27)], dtype=object).reshape(3, 3, 3)
    clock = pace  # the clock enters the mass alone, no Link
    factors = []
    for port in range(PORTS):
        if port % 2 == 0:
            q = np.array([int(x) for x in rng.integers(0, G * G + 1, 27)], dtype=object).reshape(3, 3, 3)
            factors.append(q)
        else:
            factors.append(across(factors[-1], port))  # Q_ij read the same from both ends: the - Port's factor is the + Port's at the far end
    return pace, clock, tuple(factors)


def reaches(form, pace, clock, factors):
    others = tuple(across(pace, port) for port in range(PORTS)) if form else None
    if form == "link":
        others = tuple((p + o) // 2 for p, o in zip((pace,) * PORTS, others))  # a Link pace symmetric in the ends stands in for the table
    return rule3.rule_integers(NUM, DEN, GAMMA, clock, pace, factors, G, others, form).reaches


def far(reach, port):
    return across(reach[port ^ 1], port)  # R_ji: the neighbour's reach on the Link back


def test_head_is_weighted_symmetric_and_not_plain():
    pace, clock, factors = board(1)
    r = reaches("", pace, clock, factors)
    plain = 0
    for port in range(PORTS):
        pj = across(pace, port)
        assert np.all(pj * pj * r[port] == pace * pace * far(r, port)), "D M symmetric (the law's weighted form)"
        plain += int(np.sum(r[port] != far(r, port)))
    assert plain > 0, "M itself is not symmetric where the paces differ"
    assert np.all(r[0] == 2 * NUM * pace * pace * factors[0]), "the head's reach bit for bit"


def test_every_symmetric_form_is_plain_symmetric_and_loses_the_weight():
    pace, clock, factors = board(1)
    for form in ("sum", "geo", "link"):
        r = reaches(form, pace, clock, factors)
        lost = 0
        for port in range(PORTS):
            assert np.all(r[port] == far(r, port)), (form, "R_ij = R_ji at every Link")
            pj = across(pace, port)
            lost += int(np.sum((pj * pj * r[port] != pace * pace * far(r, port)) & (pj != pace) & (factors[port] != 0)))
        assert lost > 0, (form, "the weighted symmetry is lost where the paces differ")


def test_uniform_paces_give_the_head_for_every_form():
    pace = np.full((3, 3, 3), 700, dtype=object)
    _, _, factors = board(2)
    head = reaches("", pace, pace, factors)
    for form in ("sum", "geo", "link"):
        assert all(np.all(a == b) for a, b in zip(reaches(form, pace, pace, factors), head)), form


def test_the_horizon_reads_alike_under_every_form():
    """At p = 1 on both ends every form reads 2 num Q_ij; across a Link with a frozen end Q_ij = 0 and every form reads 0."""
    pace = np.full((3, 3, 3), 1, dtype=object)
    pace[0, 0, 0] = 0
    _, _, factors = board(3)
    factors = tuple(np.where((pace == 0) | (across(pace, port) == 0), 0, q) for port, q in enumerate(factors))
    head = reaches("", pace, pace, factors)
    for form in ("sum", "geo", "link"):
        assert all(np.all(a == b) for a, b in zip(reaches(form, pace, pace, factors), head)), form
    assert np.all(head[0] == 2 * NUM * factors[0] * (pace != 0))
