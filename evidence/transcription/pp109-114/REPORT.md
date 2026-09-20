# Source-faithful transcription report: PDF pages 109--114

- Range: official PDF pages 109--114, inclusive.
- Frozen authority: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp109-114.tex`.
- Output byte count after notation audit: 27,515.
- Output SHA-256 after notation audit: `7e8094ab1cb8144eec7c9e0e746935f921f3307ff83a78a37996ee83ee4199c1`.
- Notation-audit correction (2026-09-20): the bold covariance vector, ordinary incremental potentials, calligraphic residual functional, sans-serif coefficient/primitive glyphs, and Fraktur time derivative were restored from the frozen PDF fonts. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected renders: `page-109.png`, `page-110.png`, `page-111.png`, `page-112.png`, `page-113.png`, and `page-114.png` in `sources/official/paper/renders/180dpi/`.
- Pages visually inspected: 6.
- Formula occurrences visually compared: 204 total (41, 33, 27, 33, 34, and 36 by page).
- Displayed formula markers: 24; inline formula markers: 180.
- Source figures: 0.
- Unresolved uncertainties: 0. `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Boundary state

Page 109 begins mid-paragraph inside the proof of Proposition 9.6, continuing the source exactly. Page 111 closes that proof. The fragment then contains subsection 9.4, all of Lemma 9.7, and all of Lemma 9.8. Page 114 begins subsection 9.5 and Proposition 9.9, whose proof remains deliberately open at the end of this fragment and continues directly on page 115. The adjacent page-103--108 and page-115--120 agents independently confirmed both boundaries.

## Extraction defects handled

The untrusted extracted text flattened display alignment and table rules; displaced several superscripts and subscripts; obscured the exponent in `r^{d_r-1}\Lambda_g^{i_0}`; and lost distinctions among calligraphic, script, and ordinary letters in symbols such as `\mathcal P`, `\mathcal J`, `\mathcal F_{\mathrm{ax}}`, `\mathscr B`, and `\mathscr R`. Every such location was resolved from the frozen page renders, including a magnified inspection of the small formula text on page 113. Physical line-wrap hyphenation was removed only when it split an ordinary word.

No correction, normalization, paraphrase, translation, or teaching material was introduced. Equation numbers (9.13)--(9.19), theorem-like boundaries, proof end marks, source order, cross-references, and page breaks were preserved. Final integration, compilation, cross-reference resolution, and rendered comparison remain root-level acceptance tasks.
