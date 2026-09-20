# Source-faithful transcription report: PDF pages 127--132

- Inclusive source range: 127--132
- Frozen source: `sources/official/paper/navier-stokes.pdf`
- Frozen source SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Output: `reconstruction/sections/pp127-132.tex`
- Output bytes after notation-font audit: `29840`
- Output SHA-256 after notation-font audit: `a3549d2b3d57019253e46ab04e94441e4d70b64abd497d73f7fa0199d9f2a6c8`
- Source renders inspected: `page-127.png`, `page-128.png`, `page-129.png`, `page-130.png`, `page-131.png`, `page-132.png` under `sources/official/paper/renders/180dpi/`
- Pages checked: 6
- Formula markers: 315 total (289 inline and 26 display)
- Per-page formula-marker counts: 127: 56; 128: 44; 129: 42; 130: 71; 131: 51; 132: 51
- Source figures: 0
- Unresolved uncertainty IDs: none

## Coverage and boundaries

Page 127 begins the proof of Lemma A.1 after its complete statement on page 126, then closes that proof, states Lemma A.2, and begins its proof. Page 128 completes Lemma A.2 and gives Corollary A.3 and its proof. Page 129 opens Subsection A.2. Proposition A.4 begins on page 130 and its statement continues onto page 131. Page 131 opens Subsection A.3. The inline expression `r_I-(1-lambda)^(-1)` crosses the physical 131--132 break and is marked by its page-visible pieces. The final sentence on page 132 closes its paragraph; the visibly indented text on page 133 begins a new paragraph.

The page-126 and page-133 boundary structures were checked with the adjacent range owners. No environment is unintentionally open at either range boundary.

## Visual and formula inspection

Every page was inspected first as a complete 180-dpi render and then in enlarged overlapping crops. Every displayed and inline mathematical occurrence was compared visually with the frozen render. Numbered displays (A.1)--(A.18) appearing in this range retain their printed numbers, and live labels/references were supplied. No figure occurs in this range.

Extraction defects resolved from the page images included lost layout and theorem styling, ambiguous radical grouping, malformed norm subscripts, the pulse coordinate being rendered as an xi-like character instead of `zeta_b`, and loss of the calligraphic form of the prefix-average operator `mathcal A_X`. Physical line-wrap hyphenation was removed only where it split ordinary words.

## Fidelity statement

The fragment is a source-faithful transcription only. No source correction, paraphrase, translation, explanatory addition, or mathematical normalization was introduced. There are no unresolved readings; consequently `UNCERTAINTIES.jsonl` is intentionally zero bytes. Root integration, compilation, cross-reference auditing, and rendered reconstruction comparison remain separate acceptance gates.

## Notation-font audit correction, 2026-09-20

The frozen renders and MuPDF font resources/content streams confirm calligraphic `\mathcal Q` for the bilinear map on page 127 and `\mathcal D_X` for the logarithmic radial derivative on page 129, upright `\mathrm p` in the named radius `X_{\mathrm p}` on pages 130--131, and sans-serif `\mathsf C` for the normalization on page 131. Only those glyph-family choices changed. Prose, formula content, page markers, and all 315 formula markers are unchanged; the byte count and SHA-256 above are the post-audit values.
