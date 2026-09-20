# Static manuscript-to-Lean map

Record: `NS-MANUSCRIPT-LEAN-MAP-20260920-001`  
Audit date: 2026-09-20  
Machine-readable companion: [`MANUSCRIPT_LEAN_MAP.json`](MANUSCRIPT_LEAN_MAP.json)

## Status and scope

This is a **static source concordance**, not a Lean build certificate. No Lean, Lake, or Elan process was started for this audit. In particular, this work did not elaborate or typecheck the source, reproduce `#print axioms`, inspect a compiled artifact, or observe a successful build. The `sorry_count`, `status: proved`, and axiom lists in `formalization.yaml` are repository metadata, not results independently reproduced here.

The concordance covers all 80 numbered theorem, proposition, lemma, corollary, definition, and remark environments in the complete reconstruction (`reconstruction/main.tex`, Sections 1-10 and Appendices A-C). Manuscript locators are one-based lines at which environments begin. The sole split-label case is Lemma 5.1: its environment begins at `pp043-048.tex:457`, and `\label{lem:5.1}` is on line 458.

The frozen repository says its scope is “Full formalization of main results” at `formalization.yaml:48` and labels review status “self-assessed” at line 104. Its `alignment` section explicitly pairs manuscript Theorem 1.1 with `NavierStokes.Comparator.navier_stokes_breakdown_R3` at lines 111-112 and Corollary 10.6 with `NavierStokes.Comparator.navier_stokes_breakdown_periodic` at lines 115-116. The remaining correspondences below are conservative static source-reading judgments; none is promoted to an official alignment.

## Frozen identity

| Item | Exact value |
|---|---|
| Repository | `https://github.com/openai/NavierStokesAndEuler.git` |
| Checkout | `sources/official/lean/NavierStokesAndEuler` (detached and clean when inspected) |
| Commit | `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` |
| Tree | `a503f07635f200c0f2f9c5361df1fa07f95c4741` |
| Frozen archive | `sources/official/lean/NavierStokesAndEuler-f9e8bc5b38b6e212696e8a30e3e91517af887bbd.tar` |
| Archive SHA-256 | `a9322b2112ef89c9a0cbb5029578cd672a757fe715a565d55f032e0b443cb7a7` |
| Archive size | 36,454,400 bytes |
| Freeze receipt | `evidence/source_freeze/SOURCE_FREEZE.json`, record `NS-SOURCE-FREEZE-20260919-001` |
| Reconstruction entrypoint SHA-256 at audit | `e3bd305f4228f1c814a593a8070741903ed9c18543cc39ab66b0e54d5140feaa` |

The receipt describes the Lean repository as a “complementary formal main-result authority; not transcription authority.” That limitation governs this map.

## Coverage categories

| Code | Category | Meaning | Count |
|---|---|---|---:|
| OA | `official_alignment` | `formalization.yaml` explicitly aligns the manuscript statement with the public declaration. Static inspection confirms that the named declaration and adapter chain exist. | 2 |
| SS | `strong_static_correspondence` | A declaration, or a small explicit package, substantially mirrors the manuscript result. This is not an official alignment and is not a build claim. | 38 |
| PS | `partial_static_correspondence` | Exact declarations cover identifiable formulas, clauses, or construction components, but not the whole numbered result as one theorem. | 24 |
| IP | `indirect_pipeline_only` | Relevant modules or downstream packages consume the subject, but no declaration-level match for the complete numbered result was identified. | 14 |
| NI | `not_identified` | No defensible declaration-level or pipeline correspondence was identified in this bounded audit. | 2 |

The IDs in the statement matrix resolve to exact names, source files, one-based declaration-header lines, and dependency roles in the declaration catalog below and in the JSON companion.

## Import and dependency spine

- `NavierStokes.lean` imports `NavierStokes.ComparatorSolution` and `NavierStokes.PaperResults`.
- `NavierStokes/ComparatorSolution.lean` imports the whole-space and periodic comparator adapters.
- `NavierStokes/ComparatorR3Theorem.lean` imports the whole-space theorem/candidate/comparison bridge; `NavierStokes/ComparatorTheorem.lean` imports the periodic candidate and comparator bridge.
- `NavierStokes/PaperResults.lean` imports the periodic theorem, local angular/heat results, and `PaperAdditionalResults`.
- `NavierStokes/PaperAdditionalResults.lean` is a broad import-only aggregator. A module appearing there is **not**, by itself, evidence that any manuscript statement is formalized.

## Statement concordance

### Sections 1 and 3

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Theorem 1.1 (`thm:1.1`) | `reconstruction/sections/pp001-006.tex:42` | OA | D001, D003, D005-D007 | Explicitly aligned to D001; the other entries are the inspected bridge and whole-space theorem packages. |
| Theorem 3.1 (`thm:3.1`) | `reconstruction/sections/pp013-018.tex:124` | SS | D009-D015 | The property record mirrors the principal local-theorem clauses, and D010 closes the existential package. |
| Definition 3.2 (`def:3.2`) | `reconstruction/sections/pp013-018.tex:409` | PS | D115-D117 | Smoothness and axis jets are proved for the actual slow-axis profiles; no verbatim definition of “regular at the axis” was identified. |
| Definition 3.3 (`def:3.3`) | `reconstruction/sections/pp013-018.tex:417` | NI | — | Prose convention for order of choices and uniform smallness; no single Lean definition was identified. |

### Section 4

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Lemma 4.1 | `reconstruction/sections/pp025-030.tex:15` | PS | D033-D034 | Time- and axial-chain coefficients are exact components, not the whole displayed chain-rule suite. |
| Proposition 4.2 | `reconstruction/sections/pp025-030.tex:257` | PS | D035-D036 | The two leading-stress divergence components are explicit; the full physical-residual package is broader. |
| Lemma 4.3 | `reconstruction/sections/pp025-030.tex:338` | SS | D037-D038 | The angular and axial integrated stress identities cover the two principal formulas. |
| Lemma 4.4 | `reconstruction/sections/pp025-030.tex:382` | PS | D039-D040 | Exact moment propagation and a comparison norm are present; not every hypothesis/conclusion is one declaration. |
| Lemma 4.5 | `reconstruction/sections/pp031-036.tex:11` | SS | D041-D042 | Algebraic and paper-facing admissible-cone equivalences match the criterion. |
| Theorem 4.6 | `reconstruction/sections/pp031-036.tex:111` | SS | D028-D032 | Distributed over the final profile record, base existence, weighted cone bounds, and nominal-cone certificate; not officially number-aligned. |
| Lemma 4.7 | `reconstruction/sections/pp031-036.tex:180` | SS | D043-D046 | Determinant, smooth inverse, and compact-family inverse-jet bounds cover the moment-matrix result. |
| Lemma 4.8 | `reconstruction/sections/pp031-036.tex:219` | IP | D121 | A prepared outgoing profile exists downstream, but the full ordered choices, exterior formulae, moments, and heat behavior were not isolated. |
| Lemma 4.9 | `reconstruction/sections/pp031-036.tex:287` | IP | D101-D102 | Right-edge stress vanishing is proved; the displayed tail integrals and limiting direction were not matched as one theorem. |
| Proposition 4.10 | `reconstruction/sections/pp031-036.tex:318` | IP | D112-D114, D122-D123 | Entrance, exit, continuation, and matching packages collectively support the construction, without a one-declaration match. |
| Lemma 4.11 | `reconstruction/sections/pp037-042.tex:194` | SS | D047-D048 | Periodic cone family, positive margin, boundary matching, and uniform collar are explicit. |

### Section 5

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Lemma 5.1 | `reconstruction/sections/pp043-048.tex:457` | PS | D049 | An all-order local slow hierarchy is constructed; the uniqueness and every displayed profile equation are not one theorem. |
| Lemma 5.2 | `reconstruction/sections/pp049-054.tex:96` | SS | D050 | The source comment identifies the actual reference-path extension and its uniform bounds with Lemma 5.2. |
| Proposition 5.3 | `reconstruction/sections/pp055-060.tex:31` | IP | D049-D050 | The hierarchy and bounds feed finite sums, but the exact divergence/residual estimate package was not isolated. |
| Lemma 5.4 | `reconstruction/sections/pp055-060.tex:267` | SS | D051 | The Borel-type summation is packaged as existence of smooth base fields. |
| Proposition 5.5 | `reconstruction/sections/pp055-060.tex:474` | SS | D028-D029, D052 | Constructed/final base packages collect divergence, residual-stress, support, and profile conclusions. |

### Section 6

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Lemma 6.1 | `reconstruction/sections/pp061-066.tex:229` | PS | D053-D054 | Oriented slots and proper coloring formalize the separation mechanism, not every rectangle/support clause. |
| Lemma 6.2 | `reconstruction/sections/pp067-072.tex:41` | PS | D055 | Exact lifted-rectangle cardinality is present; the other analytic/averaging clauses are distributed. |
| Lemma 6.3 | `reconstruction/sections/pp067-072.tex:123` | SS | D056 | Uniform relevant-label count is stated directly. |
| Definition 6.4 | `reconstruction/sections/pp067-072.tex:290` | PS | D057 | `MeanClass` is the Lean carrier, not a verbatim prose transcription. |
| Definition 6.5 | `reconstruction/sections/pp067-072.tex:382` | PS | D058 | `WaveClass` is the Lean carrier, not a verbatim transcription of every chart/support clause. |
| Proposition 6.6 | `reconstruction/sections/pp067-072.tex:454` | PS | D059-D062 | Representative addition, differentiation, bilinear, and graph-iterate rules are exact; the selection is not an exhaustive clause list. |

### Section 7

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Lemma 7.1 | `reconstruction/sections/pp073-078.tex:180` | PS | D063 | Actual phase geometry supplies the nondegeneracy component, not every displayed bound. |
| Proposition 7.2 | `reconstruction/sections/pp073-078.tex:349` | IP | — | Projected amplitude inversion is spread across `TangentODE`, `ParticularWaveAssembly`, and `ParticularWaveBounds`; no exact package was isolated. |
| Corollary 7.3 | `reconstruction/sections/pp079-084.tex:139` | IP | — | Finite-stage solution operators are used by the particular-wave pipeline, but no exact corollary declaration was identified. |
| Lemma 7.4 | `reconstruction/sections/pp079-084.tex:163` | IP | — | Homogeneous pulse amplitude, growth, and covariance are split across pulse modules. |
| Proposition 7.5 | `reconstruction/sections/pp079-084.tex:329` | PS | D065-D066 | Covariance identities are exact; invertibility, amplitude choice, and supports form a larger package. |
| Proposition 7.6 | `reconstruction/sections/pp079-084.tex:542` | IP | — | Signed covariance realization is present in the pipeline, but the linear operation with all weighted bounds was not isolated. |
| Lemma 7.7 | `reconstruction/sections/pp085-090.tex:107` | SS | D067-D068 | Divergence-free curl realization and stripped formula match the central claim. |
| Corollary 7.8 | `reconstruction/sections/pp085-090.tex:226` | IP | D067-D068 | Curl realization is exact, but the complete residual/class estimate was not matched to one declaration. |

### Section 8

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Proposition 8.1 | `reconstruction/sections/pp085-090.tex:364` | SS | D070 | Exact Cartesian mean-balance identities are packaged together. |
| Lemma 8.2 | `reconstruction/sections/pp085-090.tex:488` | PS | D069 | Smooth compact radial primitive is exact; the manuscript bundles additional operator and weighted estimates. |
| Proposition 8.3 | `reconstruction/sections/pp091-096.tex:161` | IP | D069 | Radial-primitive and mean-residual infrastructure support it, but the full pressure/temporal correction theorem was not isolated. |
| Proposition 8.4 | `reconstruction/sections/pp091-096.tex:275` | IP | D070 | Mean balances are exact; the full residual decomposition and moment hypotheses remain distributed. |
| Corollary 8.5 | `reconstruction/sections/pp091-096.tex:363` | PS | D065-D066 | Covariance realization is explicit; the full dependency on Proposition 8.4 remains distributed. |
| Lemma 8.6 | `reconstruction/sections/pp091-096.tex:429` | SS | D064 | Smooth zero-mean Fourier inverse and its estimates match the central assertion. |
| Lemma 8.7 | `reconstruction/sections/pp097-102.tex:22` | SS | D071-D073 | Five-row system, repair existence, and finite-jet bounds supply the correction. |
| Lemma 8.8 | `reconstruction/sections/pp097-102.tex:139` | IP | — | Curl geometry, mean residual, and rank repair are separate; no exact full mean-correction theorem was identified. |

### Section 9

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Proposition 9.1 | `reconstruction/sections/pp097-102.tex:378` | IP | — | Coefficient-level linear-wave bounds exist, but no exact full proposition declaration was isolated. |
| Lemma 9.2 | `reconstruction/sections/pp097-102.tex:471` | PS | D061-D062 | Bilinear class and graph-derivative bounds capture the product mechanism, not every cylindrical shift. |
| Proposition 9.3 | `reconstruction/sections/pp103-108.tex:45` | PS | D075 | The state residual decomposition is exact; finite construction/support/class conclusions remain distributed. |
| Definition 9.4 | `reconstruction/sections/pp103-108.tex:269` | SS | D074 | Dedicated finite correction-state structure serves the same role. |
| Proposition 9.5 | `reconstruction/sections/pp103-108.tex:318` | SS | D076 | The actual initialization theorem establishes the initial invariant. |
| Proposition 9.6 | `reconstruction/sections/pp103-108.tex:405` | SS | D077-D080 | Cycle preservation, next-state result, and rate ledger formalize the induction step and improving rates. |
| Lemma 9.7 | `reconstruction/sections/pp109-114.tex:237` | PS | D086 | A positive common `qbig` is proved; stage/derivative finiteness is distributed. |
| Lemma 9.8 | `reconstruction/sections/pp109-114.tex:331` | SS | D080-D083 | Residual-rate growth, jet identities, tail bounds, and an all-rate schedule mirror summability/flatness. |
| Proposition 9.9 | `reconstruction/sections/pp109-114.tex:452` | SS | D009-D010, D083-D084 | The selected schedule feeds the unconditional local theorem with all recorded properties. |

### Section 10

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Proposition 10.1 | `reconstruction/sections/pp115-120.tex:214` | SS | D016-D017, D021-D022 | Localization and pressure agreement tie the local fields to the compact whole-space candidate. |
| Lemma 10.2 | `reconstruction/sections/pp115-120.tex:309` | PS | D018-D019, D085 | Candidate witness records smooth forcing and all endpoint derivative values, not the lemma's uniform convergence formulation verbatim. |
| Lemma 10.3 | `reconstruction/sections/pp115-120.tex:435` | SS | D022-D024 | Selected candidate has initial rest; force is smooth and compactly supported in positive time. |
| Lemma 10.4 | `reconstruction/sections/pp121-126.tex:13` | SS | D025, D007 | Force/dissipation integrability and sharp finite/total energy inequalities are explicitly packaged. |
| Lemma 10.5 | `reconstruction/sections/pp121-126.tex:61` | SS | D026-D027 | Presingular finite-energy uniqueness and global-before-one agreement are explicit. |
| Corollary 10.6 | `reconstruction/sections/pp121-126.tex:406` | OA | D002, D004, D008 | Explicitly aligned to D002; D004 and D008 are the periodic adapter and paper-corollary layers. |

### Appendix A

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Lemma A.1 | `reconstruction/sections/pp121-126.tex:532` | SS | D043-D046 | Ordered moment determinant and smooth compact-family inverse bounds match the result. |
| Lemma A.2 | `reconstruction/sections/pp127-132.tex:55` | SS | D087-D088 | Closed-interval smooth same-branch repair and linear solution represent the finite moment correction. |
| Corollary A.3 | `reconstruction/sections/pp127-132.tex:127` | SS | D089-D090 | Five-profile determinant and compact-parameter repair represent the five-moment specialization. |
| Proposition A.4 | `reconstruction/sections/pp127-132.tex:374` | IP | D121, D123 | Outer profile is consumed downstream; no single declaration matches every staged formula and choice order. |
| Lemma A.5 | `reconstruction/sections/pp133-138.tex:56` | PS | D091-D094 | Smoothness, derivative sign, prefix bound, and pressure sign are exact components. |
| Lemma A.6 | `reconstruction/sections/pp133-138.tex:435` | SS | D095-D099 | Smoothness, derivative bounds, heat equation, monotonicity, and endpoint derivatives cover the analytic core. |
| Proposition A.7 | `reconstruction/sections/pp139-144.tex:8` | PS | D100 | Terminal heat compensation is constructed; the full replacement formula and retained properties are broader. |
| Lemma A.8 | `reconstruction/sections/pp139-144.tex:132` | SS | D101-D102 | Coefficient and physical stress are proved zero to the right. |
| Lemma A.9 | `reconstruction/sections/pp139-144.tex:238` | SS | D103 | Flat factorization includes the rectangle and mixed-jet bounds. |
| Proposition A.10 | `reconstruction/sections/pp139-144.tex:275` | PS | D104, D030 | Terminal lower bound and final edge collar are formalized; full cone statement is composite. |

### Appendix B

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Lemma B.1 | `reconstruction/sections/pp145-150.tex:47` | PS | D105-D111 | Banach carriers, completeness, product, regular inverse, and primitive are exact components. |
| Proposition B.2 | `reconstruction/sections/pp145-150.tex:172` | SS | D112, D124-D125 | Jointly analytic natural-axis profiles and initial margin/source identities represent the axis construction. |
| Proposition B.3 | `reconstruction/sections/pp145-150.tex:345` | PS | D113-D114, D126 | Exit bounds, ideal prefix, and reference lower bound cover key clauses. |
| Lemma B.4 | `reconstruction/sections/pp145-150.tex:512` | SS | D050 | The actual reference path and literal histories are packaged in the reference-bounds theorem. |
| Proposition B.5 | `reconstruction/sections/pp151-156.tex:70` | PS | D120, D123 | Ordered outgoing cone and entrance envelope are exact components; continuation/factorization remains distributed. |
| Corollary B.6 | `reconstruction/sections/pp151-156.tex:230` | SS | D115-D117 | Smooth actual slow-axis profiles, zero-axis values, and exact axis jets give the regularity conclusion. |
| Lemma B.7 | `reconstruction/sections/pp151-156.tex:269` | SS | D118-D120 | Finite-order constants, endpoint log bounds, and entrance envelope correspond to the endpoint-rate result. |
| Proposition B.8 | `reconstruction/sections/pp151-156.tex:377` | SS | D121-D122 | Prepared outgoing profile and exact nominal matching capture the continuation and field/pressure/moment match. |
| Remark B.9 | `reconstruction/sections/pp157-162.tex:21` | NI | — | Global order of parameter choices; no proposition encoding the prose ordering was identified. |
| Corollary B.10 | `reconstruction/sections/pp157-162.tex:55` | SS | D121-D122, D031-D032 | Prepared/matched outgoing existence and nominal cone certificates represent the completed join. |

### Appendix C

| Statement | Manuscript locator | Coverage | Declaration IDs | Static assessment |
|---|---|---|---|---|
| Lemma C.1 | `reconstruction/sections/pp157-162.tex:118` | SS | D047-D048 | Periodic loop, prescribed averages, true-cone margin, boundary matching, and collar are explicit. |
| Proposition C.2 | `reconstruction/sections/pp157-162.tex:337` | SS | D127-D132 | Exact shears, uniform jets, all-jet moment repair, and restored cone form an explicit composite match. |
| Proposition C.3 | `reconstruction/sections/pp163-164.tex:54` | SS | D028-D030 | Final weighted profile and final-base package collect the restored conclusions; not officially number-aligned. |

## Explicit gaps and limits

The two numbered manuscript items for which no static correspondence was identified are Definition 3.3 and Remark B.9.

The following 14 items are represented only through a broader dependency pipeline, not by an identified declaration-level match for the complete statement: Lemmas 4.8 and 4.9; Propositions 4.10 and 5.3; Proposition 7.2, Corollary 7.3, Lemma 7.4, Proposition 7.6, and Corollary 7.8; Propositions 8.3 and 8.4 and Lemma 8.8; Proposition 9.1; and Proposition A.4.

The 24 `PS` items have exact component declarations but remain incomplete at the numbered-statement level. They must not be described as full formalizations on the strength of this map. Conversely, a negative finding here means only that this bounded static audit did not identify the declaration; it is not proof that no relevant declaration exists among the 2,659 `.lean` files in the frozen tree.

## Declaration locator catalog

Every locator below is relative to the frozen repository checkout. The line is the one-based declaration header. “Role” describes how the declaration participates in this concordance; it is not a claim about successful compilation.

| ID | Exact declaration | Source locator | Dependency role |
|---|---|---|---|
| D001 | `NavierStokes.Comparator.navier_stokes_breakdown_R3` | `NavierStokes/ComparatorSolution.lean:16` | Public comparator-facing option (C) wrapper; explicitly aligned to Theorem 1.1. |
| D002 | `NavierStokes.Comparator.navier_stokes_breakdown_periodic` | `NavierStokes/ComparatorSolution.lean:23` | Public comparator-facing option (D) wrapper; explicitly aligned to Corollary 10.6. |
| D003 | `NavierStokes.ComparatorBridge.navier_stokes_breakdown_R3` | `NavierStokes/ComparatorR3Theorem.lean:38` | Adapter from the whole-space paper theorem to option (C). |
| D004 | `NavierStokes.ComparatorBridge.navier_stokes_breakdown_periodic` | `NavierStokes/ComparatorTheorem.lean:47` | Adapter from the periodic paper theorem to option (D). |
| D005 | `NavierStokesR3.theorem_1_1_with_initial_rest` | `NavierStokes/R3/Theorem.lean:26` | Whole-space theorem package with zero initial interval. |
| D006 | `NavierStokesR3.theorem_1_1` | `NavierStokes/R3/Theorem.lean:46` | Whole-space Theorem 1.1 package. |
| D007 | `NavierStokesR3.theorem_1_1_with_dissipation` | `NavierStokes/R3/Theorem.lean:66` | Whole-space theorem plus energy/dissipation conclusions. |
| D008 | `NavierStokes.PeriodicPaper.periodic_corollary` | `NavierStokes/PeriodicPaperTheorem.lean:155` | Periodic paper corollary before comparator adaptation. |
| D009 | `NavierStokes.LocalPaper.Properties` | `NavierStokes/LocalPaperTheorem.lean:53` | Bundles local smoothness, decomposition, divergence, residual flatness, heat exterior, and angular growth. |
| D010 | `NavierStokes.LocalPaper.local_theorem` | `NavierStokes/LocalPaperTheorem.lean:179` | Unconditional existential local-theorem package. |
| D011 | `NavierStokes.LocalPaper.Properties.exterior_profile_smooth` | `NavierStokes/LocalPaperHeat.lean:22` | Heat-exterior smoothness. |
| D012 | `NavierStokes.LocalPaper.Properties.exterior_profile_derivatives_bounded` | `NavierStokes/LocalPaperHeat.lean:27` | Heat-exterior derivative bounds. |
| D013 | `NavierStokes.LocalPaper.Properties.exterior_amplitude_formula` | `NavierStokes/LocalPaperHeat.lean:34` | Literal exterior amplitude formula. |
| D014 | `NavierStokes.LocalPaper.Properties.exterior_heat_equation` | `NavierStokes/LocalPaperHeat.lean:40` | Exterior heat equation. |
| D015 | `NavierStokes.LocalPaper.Properties.exterior_radial_form` | `NavierStokes/LocalPaperHeat.lean:51` | Radial heat-profile representation. |
| D016 | `NavierStokes.PaperLocalization.local_theorem_with_compact_candidate` | `NavierStokes/PaperLocalization.lean:28` | Ties the local theorem to the compact whole-space candidate. |
| D017 | `NavierStokes.PaperLocalization.compact_pressure_eq_local` | `NavierStokes/PaperLocalization.lean:20` | Pressure agreement on the localization region. |
| D018 | `NavierStokes.ActualCandidateAssembly.Witness` | `NavierStokes/ActualCandidateAssembly.lean:1121` | Selected-schedule package with force smoothness, decay, and endpoint derivative data. |
| D019 | `NavierStokes.ActualCandidateAssembly.selected_witness` | `NavierStokes/ActualCandidateAssembly.lean:1177` | Closed choice of the candidate witness. |
| D020 | `NavierStokes.ActualCandidateAssembly.selected_candidate` | `NavierStokes/ActualCandidateAssembly.lean:1183` | Periodic candidate assembled from the witness. |
| D021 | `NavierStokesR3.ActualCandidate.of_localized_fields` | `NavierStokes/R3/ActualCandidate.lean:78` | Whole-space candidate from localized fields. |
| D022 | `NavierStokesR3.ActualCandidate.selected_candidate_one_with_initial_rest` | `NavierStokes/R3/ActualCandidate.lean:143` | Viscosity-one whole-space candidate with initial rest. |
| D023 | `NavierStokesR3.PositiveTimeForce.force_contDiff` | `NavierStokes/R3/PositiveTimeForce.lean:49` | Smooth positive-time force extension. |
| D024 | `NavierStokesR3.PositiveTimeForce.force_compactPositiveTimeSupport` | `NavierStokes/R3/PositiveTimeForce.lean:72` | Compact support strictly in positive time. |
| D025 | `NavierStokesR3.CompactEnergy.candidate_energy_estimates` | `NavierStokes/R3/IntegratedDissipation.lean:279` | Force/dissipation integrability and sharp energy inequalities. |
| D026 | `NavierStokesR3.WholeSpaceUniqueness.candidate_unique_on_Icc` | `NavierStokes/R3/WholeSpaceUniqueness.lean:72` | Finite-energy uniqueness on a compact presingular interval. |
| D027 | `NavierStokesR3.WholeSpaceUniqueness.candidate_global_agrees_before_one` | `NavierStokes/R3/WholeSpaceUniqueness.lean:104` | Global finite-energy solution agrees before time one. |
| D028 | `NavierStokes.FinalSlowBase.ProfileData` | `NavierStokes/FinalSlowBase.lean:619` | Record of final slow-profile conclusions. |
| D029 | `NavierStokes.FinalSlowBase.exists_final_base` | `NavierStokes/FinalSlowBase.lean:639` | Existence of the final slow base. |
| D030 | `NavierStokes.LeadingStressWeights.exists_weighted_profile` | `NavierStokes/LeadingStressWeights.lean:1154` | Final weighted true-cone profile with both edge collars. |
| D031 | `NavierStokes.NominalConeAssembly.Assembly.certificate` | `NavierStokes/NominalConeAssembly.lean:1458` | Certificate for the assembled nominal-cone profile. |
| D032 | `NavierStokes.NominalConeAssembly.exists_nominal_cone` | `NavierStokes/NominalConeAssembly.lean:1517` | Existence of the nominal-cone package. |
| D033 | `NavierStokes.CoordinateAlgebra.time_chain_coefficient` | `NavierStokes/CoordinateAlgebra.lean:190` | Time-chain coefficient in self-similar coordinates. |
| D034 | `NavierStokes.CoordinateAlgebra.axial_chain_coefficient` | `NavierStokes/CoordinateAlgebra.lean:200` | Axial-chain coefficient in self-similar coordinates. |
| D035 | `NavierStokes.LeadingStress.theta_divergence` | `NavierStokes/LeadingStress.lean:138` | Angular leading-stress divergence identity. |
| D036 | `NavierStokes.LeadingStress.axial_divergence` | `NavierStokes/LeadingStress.lean:167` | Axial leading-stress divergence identity. |
| D037 | `NavierStokes.StressAlgebra.angular_integrated_identity` | `NavierStokes/StressAlgebra.lean:155` | Angular integrated stress formula. |
| D038 | `NavierStokes.StressAlgebra.axial_integrated_identity` | `NavierStokes/StressAlgebra.lean:212` | Axial integrated stress formula including pressure. |
| D039 | `NavierStokes.NominalProfile.moments_propagate` | `NavierStokes/NominalProfile.lean:486` | Propagation of matching moment data. |
| D040 | `NavierStokes.SeedHandbackJets.profile_comparison_norm` | `NavierStokes/SeedHandbackJets.lean:354` | Quantitative profile comparison. |
| D041 | `NavierStokes.ConeAlgebra.true_cone_iff` | `NavierStokes/ConeAlgebra.lean:69` | Algebraic true/admissible-cone equivalence. |
| D042 | `NavierStokes.SeedConePaper.admissible_iff` | `NavierStokes/SeedConePaper.lean:37` | Paper-facing admissible-cone equivalence. |
| D043 | `NavierStokes.PowerMomentMatrix.bumpMomentMatrix_det_ne_zero` | `NavierStokes/PowerMomentMatrix.lean:261` | Nonzero determinant for ordered power moments. |
| D044 | `NavierStokes.SmoothExponentialMomentMatrix.Family.matrix_det_ne_zero` | `NavierStokes/SmoothExponentialMomentMatrix.lean:69` | Invertibility of a smooth exponential-moment family. |
| D045 | `NavierStokes.SmoothExponentialMomentMatrix.Family.matrix_inverse_contDiffOn` | `NavierStokes/SmoothExponentialMomentMatrix.lean:80` | Smooth parameter dependence of the inverse. |
| D046 | `NavierStokes.SmoothExponentialMomentMatrix.Family.compact_inverse_jets_bound` | `NavierStokes/SmoothExponentialMomentMatrix.lean:98` | Compact-family inverse-jet bounds. |
| D047 | `NavierStokes.TrueConeLoopPaper.exists_local_family_with_margin` | `NavierStokes/TrueConeLoopPaper.lean:21` | Periodic true-cone loop with margin and boundary matching. |
| D048 | `NavierStokes.TrueConeLoopPaper.uniform_boundary_collar` | `NavierStokes/TrueConeLoopPaper.lean:60` | One positive uniform boundary-collar width. |
| D049 | `NavierStokes.SlowRecursion.exists_local_slow_hierarchy` | `NavierStokes/SlowRecursion.lean:1283` | All-order local slow-profile hierarchy. |
| D050 | `NavierStokes.ReferenceBounds.exists_reference_bounds` | `NavierStokes/ReferenceBounds.lean:1180` | Actual reference-path extension and uniform bounds. |
| D051 | `NavierStokes.SlowBorelBase.exists_base_fields` | `NavierStokes/SlowBorelBase.lean:1215` | Borel-type summation into smooth base fields. |
| D052 | `NavierStokes.ConstructedSlowBase.Modulated.exists_actual_base` | `NavierStokes/ConstructedSlowBase.lean:932` | Constructed modulated base package. |
| D053 | `NavierStokes.SlotGeometry.exists_oriented_slots` | `NavierStokes/SlotGeometry.lean:410` | Existence of oriented slot geometry. |
| D054 | `NavierStokes.SlotColoring.color_proper` | `NavierStokes/SlotColoring.lean:185` | Adjacent labels receive distinct colors. |
| D055 | `NavierStokes.TorusCoverDegree.card_liftedRectangles` | `NavierStokes/TorusCoverDegree.lean:296` | Exact number of lifted rectangles. |
| D056 | `NavierStokes.LabelCounting.number_of_relevant_labels` | `NavierStokes/LabelCounting.lean:259` | Uniform local relevant-label bound. |
| D057 | `NavierStokes.WeightedClasses.MeanClass` | `NavierStokes/WeightedClasses.lean:115` | Lean mean-coefficient class. |
| D058 | `NavierStokes.WeightedClasses.WaveClass` | `NavierStokes/WeightedClasses.lean:118` | Lean labelled-wave class. |
| D059 | `NavierStokes.WeightedClasses.MemClass.add` | `NavierStokes/WeightedClasses.lean:204` | Closure under addition. |
| D060 | `NavierStokes.WeightedClasses.MemClass.fderiv` | `NavierStokes/WeightedClasses.lean:228` | Closure/control under Fréchet differentiation. |
| D061 | `NavierStokes.WeightedClasses.MemClass.bilinear` | `NavierStokes/WeightedClasses.lean:299` | Bilinear product exponent rule. |
| D062 | `NavierStokes.WeightedClasses.MemClass.graphIterate` | `NavierStokes/WeightedClasses.lean:498` | Iterated graph-derivative bound. |
| D063 | `NavierStokes.PhaseEstimates.actual_phase_geometry` | `NavierStokes/PhaseEstimates.lean:930` | Actual phase nondegeneracy/geometry package. |
| D064 | `NavierStokes.TorusInverse.zero_mean_series_has_smooth_inverse` | `NavierStokes/TorusInverse.lean:586` | Smooth zero-mean Fourier inverse with estimates. |
| D065 | `NavierStokes.PartitionedCovariance.assembled_covariance` | `NavierStokes/PartitionedCovariance.lean:890` | Assembled covariance identity. |
| D066 | `NavierStokes.PartitionedCovariance.physical_primary_covariance` | `NavierStokes/PartitionedCovariance.lean:947` | Physical primary-wave covariance identity. |
| D067 | `NavierStokes.OscillatoryCurl.wave_divergence_free` | `NavierStokes/OscillatoryCurl.lean:188` | Divergence-free curl wave. |
| D068 | `NavierStokes.OscillatoryCurl.wave_eq_stripped` | `NavierStokes/OscillatoryCurl.lean:274` | Stripped oscillatory wave formula. |
| D069 | `NavierStokes.RadialPrimitive.exists_smooth_compact_primitive` | `NavierStokes/RadialPrimitive.lean:228` | Compact smooth radial primitive with moment condition. |
| D070 | `NavierStokes.MeanResidual.exact_cartesian_mean_balances` | `NavierStokes/MeanResidual.lean:1091` | Exact Cartesian mean-residual balances. |
| D071 | `NavierStokes.FiveRowRank.five_rows_on_patch` | `NavierStokes/FiveRowRank.lean:249` | Five-row linear system on a patch. |
| D072 | `NavierStokes.FiveRowRank.exists_five_row_repair` | `NavierStokes/FiveRowRank.lean:311` | Existence of the five-row repair. |
| D073 | `NavierStokes.FiveRowRank.uniform_finite_jet_bound` | `NavierStokes/FiveRowRank.lean:474` | Finite-jet repair bound. |
| D074 | `NavierStokes.CorrectionState.State` | `NavierStokes/CorrectionState.lean:65` | Finite correction-state structure. |
| D075 | `NavierStokes.CorrectionState.State.meanResidual_eq_good_add_excluded` | `NavierStokes/CorrectionState.lean:140` | Residual split into controlled and excluded parts. |
| D076 | `NavierStokes.ActualInitialization.initial_invariant` | `NavierStokes/ActualInitialization.lean:1427` | Initial-stage invariant. |
| D077 | `NavierStokes.ActualCyclePreservation.state_invariant` | `NavierStokes/ActualCyclePreservation.lean:835` | Invariant preservation through a correction cycle. |
| D078 | `NavierStokes.ActualCyclePreservation.state_result` | `NavierStokes/ActualCyclePreservation.lean:882` | Next-stage result and estimates. |
| D079 | `NavierStokes.ActualIterationLedger.gain_tendsto_atTop` | `NavierStokes/ActualIterationLedger.lean:107` | Iteration gain tends to infinity. |
| D080 | `NavierStokes.ActualIterationLedger.residualRate_tendsto_atTop` | `NavierStokes/ActualIterationLedger.lean:302` | All-order residual rate tends to infinity. |
| D081 | `NavierStokes.DiagonalJetBounds.tsum_jet_identity` | `NavierStokes/DiagonalJetBounds.lean:54` | Jets of the diagonal infinite sum. |
| D082 | `NavierStokes.DiagonalJetBounds.norm_tsum_sub_prefix_jet_le_of_locallyFinite` | `NavierStokes/DiagonalJetBounds.lean:180` | Jet-tail bound after a finite prefix. |
| D083 | `NavierStokes.LocalResidualFlatness.exists_schedule_all_jetRates` | `NavierStokes/LocalResidualFlatness.lean:80` | Schedule retaining every residual jet rate. |
| D084 | `NavierStokes.LocalResidualFlatness.selected_schedule` | `NavierStokes/LocalResidualFlatness.lean:113` | Closed selected schedule. |
| D085 | `NavierStokes.GermCandidateAssembly.exists_candidate_witness_of_finite_stages` | `NavierStokes/GermCandidateAssembly.lean:164` | Candidate witness from finite-stage data. |
| D086 | `NavierStokes.ActualCandidateConstruction.qbig_pos` | `NavierStokes/ActualCandidateConstruction.lean:157` | Positivity of the common `qbig` domain parameter. |
| D087 | `NavierStokes.ClosedIntervalMomentRepair.Data.exists_smooth_same_branch` | `NavierStokes/ClosedIntervalMomentRepair.lean:151` | Smooth same-branch moment repair. |
| D088 | `NavierStokes.ClosedIntervalMomentRepair.linear_solution` | `NavierStokes/ClosedIntervalMomentRepair.lean:210` | Linearized moment-equation solution. |
| D089 | `NavierStokes.FiveProfileMoments.momentMatrix_det_ne_zero` | `NavierStokes/FiveProfileMoments.lean:202` | Invertibility of the five-profile moment matrix. |
| D090 | `NavierStokes.FiveProfileMoments.compact_parameter_repair` | `NavierStokes/FiveProfileMoments.lean:805` | Compact-parameter five-moment repair. |
| D091 | `NavierStokes.PressureDatum.pressure_contDiff` | `NavierStokes/PressureDatum.lean:243` | Smooth pressure datum. |
| D092 | `NavierStokes.PressureDatum.deriv_pressure_pos_of_active` | `NavierStokes/PressureDatum.lean:354` | Positive derivative on the active region. |
| D093 | `NavierStokes.PressureDatum.manuscript_prefix_bound` | `NavierStokes/PressureDatum.lean:401` | Prefix estimate for pressure construction. |
| D094 | `NavierStokes.PressureDatum.pressure_neg_of_ideal_prefix` | `NavierStokes/PressureDatum.lean:446` | Negative pressure from the ideal prefix. |
| D095 | `NavierStokes.RadialHeatProfile.profile_contDiffOn` | `NavierStokes/RadialHeatProfile.lean:226` | Smooth radial heat profile. |
| D096 | `NavierStokes.RadialHeatProfile.profile_derivative_bound` | `NavierStokes/RadialHeatProfile.lean:234` | Fixed-order derivative bounds. |
| D097 | `NavierStokes.RadialHeatProfile.radial_heat_equation` | `NavierStokes/RadialHeatProfile.lean:624` | Radial heat equation. |
| D098 | `NavierStokes.RadialHeatProfile.scaled_radialProfile_derivative_neg` | `NavierStokes/RadialHeatProfile.lean:727` | Strict negative scaled radial derivative. |
| D099 | `NavierStokes.AppendixHeatResults.endpoint_derivatives` | `NavierStokes/AppendixHeatResults.lean:66` | Endpoint derivative formula. |
| D100 | `NavierStokes.TerminalCompensation.exists_heat_compensation` | `NavierStokes/TerminalCompensation.lean:896` | Terminal heat compensation with required moments. |
| D101 | `NavierStokes.FinalSlowBase.coefficient_stress_zero_right` | `NavierStokes/FinalSlowBase.lean:445` | Coefficient stress vanishes beyond the right edge. |
| D102 | `NavierStokes.FinalSlowBase.physicalStress_zero_right` | `NavierStokes/FinalSlowBase.lean:482` | Physical stress vanishes beyond the right edge. |
| D103 | `NavierStokes.FlatPrimitivePaper.exists_factor_on_rectangle` | `NavierStokes/FlatPrimitivePaper.lean:76` | Flat primitive factorization with mixed-jet bounds. |
| D104 | `NavierStokes.TerminalEdgePaper.profileStress_lower_bound` | `NavierStokes/TerminalEdgePaper.lean:16` | Terminal profile-stress lower bound. |
| D105 | `NavierStokes.AxisCoefficientSpace.CoefficientSpace` | `NavierStokes/AxisCoefficientSpace.lean:130` | Weighted coefficient Banach-space carrier. |
| D106 | `NavierStokes.AxisCoefficientSpace.coefficientSpace_complete` | `NavierStokes/AxisCoefficientSpace.lean:132` | Completeness instance for coefficient space. |
| D107 | `NavierStokes.AxisCoefficientSpace.AxisSpace` | `NavierStokes/AxisCoefficientSpace.lean:430` | Axis-profile fixed-point space. |
| D108 | `NavierStokes.AxisCoefficientSpace.axisSpace_complete` | `NavierStokes/AxisCoefficientSpace.lean:434` | Completeness of axis space. |
| D109 | `NavierStokes.AxisEvaluationAlgebra.profile_product` | `NavierStokes/AxisEvaluationAlgebra.lean:42` | Bounded profile multiplication. |
| D110 | `NavierStokes.AxisEvaluationAlgebra.regularInverse_equation` | `NavierStokes/AxisEvaluationAlgebra.lean:135` | Regular inverse for the singular radial operator. |
| D111 | `NavierStokes.AxisEvaluationAlgebra.primitive_integral` | `NavierStokes/AxisEvaluationAlgebra.lean:454` | Primitive/integration operator identity. |
| D112 | `NavierStokes.NaturalEntrance.exists_common_joint_analytic_profiles` | `NavierStokes/NaturalAxisJointAnalytic.lean:126` | Common jointly analytic natural-axis profiles. |
| D113 | `NavierStokes.NaturalExitBounds.exists_exit` | `NavierStokes/NaturalExitBounds.lean:155` | Controlled natural-axis exit data. |
| D114 | `NavierStokes.NaturalExitBounds.ideal_prefix_exit` | `NavierStokes/NaturalExitBounds.lean:230` | Ideal-prefix form of the exit. |
| D115 | `NavierStokes.ActualSlowAxis.fromNatural_profiles_smooth` | `NavierStokes/ActualSlowAxis.lean:468` | Smooth actual slow-axis profiles. |
| D116 | `NavierStokes.ActualSlowAxis.fromNatural_zero_axis` | `NavierStokes/ActualSlowAxis.lean:478` | Axis boundary values. |
| D117 | `NavierStokes.ActualSlowAxis.fromNatural_axis_jets` | `NavierStokes/ActualSlowAxis.lean:485` | Exact axis jets. |
| D118 | `NavierStokes.ReferenceEndpointRate.exists_linear_Ck_constants` | `NavierStokes/ReferenceEndpointRate.lean:156` | Finite-order endpoint constants. |
| D119 | `NavierStokes.ReferenceEndpointRate.exists_endpointLog_bound` | `NavierStokes/ReferenceEndpointRate.lean:226` | Endpoint logarithmic bound. |
| D120 | `NavierStokes.ReferenceEndpointRate.exists_entrance_envelope` | `NavierStokes/ReferenceEndpointRate.lean:275` | Entrance envelope retaining finite jets. |
| D121 | `NavierStokes.PreparedOutgoing.exists_prepared` | `NavierStokes/PreparedOutgoing.lean:36` | Existence of a prepared outgoing profile. |
| D122 | `NavierStokes.PreparedOutgoing.exists_matched_nominal` | `NavierStokes/PreparedOutgoing.lean:121` | Exact matching to the nominal outer profile. |
| D123 | `NavierStokes.OutgoingNegativeSlopeCone.exists_ordered_full_profile_cone` | `NavierStokes/OutgoingNegativeSlopeCone.lean:137` | Ordered continuation satisfying the full outgoing cone. |
| D124 | `NavierStokes.AppendixJoiningResults.axis_initial_margin` | `NavierStokes/AppendixJoiningResults.lean:17` | Initial cone margin for the axis join. |
| D125 | `NavierStokes.AppendixJoiningResults.axis_base_source_identity` | `NavierStokes/AppendixJoiningResults.lean:40` | Axis base-source identity. |
| D126 | `NavierStokes.AppendixJoiningResults.reference_first_gt_three` | `NavierStokes/AppendixJoiningResults.lean:67` | Reference lower-bound inequality for the join. |
| D127 | `NavierStokes.RadialModulation.angular_shear_exact` | `NavierStokes/RadialModulation.lean:136` | Exact angular shear after modulation. |
| D128 | `NavierStokes.RadialModulation.axial_shear_exact` | `NavierStokes/RadialModulation.lean:152` | Exact axial shear after modulation. |
| D129 | `NavierStokes.RadialModulation.uniform_modulatedE_eta_jets` | `NavierStokes/RadialModulation.lean:372` | Uniform parameter jets for modulated angular profile. |
| D130 | `NavierStokes.RadialModulation.uniform_modulatedU_eta_jets` | `NavierStokes/RadialModulation.lean:398` | Uniform parameter jets for modulated axial profile. |
| D131 | `NavierStokes.ModulatedProfileJetRates.exists_with_moment_repair_all_jets` | `NavierStokes/ModulatedProfileJetRates.lean:347` | Modulation plus moment repair with all-jet control. |
| D132 | `NavierStokes.ModulatedCone.exists_with_moment_repair` | `NavierStokes/ModulatedCone.lean:1414` | Moment-repaired modulated profile with restored cone. |

## Bottom line

The static source provides an explicit official path for exactly two numbered manuscript results: Theorem 1.1 and Corollary 10.6. It also contains a substantial network of declaration-level counterparts for many intermediate constructions and appendices, but a filename, import, suggestive theorem name, or downstream use is not treated as full coverage. Any stronger claim requires a successful build and, for statement identity beyond the two metadata alignments, a separate semantic proof of equivalence.
