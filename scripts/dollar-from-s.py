"""Replace the S in `dollar` and `dollar.nobar` with each master's own `S`, keeping the bars.

Usage: python3 -I scripts/dollar-from-s.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
Safe to rerun: the result depends only on `S` and the bars.
"""
import re
import sys


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


def main(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    s_paths = layer_paths(lines, *glyph_block(lines, "S"))
    s_nodes = {}
    for lid, paths in s_paths.items():
        if len(paths) != 1:
            sys.exit(f"S layer {lid} has {len(paths)} paths, expected 1")
        a, b = paths[0]
        s_nodes[lid] = [ln.rstrip(",") + "," for ln in lines[a:b + 1]]
        s_nodes[lid][-1] = s_nodes[lid][-1].rstrip(",")

    edits = []
    for glyph, bars in (("dollar", 3), ("dollar.nobar", 2)):
        layers = layer_paths(lines, *glyph_block(lines, glyph))
        if set(layers) != set(s_nodes):
            sys.exit(f"{glyph} masters differ from S masters")
        for lid, paths in layers.items():
            if len(paths) != bars + 1:
                sys.exit(f"{glyph} layer {lid} has {len(paths)} paths, expected {bars + 1}")
            a, b = paths[-1]
            edits.append((a, b, s_nodes[lid]))
    for a, b, text in sorted(edits, reverse=True):
        lines[a:b + 1] = text
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"replaced the S in {len(edits)} layers")


if __name__ == "__main__":
    main(sys.argv[1])
