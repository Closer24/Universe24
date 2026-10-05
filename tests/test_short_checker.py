def test_the_long_version_passes_its_own_checker_and_a_foreign_number_is_a_miss() -> None:
    """The self-test (short = long at the frozen commit) reports 0 misses and 0 unresolved pointers, and the
    long main text's first number beside a number of the probe's own gives one miss, the probe's; the imports
    stand inside the test so the file is the test alone."""
    import importlib.util
    import sys
    from pathlib import Path

    import pytest

    path = Path(__file__).resolve().parents[1] / "paper" / "general_formula" / "short_checker.py"
    spec = importlib.util.spec_from_file_location("short_checker", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    try:
        audit, pointers, text = module.self_test()
    except FileNotFoundError as error:
        pytest.skip(f"the frozen long version is not in this clone's history: {error}")
    assert audit.misses == [] and pointers.unresolved == [], text
    assert audit.distinct > 0 and pointers.checked > 0
    long, _sources = module.long_version(module.LONG_REF, None, None)
    first = module.tokens(long["long main"])[0].written
    probe = module.audit_numbers({"probe": f"\\begin{{document}} ${first}$ and $12345678901234$"}, long)
    assert [miss.normalised for miss in probe.misses] == ["12345678901234"]
