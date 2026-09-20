# Transcription report: PDF pages 121--126

- Range: official PDF pages 121--126, inclusive.
- Frozen PDF SHA-256: 0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f.
- Frozen PDF properties rechecked directly: 166 pages, 612 by 792 points, PDF 1.5.
- Output: reconstruction/sections/pp121-126.tex.
- Output bytes after notation-font audit: 25,232.
- Output SHA-256 after notation-font audit: 243fc34f2eb91236228fe2afa1f6d12b4562bdab426c0a2b77ebbdb1bb3cf833.
- Inspected renders: page-121.png, page-122.png, page-123.png, page-124.png, page-125.png, and page-126.png in sources/official/paper/renders/180dpi/.
- Direct source check: pages 121--126 were also read from the frozen PDF itself with page-bounded Poppler extraction; the image controlled every mathematical and layout-sensitive decision.
- Pages checked: 6.
- Formula markers: 217 total (44, 46, 39, 37, 27, and 24 by page).
- Figures: 0.
- Unresolved uncertainty IDs: none; UNCERTAINTIES.jsonl is intentionally zero bytes.

## Structural coverage

The fragment contains all of subsection 10.3, including Lemmas 10.4 and 10.5 and their proofs; subsection 10.4 and the proof of Theorem 1.1; subsection 10.5, Corollary 10.6, and its proof; and the start of Appendix A through the complete statement of Lemma A.1. The preceding range closes its environments before page 121. Corollary 10.6's proof crosses pages 125--126 and closes here. Lemma A.1's proof begins on page 127 and therefore belongs to the next range.

## Extraction defects resolved by visual reading

The text draft flattened display layouts and summation limits throughout the range. It also obscured the calligraphic form of \mathcal F, displaced the square on the page-122 \|g\|_1^2 bound, lost or separated tilde accents in the periodic rescaling, and made square-root scope and embedding arrows on page 124 unreliable. Each of these items was transcribed from the page image, not inferred from the extraction. The matrix indices and power weight in Lemma A.1 were likewise checked visually.

No source correction, normalization, translation, explanatory addition, or figure reconstruction was introduced. This is an agent-level page and formula inspection; compilation, cumulative cross-reference validation, and rendered reconstruction comparison remain root-integration gates.

## Notation-font audit correction, 2026-09-20

Direct comparison of the frozen page renders with MuPDF structured text and page content streams confirmed that the operator `T` on page 122 and the support symbols `K` and `K_\nu` on pages 124--125 use the source's calligraphic family. Their source forms are now `\mathcal T`, `\mathcal K`, and `\mathcal K_\nu`. Only glyph-family markup changed: prose, formula content, page markers, and all 217 formula markers are unchanged. The byte count and SHA-256 above are the post-audit values.
