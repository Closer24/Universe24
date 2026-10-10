"""The paper's words: the forbidden lists (the program's internal words, proof words, names outside the citations, words about the tool that wrote nothing here, root signs, 'in nature' beyond the three sentences that carry it, 'coin' beyond the slot image, 'window'), the claim sentence present once and whole, the nature sentence once, the three open sentences once each, the ledger sentence at most once in the body, the phrases the owner struck ('readings of the first paper', 'unchecked', 'in short' and the like) absent, the status words present and in square brackets only in the Conclusion's list, a source sentence before every displayed equation, no wave word in the clocks' section and 'wave' there only in its one closing clause, the body ending by page 14, the Abstract under 200 words and 1,920 characters with no macro. Usage: python3 check_words.py [arrow.pdf] [abstract word limit, 200 unless given]."""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PAPER, abstract_of, body_of, plain, read_tex, sections_of

INTERNAL = ["notebook", "face", "front", "credit line", "lay line", "re-lay", "wall", "Gamma", "engine", "window", "seed", "generator", "blind", "twin", "ball", "hull", "shell", "presented", "crossed", "Rule3", "W_rec", "walls", "one_photon", "back_in_time", "engine-v2", "lattice", "quantum", "sqrt"]
INTERNAL_OK = {"seed": ["toss's seed", "the seed, the number that fixes"], "ball": ["balls colliding", "wiped ball", "the ball filled", "the ball fills", "the ball growing", "a ball, counted", "a ball counted", "outside the ball", "the ball within"], "front": ["front and back"], "face": ["face diagonal"], "shell": ["shells"], "quantum": ["quantum physics", "quantum systems", "not a quantum system", "quantum mechanics"]}
PROOF = ["theorem", "prove", "proof", "proves", "bijection", "lemma", "corollary"]
NAMES = ["Loschmidt", "Boltzmann", "Landauer", "Bennett", "Zurek", "Maccone", "Rovelli", "Ghirardi", "Rimini", "Weber", "Penrose", "Zuse", "Toffoli", "Margolus", "Fredkin", "Hooft", "Wolfram", "Tegmark", "Einstein", "Michelson", "Morley", "Brecher", "Pound", "Rebka", "Ives", "Stilwell", "Hafele", "Keating", "Dyson", "Eddington", "Davidson", "Shapiro", "Newton", "Planck", "Born", "Lorentz", "Maxwell", "Schr"]
AI = ["AI", "model", "Claude", "Anthropic", "language model", "assist", "LLM"]
CLAIM = "A board of Nodes, each speaking only with its six neighbours once per tick and stepped by one whole-number rule, has no direction of time: every step runs back exactly. The direction appears only where detectors we place click: the wiping removes the piece's numbers, and for anyone without a record of them (in the run, our log) the backward run fails where the wiping reached; the failure has a place, a speed never above one step per tick, and a size, a count of whole numbers. By the rule no body forgets."
NATURE = "If the world is built as such a board, this is where the direction of time in nature comes from: not in the law, but in the ledger of what was measured. We propose that it is so."
POSTULATES = ["Nature is discrete: a board of events", "once per tick and writes only itself; nothing passes faster than one step per tick", "What we see is clicks, not the board", "Every number at a Node is a whole number", "one simple act, the step of equation", "Light is the kind with the top equal to the bottom", "One kind, gravity, has a content at the Node", "The click, put in by hand"]
REPO_SENTENCE = "Everything here is in the public repository and can be run by anyone."
LAST_CLAUSE = "is what we call entanglement on the board."
PAGE_LIMIT = 18  # the owner's yes to the table of symbols (the owner: "a table of symbols, in my view yes") allowed page 16; the table took four fifths of a page, not half, and the external review's items a further half page; the editor asked for page 17 after its cuts of round 12, and 18 if the round's additions (the momentum paragraph in full, the three bursts, the clocks' largest numbers) did not let it hold: the body ends a third of a page into 18, so 18 stands here pending the owner's word; before the table the owner's rule was page 14, then 15 with the ensemble over seeds and the gathered open paragraph (round 8)  # the owner's rule: the body may run to page 14; shorten only where a sentence is uninteresting (the owner: "cut pages only where it can be done and where there are things of no interest")
OPEN = ["The detector is placed by us, its reset after a click and the keeping of its record ours too, outside the board; in nature the detector is a body on the board and keeps the rule, so nothing it does outruns light, and what it does in detail is not built here.", "What a moving body reads with a ruler of its own, the two-way sameness that was measured \\cite{michelson1887}, and what it reads of light from one side, and what a body standing in the content reads of light with its own clock and its own ruler, are not shown here; the one-side reading depends on the matter pair, and we do not settle it here.", "Whether a body keeps its own record we do not know."]
LEDGER = "the ledger of what was measured"
AI_DECLARATION = "\\bmhead{Use of AI tools} The author used AI tools in preparing this manuscript, under the author's direction and review; the author takes full responsibility for its content."
LIMITS = ["not shown here", "not done here", "we do not know", "we do not say", "not counted on the board", "not set here", "is not shown", "we have not", "not settle", "not built here"]  # allowed in the paragraph "What is open" alone
ENTANGLEMENT = "A classical piece is as exclusive; whether the tie gives the correlations that in nature tell entanglement from a shared piece we have not tested."
GONE = ["reading of the first paper", "readings of the first paper", "unchecked", "not refereed", "not checked here", "in short", "note that", "remarkabl", "it is important", "simply put", "whole paper in", "five sentences", "that is the whole", "exactly this"]
WAVE_WORDS = ["wave number", "dispersion", "phase", "frequency", "group velocity", "wavelength"]
WAVE_CLAUSE = "seen from far, the pattern looks like a wave"
STATUS_WORDS = ["the rule's definition", "follows from the rule", "counted on the board", "we propose"]
SOURCE_VERB = r"\b(from|by|says|gives|give)\b"
SOURCE_NOUN = r"\b(rule|rule's|Node|Node's|definition|measured|books|equation|detector's|hand)\b"
STATUS_BRACKET = r"\[(the rule's definition|derived|computed|checked|shown|proposed|put in)[^\]]*\]"
TITLE = "A discrete spacetime of events in whole numbers: why clocks slow, why nothing outruns light, and why time has a direction only where something was measured"
RUNNING_HEAD = "\\title[A discrete spacetime of events in whole numbers]"


def count_word(text: str, word: str) -> int:
    return len(re.findall(r"(?<![A-Za-z_])" + re.escape(word) + r"(?![A-Za-z_])", text, flags=re.I))


def main(argv: list[str]) -> int:
    tex = read_tex()
    body_tex = body_of(tex)
    body = plain(body_tex)
    whole = plain(tex)
    cited_removed = re.sub(r"\\cite\{[^}]*\}", "", tex)
    musts, notes = [], []
    for w in INTERNAL:
        n = count_word(whole, w)
        ok = INTERNAL_OK.get(w, [])
        n_ok = sum(len(re.findall(re.escape(phrase), whole, flags=re.I)) for phrase in ok)
        if n - n_ok > 0:
            musts.append(f"internal word '{w}': {n - n_ok} use(s) beyond the allowed phrases")
    for w in PROOF:
        if count_word(whole, w):
            musts.append(f"proof word '{w}': {count_word(whole, w)}")
    for w in NAMES:
        if count_word(plain(cited_removed), w):
            musts.append(f"name outside a citation: '{w}' x {count_word(plain(cited_removed), w)}")
    for w in AI:
        for fname in ("arrow.tex", "figures.tex", "refs.bib", "refs_more.bib"):
            text = (PAPER / fname).read_text(encoding="utf-8")
            if fname == "arrow.tex":
                text = text.replace(AI_DECLARATION, " ")  # the one sentence the journal requires, in the Declarations alone
                if text.count("\\bmhead{Use of AI tools}") or tex.count(AI_DECLARATION) != 1 or AI_DECLARATION not in tex[tex.index("\\section*{Statements and Declarations}"):]:
                    musts.append("the declaration of AI use is not the one sentence in the Declarations")
            n = len(re.findall(r"(?<![A-Za-z_])" + re.escape(w) + r"(?![A-Za-z_])", text)) if w.isupper() else count_word(text, w)
            if n:
                musts.append(f"'{w}' in {fname} x {n}")
    for g in GONE:
        n = len(re.findall(re.escape(g), whole, flags=re.I))
        if n:
            musts.append(f"a phrase that left the paper: '{g}' x {n}")
    secs = sections_of(tex)
    for name, text in secs.items():
        if name != "Conclusion":
            n_br = len(re.findall(STATUS_BRACKET, plain(text)))
            if n_br:
                musts.append(f"a status in square brackets inside the prose of '{name}': {n_br}; the brackets belong to the Conclusion's list only")
    for sw in STATUS_WORDS:
        if sw not in body:
            musts.append(f"the status words '{sw}' are missing from the body")
    # a source sentence before every displayed equation: the last two sentences of the paragraph before it name where it comes from
    src_lines = tex.splitlines()
    for k, line in enumerate(src_lines):
        if line.startswith("\\begin{equation}"):
            before = plain(src_lines[k - 1])
            tail = " ".join(re.split(r"(?<=[.;:])\s+", before.strip())[-2:])
            if not (re.search(SOURCE_VERB, tail) and re.search(SOURCE_NOUN, tail)):
                musts.append(f"the equation at line {k + 1} has no source sentence before it (one with 'from', 'by', 'says' or 'gives' and the rule's, the Node's, the books' or the measurement's name)")
    time_sec = plain(secs["What time is on the board"])
    for wv in WAVE_WORDS:
        if count_word(time_sec, wv) or (wv == "wave number" and re.search(r"\bk\b", time_sec)):
            musts.append(f"a wave word in the clocks' section: '{wv}'")
    n_wave = count_word(time_sec, "wave")
    if n_wave != 1 or WAVE_CLAUSE not in time_sec:
        musts.append(f"'wave' in the clocks' section {n_wave} time(s); once, in '{WAVE_CLAUSE}'")
    if "\u221a" in whole or re.search(r"square root", whole, re.I):
        musts.append("a root sign or 'square root'")
    n_nature = len(re.findall(r"in nature", whole))
    if n_nature != 3:
        musts.append(f"'in nature' appears {n_nature} times; three are mandated (the nature sentence, the detector's open sentence, the entanglement sentence)")
    n_coin = count_word(whole, "coin")
    if n_coin:
        notes.append(f"'coin' appears {n_coin} time(s); allowed only in the slot image")
    if count_word(whole, "window"):
        musts.append("'window' used")
    def once(sentence: str, where: str, label: str, at_most: bool = False):
        n = where.count(sentence)
        if at_most and n > 1:
            musts.append(f"{label}: {n} times, at most once allowed")
        elif not at_most and n != 1:
            musts.append(f"{label}: found {n} times, once required")
    once(CLAIM, body, "the claim sentence (verbatim)")
    once(ENTANGLEMENT, body, "the entanglement sentence (the owner's, before the tie sentence)")
    if CLAIM not in plain(sections_of(tex)["Conclusion"]):
        musts.append("the claim sentence is not in the Conclusion")
    once(NATURE, body, "the nature sentence")
    for i, o in enumerate(OPEN, 1):
        once(re.sub(r" +", " ", plain(o)), body, f"open sentence {i}")  # the sentence read as plain() reads the body, its mathematics stripped the same way
    once(LEDGER, body, "the ledger sentence in the body", at_most=True)
    # the owner's word: every limitation sentence in the one section "What is open" (Section 6, before the Conclusion), the rest of the text without them
    open_par = re.search(r"\\section\{What is open\}\\label\{sec:open\}.*?(?=\\section\{)", tex, flags=re.S)
    rest = plain(tex.replace(open_par.group(0), " ")) if open_par else body
    rest = rest.replace("the direction of the burst on the board we do not know", " ")  # the owner: it stays in Section 5, the reason for the two numbers, not a limitation
    for phrase in LIMITS:
        n = len(re.findall(re.escape(phrase), rest))
        if n:
            musts.append(f"a limitation outside the section 'What is open': '{phrase}' x {n}")
    if open_par is None:
        musts.append("no section 'What is open'")
    if TITLE not in tex:
        musts.append("the title is not the owner's")
    if RUNNING_HEAD not in tex:
        musts.append("the running head is not the owner's")
    # the abstract
    abstract = abstract_of(tex)
    words = len(abstract.split())
    limit = int(argv[2]) if len(argv) > 2 else 200
    if words > limit:
        musts.append(f"the Abstract has {words} words (limit {limit})")
    if len(abstract) > 1920:
        musts.append(f"the Abstract has {len(abstract)} characters (limit 1,920)")
    for ph in POSTULATES:
        if ph not in body:
            musts.append(f"an assumption of Section 2 is missing: '{ph}'")
    if REPO_SENTENCE not in abstract:
        musts.append("the Abstract must end with the sentence that everything can be checked and rerun")
    if "no faster than" not in abstract:
        musts.append("the Abstract must say the failure spreads 'no faster than' the wiping's pace (the ends moved 60 and 8 Nodes in 171 ticks)")
    if "\\" in abstract or "$" in abstract:
        musts.append("the Abstract holds a macro or a formula")
    # the body ends by page 14 (the owner's rule): the Conclusion's last sentence on a page no later than 14
    pdf = Path(argv[1]) if len(argv) > 1 else PAPER / "arrow.pdf"
    if pdf.exists():
        last_page = None
        for pg in range(1, 24):
            text_pg = subprocess.run(["pdftotext", "-f", str(pg), "-l", str(pg), str(pdf), "-"], capture_output=True, text=True).stdout
            if not text_pg.strip():
                break
            if LAST_CLAUSE in re.sub(r"\s+", " ", text_pg):  # the page's line breaks folded  # the last clause of the Conclusion's last sentence, short enough not to break across a line; the last page that holds it (Section 3 says it once too)
                last_page = pg
        if last_page is None or last_page > PAGE_LIMIT:
            musts.append(f"the body does not end by page {PAGE_LIMIT} (the Conclusion's last sentence is on page {last_page})")
    else:
        notes.append("no PDF to check the page count")
    print(f"check_words: Abstract {words} words, {len(abstract)} characters; 'in nature' {n_nature}; ledger in body {body.count(LEDGER)}")
    for n in notes:
        print("  note: " + n)
    if musts:
        print("MUST:")
        for m in musts:
            print("  " + m)
        return 1
    print("the words pass")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
