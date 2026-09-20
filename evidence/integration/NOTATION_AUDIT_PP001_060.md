# Notation-family fidelity audit: official PDF pages 001--060 (bounded scope)

Audit date: 2026-09-20

## Exact scope

This audit covers official PDF pages **001--012 and 019--060**, and only the corresponding reconstruction fragments:

- `reconstruction/sections/pp001-006.tex`
- `reconstruction/sections/pp007-012.tex`
- `reconstruction/sections/pp019-024.tex`
- `reconstruction/sections/pp025-030.tex`
- `reconstruction/sections/pp031-036.tex`
- `reconstruction/sections/pp037-042.tex`
- `reconstruction/sections/pp043-048.tex`
- `reconstruction/sections/pp049-054.tex`
- `reconstruction/sections/pp055-060.tex`

Pages 013--018 are expressly excluded because they were audited separately. The pass was limited to glyph-family fidelity: `\mathcal`, `\mathscr`, `\mathsf`, `\mathfrak`, `\boldsymbol`, ordinary math italic, and ordinary roman. It did not alter prose, page/formula markers, formula order, equation structure, labels, references, or publication files.

No actionable family mismatch was found in `pp007-012.tex` or `pp019-024.tex`; those two files were not edited.

## Frozen evidence and method

- Frozen PDF: `sources/official/paper/navier-stokes.pdf`
- PDF size: 2,959,204 bytes
- PDF SHA-256: `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`
- Frozen renders: `sources/official/paper/renders/180dpi/page-NNN.png`
- Structured extraction tool: MuPDF `mutool` 1.23.0, `stext.json` output
- Pages 001--012 structured output: `tmp/notation_audit_pp001_060/pp001-012.json`, 589,247 bytes, SHA-256 `b837e1105271a3984aafca4569bb3c38bacc6d6191957d5e4c7207d96bc57ba6`
- Pages 019--060 structured output: `tmp/notation_audit_pp001_060/pp019-060.json`, 3,997,311 bytes, SHA-256 `3629c8169a3578ecb08ad19839db9abd6de30c69f75ac78f0ac20946598d52b9`

Every scoped page was traversed in the structured output. Candidate glyphs were classified from their embedded font runs and neighboring runs on the same PDF baseline, not from text extraction without font information. The 180-dpi frozen renders were used to check glyph appearance and mathematical role, with targeted enlarged inspection on pages 6, 19, 25, 27, 34, 36--43, 46--52, 55, 56, and 60. The coordinates below are MuPDF user-space `x,y` baselines from the structured output.

The embedded subsets used in this PDF resolve as follows:

| Embedded font | Family used in the source | Audit rule |
|---|---|---|
| `JYFHIJ+rsfs10` | rsfs script | Encode letter runs as `\mathscr` |
| `WSDGPG+EUFM10` | Euler Fraktur | Encode letter runs as `\mathfrak` |
| `PGQVUE+CMSS10`, `BNEDNK+CMSS8` | Computer Modern sans serif | Encode letter runs as `\mathsf` |
| `CFFJWH+CMSY10` | Computer Modern symbols | An uppercase *letter* run is calligraphic; operators and relation glyphs from this font are not thereby calligraphic variables |
| `UMHUTX+PazoMath-BoldItalic` | bold math italic | Encode the corresponding source vector/Greek run as `\boldsymbol` when present |
| `NSFDSI+URWPalladioL-Ital`, `KADRGS+PazoMath-Italic` | ordinary math italic | Do not add a special alphabet command |
| `MCXIFN+URWPalladioL-Roma`, `SOSTRQ+CMR10` | ordinary roman | Preserve roman text/operator/numeral use |

## Confirmed actionable mismatches and repairs

The source-line references below are post-repair line numbers.

| Fragment and source line(s) | Official PDF locator and embedded-font evidence | Confirmed repair |
|---|---|---|
| `pp001-006.tex:351` | p. 6, Equation (3.1), `R` at `(216,691)` in `JYFHIJ+rsfs10` | `\mathcal R` to `\mathscr R` |
| `pp025-030.tex:9,25-26` | p. 25, definition and (4.2): `D` at `(193,134)`, `(448,200)`, `(456,215)` in `CFFJWH+CMSY10`, with italic subscript `X` in `NSFDSI` | `D_X` to `\mathcal D_X` |
| `pp025-030.tex:51,59,62,73` | p. 25, normalization and (4.3)--(4.4): `C` at `(153,333)`, `(456,354)`, `(173,379)`, `(314,437)` in `PGQVUE+CMSS10` | fixed normalization `C` to `\mathsf C` |
| `pp025-030.tex:156,174,176-177,193` | p. 26, (4.8)--(4.10): derivative `D` at `y=370,472,506,522` in `CFFJWH+CMSY10`; normalization `C` at `(442,606)` in `PGQVUE+CMSS10` | `\mathcal D_X`; `\mathsf C` |
| `pp025-030.tex:219,221,282,354-355` | p. 27, (4.11) and (4.14), derivative `D` at `y=149,509` in `CFFJWH+CMSY10`; p. 28 proof, the two operative `D` runs at `(427,346)` and `(501,346)` in the same font | remaining named `D_X` occurrences to `\mathcal D_X` |
| `pp031-036.tex:112,115` | p. 32 theorem statement `C` at `(350,621)` and p. 33 item (i) `C` at `(300,95)`, both `PGQVUE+CMSS10` | fixed normalization to `\mathsf C` |
| `pp031-036.tex:188,196,198,207,210` | p. 34, Lemma 4.7: letter `Q` at `y=468,496,547,563,686,705` in `CFFJWH+CMSY10` | bilinear map `Q, Q_\eta` to `\mathcal Q,\mathcal Q_\eta` |
| `pp031-036.tex:288,291,293,298-299` | p. 36, Lemma 4.9: physical `T` at `(about 148,302)`, component `T` runs at `y=325,367` are `NSFDSI+URWPalladioL-Ital`; the profile `T_0` at `(212,302)`, `(94,349)`, and `y=411` is `CFFJWH+CMSY10` | physical `T,T_\theta,T_z` restored to ordinary italic while `\mathcal T_0` remains calligraphic |
| `pp031-036.tex:319,322,325` | p. 36, Proposition 4.10: `C` at `y=575` (three runs), `593`, `611`, and `625` in `PGQVUE+CMSS10` | `C_0,C` and their scale occurrences to `\mathsf C_0,\mathsf C` |
| `pp037-042.tex:103,110,157,160,165,168` | p. 37 derivative `D` at `(403,650)` in `CFFJWH+CMSY10`, normalization `C` at `(277,694)` in `PGQVUE+CMSS10`; p. 38 derivative at `(456,329)` and normalization at `(395,342)`, `(304,373)`, `(329,391)` | `\mathcal D_X`; `\mathsf C` |
| `pp037-042.tex:297-304,312,314,319,323` | p. 39 normalization `C` at `(464,624)`, `(278,636)`, and three runs at `y=675`; p. 40 normalization at `(136,136)`, `(347,155)`, `(246,186)`, `(393,217)`, all in `PGQVUE+CMSS10` | all occurrences of the fixed normalization to `\mathsf C`/`\mathsf C_0` |
| `pp037-042.tex:438-446` | p. 41 shear identities: `D` at `(242,359)`, `(294,359)`, `(355,388)`, `(260,396)`, and two runs at `y=416`, all `CFFJWH+CMSY10` | `D_X` to `\mathcal D_X`; existing `\mathscr A,\mathscr B` retained |
| `pp037-042.tex:576` | p. 42, (4.42), `Q` at `(359,548)` in `CFFJWH+CMSY10` | `Q_\eta` to `\mathcal Q_\eta` |
| `pp043-048.tex:10-18,29,37,48,55,62-64` | p. 43: `Q` at `(94,134)` is `CFFJWH+CMSY10`; `d` at `(309,134)`, `c` at `(298,177)`, and `p` at `y=291,359,451` are ordinary `NSFDSI`; moment `m` at `y=245,390,430` is `WSDGPG+EUFM10` | `\mathcal Q`; remove false `\boldsymbol` from ordinary `d,c,p`; encode moment vector as `\mathfrak m` |
| `pp043-048.tex:89-90` | p. 43, two `C` runs at `(145,611)` and `(224,611)` in `PGQVUE+CMSS10` | fixed normalization to `\mathsf C` |
| `pp043-048.tex:134,156` | p. 44: shear `s` at `(460,253)` and `(315,404)` in `WSDGPG+EUFM10`; stress-coordinate `p` at `(295,404)` in ordinary `NSFDSI` | `\mathfrak s`; ordinary `p_s` (remove false bold family) |
| `pp043-048.tex:300-301,394,411-412,426,431,521` | p. 46 `C` at `x=281,379,y=127` and `(172,610)`; p. 47 at `x=241,292,y=134`, `(133,239)`, `(519,254)`; p. 48 `(508,162)`, all `PGQVUE+CMSS10` | every fixed-normalization occurrence to `\mathsf C` |
| `pp043-048.tex:500` | p. 47, transpose `T` at `(441,681)` in `BNEDNK+CMSS8` | `{}^{\mathrm T}` to `{}^{\mathsf T}` |
| `pp049-054.tex:30,169,194,206` | p. 49 `(133,357)`, p. 50 `(347,597)`, p. 51 `(410,173)` and `(270,309)`, all `PGQVUE+CMSS10` | exactly four fixed-normalization occurrences to `\mathsf C`; no other `C` in this range changed |
| `pp055-060.tex:24,65,67` | p. 55: residual `R` at `(240,248)` in `JYFHIJ+rsfs10`; coefficient residual `r` at `(276,530)` and `(414,530)` in `WSDGPG+EUFM10` | `\mathscr R`; `\mathfrak r_{\theta,n},\mathfrak r_{z,n}` |
| `pp055-060.tex:138-142,150` | p. 56: generic Stokes `S` at `y=339,369,376,399` is ordinary `NSFDSI`; every positive-order `S_n` in (5.27) and its Cartesian formula is `CFFJWH+CMSY10` at `x=267,404,y=444`, `x=278,361,y=460`, `(219,517)` | generic `S` remains ordinary; specific positive-order streamfunction becomes `\mathcal S_n` |
| `pp055-060.tex:434,442` | p. 59: residual `R` at `(112,489)`, `(198,489)`, `(156,546)` in `JYFHIJ+rsfs10` | `\mathscr R` |
| `pp055-060.tex:477,482-484,494,496,503,509-512,517,522,529` | p. 60: residual `R` `(159,210)` and derivative `D` at `y=322,341,361,414` are `JYFHIJ+rsfs10`; physical stress `T` at `y=192,210,256,381,414,431` and positive-order `S_n` `(330,269)` are `CFFJWH+CMSY10` | `\mathscr R`, `\mathscr D^I`, `\mathcal T_{\mathrm{phys}}`, `\widehat{\mathcal T}`, and `\mathcal S_n` |

## Deliberate non-changes and disambiguations

- **Stress notation is role-sensitive.** On p. 19 at `y=611`, both profile glyphs `T_0` (`x=85` and `x=157`) are `CFFJWH+CMSY10`, while the physical stress `T` at `x=97` is ordinary italic `NSFDSI`. The glossary line therefore remains `\mathcal T_0,T=q^{-A-1/2}\mathcal T_0`. The same distinction appears on p. 27 at `y=273`: physical `T` is ordinary italic at `x=129`, while profile `T_0` is `CFFJWH+CMSY10` at `x=193`. Conversely, the named base stress `\mathcal T_{\mathrm{phys}}` on p. 60 is explicitly calligraphic.
- **Interval names are not uniform by spelling alone.** On p. 21 the reserved profile intervals at `y=482` use calligraphic `I` (`CFFJWH+CMSY10`), while `I_m` at `(107,532)` is ordinary italic `NSFDSI`; the existing distinction was retained.
- **Generic and positive-order streamfunctions differ.** The p. 56 generic `S` is ordinary italic, but `S_n` is calligraphic by the distinct embedded font runs listed above. The p. 60 reference at `(330,269)` confirms the calligraphic positive-order family. This resolves a visual ambiguity without relying on extracted text.
- **The fixed normalization is not every letter `C`.** `C_Q,C_N,C_p,C_k,C_\Psi,C_{\mathrm{rep}},C_{N,m},C^k,C_c^\infty` and generic estimate constants remain ordinary italic/roman as printed. For example, p. 43 generic bound constants near `y=203,245,291,316,329,341,359` are ordinary `NSFDSI`, unlike the normalization at `y=611` in `PGQVUE+CMSS10`.
- **Bold vectors remain bold where the source is bold.** The p. 52 coefficient vectors `\boldsymbol\alpha_n,\boldsymbol\beta_n` and bold/roman right-hand-side vectors were already source-faithful. Only the false page-43 bold encodings of ordinary `d,c,p` and Fraktur `m` were removed.
- `CFFJWH+CMSY10` also supplies operators, delimiters, and relations. Only uppercase letter runs whose mathematical role and render identify a named calligraphic variable were changed.

## Output identity after repair

| Fragment | Pre-audit bytes / SHA-256 | Post-audit bytes / SHA-256 |
|---|---|---|
| `pp001-006.tex` | 21,543 / `328b99f3c4a51e7a9f1f4f63e9d04e28c5d8296143a43d9bdafa06dbe8ca53e5` | 21,543 / `a5efa27522db4b97a5d18e90b8414bca74e44f2e98ed2de0477e9c5bbb78080d` |
| `pp007-012.tex` | unchanged | 22,842 / `077c50a30e68490736f531773ccc5bfdf168ca03df5703087a18d7ba94c2fc12` |
| `pp019-024.tex` | unchanged | 23,024 / `bbf2df9723d4720b63cab67fcac8e3818a454e020ca688eab543fbbd258a77ab` |
| `pp025-030.tex` | 26,436 / `d9282b524531207ce59f192f3ffa159451aa13583f7568bdd4468bddc0f7b17d` | 26,593 / `79f3c38dc7d0c46ca254632bcf74b7712997f23325883bbf72ee46ec82e43d95` |
| `pp031-036.tex` | 28,349 / `a50fcfdf76d0776ff80a6d892a6e708b4075b3cc7e3de1750e42ae4814ced25d` | 28,407 / `0e6b8389b167db12a1d3b79d450fdbd2581be66b065709e022f7175a583ababc` |
| `pp037-042.tex` | 27,845 / `c5f5573477200ed0ed92ce789b5e17225671bcc1b82c94dbc5325734e51c5f67` | 28,035 / `34962ea692d33c871c69aefad76f11d4fc967bd3674d00fcadacdc58f7ebb08b` |
| `pp043-048.tex` | 27,418 / `172f882adb90af8fd938e04a81c2cfb1a6d8013312e96d0a39c31bf5742d56a6` | 27,381 / `e2c83a1f3693f8bed47b426917a7586566b85e5b3617fb9dace89f785353359d` |
| `pp049-054.tex` | 25,791 / `5cd583c01a4d75379db44886e414bb0ddbd54884e9beaec8ed368ec557828cff` | 25,823 / `2a5bb1406c6994122c2b2f6abde3eca056e80993740c5ce15c731ef6f767c5b2` |
| `pp055-060.tex` | 29,784 / `99203b174a967afa96b4f04c8212bedc99d231e142b2f05a094c090b650a106b` | 29,986 / `5d5f23647375e6c69e60d866ddf6802d40f1e7fbc7e4fe45f27516d05b7a6864` |

The two existing `\qquad` repairs in `pp025-030.tex` are present in the post-audit file. A whole-scope PCRE2 scan found no raw unescaped `quad` or `qquad`. All nine fragments retain their original page-marker, formula-marker, and line counts; the seven edited fragments retain totals 69, 244, 281, 280, 234, 206, and 288 marked mathematical occurrences respectively. Residual scans found no remaining ordinary italic `D_X` in the audited named-operator contexts, no false `\boldsymbol` in `pp043-048.tex`, no ordinary italic quadratic-map `Q_\eta` in the repaired lemma/equation contexts, and no ordinary italic residual operator `R` in the repaired `\mathscr R` contexts.
