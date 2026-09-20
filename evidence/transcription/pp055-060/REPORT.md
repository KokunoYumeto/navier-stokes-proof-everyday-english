# Transcription report: official PDF pages 055--060

- Range: PDF pages 55 through 60, inclusive.
- Frozen authority: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp055-060.tex`.
- Output bytes after notation audit: 29,986.
- Output SHA-256 after notation audit: `5d5f23647375e6c69e60d866ddf6802d40f1e7fbc7e4fe45f27516d05b7a6864`.
- Direct frozen-PDF check: pages 55--60 were queried from the exact hashed PDF in addition to the render and extraction checks.
- Inspected full-page renders: `page-055.png`, `page-056.png`, `page-057.png`, `page-058.png`, `page-059.png`, and `page-060.png` under `sources/official/paper/renders/180dpi/`.
- Pages checked: 6.
- Formula occurrences marked: 288 total, consisting of 253 inline occurrences and 35 displayed occurrences.
- Per-page formula counts: page 55: 35; page 56: 42; page 57: 54; page 58: 51; page 59: 52; page 60: 54.
- Figures: 0.
- Unresolved uncertainties: 0; `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Boundary state

Page 55 continues subsection 5.3 from the preceding range. Proposition 5.3 begins and its proof crosses to page 56, where it closes. Subsection 5.4 and Lemma 5.4 then begin; the lemma statement crosses from page 57 to page 58, and its proof crosses from page 58 to page 59 before closing. Page 60 begins subsection 5.5 and Proposition 5.5. The proposition itself closes on page 60, but its proof remains open at the end of this fragment and must be continued by the page-61 range.

## Extraction defects encountered

The extracted text was useful only as an ordering draft. It flattened distinctions among ordinary and calligraphic letters (`U`/`\mathcal U`, `T`/`\mathcal T`, `A`/`\mathcal A`, and `F`/`\mathcal F`), displaced hats and primes, obscured the superscript in `K_m^{\mathcal F}`, collapsed subscripts such as `\lambda_n`, and lost two-dimensional display layout, delimiter sizing, square-root bars, and equation alignment. It also retained physical line-wrap hyphenation. Every such item was read from the frozen page image; physical line-wrap hyphenation was removed while lexical hyphens and all mathematical signs were preserved.

No source figure occurs in this range. No correction, normalization, paraphrase, translation, or first-use teaching was introduced. Apparent notation was transcribed as printed rather than silently changed. Agent-level page and formula checks are complete; cumulative compilation, live-reference checking, and rendered reconstruction comparison remain root-integration gates.

## Notation-family audit integration, 2026-09-20

Direct MuPDF structured-font evidence and the frozen renders corrected the residual operator to `\mathscr R`, coefficient residuals to `\mathfrak r`, positive-order Stokes streamfunctions to `\mathcal S_n`, the composed derivative to `\mathscr D^I`, and the physical/base stresses (including the hatted stress) to `\mathcal T`. The generic Stokes streamfunction `S` on page 56 remains ordinary italic: the embedded font explicitly distinguishes it from the calligraphic positive-order `\mathcal S_n`. Only glyph-family encodings changed; prose, formula structure, equation labels, and all page/formula markers are unchanged. The byte count and SHA-256 above are post-audit values.
