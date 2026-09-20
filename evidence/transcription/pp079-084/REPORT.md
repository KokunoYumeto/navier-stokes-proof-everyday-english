# Source-faithful transcription report: PDF pages 079--084

- Inclusive source range: PDF pages 79--84.
- Frozen source: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output fragment: `reconstruction/sections/pp079-084.tex`.
- Inspected renders: `page-079.png`, `page-080.png`, `page-081.png`, `page-082.png`, `page-083.png`, and `page-084.png` in `sources/official/paper/renders/180dpi/`.
- Source pages checked: 6.
- Stable formula markers: 248 total (45, 31, 42, 49, 44, and 37 on pages 79--84 respectively).
- Source figures in range: 0.
- Unresolved uncertainty IDs: none; `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Boundary and structure

Page 79 continues Step 1 in the proof of Proposition 7.2 from page 78 without opening a second proof environment. The inherited proof closes on page 80. Corollary 7.3 and its proof are complete on page 80. Lemma 7.4 is stated on page 80 and proved on page 81. Subsection 7.3 begins on page 81. Proposition 7.5 is stated on page 82 and its proof closes on page 83. Proposition 7.6 and its proof are complete on page 84, so no environment remains open for page 85.

## Extraction defects resolved by visual inspection

The text extraction was used only as a draft. Visual checking and the embedded-font/content stream restored mathematical font roles, including calligraphic `\mathcal A`, `\mathcal K`, `\mathcal T`, `\mathcal B`, `\mathcal C`, and `\mathcal L`; sans-serif `\mathsf H`, `\mathsf W`, and `\mathsf M`; bold-italic vector `\boldsymbol y`; and ordinary italic lookalikes with different roles. It also restored subscripts and superscripts, radical extents, integral bounds, absolute-value and norm delimiters, the binomial coefficient in (7.20), the evaluation bar in the Riccati barrier estimate, primes on the page-83 and page-84 derivative exponents, the `\varepsilon` glyph, and multi-line display structure. Physical line-wrap hyphenation in ordinary words was removed; lexical hyphens and source punctuation were retained.

## Checks

All six rendered pages were inspected visually. Every numbered and unnumbered display and every marked inline occurrence was compared to the page image. Formula IDs are unique and gapless within each page. The fragment has six ordered page markers, 34 display markers matched to 34 display environments, balanced braces, balanced local theorem-like environments, and the single expected inherited-proof imbalance at the leading boundary.

No source correction, paraphrase, translation, explanatory addition, or figure redraw was introduced. Apparent source content was transcribed as printed.
