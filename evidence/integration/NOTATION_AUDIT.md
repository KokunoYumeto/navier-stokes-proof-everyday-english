# Notation audit against the frozen official PDF

Audit target: `sources/official/paper/navier-stokes.pdf`, SHA-256
`0E779481C4DA40BD28D1E642E1D8CA57447D129610DF28DFA5A11E9AF8AE228F`.
Completed scope: official pages 13-18 and 61-120 only.  Pages 121-166 were
not audited in this pass, so this report makes no claim about notation-font
agreement in that tail.  Within the completed scope, pages 79-84 were checked
and produced no actionable mismatch.
The line references below are to the stable reconstruction fragments as read on
2026-09-20 UTC.  I inspected the existing 180 dpi page renders and MuPDF
structured-text/content streams; I did not infer font roles from extracted text
alone.

Embedded-font key used below:

- `CFFJWH+CMSY10`: calligraphic math capitals (`\mathcal`).
- `JYFHIJ+rsfs10`: script capitals (`\mathscr`).
- `PGQVUE+CMSS10`: sans-serif math capitals (`\mathsf`).
- `WSDGPG+EUFM10`: Fraktur letters (`\mathfrak`).
- `DIATYS+URWPalladioL-BoldItal`: bold italic vector glyphs (`\boldsymbol`).
- `NSFDSI+URWPalladioL-Ital`: ordinary math italic.

## Confirmed actionable mismatches

All entries in this table were subsequently corrected in the listed fragments
on 2026-09-20; the table preserves the pre-correction form as the audit trail.

| Official page(s) | Fragment and exact line(s) | Pre-correction form | Required form | PDF/content-stream evidence |
|---|---|---|---|---|
| 15-16 | `reconstruction/sections/pp013-018.tex`: 134, 137, 140, 143, 161; 195, 206 | ordinary italic `B` | `\mathcal B` at every listed occurrence | The PDF has five `B` glyphs on p.15 and two on p.16 in `CFFJWH+CMSY10`; the renders show the calligraphic azimuthal coefficient. |
| 17 | `pp013-018.tex`: 357-358 | `\mathsf r` | `\mathfrak r` | Both p.17 `r` glyphs are in `WSDGPG+EUFM10` (stream y=676), not CMSS10. |
| 18 | `pp013-018.tex`: 377, 388, 391, 395 | ordinary italic `W_\alpha`, `M_\alpha`, `S_\alpha` | `\mathsf W_\alpha`, `\mathsf M_\alpha`, `\mathsf S_\alpha` | P.18 has two occurrences of each class letter in `PGQVUE+CMSS10`. |
| 63-65 | `reconstruction/sections/pp061-066.tex`: p.63 lines 86-87, 91, 105, 107; p.64 line 126; p.65 lines 192, 223 | `\mathsf t`, `\mathsf t_*`, `\mathsf r` | `\mathfrak t`, `\mathfrak t_*`, `\mathfrak r` | `WSDGPG+EUFM10` supplies p.63 `t` x4/`r` x3, p.64 `t`/`r` x1, and p.65 `t` x2. |
| 65 | `pp061-066.tex`: 190 | ordinary italic profile-scale `C` | `\mathsf C` | The sole p.65 scale `C` is in `PGQVUE+CMSS10` (stream y=239). |
| 67-68 | `reconstruction/sections/pp067-072.tex`: 9 (both occurrences), 159 | ordinary italic `D_\ell` | `\mathcal D_\ell` | P.67 has two `D` glyphs and p.68 one `D` glyph in `CFFJWH+CMSY10`. |
| 69-71 | `pp067-072.tex`: p.69 lines 237-239, 292; p.70 lines 315, 325, 387; p.71 lines 434, 442, 444, 459, 461, 464-465, 470, 472, 485 | `\mathrm M`, `\mathrm W`, `\mathrm S` | `\mathsf M`, `\mathsf W`, `\mathsf S` | All coefficient-class glyphs at these locations are `PGQVUE+CMSS10` (p.69: Mx2/W/S; p.70: Sx2/W; p.71: Mx6/Wx9). |
| 71 | `pp067-072.tex`: 485, 494-499 | ordinary italic generic-class placeholder `C`/`C_\alpha` | `\mathcal C`/`\mathcal C_\alpha` | The eleven generic `C` glyphs on p.71 are `CFFJWH+CMSY10`.  This is distinct from the p.65 sans-serif scale `\mathsf C`. |
| 72 | `pp067-072.tex`: 592, 594 | ordinary italic `L_{i_0}`, `L_{\mathrm{abs}}` | `\mathcal L_{i_0}`, `\mathcal L_{\mathrm{abs}}` | Both p.72 `L` glyphs are `CFFJWH+CMSY10`. |
| 75-76 | `reconstruction/sections/pp073-078.tex`: 189, 237 | `\mathsf t_*` | `\mathfrak t_*` | Each page has one `t` in `WSDGPG+EUFM10`. |
| 85 | `reconstruction/sections/pp085-090.tex`: 5 | ordinary italic named stress `T_{0,*}` | `\mathcal T_{0,*}` | P.85 y=112 uses `CFFJWH+CMSY10` for this `T`.  This is the stress target, not the sans-serif primitive operator below. |
| 85-88 | `pp085-090.tex`: p.85 lines 15, 42-43, 81; p.86 lines 109, 113-114, 124; p.87 lines 213, 216, 233-234, 236, 240, 252-254, 278-279; p.88 lines 316-317 | ordinary italic coefficient classes `W`, `M`, `S` | `\mathsf W`, `\mathsf M`, `\mathsf S` | The matching class glyphs are all `PGQVUE+CMSS10` (p.85 Mx1/Wx3; p.86 Wx4; p.87 Mx5/Wx6; p.88 M/S).  Named fields such as the first `W_0^{\mathrm{as}}` on p.85 and tensors `W_{ab}` remain ordinary italic. |
| 89 | `pp085-090.tex`: 376, 379, 381 | ordinary italic `t_*` | `\mathfrak t_*` | Three p.89 `t` glyphs are in `WSDGPG+EUFM10`. |
| 90 | `pp085-090.tex`: 466, 504 | ordinary italic `D_e` | `\mathcal D_e` | Both p.90 `D` glyphs are `CFFJWH+CMSY10`. |
| 90 | `pp085-090.tex`: 467, 478, 500, 504 | `\mathcal T_e` | `\mathsf T_e` | All four p.90 primitive-operator `T` glyphs are `PGQVUE+CMSS10`. |
| 90 | `pp085-090.tex`: 493, 501 | ordinary italic class `M_\alpha` | `\mathsf M_\alpha` | Both p.90 class glyphs are `PGQVUE+CMSS10`. |
| 91 | `reconstruction/sections/pp091-096.tex`: 43; 54 | ordinary italic class `M_\alpha`; `\mathsf r` | `\mathsf M_\alpha`; `\mathfrak r` | P.91 uses `PGQVUE+CMSS10` for M and `WSDGPG+EUFM10` for r. |
| 92 | `pp091-096.tex`: 121, 125 | ordinary italic `I_{\mathrm{mean}}` | `\mathcal I_{\mathrm{mean}}` | Besides the already-correct `\mathcal I_c`, the two interval-name `I` glyphs are also `CFFJWH+CMSY10`. |
| 92-96 | `pp091-096.tex`: p.92 lines 139-141; p.93 lines 171, 197; p.95 lines 368, 370; p.96 line 468 | `\mathcal T_0`, `\mathcal T_1`, `\mathcal T_2` | `\mathsf T_0`, `\mathsf T_1`, `\mathsf T_2` | The corresponding `T` glyphs are `PGQVUE+CMSS10` (p.92 x4, p.93 x2, p.95 x2, p.96 x1). |
| 93-96 | `pp091-096.tex`: p.93 lines 182-185, 204-206, 223-227; p.95 line 443; p.96 lines 461, 470 | ordinary italic class `M`/`S` | `\mathsf M`/`\mathsf S` | CMSS10 counts agree exactly: p.93 Mx8/Sx2, p.95 Mx1, p.96 Mx4. |
| 93-95 | `pp091-096.tex`: p.93 lines 233-234, 238; p.94 line 295; p.95 line 423 | `\mathsf r`, `\mathsf t_*` | `\mathfrak r`, `\mathfrak t_*` | EUFM10 supplies p.93 `r` x4, p.94 `t` x1, and p.95 `t` x1. |
| 97-102 | `reconstruction/sections/pp097-102.tex`: p.97 lines 42-43, 46; p.98 lines 126-127; p.99 lines 186-193, 209-210, 218-223, 226; p.100 line 310; p.101 lines 358-359, 380, 385, 389, 392; p.102 lines 432, 472, 474, 476 | ordinary italic coefficient classes `W`, `M`, `S` | `\mathsf W`, `\mathsf M`, `\mathsf S` | Every matching glyph is `PGQVUE+CMSS10` (per-page counts: p.97 M2/S1; p.98 M/S; p.99 M12/S2; p.100 W/M/S; p.101 W6; p.102 W3/M2). |
| 99, 102 | `pp097-102.tex`: p.99 lines 161, 212, 218; p.102 line 400 | `\mathsf t_*` | `\mathfrak t_*` | EUFM10 gives p.99 `t` x3 and p.102 `t` x1. |
| 100 | `pp097-102.tex`: 251 | `\mathcal T_0` | `\mathsf T_0` | The p.100 `T` is `PGQVUE+CMSS10`. |
| 101-102 | `pp097-102.tex`: p.101 lines 368, 374, 384; p.102 lines 406, 431 | `\mathcal L_m` | `\mathscr L_m` | The five operator `L` glyphs are `JYFHIJ+rsfs10` (p.101 x3, p.102 x2). |
| 103 | `reconstruction/sections/pp103-108.tex`: 67, 69, 73 | `\mathcal H_j` (four occurrences) | `\mathscr H_j` | All four p.103 `H` glyphs are `JYFHIJ+rsfs10` (stream y=595, 612, 628). |
| 103-108 | `pp103-108.tex`: p.103 lines 5-6; p.104 lines 90, 92; p.105 lines 172, 192, 230; p.106 lines 284-286, 296-299; p.107 lines 334-335, 359, 362, 365-366, 376-377; p.108 lines 467-468, 485, 487, 496 | ordinary italic coefficient classes `W`, `M`, `S` | `\mathsf W`, `\mathsf M`, `\mathsf S` | All matching glyphs are `PGQVUE+CMSS10`; e.g. p.103 W/M, p.106 W3/M3/S, p.107 W/M5/S2, and p.108 W2/M/S2. |
| 104, 108 | `pp103-108.tex`: 116, 449 | `\mathcal T_0` | `\mathsf T_0` | Each `T` is `PGQVUE+CMSS10` (p.104 y=252; p.108 y=293). |
| 105 | `pp103-108.tex`: 175 | ordinary italic matrix/map `H^{-1}` | `\mathsf H^{-1}` | P.105 y=148 uses `PGQVUE+CMSS10`.  This is not the ordinary exponent label `H_0` on p.107. |
| 108 | `pp103-108.tex`: 464 | `\mathcal L_m` | `\mathscr L_m` | P.108 y=383 uses `JYFHIJ+rsfs10`. |
| 109 | `reconstruction/sections/pp109-114.tex`: 37 | scalar-looking `y+d\Sigma` | `\boldsymbol y+d\Sigma` | The vector `y` at p.109 y=355 is `DIATYS+URWPalladioL-BoldItal`; the component `y_\sigma` at line 35 is separately ordinary italic and must stay so. |
| 109-111 | `pp109-114.tex`: p.109 lines 23, 31, 54; p.110 lines 92-94, 119-122, 167, 169-170, 175, 177; p.111 lines 185-186, 205 | ordinary italic coefficient classes `W`, `M`, `S` | `\mathsf W`, `\mathsf M`, `\mathsf S` | Matching PDF glyphs are CMSS10 (p.109 M/W2; p.110 M7/W2/S2; p.111 M2/S2).  Moment names `M_e` remain ordinary italic. |
| 110 | `pp109-114.tex`: 111; 131 | `\mathcal T_1`; ordinary italic `t_*` | `\mathsf T_1`; `\mathfrak t_*` | P.110 has `T` in `PGQVUE+CMSS10` (y=212) and `t` in `WSDGPG+EUFM10` (y=336). |
| 113 | `pp109-114.tex`: 319, 324 | `\mathcal T_0` | `\mathsf T_0` | Both p.113 `T` glyphs are `PGQVUE+CMSS10`. |
| 112, 114 | `pp109-114.tex`: p.112 lines 298, 302, 307-311; p.114 lines 475, 480-481 | over-styled `\mathcal A_j`, `\mathcal B_j` | ordinary `A_j`, `B_j` | Every corresponding p.112/p.114 glyph is `NSFDSI+URWPalladioL-Ital` (not CMSY10).  This is the same incremental-potential distinction visible again in (9.21) on p.115. |
| 114 | `pp109-114.tex`: 461 | ordinary italic `F(u,p)` | `\mathcal F(u,p)` | P.114 y=457 uses `CFFJWH+CMSY10` for F and `JYFHIJ+rsfs10` for the already-correct `\mathscr R`. |
| 115 | `reconstruction/sections/pp115-120.tex`: 38-39, final summand in each line only | `\sum\chi(a_jq)\mathcal A_j`, `\sum\chi(a_jq)\mathcal B_j` | `\sum\chi(a_jq)A_j`, `\sum\chi(a_jq)B_j` | The p.115 stream/render is deliberately mixed: the main `\mathcal A,\mathcal B` and bases `\mathcal A_0,\mathcal B_0` are CMSY10, but the summand `A_j,B_j` is ordinary `NSFDSI+URWPalladioL-Ital`.  The current source has five calligraphic A/B occurrences; the PDF has four of each plus one ordinary summand. |
| 117 | `pp115-120.tex`: 171 (one), 172 (three), 173, 182, 185 | ordinary italic Stokes streamfunction `S_n,S,S_0` | `\mathcal S_n,\mathcal S,\mathcal S_0` | All seven p.117 streamfunction `S` glyphs are `CFFJWH+CMSY10` (rendered in (10.1) and the two following uses).  These are not the sans-serif coefficient class `\mathsf S`. |
| 119 | `pp115-120.tex`: 330, 335, 337 | `\mathcal K_0` | ordinary `K_0` | The compact-test-set `K_0` at p.119 y=134/165/166 is `NSFDSI+URWPalladioL-Ital`.  By contrast, the fixed support set `\mathcal K` later on that page (lines 409, 411; stream y=676/689) is CMSY10. |

## Checked distinctions that are already correct

- **Pages 82-84 (`pp079-084.tex`)**: the matrix/map `\mathsf H`, coefficient
  classes `\mathsf W` and `\mathsf M`, and vector
  `\boldsymbol y` are correct (notably lines 320-341, 358-359, 387-390,
  460-470, 492-494, 524-596).  The PDF uses CMSS10 for H/W/M and
  `URWPalladioL-BoldItal` for vector y.  Scalar components `y_\sigma` are
  ordinary italic in both source and PDF.  No p.79-84 correction is needed.
- **Stress versus primitive T**: `\mathcal T_{\mathrm{phys},a}` on p.89
  (lines 361, 369) and `\mathcal T_{0,*}` on pp.82-84 are correctly
  calligraphic.  Only p.85 line 5 lost the calligraphic stress glyph.  In
  contrast, the radial primitives `T_e,T_0,T_1,T_2` on pp.90-113 are
  sans-serif, as itemized above.
- **Page 115 A/B**: retain the calligraphic main and base symbols at lines
  32, the left/base portions of 38-39, and line 41.  Only the incremental
  `A_j,B_j` summands are ordinary italic.  The 180 dpi render makes this
  contrast visible and the stream assigns the two roles to CMSY10 versus
  Palatino Italic.
- **Compact-set K**: `\mathcal K` is correct on p.117 lines 215/218,
  p.118 lines 281/315, p.119 lines 409/411, and p.120 lines 438/480/486.
  Exterior heat-field `K(r,\tau)` is ordinary italic, also correctly.  The
  only over-styled K is `K_0` on p.119.
- **Epsilon**: every audited fragment uses `\varepsilon`; no `\epsilon`
  occurrence was found.  The frozen PDF uses the PazoMath-Italic U+03B5
  glyph at the checked occurrences, matching `\varepsilon`; no epsilon swap
  is required.
- **Do not bulk-style names**: `W_{ab}` (Reynolds tensor), `M_i`, `M_e`,
  `M_\theta,M_z`, and exponent labels such as `H_0` are ordinary italic in
  the PDF.  The sans-serif corrections above apply only to the explicitly
  identified coefficient classes/maps.
