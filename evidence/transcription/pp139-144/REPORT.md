# Source-faithful transcription report: PDF pages 139--144

- Range: official PDF pages 139--144 inclusive.
- Frozen source: `sources/official/paper/navier-stokes.pdf`.
- Required and inspected PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp139-144.tex`.
- Output bytes after notation-font audit: 27,314.
- Output SHA-256 after notation-font audit: `1850511f0e279a13fcaf57fa9c66975b5b495909da200e366ba9e2a143cbe137`.
- Inspected renders: `page-139.png`, `page-140.png`, `page-141.png`, `page-142.png`, `page-143.png`, and `page-144.png` under `sources/official/paper/renders/180dpi/`.
- Pages checked: 6.
- Stable formula markers: 247 total: 42 on page 139, 44 on page 140, 40 on page 141, 38 on page 142, 40 on page 143, and 43 on page 144.
- Figures: 0.
- Unresolved uncertainties: 0; `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Range structure and boundaries

Page 139 begins cleanly after the page-138 completion of Lemma A.6. This range contains Proposition A.7 and its proof, subsection A.7, Lemmas A.8 and A.9 with their proofs, Proposition A.10 and its proof, the opening of Appendix B, and subsection B.1 through equation (B.2). Page 144 ends in the middle of the sentence that continues on page 145: “on whose closure L and H_*^2 + sigma_*^2 do not / vanish ...”. The fragment intentionally leaves that paragraph open while leaving no theorem, proof, list, or display environment open.

## Extraction defects checked against the page images

The untrusted text extraction flattened the calligraphic heat factor `\mathcal H` to ordinary `H`, displaced several primes, subscripts, superscripts, and integral limits, obscured the script residual symbol `\mathscr R`, and made some page-break and display relationships ambiguous. Every affected occurrence was resolved from the frozen 180 dpi page render. Physical line-wrap hyphenation was removed only where it split an ordinary word; lexical hyphens such as “power-law”, “large-radius”, “closed-parameter”, and “z-independent” were retained.

No source correction, translation, explanation, or new mathematical claim was introduced. Apparent source content was transcribed as printed. This range-level pass remains subject to root integration, compilation, cross-reference checking, exact correspondence audit, and rendered comparison of the reconstructed edition.

## Notation-font audit correction, 2026-09-20

Direct rendered-page and MuPDF font-stream inspection confirms that the class labels in `P_{\mathrm c}` and `J_{\mathrm c}` on page 143 use upright roman `\mathrm c`, not an ordinary italic variable. Only those two glyph-family choices changed. Prose, formula content, page markers, and all 247 formula markers are unchanged; the byte count and SHA-256 above are the post-audit values.
