# Independent transcription report: PDF pages 037--042

- Range record: `NS-TRANSCRIPTION-PP037-042`
- Frozen authority: `sources/official/paper/navier-stokes.pdf`
- Frozen PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Confirmed source extent: 166 pages, US Letter, PDF 1.5
- Output: `reconstruction/sections/pp037-042.tex`
- Output byte length after notation audit: 28,035
- Output SHA-256 after notation audit: `34962ea692d33c871c69aefad76f11d4fc967bd3674d00fcadacdc58f7ebb08b`
- Page count transcribed and independently checked: 6
- Marked mathematical occurrences: 280
- Source figures: 0
- Unresolved uncertainties: 0

## Inputs inspected

Every page was checked against the frozen PDF, the full-page 180 dpi render, and the untrusted per-page extraction draft. The inspected render files and their SHA-256 hashes are:

| PDF page | Render | SHA-256 |
|---:|---|---|
| 37 | `sources/official/paper/renders/180dpi/page-037.png` | `6e3c4c6a10c1e95089fd0e43e89a226c3e475f12441d11492d78bd8c14e009fb` |
| 38 | `sources/official/paper/renders/180dpi/page-038.png` | `5d261f7bc731aed1fb9ac739552e2f757cd1602ac21ad992f0265a7b33fd3b96` |
| 39 | `sources/official/paper/renders/180dpi/page-039.png` | `00cc6a343804c3624db0b9366dfe3c55a4dd21b94d6d3e9a02f692c98cde910c` |
| 40 | `sources/official/paper/renders/180dpi/page-040.png` | `1eed34cbecfc579c4d2aaa42222ce44d753b5c51e7b73b78a90318abbc364628` |
| 41 | `sources/official/paper/renders/180dpi/page-041.png` | `3b1823b52813d7dce7d1eee75ae230ae401babf1c514617c8758ea555f7a2470` |
| 42 | `sources/official/paper/renders/180dpi/page-042.png` | `e604c5fc4ddcb5193efc87b9e55728065b05a78bbcc45c2dcd78f18f6961ac7a` |

The PDF itself was also interrogated directly for page geometry, text/font structure, and the relevant glyph families. In particular, direct PDF font inspection confirmed the use of Euler Fraktur for the moment/shear symbols and rsfs glyphs for the periodic primitives on page 41.

## Coverage and boundaries

The fragment begins at Proposition 4.10 item (ii). It therefore intentionally closes the `enumerate` and `proposition` environments opened by the preceding fragment. It contains item (iii), the complete proof of Proposition 4.10, all of Lemma 4.11 and its proof, Section 4.6, and Steps 1--3 of the proof of Theorem 4.6 through the end of source page 42. The fragment intentionally leaves the Theorem 4.6 proof open: page 42 ends after the comma in “both blocks are invertible,” and page 43 supplies the continuation.

Exact source page breaks are represented by six `\NSPage` markers. Equation tags (4.33)--(4.42) were retained, as were live statement/equation references and the source order of all prose and mathematics.

## Formula checks

The page-level marked-occurrence counts are:

| PDF page | `\NSi` plus `\NSFormula` count |
|---:|---:|
| 37 | 55 |
| 38 | 54 |
| 39 | 38 |
| 40 | 36 |
| 41 | 53 |
| 42 | 44 |

All IDs are unique and sequential within each page. Every displayed formula and every marked inline occurrence was compared visually with the corresponding PDF page. Formula-sensitive checks included hats and Fraktur symbols in the normalized moment vector; the coefficient `5\sqrt{2}/8` in (4.34); decimal constants without leading zero on page 38; the lifted-parameter change (4.37); the complete parameter hierarchy on page 40; the five-entry moment vectors on pages 40--42; rsfs `\mathscr A,\mathscr B`; signs in the two exact chain-rule identities; both inequalities in (4.41); the row order `(M,J,I,S,C_p)` in (4.42); and the two moment-matrix blocks at the foot of page 42.

## Extraction defects encountered and resolved

The text extraction was used only as a draft. It inserted physical-line hyphenation into ordinary words such as “Corollary” and “Proposition”; displaced radicals, hats, fractions, and vector entries; flattened calligraphic, Fraktur, and rsfs alphabets; and obscured the row structure of matrices and aligned displays. Page 37's extracted form of `5\sqrt{2}/8`, the page-40 five-entry integral vector, the page-41 exact increment vector, and the page-42 block matrices were especially unreliable. Each was resolved from the full-page visual source and direct PDF glyph/font evidence. No ambiguity remains.

## Fidelity statement

No correction, paraphrase, translation, teaching addition, or mathematical normalization was introduced. Apparent line-wrap hyphenation was removed only where it split an ordinary word. Running headers and page numbers were omitted as required because the master style supplies them. This is an agent-level independent transcription pass; cumulative compilation, cross-range boundary integration, reference resolution, and rendered comparison remain root-integration tasks.

## Notation-family audit integration, 2026-09-20

Direct MuPDF structured-font evidence and the frozen renders corrected the named logarithmic derivative to `\mathcal D_X`, the fixed amplitude normalization to `\mathsf C`, and the quadratic correction map in Equation (4.42) to `\mathcal Q_\eta`. The already-correct rsfs periodic primitives `\mathscr A,\mathscr B` were retained. Only glyph-family encodings changed; prose, formula structure, labels, page/formula markers, and ordering are unchanged. The byte count and SHA-256 above are post-audit values.
