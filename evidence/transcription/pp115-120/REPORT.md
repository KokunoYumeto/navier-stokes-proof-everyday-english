# Transcription report: official PDF pages 115--120

- Range: official PDF pages 115--120, inclusive.
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp115-120.tex`.
- Output size and SHA-256 after notation audit: 27,814 bytes; `349578662f5c4b29f1021d09199731a9aa764e5c2703d8c4c75b9bce7bca3726`.
- Notation-audit correction (2026-09-20): ordinary incremental potentials, calligraphic Stokes streamfunctions, and ordinary local compact-set `K_0` were restored while retaining the printed calligraphic main fields/support set. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected renders: `sources/official/paper/renders/180dpi/page-115.png` through `page-120.png`, each inspected at full-page and enlarged formula detail.
- Pages checked: 6.
- Formula markers: 225 total, consisting of 196 inline occurrences and 29 displayed occurrences.
- Per-page formula counts: page 115: 25; page 116: 34; page 117: 38; page 118: 44; page 119: 45; page 120: 39.
- Figures: 0.
- Unresolved uncertainty IDs: none. `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Boundary state

Page 115 directly continues the proof of Proposition 9.9 and its Step 1 from page 114. Page 115 ends in the middle of a sentence after “mean”; page 116 continues that sentence, completes Steps 3--5, and closes the proof. Page 116 then begins Section 10 and ends mid-sentence. Page 117 completes that sentence, begins Subsection 10.1, and states Proposition 10.1. Page 118 opens and closes its proof, defines the localized force, begins Subsection 10.2, and states Lemma 10.2. Page 119 opens Lemma 10.2's proof. Page 120 completes that proof, states and proves Lemma 10.3, and closes every environment before page 121 begins a fresh subsection. Both adjacent-range agents confirmed these boundaries.

## Visual and extraction checks

The untrusted text extraction flattened calligraphic glyphs, superscripts/subscripts, radical extent, derivative scope, and some display alignment. Every such item was read from the page images. In particular, the reconstruction preserves the calligraphic local fields `\mathcal A` and `\mathcal B`; the source's visible switch from subscripted `u_{\mathrm{loc}},p_{\mathrm{loc}}` in Proposition 9.9 to superscripted `u^{\mathrm{loc}},p^{\mathrm{loc}}` in Section 10; the unsigned primitive formula for `\Psi` on page 117; the derivative scope over the quotient in (10.8); and the floor and norm indices in the definition of `b_j` on page 120.

The enlarged visual pass checked all prose, headings, statement/proof boundaries, cross-references, punctuation, and all 225 formula occurrences in source order. No figures occur in the range. ChkTeX was run as a non-building syntax screen; its remaining notices were spacing/style heuristics plus the intentional inherited `\end{proof}` and half-open-interval delimiter, not unresolved source readings.

No correction, normalization, paraphrase, translation, or teaching material was introduced. Apparent notation changes were preserved rather than silently regularized. Root integration, compilation, cumulative cross-reference validation, and rendered comparison remain separate acceptance gates.
