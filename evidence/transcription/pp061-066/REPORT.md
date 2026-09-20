# Source-faithful transcription report: PDF pages 061--066

- Range: official PDF pages 61 through 66 inclusive.
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`.
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- Output fragment: `reconstruction/sections/pp061-066.tex`.
- Output fragment byte count after notation audit: 27,600.
- Output fragment SHA-256 after notation audit: `a2bfb467ef8525e59037cab98de4e9a28e30ee6c582fb12a05bcb54a22694152`.
- Notation-audit correction (2026-09-20): the derivative letters were restored to Fraktur and the profile-scale `\mathsf C` to sans serif from the frozen PDF fonts. Wording, markers, pagination, and mathematics were unchanged; exact locations are recorded in `evidence/integration/NOTATION_AUDIT.md`.
- Inspected renders: `page-061.png`, `page-062.png`, `page-063.png`, `page-064.png`, `page-065.png`, and `page-066.png` under `sources/official/paper/renders/180dpi/`.
- Page count: 6.
- Formula-marker count: 200 total: 33, 22, 40, 34, 35, and 36 on pages 61--66 respectively.
- Figure count: 0.
- Unresolved uncertainty IDs: none; `UNCERTAINTIES.jsonl` is intentionally zero bytes.

## Range structure

Page 61 continues the proof of Proposition 5.5 from the preceding range. Page 62 closes that proof, begins Section 6, and begins Subsection 6.1. Page 65 begins Lemma 6.1 and its proof; the proof crosses the page boundary after the words "This graph has" and closes on page 66. Page 66 begins Subsection 6.3 and ends mid-sentence, which continues on page 67. Accordingly, a fragment-only `lacheck` correctly reports one unmatched `\end{proof}`: its matching opening belongs to the preceding fragment. All environments opened within this fragment are otherwise balanced.

## Extraction defects resolved by the page images

The untrusted extraction flattened the distinct evaluated derivative glyphs into ordinary letters, lost the overlines on the two closed auxiliary rectangles in equation (6.13), and obscured several floors, superscripts, subscripts, display groupings, and delimiter scopes. The page images controlled each of those readings. Physical line-wrap hyphenation was removed only where it joined an ordinary word; lexical hyphens and source punctuation were retained.

Every visible substantive item in this range was transcribed in source order. Every inline mathematical occurrence and every displayed formula has a stable marker in visual order. No figure occurs in this range. No correction, paraphrase, translation, or teaching addition was introduced.

This range-level pass is an independent transcription check only. Root integration, cumulative compilation, cross-reference resolution, page correspondence, and rendered visual comparison remain required.
