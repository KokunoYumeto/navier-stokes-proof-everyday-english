# Transcription report: PDF pages 073--078

- Inclusive source range: pages 073--078.
- Frozen source: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output fragment: `reconstruction/sections/pp073-078.tex`.
- Output fragment byte count after notation audit: 29,025.
- Output fragment SHA-256 after notation audit: `5b38e8311290ab187574af3428418fbdbf4decf2b5025fc1eb0ff6790e841c79`.
- Notation-audit correction (2026-09-20): the two fast-time derivative symbols were restored from sans serif to Fraktur as printed. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected renders: `page-073.png`, `page-074.png`, `page-075.png`, `page-076.png`, `page-077.png`, and `page-078.png` under `sources/official/paper/renders/180dpi/`.
- Pages inspected: 6.
- Marked formula occurrences: 254 total (32, 39, 40, 57, 50, and 36 on pages 073 through 078 respectively).
- Source figures: 0.
- Unresolved uncertainty IDs: none.

## Range structure

The fragment starts with the final sentence of the paragraph begun on page 72, contains Section 7, Subsections 7.1 and 7.2, Lemma 7.1 and its complete proof, and Proposition 7.2. Proposition 7.2 closes on page 78. Its proof then opens and deliberately remains open after Equation (7.17), because that proof continues on PDF page 79.

## Extraction defects and source anomaly

The text extraction was used only as a draft. Formula glyphs, accents, subscripts, superscripts, matrix entries, delimiters, and page boundaries were checked against the page renders. Physical line-wrap hyphenation in ordinary words on page 76 was removed as required. The extraction flattened the two rows of the matrix in Equation (7.8) into apparent fractions; enlarged visual inspection resolved the printed object as the 2-by-2 matrix whose first row is `(1,1)` and whose second row is `(c_0 sqrt(1+s^2),-c_0 sqrt(1+s^2))`. No ambiguity remains.

No correction, translation, summary, or teaching material was introduced. Root integration, compilation, cross-range environment checking, live-reference auditing, cumulative rendering, and final page-level visual acceptance remain separate required gates.
