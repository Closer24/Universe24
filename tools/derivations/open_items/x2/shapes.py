"""Hand X2: the shapes' arithmetic written inline or twice (the owner's addition of 2026-10-25: every vector and tensor
operation one function used from there alone). Per function, the lines matching each idiom:
  BILINEAR   the Wronskian or the current, now_i before_j - before_i now_j (re im' - im re')
  SENSE_J    the sign's current J_a = re (im_+ - im_-) - im (re_+ - re_-)
  TENSION    the axis part, a centred difference squared (or the former h_a product)
  TRACE      the trace of the three axis parts and the traceless part 3 T_aa - trace
  AXIS_LOOP  a loop over the three axes with the two Ports 2a, 2a + 1 (the vector's components by position)
  CONJUGATE  the sense's exchange, im -> -im, or a frame sign on the im part
  COMPLEMENT the carry's mirror, wall - 1 - r
  IMAGE48    an element of the cube's 48 applied to a Node, an axis or a sign (permutations, signs, det)
  FORM       the form D = now^2 - next x before or w (now^2 + before^2) - S now before
Usage: python shapes.py <root> <subdir> <out.json>
"""
import ast
import json
import re
import sys
from pathlib import Path

IDIOMS = {
    "BILINEAR": r"(now|lnow)\S*\s*\*\s*\S*(before|lbefore)\S*\s*-\s*\S*(now|lnow|before|lbefore)\S*\s*\*\s*\S*(before|lbefore|now|lnow)|here\.now \* there\.before - here\.before \* there\.now",
    "SENSE_J": r"dz_re|dz_im|im_at\[plus\] - im_at\[minus\]|re_at\[plus\] - re_at\[minus\]",
    "TENSION": r"difference \* difference|\bd \* d\b|roll\(line\.now, a, -1\) \* roll\(line\.now, a, 1\)|now_\(i-a\) now_\(i\+a\)|aa_i \+ aa_j|here \+ there",
    "TRACE": r"trace = trace \+ exact|parts\[0\] \+ parts\[1\] \+ parts\[2\]|sum\(stresses\[s\]\[a\]|3 \* parts\[a\] - trace|AXES \* axes\[s\]|AXES \* np\.asarray\(flux, dtype=object\) - total|trace \* p0|- trace\b",
    "AXIS_LOOP": r"for axis in range\((3|AXES)\)|for a in range\(3\)|for a in range\(AXES\)|2 \* axis \+ 1|2 \* a \+ 1|\[2 \* axis\]|\(axis, side\) in AXES|PORT_SIDES|frames\[2 \* a\]",
    "CONJUGATE": r"-im\.|sgn = -1 if im|-line\.before|frames\[port\] \* im_j|fr\[port\]|\* im_j\b|signs\[2 \* axis|1 - 2 \* \(|np\.where\(mask, -im|fp \* roll|fm \* roll|-signs\[",
    "COMPLEMENT": r"wall - 1 - |complement\(|1 - self\.phi\.rem|1 - phi|born - 1 - |entered - 1 -",
    "IMAGE48": r"signed_permutations|permutations\(|m @ |perm\[|signs\[ax\]|linalg\.det|image\(|signed permutation",
    "FORM": r"now \* now \+ before \* before|re\.now \* re\.now - nre\.now \* re\.before|before\.now \* before\.now - after\.now \* before\.before|form_term\(|\.now \* \w+\.now - \w+\.now \* \w+\.before",
}


def main():
    root, sub, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    base = root / sub
    places = []
    by_idiom = {k: 0 for k in IDIOMS}
    for path in sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        tree = ast.parse(text)
        rel = str(path.relative_to(base))
        functions = [(n.name, n.lineno, n.end_lineno) for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        for name, start, end in functions:
            hits = {}
            for number in range(start, end + 1):
                line = lines[number - 1]
                code = line.split('"""')[0] if line.strip().startswith('"""') else line
                if code.strip().startswith("#"):
                    continue
                code = code.split("  # ")[0]
                for idiom, rx in IDIOMS.items():
                    if re.search(rx, code):
                        hits.setdefault(idiom, []).append(number)
            if hits:
                # a nested function's hits are its own: drop lines of inner functions
                inner = [(s, e) for n2, s, e in functions if start < s and e <= end and (n2, s, e) != (name, start, end)]
                for idiom in list(hits):
                    hits[idiom] = [l for l in hits[idiom] if not any(s <= l <= e for s, e in inner)]
                    if not hits[idiom]:
                        del hits[idiom]
            if hits:
                for idiom, found in hits.items():
                    by_idiom[idiom] += len(found)
                places.append({"file": rel, "function": name, "start": start, "end": end, "lines": end - start + 1, "hits": hits})
    report = {"subdir": sub, "functions_with_shape_arithmetic": len(places), "lines_by_idiom": by_idiom,
              "idiom_lines_total": sum(by_idiom.values()), "list": places}
    Path(out).write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{sub}: {len(places)} functions hold the shapes' arithmetic inline; matching lines by idiom {by_idiom}; total {sum(by_idiom.values())}")
    for p in places:
        print(f"  {p['file']}:{p['function']} {p['start']}-{p['end']} " + "; ".join(f"{k} {v}" for k, v in p["hits"].items()))


if __name__ == "__main__":
    main()
