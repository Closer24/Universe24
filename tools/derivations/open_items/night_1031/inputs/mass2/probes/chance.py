"""MASS2 probe 3: the chance control for MASS1 3.5, by distinct products. Twelve integers of the structure, as MASS1
chose them (after its hit, the look-elsewhere effect named in the text):
  2 and 3 (the senses of an axis; the board's axes and a triangle's edges), 4 (G3/2's dimension), 6 (the Spokes),
  8 (the 8-gear train), 9 (L's order modulo 27), 10 (the discriminant's square-free part), 12 (T's rotations),
  16 (2^4), 24 (the 24), 38 (L's trace), 48 (the lifts).
It counts the multisets of at most three of them, their distinct products, the least and the most, and the distinct
products in every octave [2^j, 2^(j+1)). It prints no product: no product is picked or shown for its nearness to
anything. Whole numbers only; no float, root or logarithm (the e-folds are said in the text).
"""


def main() -> None:
    S = [2, 3, 4, 6, 8, 9, 10, 12, 16, 24, 38, 48]
    multisets = []
    for i in range(len(S)):
        multisets.append((S[i],))
        for j in range(i, len(S)):
            multisets.append((S[i], S[j]))
            for k in range(j, len(S)):
                multisets.append((S[i], S[j], S[k]))
    products = {}
    for m in multisets:
        v = 1
        for x in m:
            v = v * x
        products.setdefault(v, []).append(m)
    distinct = sorted(products)
    print("integers:", len(S), "| multisets of at most three:", len(multisets),
          "| of one, two, three:", sum(1 for m in multisets if len(m) == 1), sum(1 for m in multisets if len(m) == 2),
          sum(1 for m in multisets if len(m) == 3))
    print("distinct products:", len(distinct), "| the least:", distinct[0], "| the most:", distinct[-1],
          "| the most's bit length:", distinct[-1].bit_length())
    print("distinct products per octave [2^j, 2^(j+1)):")
    for j in range(distinct[-1].bit_length()):
        n = sum(1 for v in distinct if v.bit_length() == j + 1)
        print(f"  j = {j:2d}: {n}")
    most = max(len(r) for r in products.values())
    print("the most multisets one distinct product has:", most)


if __name__ == "__main__":
    main()
