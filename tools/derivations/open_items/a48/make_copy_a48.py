"""a48: the flagged copy of src/event_universe under tools/derivations/a48/src_a48/, written from the engine's files by exact text
replacements, each matched once and named; the flag the environment variable A48_READ (unset or anything but "even": the
engine's path bit for bit; "even": the draw's digit read even under the mirror of its line, the remainder's distance from the
half wall it was born at, |r - half(W)| on its lattice, the base half(W) div F + 1). Never touches src/.
Usage: python make_copy_a48.py"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parents[2] / "src" / "event_universe"
OUT = HERE / "src_a48" / "event_universe"

REPLACEMENTS = {
    "node.py": [
        (
            # 1. the digit's read takes the wall and the lattice, and reads even under the flag
            '''    def digit_of(self, rem: int, values: int) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds."""
        return rem, values
''',
            '''    def digit_of(self, rem: int, wall: int, lattice_f: int) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds (the engine's
        path, A48_READ unset); under A48_READ=even the remainder read by its distance from the half wall it was born at,
        |r - half(W)|, even under the mirror r -> 2 half(W) - r of a reversed line, the count half(W) div F."""
        if os.environ.get("A48_READ") == "even":
            h = int(half(wall))
            return abs(rem - h), quotient(h, lattice_f)
        return rem, quotient(wall, lattice_f)
''',
        ),
        (
            "from event_universe.core.rule3 import carried_division, half, link_unit_of, mirrored, unit_of, wall_of\n",
            "import os\n\nfrom event_universe.core.rule3 import (\n    carried_division,\n    half,\n    link_unit_of,\n    mirrored,\n    quotient,\n    unit_of,\n    wall_of,\n)\n",
        ),
        (
            # 3. the swap's mirror of a born remainder: the one rule's path unless A48_SWAP=half (the involution about the birth)
            '            line.rem = np.where(top, mirrored(h.rem, h.wall, 1 + (sgn < 0)), line.rem)\n',
            '            line.rem = np.where(top, about_birth(h.rem, h.wall, 1 + (sgn < 0)), line.rem)\n',
        ),
        (
            '                line.wr = np.where(top, mirrored(h.wr, line.wwall, 1), line.wr)\n',
            '                line.wr = np.where(top, about_birth(h.wr, line.wwall, 1), line.wr)\n',
        ),
        (
            'def bits_of(a: Any) -> int:\n',
            'def about_birth(remainder: Any, wall: Any, reversals: int) -> Any:\n    """The mirror of a born remainder at the swap: the engine\'s path (A48_SWAP unset) the one rule\'s wall - 1 - r\n    (rule3.mirrored); under A48_SWAP=half the involution about the remainder\'s birth point, 2 half(wall) - r with 0 its own\n    mirror, the mirror the riding division itself imposes on a reversed line seeded at the half wall (a48)."""\n    if os.environ.get("A48_SWAP") != "half" or reversals % 2 == 0:\n        return mirrored(remainder, wall, reversals)\n    doubled = 2 * half(wall)\n    return np.where(np.asarray(remainder, dtype=object) == 0, 0, doubled - remainder)\n\n\ndef bits_of(a: Any) -> int:\n',
        ),
    ],
    "take.py": [
        (
            # 2. the read passes the wall and the lattice; the origin check reads the raw remainder as before
            "            rem, values = node.digit_of(int(line.rem[n]), quotient(wl, f))\n            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))\n",
            "            raw = int(line.rem[n])\n            rem, values = node.digit_of(raw, wl, f)\n            origin = origin and raw in (w_half, mirrored(w_half, node.w, 1))\n",
        ),
    ],
}


def main():
    if OUT.parent.exists():
        shutil.rmtree(OUT.parent)
    shutil.copytree(SRC, OUT)
    for name, pairs in REPLACEMENTS.items():
        path = OUT / name
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            if text.count(old) != 1:
                print(f"{name}: the text to replace is matched {text.count(old)} times, not once:\n{old}")
                sys.exit(1)
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
    print(f"the flagged copy written under {OUT.parent} ({sum(len(p) for p in REPLACEMENTS.values())} replacements)")


if __name__ == "__main__":
    main()
