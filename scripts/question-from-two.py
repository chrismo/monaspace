"""Rebuild `question` in every master: top of that master's `two`, stem and dot of its own `?`.

Usage: python3 -I scripts/question-from-two.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
Run it on upstream's file: it reads the `?` it replaces, so a second run changes the shape again.
"""
import re
import sys

NODE = re.compile(r"^\((-?[\d.]+),(-?[\d.]+),(\w+)\),?$")


def glyph_block(lines, name):
    start = lines.index(f"glyphname = {name};")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("glyphname = "))
    return start, end


def first_shape_nodes(lines, start, end):
    layer = None
    i = start
    while i < end:
        m = re.match(r'^layerId = "([^"]+)";$', lines[i])
        if m:
            layer = m.group(1)
        if lines[i] == "nodes = (" and layer:
            j = i + 1
            while lines[j] != ");":
                j += 1
            yield layer, i + 1, j - 1
            layer = None
            i = j
        i += 1


def parse(lines, a, b):
    out = []
    for ln in lines[a:b + 1]:
        m = NODE.match(ln)
        if not m:
            raise ValueError(f"unexpected node line: {ln!r}")
        out.append((float(m.group(1)), float(m.group(2)), m.group(3)))
    return out


def fmt(v):
    return str(int(v)) if v == int(v) else f"{v:.2f}".rstrip("0").rstrip(".")


def build(q, t):
    assert len(q) == 23 and len(t) == 26, (len(q), len(t))
    def p(n, kind):
        return (n[0], n[1], kind)
    def shifted(n, frm, to):
        return (n[0] + to[0] - frm[0], n[1] + to[1] - frm[1], "o")
    return [
        q[0],                                          # open corner into the stem, as drawn
        q[1], shifted(q[2], q[3], t[2]), p(t[2], "cs"),  # ?'s lower outer curve onto 2's outer right
        p(t[1], "o"), p(t[0], "o"), p(t[25], "cs"),    # 2's outer top
        p(t[24], "o"), p(t[23], "o"), p(t[22], "c"),
        p(t[21], "l"),                                 # 2's terminal cut
        p(t[20], "o"), p(t[19], "o"), p(t[18], "cs"),  # 2's inner top
        p(t[17], "o"), p(t[16], "o"), p(t[15], "cs"),
        shifted(q[17], q[16], t[15]), q[18], q[19],    # ?'s inner curve into the stem
        q[20], q[21], q[22],
    ]


def main(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    qs, qe = glyph_block(lines, "question")
    ts, te = glyph_block(lines, "two")
    twos = {lid: parse(lines, a, b) for lid, a, b in first_shape_nodes(lines, ts, te)}
    edits = []
    for lid, a, b in first_shape_nodes(lines, qs, qe):
        new = build(parse(lines, a, b), twos[lid])
        text = [f"({fmt(x)},{fmt(y)},{k})," for x, y, k in new]
        text[-1] = text[-1].rstrip(",")
        edits.append((a, b, text))
    if len(edits) != 8:
        sys.exit(f"expected 8 master layers, found {len(edits)}")
    for a, b, text in sorted(edits, reverse=True):
        lines[a:b + 1] = text
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"rebuilt question in {len(edits)} layers")


if __name__ == "__main__":
    main(sys.argv[1])
