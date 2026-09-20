# Source-faithful transcription report: PDF pages 019--024

- Range record: `NS-RANGE-PP019-024`
- Frozen source: `sources/official/paper/navier-stokes.pdf`
- Frozen source SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Output: `reconstruction/sections/pp019-024.tex`
- Output byte length after root integration: `23024`
- Output SHA-256 after root integration: `bbf2df9723d4720b63cab67fcac8e3818a454e020ca688eab543fbbd258a77ab`
- Inspected renders: `page-019.png`, `page-020.png`, `page-021.png`, `page-022.png`, `page-023.png`, `page-024.png` under `sources/official/paper/renders/180dpi/`
- Inspected source pages: frozen PDF pages 19--24, with `pdftohtml -xml -hidden -i -f 19 -l 24` used only to disambiguate embedded mathematical font families after visual inspection
- Page count: 6
- Formula-marker count: 184 total (`29 + 40 + 34 + 26 + 28 + 27`)
- Display-formula count: 1, equation `(4.1)` on PDF page 24
- Figure count: 0
- Unresolved uncertainty IDs: none

## Content and boundaries

Pages 19--24 contain all of Table 1, “Guide to the principal symbols,” followed on page 24 by the start of Section 4, the start of Subsection 4.1, and equation `(4.1)`. The page-24 closing sentence continues onto PDF page 25; the TeX deliberately leaves that sentence open so the next fragment can continue it without inserting a paragraph break.

Root integration added a non-visible LaTeX table-counter step and `tab:1` label at the printed Table 1 caption, and made the printed numeral derive from `\thetable`. This preserves the visible source text while resolving the manuscript's later Table 1 cross-reference.

The table was transcribed in six source-page-aligned `tabular` blocks because it spans the entire assigned range. Repeated continuation headings, column headings, group headings, and “Continued on the next page.” notices were retained. Cross-references use live LaTeX references.

## Extraction defects encountered

Text extraction without font information did not preserve mathematical font families and flattened several radicals, superscripts, subscripts, and stacked fractions. It also rendered the map arrow in `X\mapsto\sqrt{2X}` as two apparent glyphs, split square-bracketed stage superscripts, and interleaved components of equation `(4.1)`. The PDF render and embedded-font XML resolved these defects. In particular, the reconstruction preserves the distinct `\mathscr R`, Euler-fraktur `\mathfrak m`, `\mathfrak s`, `\mathfrak r`, and `\mathfrak t`, calligraphic operators and intervals, sans-serif normalization, covariance, inverse, and coefficient-class symbols, and bold vector `\boldsymbol y`.

## Attestation

Every assigned source page and every marked formula occurrence was visually inspected against the frozen official page render, with the PDF controlling over extraction. No source wording or mathematics was corrected, normalized, translated, paraphrased, or supplemented. This agent-level pass does not replace root compilation, integrated cross-reference checking, source-page correspondence, or rendered visual comparison of the cumulative reconstruction.
