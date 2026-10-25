"""ws1's INSTRUMENTED COPY of the engine (engine-5.0-test b9cec88e0): src/event_universe copied whole to src_ws1/event_universe and two files
changed by exact text replacements, each named below (the script refuses where a replacement does not match exactly once); src is never edited.
The instrument reads and never acts: (1) node.swap reads, at every turned Node and every plane with a gap, W of the held pre-state (W_pre),
W of the step's output the swap discards (W_post) and W after the exchange (W_after), and counts kept / negated / changed against W_pre;
(2) interval.close reads the board's W of the planes with a gap at four points of the interval: W0 the pre-state (held), W1 after the step
(set_rows and the frozen restore), W2 after the swap, W3 after the click; and the births and credits of the interval. Run: python make_src_ws1.py"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "src", "event_universe")
DST_ROOT = os.path.join(HERE, "src_ws1")
DST = os.path.join(DST_ROOT, "event_universe")
if os.path.isdir(DST_ROOT):
    shutil.rmtree(DST_ROOT)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__"))


def patch(path, replacements):
    text = open(path, encoding="utf-8").read()
    for old, new in replacements:
        if text.count(old) != 1:
            raise SystemExit(f"replacement matches {text.count(old)} times in {path}, refused:\n{old}")
        text = text.replace(old, new)
    open(path, "w", encoding="utf-8").write(text)


# node.py: the swap's reading at the turned Nodes
patch(os.path.join(DST, "node.py"), [
    ('"""The generic Node (the owner\'s word of 2026-10-25',
     '"""ws1\'s INSTRUMENTED COPY (2026-10-25, make_src_ws1.py names every delta; src untouched). The generic Node (the owner\'s word of 2026-10-25'),
    ("from event_universe.links import Link, turn_pair\n",
     "from event_universe.links import Link, turn_pair, wronskian\n"),
    ('        self.stepped: list[list[Line]] = []\n\n        gamma, action = self.gamma, self.T',
     '        self.stepped: list[list[Line]] = []\n'
     '        self.wcounts: dict[str, int] = {"sites": 0, "kept": 0, "negated": 0, "changed": 0, "kept_zero": 0, "post_equal_pre": 0, "nodes": 0, "node_sum_kept": 0, "sum_pre": 0, "sum_post": 0, "sum_after": 0}  # ws1\n'
     '        self.wlog: list[list[int]] = []  # ws1: per interval [i, w0 pre, w1 step, w2 swap, w3 click, turned, births, credits, frozen]\n\n        gamma, action = self.gamma, self.T'),
    ("            self.exchange(top, held)\n        return top",
     "            self.exchange_read(top, held)  # ws1: the exchange with its reading\n        return top\n\n"
     "    def gapped_indices(self) -> list[int]:\n"
     '        """ws1: the rows\' indices of the planes with a gap."""\n'
     "        return [k for k, r in enumerate(self.rows_) if r.shape == PLANE and r.gap]\n\n"
     "    def exchange_read(self, top: Any, held: list[list[Line]]) -> None:\n"
     '        """ws1: W at the turned Nodes before (the held pre-state), the step\'s output the swap discards, and after the exchange; counted."""\n'
     "        ks = self.gapped_indices()\n"
     "        rows = self.rows()\n"
     "        pre = [wronskian(*held[k]) for k in ks]\n"
     "        post = [wronskian(*rows[k]) for k in ks]\n"
     "        self.exchange(top, held)\n"
     "        rows = self.rows()\n"
     "        after = [wronskian(*rows[k]) for k in ks]\n"
     "        c = self.wcounts\n"
     "        where = list(zip(*np.nonzero(top), strict=True))\n"
     "        c['nodes'] += len(where)\n"
     "        for at in where:\n"
     "            node_pre = node_after = 0\n"
     "            for a, b, d in zip(pre, post, after, strict=True):\n"
     "                wp, wq, wa = int(a[at]), int(b[at]), int(d[at])\n"
     "                c['sites'] += 1\n"
     "                c['sum_pre'] += wp\n"
     "                c['sum_post'] += wq\n"
     "                c['sum_after'] += wa\n"
     "                node_pre += wp\n"
     "                node_after += wa\n"
     "                if wa == wp:\n"
     "                    c['kept'] += 1\n"
     "                    if wp == 0:\n"
     "                        c['kept_zero'] += 1\n"
     "                elif wa == -wp:\n"
     "                    c['negated'] += 1\n"
     "                else:\n"
     "                    c['changed'] += 1\n"
     "                if wq == wp:\n"
     "                    c['post_equal_pre'] += 1\n"
     "            if node_after == node_pre:\n"
     "                c['node_sum_kept'] += 1\n"),
])

# interval.py: the board's W at four points of the interval
patch(os.path.join(DST, "interval.py"), [
    ('"""The interval, the Node\'s one program',
     '"""ws1\'s INSTRUMENTED COPY (2026-10-25, make_src_ws1.py names every delta; src untouched). The interval, the Node\'s one program'),
    ("        top = node.swap(self.held, self.frozen)\n        log_from = len(node.log)\n        node.click(self.plane_starts, self.held)\n",
     "        ks = node.gapped_indices()  # ws1: the reading at four points\n"
     "        total = lambda rows: int(sum(int(x) for k in ks for x in wronskian(*rows[k]).reshape(-1)))\n"
     "        w0, w1 = total(self.held), total(node.rows())\n"
     "        births0, credits0 = node.counts['births'], node.counts['body_clicks']\n"
     "        top = node.swap(self.held, self.frozen)\n"
     "        w2 = total(node.rows())\n"
     "        log_from = len(node.log)\n"
     "        node.click(self.plane_starts, self.held)\n"
     "        w3 = total(node.rows())\n"
     "        node.wlog.append([node.interval, w0, w1, w2, w3, int(top.sum()), node.counts['births'] - births0, node.counts['body_clicks'] - credits0, int(self.frozen.sum())])\n"),
])
print("written", DST)
