# Source-faithful transcription report: PDF pages 133--138

- Range: official PDF pages 133--138, inclusive.
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output fragment: `reconstruction/sections/pp133-138.tex`.
- Output fragment bytes: 28,443.
- Output fragment SHA-256: `fb6f194afd8606aa273941827ab8065d80cdc4c9c04c23e51cd22c5bad05ca99`.
- Inspected full-page renders: `page-133.png`, `page-134.png`, `page-135.png`, `page-136.png`, `page-137.png`, and `page-138.png` under `sources/official/paper/renders/180dpi/`.
- Pages checked: 6.
- Stable formula markers: 288 total (43, 40, 63, 49, 51, and 42 on pages 133--138 respectively).
- Printed numbered displays: 20, covering (A.19)--(A.38).
- Figures: 0.
- Unresolved uncertainties: none; `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Boundary state

Page 133 starts a new indented paragraph after the page-132 paragraph closes. Page 134 begins inside the proof of Lemma A.5 and ends in a paragraph that continues on page 135. Page 135 ends after display (A.28), whose explanatory paragraph continues on page 136. Page 136 ends with the word “Combining,” and page 137 completes that sentence. Page 138 closes the proof of Lemma A.6 after (A.38); page 139 begins a new paragraph and no environment crosses that boundary. Both adjacent-range owners received these boundary states.

## Extraction defects resolved by visual inspection

The untrusted text extraction flattened or ambiguously spaced several mathematical glyphs and structures, notably the pulse coordinate `\zeta_b` (which extraction could suggest was `\xi_b`), the prefix-average operator `\mathcal A_X`, the heat factor `\mathcal H`, the scripted residual `\mathscr R`, the subscript in `\vartheta_f`, and stacked limits, exponents, derivatives, and norms. Physical line-wrap hyphenation also split ordinary words. Each affected occurrence was read from the rendered PDF page, compared in context, and transcribed without retaining physical line-wrap hyphens.

Every visible substantive item in the assigned range was transcribed in source order. Every inline and displayed mathematical occurrence was compared visually with the frozen official page. No correction to the official paper, modernization, normalization, translation, explanatory insertion, or other semantic edit was introduced.

## Root integration correction, 2026-09-20

A repository-wide control-sequence scan found two transcription-only omissions: the draft contained literal `qquad` text in Equation (A.26) on page 135 and Equation (A.32) on page 138. The frozen PDF shows mathematical spacing at both positions and no printed word “qquad.” Root restored the missing backslashes. No displayed symbol, relation, constant, hypothesis, equation number, marker, page order, or source claim changed. Immediately after that repair the fragment was 28,396 bytes with SHA-256 `301e874f63e2bf1bfada7c981b70f1d53a93662cbe64d08a05cb4de3dfed3756`; the later notation audit supersedes that identity with the values above while preserving both `\qquad` controls.

## Notation-font audit correction, 2026-09-20

The frozen renders and MuPDF structured text/content streams confirm upright `\mathrm p` in `X_{\mathrm p}` on page 133, upright `\mathrm c` in `P_{\mathrm c}` on page 134, sans-serif `\mathsf C` for the named amplitude on page 136, and calligraphic `\mathcal I_2` for the reserved interval on page 137. These glyph-family-only corrections preserve the two preceding `\qquad` repairs verbatim. Prose, formula content, page markers, and all 288 formula markers are unchanged; the byte count and SHA-256 above are the post-audit values.
