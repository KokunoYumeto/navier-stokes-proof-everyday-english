# Transcription report: PDF pages 049--054

- Range: official PDF pages 49 through 54, inclusive.
- Frozen authority: `sources/official/paper/navier-stokes.pdf`.
- PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f` (rechecked before the page receipts were written).
- Output: `reconstruction/sections/pp049-054.tex`.
- Output SHA-256 after notation audit: `2a5bb1406c6994122c2b2f6abde3eca056e80993740c5ce15c731ef6f767c5b2`.
- Output size after notation audit: 25,823 bytes.
- Inspected renders: `page-049.png`, `page-050.png`, `page-051.png`, `page-052.png`, `page-053.png`, and `page-054.png` under `sources/official/paper/renders/180dpi/`; each is 1530 by 1980 pixels.
- Page markers: 6.
- Marked formula occurrences: 206 total (168 inline and 38 display).
- Per-page formula counts: page 49: 28; page 50: 48; page 51: 20; page 52: 44; page 53: 25; page 54: 41.
- Figures: 0.
- Unresolved uncertainties: 0; `UNCERTAINTIES.jsonl` is therefore a zero-byte file.

## Range boundaries and structure

Page 49 begins in the final paragraph of the proof of Lemma 5.1 and closes that proof before subsection 5.2. Pages 50--54 contain the complete statement and proof of Lemma 5.2. The display at the foot of page 50 is followed on page 51 by the same sentence's words “with mutually disjoint ordered supports.” Page 53 ends after the word “from”; page 54 resumes with the live reference to equation (5.19). Page 54 then closes Lemma 5.2 and opens subsection 5.3. These cross-page positions are represented directly by the `\NSPage` markers; no artificial paragraph or environment boundary was introduced.

## Extraction defects resolved by visual inspection

The extracted text was used only as an untrusted draft. It flattened multiline displays and frequently obscured the distinctions among the script residual `\mathscr R`, the Fraktur coefficient residual `\mathfrak r`, the calligraphic stress `\mathcal T`, and ordinary roman or italic letters. It also displaced superscripts and subscripts in the residual formulas, flattened the vectors and transposes in the moment systems, split radicals and quotients, and made several integral limits and grouping delimiters ambiguous. Every such item was resolved against the corresponding full-page render and, for the densest formulas on pages 49 and 50, against enlarged crops of those renders. The resulting formula IDs are sequential in visual order on every page, with no duplicate or missing ID in the range.

## Scope statement

This is an agent-level independent transcription check. No source correction, translation, paraphrase, or teaching addition was introduced. Apparent source defects would have been recorded separately rather than repaired silently; none remained unresolved in this range. Root integration, compilation, cross-reference resolution, cumulative page correspondence, and rendered-output comparison remain separate acceptance stages.

## Root integration repair

The initial fragment had accidentally appended the page-049 block following equation (5.9), including formula markers `NS-F-P049-020` through `NS-F-P049-028` and equations (5.10)--(5.11), after all page-054 content. Root moved that exact unchanged block to its visually verified position immediately before `\NSPage{050}`. A strengthened audit now fails whenever a formula marker's declared PDF page differs from the page-marker span that contains it. That repaired source order remains unchanged after the later notation audit.

## Notation-family audit integration, 2026-09-20

Direct MuPDF structured-font evidence and the frozen renders identify exactly four occurrences of the fixed amplitude normalization in this range as sans-serif `\mathsf C`: `R/\mathsf C` on pages 49 and 50, `\mathsf C/R` on page 51, and `\mathsf C^{-2}` in Equation (5.15). All other `C`-symbols in the range remain ordinary constants or function-space notation. No prose, marker, formula structure, or repaired source order changed. The byte count and SHA-256 above are post-audit values.
