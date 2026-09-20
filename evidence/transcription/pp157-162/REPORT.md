# Source-faithful transcription report: PDF pages 157--162

- Inclusive source range: PDF pages 157--162.
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output fragment: `reconstruction/sections/pp157-162.tex`.
- Output fragment bytes after notation-font audit: 28,962.
- Output fragment SHA-256 after notation-font audit: `147f8815f76008cc51baed23d67a6dc4e63a531cfd03a05e0e7d5198ee45017d`.
- Inspected full-page renders: `page-157.png`, `page-158.png`, `page-159.png`, `page-160.png`, `page-161.png`, and `page-162.png` in `sources/official/paper/renders/180dpi/`.
- Pages checked: 6.
- Marked formula occurrences checked: 245 total (page counts 27, 33, 61, 42, 42, and 40).
- Source figures: 0.
- Unresolved uncertainty IDs: none.

## Boundary state

Page 157 begins inside the proof of Proposition B.8 inherited from the pages 151--156 fragment; the proof closes at the visible square on page 157. Appendix C's opening paragraph crosses pages 157--158. Lemma C.1 begins on page 158, its statement crosses onto page 159, and its proof crosses pages 159--160 before closing at the visible square on page 160. Proposition C.2 begins on page 161. Its proof remains open at the end of this fragment, and the page-162 text ends mid-sentence after `Its partial radial`; page 163 continues with `moment functions`. Both adjacent range owners were notified of the exact boundary state.

## Extraction defects encountered

The untrusted extraction flattened displayed alignment and lost or displaced accents, tildes, blackletter and calligraphic letter forms, subscripts, superscripts, integral limits, square-root spans, and table structure. Notable examples resolved by direct inspection were the nested natural-index constant on page 157, the squared denominator in the asymptotic ratio following Equation (C.6), the calligraphic upper cone bound in Equation (C.8), the tilded profile and moment tuple in Proposition C.2, the script antiderivatives in Equations (C.11)--(C.13), and the two-block moment-weight table on page 162. Physical line wraps and the page-162 sentence break were also checked against the frozen page images.

No correction, normalization, paraphrase, translation, or teaching text was introduced. The fragment transcribes the visible source order and mathematics, with suspected-error handling reserved for the separate uncertainty/errata layer.

## Notation-font audit correction, 2026-09-20

The frozen renders and MuPDF font resources/content streams confirm sans-serif `\mathsf C`, calligraphic `\mathcal B_k`, `\mathcal T_0`, and `\mathcal D_X`, upright roman `\mathrm r` and `\mathrm c` labels, and the distinct RSFS script family `\mathscr A,\mathscr B` in Equations (C.11)--(C.13). The latter are not the calligraphic family used for `\mathcal D_X`. Only confirmed glyph styling changed; prose, formula content, page markers, and all 245 formula markers are unchanged. The byte count and SHA-256 above are the post-audit values.
