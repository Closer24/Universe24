"""Exact small quantum fixtures; expected outcomes remain in their tests."""

from fractions import Fraction

from event_universe.quantum.event_network import EventNetwork, EventNetworkConfig
from event_universe.quantum.event_rules import LocalInstrument, LocalUnitary
from event_universe.quantum.state import Amplitude


def matrix(rows):
    return tuple(tuple(Amplitude(value, 0) for value in row) for row in rows)


H = LocalUnitary(matrix(((1, 1), (1, -1))))


Z = LocalUnitary(matrix(((1, 0), (0, -1))))


CX = LocalUnitary(matrix(((1, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0))))


CZ = LocalUnitary(matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, -1))))


R = LocalUnitary(matrix(((5, 0, 0, 0), (0, 3, -4, 0), (0, 4, 3, 0), (0, 0, 0, 5))))


RI = LocalUnitary(matrix(((5, 0, 0, 0), (0, 3, 4, 0), (0, -4, 3, 0), (0, 0, 0, 5))))


POSITION = LocalInstrument((matrix(((1, 0), (0, 0))), matrix(((0, 0), (0, 1)))))


DAMPING = LocalInstrument((matrix(((5, 0), (0, 3))), matrix(((0, 4), (0, 0)))))


GRID = tuple((x, y, 0) for y in range(4) for x in range(4))


def network(occupied=(), **budgets):
    return EventNetwork(EventNetworkConfig(GRID, occupied, **budgets))


def probability(reply, outcome=1):
    return Fraction(reply.weights[outcome], sum(reply.weights))


def choose(g, record, register_index, instrument, outcome):
    decision = g.prepare(record, register_index, instrument)
    assert decision.weights[outcome] > 0
    ticket = sum(decision.weights[:outcome])
    return g.commit(decision, ticket)


def fingerprint(g):
    return (g.tick, g.heads, g.events, g.records, g.successful_queries, g.host_evaluated_nodes)
