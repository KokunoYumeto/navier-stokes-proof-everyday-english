# Source-faithful transcription report: PDF pages 031--036

- Range record: NS-TRANSCRIPTION-PP031-036
- Frozen authority: sources/official/paper/navier-stokes.pdf
- Frozen PDF SHA-256: 0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f
- Output: reconstruction/sections/pp031-036.tex
- Output byte count after notation audit: 28,407
- Output SHA-256 after notation audit: 0e6b8389b167db12a1d3b79d450fdbd2581be66b065709e022f7175a583ababc
- Inspected full-page renders: page-031.png, page-032.png, page-033.png, page-034.png, page-035.png, page-036.png
- Inspected pages: 6
- Stable formula markers: 281
- Formula markers by page: 031 = 42; 032 = 42; 033 = 61; 034 = 40; 035 = 49; 036 = 47
- Source figures: 0
- Unresolved uncertainty IDs: none

## Range boundaries

PDF page 031 begins with an ordinary-prose continuation from page 030. Lemma 4.5 and its proof are fully contained across pages 031--032. Theorem 4.6 begins on page 032 and closes on page 034. The proof of Lemma 4.7 crosses pages 034--035. Lemma 4.8 is stated on page 035 and proved at the start of page 036. Proposition 4.10 begins on page 036; its proposition and enumerate environments intentionally remain open because item (i) continues on PDF page 037.

## Extraction defects resolved by the frozen renders

- On page 031, extraction flattened the fraktur shear symbol \mathfrak{s} to an ordinary s; a 500-dpi visual crop resolved the glyph.
- On page 033, extraction dropped or displaced square-root bars in E=\sqrt{2X}F and in the definition of H_{\mathrm{pow}}; the render controlled both readings.
- On page 034, extraction garbled the terminal fraction 1/2 in the contraction estimate as 21; the render clearly shows \tfrac12.
- On page 036, extraction inserted a spurious square-root reading in the logarithmic coordinate. The high-resolution render clearly shows \log(X/X_a).
- Several extraction lines misplaced integral limits, superscripts, subscripts, and display grouping. Each was transcribed from the page image rather than accepted from extraction.

## Verification statement

Every visible prose passage, theorem-like boundary, list item, inline mathematical occurrence, displayed formula, printed equation number, and cross-reference in this range was compared against the frozen 180-dpi render, with higher-resolution PDF renders used where a glyph remained ambiguous. Formula IDs are consecutive in visual order on each page, and the page-check counts equal the LaTeX marker counts. No correction, paraphrase, translation, teaching addition, or figure reconstruction was introduced. Final acceptance still belongs to root integration, cumulative compilation, reference auditing, and rendered-page comparison.

Root integration added `\allowbreak` at the two multiplication signs in the long item-(iii) intervals on source page 035. This is a line-breaking control only; the visible mathematical expressions and all formula/source markers are unchanged.

## Notation-family audit integration, 2026-09-20

Direct MuPDF structured-font evidence and the frozen renders corrected three named-family distinctions: the amplitude normalization is `\mathsf C`; the quadratic map in Lemma 4.7 is `\mathcal Q`; and Lemma 4.9 uses ordinary italic physical stress `T,T_\theta,T_z` while retaining calligraphic stress profile `\mathcal T_0`. Only glyph-family encodings changed. The pre-existing `\allowbreak` controls, prose, formula structure, equation labels, and all markers are unchanged. The byte count and SHA-256 above are post-audit values.
