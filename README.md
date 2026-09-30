# Everyday English Edition of the Navier–Stokes Proof

**Experimental attempt; unfinished and not established as successful.**
This repository preserves an attempt to present the paper in Everyday English.
A full-paper draft and its PDF, EPUB, HTML and LaTeX were produced, but page
coverage and build checks did not establish that the writing met its intended
purpose. That draft was subsequently rejected as the basis for a new rewrite.
The later manual effort returned to source page 1 and remained unfinished.
The earlier files are retained for reading, comparison and reference. Statements
of completion in older receipts describe the producer's earlier release decision,
not current acceptance of the experiment.

[Read the experimental draft online](https://kokunoyumeto.github.io/navier-stokes-proof-everyday-english/) · [Read the PDF](output/everyday-english/pdf/everyday-english-edition.pdf) · [Download the EPUB](output/everyday-english/epub/everyday-english-edition.epub) · [Open the LaTeX](everyday/main.tex)

The earlier full-paper draft attempts an Everyday English treatment of OpenAI's 166-page paper *Finite Time Blowup for Navier–Stokes*. It keeps the mathematics, formulas, notation, claim order, numbered statements, proofs, citations, and source-page links. The prose around them has been rewritten so that each idea says who or what acts, what it acts on, why the step is needed, and what follows from it.

Technical terms stay when the mathematics needs them. The first place that needs a term also says what the term means and what job it does there. Explanations added for the reader are marked and kept separate from claims made by the source paper.

This is an independent edition, not an official OpenAI release. The [official paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) remains the authority for the paper itself. The editable source-faithful reconstruction used to make this edition lives in the separate [`openai-navier-stokes-latex`](https://github.com/KokunoYumeto/openai-navier-stokes-latex) repository.

## Ways to read it

- The [online edition](https://kokunoyumeto.github.io/navier-stokes-proof-everyday-english/) has stable source-page anchors, native MathML, keyboard-readable links, and text alternatives for images.
- The [PDF](output/everyday-english/pdf/everyday-english-edition.pdf) is the page-based reading copy.
- The [EPUB](output/everyday-english/epub/everyday-english-edition.epub) is made for reflowable reading software.
- [`everyday/main.tex`](everyday/main.tex) and [`everyday/sections/`](everyday/sections/) contain the complete editable edition.

## How the edition is checked

Every section is tied to the matching source span and source-page marker. The records under [`evidence/translation/`](evidence/translation/) give the source and target hashes, the exact change, its language evidence, its mathematical checks, and any term that had to stay. The formula records check each formula in both directions. The [first-use record](evidence/translation/FIRST_USE_FINALIZATION.json) shows where technical ideas first become clear in the running text.

The historical release gate accepted builds designated final by the producer. It checks the PDF, HTML, and EPUB against their recorded SHA-256 hashes; requires two matching builds of each format; requires all 29 Everyday English range audits to pass; requires zero unresolved references, zero unresolved citations, and zero overfull boxes; requires EPUBCheck to pass; and requires the final PDF's every-page visual record. The exact release decision is in [`EVERYDAY_ENGLISH_FINAL_QA.json`](evidence/build/EVERYDAY_ENGLISH_FINAL_QA.json). [`MANIFEST.sha256`](MANIFEST.sha256) binds every file in the repository to the bytes that were staged.

The historical checks record correspondence, build integrity, and review work; they do not establish the success of the writing experiment. They do not independently prove the mathematics, turn this edition into an official source, or decide recognition by the Clay Mathematics Institute.

## Illustrations

The edition includes a mathematical sign diagram for the angular-momentum flux mechanism. Its PDF and SVG are in [`everyday/illustrations/`](everyday/illustrations/), and its reproducible TikZ source is in [`everyday/illustrations/src/`](everyday/illustrations/src/). The caption states exactly what the diagram shows and what it does not show. The [illustration ledger](evidence/illustrations/ILLUSTRATIONS.jsonl) records the mathematical claims, coordinates, labels, source locators, and checked output hashes.

The six figures from the paper remain separate source figures. Their checked vector assets are under [`reconstruction/assets/figures/`](reconstruction/assets/figures/).

## Build the book

The checked build uses Python 3, pdfLaTeX, Pandoc, Poppler's `pdfinfo`, Java, and the locked EPUBCheck release named in [`everyday/epubcheck-lock.json`](everyday/epubcheck-lock.json). The Python environment needs `lxml`, `latex2mathml`, and `pypdf`. A TeX Live or MiKTeX installation also needs the packages named in `everyday/ee-edition.sty` and `reconstruction/ns-edition.sty`.

On Windows, fetch and verify the locked EPUBCheck files once:

```powershell
powershell -NoProfile -File scripts/fetch_epubcheck.ps1
```

Then run the complete deterministic build from the repository root:

```powershell
python scripts/build_everyday_edition.py all --profile final
```

The command builds each format twice, compares the resulting bytes, runs the range and structure checks, runs EPUBCheck, and writes exact receipts under `output/everyday-english/receipts/`. A final build does not by itself replace the separate every-page visual review named by the release gate.

## Repository map

- `everyday/` contains the full-paper Everyday English draft in LaTeX and the edition's illustration files.
- `docs/` contains the checked HTML served by GitHub Pages.
- `output/everyday-english/pdf/` contains the checked PDF.
- `output/everyday-english/epub/` contains the checked EPUB.
- `reconstruction/` contains the verified source layer needed for exact comparison and a local rebuild.
- `evidence/translation/` contains the segment, change, first-use, mathematics, and addition records.
- `evidence/transcription/` contains the source-page and LaTeX correspondence records used by this edition.
- `evidence/lean/` maps manuscript statements to exact locations in OpenAI's frozen Lean revision and says where the mapping stops.
- `evidence/illustrations/` records the edition's added mathematical illustration.
- `evidence/build/` and `output/everyday-english/receipts/` contain the final release and build checks.
- `scripts/` contains the reproducible builders and audits.

## Source, formal code, and status

The official paper and OpenAI's formal repository have different jobs. The PDF is the authority for the paper's prose and printed mathematics. The [official Lean repository](https://github.com/openai/NavierStokesAndEuler) is the authority for its own code. [`MANUSCRIPT_LEAN_MAP.md`](evidence/lean/MANUSCRIPT_LEAN_MAP.md) links the two where exact source reading supports a link and states the remaining gaps. A Lean file or successful build cannot prove that a sentence was transcribed or rewritten without a change in meaning.

For the mathematical work, cite the official OpenAI paper. When referring to this edition, also give this repository and the exact Git commit used. No personal attribution has been inferred for the independent edition.

## Rights and reuse

The records examined for this project do not establish a licence for the paper, its figures, the source-faithful reconstruction, or this complete edition. Public access and source links do not settle reuse rights. See [`LICENSE-NOTICE.md`](LICENSE-NOTICE.md) before redistributing or adapting the files.
