# Pack: RAG Knowledge Assistant

**Applies to:** internal policy Q&A, help-center copilots, product documentation assistants, "ask your handbook", sales enablement Q&A.
**Typical stakes:** Low for internal use with review; Medium when customers or employees rely on it directly.

## Failure modes to look for first
`unsupported-claim` · `wrong-source` · `citation-mismatch` · `missed-document` · `stale-index` · `over-refusal` · `missed-constraint` (region, role, plan, year)

## Metrics

| Question | Metric | Grader | How |
|---|---|---|---|
| Right | Recall@k on gold documents | Code | Gold doc IDs per question; check presence in top-k |
| Right | Context precision | Code or judge | Share of retrieved chunks that are relevant ([Ragas](https://docs.ragas.io) has a judge-based version) |
| Right | Freshness | Code | Max age of retrieved chunk vs source last-modified |
| Right | Faithfulness | Judge | Every claim in the answer is supported by retrieved context (binary per answer, or share of supported claims) |
| Right | Answer correctness | Code or judge | Against a reference answer or a list of required key facts |
| Right | Citation accuracy | Code + judge | Cited doc was retrieved (code) and contains the claim (judge) |
| Right | Correct abstention | Code | On unanswerable questions, says it does not know and routes appropriately |
| Right | Over-refusal rate | Code | Refuses on answerable questions |
| Safe | Permission leak | Code | See [enterprise search pack](enterprise-search-permissions.md) |
| Worth it | Deflection, thumbs-down rate, follow-up rate | Analytics | Repeat question within 10 min is a strong negative signal |

## Dataset design

| Slice | Share | Notes |
|---|---|---|
| Answerable, single document | 35% | Taken from real tickets or search logs |
| Answerable, multi-document synthesis | 20% | Needs combining two sources |
| Conditional answers | 15% | Answer depends on role, region, plan, date |
| Unanswerable / out of corpus | 15% | Correct behavior is abstain + route |
| Conflicting or superseded sources | 10% | Old and new policy both indexed |
| Adversarial | 5% | Injected instructions inside documents ([security pack](security-red-teaming.md)) |

For each case store: `question`, `user_context` (role, tenant, region), `gold_doc_ids`, `required_facts`, `forbidden_doc_ids`, `expected_behavior` (answer / abstain / clarify / escalate).

## Pass bars (Medium stakes default)
- Faithfulness >= 95%, citation accuracy >= 95%
- Recall@5 >= 90% on single-document slice
- Correct abstention >= 90%; over-refusal <= 5%
- Zero permission leaks on golden + adversarial

## Online signals
Thumbs-down with reason, repeat questions, escalation to human, "open cited source" click-through (low click-through on high-stakes answers can mean over-trust).

## Borrow from
Ragas (metrics, synthetic question generation), DeepEval (CI), your observability platform's dataset-from-traces feature.
