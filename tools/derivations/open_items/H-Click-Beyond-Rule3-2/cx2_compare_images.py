"""H-Click-Beyond-Rule3-2: two readings of one world (the base and an image carried back) compared Link by Link: the + end (same or exchanged), the plane born (the digit), the refusal's share and verdict; the first interval apart per reading. Usage: python cx2_compare_images.py base.json image.json"""
import json
import sys


def link_key(r):
    return (r["i"], frozenset(map(tuple, r["link"])), r["rec"])


def main(a, b):
    b0, b1 = json.load(open(a)), json.load(open(b))
    m0 = {link_key(r): r for r in b0["births"]}
    m1 = {link_key(r): r for r in b1["births"]}
    common = sorted(set(m0) & set(m1), key=lambda k: k[0])
    found = {
        "links_base": len(m0), "links_image": len(m1), "links_common": len(common),
        "first_link_only_one_side": min([k[0] for k in set(m0) ^ set(m1)] or [None]),
        "plus_same": sum(1 for k in common if m0[k]["plus_head"] == m1[k]["plus_head"]),
        "plus_exchanged": sum(1 for k in common if m0[k]["plus_head"] != m1[k]["plus_head"]),
        "first_plus_same": min([k[0] for k in common if m0[k]["plus_head"] == m1[k]["plus_head"]] or [None]),
        "h_negated": sum(1 for k in common if m0[k]["h_sign"] == -m1[k]["h_sign"]),
        "plane_same": sum(1 for k in common if m0[k]["plane_head"] == m1[k]["plane_head"]),
        "first_plane_apart": min([k[0] for k in common if m0[k]["plane_head"] != m1[k]["plane_head"]] or [None]),
        "number_same": sum(1 for k in common if m0[k]["number"] == m1[k]["number"]),
        "first_number_apart": min([k[0] for k in common if m0[k]["number"] != m1[k]["number"]] or [None]),
        "flow_sign_same": sum(1 for k in common if m0[k]["flow_sign"] == m1[k]["flow_sign"]),
    }
    r0 = {(r["i"], r["plane"], frozenset(map(tuple, (r["minus"], r["plus"])))): r for r in b0["refusals"]}
    r1 = {(r["i"], r["plane"], frozenset(map(tuple, (r["minus"], r["plus"])))): r for r in b1["refusals"]}
    rc = sorted(set(r0) & set(r1), key=lambda k: k[0])
    found.update({
        "refusals_common": len(rc), "refusals_base": len(r0), "refusals_image": len(r1),
        "owns_same": sum(1 for k in rc if sorted(r0[k]["owns"]) == sorted(r1[k]["owns"])),
        "first_owns_apart": min([k[0] for k in rc if sorted(r0[k]["owns"]) != sorted(r1[k]["owns"])] or [None]),
        "kept_same": sum(1 for k in rc if r0[k].get("kept") == r1[k].get("kept")),
        "first_kept_apart": min([k[0] for k in rc if r0[k].get("kept") != r1[k].get("kept")] or [None]),
        "first_refusal_only_one_side": min([k[0] for k in set(r0) ^ set(r1)] or [None]),
    })
    print(json.dumps(found))


main(sys.argv[1], sys.argv[2])
