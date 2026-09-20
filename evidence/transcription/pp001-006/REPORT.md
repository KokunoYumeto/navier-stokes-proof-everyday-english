# Source-faithful transcription report: PDF pages 001--006

- Range record: `NS-TRANSCRIPTION-PP001-006`
- Inclusive source range: PDF pages 1--6
- Frozen PDF: `sources/official/paper/navier-stokes.pdf`
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Output fragment: `reconstruction/sections/pp001-006.tex`
- Output bytes after notation audit: 21,543
- Output SHA-256 after notation audit: `a5efa27522db4b97a5d18e90b8414bca74e44f2e98ed2de0477e9c5bbb78080d`
- Page checks: `evidence/transcription/pp001-006/PAGE_CHECKS.jsonl`
- Uncertainty ledger: `evidence/transcription/pp001-006/UNCERTAINTIES.jsonl` (zero bytes; no unresolved readings)

## Inspected source material

The frozen PDF itself was queried directly with Poppler: `pdfinfo` reported 166 letter-size pages and PDF version 1.5, and `pdftotext -f 1 -l 6 -layout` was read for this exact range. Every page was also independently inspected in the following 180 dpi renders:

- `sources/official/paper/renders/180dpi/page-001.png`
- `sources/official/paper/renders/180dpi/page-002.png`
- `sources/official/paper/renders/180dpi/page-003.png`
- `sources/official/paper/renders/180dpi/page-004.png`
- `sources/official/paper/renders/180dpi/page-005.png`
- `sources/official/paper/renders/180dpi/page-006.png`

The corresponding untrusted extraction drafts `page-001.txt` through `page-006.txt` were used only for routing and prose comparison. The render controlled all notation, layout relations, page breaks, displayed mathematics, and figure captions.

## Coverage

| PDF page | Formula markers | Figures | Result |
|---:|---:|---|---|
| 1 | 13 | none | pass |
| 2 | 7 | none | pass |
| 3 | 20 | none | pass |
| 4 | 21 | `NS-FIG-1` | pass |
| 5 | 7 | `NS-FIG-2` | pass |
| 6 | 1 | none | pass |
| **Total** | **69** | **2** | **6 pages checked** |

The fragment contains one `\NSPage` marker for each source page. Its 69 formula IDs are unique and consecutive within each page. Static checks also found balanced counts of LaTeX `begin` and `end` environments. The six page-check lines parse as valid JSON and their formula counts agree with the fragment.

Figure 1 on page 4 and Figure 2 on page 5 were visually inspected, including their captions and visible internal labels. In accordance with the transcription protocol, the source currently contains `\NSFigurePlaceholder{NS-FIG-1}` and `\NSFigurePlaceholder{NS-FIG-2}` until the root integration stage supplies separately extracted, hashed, and equivalence-checked vector crops. The captions and live labels `fig:1` and `fig:2` are present now.

The following source-page transitions were preserved rather than rewritten as new prose paragraphs:

- page 2 to page 3: “Our construction also exploits / dynamical amplification”;
- page 3 to page 4: “The radial / and axial scales” with Figure 1 at the top of page 4;
- page 4 to page 5: “transport and diffusion / rates satisfy” with Figure 2 at the top of page 5.

## Extraction defects encountered

- Page 1 text extraction misplaced an integral glyph into the domain following `\mathbb R^3\times` and flattened the theorem's display alignment. The render supplied the checked reading.
- Page 2 extraction visually displaced the superscripts and subscripts in `L_t^\infty L_x^3`; the render supplied their exact order.
- Physical line-wrap hyphenation in such words as “fundamental,” “three-dimensional,” “finite-energy,” “hypodissipative,” “constructions,” “successive,” and “azimuthal” was removed while lexical hyphens were retained.
- The page 4 and page 5 extraction did not preserve the vector figure artwork and flattened fraction, superscript, subscript, and alignment relations in the displayed scale estimates. Those relations were transcribed from the renders.

## Scope statement

This is an agent-level transcription and formula-visual-check pass for pages 001--006. No source wording or mathematical notation was corrected, normalized, paraphrased, translated, or supplemented. No suspected source defect remains unresolved in this range. Root integration must still perform cumulative compilation, cross-reference checking, vector-figure insertion, source-to-render correspondence, and final rendered-page comparison before accepting the range into a released edition.

## Notation-family audit integration, 2026-09-20

Direct MuPDF structured-font evidence and the frozen page render identify the residual operator in Equation (3.1) as an rsfs glyph. The fragment's `\mathcal R` was therefore corrected to source-faithful `\mathscr R`. This changes only the encoded glyph family; prose, formula structure, the equation label, and all source/formula/page markers are unchanged. The byte count and SHA-256 above are post-audit values.
