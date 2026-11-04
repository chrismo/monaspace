# Why this fork exists

A personal fork to give Monaspace Argon a `?`, `$` and `&` that match its letters. It isn't
meant to go upstream and isn't a maintained font release.

## The problem

Argon's letters have strong details: steep stroke endings, squarish curves, slab
serifs on `i l f r j`. Its `?` looks like a generic sans `?` next to them, and its
`$` and `&` have the same problem.

### Why it doesn't fit

Measured from Argon NF Regular v1.400 outlines (units per em 2000):

| Glyph | Open stroke ends in |
|---|---|
| `2` top | near-vertical cut, (138,1205)→(150,1390) |
| `c` bottom | near-vertical cut, (1072,36)→(1087,192) |
| `3` bottom | near-vertical cut, (155,171)→(203,-13) |
| `?` (upstream) | **near-horizontal cut**, (129,1087)→(315,1070) |
| `S` top / bottom (Black) | near-vertical cuts, (1076,1177)→(1064,1459) and (125,310)→(137,31) |
| `$` (upstream, Black) | **near-horizontal cuts**, (846,1013)→(1151,1044) and (385,467)→(73,418) |
| `&` top loop (upstream, Black) | **near-horizontal cut**, (720,1092)→(1000,1150) |

Every open stroke in `2 a c s 3 5 j f r` ends in a steep cut after a sweeping
curve. The upstream `?` curls down and ends in a near-flat cut. That mismatch is
the main reason it looks out of place. This is a reading of the shapes; the cut
angles themselves are measured.

### Why it can't be fixed with a setting

- No character variant (`cv`) or stylistic set (`ss`) changes `?`. The installed
  font has one `question` glyph and no feature that swaps it. There's also an
  undocumented `cv33`, but it only changes `∊ ○ □`.
- The `?` outline is identical, point for point, in Argon, Neon, Xenon and
  Krypton. Only Radon draws its own, a hand-drawn shape that clashes with
  upright Argon. Borrowing a `?` from another family doesn't help.

### Upstream context

Gathered in another session and not re-checked here:

- Issue #138 ("Every character except for the letters, accents and bigger
  numbers look like Neon's") was closed in Feb 2025: "this is not a bug, that's
  just how the fonts are! We did add some stylized punctuation and symbols for
  Radon and Krypton in 1.2."
- The README lists `cv80`–`cv99` as "reserved for future use", with nothing for
  `?`. Issue #380, which asks for a `cv` for a serifed `7` (Apr 2026), is open
  with no replies.
- As of 2026-11-03, none of the 324 forks had changed `sources/*.glyphs`. The
  forks with their own commits change only build tooling, font metrics,
  READMEs or install scripts. Upstream has no pull requests that change glyph
  designs, and nobody has asked for a new `?`.
- The README credits Heather Cran as "Lead Symbols & Punctuation" for all five
  families. The shared `?` is one deliberate drawing used across the whole
  superfamily.
- Across the full character set (2408 glyphs, compared within 2/1000 em), 1735
  glyphs are identical in all five families. Argon's own drawings are the
  letters, the digits and `!`. For ASCII punctuation:
  - shared by all five: `# * < > @ ^ _ | ~`
  - shared by Argon, Neon, Xenon and Krypton, with only Radon different:
    `$ % ( ) + - / = ? [ \ ] { }`
  - redrawn by both Krypton and Radon: `" & ' , `` ` ``
  - matching only between Argon and Neon: `. : ;`

  So `?` was one of 14 marks in that second group, and `!` is the only ASCII
  punctuation mark that carries Argon's own design. Redrawing `?` alone makes it
  different from the other 13. Most of those 13 are straight-line brackets and
  operators with no open curved stroke, so the stroke-ending mismatch mainly
  applies to `?` and `$`, which is why `$` was done next.

## What was tried

The mockups were made on Regular only, by patching the installed OTF.

- **Ink trap** (a notch where the hook meets the stem): only visible at display
  sizes, and at those sizes it read as a glitch. Dropped.
- **Squarer hook** (C, a rounded rectangle): clearly different, but not right.
- **Faceted counter** (D, copying the diagonal flat spot in the counters of `O`,
  `c` and `D`): left a heavy lump in the curve. No other Argon letter has
  anything like it.
- **Top of the `2`** (E): the `2`'s outer curve, stroke start and inner curve,
  turned down into the `?`'s own stem. **This is the one in this fork.** It gets
  the steep stroke ending and visibly belongs with Argon's digits.

For `$`, the first try was Argon's own `S` with upstream's bars, and that
worked. `S` and `$` are both 1240 wide and nearly the same height, so nothing
had to be redrawn. The pair `$?`, common in shell, now matches.

For `&`, only the top loop's terminal changed. Its right arm already ends in a
square slab. Two versions put the flat arm and steep cut from the top of `S` on
the loop:

- **A**, with the arm as long as the `S`'s: it read as Argon, but next to `?`
  the arm looked short.
- **B**, with the arm stretched to where the old terminal reached: **this is the
  one in this fork.** `&?` then mirror each other, with arms of about the same
  length opening in opposite directions.

## What changed

Eight glyphs in `sources/Variable Fonts/Monaspace Argon Var.glyphs`. In each of
the 8 masters (Light/Black × normal/Wide × upright/Italic):

- `question` is built from that master's own `2` and `?`.
- `dollar` and `dollar.nobar` take that master's `S` in place of their own S
  and keep their bars. Above wght 599 a feature-variation rule swaps `dollar`
  for `dollar.nobar`, which drops the bar through the middle, so both need it.
- `ampersand` and its four variants get the top arm of that master's `S` on
  their top loop. The variants are `.left`, `.right` and `.both` for texture
  healing, plus `.init` for the `&&` ligature in `ss06`. Texture healing picks
  among them by context, so all five need the change.

Building from each master's own glyphs keeps the masters compatible, so every
weight, width and slant blends from them.

The family is **not** renamed. Monaspace's OFL reserves the names "Monaspace",
"Argon", "Neon", "Xenon", "Radon" and "Krypton". chrismo chose to leave the
name alone for this personal experiment.

## Working on it

```bash
python3 -I scripts/question-from-two.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
python3 -I scripts/dollar-from-s.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
python3 -I scripts/ampersand-from-s.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
scripts/build-argon.sh        # -> build/Monaspace Argon Var.ttf (~40s)
```

- **Syncing upstream:** run `git fetch upstream && git merge upstream/main`. If the
  `.glyphs` file conflicts, take upstream's version and rerun
  all three scripts. Only run `question-from-two.py` on upstream's `?`: a second
  run reshapes it again. `dollar-from-s.py` and `ampersand-from-s.py` are safe
  to rerun.
- **Building:** `fontmake` fails on the untouched source because glyphsLib's
  default `eraseOpenCorners` filter makes `softsign-cy.both` incompatible across
  masters. `build-argon.sh` strips that filter. With it stripped, the build
  pixel-matches the v1.400 release at Regular: median difference 0 across 2459
  characters, and the worst cases are edge pixels on tiny glyphs.
- **Checkout:** the local clone is a blobless sparse checkout (Argon source,
  `docs/`, `scripts/`, `LICENSE`, `README.md`). Add paths with
  `git sparse-checkout add <path>`.

## In use (Rex, macOS)

Tested 2026-11-03. Copy `build/Monaspace Argon Var.ttf` into `~/Library/Fonts`.
It installs alongside "Monaspace Argon NF" with no clash. In Rex's Settings >
Terminal:

- Typography > Terminal font: **Monaspace Argon Var**.
- Typography > Font weight: **400**. The font's default weight is 200
  (ExtraLight), so leaving this alone makes text thin.
- Advanced Font Settings > fallback fonts: add **Monaspace Argon NF**.

The build has 55 icons of its own in U+E000–F8FF (Powerline among them). The
fallback supplies the remaining Nerd Font icons: Font Awesome, Devicons,
Octicons, and Material in U+F0000+. All of these rendered when printed with
`printf` in Rex, so there's no need to run the nerd-fonts patcher.

Texture healing (the `calt` feature) works in Rex: in `imi`, the `m` widens
into the space the `i`s leave. Stylistic sets such as `ss06`, which joins `&&`,
aren't reachable: per-feature settings are accepted in Rex feedback but haven't
shipped.

Rex only exposes the weight axis. Ghostty-style `font-variation` is "deferred"
in Rex feedback, so the width axis isn't reachable there.

Nerd Font icons in U+E000–F8FF render blank when they're inside one of Claude
Code's own replies, but fine in command output. That's Claude Code's display,
not this font.

## Open

- Only the variable font is built, with no static font files.
