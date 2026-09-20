# Source-faithful transcription report: PDF pages 025--030

- Range: official PDF pages 25 through 30, inclusive.
- Frozen PDF authority: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp025-030.tex`.
- Output bytes at this check: 26,593.
- Output SHA-256 at this check: `79f3c38dc7d0c46ca254632bcf74b7712997f23325883bbf72ee46ec82e43d95`.
- Inspected renders: `page-025.png`, `page-026.png`, `page-027.png`, `page-028.png`, `page-029.png`, and `page-030.png` under `sources/official/paper/renders/180dpi/`.
- Page markers: 6, in the exact order 025, 026, 027, 028, 029, 030.
- Formula markers: 244 total: 44 on page 25, 44 on page 26, 32 on page 27, 40 on page 28, 43 on page 29, and 41 on page 30.
- Source figures: 0 in this range.
- Unresolved uncertainties: none. `UNCERTAINTIES.jsonl` is therefore a zero-byte file.

## Content and boundary checks

The range contains the continuation of Section 4.1; Lemma 4.1; equations (4.2)--(4.14); Proposition 4.2 and its proof; Section 4.2; equations (4.15)--(4.19); Lemmas 4.3 and 4.4 with their proofs; and the beginning of Section 4.3 through equation (4.20). The page-25 marker is inside the paragraph begun on page 24. The page-27 marker is inside the paragraph begun on page 26. Lemma 4.4 remains open across the page-28/29 boundary, and its proof remains open across the page-29/30 boundary. These boundaries were preserved rather than converted into artificial paragraph or environment breaks.

Every displayed and inline formula was compared to the page image. Embedded PDF font data were additionally inspected where extraction discarded notation class: the stress profile uses calligraphic `T`, while the shear vector and cumulative-integral tuple use fraktur `s` and `m`. All displayed equation numbers (4.2)--(4.20) present in the range have explicit tags and stable labels. The theorem-like statements and proofs retain their source order and scope.

## Extraction defects encountered

The untrusted text extraction flattened aligned displays and cases, displaced fraction material and accents, normalized calligraphic and fraktur symbols to ordinary letters, and detached hats from hatted quantities on page 30. In equation (4.15), extraction order misleadingly placed the superscript `2` next to `C_p`; the rendered page confirms `C_p=\int_0^X E^2/(2x)\,dx`. Physical line-wrap hyphenation in words such as “following,” “pressure,” and “momentum” was removed, while lexical hyphens such as “centrifugal-pressure,” “higher-order,” “radial-viscosity,” “scalar-profile,” and “one-sided” were retained.

Static checks found six unique page markers, 244 unique and contiguous per-page formula IDs, balanced environment counts by environment type, six valid JSON page-check objects, and no duplicate formula IDs. No PDF was compiled in this range task; cumulative compilation and rendered comparison remain root-integration responsibilities.

No correction to the official paper, paraphrase, translation, teaching insertion, or silent normalization was introduced. Apparent source defects would have been logged separately rather than repaired; none remained unresolved in this range.

## Root integration correction, 2026-09-20

An independent translation-side comparison found two transcription-only control-sequence omissions: the draft had literal text `qquad` after `H_i=\sqrt{2X}E_i` on page 28 and twice in Equation (4.19) on page 30. The frozen PDF visibly has mathematical spacing at those positions and no printed word “qquad.” Root restored the missing backslashes, without changing any displayed symbol, relation, value, formula identifier, page marker, or source claim. These spacing repairs remain present after the later notation audit.

## Notation-family audit integration, 2026-09-20

Direct MuPDF structured-font evidence and the frozen renders identify the logarithmic radial derivative as calligraphic `\mathcal D_X` and the fixed amplitude normalization as sans-serif `\mathsf C`. Those family encodings were corrected throughout pages 25--28 where the named quantities occur. Ordinary constants such as `C_Q`, `C_N`, `C_p`, `C_k`, and `C^k` were deliberately left ordinary. No prose, marker, formula ordering, equation structure, or the earlier `\qquad` repairs changed. The byte count and SHA-256 above are post-audit values.
