# Transcription report: PDF pages 007--012

- Inclusive PDF range: pages 7--12.
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output fragment: `reconstruction/sections/pp007-012.tex`.
- Output fragment SHA-256 at this report: `077c50a30e68490736f531773ccc5bfdf168ca03df5703087a18d7ba94c2fc12`.
- Inspected renders: `page-007.png`, `page-008.png`, `page-009.png`, `page-010.png`, `page-011.png`, and `page-012.png` under `sources/official/paper/renders/180dpi/`.
- Page markers: 6.
- Formula markers: 144 total (113 inline and 31 displayed): page 7, 32; page 8, 29; page 9, 17; page 10, 19; page 11, 26; page 12, 21.
- Figures: 2 (`NS-FIG-3` on page 9 and `NS-FIG-4` on page 10). Both complete captions are transcribed. The art is represented by checked-crop placeholders as required until exact vector crops are integrated by the root workflow.
- Unresolved uncertainties: none; `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Extraction defects encountered

- Page 7 text extraction flattened the fractions defining `A` and `D` into `12`; the page image establishes `1/2+h` and `1/2-h`.
- Page 8 extraction displaced radical bars, superscripts, norm subscripts, and parentheses in several displays; every affected relation was read from the page image.
- Page 9 extraction interleaved the two panels of Figure 3 and detached radicals from their radicands. The caption, stress equations, integration limits, and annular radii were checked visually.
- Page 10 extraction could not preserve the two-dimensional layout of Figure 4 and visually joined the radical in `E/\sqrt{2X}` to adjacent prose. The page image controls both readings.
- Page 11 extraction collapsed subscripts and superscripts, duplicated an asymptotic-comparison symbol in the pulse-scale display, and did not distinguish the script residual and calligraphic stress glyphs. The page image and embedded font identities establish `\mathscr R`, `\mathcal T`, and the two separate `\asymp` relations.
- Page 12 extraction displaced tildes, the exponent on `\mathbb T^2`, covariance-vector rows, and the indices in the energy identity. These items were checked against the page image and PDF character/font data.

The page-11/page-12 sentence boundary is preserved exactly: page 11 ends after “while,” and page 12 resumes with “retaining periodic averaging.” The page-7/page-8 paragraph through the leading radial pressure balance is also left continuous across the page marker. No source correction, paraphrase, translation, or teaching addition was introduced. This range-level pass remains subject to root integration, compilation, reference audits, exact figure-crop integration, and rendered comparison.
