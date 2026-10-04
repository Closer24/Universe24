def test_every_row_of_the_proofs_inventory_returns_its_verdict_and_the_unchecked_only_fall():
    """The proofs' gate (the owner's order of 2026-10-04, 07:50 UTC; the advisor's design, #1793 comment 5977935062): every row of tools/derivations/proofs_inventory.json with a check runs it to the row's verdict (holds and witness only True, a finding False, the discrepancy reproduced), every check_ function of the proofs_ modules is a row's, the rows of the kinds A, B and C without a machine check are a ratchet that only falls, the header's counts are the rows', and no proofs_ module imports the engine or names a run's file."""
    import ast
    import importlib.util
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    derivations = root / "tools" / "derivations"
    modules = (
        "proofs_ground.py",
        "proofs_band.py",
        "proofs_form.py",
        "proofs_booking.py",
        "proofs_paces.py",
        "proofs_credit.py",
        "proofs_bodies.py",
        "proofs_audit.py",
        "proofs_far_regime.py",
    )
    theorems_without_machine_check = (
        13  # the ratchet: the rows of the kinds A, B and C with no check or a witness only
    )
    document = json.loads((derivations / "proofs_inventory.json").read_text(encoding="utf-8"))
    rows, counts = document["rows"], document["header"]["counts"]
    loaded = {}
    for name in modules:
        spec = importlib.util.spec_from_file_location(name[:-3], derivations / name)
        assert spec is not None and spec.loader is not None
        loaded[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded[name])
        tree = ast.parse((derivations / name).read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert not imported & {"event_universe", "src", "click_counts"}, (name, imported)
        strings = [
            n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)
        ]
        assert not [
            s for s in strings for marker in ("runs/", ".output.json", ".look.json") if marker in s
        ], name
    referenced = set()
    for row in rows:
        assert row["kind"] in "ABCD" and row["verdict"] in (
            "holds",
            "witness only",
            "finding",
            "none",
        ), row["id"]
        if row["check"] is None:
            assert row["verdict"] == "none", row["id"]
            continue
        name, function = Path(row["check"]["module"]).name, row["check"]["function"]
        held, computed = getattr(loaded[name], function)()
        assert held == (row["verdict"] in ("holds", "witness only")), (
            row["id"],
            row["name"],
            row["verdict"],
            computed,
        )
        referenced.add((name, function))
    defined = {(name, f) for name in modules for f in dir(loaded[name]) if f.startswith("check_")}
    assert defined == referenced, defined ^ referenced
    unchecked = [
        r["id"]
        for r in rows
        if r["kind"] in "ABC" and (r["check"] is None or r["verdict"] == "witness only")
    ]
    assert len(unchecked) <= theorems_without_machine_check, unchecked
    assert counts["without_machine_check"] == len(unchecked) and counts["rows"] == len(rows), counts
    assert [r["id"] for r in rows[:10]] == [f"A{i:02d}" for i in range(1, 11)], (
        "the audit's ten items first"
    )
