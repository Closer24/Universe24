"""THE REGISTER OF PRIMITIVES, FOUND BY THEIR FOLDERS (issue #1154, cuts 1 and 2; the
model owner's decisions of 2026-09-26 through the Boss, records 2208, 2212 and 2221; the
short procedure of skills/workflow.md, point 5; ALGEBRA.md 9.110 item 7, 9.111 item 7,
9.112 item 1).

The engine holds one register, name to function, read by the central loop alone; a
primitive's identity is its unique English name, the key of the ledger's table
(docs/designs/generic_engine/ENGINE_LEDGER.md section 3); every primitive is one folder
under src/event_universe/features/<name>/ declaring its name, place (a code of 9.91 (8)),
word (9.111 item 7), reads, writes and order, and binding its function; the register
discovers the folders, so adding a feature touches no shared file. The refusals at load,
by name: a folder without a declaration or with a name not its own; a name registered
twice; a term naming a primitive the register lacks or one not built; two writers of one
value at one place with no order; a call at a place other than the declared one. Cut 2
binds the names to today's methods and moves no body of code: every shipped world bit for
bit (the digest tests of the suites; the five worlds' comparison of the gate)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from event_universe.core.register import PLACES, WORDS, Declaration, Register, discover, folder_of
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.test_emitter import emitter_world

# the twenty-three of the ledger's table and the mathematician's lines of record 2221 (the
# giving at (ii); the feed, the induction, the spin's step, the hop and the recoil's
# accumulator at (v)), in the folders' order (the register's)
FOLDER_NAMES = (
    "the clicks",
    "the clicks list",
    "the degree",
    "the feed",
    "the giving",
    "the hand",
    "the hold",
    "the hop",
    "the induction",
    "the internal representation",
    "the lifetime",
    "the operation",
    "the pair",
    "the phase",
    "the receive",
    "the recoil's accumulator",
    "the self-source",
    "the send",
    "the signed read",
    "the source",
    "the spin's step",
    "the trace",
    "the wait",
)
BUILT = {
    "the pair",
    "the degree",
    "the phase",
    "the signed read",
    "the hold",
    "the clicks",
    "the giving",
    "the self-source",
    "the send",
    "the receive",
    "the wait",
    "the operation",
    "the spin's step",
    "the hop",
}


def noop() -> None:
    return None


def test_a_name_registered_twice_or_an_unknown_place_or_word_is_refused_by_name():
    """One register, one name to one function (record 2212 (2)); a place is one of
    9.91 (8)'s five or "any"; a word one of 9.111 item 7's three or "any"."""
    register = Register()
    register.add(
        Declaration(
            "the hold",
            "(iv)",
            "the right side",
            ("the body's count M_k",),
            ("the held level",),
            None,
            "",
            noop,
        )
    )
    with pytest.raises(ValueError, match="'the hold' is registered twice"):
        register.add(Declaration("the hold", "(iv)", "the right side", (), (), None, "", noop))
    assert register.names == ("the hold",)
    with pytest.raises(ValueError, match="none of the interval's places"):
        register.add(Declaration("the source", "(vi)", "the right side", (), (), None, "", noop))
    with pytest.raises(ValueError, match="none of \\['the right side'"):
        register.add(Declaration("the source", "(iv)", "before", (), (), None, "", noop))
    assert PLACES == ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")
    assert WORDS == ("the right side", "the step", "after the step", "any")
    assert (
        folder_of("the spin's step") == "the_spins_step"
        and folder_of("the self-source") == "the_self_source"
    )


def test_two_writers_of_one_value_at_one_place_need_a_declared_order():
    """The loop refuses two primitives that write the same value at the same place
    unless their order is declared (record 2212 (3)); distinct orders pass; the
    same value at another place is no conflict."""
    register = Register()
    register.add(
        Declaration(
            "the receive", "(i)", "the step", ("the Link's value",), ("the arrivals",), None, "", noop
        )
    )
    register.add(
        Declaration(
            "the internal representation",
            "(i)",
            "the right side",
            ("n pairs",),
            ("the arrivals",),
            None,
            "",
            noop,
        )
    )
    with pytest.raises(
        ValueError, match="all write 'the arrivals' at the place \\(i\\) and declare no order"
    ):
        register.check_writers()
    ordered = Register()
    ordered.add(
        Declaration(
            "the receive", "(i)", "the step", ("the Link's value",), ("the arrivals",), 1, "", noop
        )
    )
    ordered.add(
        Declaration(
            "the internal representation",
            "(i)",
            "the right side",
            ("n pairs",),
            ("the arrivals",),
            2,
            "",
            noop,
        )
    )
    ordered.add(Declaration("the trace", "any", "any", ("every word's integers",), (), None, "", None))
    ordered.check_writers()
    same_order = Register()
    same_order.add(Declaration("a", "(ii)", "after the step", (), ("the tally",), 1, "", noop))
    same_order.add(Declaration("b", "(ii)", "after the step", (), ("the tally",), 1, "", noop))
    with pytest.raises(ValueError, match="declare no order between them"):
        same_order.check_writers()
    apart = Register()
    apart.add(Declaration("a", "(i)", "the step", (), ("the tally",), None, "", noop))
    apart.add(Declaration("b", "(ii)", "after the step", (), ("the tally",), None, "", noop))
    apart.check_writers()


def test_a_term_naming_an_unknown_or_unbuilt_primitive_is_refused_by_name():
    """A term of the files names a primitive the register holds with a function;
    a name the register lacks and a row of the ledger not built are refused
    naming the file's line and the primitive."""
    register = Register()
    register.add(
        Declaration(
            "the hold",
            "(iv)",
            "the right side",
            ("the body's count M_k",),
            ("the held level",),
            None,
            "",
            noop,
        )
    )
    register.add(
        Declaration(
            "the source",
            "(iv)",
            "the right side",
            ("the record's form",),
            ("the sourced level",),
            None,
            "",
            None,
        )
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
    register.add(Declaration("the hold", "(iv)", "the right side", (), (), None, "", noop))
    register.add(Declaration("the trace", "any", "any", (), (), None, "", noop))
    register.add(Declaration("the source", "(iv)", "the right side", (), (), None, "", None))
    assert register.at("the hold", "(iv)") is noop
    assert register.at("the trace", "(ii)") is noop
    with pytest.raises(
        ValueError, match="calls the primitive 'the hold' at the place \\(i\\), but it declares \\(iv\\)"
    ):
        register.at("the hold", "(i)")
    with pytest.raises(ValueError, match="'the source' has no function"):
        register.at("the source", "(iv)")


def write_package(root: Path, folders: dict[str, str]) -> str:
    """A features package under `root` with the folders' sources, importable by name."""
    package = root / "features_under_test"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    for folder, source in folders.items():
        (package / folder).mkdir()
        (package / folder / "__init__.py").write_text(source, encoding="utf-8")
    sys.path.insert(0, str(root))
    return "features_under_test"


def test_the_register_finds_the_folders_and_refuses_a_folder_without_its_declaration(
    tmp_path, monkeypatch
):
    """Discovery by folders (record 2221 (3)): a folder declares its own name, place,
    word, reads and writes and binds its function; a folder without DECLARATION, a
    folder whose name is not its declared name's, a declaration with an unknown key
    and two folders declaring one name are refused by name; the folders' order is
    the register's; a folder without bind is a row not built."""
    good = (
        'DECLARATION = {"name": "the hold", "place": "(iv)", "word": "the right side", '
        '"reads": ("the body\'s count M_k",), "writes": ("the held level",), "section": "9.91 (3)"}\n'
        "def bind(loop):\n    return loop\n"
    )
    unbuilt = (
        'DECLARATION = {"name": "the source", "place": "(iv)", "word": "the right side", '
        '"reads": ("D_i",), "writes": ("the sourced level",), "section": "9.108 item 10"}\n'
    )
    package = write_package(tmp_path, {"the_hold": good, "the_source": unbuilt})
    monkeypatch.delitem(sys.modules, package, raising=False)
    register = discover(package)
    assert register.names == ("the hold", "the source")
    assert register.built_names() == ("the hold",)
    register.bind("the loop")
    assert register.at("the hold", "(iv)") == "the loop"
    with pytest.raises(ValueError, match="'the source', a row of the ledger not built yet"):
        register.check_terms([("universe.families[0].sourced", "the source")])
    for folder, source, message in (
        ("the_well", "WELL = 1\n", "declares no DECLARATION"),
        ("the_well", good, "declares the name 'the hold', whose folder is 'the_hold'"),
        (
            "the_well",
            'DECLARATION = {"name": "the well", "place": "(iv)", "word": "the right side", "reads": (), "writes": (), "section": "", "depth": 3}\n',
            "unknown keys \\['depth'\\]",
        ),
    ):
        bad_root = tmp_path / f"case_{len(list(tmp_path.iterdir()))}" / "root"
        bad_root.mkdir(parents=True)
        bad_package = write_package(bad_root, {"the_hold": good, folder: source})
        monkeypatch.delitem(sys.modules, bad_package, raising=False)
        for name in list(sys.modules):
            if name.startswith(bad_package):
                del sys.modules[name]
        with pytest.raises(ValueError, match=message):
            discover(bad_package)
        sys.path.remove(str(bad_root))


def test_the_engine_registers_the_twenty_three_by_their_folders_and_checks_every_term():
    """On a shipped test world the engine's register holds exactly the twenty-three
    folders' names in the folders' order, each with a place, a word and a section,
    the built ones bound to a function and the rows to do without one; every term a
    family or a body declares (the giving of an emitter among them) names a built
    primitive; the hold and the clicks are called through the register (the shipped
    worlds bit for bit: the suites' digests)."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=20)))
    assert simulation.register.names == FOLDER_NAMES
    assert set(simulation.register.built_names()) == BUILT
    for declaration in simulation.register.declarations.values():
        assert declaration.place in PLACES and declaration.word in WORDS and declaration.section
        assert (
            declaration.name.startswith("the ")
            and folder_of(declaration.name) == folder_of(declaration.name).strip()
        )
    terms = simulation.family_terms()
    names = {name for _label, name in terms}
    assert names <= BUILT
    assert {
        "the pair",
        "the send",
        "the operation",
        "the signed read",
        "the hold",
        "the giving",
    } <= names
    assert any(label.startswith("measured[") and name == "the giving" for label, name in terms)
    simulation.register.check_terms(terms)
    assert simulation.register.at("the wait", "(i)")() == 1
    for _ in range(20):
        simulation.step()
        assert simulation.books()["balanced"]
