"""The register of primitives found by their folders: one register, name to function, read by the loop alone; each folder declares its name, place, word, reads and writes, and the register refuses the rest."""

from __future__ import annotations

import importlib
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
    declaration_of,
    discover,
    folder_of,
)
from event_universe.core.step import Step
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.running import ORDERS
from tests.worlds import emitter_world


def declared_folders() -> list[tuple[str, str, bool]]:
    """Every folder of the features package on disk with its declared name and whether it is built (a function or a bind), in the folders' order: the register lists nothing by hand (record 2221 (3)), so a folder added or built touches no shared file."""
    package = Path(features.__file__).parent
    found = []
    for folder in sorted(p for p in package.iterdir() if p.is_dir() and (p / "__init__.py").is_file()):
        module = importlib.import_module(f"{features.__name__}.{folder.name}")
        declaration = declaration_of(folder.name, module)
        found.append((folder.name, declaration.name, declaration.built))
    return found


# the values named once in ALGEBRA.md #the-primitives (and the source row's own word for its remainder): the rows of 9.117 write these and no other
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
    "the spin's step",
    "the trace",
)


def noop() -> None:
    return None


def test_a_name_registered_twice_or_an_unknown_place_or_word_is_refused_by_name():
    """One register, one name to one function (record 2212 (2)); a place is one of ALGEBRA.md #the-interval's five or "any"; a word one of ALGEBRA.md #the-primitives's three or "any"; a folder is the name without the article, the apostrophe dropped, a space or a hyphen an underscore (the mathematician's folders signed_read and recoil, PRs 1164 and 1165)."""
    register = Register()
    register.add(
        Declaration(
            "the hold",
            "(iv)",
            ("a body's content M_k",),
            ("a family's level at a Node",),
            noop,
            "ALGEBRA.md #the-interval",
            word="the right side",
        )
    )
    with pytest.raises(ValueError, match="'the hold' is registered twice"):
        register.add(Declaration("the hold", "(iv)", (), (), noop, ""))
    assert register.names == ("the hold",)
    with pytest.raises(ValueError, match="none of the interval's places"):
        register.add(Declaration("the source", "(vi)", (), (), noop, ""))
    with pytest.raises(ValueError, match="none of \\['the right side'"):
        register.add(Declaration("the source", "(iv)", (), (), noop, "", word="before"))
    assert PLACES == ("(i)", "(ii)", "(iii)", "(iv)", "(v)", "any")
    assert WORDS == ("the right side", "the step", "after the step", "any")
    assert folder_of("the spin's step") == "spins_step" and folder_of("the self-source") == "self_source"
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


def test_the_step_file_orders_the_writers_of_one_value_and_a_writer_it_leaves_out_is_refused():
    """The order among the writers of one value at one place is the step file's (record 2251), a write deferred from (ii) to (iv) (ALGEBRA.md #the-primitives) before the place's own writers; a writer the file leaves out is refused by name; a remainder is the writer's own and never collides; the same value at another place is no conflict."""
    register = Register()
    register.add(Declaration("the receive", "(i)", ("the Link's value",), ("the arrivals",), noop, ""))
    register.add(
        Declaration("the internal representation", "(i)", ("n pairs",), ("the arrivals",), noop, "")
    )
    step = Step({"(i)": ("the receive", "the internal representation")}, "d")
    assert register.writers("the arrivals", "(i)", step) == (
        "the receive",
        "the internal representation",
    )
    register.check_writers(step)
    with pytest.raises(
        ValueError,
        match="'the internal representation' writes 'the arrivals' at the place \\(i\\) and is not in the step file",
    ):
        register.check_writers(Step({"(i)": ("the receive",)}, "d"))
    deferred = Register()
    clicks = Declaration(
        "the clicks", "(ii)", (), ("the record's tally", "a body's content M_k"), noop, ""
    )
    giving = Declaration(
        "the giving",
        "(ii)",
        (),
        ("a family's level at a Node", "a body's content M_k", "a body's momentum n"),
        noop,
        "",
    )
    recoil = Declaration(
        "the recoil", "(iv)", (), ("a body's momentum n", "a body's remainders"), noop, ""
    )
    hold = Declaration(
        "the hold", "(iv)", (), ("a family's level at a Node", "a body's remainders"), noop, ""
    )
    for declaration in (clicks, giving, recoil, hold):
        deferred.add(declaration)
    step = Step({"(ii)": ("the clicks", "the giving"), "(iv)": ("the hold", "the recoil")}, "d")
    deferred.check_writers(step)
    assert (
        clicks.place_of("a body's content M_k") == "(iv)"
        and clicks.place_of("the record's tally") == "(ii)"
    )
    assert recoil.place_of("a body's momentum n") == "(iv)"
    assert deferred.writers("a body's content M_k", "(iv)", step) == ("the clicks", "the giving")
    assert deferred.writers("a body's momentum n", "(iv)", step) == ("the giving", "the recoil")
    # the giving's level write is at (ii) itself (not a body's value): no conflict with the hold's at (iv)
    assert deferred.writers("a family's level at a Node", "(iv)", step) == ("the hold",)
    # a remainder is the writer's own: two writers of it at one place need no order
    assert deferred.writers("a body's remainders", "(iv)", step) == ("the hold", "the recoil")
    own = Register()
    own.add(Declaration("a push", "(v)", (), ("a body's momentum n", "a body's remainders"), None, ""))
    own.add(Declaration("a shift", "(v)", (), ("a body's position", "a body's remainders"), None, ""))
    own.check_writers(Step({"(v)": ("a push",)}, "d"))


def test_a_term_naming_an_unknown_or_unbuilt_primitive_is_refused_by_name():
    """A term of the files names a primitive the register holds with a function; a name the register lacks and a row of the ledger not built are refused naming the file's line and the primitive."""
    register = Register()
    register.add(
        Declaration(
            "the hold", "(iv)", ("a body's content M_k",), ("a family's level at a Node",), noop, ""
        )
    )
    register.add(
        Declaration(
            "the source", "(iv)", ("the record's form",), ("a family's level at a Node",), None, ""
        )
    )
    register.check_terms([("universe.families[0].held", "the hold")])
    with pytest.raises(ValueError, match="names the primitive 'the well', which the register lacks"):
        register.check_terms([("universe.families[0].well", "the well")])
    with pytest.raises(ValueError, match="'the source', a row of the ledger not built yet"):
        register.check_terms([("universe.families[1].sourced", "the source")])
    assert register.built_names() == ("the hold",)


def test_the_loop_calls_a_primitive_at_its_declared_place_alone():
    """A call at a place other than the declared one is refused; the trace's place "any" admits every place; an unbuilt row has no function to call; a binder gives its function for the loop at `bind`, once."""
    register = Register()
    register.add(Declaration("the hold", "(iv)", (), (), noop, ""))
    register.add(Declaration("the trace", "any", (), (), noop, "", word="any"))
    register.add(Declaration("the source", "(iv)", (), (), None, ""))
    register.add(Declaration("the wait", "(i)", (), (), None, "", binder=lambda loop: loop))
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
    """Discovery by folders (record 2221 (3)): a folder declares its own name, place, word, reads, writes and order as a Declaration of the register with its own function (the mathematician's form, PRs 1164 and 1165) or as a dict of its words with `bind`; a folder without DECLARATION, a folder whose name is not its declared name's, a declaration with an unknown key, a bind that is no function and two folders declaring one name are refused by name; the folders' order is the register's; a folder with neither function nor bind is a row not built."""
    good = (
        'DECLARATION = {"name": "the hold", "place": "(iv)", "word": "the right side", '
        '"reads": ("a body\'s content M_k",), "writes": ("a family\'s level at a Node",), '
        '"section": "ALGEBRA.md #the-interval"}\n'
        "def bind(loop):\n    return loop\n"
    )
    unbuilt = (
        'DECLARATION = {"name": "the source", "place": "(iv)", "word": "the right side", '
        '"reads": ("D_i",), "writes": ("a family\'s level at a Node",), '
        '"section": "ALGEBRA.md #the-primitives"}\n'
    )
    own_function = (
        "from event_universe.core.register import Declaration\n"
        "def apply(term, start, own):\n    return ('the paces', term)\n"
        'DECLARATION = Declaration("the signed read", "(i)", ("the read families\' arguments",), '
        '("the paces",), apply, "ALGEBRA.md #the-primitives, the first row")\n'
    )
    package = write_package(tmp_path, {"hold": good, "source": unbuilt, "signed_read": own_function})
    forget(package)
    register = discover(package)
    assert register.names == ("the hold", "the signed read", "the source")
    assert register.built_names() == ("the hold", "the signed read")
    register.check_writers(Step({"(i)": ("the signed read",), "(iv)": ("the hold", "the source")}, "d"))
    register.bind("the loop")
    assert register.at("the hold", "(iv)") == "the loop"
    assert register.at("the signed read", "(i)")("a term", None, None) == ("the paces", "a term")
    assert register.declarations["the hold"].word == "the right side"
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


def test_the_engine_registers_every_folder_on_disk_and_checks_every_term():
    """On a shipped test world the engine's register holds exactly the folders' names in the folders' order, found on disk and listed nowhere by hand (the recoil's folder among them, PR #1165), each folder the name's, each with a place, a word and a section, the built ones bound to a function and the rows to do without one; the rows of 9.117 write the values named once (item 1) and the writers' orders are ALGEBRA.md #the-primitives's; every term a family or a body declares (the giving of an emitter among them) names a built primitive; the hold and the clicks are called through the register (the shipped worlds bit for bit: the suites' digests)."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=20)))
    register = simulation.register
    folders_found = declared_folders()
    assert register.names == tuple(name for _folder, name, _built in folders_found)
    assert set(register.built_names()) == {name for _folder, name, built in folders_found if built}
    assert "the recoil" in register.built_names() and len(folders_found) == len(register.names)
    folders = Path(features.__file__).parent
    for declaration in register.declarations.values():
        assert declaration.place in PLACES and declaration.word in WORDS and declaration.section
        assert declaration.name.startswith("the ") and not folder_of(declaration.name).startswith("the_")
        assert (folders / folder_of(declaration.name) / "__init__.py").is_file()
    for name in ROWS_OF_9_117:
        assert set(register.declarations[name].writes) <= NAMED_VALUES, name
    step = simulation.world.step
    for (place, value), expected in ORDERS.items():
        assert register.writers(value, place, step) == expected, (place, value)
    register.check_writers(step)
    assert register.step is step and step.digest
    terms = simulation.family_terms()
    names = {name for _label, name in terms}
    assert (
        names <= set(register.built_names())
        and {"the pair", "the send", "the operation", "the signed read", "the hold", "the giving"}
        <= names
    )
    assert any(label.startswith("measured[") and name == "the giving" for label, name in terms)
    register.check_terms(terms)
    assert register.at("the wait", "(i)")() == 1
    for _ in range(20):
        simulation.step()
        assert simulation.books()["balanced"]
