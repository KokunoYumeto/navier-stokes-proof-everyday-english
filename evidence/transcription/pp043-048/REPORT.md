# Transcription report: PDF pages 043--048

- Range: 043--048 inclusive
- Frozen authority: `sources/official/paper/navier-stokes.pdf`
- PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Verified PDF page count: 166
- Output: `reconstruction/sections/pp043-048.tex`
- Output bytes after notation audit: 27,381
- Output SHA-256 after notation audit: `e2c83a1f3693f8bed47b426917a7586566b85e5b3617fb9dace89f785353359d`
- Inspected renders: `page-043.png`, `page-044.png`, `page-045.png`, `page-046.png`, `page-047.png`, `page-048.png`
- Page records: 6
- Stable formula markers: 234 total (43: 39; 44: 36; 45: 30; 46: 40; 47: 49; 48: 40)
- Figures: 0
- Unresolved uncertainties: 0

## Boundary structure

Page 043 begins inside the proof of Theorem 4.6 and continues directly from page 042. The paragraph at the foot of page 043 continues onto page 044. Page 045 closes that proof, starts Section 5 and subsection 5.1, and ends inside a paragraph continued on page 046. Page 047 opens the proof of Lemma 5.1; page 048 ends mid-sentence inside that proof, which must remain open for page 049.

## Extraction defects resolved by visual inspection

The untrusted text extraction discarded bold-vector and calligraphic distinctions for the cumulative vector, stress coordinates, correction vectors, and annular stress. It also flattened stacked extrema, radicals, integrals, superscript `[2]`, matrix subscripts, fractions, operator compositions, and multiline equation alignment. Every such item was read from the frozen page image and checked against the PDF-derived render. Physical line-wrap hyphenation was removed only where it split an ordinary word; intentional hyphens and all paragraph boundaries were retained.

## Verification statement

All six frozen PDF pages, all six 180-dpi page renders, and all six extracted-text drafts were inspected. Text order and every displayed and inline mathematical occurrence were compared visually. No source figure occurs in this range. No correction, normalization, paraphrase, translation, or teaching addition was introduced. The empty uncertainty ledger records that every visible item in this range was resolved at agent level. Root integration, cumulative compilation, cross-reference audit, and rendered-source comparison remain separate acceptance gates.

## Notation-family audit integration, 2026-09-20

Direct MuPDF structured-font evidence and the frozen renders corrected the quadratic map to `\mathcal Q`; ordinary correction data `d_N,c`; Fraktur moment and shear symbols `\mathfrak m,\mathfrak s`; ordinary stress-coordinate vectors `p`; the fixed normalization `\mathsf C`; and the sans-serif transpose `{}^{\mathsf T}`. Earlier `\boldsymbol` encodings on page 43 were removed only where the source uses ordinary italic or Fraktur glyphs. Prose, formula structure, labels, and all markers are unchanged. The byte count and SHA-256 above are post-audit values.
