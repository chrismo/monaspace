"""Rebuild `%` in every master: rings from that master's `zero.numr`/`zero.dnom` (no dot,
counter shrunk 20% for weight), slash widened to the weight of its `/`.

Usage: python3 -I scripts/percent-from-zero.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
Safe to rerun: rings land where the old ones were, and a slash already at `/` weight stays put.
"""
import re
import sys

NODE = re.compile(r"^\((-?[\d.]+),(-?[\d.]+),(\w+)\),?$")
GLYPHS = ["percent", "percent.left", "percent.right", "percent.both"]
COUNTER = 0.8


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


def shapes_of(lines, name):
    return {lid: [parse(lines, a, b) for a, b in ps] for lid, ps in layer_paths(lines, *glyph_block(lines, name)).items()}


def fmt(v):
    v = round(v, 1)
    return str(int(v)) if v == int(v) else str(v)


def bbox(ns):
    xs, ys = [n[0] for n in ns], [n[1] for n in ns]
    return min(xs), min(ys), max(xs), max(ys)


def ring(old_outer, zero, anchor):
    """Zero's outer and shrunk inner contour, centred on the old ring and aligned at its top or bottom."""
    ox0, oy0, ox1, oy1 = bbox(old_outer)
    zx0, zy0, zx1, zy1 = bbox(zero[0])
    dx = (ox0 + ox1 - zx0 - zx1) / 2
    dy = oy1 - zy1 if anchor == "top" else oy0 - zy0
    ix0, iy0, ix1, iy1 = bbox(zero[1])
    cx, cy = (ix0 + ix1) / 2, (iy0 + iy1) / 2
    inner = [(cx + (x - cx) * COUNTER, cy + (y - cy) * COUNTER, t) for x, y, t in zero[1]]
    return [[(x + dx, y + dy, t) for x, y, t in c] for c in (zero[0], inner)]


def widened(bar, slash):
    """Bar nodes run top-right, top-left, bottom-left, bottom-right, as in `slash`."""
    grow = ((slash[0][0] - slash[1][0]) - (bar[0][0] - bar[1][0])) / 2
    return [(bar[0][0] + grow, bar[0][1], "l"), (bar[1][0] - grow, bar[1][1], "l"),
            (bar[2][0] - grow, bar[2][1], "l"), (bar[3][0] + grow, bar[3][1], "l")]


def main(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    numr, dnom, slash = shapes_of(lines, "zero.numr"), shapes_of(lines, "zero.dnom"), shapes_of(lines, "slash")
    edits = []
    for glyph in GLYPHS:
        layers = layer_paths(lines, *glyph_block(lines, glyph))
        if set(layers) != set(numr):
            sys.exit(f"{glyph} masters differ from zero.numr masters")
        for lid, ps in layers.items():
            old = [parse(lines, a, b) for a, b in ps]
            if [len(s) for s in old] != [12, 12, 12, 12, 4] or bbox(old[0])[1] <= bbox(old[2])[3]:
                sys.exit(f"{glyph} layer {lid}: expected top ring, bottom ring, slash")
            new = [*ring(old[0], numr[lid], "top"), *ring(old[2], dnom[lid], "bottom"), widened(old[4], slash[lid][0])]
            for (a, b), ns in zip(ps, new):
                text = [f"({fmt(x)},{fmt(y)},{t})," for x, y, t in ns]
                text[-1] = text[-1].rstrip(",")
                edits.append((a, b, text))
    for a, b, text in sorted(edits, reverse=True):
        lines[a:b + 1] = text
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"rebuilt % in {len(edits) // 5} layers")


if __name__ == "__main__":
    main(sys.argv[1])
