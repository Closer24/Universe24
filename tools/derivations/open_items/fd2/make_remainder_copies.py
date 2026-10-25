"""The one rule of the remainder tried on David's toy (the owner's word relayed by the Boss, 2026-10-25): three further flagged copies from toy_david/lean_full.py, each one exact text replacement asserted once, written here and never by hand:
  toy_r_odd/      the turn's rounding of a signed arrival odd (half away from zero, paces.odd_rounded) in place of half up: the one rule's mirrored birth of a dropped remainder;
  toy_r_imcomp/   every remainder mirrored at the turn, the im line's rotation remainder too (David keeps it): the one rule's mirror on every kept remainder;
  toy_r_fold/     the folded digit (the control key digits = folded) read even under the law's mirror, min(r, w - 1 - r) over w div 2 classes, in place of David's min(r, w - r) over w div 2 + 1.
Run: python make_remainder_copies.py"""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'toy_david')
text = open(os.path.join(SRC, 'lean_full.py')).read()
copies = {
 'toy_r_odd': [("        a_re, a_im = (2 * a_re + self.X) // (2 * self.X), (2 * a_im + self.X) // (2 * self.X)\n        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)\n        return [(2 * b_re + tw) // (2 * tw), (2 * b_im + tw) // (2 * tw)]",
                "        a_re, a_im = paces.odd_rounded(a_re, self.X), paces.odd_rounded(a_im, self.X)  # fd2 R-odd: the signed coefficient's rounding half away from zero (the mirrored birth of the dropped remainder)\n        b_re = (tc * a_re - ts * a_im); b_im = (ts * a_re + tc * a_im)\n        return [paces.odd_rounded(b_re, tw), paces.odd_rounded(b_im, tw)]")],
 'toy_r_imcomp': [("np.where(top, h.rem if im else h.wall - 1 - h.rem, line.rem)", "np.where(top, h.wall - 1 - h.rem, line.rem)  # fd2 R-imcomp: every remainder mirrored at the turn, the im line's too")],
 'toy_r_fold': [("if self.control.get('digits') == 'folded': rem = min(rem, wl - rem); values = values // 2 + 1", "if self.control.get('digits') == 'folded': rem = min(rem, wl - 1 - rem); values = values // 2  # fd2 R-fold: the digit even under the law's mirror r -> w - 1 - r, w div 2 classes")],
}
for name, reps in copies.items():
    out = text
    for old, new in reps:
        if out.count(old) != 1: sys.exit('refused (%s): %d matches: %r' % (name, out.count(old), old[:80]))
        out = out.replace(old, new)
    dst = os.path.join(HERE, name); os.makedirs(dst, exist_ok=True)
    open(os.path.join(dst, 'lean_full.py'), 'w').write(out)
    for f in os.listdir(SRC):
        if f.endswith('.json') or f in ('runback_test.py', 'cube48_test.py', 'decoder_full.py'): shutil.copy(os.path.join(SRC, f), os.path.join(dst, f))
    print('written', name)
