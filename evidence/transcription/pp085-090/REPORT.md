# Source-faithful transcription report: PDF pages 085--090

- Inclusive source range: PDF pages 85--90.
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output fragment: `reconstruction/sections/pp085-090.tex`.
- Output fragment byte count after notation audit: 28,695.
- Output fragment SHA-256 after notation audit: `c2533e877bec521c56d44bff81e21fd2c16c5b8d35789803b6a1b0977119a08a`.
- Notation-audit correction (2026-09-20): the calligraphic named stress, sans-serif coefficient classes and primitive operator, calligraphic radial operator, and Fraktur fast-time derivative were restored from the frozen PDF fonts. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected full-page renders: `page-085.png`, `page-086.png`, `page-087.png`, `page-088.png`, `page-089.png`, and `page-090.png` in `sources/official/paper/renders/180dpi/`.
- Pages checked: 6.
- Marked formula occurrences checked: 209 total (page counts 38, 49, 36, 21, 23, and 42).
- Source figures: 0.
- Unresolved uncertainty IDs: none.

## Boundary state

The page markers retain all source-page crossings in place. Page 86 begins and ends inside prose continued across neighboring pages. The proof of Corollary 7.8 crosses pages 87--88 and is closed only where the source closes it. The physical-definition sentence crosses pages 89--90. Lemma 8.2 begins on page 90 and continues on page 91, so the `lemma` environment is deliberately left open at this fragment's end for the following source fragment to continue and close.

## Extraction defects encountered

The untrusted text extraction flattened display alignment and lost distinctions carried by glyph shape or vertical placement, including hats, superscripts, subscripts, calligraphic operator letters, and integral limits. It also represented physical line-wrap hyphenation as textual breaks. Every such location was resolved by direct inspection of the frozen page renders; enlarged crops were additionally used for the calligraphic stress and defect notation on pages 88--89 and for Equations (8.4)--(8.8) on page 90.

No correction, normalization, paraphrase, translation, or teaching text was introduced. The fragment transcribes the visible source order and mathematics, with suspected-error handling reserved for the separate uncertainty/errata layer.
