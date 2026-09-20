# Notation-font fidelity audit: official PDF pages 121--166

Date: 2026-09-20  
Status: complete for the stated range and families

## Scope and authority

This audit compares every official source page from PDF page 121 through PDF page 166, inclusive, with these nine reconstruction fragments:

- `reconstruction/sections/pp121-126.tex`
- `reconstruction/sections/pp127-132.tex`
- `reconstruction/sections/pp133-138.tex`
- `reconstruction/sections/pp139-144.tex`
- `reconstruction/sections/pp145-150.tex`
- `reconstruction/sections/pp151-156.tex`
- `reconstruction/sections/pp157-162.tex`
- `reconstruction/sections/pp163-164.tex`
- `reconstruction/sections/pp165-166.tex`

The audited distinctions are calligraphic (`\mathcal`), RSFS script (`\mathscr`), sans serif (`\mathsf`), Fraktur/blackletter (`\mathfrak`), bold math, ordinary math italic, and upright roman. Named parameters, named radii, reference-profile suffixes, class labels, operators, spaces, and coefficient families were classified by their actual embedded PDF font and visible glyph, not merely by the extracted Unicode letter. Context-sensitive uses were not normalized globally.

The sole source authority is `sources/official/paper/navier-stokes.pdf`, SHA-256 `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`. All 46 supplied 180-dpi page renders in `sources/official/paper/renders/180dpi/` were inspected. Ambiguous letters were re-inspected in enlarged crops. Extracted text without font information was used only for navigation and was never treated as font evidence.

No prose, mathematical relation, sign, constant, hypothesis, marker, equation number, or page order was intentionally changed. No build, cumulative PDF regeneration, publication file, shared script, or illustration file was touched by this audit.

## MuPDF evidence and font identification

MuPDF structured text was regenerated page-bounded with:

```text
mutool draw -q -F stext.json -o official-pp121-166.stext.json navier-stokes.pdf 121-166
```

The resulting evidence file is `tmp/notation_font_audit_pp121_166/official-pp121-166.stext.json`, 3,937,050 bytes, SHA-256 `922f81070508a0c27557db106e60d4f7f2de60ed9ba0b13372f3cdf0bd735804`. Page resources and raw content streams were then read with `mutool show ... pages/<page>/Resources/Font` and `mutool show ... pages/<page>/Contents`. The relevant embedded resources are:

| PDF resource | Object | Embedded face | Audit meaning |
|---|---:|---|---|
| `/F133` | 3818 | `URWPalladioL-Roma` | ordinary upright roman |
| `/F169` | 3820 | `URWPalladioL-Ital` | ordinary italic |
| `/F180` | 3823 | `CMSY10` | calligraphic capitals in the audited contexts |
| `/F504` | 3832 | `EUFM10` | Fraktur/blackletter |
| `/F510` | 3833 | `CMSS10` | sans-serif named amplitude/normalization |
| `/F99` | 3829 | `rsfs10` | RSFS script, distinct from `/F180` |

`CMSY10` also carries nonalphabetic mathematical symbols, so a font-name match alone was not enough: the letter, its coordinates, the visible render, and its formula context were checked together. Conversely, the RSFS `A,B` on page 161 were not collapsed into the calligraphic family merely because text extraction without font information reports the same ASCII letters.

For routing, the existing pre-audit 166-page reconstruction PDF (SHA-256 `7645ecd59a3d6614695391bbd89e9ff587a9963af0c29a19a969ff10bff29253`) was also extracted page-bounded. Its 46-page structured-text file is `tmp/notation_font_audit_pp121_166/reconstruction-pp121-166.stext.json`, 3,739,690 bytes, SHA-256 `bd7182f69bac2af4bba7c258017fb428aa0e1f32861e8fd34b67679c84f5350e`. Coordinate-aligned comparison against the official spans isolated 60 calligraphic-to-italic glyph losses, 51 sans-to-italic losses, 32 Fraktur-to-italic losses, and nine RSFS-script-to-calligraphic losses. The roman-to-italic losses localized to the named suffixes and page-156 asymptotic subscript reported below; no italic-to-roman loss survived inspection. This old reconstruction rendering was a diagnostic only: it predates the corrections, and no post-audit build is claimed here.

Representative raw-stream switches make the distinctions explicit: page 145 selects `/F510` for the named amplitude `C` and `/F504` for coefficient weights `a`; page 161 selects `/F99` for `A,B` in (C.11)--(C.13) and `/F180` for the operator `D`. Structured spans retain page-local coordinates; examples include page 122 `/F180` `T` at y=494 and 507, page 145 `/F504` `a` at y=296 and 304, page 145 `/F510` `C` at y=143, page 161 `/F99` `A,B` at y=356--504, and page 164 `/F133` `v` at y=696.

## Confirmed actionable mismatches and corrections

Line numbers below refer to the post-audit fragments. Every line listed contains at least one corrected glyph occurrence; where a line repeats the symbol, every occurrence on that line was checked.

### Pages 121--144

| Official page(s) | Reconstruction line evidence | Official PDF evidence | Confirmed source-faithful form |
|---|---|---|---|
| 122 | `pp121-126.tex:166-167` | Four `T` glyphs are `/F180` (`CMSY10`) at y=494 and 507. | `\mathcal T` for the linear operator and commutator. |
| 124--125 | `pp121-126.tex:360,368,424,426` | Six `K` glyphs are `/F180` at page-124 y=518,562 and page-125 y=344,358. | `\mathcal K`, including `\mathcal K_\nu`. |
| 127 | `pp127-132.tex:62,66,70,79-80,85,96,99` | Eight `Q` glyphs are `/F180` at y=516--677. | `\mathcal Q` for the bilinear map. |
| 129 | `pp127-132.tex:204` | The operator `D` is `/F180` at x=145,y=262. | `\mathcal D_X`. |
| 130--131 | `pp127-132.tex:289-290,418,435` | Each suffix `p` in the named radius is `/F133`; page-130 spans are at y=109,123 and page-131 spans at y=329,346,474,487. | `X_{\mathrm p}`. |
| 131 | `pp127-132.tex:407` | The normalization `C` is `/F510` at x=236,y=282. | `\mathsf C`. |
| 133 | `pp133-138.tex:2,7` | Both named-radius suffixes `p` are `/F133` at y=96,143. | `X_{\mathrm p}`. |
| 134 | `pp133-138.tex:150` | The class suffix `c` is `/F133` at x=169,y=577. | `P_{\mathrm c}`. |
| 136 | `pp133-138.tex:288` | The named amplitude `C` is `/F510` at x=271,y=300. | `\mathsf C`. |
| 137 | `pp133-138.tex:395` | The reserved-interval `I` is `/F180` at x=237,y=513. | `\mathcal I_2`. |
| 143 | `pp139-144.tex:368-369` | Both class suffixes `c` are `/F133` at x=91 and 214,y=293. | `P_{\mathrm c}`, `J_{\mathrm c}`. |

No new glyph-family mismatch was found on pages 121, 123, 126, 128, 132, 135, 138--142, or 144. Existing calligraphic/script forms on those pages were nevertheless included in the page-by-page reconciliation.

### Pages 145--150

| Official page(s) | Reconstruction line evidence | Official PDF evidence | Confirmed source-faithful form |
|---|---|---|---|
| 145--146 | `pp145-150.tex:28,34,101,108,123` | Coefficient-weight `a` glyphs select `/F504`; visible spans occur at page-145 y=296,304 and page-146 y=112--160,241. | `\mathfrak a_{\alpha\beta}` and its indexed variants. |
| 146--149 | `pp145-150.tex:181,187,195,210,212,229,234-236,250-251,256,302,305,307,309,372,439` | Correction-field `u` glyphs select `/F504`; the densest run is page 147 y=95--567. | `\mathfrak u` throughout the correction-field construction. |
| 145, 147, 149--150 | `pp145-150.tex:42,66,234,236-237,242,250-251,255,388,393,411,490,503,505` | Operator `D` glyphs select `/F180`, including page-145 x=436,y=362 and page-147 y=384--554. | `\mathcal D_X`; ordinary `D_\eta` is not changed. |
| 145--150 | `pp145-150.tex:12,175-176,183,200,222,268,313,330,346,374,468,471-472,514,526,528` | Named `C` glyphs select `/F510`: page-145 y=143; page-146 y=642,674; page-147 y=173,294,650; page-148 y=364,495,625; page-149 y=157; page-150 y=158,195,486,550,563. | `\mathsf C` and `\mathsf C_0`; generic bound constants remain italic. |
| 150 | `pp145-150.tex:481` | Stress `T` selects `/F180` at x=291,y=255. | `\mathcal T_0`. |
| 150 | `pp145-150.tex:483,494,502,504,519-521,524-527,535,540-541,544` | Reference suffix `r` and the named boundary suffix `b` select `/F133`; representative spans occur at y=282--694. | `\mathrm r` on reference quantities and `X_{\mathrm b}` in this boundary-label context. |

### Pages 151--156

| Official page(s) | Reconstruction line evidence | Official PDF evidence | Confirmed source-faithful form |
|---|---|---|---|
| 151--153,155 | `pp151-156.tex:30,35,37,77,99,209,214,224,354` | Each logarithmic-radial operator `D` selects `/F180`; representative spans are page-151 y=264,314,636, page-152 y=170, and page-153 y=280--372. | `\mathcal D_X`. |
| 151--153 | `pp151-156.tex:66,73,173,189,191` | Stress `T` selects `/F180` on pages 151--153. | `\mathcal T_0`. |
| 154 | `pp151-156.tex:279,287,316` | Bound-family `B` selects `/F180` at y=279,340,555. | `\mathcal B_k`, `\mathcal B_0`. |
| 151--156 | `pp151-156.tex:2-3,7,9,19,29,57,86,91,114,200,251,263,271,286,288,322,370,378,458,462,464-465,473,475,482,486` | Named amplitude/normalization `C` selects `/F510`; all per-page `/F510` capital counts agree with these commands. | `\mathsf C` in named-amplitude contexts. |
| 151 | `pp151-156.tex:3,7,9,17,26,29,32,35,37,43,49-50,56-59` | Reference suffix `r` selects `/F133` in the corresponding spans. | `\mathrm r`. |
| 152 | `pp151-156.tex:89-90,98-100,107,109,120,122,128,130,133-136,141,144,147,150-151` | Reference suffix `r` and class suffix `c` select `/F133`. | `\mathrm r`, `\mathrm c`. |
| 153 | `pp151-156.tex:175,181,200,206-207,209,211,213,215-217` | Reference `r`, class `c`, and named-boundary `b` select `/F133`. | `\mathrm r`, `\mathrm c`, `\mathrm b`. |
| 154,156 | `pp151-156.tex:293,295,448,451` | Reference suffixes on page 154 and class suffixes on page 156 select `/F133`. | `\mathrm r`, `\mathrm c`. |
| 156 | `pp151-156.tex:494` | In `o_C(1)`, `C` selects the upright math-roman font (`CMR10`), not `/F510` and not the italic face; the structured span is x=477,y=617. | `o_{\mathrm C}(1)`. |

The page-156 `o_{\mathrm C}(1)` occurrence is intentionally distinguished from the nearby named amplitude `\mathsf C`. This is a direct content-stream distinction, not a semantic normalization.

### Pages 157--166

| Official page(s) | Reconstruction line evidence | Official PDF evidence | Confirmed source-faithful form |
|---|---|---|---|
| 157 | `pp157-162.tex:17,31-32,45` | `/F510` supplies the two amplitude `C` glyphs, `/F180` the bound `B`, and `/F133` the three reference suffixes. | `\mathsf C`, `\mathcal B_k`, `\mathrm r`. |
| 158 | `pp157-162.tex:94` | Stress `T` selects `/F180` at x=278,y=289. | `\mathcal T_0`. |
| 159--160 | `pp157-162.tex:168-170,192,230,233,237,297` | All ten page-159 and two page-160 class suffixes `c` select `/F133`. | `P_{\mathrm c}`, `J_{\mathrm c}` and their arguments. |
| 161 | `pp157-162.tex:357,361,363,371,373,382,384` | Nine `A,B` glyphs select `/F99` (`rsfs10`) at y=356--504. | `\mathscr A`, `\mathscr B`, not `\mathcal A`, `\mathcal B`. |
| 161 | `pp157-162.tex:377,382,384,388` | Four operator `D` glyphs select `/F180` at y=458--532. | `\mathcal D_X`. |
| 163--164 | `pp163-164.tex:79,90,101,126,129,199` | Class/reference suffixes `c,r` and named-radius suffix `v` select `/F133`; the page-164 `v` span is x=428,y=696. | `\mathrm c`, `\mathrm r`, `\mathrm v`. |
| 165 | `pp165-166.tex:11` | Named-radius suffix `v` selects `/F133` at x=231,y=148. | `X_{\mathrm v}`. |

No new glyph-family mismatch was found on pages 162 or 166.

## Context-sensitive distinctions retained

- `\mathsf C` is used only where the PDF selects the sans-serif named amplitude/normalization. Generic estimate constants `C`, `C_k`, `C_I`, `C_{r,s}`, and similar occurrences remain ordinary italic.
- The page-156 asymptotic subscript is upright roman `o_{\mathrm C}(1)`, not sans serif and not italic.
- `\mathcal D_X` is the named logarithmic-radial operator. Ordinary symbols such as `D_\eta` remain ordinary italic where the PDF uses the italic face.
- `\mathscr A,\mathscr B` on page 161 use RSFS script. Calligraphic `\mathcal A_X`, `\mathcal B_\rho`, and `\mathcal B_k` remain calligraphic.
- `\mathfrak a` is the coefficient-weight family and `\mathfrak u` the correction field. Ordinary italic `a` and `u` elsewhere remain ordinary italic.
- Existing blackletter `\mathfrak p`, `\mathfrak s`, and `\mathfrak m`, and existing RSFS `\mathscr R`, were checked against their embedded fonts and required no correction.
- Upright suffixes `\mathrm p`, `\mathrm r`, `\mathrm c`, `\mathrm b`, and `\mathrm v` were applied only to the named radius/reference/class/boundary roles confirmed by `/F133`. The visually similar endpoint variable `X_b` in later Appendix C contexts remains italic where the official PDF uses the italic face.
- No mathematical bold font is embedded in pages 121--166. The bold face present in the PDF is used for prose headings and bibliography volume numbers, not bold mathematical variables. A source scan finds no `\mathbf`, `\boldsymbol`, or `\bm` in the nine fragments; therefore no boldsymbol correction was warranted.

## Validation and residual scans

After the corrections, an automated page-by-page comparison counted alphabetic glyphs in the official MuPDF font spans against the corresponding source commands for all 46 pages. It compared `/F180` uppercase letters with `\mathcal`, `/F510` uppercase letters with `\mathsf`, `/F504` letters with `\mathfrak`, and `/F99` uppercase letters with `\mathscr`. Result: `nonzero_delta_pages 0`.

The page markers and formula-occurrence markers are unchanged:

| Fragment | Formula markers |
|---|---:|
| `pp121-126.tex` | 217 |
| `pp127-132.tex` | 315 |
| `pp133-138.tex` | 288 |
| `pp139-144.tex` | 247 |
| `pp145-150.tex` | 276 |
| `pp151-156.tex` | 295 |
| `pp157-162.tex` | 245 |
| `pp163-164.tex` | 66 |
| `pp165-166.tex` | 16 |

A residual scan for unescaped raw spacing words `qquad`, `quad`, `enspace`, `thinspace`, `hspace`, and `vspace` returned no hits. The independent root repairs remain present as control sequences in Equation (A.26), `pp133-138.tex:177`, and Equation (A.32), `pp133-138.tex:427`; neither was overwritten. A residual scan also found no ordinary italic `D_X` or `T_0` in the audited fragments and no `\mathcal A`/`\mathcal B` substitution for the page-161 RSFS pair.

## Post-audit fragment identities

| Fragment | Bytes | SHA-256 |
|---|---:|---|
| `pp121-126.tex` | 25,232 | `243fc34f2eb91236228fe2afa1f6d12b4562bdab426c0a2b77ebbdb1bb3cf833` |
| `pp127-132.tex` | 29,840 | `a3549d2b3d57019253e46ab04e94441e4d70b64abd497d73f7fa0199d9f2a6c8` |
| `pp133-138.tex` | 28,443 | `fb6f194afd8606aa273941827ab8065d80cdc4c9c04c23e51cd22c5bad05ca99` |
| `pp139-144.tex` | 27,314 | `1850511f0e279a13fcaf57fa9c66975b5b495909da200e366ba9e2a143cbe137` |
| `pp145-150.tex` | 29,295 | `431e84a9dc82d0a6495936a28ea286a7f387d2149c17b712ee001901a4f2377e` |
| `pp151-156.tex` | 30,469 | `f75c526fb744ca4f6d0cad4f3ffea21d9cb0b06fc9f223280753c04c8bf567d2` |
| `pp157-162.tex` | 28,962 | `147f8815f76008cc51baed23d67a6dc4e63a531cfd03a05e0e7d5198ee45017d` |
| `pp163-164.tex` | 9,902 | `02cb72a22db9c3f3c6b6d85b6181142493550aaeb2a2475b14130b8090114ed5` |
| `pp165-166.tex` | 7,252 | `fbd28d417d02a63eeae499b4abaf7bf142217d00a3925c74a1a4d259d68819bd` |

Each affected range-level `REPORT.md` records its post-audit byte count and fragment hash and carries an explicit notation-font audit note. Compilation and cumulative rendered-PDF comparison remain separate integration stages; this audit did not invoke them.
