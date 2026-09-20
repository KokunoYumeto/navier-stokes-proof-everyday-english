# Source-faithful transcription report: PDF pages 013--018

- Range: official PDF pages 13 through 18, inclusive (six pages).
- Frozen authority: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp013-018.tex`.
- Output byte count after notation audit: 23,144.
- Output SHA-256 after notation audit: `6c6ca5561776264835f62ce04b924088a54ee999cd9c0152294ef580cdb262a1`.
- Notation-audit correction (2026-09-20): glyph-family commands were corrected against the frozen PDF content stream and render (`\mathcal B`, `\mathfrak r`, and the sans-serif coefficient classes). Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected renders: `page-013.png`, `page-014.png`, `page-015.png`, `page-016.png`, `page-017.png`, and `page-018.png` under `sources/official/paper/renders/180dpi/`.
- Page checks: six JSONL records in `PAGE_CHECKS.jsonl`.
- Formula markers: 168 total: 11 on page 13, 18 on page 14, 29 on page 15, 57 on page 16, 29 on page 17, and 24 on page 18.
- Figure records: two, `NS-FIG-5` on page 13 and `NS-FIG-6` on page 15. Their captions and labels are transcribed. Their complete source artwork was visually inspected and is represented by protocol-mandated placeholders until checked vector crops are integrated.
- Unresolved uncertainty IDs: none. `UNCERTAINTIES.jsonl` is zero bytes.

## Boundaries and structure

The range preserves Section 3.4, all four correction-cycle operations, the residual-decay recurrence, Figure 6's caption, Theorem 3.1 and its four parts, Section 3.5, Section 3.6, Equations (3.3)--(3.11), Definitions 3.2--3.3, and the prose that introduces Table 1. Theorem 3.1 is kept open across the source page 15/16 boundary. The normalized-operator sentence is kept open across the source page 17/18 boundary. Page 18 ends before Table 1, which begins on official page 19.

## Extraction defects resolved by visual inspection

The text extraction was used only as a drafting aid. It lost the flowchart geometry and edge directions on pages 13 and 15; scrambled stacked fractions in the page 14 residual-decay recurrence and the page 16 energy integral; reordered parts of Equation (3.6); obscured radicals and denominator groupings in Equations (3.5), (3.7)--(3.10); and flattened tuple, exponent, and weight structure in Equation (3.11) and the coefficient-class bounds. Each affected item was read from the 180 dpi page render and checked against the frozen PDF page rather than inferred from the extraction.

No source wording or mathematical content was corrected, translated, paraphrased, or supplemented in this range. Apparent line-wrap hyphenation alone was removed. This range-level pass is not a claim of final integrated acceptance: compilation, cross-range references, vector-crop integration, cumulative rendered comparison, and root acceptance remain required.
