# Why this fork exists

A personal fork to give Monaspace Argon a `?` that matches its letters. It isn't
meant to go upstream and isn't a maintained font release.

## The problem

Argon's letters have strong details: steep stroke endings, squarish curves, slab
serifs on `i l f r j`. Its `?` looks like a generic sans `?` next to them.

### Why it doesn't fit

Measured from Argon NF Regular v1.400 outlines (units per em 2000):

| Glyph | Open stroke ends in |
|---|---|
| `2` top | near-vertical cut, (138,1205)→(150,1390) |
| `c` bottom | near-vertical cut, (1072,36)→(1087,192) |
| `3` bottom | near-vertical cut, (155,171)→(203,-13) |
| `?` (upstream) | **near-horizontal cut**, (129,1087)→(315,1070) |

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
  applies to `?` and `$`. That makes `$` the likely next candidate.

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

## What changed

Only the `question` glyph in `sources/Variable Fonts/Monaspace Argon Var.glyphs`.
In each of the 8 masters (Light/Black × normal/Wide × upright/Italic), the new `?`
is built from that master's own `2` and `?`. That keeps the masters compatible, so
every weight, width and slant blends from them.

The family is **not** renamed. Monaspace's OFL reserves the names "Monaspace",
"Argon", "Neon", "Xenon", "Radon" and "Krypton". chrismo chose to leave the
name alone for this personal experiment.

## Working on it

```bash
python3 -I scripts/question-from-two.py "sources/Variable Fonts/Monaspace Argon Var.glyphs"
scripts/build-argon.sh        # -> build/Monaspace Argon Var.ttf (~40s)
```

- **Syncing upstream:** run `git fetch upstream && git merge upstream/main`. If the
  `.glyphs` file conflicts, take upstream's version and rerun
  `question-from-two.py`. Only run the script on upstream's `?`: a second run
  reshapes it again.
- **Building:** `fontmake` fails on the untouched source because glyphsLib's
  default `eraseOpenCorners` filter makes `softsign-cy.both` incompatible across
  masters. `build-argon.sh` strips that filter. With it stripped, the build
  pixel-matches the v1.400 release at Regular: median difference 0 across 2459
  characters, and the worst cases are edge pixels on tiny glyphs.
- **Checkout:** the local clone is a blobless sparse checkout (Argon source,
  `docs/`, `scripts/`, `LICENSE`, `README.md`). Add paths with
  `git sparse-checkout add <path>`.

## Open

- Untested in a real terminal. The family name "Monaspace Argon Var" should
  coexist with an installed "Monaspace Argon NF", but that hasn't been checked.
- There are no Nerd Font icons. The nerd-fonts patcher step hasn't been tried.
- `$` is probably next, for the reason in [Upstream context](#upstream-context).
- Only the variable font is built, with no static font files.
