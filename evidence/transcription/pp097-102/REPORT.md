# Source-faithful transcription report: PDF pages 097--102

- Range ID: `pp097-102`
- Frozen authority: `sources/official/paper/navier-stokes.pdf`
- PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Output: `reconstruction/sections/pp097-102.tex`
- Output byte count after notation audit: 27,063
- Output SHA-256 after notation audit: `2debc08f4cc388a445f3f18ad3717cd53367d13a458d0df9a41406f90cc292f2`
- Notation-audit correction (2026-09-20): sans-serif coefficient/primitive glyphs, Fraktur time derivatives, and script `\mathscr L_m` were restored from the frozen PDF fonts. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Pages transcribed and visually checked: 6
- Formula markers: 179 (`\NSi` plus `\NSFormula`)
- Source figures: 0
- Unresolved uncertainties: 0

## Inspected renders

- `sources/official/paper/renders/180dpi/page-097.png`
- `sources/official/paper/renders/180dpi/page-098.png`
- `sources/official/paper/renders/180dpi/page-099.png`
- `sources/official/paper/renders/180dpi/page-100.png`
- `sources/official/paper/renders/180dpi/page-101.png`
- `sources/official/paper/renders/180dpi/page-102.png`

Each full-page render was inspected, and every inline and displayed mathematical occurrence was
checked visually against the frozen page rather than accepted from extraction. The extraction drafts
were used only for initial reading order.

## Cross-page structure

- Page 097 starts subsection 8.6 content after the subsection heading on page 096. Lemma 8.7 begins
  and its proof crosses onto page 098, where it closes.
- Lemma 8.8 begins on page 098, crosses onto page 099, and closes there with its proof.
- Section 9 begins on page 100; its opening notation paragraph crosses onto page 101.
- Proposition 9.1 begins on page 101; its proof crosses onto page 102 and closes there.
- Lemma 9.2 begins on page 102. Its theorem environment is intentionally left open after the first
  sentence because the statement continues on page 103. The pages 103--108 owner was notified of
  the exact boundary and will close the environment after the remaining statement.

## Extraction defects encountered

- Physical line-wrap hyphenation split ordinary words including “tangential,” “expanding,” and
  “linearizing”; only those physical wrap hyphens were removed.
- Extraction flattened the matrices and summations on page 098 and displaced several exponents and
  inverse markers. Their row/column structure, signs, bounds, and transposes were taken from the
  page image.
- Extraction flattened the multi-line grouping in Equations (8.26), (8.27), and (9.2), and did not
  preserve the two mathematical tables' rules or alignment. Those structures were reconstructed from
  the visual pages.
- Angle brackets, calligraphic/script letters, subscripts, superscripts, and end-of-proof squares were
  visually resolved from the page images.

No source wording or mathematics was corrected, normalized, translated, summarized, or augmented.
No suspected source defect remains unresolved in this range.
