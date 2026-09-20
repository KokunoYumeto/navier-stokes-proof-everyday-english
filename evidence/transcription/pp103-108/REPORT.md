# Source-faithful transcription report: PDF pages 103--108

- Range: official PDF pages 103--108, inclusive.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output: `reconstruction/sections/pp103-108.tex`.
- Output byte length after notation audit: 28,116 bytes.
- Output SHA-256 after notation audit: `ca19ef475da18d2a1e15d18af7e2d66181c0fb3a3920838a199933c8ebf10ffe`.
- Notation-audit correction (2026-09-20): script harmonic/operator glyphs and sans-serif matrix, primitive, and coefficient-class glyphs were restored from the frozen PDF fonts. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected renders: `page-103.png`, `page-104.png`, `page-105.png`, `page-106.png`, `page-107.png`, and `page-108.png` from `sources/official/paper/renders/180dpi/`.
- Page count: 6.
- Stable formula markers: 159 total (page counts 29, 21, 26, 23, 40, 20).
- Figures: 0.
- Unresolved uncertainties: 0; `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Boundary state

- Page 103 begins inside the Lemma 9.2 statement opened on page 102. The fragment closes the lemma, transcribes and closes its proof, then begins Section 9.2.
- Proposition 9.3 item (i) crosses the page 103--104 boundary; its proof ends on page 105.
- The Proposition 9.5 proof crosses the page 106--107 boundary and closes on page 107.
- Proposition 9.6's statement and ordered list cross the page 107--108 boundary. Its proof begins on page 108 and remains open at the fragment end. The final page-108 paragraph ends exactly after `flatness`; page 109 continues with `bound.`.

## Inspection and extraction notes

Every page was inspected against both the frozen official page and its 180 dpi render. Every inline and displayed mathematical occurrence was read visually and assigned a stable page-local marker. The extraction draft was used only for initial prose routing. Its known defects in this range included displaced superscripts and subscripts, lost calligraphic/script styling, flattened fraction structure, and unreliable alignment of equations (9.3)--(9.12); those readings were resolved from the page images.

No figure occurs in this range. No source wording or mathematical notation was corrected, translated, simplified, or normalized. Cross-page theorem, proof, list, display, and paragraph states were preserved and coordinated with the owners of pages 97--102 and 109--114. This range-level pass remains subject to root integration, compilation, global reference checks, formula inventory checks, and rendered comparison.
