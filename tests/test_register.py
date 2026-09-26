"""THE REGISTER OF PRIMITIVES, FOUND BY THEIR FOLDERS (issue #1154, cuts 1 and 2; the
model owner's decisions of 2026-09-26 through the Boss, records 2208, 2212, 2221 and 2224;
the short procedure of skills/workflow.md, point 5; ALGEBRA.md 9.110 item 7, 9.111 item 7,
9.112 item 1, 9.117).

The engine holds one register, name to function, read by the central loop alone; a
primitive's identity is its unique English name, the key of the ledger's table
(docs/designs/generic_engine/ENGINE_LEDGER.md section 3); every primitive is one folder
under src/event_universe/features/<name>/ (the name without the article: "the spin's step"
is spins_step) declaring its name, place (a code of 9.91 (8)), word (9.111 item 7), reads,
writes (the values named once in 9.117 item 1) and order (9.117 item 3), and holding its
function (`apply`, the mathematician's folders) or binding the loop's method (`bind`); the
register discovers the folders, so adding a feature touches no shared file. The refusals
at load, by name: a folder without a declaration or with a name not its own; a name
registered twice; a term naming a primitive the register lacks or one not built; two
writers of one value at one place with no order (a body's value written by a click at (ii)
is ordered at (iv), 9.117 item 1; a remainder is the writer's own and never collides); a
call at a place other than the declared one. Cut 2 binds the names to today's methods and
moves no body of code: every shipped world bit for bit (the digest tests of the suites; the
five worlds' comparison of the gate)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

import event_universe.features as features
from event_universe.core.register import (
    DEFERRED_VALUES,
    OWN_VALUES,
    PLACES,
    WORDS,
    Declaration,
    Register,
    discover,
    folder_of,
)
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
# the values named once in ALGEBRA.md 9.117 item 1 (and the source row's own word for its
# remainder): the rows of 9.117 write these and no other
NAMED_VALUES = {
    "a family's level at a Node",
    "the level next, the remainder",
    "the paces",
    "a Port's accumulator",
    "a body's content M_k",
    "a body's momentum n",
    "a body's spin S",
    "a body's position",
    "a body's remainders",
    "the record's tally",
    "the record's remainder",
}
ROWS_OF_9_117 = (
    "the signed read",
    "the source",
    "the giving",
    "the clicks",
    "the recoil's accumulator",
    "the feed",
    "the induction",
    "the spin's step",
    "the hop",
    "the trace",
)
# the orders of ALGEBRA.md 9.117 item 3 (the recoil's 2 on n at (iv) lands with its folder),
# the lifetime's on the tally at (ii) after the clicks (a row of the ledger, 9.88 (3))
ORDERS = {
    ("(iv)", "a family's level at a Node"): {"the hold": 1, "the source": 2},
    ("(iv)", "a body's content M_k"): {"the clicks": 1, "the giving": 2, "the clicks list": 3},
    ("(iv)", "a body's momentum n"): {"the giving": 1},
    ("(v)", "a body's momentum n"): {"the feed": 1, "the induction": 2},
    ("(i)", "the arrivals"): {"the receive": 1, "the internal representation": 2},
    ("(ii)", "the record's tally"): {"the clicks": 1, "the lifetime": 2},
}


def noop() -> None:
    return None


def test_a_name_registered_twice_or_an_unknown_place_or_word_is_refused_by_name():
    """One register, one name to one function (record 2212 (2)); a place is one of
    9.91 (8)'s five or "any"; a word one of 9.111 item 7's three or "any"; a folder is
    the name without the article, the apostrophe dropped, a space or a hyphen an
    underscore (the mathematician's folders signed_read and recoil, PRs 1164 and 1165)."""
    register = Register()
    register.add(
        Declaration(
            "the hold",
            "(iv)",
            ("a body's content M_k",),
            ("a family's level at a Node",),
            1,
            noop,
            "9.91 (3)",
            word="the right side",
        )
    )
    with pytest.raises(ValueError, match="'the hold' is registered twice"):
        register.add(Declaration("the hold", "(iv)", (), (), None, noop, ""))
    assert register.names == ("the hold",)
    with pytest.raises(ValueError, match="none of the interval's places"):
        register.add(Declaration("the source", "(vi)", (), (), None, noop, ""))
    with pytest.raises(ValueError, match="none of \\['the right side'"):
        register.add(Declaration("the source", "(iv)", (), (), None, noop, "", word="before"))
    assert PLACES == ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")
    assert WORDS == ("the right side", "the step", "after the step", "any")
    assert folder_of("the spin's step") == "spins_step"
    assert folder_of("the self-source") == "self_source"
    assert folder_of("the recoil's accumulator") == "recoils_accumulator"
    assert folder_of("the signed read") == "signed_read" and folder_of("hold") == "hold"
    assert DEFERRED_VALUES == {
        "a body's content M_k",
        "a body's momentum n",
        "a body's spin S",
        "a body's position",
        "a body's remainders",
    }
    assert OWN_VALUES == {"a body's remainders", "the record's remainder"}


def test_two_writers_of_one_value_at_one_place_need_a_declared_order():
    """The loop refuses two primitives that write the same value at the same place
    unless their order is declared (record 2212 (3)); distinct orders pass, an integer
    for every value or a mapping value to integer (the giving, 9.117 item 2); the same
    value at another place is no conflict; a body's value written by a click at (ii) is
    a deferred write ordered at (iv) (9.117 item 1); a remainder is the writer's own."""
    register = Register()
    register.add(
        Declaration("the receive", "(i)", ("the Link's value",), ("the arrivals",), None, noop, "")
    )
    register.add(
        Declaration(
            "the internal representation", "(i)", ("n pairs",), ("the arrivals",), None, noop, ""
        )
    )
    with pytest.raises(
        ValueError, match="all write 'the arrivals' at the place \\(i\\) and declare no order"
    ):
        register.check_writers()
    ordered = Register()
    ordered.add(Declaration("the receive", "(i)", ("the Link's value",), ("the arrivals",), 1, noop, ""))
    ordered.add(
        Declaration("the internal representation", "(i)", ("n pairs",), ("the arrivals",), 2, noop, "")
    )
    ordered.add(
        Declaration("the trace", "any", ("every word's integers",), (), None, None, "", word="any")
    )
    ordered.check_writers()
    same_order = Register()
    same_order.add(Declaration("a", "(ii)", (), ("the tally",), 1, noop, ""))
    same_order.add(Declaration("b", "(ii)", (), ("the tally",), 1, noop, ""))
    with pytest.raises(ValueError, match="declare no order between them"):
        same_order.check_writers()
    apart = Register()
    apart.add(Declaration("a", "(i)", (), ("the tally",), None, noop, ""))
    apart.add(Declaration("b", "(ii)", (), ("the tally",), None, noop, ""))
    apart.check_writers()
    # the click's deferred writes: the clicks at (ii) with one integer for every value it
    # writes, the giving at (ii) with a mapping (M_k 2, n 1), the recoil at (iv) on n 2; the
    # writes of M_k and n are ordered at (iv), the tally stays at (ii)
    deferred = Register()
    clicks = Declaration(
        "the clicks", "(ii)", (), ("the record's tally", "a body's content M_k"), 1, noop, ""
    )
    giving = Declaration(
        "the giving",
        "(ii)",
        (),
        ("a family's level at a Node", "a body's content M_k", "a body's momentum n"),
        {"a body's content M_k": 2, "a body's momentum n": 1},
        noop,
        "",
    )
    recoil = Declaration(
        "the recoil", "(iv)", (), ("a body's momentum n", "a body's remainders"), 2, noop, ""
    )
    hold = Declaration(
        "the hold", "(iv)", (), ("a family's level at a Node", "a body's remainders"), 1, noop, ""
    )
    for declaration in (clicks, giving, recoil, hold):
        deferred.add(declaration)
    deferred.check_writers()
    assert (
        clicks.place_of("a body's content M_k") == "(iv)"
        and clicks.place_of("the record's tally") == "(ii)"
    )
    assert giving.order_of("a body's content M_k") == 2 and giving.order_of("a body's momentum n") == 1
    assert (
        giving.order_of("a family's level at a Node") is None
        and clicks.order_of("the record's tally") == 1
    )
    assert recoil.place_of("a body's momentum n") == "(iv)"
    deferred.add(Declaration("the clicks list", "(ii)", (), ("a body's content M_k",), None, None, ""))
    with pytest.raises(
        ValueError,
        match="'the clicks', 'the giving', 'the clicks list' all write \"a body's content M_k\" at the place \\(iv\\)",
    ):
        deferred.check_writers()
    own = Register()
    own.add(
        Declaration(
            "the feed",
            "(v)",
            (),
            ("a body's momentum n", "a body's remainders"),
            {"a body's momentum n": 1},
            None,
            "",
        )
    )
    own.add(
        Declaration(
            "the induction",
            "(v)",
            (),
            ("a body's momentum n", "a body's remainders"),
            {"a body's momentum n": 2},
            None,
            "",
        )
    )
    own.add(
        Declaration("the hop", "(v)", (), ("a body's position", "a body's remainders"), None, noop, "")
    )
    own.check_writers()


def test_a_term_naming_an_unknown_or_unbuilt_primitive_is_refused_by_name():
    """A term of the files names a primitive the register holds with a function;
    a name the register lacks and a row of the ledger not built are refused
    naming the file's line and the primitive."""
    register = Register()
    register.add(
        Declaration(
            "the hold", "(iv)", ("a body's content M_k",), ("a family's level at a Node",), 1, noop, ""
        )
    )
    register.add(
        Declaration(
            "the source", "(iv)", ("the record's form",), ("a family's level at a Node",), 2, None, ""
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
    place "any" admits every place; an unbuilt row has no function to call; a
    binder gives its function for the loop at `bind`, once."""
    register = Register()
    register.add(Declaration("the hold", "(iv)", (), (), None, noop, ""))
    register.add(Declaration("the trace", "any", (), (), None, noop, "", word="any"))
    register.add(Declaration("the source", "(iv)", (), (), None, None, ""))
    register.add(Declaration("the wait", "(i)", (), (), None, None, "", binder=lambda loop: loop))
    assert register.at("the hold", "(iv)") is noop
    assert register.at("the trace", "(ii)") is noop
    with pytest.raises(
        ValueError, match="calls the primitive 'the hold' at the place \\(i\\), but it declares \\(iv\\)"
    ):
        register.at("the hold", "(i)")
    with pytest.raises(ValueError, match="'the source' has no function"):
        register.at("the source", "(iv)")
    assert register.built_names() == ("the hold", "the trace", "the wait")
    with pytest.raises(ValueError, match="'the wait' has no function"):
        register.at("the wait", "(i)")
    register.bind("the loop")
    assert register.at("the wait", "(i)") == "the loop"


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


def forget(package: str) -> None:
    for name in list(sys.modules):
        if name == package or name.startswith(package + "."):
            del sys.modules[name]


def test_the_register_finds_the_folders_and_refuses_a_folder_without_its_declaration(tmp_path):
    """Discovery by folders (record 2221 (3)): a folder declares its own name, place,
    word, reads, writes and order as a Declaration of the register with its own
    function (the mathematician's form, PRs 1164 and 1165) or as a dict of its words
    with `bind`; a folder without DECLARATION, a folder whose name is not its declared
    name's, a declaration with an unknown key, a bind that is no function and two
    folders declaring one name are refused by name; the folders' order is the
    register's; a folder with neither function nor bind is a row not built."""
    good = (
        'DECLARATION = {"name": "the hold", "place": "(iv)", "word": "the right side", '
        '"reads": ("a body\'s content M_k",), "writes": ("a family\'s level at a Node",), '
        '"order": 1, "section": "9.91 (3)"}\n'
        "def bind(loop):\n    return loop\n"
    )
    unbuilt = (
        'DECLARATION = {"name": "the source", "place": "(iv)", "word": "the right side", '
        '"reads": ("D_i",), "writes": ("a family\'s level at a Node",), "order": 2, '
        '"section": "9.117 item 2"}\n'
    )
    own_function = (
        "from event_universe.core.register import Declaration\n"
        "def apply(term, start, own):\n    return ('the paces', term)\n"
        'DECLARATION = Declaration("the signed read", "(i)", ("the read families\' arguments",), '
        '("the paces",), None, apply, "9.117 item 2, the first row")\n'
    )
    package = write_package(tmp_path, {"hold": good, "source": unbuilt, "signed_read": own_function})
    forget(package)
    register = discover(package)
    assert register.names == ("the hold", "the signed read", "the source")
    assert register.built_names() == ("the hold", "the signed read")
    register.check_writers()
    register.bind("the loop")
    assert register.at("the hold", "(iv)") == "the loop"
    assert register.at("the signed read", "(i)")("a term", None, None) == ("the paces", "a term")
    assert (
        register.declarations["the hold"].order == 1
        and register.declarations["the hold"].word == "the right side"
    )
    with pytest.raises(ValueError, match="'the source', a row of the ledger not built yet"):
        register.check_terms([("universe.families[0].sourced", "the source")])
    cases = (
        ("well", "WELL = 1\n", "declares no DECLARATION"),
        ("well", "DECLARATION = 3\n", "declares no DECLARATION"),
        ("well", good, "declares the name 'the hold', whose folder is 'hold'"),
        (
            "well",
            'DECLARATION = {"name": "the well", "place": "(iv)", "word": "the right side", '
            '"reads": (), "writes": (), "section": "", "depth": 3}\n',
            "unknown keys \\['depth'\\]",
        ),
        (
            "well",
            'DECLARATION = {"name": "the well", "place": "(iv)", "reads": (), "writes": (), "section": ""}\n'
            "bind = 3\n",
            "bind must be a function of the loop or absent",
        ),
        ("the_hold", good, "declares the name 'the hold', whose folder is 'hold'"),
    )
    for number, (folder, source, message) in enumerate(cases):
        bad_root = tmp_path / f"case_{number}" / "root"
        bad_root.mkdir(parents=True)
        bad_package = write_package(bad_root, {"hold": good, folder: source})
        forget(bad_package)
        with pytest.raises(ValueError, match=message):
            discover(bad_package)
        sys.path.remove(str(bad_root))
    forget(package)
    sys.path.remove(str(tmp_path))


def test_the_engine_registers_the_twenty_three_by_their_folders_and_checks_every_term():
    """On a shipped test world the engine's register holds exactly the twenty-three
    folders' names in the folders' order, each folder the name's, each with a place, a
    word and a section, the built ones bound to a function and the rows to do without
    one; the rows of 9.117 write the values named once (item 1) and the writers' orders
    are 9.117 item 3's; every term a family or a body declares (the giving of an emitter
    among them) names a built primitive; the hold and the clicks are called through the
    register (the shipped worlds bit for bit: the suites' digests)."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=20)))
    register = simulation.register
    assert register.names == FOLDER_NAMES
    assert set(register.built_names()) == BUILT
    folders = Path(features.__file__).parent
    for declaration in register.declarations.values():
        assert declaration.place in PLACES and declaration.word in WORDS and declaration.section
        assert declaration.name.startswith("the ") and not folder_of(declaration.name).startswith("the_")
        assert (folders / folder_of(declaration.name) / "__init__.py").is_file()
    for name in ROWS_OF_9_117:
        assert set(register.declarations[name].writes) <= NAMED_VALUES, name
    for (place, value), expected in ORDERS.items():
        for name, order in expected.items():
            declaration = register.declarations[name]
            assert declaration.place_of(value) == place, (name, value)
            assert declaration.order_of(value) == order, (name, value)
    register.check_writers()
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
    register.check_terms(terms)
    assert register.at("the wait", "(i)")() == 1
    for _ in range(20):
        simulation.step()
        assert simulation.books()["balanced"]
