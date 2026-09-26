"""THE REGISTER OF PRIMITIVES (issue #1154, cut 1; the model owner's decisions of
2026-09-26 through the Boss, records 2208 and 2212; the short procedure of
skills/workflow.md, point 5; ALGEBRA.md 9.110 item 7, 9.111 item 7, 9.112 item 1).

The engine holds one register, name to function, read by the central loop alone;
a primitive's identity is its unique English name, the key of the ledger's table
(docs/designs/generic_engine/ENGINE_LEDGER.md section 3); each declares its place
in the interval, what it reads, what it writes and its order among the writers of
one value at one place. The refusals at load, by name: a name registered twice; a
term naming a primitive the register lacks or one not built; two writers of one
value at one place with no order; a call at a place other than the declared one.
Cut 1 binds the names to today's methods and moves no body of code: every shipped
world bit for bit (the digest tests of the suites; the five worlds' comparison of
the gate)."""

from __future__ import annotations

import pytest

from event_universe.core.register import PLACES, Declaration, Register
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.test_emitter import emitter_world

# the seventeen names of the ledger's table (section 3), the identities of the primitives
LEDGER_NAMES = (
    "the pair",
    "the degree",
    "the phase",
    "the signed read",
    "the hold",
    "the source",
    "the clicks",
    "the lifetime",
    "the internal representation",
    "the clicks list",
    "the hand",
    "the self-source",
    "the send",
    "the receive",
    "the wait",
    "the operation",
    "the trace",
)


def noop() -> None:
    return None


def test_a_name_registered_twice_is_refused_by_name():
    """One register, one name to one function (record 2212 (2))."""
    register = Register()
    register.add(
        Declaration("the hold", "(iv)", ("a body's count M_k",), ("the held level",), None, noop)
    )
    with pytest.raises(ValueError, match="'the hold' is registered twice"):
        register.add(Declaration("the hold", "(iv)", (), (), None, noop))
    assert register.names == ("the hold",)
    with pytest.raises(ValueError, match="none of the interval's places"):
        register.add(Declaration("the source", "(vi)", (), (), None, noop))
    assert PLACES == ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")


def test_two_writers_of_one_value_at_one_place_need_a_declared_order():
    """The loop refuses two primitives that write the same value at the same place
    unless their order is declared (record 2212 (3)); distinct orders pass; the
    same value at another place is no conflict."""
    register = Register()
    register.add(Declaration("the receive", "(i)", ("the Link's value",), ("the arrivals",), None, noop))
    register.add(
        Declaration("the internal representation", "(i)", ("n pairs",), ("the arrivals",), None, noop)
    )
    with pytest.raises(
        ValueError, match="all write 'the arrivals' at the place \\(i\\) and declare no order"
    ):
        register.check_writers()
    ordered = Register()
    ordered.add(Declaration("the receive", "(i)", ("the Link's value",), ("the arrivals",), 1, noop))
    ordered.add(
        Declaration("the internal representation", "(i)", ("n pairs",), ("the arrivals",), 2, noop)
    )
    ordered.add(Declaration("the trace", "any", ("every word's integers",), (), None, None))
    ordered.check_writers()
    same_order = Register()
    same_order.add(Declaration("a", "(ii)", (), ("the tally",), 1, noop))
    same_order.add(Declaration("b", "(ii)", (), ("the tally",), 1, noop))
    with pytest.raises(ValueError, match="declare no order between them"):
        same_order.check_writers()
    apart = Register()
    apart.add(Declaration("a", "(i)", (), ("the tally",), None, noop))
    apart.add(Declaration("b", "(ii)", (), ("the tally",), None, noop))
    apart.check_writers()


def test_a_term_naming_an_unknown_or_unbuilt_primitive_is_refused_by_name():
    """A term of the files names a primitive the register holds with a function;
    a name the register lacks and a row of the ledger not built are refused
    naming the file's line and the primitive."""
    register = Register()
    register.add(
        Declaration("the hold", "(iv)", ("a body's count M_k",), ("the held level",), None, noop)
    )
    register.add(
        Declaration("the source", "(i)", ("a record's form",), ("the sourced level",), None, None)
    )
    register.check_terms([("universe.families[0].held", "the hold")])
    with pytest.raises(ValueError, match="names the primitive 'the well', which the register lacks"):
        register.check_terms([("universe.families[0].well", "the well")])
    with pytest.raises(ValueError, match="'the source', a row of the ledger not built yet"):
        register.check_terms([("universe.families[1].sourced", "the source")])
    assert register.built_names() == ("the hold",)


def test_the_loop_calls_a_primitive_at_its_declared_place_alone():
    """A call at a place other than the declared one is refused; the trace's
    place "any" admits every place; an unbuilt row has no function to call."""
    register = Register()
    register.add(Declaration("the hold", "(iv)", (), (), None, noop))
    register.add(Declaration("the trace", "any", (), (), None, noop))
    register.add(Declaration("the source", "(i)", (), (), None, None))
    assert register.at("the hold", "(iv)") is noop
    assert register.at("the trace", "(ii)") is noop
    with pytest.raises(
        ValueError, match="calls the primitive 'the hold' at the place \\(i\\), but it declares \\(iv\\)"
    ):
        register.at("the hold", "(i)")
    with pytest.raises(ValueError, match="'the source' has no function"):
        register.at("the source", "(i)")


def test_the_engine_registers_the_seventeen_and_checks_every_familys_terms():
    """On a shipped test world the engine's register holds exactly the ledger's
    seventeen names in the table's order, the rows built today bound to a
    function, the rows to do without one; every term a family declares names a
    built primitive; the hold and the clicks are called through the register
    (the shipped worlds bit for bit: the suites' digests)."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=20)))
    assert simulation.register.names == LEDGER_NAMES
    built = set(simulation.register.built_names())
    assert built == {
        "the pair",
        "the degree",
        "the phase",
        "the signed read",
        "the hold",
        "the clicks",
        "the self-source",
        "the send",
        "the receive",
        "the wait",
        "the operation",
    }
    for declaration in simulation.register.declarations.values():
        assert declaration.place in PLACES and declaration.section
        assert declaration.name == declaration.name.strip() and declaration.name.startswith("the ")
    terms = simulation.family_terms()
    names = {name for _label, name in terms}
    assert (
        names <= built
        and {"the pair", "the send", "the operation", "the signed read", "the hold"} <= names
    )
    assert all(label.startswith("universe.families[") for label, _name in terms)
    simulation.register.check_terms(terms)
    assert simulation.register.at("the wait", "(i)")() == 1
    for _ in range(20):
        simulation.step()
        assert simulation.books()["balanced"]
