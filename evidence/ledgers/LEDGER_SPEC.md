# Linked ledger specification

These ledgers are append-only JSON Lines files. Their initialization records do not assert content coverage. Content records must carry stable IDs and exact-byte locators; records are superseded, never silently rewritten.

Common fields for substantive records are `id`, `record_type`, `created_at`, `authority`, `source_sha256`, `source_locator`, `target_path`, `target_locator`, `target_sha256`, `relation`, `status`, `dependency_ids`, `risk_ids`, `check_ids`, and `supersedes`.

The transcription ledger additionally records page, text/formula/structure/figure checks, visual evidence, uncertainties, and whether the source text was preserved rather than corrected. The translation and target-change ledgers additionally record the academic decoding burden, canon passage IDs, discourse job, comprehension mechanism, retained technical terms, alternatives, and bidirectional semantic/notation/formula/dependency checks. The canon ledger records authentic passage bytes, source provenance, role, fit, and limits. The additions ledger records each non-source explanation and its proof. The mathematics ledger records complete claims and exact proof or formal locators. Build and visual-QA records identify exact input and output hashes and fail on stale bytes. Work-event records link operational choices without being mathematical authority.

An audit must fail on uncovered content, stale or false locators, formula drift, missing references, unsupported canon, unexplained target changes, unproved additions, or incomplete visual coverage.
