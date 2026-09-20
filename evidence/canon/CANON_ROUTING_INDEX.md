# Everyday English canon routing index

This index routes bounded language jobs for the Everyday English Edition to the corpus's current checked human passages. It contains all 34 passages in the passing canon and no wider-pool or negative-example material.

It is evidence about attested wording and explanation shape, not a translation template. Nothing here establishes universal comprehension, population frequency, mathematical correctness, or source-to-target equivalence. The frozen mathematical source and a separate bidirectional audit remain authoritative.

In each exact-quote block, the text after the first `|` is copied unchanged from the `text_exact` field of the accepted exact record. The line number and speaker/writer before the separator are locator metadata. Each quote range is contained in its accepted passage range; no quote has been expanded beyond the stored excerpt.

## Current control basis

- Canon report: `pass`; 34 passages; 29 sources; 692 exact language lines; 4145 searchable words.
- Build report: `pass` with 0 issues.
- Reference-layer report: `pass` with 34 positive canon passages and 0 issues.
- Admission intersection: checked canon manifest membership, source status `included`, exact record `verified_direct_human_language: true`, and membership in a positive reference layer.
- Count precedence: the historical first-build section records 30 passages; the later expansion, current manifest, exact index, and passing reports agree on 34. This index follows that current 34-record intersection.

### Input fingerprints

| Corpus-relative file | SHA-256 |
|---|---|
| `README.md` | `e077b248ed37cfbe12733af7f697acbca1f68fb6db2af2594392507390b0f3e2` |
| `SELECTION_POLICY.md` | `04ec6c80e58a6c2fad696b97d20fa3b72221b4d762f97ffa9a1006076cbed6a9` |
| `EXCLUSIONS.md` | `7cbe8444c73a9e1583efcce3911194198d6ef761514bd14191745e2d083cdaaa` |
| `CANON_USAGE_GUIDE.md` | `7455890f484e221df9352e897ff5ef9f75a7ed0513b8b6d918773c1f0679cc3b` |
| `BUILD_LOG.md` | `6b6cea5973d601ddf01dce5ae8f6f82dcbc37f91be7ee522b73d8231e1b7a19d` |
| `sources/source_selection.json` | `8e2ff8e67a1ef7f9932830d421ba09630bb5ffa82aa8393910435528caa8a627` |
| `sources/canon_passages.json` | `6baa9a1b6071fcbcd6192695e55efb1d056d111f3ec7055bfc6e04dc4f4f5601` |
| `sources/reference_layers.json` | `303b8f00dc0b96df6adbf3ee36c4802ac00d3d12ebf1a4e7542f8f26685de9f7` |
| `derived/CANON_INDEX.md` | `10043ee86ecb4cb11d05eda1295dafdbedfeb7b11dc1de4e352d95d1e8d20520` |
| `derived/canon_passages_exact.jsonl` | `11f5fbd4bbdf22cf1ce97c91e469a69048207d26156e7be7035eaf566abf5237` |
| `checks/build_report.json` | `507ab96cd0c29285607ee8114d20a8c48d92bcc7f389930deddc85c7e654c95e` |
| `checks/canon_report.json` | `c8dd8f58bc55cfb54e45b1a07c3d33bb2aba6d36e75063bc81ee56ad01d38d9a` |
| `checks/reference_layers_report.json` | `39cde94c53155936c1d3a33ee1470befd1eda3af0c23668e3f847178d247c78b` |

## Bounded role vocabulary

| Role | Meaning in this index |
|---|---|
| `afterthought` | Add a practical extra after the main message has closed. |
| `alternative_cases` | Lay out distinct cases or branches explicitly. |
| `causal_explanation` | State a reason or cause and connect it to a result. |
| `comparison_analogy` | Set cases side by side or use a comparison to make an experience intelligible. |
| `concrete_description` | Answer what a named thing is like or contains without claiming a formal definition. |
| `contrast` | Make a difference, reversal, exception, or catch visible. |
| `correction` | Reject a proposed reading or move and supply a repair. |
| `definition` | State a technical defining condition while retaining the technical object. |
| `direct_instruction` | Tell a listener a concrete action to perform. |
| `direct_request` | Ask directly for one concrete action or confirmation without implying a wider negotiation. |
| `equivalent_restatement` | Put two equivalent readings of one condition next to each other. |
| `inference` | Make a conclusion explicit from facts or counts already stated. |
| `narrative` | Put events in time order and show what changed or resulted. |
| `observable_cue` | Tie an action to a visible or otherwise directly checkable signal. |
| `personal_update` | Give connected private news or circumstances in ordinary writing. |
| `practical_rationale` | Explain why an action, order, or choice is useful in practice. |
| `process_explanation` | Explain how a physical or practical process unfolds. |
| `question_and_response` | Pose a concrete question and give or elicit a direct answer. |
| `reference_recovery` | Ask or show where an earlier result, detail, or referent came from. |
| `reported_speech` | Retell what people said as part of an event narrative. |
| `request_negotiation` | Ask for an action and adjust its timing, scope, or terms in interaction. |
| `response_evaluation` | Give a direct response or evaluation after a question, proposal, or trial. |
| `rule_statement` | State the aim or governing rule of an activity. |
| `scope_condition` | State the case, requirement, exception, or boundary under which a claim or action applies. |
| `sequence` | Order steps, actions, or events so their progression is explicit. |
| `sympathy_support` | Express concern or support while giving the circumstances that call for it. |
| `time_anchoring` | Place an event relative to a remembered or dated point in time. |

Roles name only what the cited passage can support in its recorded setting. They do not turn a local example into a general rule of English.

## Quick routing table

| Canon ID | Stable source ID and accepted locator | Mode | Bounded roles |
|---|---|---|---|
| `EE-001` | `SBC009:L11-L20` | spoken | `reference_recovery`, `sequence` |
| `EE-002` | `SBC009:L84-L105` | spoken | `sequence`, `scope_condition`, `causal_explanation` |
| `EE-003` | `SBC009:L443-L460` | spoken | `correction`, `direct_instruction` |
| `EE-004` | `SBC009:L663-L678` | spoken | `rule_statement`, `causal_explanation`, `alternative_cases` |
| `EE-005` | `SBC024:L519-L544` | spoken | `rule_statement`, `direct_instruction`, `scope_condition` |
| `EE-006` | `SBC024:L642-L652` | spoken | `inference`, `causal_explanation` |
| `EE-007` | `SBC002:L75-L104` | spoken | `process_explanation`, `sequence`, `causal_explanation` |
| `EE-008` | `SBC031:L6-L19` | spoken | `concrete_description`, `response_evaluation` |
| `EE-009` | `SBC043:L472-L496` | spoken | `sequence`, `practical_rationale`, `causal_explanation` |
| `EE-010` | `SBC051:L1512-L1522` | spoken | `direct_instruction`, `sequence` |
| `EE-011` | `SBC052:L905-L916` | spoken | `scope_condition`, `contrast` |
| `EE-012` | `SBC050:L19-L48` | spoken | `direct_instruction`, `response_evaluation` |
| `EE-013` | `SBC034:L25-L50` | spoken | `narrative`, `reported_speech`, `causal_explanation` |
| `EE-014` | `SBC003:L160-L180` | spoken | `question_and_response`, `causal_explanation` |
| `EE-015` | `SBC005:L23-L50` | spoken | `comparison_analogy`, `contrast`, `narrative` |
| `EE-016` | `SBC058:L28-L57` | spoken | `request_negotiation`, `direct_instruction`, `sequence`, `causal_explanation` |
| `EE-017` | `SBC059:L30-L58` | spoken | `narrative`, `sequence`, `causal_explanation`, `inference` |
| `EE-018` | `SBC060:L1-L42` | spoken | `narrative`, `time_anchoring`, `causal_explanation` |
| `EE-019` | `SBC047:L18-L61` | spoken | `narrative`, `sequence`, `causal_explanation` |
| `EE-020` | `SBC048:L45-L68` | spoken | `question_and_response`, `direct_instruction`, `observable_cue` |
| `EE-021` | `SCOTS996:L13-L50` | spoken | `practical_rationale`, `contrast`, `direct_instruction` |
| `EE-022` | `SCOTS1384:L19-L49` | spoken | `narrative`, `sequence`, `contrast` |
| `EE-023` | `SCOTS027:L239-L253` | spoken | `contrast`, `comparison_analogy` |
| `EE-024` | `SCOTS1570:L14-L53` | spoken | `direct_instruction`, `sequence`, `correction`, `scope_condition` |
| `EE-025` | `SCOTS394:L19-L31` | written | `personal_update`, `inference`, `causal_explanation` |
| `EE-026` | `SCOTS395:L16-L28` | written | `sympathy_support`, `personal_update` |
| `EE-027` | `SCOTS397:L15-L38` | written | `personal_update`, `causal_explanation`, `scope_condition` |
| `EE-028` | `SCOTS399:L18-L42` | written | `narrative`, `personal_update`, `sympathy_support` |
| `EE-029` | `SCOTS1458:L15-L31` | written | `personal_update`, `direct_request`, `practical_rationale` |
| `EE-030` | `SCOTS1458:L45-L59` | written | `personal_update`, `afterthought` |
| `EE-031` | `COOK116793:L14` | written | `sequence`, `causal_explanation`, `practical_rationale` |
| `EE-032` | `COOK40170:L14` | written | `causal_explanation`, `inference` |
| `EE-033` | `MSE1087517:L14` | written | `definition` |
| `EE-034` | `MSE3427924:L14` | written | `definition`, `equivalent_restatement` |

## Passage records

### EE-001 — SBC009:L11-L20

- Stable source ID: `SBC009`
- Accepted source locator: `SBC009:L11-L20`
- Exact quote locator: `SBC009:L11-L20`
- Bounded roles: `reference_recovery`, `sequence`
- Canonical function: Ask where a result came from and unpack the calculation into actions.
- Context: spoken; one teenager helping another study for a math test; US English; Mobile, Alabama
- Public/source links: [Zero Equals Zero](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC009.trn)
- Local corpus file: `sources/sbcsae/raw/SBC009.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L11 NATHAN | [I] don't know what I did to ge=t that.
L12 NATHAN | .. Where did I get that .. square root of- --
L13 NATHAN | um=,
L14 NATHAN | ... ex squa[red].
L15 KATHY | [Because] you brought this .. over here.
L16 KATHY | ... You brought ... three (H) over here.
L17 KATHY | ... divided by three,
L18 KATHY | (H) and then you have ex squared,
L19 KATHY | so if you want to find ex,
L20 KATHY | you have the square root of ex squared.
```

Limits: Evidence for explanatory language only. It is not a check that the calculation is right. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-002 — SBC009:L84-L105

- Stable source ID: `SBC009`
- Accepted source locator: `SBC009:L84-L105`
- Exact quote locator: `SBC009:L84-L105`
- Bounded roles: `sequence`, `scope_condition`, `causal_explanation`
- Canonical function: Give the next calculation step, answer a scope question, and say why the step is needed.
- Context: spoken; one teenager helping another study for a math test; US English; Mobile, Alabama
- Public/source links: [Zero Equals Zero](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC009.trn)
- Local corpus file: `sources/sbcsae/raw/SBC009.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L84 KATHY | ... So then you just multiply=,
L85 KATHY | the whole thing by the square root of two,
L86 KATHY | and you get the square root of two over two.
L87 KATHY | ... @ (H)[=]
L88 NATHAN | [Even f]or the top .. one?
L89 NATHAN | ... Even for that one?
L90 KATHY | ... No=.
L91 KATHY | For- --
L92 KATHY | I'm talking about for this one.
L93 NATHAN | ... Oh=.
L94 NATHAN | ... (H) All you do is like go,
L95 NATHAN | .. [t- .. two over one],
L96 KATHY | [You have the square root of one=],
L97 NATHAN | like that,
L98 NATHAN | right?
L99 KATHY | ... M-m.
L100 KATHY | ... Since you have the square root of two on the bottom,
L101 KATHY | ... to make that a square,
L102 KATHY | you have to multiply by the square root of two.
L103 KATHY | ... (H) And then you get two=,
L104 KATHY | (H) and you multiply the top by the square root of two,
L105 KATHY | .. and you get,
```

Limits: Evidence for wording, scope repair, and sequencing only; not mathematical authority. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-003 — SBC009:L443-L460

- Stable source ID: `SBC009`
- Accepted source locator: `SBC009:L443-L460`
- Exact quote locator: `SBC009:L447-L460`
- Bounded roles: `correction`, `direct_instruction`
- Canonical function: Correct a proposed method and restate the concrete move to make.
- Context: spoken; one teenager helping another study for a math test; US English; Mobile, Alabama
- Public/source links: [Zero Equals Zero](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC009.trn)
- Local corpus file: `sources/sbcsae/raw/SBC009.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L447 KATHY | ... Just bring nega- --
L448 KATHY | .. Just bring two-thirds,
L449 KATHY | ... over to the other side.
L450 KATHY | Negative two-thirds,
L451 KATHY | over to the other side.
L452 NATHAN | ... And make it equal to zero?
L453 KATHY | ... No.
L454 KATHY | No keep that there,
L455 KATHY | .. (H) But then have,
L456 NATHAN | Another one over there?
L457 KATHY | Yeah,
L458 KATHY | have,
L459 KATHY | ... is .. less than or equal to,
L460 KATHY | .. (H) negative two ... thirds.
```

Limits: Evidence for correction and instruction language only; not mathematical authority. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-004 — SBC009:L663-L678

- Stable source ID: `SBC009`
- Accepted source locator: `SBC009:L663-L678`
- Exact quote locator: `SBC009:L663-L678`
- Bounded roles: `rule_statement`, `causal_explanation`, `alternative_cases`
- Canonical function: State a rule, give the reason, and split the result into alternatives.
- Context: spoken; one teenager helping another study for a math test; US English; Mobile, Alabama
- Public/source links: [Zero Equals Zero](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC009.trn)
- Local corpus file: `sources/sbcsae/raw/SBC009.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L663 KATHY | ... And when you divide by a ne[gative],
L664 NATHAN | [(Hx)]
L665 KATHY | .. [2you have to flip the signs2].
L666 NATHAN | [2(TSK) Yeah=2].
L667 NATHAN | (H) .. Okay.
L668 KATHY | ... And when you do that,
L669 KATHY | .. it's gonna be a o=r.
L670 KATHY | ... (H) Because if you look at it,
L671 KATHY | ... cause,
L672 KATHY | you know,
L673 KATHY | it can't be greater ... than seven-halves,
L674 KATHY | ... and less than negative halve at the sa-,
L675 KATHY | one-half at the same time.
L676 KATHY | ... So it's gonna be either ex,
L677 KATHY | .. is less than or equal to negative ... one-half,
L678 KATHY | .. (H) or,
```

Limits: Evidence for causal and alternative structure only; not mathematical authority. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-005 — SBC024:L519-L544

- Stable source ID: `SBC024`
- Accepted source locator: `SBC024:L519-L544`
- Exact quote locator: `SBC024:L522-L544`
- Bounded roles: `rule_statement`, `direct_instruction`, `scope_condition`
- Canonical function: Teach the aim and basic rules of a card game.
- Context: spoken; a couple teaching and playing a computer game; US English; Cape Cod, Massachusetts
- Public/source links: [Risk](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC024.trn)
- Local corpus file: `sources/sbcsae/raw/SBC024.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L522 JENNIFER | .. Always pass left.
L523 DAN | ... (THROAT)
L524 JENNIFER | ... Alright.
L525 JENNIFER | ... (TSK) (H) So this is us[=.
L526 DAN | [<@ Groucho,
L527 DAN | Harpo @>],
L528 JENNIFER | .. % The object,
L529 JENNIFER | okay,
L530 JENNIFER | every] heart,
L531 JENNIFER | ... okay,
L532 JENNIFER | every heart is one [point,
L533 DAN | [Is tr-] --
L534 JENNIFER | the q-] queen of spades is thirteen points,
L535 JENNIFER | the object is not to have any points.
L536 JENNIFER | .. And,
L537 JENNIFER | (H) you p=lay following suit,
L538 JENNIFER | ... an=d,
L539 JENNIFER | ... you can take,
L540 JENNIFER | if you take tricks,
L541 JENNIFER | th- the highest card of the suit,
L542 JENNIFER | takes the trick.
L543 JENNIFER | If you don't have the card of the suit,
L544 JENNIFER | [you throw] (H) whatever you want.
```

Limits: The overlapping turns and false starts belong to speech and are not a model for finished prose. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-006 — SBC024:L642-L652

- Stable source ID: `SBC024`
- Accepted source locator: `SBC024:L642-L652`
- Exact quote locator: `SBC024:L648-L652`
- Bounded roles: `inference`, `causal_explanation`
- Canonical function: Reason from a total and a visible count to what remains.
- Context: spoken; a couple teaching and playing a computer game; US English; Cape Cod, Massachusetts
- Public/source links: [Risk](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC024.trn)
- Local corpus file: `sources/sbcsae/raw/SBC024.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L648 JENNIFER | [Okay,
L649 JENNIFER | cause there are] thirteen cards,
L650 JENNIFER | I'm assuming it's an equal deal.
L651 JENNIFER | Now there are eight clubs out,
L652 JENNIFER | (H) that means there are only f=our more left.
```

Limits: Evidence for making an inference explicit in conversation, not a mathematical proof model. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-007 — SBC002:L75-L104

- Stable source ID: `SBC002`
- Accepted source locator: `SBC002:L75-L104`
- Exact quote locator: `SBC002:L85-L100`
- Bounded roles: `process_explanation`, `sequence`, `causal_explanation`
- Canonical function: Explain a physical process and connect it to an observed difference.
- Context: spoken; friends talking after dinner; US English; San Francisco, California
- Public/source links: [Lambada](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC002.trn)
- Local corpus file: `sources/sbcsae/raw/SBC002.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L85 MILES | there's] less calcium % deposits <X in them X>.
L86 MILES | ... [2And2] also,
L87 PETE | [2Mm2].
L88 MILES | .. they're still growing.
L89 MILES | ... And the way= ... bones grow is,
L90 MILES | .. you make cartilage,
L91 MILES | .. and then you deposit calcium in it.
L92 HAROLD | Oh,
L93 HAROLD | and [then that turns into hard bone].
L94 MILES | [So that's why they always have] ... more flexibility.
L95 MILES | Cause [2as2] they're growing,
L96 PETE | [2Hm2].
L97 MILES | ... you're making cartilage.
L98 MILES | So it [al- --
L99 PETE | [Mhm].
L100 MILES | They] always have that,
```

Limits: The biological claims have not been fact-checked; only the language is evidence here. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-008 — SBC031:L6-L19

- Stable source ID: `SBC031`
- Accepted source locator: `SBC031:L6-L19`
- Exact quote locator: `SBC031:L12-L19`
- Bounded roles: `concrete_description`, `response_evaluation`
- Canonical function: Answer what a named thing is by listing its concrete parts.
- Context: spoken; family talking over lunch in a restaurant; US English; Pullman, Washington
- Public/source links: [Tastes Very Special](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC031.trn)
- Local corpus file: `sources/sbcsae/raw/SBC031.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L12 ROSEMARY | [What in the w]orld is a Philadelphia [2s-2] --
L13 SHERRY | [2(TSK)2] .. It's [3r=oast3] beef with,
L14 ROSEMARY | [3(Hx)3]
L15 SHERRY | ... [4melted4] cheese and sauteed onion[5s.
L16 ROSEMARY | [4(Hx)4]
L17 ROSEMARY | [5Mm.
L18 ROSEMARY | That does sound good5].
L19 SHERRY | On a hoagie roll5].
```

Limits: This is an ordinary practical description, not a formal definition. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-009 — SBC043:L472-L496

- Stable source ID: `SBC043`
- Accepted source locator: `SBC043:L472-L496`
- Exact quote locator: `SBC043:L483-L495`
- Bounded roles: `sequence`, `practical_rationale`, `causal_explanation`
- Canonical function: Explain a simple recipe and the practical result of doing it that way.
- Context: spoken; mother and daughter talking at home; US English; Boise, Idaho
- Public/source links: [Try a Couple Spoonfuls](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC043.trn)
- Local corpus file: `sources/sbcsae/raw/SBC043.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L483 ALICE | we stopped at the store and got the stuff,
L484 ALICE | ... cause all you have to do is brown some hamburger and,
L485 ALICE | ... [onions],
L486 ANNETTE | [Yeah].
L487 ALICE | and then toss ca=ns of stuff in,
L488 ALICE | and spices.
L489 ALICE | .. (H) He says [that'd] good,
L490 ANNETTE | [(SNIFF)]
L491 ALICE | and,
L492 ALICE | ... then we wouldn't have to --
L493 ANNETTE | ... To .. cook a lot.
L494 ANNETTE | And you don't end up dirtying a lot of dish[es,
L495 ALICE | [Yeah.
```

Limits: Some wording is reported speech; none is read from an outside written source. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-010 — SBC051:L1512-L1522

- Stable source ID: `SBC051`
- Accepted source locator: `SBC051:L1512-L1522`
- Exact quote locator: `SBC051:L1519-L1522`
- Bounded roles: `direct_instruction`, `sequence`
- Canonical function: Give a short sequence of practical actions.
- Context: spoken; friends talking before and during dinner at home; US English; Laguna Beach, California
- Public/source links: [New Yorkers Anonymous](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC051.trn)
- Local corpus file: `sources/sbcsae/raw/SBC051.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L1519 FRAN | ... See what you do is,
L1520 FRAN | you sort of sidle up to em,
L1521 FRAN | and you give em a bump.
L1522 FRAN | ... And then you get in.
```

Limits: The advice is humorous; it is evidence for conversational instruction shape only. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-011 — SBC052:L905-L916

- Stable source ID: `SBC052`
- Accepted source locator: `SBC052:L905-L916`
- Exact quote locator: `SBC052:L906-L915`
- Bounded roles: `scope_condition`, `contrast`
- Canonical function: Explain how an offer works, including the requirement and the catch.
- Context: spoken; family Christmas phone call; US English; New Mexico and Texas
- Public/source links: [Oh You Need a Breadbox](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC052.trn)
- Local corpus file: `sources/sbcsae/raw/SBC052.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L906 CINDY | One thing,
L907 CINDY | we joined a book club.
L908 CINDY | And I got it for hardly any money,
L909 CINDY | you know,
L910 CINDY | they'll send you all these free books,
L911 CINDY | all you have to do is do postage,
L912 CINDY | (H) and then supposedly,
L913 CINDY | you don't have to u=m (Hx),
L914 CINDY | .. (TSK) (H) buy any more books,
L915 CINDY | but they want you to (Hx).
```

Limits: The account is personal recollection, not verified consumer advice. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-012 — SBC050:L19-L48

- Stable source ID: `SBC050`
- Accepted source locator: `SBC050:L19-L48`
- Exact quote locator: `SBC050:L41-L48`
- Bounded roles: `direct_instruction`, `response_evaluation`
- Canonical function: Ask what something is like, answer briefly, and respond after trying it.
- Context: spoken; roommates making plans and talking about their home; US English; Burlington, Vermont
- Public/source links: [Just Wanna Hang](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC050.trn)
- Local corpus file: `sources/sbcsae/raw/SBC050.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L41 DANA | ... You wanna piece of toast?
L42 KELLY | ... (TSK) Sure (Hx).
L43 DANA | ... Here.
L44 DANA | Try some of it first.
L45 KELLY | ... (TSK)
L46 KELLY | ... <FOOD It's different.
L47 KELLY | ... I like it.
L48 KELLY | ... When'd she start making this FOOD>.
```

Limits: Speech fragments and event tags are preserved in the exact source but need not be copied into prose. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-013 — SBC034:L25-L50

- Stable source ID: `SBC034`
- Accepted source locator: `SBC034:L25-L50`
- Exact quote locator: `SBC034:L42-L50`
- Bounded roles: `narrative`, `reported_speech`, `causal_explanation`
- Canonical function: Retell a small problem in time order and include what people said.
- Context: spoken; a married couple talking at home late at night; US English; Northampton, Massachusetts
- Public/source links: [What Time is it Now?](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC034.trn)
- Local corpus file: `sources/sbcsae/raw/SBC034.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L42 KAREN | ... (H) These kids were- came in,
L43 KAREN | and,
L44 KAREN | ... I was .. like,
L45 KAREN | w- we're closing %.
L46 KAREN | In a few minutes,
L47 KAREN | they said,
L48 KAREN | well we'll --
L49 KAREN | We'll wait until you kick us out.
L50 KAREN | Cause they didn't really want to buy anything,
```

Limits: Quoted lines are the speaker's own retelling, not language read from a script or document. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-014 — SBC003:L160-L180

- Stable source ID: `SBC003`
- Accepted source locator: `SBC003:L160-L180`
- Exact quote locator: `SBC003:L168-L180`
- Bounded roles: `question_and_response`, `causal_explanation`
- Canonical function: Ask whether something existed before and give a reason for a guess.
- Context: spoken; friends making dinner; US English; Southern California
- Public/source links: [Conceptual Pesticides](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC003.trn)
- Local corpus file: `sources/sbcsae/raw/SBC003.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L168 ROY | ... Is this= like something you had when you were young,
L169 ROY | in your own family?
L170 MARILYN | .. No.
L171 MARILYN | .. It's brand new.
L172 MARILYN | [Oh shit].
L173 PETE | [Yeah,
L174 PETE | I don't think] they ever --
L175 PETE | .. did they actually exist [2back then2]?
L176 MARILYN | [2<X Hey bud X>2].
L177 MARILYN | [3X3].
L178 ROY | [3No3],
L179 ROY | and they probably didn't have to wash their salads back then,
L180 ROY | because they didn't know= what was on them.
```

Limits: The pesticide claim is not fact-checked; the passage supplies language evidence only. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-015 — SBC005:L23-L50

- Stable source ID: `SBC005`
- Accepted source locator: `SBC005:L23-L50`
- Exact quote locator: `SBC005:L31-L50`
- Bounded roles: `comparison_analogy`, `contrast`, `narrative`
- Canonical function: Make a difficult personal experience understandable through an extended comparison.
- Context: spoken; a couple talking in bed; US English; Santa Barbara, California
- Public/source links: [A Book About Death](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC005.trn)
- Local corpus file: `sources/sbcsae/raw/SBC005.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L31 PAMELA | ... (H) that the marriage itself=,
L32 PAMELA | I mean as h=ellish as it was,
L33 PAMELA | ... % .. it's like it pulled me under,
L34 PAMELA | like a giant octopus,
L35 PAMELA | or a giant,
L36 PAMELA | % ... giant shark.
L37 PAMELA | (H) And it pulled me all the way under.
L38 PAMELA | And then,
L39 PAMELA | (H) ... and there I was,
L40 PAMELA | it was like the silent scream,
L41 PAMELA | and then,
L42 PAMELA | .. then I found that .. I% was on my own two feet again.
L43 PAMELA | And it r=eally was --
L44 PAMELA | (H) .. (Hx) ... % .. % (Hx) (H) (TSK)
L45 PAMELA | S- what was hell in that .. that marriage became,
L46 PAMELA | ... became a way out for me.
L47 PAMELA | ... It was the flip side.
L48 PAMELA | (H) .. It's like sometimes you go through things,
L49 PAMELA | ... and you come out the other side of them,
L50 PAMELA | <WH you WH> .. come out so much better.
```

Limits: The imagery belongs to this speaker and is not a stock template for explanatory prose. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-016 — SBC058:L28-L57

- Stable source ID: `SBC058`
- Accepted source locator: `SBC058:L28-L57`
- Exact quote locator: `SBC058:L28-L48`
- Bounded roles: `request_negotiation`, `direct_instruction`, `sequence`, `causal_explanation`
- Canonical function: Make a request, break it into actions, negotiate timing, and give a reason.
- Context: spoken; mother and son talking while making dinner; US English; Boise, Idaho
- Public/source links: [Swingin' Kid](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC058.trn)
- Local corpus file: `sources/sbcsae/raw/SBC058.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L28 SHERI | You know what you could do,
L29 SHERI | that would be just .. really helpful?
L30 STEVEN | ... Say it.
L31 SHERI | .. @ 
L32 SHERI | You could p- take these Coke cans,
L33 SHERI | ... and put them in the bag full of Coke cans that are in your bedroom,
L34 SHERI | ... and then we can do can squish.
L35 SHERI | And squish em.
L36 SHERI | For the recycling bin.
L37 SHERI | ... Ok[ay]?
L38 STEVEN | [Tomorrow] please,
L39 STEVEN | my feet [2are hurting2].
L40 SHERI | [2Tomorrow2]?
L41 SHERI | ... (H) Well can you just put em in the bag,
L42 SHERI | ... in there for now,
L43 SHERI | okay?
L44 STEVEN | ... Ok[ay].
L45 SHERI | [Cause] I gotta clean up in here,
L46 SHERI | this .. place is just totally trashed,
L47 SHERI | .. cause I've done nothing this week but,
L48 SHERI | ... study and be sick.
```

Limits: This shows ordinary interaction, including repetition and negotiation, not polished writing. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-017 — SBC059:L30-L58

- Stable source ID: `SBC059`
- Accepted source locator: `SBC059:L30-L58`
- Exact quote locator: `SBC059:L33-L58`
- Bounded roles: `narrative`, `sequence`, `causal_explanation`, `inference`
- Canonical function: Tell what happened in a game and connect the sequence to its outcome.
- Context: spoken; family talking at home on Christmas Eve; US English; near Beloit, Wisconsin
- Public/source links: [You Baked](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC059.trn)
- Local corpus file: `sources/sbcsae/raw/SBC059.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L33 WESS | [2Well yeah2]=,
L34 WESS | because uh,
L35 WESS | (H) the t- .. the,
L36 WESS | ... Steelers,
L37 WESS | were on the one yard line,
L38 CAM | Unhunh?
L39 WESS | for four downs.
L40 WESS | And [they didn't get in].
L41 CAM | [Wow=].
L42 WESS | (H) And then they were on the ten yard line,
L43 WESS | with fourth down to go,
L44 WESS | (H) and they had inches to go,
L45 WESS | (H) the guy didn't even get up to the line of scrimmage,
L46 WESS | ... that was .. had the ball,
L47 CAM | ... Nice.
L48 WESS | But he must've pushed it up there or something,
L49 WESS | I don't know,
L50 WESS | how he got it up there.
L51 WESS | (H) But they gave it to them then,
L52 WESS | (H) then,
L53 WESS | that'd give em another four down- %,
L54 WESS | ... four ... downs on the ... one yard line,
L55 JO | ... So it's over with.
L56 WESS | .. So it's over with,
L57 CAM | [<X They X> won].
L58 WESS | [Green Bay] won twenty-four to nine[2teen2].
```

Limits: Sports terms are local to the topic; the passage is useful mainly for sequence and cause. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-018 — SBC060:L1-L42

- Stable source ID: `SBC060`
- Accepted source locator: `SBC060:L1-L42`
- Exact quote locator: `SBC060:L11-L42`
- Bounded roles: `narrative`, `time_anchoring`, `causal_explanation`
- Canonical function: Set up a story, place it in time, and explain how the situation changed.
- Context: spoken; two friends and coworkers talking during a break; US English; Shreveport, Louisiana
- Public/source links: [Shaggy Dog Story](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC060.trn)
- Local corpus file: `sources/sbcsae/raw/SBC060.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L11 ALAN | It must've been,
L12 ALAN | ... four to six months after my dad died.
L13 ALAN | That’s how I remember it,
L14 ALAN | he [died in s]ixty-s=- --
L15 JON | [Oh God].
L16 ALAN | ... December sixty-seven,
L17 ALAN | so,
L18 ALAN | (H)= sometime in sixty-eight we took this trip,
L19 ALAN | we’d been ... talking about it for a while,
L20 ALAN | ... uh=,
L21 ALAN | flew down to Mexico City,
L22 ALAN | ... uh we,
L23 ALAN | (Hx) c- think of the name of my hotel,
L24 ALAN | which wouldn’t mean anything now,
L25 ALAN | but we ended up in a ... fabulous hotel,
L26 ALAN | ... uh=,
L27 ALAN | ... first night,
L28 ALAN | we were <VOX very unhappy VOX> with our rooms,
L29 ALAN | we got down there,
L30 ALAN | (H)= and the next morning,
L31 ALAN | Buddy,
L32 ALAN | who’s a ... early riser anyhow,
L33 ALAN | was probably up ... four o'clock,
L34 ALAN | and he went down there complaining to the manager,
L35 ALAN | ... So,
L36 ALAN | .. cause it was not w- the accommodation we were supposed to have had,
L37 ALAN | we checked in about eight o’clock at night or so,
L38 ALAN | which is,
L39 ALAN | (H)= in Mexico is like,
L40 ALAN | .. you know,
L41 ALAN | ... <X the X> --
L42 ALAN | (H) ... Well we ended up with a .. corner .. suite.
```

Limits: This is spoken narrative with pauses and repairs, not edited prose. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-019 — SBC047:L18-L61

- Stable source ID: `SBC047`
- Accepted source locator: `SBC047:L18-L61`
- Exact quote locator: `SBC047:L34-L61`
- Bounded roles: `narrative`, `sequence`, `causal_explanation`
- Canonical function: Describe a work problem step by step and explain an entry on a record card.
- Context: spoken; two cousins talking in a private home; US English; East Los Angeles, California
- Public/source links: [On the Lot](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC047.trn)
- Local corpus file: `sources/sbcsae/raw/SBC047.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L34 FRED | .. (H) And on my production card.
L35 FRED | ... (TSK) (H) Let's see.
L36 FRED | ... The day before yesterday.
L37 FRED | .. I did ice cream.
L38 FRED | .. Right,
L39 FRED | Balian?
L40 RICHARD | Unh[unh].
L41 FRED | [(H)] And you gotta pack those in cases.
L42 FRED | ... (H)[2= And2],
L43 RICHARD | [2Right2].
L44 FRED | so like,
L45 FRED | I didn't put that down on my production c[ard].
L46 RICHARD | [How many] cases you packed.
L47 FRED | (H) I don't know man.
L48 FRED | ... I packed two pallets.
L49 FRED | ... You know,
L50 FRED | ... I don't know how many .. cases [that is],
L51 RICHARD | [Unhunh],
L52 FRED | but,
L53 FRED | (H)= you know,
L54 FRED | that,
L55 FRED | .. that shit was heavy man.
L56 FRED | And like,
L57 FRED | ... and like,
L58 FRED | ... I put down on the card,
L59 FRED | you know,
L60 FRED | no cases.
L61 FRED | Because it was lost time.
```

Limits: Work terms are part of the event being discussed, not institutional prose supplied by the employer. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-020 — SBC048:L45-L68

- Stable source ID: `SBC048`
- Accepted source locator: `SBC048:L45-L68`
- Exact quote locator: `SBC048:L52-L58`
- Bounded roles: `question_and_response`, `direct_instruction`, `observable_cue`
- Canonical function: Ask how to use a device and answer with the visible step to wait for.
- Context: spoken; family exchanging gifts on Christmas morning; US English; Fresno, California
- Public/source links: [Mickey Mouse Watch](https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english); [raw source](https://www.linguistics.ucsb.edu/sites/default/files/sitefiles/research/SBC/SBC048.trn)
- Local corpus file: `sources/sbcsae/raw/SBC048.trn`
- Rights/licence: CC BY-ND 3.0 US. Raw files are kept unchanged. Search views are local working aids and are not cleared for republication. [Licence link](https://creativecommons.org/licenses/by-nd/3.0/us/)

Exact quote:

```text
L52 TIM | [5%uh,
L53 TIM | I just5],
L54 TIM | .. push down on this thing,
L55 TIM | right?
L56 JUDY | (H) Yeah,
L57 JUDY | you wait until you see the green light.
L58 JUDY | ... In there.
```

Limits: The exchange is short and overlapping; use it as wording evidence, not a complete instruction model. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-021 — SCOTS996:L13-L50

- Stable source ID: `SCOTS996`
- Accepted source locator: `SCOTS996:L13-L50`
- Exact quote locator: `SCOTS996:L13-L37`
- Bounded roles: `practical_rationale`, `contrast`, `direct_instruction`
- Canonical function: Explain a practical choice, its cost, and why it suits the speaker.
- Context: spoken; friends talking over lunch about ordinary home life; Scottish English and Scots; Stirling
- Public/source links: [Conversation 24: Three women chatting in a garden centre](https://scottishcorpus.ac.uk/document/?documentid=996); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=996)
- Local corpus file: `sources/scots/raw/SCOTS_996.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L13 F606 | So what would you buy if you had a big garden?
L14 F890 | Small things and let them grow,
L15 F606 | Yeah [laugh]
L16 F889 | Well I've just done mines //Christian.//
L17 F890 | //so that it'll be cheaper.//
L18 F889 | Ah an I've covered it wi stones
L19 F606 | Yeah.
L20 F889 | an a big rock an itwis eh, it wis quite expensive, but at the same
L21 F889 | time that's it done forever.
L22 F606 | mmhm
L23 F889 | I'm so pleased wi it I keep lookin at it an think, "Oh that's lovely,
L24 F889 | that's lovely!" //[laugh]//
L25 F890 | //[laugh]//
L26 F606 | So have you got no plants at all //in it?//
L27 F889 | //Eh// just shrubs, just shrubs, but I canna look after plants
L28 F889 | neither, it's gotta be just be something that lasts forever and
L29 F890 | Yeah.
L30 F889 | looks after itself.
L31 F606 | mmhm
L32 F889 | I like to see them but I'm no one for that neither, aw the flowers, I
L33 F889 | like the shrubs
L34 F890 | Mm an it's quite simple, if anything's withered //cut it off.//
L35 F889 | //Cut it off// //[inaudible]//
L36 F606 | //Yeah.//
L37 F889 | Cut it off if it's withered, eh?
```

Limits: The Scottish forms belong to these speakers and are not silently treated as universal English. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-022 — SCOTS1384:L19-L49

- Stable source ID: `SCOTS1384`
- Accepted source locator: `SCOTS1384:L19-L49`
- Exact quote locator: `SCOTS1384:L25-L47`
- Bounded roles: `narrative`, `sequence`, `contrast`
- Canonical function: Tell how a plan began, was delayed, and became more complicated.
- Context: spoken; two friends talking about a recent wedding; Scottish English and Scots; Glasgow
- Public/source links: [Conversation 26: Two females from Glasgow talking about weddings](https://scottishcorpus.ac.uk/document/?documentid=1384); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=1384)
- Local corpus file: `sources/scots/raw/SCOTS_1384.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L25 F689 | Och, it was just, I never really thought about it, cause erm, I was
L26 F689 | quite happy ploddin along, but we'd said like years ago before Rosalyn was
L27 F689 | even born that we should perhaps get married at some point, [laugh], //so
L28 F689 | it just sort o//
L29 F631 | //Mmhm//
L30 F689 | got put on hold and put on hold. And then what with the movin house
L31 F689 | and stuff. Ehm, so it originally turned out that we'd just go for a really
L32 F689 | really small do.
L33 F631 | Mmhm
L34 F689 | And [throat] of course I told Mum and she was like "Oh, we'll need to
L35 F689 | have a reception" [laugh] and things like that. //So,//
L36 F631 | //Right.//
L37 F689 | it just started out ehm tryin to keep it as simple an as sort o cheap
L38 F689 | as possible. [laugh]
L39 F631 | Mmhm
L40 F689 | Ehm, but it was quite horrendous tryin to find like a place that
L41 F689 | would accept children, //and stuff like that.//
L42 F631 | //Really?//
L43 F689 | Mmhm, it was like erm, totally, erm, "You're only allowed kids until
L44 F689 | half past eight and that's it. No exceptions." //[laugh] Uh-huh//
L45 F631 | //Up until half eight, right.//
L46 F689 | And, so we tried about four different pubs and phoned other places
L47 F689 | and it was "no no no no" //[laugh].//
```

Limits: The opening question was prompted for a corpus recording; the answer remains the speaker's own wording. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-023 — SCOTS027:L239-L253

- Stable source ID: `SCOTS027`
- Accepted source locator: `SCOTS027:L239-L253`
- Exact quote locator: `SCOTS027:L239-L243`
- Bounded roles: `contrast`, `comparison_analogy`
- Canonical function: Answer a comparison question by putting the two cases side by side.
- Context: spoken; three sisters talking in a family home; Scottish English and Scots; Ayrshire
- Public/source links: [Conversation 06: Three Ayrshire sisters reminiscing](https://scottishcorpus.ac.uk/document/?documentid=027); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=027)
- Local corpus file: `sources/scots/raw/SCOTS_27.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L239 M608 | What was the difference between the the big school and the junior
L240 M608 | school? I mean what kinda?
L241 F638 | Well then it was like eh movin now. Ye had a different teacher for
L242 F638 | each subject, whereas ye had the same teacher for the the whole year.
L243 M608 | Aye, right.
```

Limits: The question was elicited in a recorded conversation; the answer is not a prepared or academic text. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-024 — SCOTS1570:L14-L53

- Stable source ID: `SCOTS1570`
- Accepted source locator: `SCOTS1570:L14-L53`
- Exact quote locator: `SCOTS1570:L35-L49`
- Bounded roles: `direct_instruction`, `sequence`, `correction`, `scope_condition`
- Canonical function: Help a child complete a writing task by giving one concrete step at a time.
- Context: spoken; mother and child getting ready for a birthday party at home; Scottish English and Scots; Buckie and Portknockie
- Public/source links: [Conversation: Buckie - Mother and child 20, recording 1](https://scottishcorpus.ac.uk/document/?documentid=1570); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=1570)
- Local corpus file: `sources/scots/raw/SCOTS_1570.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L35 F1139 | Will I gie you a pencil, so you can rub it oot if you mak a
L36 F1139 | mistake?
L37 F1140 | Aye.
L38 F1139 | Haud on till I get a bit o paper. This is "from", right? That's an
L39 F1139 | F. And then an R. An O. And then M., but it's a little M., nae a big M.
L40 F1139 | like the start o your name. [CENSORED: forename spelt out] And dae some
L41 F1139 | kisses. And then you can maybe try and write [CENSORED: forename] on the
L42 F1139 | envelope.
L43 F1140 | Mmhm.
L44 F1139 | Okay? Can you write "from [CENSORED: forename]" on the card there.
L45 F1140 | I canna write [CENSORED: forename].
L46 F1139 | Well, just write "from [CENSORED: forename]" just now and I'll write
L47 F1139 | [CENSORED: forename] on the envelope. Oh, you've tae dae yer kisses last,
L48 F1139 | ye neep! [laugh] Right, you write "from [CENSORED: forename]" and then you
L49 F1139 | dae yer kisses last. //Will I write "from"?//
```

Limits: The local Scots forms are kept as evidence from this family, not rewritten as a supposed standard. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-025 — SCOTS394:L19-L31

- Stable source ID: `SCOTS394`
- Accepted source locator: `SCOTS394:L19-L31`
- Exact quote locator: `SCOTS394:L27-L31`
- Bounded roles: `personal_update`, `inference`, `causal_explanation`
- Canonical function: Give family news, make a joke, and connect one practical consequence to another.
- Context: written; a private letter to a family member, 1945; Scottish English; personal letter written from Italy
- Public/source links: [Biggam Collection Letter: 01](https://scottishcorpus.ac.uk/document/?documentid=394); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=394)
- Local corpus file: `sources/scots/raw/SCOTS_394.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L27 James Taylor | I'm in complete agreement with you regarding my being home to keep Madge in
L28 James Taylor | order, but I just can't convince the C-in-C Mediterranean. However, the
L29 James Taylor | more boys take Madge out, the more money she can save to take me out, and
L30 James Taylor | that means I can save to take my six machinists out. I haven't seen the pen
L31 James Taylor | pal since before Christmas, but what tales I can tell when I do.
```

Limits: This 1945 Scottish letter is one person's ordinary written voice, not a present-day universal model. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-026 — SCOTS395:L16-L28

- Stable source ID: `SCOTS395`
- Accepted source locator: `SCOTS395:L16-L28`
- Exact quote locator: `SCOTS395:L16-L25`
- Bounded roles: `sympathy_support`, `personal_update`
- Canonical function: Share sympathy and explain recent personal circumstances plainly.
- Context: written; a private letter to a friend or family member, 1984; Scottish English; Glasgow
- Public/source links: [Biggam Collection Letter: 02](https://scottishcorpus.ac.uk/document/?documentid=395); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=395)
- Local corpus file: `sources/scots/raw/SCOTS_395.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L16 May Trotter | What a shock Alice and I got to hear of the death of Arthur. We did not
L17 May Trotter | know he was ailing and what a worrying time you must have had. You will
L18 May Trotter | miss him very much. So many of our friends are slipping away. I am glad
L19 May Trotter | Chrissie has managed to be with you. Alice and I would like to take a run
L20 May Trotter | through soon to visit you and we will let you know first.
L22 May Trotter | I have been attending the hospital for 6 months now for treatment to my
L23 May Trotter | right eye. A blockage was discovered and I have lost the sight of the eye.
L24 May Trotter | How worried I was but fortuneately my left eye is able to function and I
L25 May Trotter | get along not so bad. We don't get out so much at night now. Too many
```

Limits: The topic is personal and the wording is from 1984 Scottish English. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-027 — SCOTS397:L15-L38

- Stable source ID: `SCOTS397`
- Accepted source locator: `SCOTS397:L15-L38`
- Exact quote locator: `SCOTS397:L15-L30`
- Bounded roles: `personal_update`, `causal_explanation`, `scope_condition`
- Canonical function: Give a detailed family health update and explain day-to-day consequences.
- Context: written; a private letter about a family member's health; Scottish English; Glasgow
- Public/source links: [Biggam Collection Letter: 04](https://scottishcorpus.ac.uk/document/?documentid=397); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=397)
- Local corpus file: `sources/scots/raw/SCOTS_397.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L15 Catherine O'Rourke | Thank you very much for the money you shouldn't have Jimmy isn't alowd
L16 Catherine O'Rourke | sweets at the moment his food has to be liquidized because of his throat he
L17 Catherine O'Rourke | can't even get porridge in the morning he has to get thickener in his
L18 Catherine O'Rourke | drinks so if its alright with you I'll get him a couple of Light Weight
L19 Catherine O'Rourke | Trousers with the money. He still cant talk but he knows everything your
L20 Catherine O'Rourke | saying to him. I took your letter up and says did you get one and he took
L21 Catherine O'Rourke | your letter out his pocket and gave me it home with me. Anna asked to get
L22 Catherine O'Rourke | him out last Saturday for a couple of hours to my house so he was as happy
L23 Catherine O'Rourke | as Larry but Anna and Loraine took him back at night so he seems a bit more
L24 Catherine O'Rourke | content now. I says to him once he finishes treatment hell get home for
L25 Catherine O'Rourke | good and he gave me a wink and started laughing. When he was home he was
L26 Catherine O'Rourke | watching the racing on TV and pressed the remote controll and lost the
L27 Catherine O'Rourke | picture so he was shouting YO YO YO and I rushed in and it was the picture
L28 Catherine O'Rourke | he lost and didnt know how to get it back. He can go to the toilet himself
L29 Catherine O'Rourke | but thats about all need help to dress and other things so it might come
L30 Catherine O'Rourke | back out of the Blue you never know he's such a good man doesnt deserve
```

Limits: The medical account is not medical advice; the passage is language evidence only. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-028 — SCOTS399:L18-L42

- Stable source ID: `SCOTS399`
- Accepted source locator: `SCOTS399:L18-L42`
- Exact quote locator: `SCOTS399:L18-L25`
- Bounded roles: `narrative`, `personal_update`, `sympathy_support`
- Canonical function: Explain a failed phone call and give personal news and support.
- Context: written; a private letter to a friend or family member, 1995; Scottish English; Glasgow
- Public/source links: [Biggam Collection Letter: 06](https://scottishcorpus.ac.uk/document/?documentid=399); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=399)
- Local corpus file: `sources/scots/raw/SCOTS_399.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L18 Alice Trotter | I was so very nice to hear your voice but we somehow got cut off. I phoned
L19 Alice Trotter | your old number and got a very nice man who answered. I explained that I
L20 Alice Trotter | was trying to get you and he seemed to know about you but he couldn't give
L21 Alice Trotter | me your new number.
L23 Alice Trotter | I was very sorry to hear about Madge. Our circle is beginning to become
L24 Alice Trotter | very small now-a-days. It is great to have someone you can say "Do you
L25 Alice Trotter | remember?" However we have our good times to look back on.
```

Limits: The writer sometimes uses words that may sound more formal today. Inclusion records real use; it does not endorse every choice. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-029 — SCOTS1458:L15-L31

- Stable source ID: `SCOTS1458`
- Accepted source locator: `SCOTS1458:L15-L31`
- Exact quote locator: `SCOTS1458:L25-L31`
- Bounded roles: `personal_update`, `direct_request`, `practical_rationale`
- Canonical function: Give a family update and ask for confirmation about a practical matter.
- Context: written; a private letter from a mother to her daughter, 1989; Scottish English; Edinburgh
- Public/source links: [Letter from Frances Gardner 04 - 11/10/89](https://scottishcorpus.ac.uk/document/?documentid=1458); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=1458)
- Local corpus file: `sources/scots/raw/SCOTS_1458.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L25 Frances Gardner | Spring. I hope all is well with you and that you are now nicely esconced in
L26 Frances Gardner | your new home. I am looking forward to having more details from you. Also,
L27 Frances Gardner | can you please confirm that you have received Dad's money and our flowers.
L28 Frances Gardner | I understand they had difficulty in delivering the latter and I eventually
L29 Frances Gardner | gave them your work phone number. Obviously, it will be better to send any
L30 Frances Gardner | parcels etc to you at the University. I did think the caretaker might have
L31 Frances Gardner | taken in messages. 
```

Limits: The writer uses several more formal connectives. This is evidence that private writing varies, not a reason to copy them by default. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-030 — SCOTS1458:L45-L59

- Stable source ID: `SCOTS1458`
- Accepted source locator: `SCOTS1458:L45-L59`
- Exact quote locator: `SCOTS1458:L45-L59`
- Bounded roles: `personal_update`, `afterthought`
- Canonical function: Share ordinary daily details and add practical afterthoughts.
- Context: written; a private letter from a mother to her daughter, 1989; Scottish English; Edinburgh
- Public/source links: [Letter from Frances Gardner 04 - 11/10/89](https://scottishcorpus.ac.uk/document/?documentid=1458); [raw source](https://scottishcorpus.ac.uk/download-plaintext/?documentid=1458)
- Local corpus file: `sources/scots/raw/SCOTS_1458.txt`
- Rights/licence: Local educational/research use under the SCOTS terms. Do not redistribute this collection without checking each holder's permission. [Licence link](https://www.scottishcorpus.ac.uk/termsandconditions.html)

Exact quote:

```text
L45 Frances Gardner | Well its lunch time now. Soup and a roll as usual. mince and potatoes for
L46 Frances Gardner | tea to-night. What a lot more rubbish you can write when you get going on
L47 Frances Gardner | the type writer. 
L49 Frances Gardner | Much love, 
L51 Frances Gardner | Mum xxx
L53 Frances Gardner | PS. Uncle Bill could only be persuaded to take your dressing gown! He was
L54 Frances Gardner | quite flustered about his luggage and it was only with difficulty that I
L55 Frances Gardner | could persuade him to take a very small packet of Edinburgh Rock to Sheila
L56 Frances Gardner | & co!!
L58 Frances Gardner | Also you will be pleased to know that I put up your net curtain in the back
L59 Frances Gardner | porch - what an improvement on the torn rag that was there!!
```

Limits: This passage is evidence for informal personal writing, not explanatory mathematics. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-031 — COOK116793:L14

- Stable source ID: `COOK116793`
- Accepted source locator: `COOK116793:L14`
- Exact quote locator: `COOK116793:L14`
- Bounded roles: `sequence`, `causal_explanation`, `practical_rationale`
- Canonical function: State the order of two actions and give the practical difference that explains the order.
- Context: written; a person explaining the order and reason for two cooking steps; Online English; the post does not establish the author's regional variety
- Public/source links: [What is ‘layering flavors’? — answer 116793 excerpt](https://cooking.stackexchange.com/a/116793); [raw source](https://api.stackexchange.com/2.3/answers/116793?site=cooking&filter=withbody)
- Local corpus file: `sources/stackexchange/raw/COOK_116793.txt`
- Rights/licence: Selected user-contributed excerpt only. Attribution, post identity, revision dates, and the post's stated CC BY-SA version are retained in the raw excerpt record. [Licence link](https://stackoverflow.com/help/licensing)
- Source version: Seasoned Advice answer 116793, last edited 2021-08-11T07:55:40Z, CC BY-SA 4.0

Exact quote:

```text
L14 AnoE | The reason why onions are added first, and then the garlic, is that onions can and should be heated much longer than garlic.
```

Limits: One short online answer is not private conversation, does not establish a regional variety, and does not make every phrase broadly familiar. The cooking claim is not technical authority for mathematics. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-032 — COOK40170:L14

- Stable source ID: `COOK40170`
- Accepted source locator: `COOK40170:L14`
- Exact quote locator: `COOK40170:L14`
- Bounded roles: `causal_explanation`, `inference`
- Canonical function: Give a cause and its immediate practical consequence in one connected sentence.
- Context: written; a person explaining a practical cooking choice to another user; Online English; the post does not establish the author's regional variety
- Public/source links: [First onion or first minced meat? — answer 40170 excerpt](https://cooking.stackexchange.com/a/40170); [raw source](https://api.stackexchange.com/2.3/answers/40170?site=cooking&filter=withbody)
- Local corpus file: `sources/stackexchange/raw/COOK_40170.txt`
- Rights/licence: Selected user-contributed excerpt only. Attribution, post identity, revision dates, and the post's stated CC BY-SA version are retained in the raw excerpt record. [Licence link](https://stackoverflow.com/help/licensing)
- Source version: Seasoned Advice answer 40170, created 2013-12-11T18:27:54Z, CC BY-SA 3.0

Exact quote:

```text
L14 SAJ14SAJ | The onions would express water, which would lower the temperature to simmer or steam, preventing the beef from browning.
```

Limits: This public specialist forum is not a sample of ordinary private writing or worldwide English. The passage supports a causal construction, not the factual accuracy of every cooking claim. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

### EE-033 — MSE1087517:L14

- Stable source ID: `MSE1087517`
- Accepted source locator: `MSE1087517:L14`
- Exact quote locator: `MSE1087517:L14`
- Bounded roles: `definition`
- Canonical function: State the defining input-output condition for a function in a direct sentence while retaining the notation and technical name.
- Context: written; a person answering a learner's question about functions; Online English; the post does not establish the author's regional variety
- Public/source links: [What is a function? — answer 1087517 excerpt](https://math.stackexchange.com/a/1087517); [raw source](https://api.stackexchange.com/2.3/answers/1087517?site=math&filter=withbody)
- Local corpus file: `sources/stackexchange/raw/MSE_1087517.txt`
- Rights/licence: Selected user-contributed excerpt only. Attribution, post identity, revision dates, and the post's stated CC BY-SA version are retained in the raw excerpt record. [Licence link](https://stackoverflow.com/help/licensing)
- Source version: Mathematics Stack Exchange answer 1087517, last edited 2022-06-21T01:45:29Z, CC BY-SA 4.0

Exact quote:

```text
L14 Clive Newstead | What it means to be a function $f : A \to B$ is this: $f$ assigns to each element of $A$ exactly one element of $B$.
```

Limits: A Mathematics Stack Exchange contributor is a self-selected mathematically experienced writer, not a representative sample of everyday English. This passage supports one explanatory construction only; the frozen mathematical source remains the authority for the project. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

Recorded mathematical cross-check (still not authority): The sentence requires one output in B for every input in A, matching the total single-valued condition in frozen function-basics.tex:29-30. It does not supply the later domain, codomain, range, or extensionality details.

### EE-034 — MSE3427924:L14

- Stable source ID: `MSE3427924`
- Accepted source locator: `MSE3427924:L14`
- Exact quote locator: `MSE3427924:L14`
- Bounded roles: `definition`, `equivalent_restatement`
- Canonical function: Put two equivalent readings of injectivity side by side in ordinary input-output language.
- Context: written; a person correcting a learner's confusion about injectivity; Online English; the post does not establish the author's regional variety
- Public/source links: [Trouble understanding injection problem — answer 3427924 excerpt](https://math.stackexchange.com/a/3427924); [raw source](https://api.stackexchange.com/2.3/answers/3427924?site=math&filter=withbody)
- Local corpus file: `sources/stackexchange/raw/MSE_3427924.txt`
- Rights/licence: Selected user-contributed excerpt only. Attribution, post identity, revision dates, and the post's stated CC BY-SA version are retained in the raw excerpt record. [Licence link](https://stackoverflow.com/help/licensing)
- Source version: Mathematics Stack Exchange answer 3427924, last edited 2019-11-09T02:20:42Z, CC BY-SA 4.0

Exact quote:

```text
L14 Arturo Magidin | Remember what injectivity means: either “different inputs yield different outputs” or “if ‘two’ inputs yield the same output, then they are actually the same input.”
```

Limits: The public mathematics forum and its contributors are not representative of all English users. The excerpt assumes the surrounding function and its domain; it is language evidence, not an independent proof that a target passage is correct. This is attestation for the named language move in the named source and setting only; it does not establish universal comprehension, corpus-wide frequency, or mathematical authority.

Recorded mathematical cross-check (still not authority): For a function, ‘different inputs give different outputs’ is equivalent by contraposition to ‘equal outputs came from equal inputs’; this matches the two injectivity tests in frozen function-kinds.tex:64-73.

## Validation summary

- Accepted passage records: 34
- Stable source IDs represented: 29
- Exact quoted language lines: 432 of 692 available accepted lines
- Modes: spoken=24, written=10
- Collections: sbcsae=20, scots=10, stackexchange=4
- Every quote was checked as a nonempty, in-range subset of its accepted exact record, with unchanged `text_exact` values.
- JSON parsing, ID uniqueness, manifest/exact-record equality, included-source status, positive-layer membership, and passing control reports are enforced by generation-time assertions.
