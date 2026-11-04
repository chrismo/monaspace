#!/usr/bin/env bash5
# glyphsLib's default eraseOpenCorners filter makes softsign-cy.both
# incompatible across masters, so it is stripped from the exported UFOs.
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
src="$repo/sources/Variable Fonts/Monaspace Argon Var.glyphs"
out="$repo/build"

rm -rf "$out/masters"
mkdir -p "$out"

uvx --from fontmake fontmake -g "$src" -o ufo --master-dir "$out/masters" >"$out/ufo.log" 2>&1

uvx --from fontmake --with defcon python -I -c '
import glob, sys
from defcon import Font
for d in glob.glob(sys.argv[1] + "/*.ufo"):
    f = Font(d)
    f.lib.pop("com.github.googlei18n.ufo2ft.filters", None)
    f.save()
' "$out/masters"

uvx --from fontmake fontmake -m "$out"/masters/*.designspace -o variable --output-dir "$out" >"$out/variable.log" 2>&1

# The OFL requires copyright (7) and license (13) to keep the reserved names.
uvx --from fonttools python -I -c '
import sys
from fontTools.ttLib import TTFont
src, dst = sys.argv[1:]
f = TTFont(src)
for r in f["name"].names:
    if r.nameID in (7, 13):
        continue
    r.string = r.toUnicode().replace("Monaspace Argon Var", "Argot").replace("MonaspaceArgonVar", "Argot")
f.save(dst)
' "$out/Monaspace Argon Var.ttf" "$out/Argot.ttf"
rm "$out/Monaspace Argon Var.ttf"

ls -la "$out"/*.ttf
