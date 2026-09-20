# Transcription report: PDF pages 163--164

- Range: source PDF pages 163--164 inclusive.
- Frozen authority: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp163-164.tex`.
- Output bytes after notation-font audit: 9,902.
- Output SHA-256 after notation-font audit: `02cb72a22db9c3f3c6b6d85b6181142493550aaeb2a2475b14130b8090114ed5`.
- Inspected supplied renders: `sources/official/paper/renders/180dpi/page-163.png` and `page-164.png`.
- Direct-PDF inspection: pages 163 and 164 were independently rendered from the frozen PDF at 360 dpi and visually inspected; PDF metadata was rechecked as 166 US-letter pages, PDF 1.5.
- Page count: 2.
- Formula-marker count: 66 total (38 on page 163; 28 on page 164).
- Figure count: 0.
- Unresolved uncertainty IDs: none.

## Boundary state

Page 163 begins mid-paragraph inside the proof of Proposition C.2. The fragment closes that proof after the final sentence on page 163, then opens subsection C.3, Proposition C.3, and its proof. Page 163 ends mid-sentence after “it is a”; page 164 continues that sentence. Page 164 ends mid-sentence after the comma following `X_v=X_{\mathrm{end}}\in(X_a,X_b)` and leaves the proof of Proposition C.3 open for `pp165-166.tex`.

## Extraction defects resolved by visual inspection

- The extraction flattened the fraktur moment vector in (C.17); the page shows `\mathfrak m` and `\widetilde{\mathfrak m}`.
- The extraction displaced superscripts and denominators in the two exponential weights in (C.18), the preserved inner-edge factorization, and (C.19). Each was transcribed from the page image.
- The extraction scrambled the powers in the outer-edge direction: the numerator is `(b_\theta,y_b^6b_z)` and the denominator is `\sqrt{b_\theta^2+y_b^{12}b_z^2}`.
- The extraction displaced the outer-collar factor. The page reads `e^{-4/y_b^2}y_b^{-3}b_\theta`.
- The script `\mathcal T_0`, derivative multi-index `I`, exponent `m_I`, and all subscripts in the cone identities were compared visually rather than accepted from extraction.

No correction, paraphrase, translation, or teaching material was introduced. Apparent source statements were preserved exactly; no suspected source defect remained unresolved in this range. This is an agent-level page/formula check and remains subject to root compilation, cross-reference, correspondence, and rendered-output audits.

## Notation-font audit correction, 2026-09-20

Direct rendered-page and MuPDF font-stream inspection confirms upright roman labels `\mathrm c`, `\mathrm r`, and `\mathrm v` in the class, reference, and named-radius subscripts on pages 163--164. Only those glyph-family choices changed. Prose, formula content, page markers, and all 66 formula markers are unchanged; the byte count and SHA-256 above are the post-audit values.
