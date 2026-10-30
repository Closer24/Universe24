"""The decoder's readings of a record written by B's draw, from the record's lines alone (Animate; beside the engine:
the decoder's code waits with the build, decision 32).

Each record is read first by the decoder's own reader (src/tensor24/decoder/records.py, the schema 1.1's guards); the
1.2 fields stand in it as fields the schema does not name, whole numbers and labels. Then nine readings, each a
comparison that can fail, each NOT READ with its cause where the record lacks what it needs:
  1. S: two parties' correlations from the takes alone (each take's frame and the part it wrote, paired through
     the birth it names, G5), against the local bound 2 and against nature's S at those frames;
  2. M: Mermin's combination for three parties, against 2 and against nature's;
  3. the joint clicks: per setting pair or triple, the joint outcomes' counts against nature's law at those frames;
  4. the draw: every split click's c over room and drawn, law 9 over sigma_f sigma_b (G6), line by line;
  5. the sizes: at every source, sigma_f sigma_b over room is nature's law at the frames brought back, exactly, and
     for one quantum the future is silent (sigma_b alike, Born);
  6. no signal: each party's marginal against the other parties' settings;
  7. one quantum written once: the takes per birth of a quantum with no frame, and g2 per pair of absorbers;
  8. the handshake: the frames brought back to the source are the frames its takes took in, and the drawn part is
     what each take wrote;
  9. late: each take's frame was set by its detector's last choice, made spacelike to the birth and outside every
     other take's past light cone.
Nature's laws are the decoder's to hold: the singlet's for two parties and GHZ's for three (frames on the equator),
in whole numbers from the frames' axis form. A statistical reading departs where it stands Z_BOUND standard errors
off, and a chi-square where its upper tail is below a normal's two-sided tail at Z_BOUND standard deviations: the
toy's bound, named.
"""

import math
import sys
from bisect import bisect_left
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.decoder import records  # noqa: E402

ORDER = "z fastest: the site (x sy + y) sz + z"  # the runner's, so the reader can place each Node-clock
Z_BOUND = 4
ALPHA = math.erfc(Z_BOUND / math.sqrt(2))  # a normal's two-sided tail at Z_BOUND standard deviations
HOLDS, FAILS, NOT_READ = "holds", "fails", "not read"
NAMES = (
    "1. S, two parties",
    "2. M, three parties",
    "3. the joint clicks",
    "4. the draw, line by line",
    "5. the sizes at the source",
    "6. no signal",
    "7. one quantum written once",
    "8. the handshake",
    "9. late settings",
)


def dot(u, v):
    return sum(a * b for a, b in zip(u, v, strict=True))


def tail(chi, dof):
    """A chi-square's upper tail at whole degrees of freedom: from one degree (erfc) or two (exp), two at a step."""
    y = chi / 2
    a, q = (1.0, math.exp(-y)) if dof % 2 == 0 else (0.5, math.erfc(math.sqrt(y)))
    while a < dof / 2:
        q += math.exp(a * math.log(y) - y - math.lgamma(a + 1)) if y > 0 else 0.0
        a += 1
    return q


def sign(take):
    """The part a take wrote along its frame: 1, -1, or 0 where the written reading is off the detector's axis."""
    frame, written = take["detector"]["spin"], take["written"]["spin"]
    return 1 if written == frame else -1 if written == [-c for c in frame] else 0


def nature(frames, signs):
    """Nature's joint law at the frames (rho, spin): the singlet's for two parties, GHZ's for three on the equator."""
    if len(frames) == 2:
        (r1, s1), (r2, s2) = frames
        return Fraction(r1 * r2 - signs[0] * signs[1] * dot(s1, s2), 4 * r1 * r2)
    if len(frames) == 3 and all(spin[2] == 0 for _, spin in frames):
        re, im, rho = 1, 0, 1
        for r, spin in frames:
            re, im, rho = re * spin[0] - im * spin[1], re * spin[1] + im * spin[0], rho * r
        return Fraction(rho + math.prod(signs) * re, 8 * rho)
    return None


def takes_by_birth(record):
    """The takes (whole clicks naming a birth, G5), by the birth's round and site and the train."""
    found = defaultdict(list)
    for take in record.of("whole"):
        if "birth" in take:
            found[(take["birth"][0], take["birth"][1], take["train"])].append(take)
    return found


def settings_by_source(record):
    """The births whose takes hold their frames, by train and detectors: per setting, the joint parts' counts."""
    found = defaultdict(lambda: defaultdict(Counter))
    for (_, _, train), takes in takes_by_birth(record).items():
        if all("detector" in t for t in takes):
            takes = sorted(takes, key=lambda t: t["site"])
            frames = tuple((t["detector"]["rho"], tuple(t["detector"]["spin"])) for t in takes)
            found[(train, tuple(t["site"] for t in takes))][frames][tuple(sign(t) for t in takes)] += 1
    return found


def combined(table, terms):
    """A sum of correlations, read from the counts and nature's at the same frames, with its standard error."""
    read, law, variance = Fraction(0), Fraction(0), 0.0
    for coefficient, frames in terms:
        counts = table.get(frames)
        laws = [nature(frames, signs) for signs in product((1, -1), repeat=len(frames))]
        if not counts or None in laws:
            return None
        n = sum(counts.values())
        e = Fraction(sum(math.prod(k) * v for k, v in counts.items()), n)
        read += coefficient * e
        law += coefficient * sum(
            math.prod(s) * p for s, p in zip(product((1, -1), repeat=len(frames)), laws, strict=True)
        )
        variance += float(1 - e * e) / n
    return read, law, math.sqrt(variance)


def arrangements(table, parties):
    """Bell's four arrangements for two parties, Mermin's eight for three, each party's two frames as its own."""
    own = [sorted({frames[k] for frames in table}) for k in range(parties)]
    if any(len(frames) != 2 for frames in own):
        return []
    if parties == 2:
        every = list(product(*own))
        return [[(-1 if pair == minus else 1, pair) for pair in every] for minus in every]
    found = []
    for order in product((0, 1), repeat=3):
        x = [own[k][order[k]] for k in range(3)]
        y = [own[k][1 - order[k]] for k in range(3)]
        found.append(
            [
                (1, (x[0], x[1], x[2])),
                (-1, (x[0], y[1], y[2])),
                (-1, (y[0], x[1], y[2])),
                (-1, (y[0], y[1], x[2])),
            ]
        )
    return found


def violation(record, parties, name):
    """S or M: the arrangement where nature's value is largest, read against the bound 2 and against nature's."""
    tables = [t for (_, sites), t in settings_by_source(record).items() if len(sites) == parties]
    if not tables:
        return NOT_READ, f"no birth with {parties} takes holding their frames"
    verdict, said = HOLDS, []
    for table in tables:
        values = [v for v in (combined(table, terms) for terms in arrangements(table, parties)) if v]
        if not values:
            return (
                NOT_READ,
                "a party with other than two frames, or frames nature's law here does not reach",
            )
        read, law, se = max(values, key=lambda v: abs(v[1]))
        past, at = abs(read) - 2 > Z_BOUND * se, abs(read - law) <= Z_BOUND * se
        verdict = verdict if past and at else FAILS
        said.append(
            f"{name} = {float(read):+.4f} +- {se:.4f} (nature's {law} = {float(law):+.4f}; "
            f"{'past' if past else 'NOT past'} the bound 2, {'at' if at else 'OFF'} nature's)"
        )
    return verdict, "; ".join(said)


def joint(record):
    """Per setting, the joint outcomes' counts against nature's law at those frames: one chi-square."""
    chi, dof, never, settings = 0.0, 0, 0, 0
    for table in settings_by_source(record).values():
        for frames, counts in table.items():
            n, settings = sum(counts.values()), settings + 1
            laws = {s: nature(frames, s) for s in product((1, -1), repeat=len(frames))}
            if None in laws.values():
                return NOT_READ, "frames nature's law here does not reach"
            never += sum(v for k, v in counts.items() if not laws.get(k))
            live = [s for s, p in laws.items() if p > 0]
            chi += sum(float((counts.get(s, 0) - n * laws[s]) ** 2 / (n * laws[s])) for s in live)
            dof += len(live) - 1
    if not settings:
        return NOT_READ, "no birth with takes holding their frames"
    odds = tail(chi, dof)
    verdict = HOLDS if never == 0 and odds >= ALPHA else FAILS
    said = f"chi-square {chi:.1f} on {dof} degrees over {settings} settings, its tail {odds:.2g}"
    return verdict, f"{said}; {never} clicks nature never makes"


def rank(weights, c):
    """The rank count: the running sums at or below c."""
    total, count = 0, 0
    for w in weights:
        total += w
        count += total <= c
    return count


def draws(record):
    """Every split click: room the sum of sigma_f sigma_b (sigma_b 1 where the line holds none), c below it, drawn
    the rank count of c."""
    lines = [e for e in record.of("split") if all(k in e for k in ("sizes", "c", "room", "drawn"))]
    if not lines:
        return NOT_READ, "no split click holds its sizes, c, room and drawn"
    off = 0
    for e in lines:
        back = e.get("back", [1] * len(e["sizes"]))
        products = [w * b for w, b in zip(e["sizes"], back, strict=False)]
        right = len(back) == len(e["sizes"]) and e["room"] == sum(products) and 0 <= e["c"] < e["room"]
        off += not (right and e["drawn"] == rank(products, e["c"]))
    with_back = sum("back" in e for e in lines)
    return (
        HOLDS if off == 0 else FAILS,
        f"{len(lines)} split clicks ({with_back} with sigma_b), {off} off law 9",
    )


def sizes(record):
    """At every source: sigma_f sigma_b over room is nature's law at the frames brought back; one quantum's alike."""
    sources = [e for e in record.of("split") if "frames" in e]
    if not sources:
        return NOT_READ, "no split click carries the frames brought back (one board)"
    off = 0
    for e in sources:
        back = e.get("back", [1] * len(e["sizes"]))
        frames = [(f["rho"], tuple(f["spin"])) for f in e["frames"] if "spin" in f]
        if len(frames) == len(e["frames"]):
            laws = [nature(frames, tuple(part)) for part in e["parts"]]
            off += any(
                p is None or Fraction(w * b, e["room"]) != p
                for w, b, p in zip(e["sizes"], back, laws, strict=True)
            )
        else:
            off += len(set(back)) != 1
    return (
        HOLDS if off == 0 else FAILS,
        f"{len(sources)} sources, {off} off nature's law at their frames",
    )


def marginals(record):
    """Each party's marginal, per own setting, against the other parties' settings: a chi-square of homogeneity
    for each party and own setting, the reading departing where any one does."""
    tests = []  # (tail, chi-square, degrees, the party's site, its own setting)
    for (_, sites), table in settings_by_source(record).items():
        for k in range(len(sites)):
            columns = defaultdict(lambda: defaultdict(lambda: [0, 0]))
            for frames, counts in table.items():
                for signs, v in counts.items():
                    columns[frames[k]][frames[:k] + frames[k + 1 :]][0 if signs[k] == 1 else 1] += v
            for own, others in columns.items():
                total, chi = sum(sum(c) for c in others.values()), 0.0
                rows = (sum(c[0] for c in others.values()), sum(c[1] for c in others.values()))
                for c in others.values():
                    for i, row in enumerate(rows):
                        expected = row * sum(c) / total
                        chi += (c[i] - expected) ** 2 / expected if expected else 0.0
                if len(others) > 1:
                    tests.append((tail(chi, len(others) - 1), chi, len(others) - 1, sites[k], own))
    if not tests:
        return NOT_READ, "no party seen against two settings of another"
    odds, chi, dof, place, own = min(tests)
    worst = f"the least tail {odds:.2g} (chi-square {chi:.1f} on {dof}, the party at site {place}, its frame {own})"
    return HOLDS if odds >= ALPHA else FAILS, f"{len(tests)} parties and own settings; {worst}"


def once(record):
    """A quantum with no frame (its takes hold none): the takes per birth, and g2 per pair of absorbers."""
    takes = takes_by_birth(record)
    trains = {k[2] for k, v in takes.items() if all("detector" not in t for t in v)}
    births = {
        (e["round"], e["site"], e["train"])
        for e in record.of("whole")
        if "birth" not in e and e["train"] in trains
    }
    if not births:
        return NOT_READ, "no birth of a quantum with no frame"
    orphans = sum(1 for k in takes if k[2] in trains and k not in births)
    per = Counter(len(takes.get(b, [])) for b in births)
    single, double = Counter(), Counter()
    for b in births:
        sites = sorted({t["site"] for t in takes.get(b, [])})
        single.update(sites)
        double.update(combinations(sites, 2))
    n = len(births)
    g2 = [
        f"{float(Fraction(double[p] * n, single[p[0]] * single[p[1]])):.3f}"
        for p in combinations(sorted(single), 2)
    ]
    shown = ", ".join(f"{taken} for {count}" for taken, count in sorted(per.items()))
    verdict = HOLDS if per == Counter({1: n}) and not orphans else FAILS
    said = f"{n} quanta, the takes per quantum {shown}; g2 per pair of absorbers {', '.join(g2)}"
    return verdict, f"{said}; {orphans} takes of no birth on the record"


def handshake(record):
    """Each source's frames brought back against its takes' frames, and its drawn part against what each wrote."""
    sources = {(e["round"], e["site"], e["train"]): e for e in record.of("split") if "frames" in e}
    if not sources:
        return NOT_READ, "no split click carries the frames brought back (one board)"
    takes, off = takes_by_birth(record), 0
    for place, e in sources.items():
        got = {t["site"]: t for t in takes.get(place, [])}
        ok = set(got) <= {f["site"] for f in e["frames"]}
        for f, entry in zip(e["frames"], e["parts"][e["drawn"]], strict=True):
            t = got.get(f["site"])
            if "spin" in f:
                ok = (
                    ok
                    and t is not None
                    and [t["detector"]["rho"], t["detector"]["spin"]] == [f["rho"], f["spin"]]
                )
                ok = ok and sign(t) == entry
            else:
                ok = ok and (t is not None) == (entry == 1)
        off += not ok
    return (
        HOLDS if off == 0 else FAILS,
        f"{len(sources)} sources, {off} whose takes differ from what was brought back",
    )


def late(record):
    """Each take's frame set by its detector's last choice before it, spacelike to the birth and to the other takes."""
    sides = record.header.get("sides")
    if record.header.get("order") != ORDER or not (isinstance(sides, list) and len(sides) == 3):
        return NOT_READ, "the header names no board the reader can place"

    def where(s):
        return s // (sides[1] * sides[2]), s // sides[2] % sides[1], s % sides[2]

    def apart(s1, s2):
        return sum(
            min(abs(a - b), n - abs(a - b)) for a, b, n in zip(where(s1), where(s2), sides, strict=True)
        )

    choices = defaultdict(list)
    for e in record.of("split"):
        if "axes" in e:
            choices[e["site"]].append((e["round"], e["axes"][e["drawn"]]))
    rounds = {s: [r for r, _ in made] for s, made in choices.items()}  # the events stand in round order
    groups = [v for v in takes_by_birth(record).values() if all("detector" in t for t in v)]
    if not groups or not choices:
        return NOT_READ, "no take holding its frame, or no setting chosen on the record"
    off = Counter()
    for (r0, s0), group in ((tuple(g[0]["birth"]), g) for g in groups):
        for t in group:
            i = bisect_left(rounds.get(t["site"], []), t["round"]) - 1
            if i < 0:
                off["no setting before its take"] += 1
                continue
            r1, axis = choices[t["site"]][i]
            off["the take's frame not its last setting"] += [axis["rho"], axis["spin"]] != [
                t["detector"]["rho"],
                t["detector"]["spin"],
            ]
            off["a setting inside the birth's light cone"] += abs(r1 - r0) >= apart(t["site"], s0)
            off["a setting inside another take's past light cone"] += sum(
                o is not t and o["round"] - r1 >= apart(t["site"], o["site"]) for o in group
            )
    found = {k: v for k, v in off.items() if v}
    takes = sum(len(g) for g in groups)
    said = "; ".join(f"{v} {k}" for k, v in found.items()) or "every one spacelike"
    return (FAILS if found else HOLDS), f"{takes} takes: {said}"


READINGS = (
    lambda r: violation(r, 2, "S"),
    lambda r: violation(r, 3, "M"),
    joint,
    draws,
    sizes,
    marginals,
    once,
    handshake,
    late,
)


def report(paths):
    """Each record read by the decoder's reader, then the nine readings, as one table and each value."""
    print(
        "B's record and the decoder's readings on it, from the record's lines alone (python -I b_record.py)"
    )
    print()
    results, causes = {}, {}
    for form, path in paths.items():
        record, cause = records.read(str(path))
        causes[form] = cause or "read"
        results[form] = [reading(record) for reading in READINGS] if record else None
    for form, path in paths.items():
        lines = len(path.read_text(encoding="utf-8").splitlines())
        print(f"{form}: {lines} lines, by the decoder's reader (schema 1.1's guards): {causes[form]}")
    print()
    print(f"{'reading':30s}" + "".join(f"{form:10s}" for form in paths))
    for n, name in enumerate(NAMES):
        print(f"{name:30s}" + "".join(f"{(results[f][n][0] if results[f] else '-'):10s}" for f in paths))
    for form in paths:
        print()
        print(f"{form}:")
        for name, (_, said) in zip(NAMES, results[form] or [], strict=False):
            print(f"  {name}: {said}")
