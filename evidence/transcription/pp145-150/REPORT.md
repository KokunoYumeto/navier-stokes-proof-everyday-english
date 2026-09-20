# Transcription report: official PDF pages 145--150

- Range: 145--150 inclusive
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Output: `reconstruction/sections/pp145-150.tex`
- Output bytes after notation-font audit: 29,295
- Output SHA-256 after notation-font audit: `431e84a9dc82d0a6495936a28ea286a7f387d2149c17b712ee001901a4f2377e`
- Inspected renders: `page-145.png`, `page-146.png`, `page-147.png`, `page-148.png`, `page-149.png`, `page-150.png` under `sources/official/paper/renders/180dpi/`
- Page markers: 6
- Formula markers, inline plus display: 276 total (145: 42; 146: 39; 147: 36; 148: 46; 149: 54; 150: 59)
- Figures: 0
- Unresolved uncertainties: 0

## Boundary state

Page 145 starts in the paragraph begun on page 144 after the words "do not". Page 150 ends inside the proof of Lemma B.4 after "in each parameter norm,"; page 151 continues the same paragraph with "uniformly in ...". The LaTeX fragment deliberately leaves that proof and paragraph open for `pp151-156.tex`.

## Extraction defects resolved from the page images

- The extraction draft drops the tilde on `\widetilde{\xi}_0` in (B.3), the sign computation below (B.14), and (B.21).
- The extraction draft reduces the blackletter pressure perturbation `\mathfrak p` in (B.14) and its later occurrences to an ordinary italic `p`.
- Several stacked fractions, binomial coefficients, norm subscripts, and radical extents were spatially flattened. Each was transcribed from the rendered page, including the radicals in `E=\sqrt{2X}\phi/C` and the outer-endpoint formula for `|p_2|`.
- Physical line-wrap hyphenation was removed only where it split an ordinary word. Lexical hyphens, punctuation, and paragraph order were retained.

Every page and every displayed or inline formula marker in this range was visually checked against the frozen render. No correction, normalization, translation, teaching text, or mathematical amendment was introduced. This is an agent-level transcription pass; compilation, integration, cross-reference checking, and comparison of the cumulative rendered reconstruction remain root-level gates.

## Notation-font audit correction, 2026-09-20

The frozen renders and MuPDF structured text/content streams confirm blackletter `\mathfrak a` for the coefficient-weight family and `\mathfrak u` for the correction, calligraphic `\mathcal D_X` for the logarithmic radial derivative and `\mathcal T_0` for the stress, sans-serif `\mathsf C` for the named amplitude/normalization (including `\mathsf C_0`), and upright roman labels `\mathrm r` and `\mathrm b` in the reference and boundary subscripts. Generic estimate constants such as `C`, `C_k`, and `C_{r,s}` remain ordinary italic exactly where the source uses that family. Only confirmed glyph styling changed; prose, formula content, page markers, and all 276 formula markers are unchanged. The byte count and SHA-256 above are the post-audit values.
