"""End the `&` top loop in each master's `S` top arm, stretched to the loop's old reach.

Usage: python3 -I scripts/ampersand-from-s.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
Safe to rerun: the arm reaches the x where the terminal already is.
"""
import re
import sys

NODE = re.compile(r"^\((-?[\d.]+),(-?[\d.]+),(\w+)\),?$")
GLYPHS = ["ampersand", "ampersand.init", "ampersand.left", "ampersand.right", "ampersand.both"]


def glyph_block(lines, name):
    start = lines.index(f"glyphname = {name};")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("glyphname = "))
    return start, end


def layer_paths(lines, start, end):
    """{layerId: [(first node line, last node line), ...]}"""
    out = {}
    layer = None
    for i in range(start, end):
        m = re.match(r'^layerId = "([^"]+)";$', lines[i])
        if m:
            layer = m.group(1)
            out[layer] = []
        elif lines[i] == "nodes = (" and layer:
            j = lines.index(");", i)
            out[layer].append((i + 1, j - 1))
    return out


def parse(lines, a, b):
    out = []
    for ln in lines[a:b + 1]:
        m = NODE.match(ln)
        if not m:
            raise ValueError(f"unexpected node line: {ln!r}")
        out.append((float(m.group(1)), float(m.group(2)), m.group(3)))
    return out


def fmt(v):
    v = round(v, 1)
    return str(int(v)) if v == int(v) else str(v)


def build(q, s):
    """q: the & top loop (22 nodes); s: the S (44 nodes).

    S: 0 outer terminal, 1-2 handles, 3 outer top; 40 inner top, 41-42 handles, 43 inner terminal.
    q: 2 outer top, 17 inner top, 20 inner terminal, 21 outer terminal.
    """
    assert len(q) == 22 and q[20][2] == "c" and q[21][2] == "l", "unexpected & loop"
    assert len(s) == 44 and s[0][2] == "l" and s[43][2] == "c", "unexpected S"

    def vec(a, b, k=1.0):
        return ((b[0] - a[0]) * k, (b[1] - a[1]) * k)

    def add(p, v):
        return (p[0] + v[0], p[1] + v[1])

    top, itop = q[2], q[17]
    arm = vec(s[3], s[0])
    k = (q[21][0] - top[0]) / arm[0]
    ot = add(top, vec(s[3], s[0], k))
    stroke = (top[1] - itop[1]) / (s[3][1] - s[40][1])
    it = add(ot, vec(s[0], s[43], stroke))
    r = (it[0] - itop[0]) / (s[43][0] - s[40][0])
    return (
        [(*add(ot, vec(s[0], s[1], k)), "o"), (*add(top, vec(s[3], s[2], k)), "o")]
        + q[2:18]
        + [(*add(itop, vec(s[40], s[41], r)), "o"), (*add(it, vec(s[43], s[42], r)), "o"),
           (*it, "c"), (*ot, "l")]
    )


def main(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    s_nodes = {}
    for lid, paths in layer_paths(lines, *glyph_block(lines, "S")).items():
        if len(paths) != 1:
            sys.exit(f"S layer {lid} has {len(paths)} paths, expected 1")
        s_nodes[lid] = parse(lines, *paths[0])

    edits = []
    for glyph in GLYPHS:
        layers = layer_paths(lines, *glyph_block(lines, glyph))
        if set(layers) != set(s_nodes):
            sys.exit(f"{glyph} masters differ from S masters")
        for lid, paths in layers.items():
            if len(paths) != 2:
                sys.exit(f"{glyph} layer {lid} has {len(paths)} paths, expected 2")
            a, b = paths[1]
            text = [f"({fmt(x)},{fmt(y)},{t})," for x, y, t in build(parse(lines, a, b), s_nodes[lid])]
            text[-1] = text[-1].rstrip(",")
            edits.append((a, b, text))
    for a, b, text in sorted(edits, reverse=True):
        lines[a:b + 1] = text
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"rebuilt the & top loop in {len(edits)} layers")


if __name__ == "__main__":
    main(sys.argv[1])
