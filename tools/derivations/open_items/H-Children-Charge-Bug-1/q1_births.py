"""Per birth of a record (the engine's own log, event birth): the two children's own Wronskian (the lay alone, on
nothing: sense A B at each end for child_at's lay (sense A, 0, 0, B); 0 for a merger's exact lay, one line moved),
the plane's Wronskian at each end before the lay (the standing levels, the log's `stood`), the record's Wronskian at
each end after the lay (the log's `W_children`, read by close.child_laid and merger.light_children from the board after
the lay), and the cross term between the child and the standing levels: W_after - W_stood - W_own.
Counts: births whose own W sums to 0; births whose after-lay W sums to 0; the sums with the sign.
Usage: q1_births.py <record.json>... (an engine run's output, run.py)."""
import json
import sys

from event_universe.core import rule3


def sign(x):
    return (x > 0) * 1 - (x < 0) * 1


def cross4(re_now, re_before, im_now, im_before):
    return re_now * im_before - im_now * re_before


for path in sys.argv[1:]:
    d = json.load(open(path))
    T = int(d["T"])
    A, B = rule3.balanced_pair(rule3.half(T))
    A, B = int(A), int(B)
    births = [e for e in d["log"] if e["event"] == "birth"]
    rows = []
    n_own_zero = n_after_zero = n_stood_zero = n_exact = 0
    sum_own = sum_after = sum_stood = sum_cross = 0
    sum_cross_parts = [0, 0]
    identity_fail = 0
    for b in births:
        exact = b.get("exact_lay") or [None, None]
        stood = b.get("stood", [[0, 0, 0, 0], [0, 0, 0, 0]])
        own, after, st, cr, parts = [], [], [], [], []
        for end, sense in ((0, -1), (1, 1)):
            re_n, re_b, im_n, im_b = (int(x) for x in stood[end])
            w_stood = cross4(re_n, re_b, im_n, im_b)
            w_after = int(b["W_children"][end])
            if exact[end] is None:
                w_own = sense * A * B
                # the cross term by the letter of child_at: sense A im_before + B re_now
                part = (sense * A * im_b, B * re_n)
                if w_after != w_stood + w_own + part[0] + part[1]:
                    identity_fail += 1
            else:
                w_own = 0
                part = (w_after - w_stood, 0)
                n_exact += 1
            own.append(w_own)
            after.append(w_after)
            st.append(w_stood)
            cr.append(w_after - w_stood - w_own)
            parts.append(part)
        n_own_zero += sum(own) == 0
        n_after_zero += sum(after) == 0
        n_stood_zero += sum(st) == 0
        sum_own += sum(own)
        sum_after += sum(after)
        sum_stood += sum(st)
        sum_cross += sum(cr)
        sum_cross_parts[0] += parts[0][0] + parts[1][0]
        sum_cross_parts[1] += parts[0][1] + parts[1][1]
        rows.append(
            dict(
                i=b["i"],
                node=b["node"],
                minus=b["minus"],
                plus=b["plus"],
                exact=exact,
                stood=stood,
                W_own=own,
                W_stood=st,
                W_after=after,
                cross=cr,
                sum_own=sum(own),
                sum_after=sum(after),
                signs_after=[sign(w) for w in after],
            )
        )
    summary = dict(
        record=path.split("/")[-1],
        intervals=d.get("intervals"),
        cube=d.get("cube"),
        run_back=d.get("run_back"),
        T=T,
        A=A,
        B=B,
        AB=A * B,
        births=len(births),
        exact_lays=n_exact,
        births_own_W_sum_zero=n_own_zero,
        births_after_W_sum_zero=n_after_zero,
        births_stood_W_sum_zero=n_stood_zero,
        SUM_W_own=sum_own,
        SUM_W_after=sum_after,
        SUM_W_stood=sum_stood,
        SUM_cross=sum_cross,
        SUM_cross_sense_A_im_before=sum_cross_parts[0],
        SUM_cross_B_re_now=sum_cross_parts[1],
        identity_failures=identity_fail,
        senses_sum_after=sum(s for r in rows for s in r["signs_after"]),
        children_W_after_zero=sum(1 for r in rows for s in r["signs_after"] if s == 0),
        counts=d.get("counts"),
    )
    print(json.dumps(summary))
    for r in rows:
        print(json.dumps(r))
