# Source-faithful transcription report: PDF pages 091--096

- Range: official PDF pages 91 through 96, inclusive.
- Frozen authority: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp091-096.tex`.
- Output size after notation audit: 29,988 bytes.
- Output SHA-256 after notation audit: `6ceefdd7879aaddc86f284306be95e1014043dd5b7c1839e2772bc2f2f6692a6`.
- Notation-audit correction (2026-09-20): interval/operator, coefficient-class, and Fraktur derivative glyph families were restored from the frozen PDF fonts. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected renders: `page-091.png`, `page-092.png`, `page-093.png`, `page-094.png`, `page-095.png`, and `page-096.png` in `sources/official/paper/renders/180dpi/`.
- Pages checked: 6.
- Stable formula markers: 237 total, comprising 211 inline markers and 26 displayed-math markers.
- Per-page formula-marker counts: page 91: 46; page 92: 42; page 93: 45; page 94: 36; page 95: 33; page 96: 35.
- Source figures in this range: 0.
- Unresolved uncertainty IDs: none. `UNCERTAINTIES.jsonl` is zero bytes.

## Range boundaries and structure

Page 91 starts the proof of Lemma 8.2. The preceding range deliberately leaves that lemma environment open, so this fragment first closes the incoming lemma statement and then opens its proof. The proof closes on page 92. Proposition 8.3 starts on page 92 and continues on page 93; Proposition 8.4 lies wholly on page 94; Corollary 8.5 lies wholly on page 95; Lemma 8.6 starts on page 95 and closes on page 96. The fragment ends after the introductory paragraph of subsection 8.6, with no outgoing theorem or proof environment left open.

## Extraction defects corrected by visual reading

The extracted page text was used only as a draft. Direct inspection of the six frozen renders resolved, among other defects:

- lost distinctions among calligraphic operators, ordinary coordinates, and the math-sans-serif physical derivative operators;
- flattened superscripts and subscripts in the radial primitive, Fourier multiplier, normalization, and covering formulas;
- displaced integral signs, averaging brackets, summation bounds, transpose markers, inverse powers, and differential factors;
- interleaved columns in Equations (8.15) and (8.17);
- corrupted hats, zero-mean circles, Greek letters, and the `phys`, `abs`, and common-chart subscripts;
- unreliable physical line-wrap hyphenation and theorem/proof boundaries at page breaks.

Every visible formula on each assigned page was compared with the corresponding render. Formula IDs are gapless and unique within each page. Each page has exactly one `\NSPage` marker. The six JSONL page-check objects parse successfully and their formula counts sum to 237. As expected for a split source fragment, standalone `lacheck` reports the initial `\end{lemma}` as unmatched. A concatenated audit of `pp085-090.tex` and this fragment balances every lemma, proposition, corollary, proof, enumeration, and displayed-math environment, including the incoming Lemma 8.2 boundary.

No wording was translated, summarized, corrected, or intentionally modernized. No mathematical correction was introduced. Apparent source content was preserved rather than silently repaired. Final acceptance still requires root integration, compilation, cross-reference checking, correspondence audit, and rendered comparison.
