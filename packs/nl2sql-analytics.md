# Pack: NL2SQL and Conversational Analytics

**Applies to:** "ask your data" features, BI copilots, metric explainers, analytics agents over Snowflake, BigQuery, Postgres, semantic layers.
**Typical stakes:** Low for exploratory internal use; Medium when numbers go to customers, boards or pricing decisions.

Public benchmarks show the gap clearly: methods near 91% on Spider 1.0 solved only about 21% of enterprise-style [Spider 2.0](https://arxiv.org/abs/2411.07763) tasks at release. Your warehouse looks more like Spider 2.0. And neither benchmark knows *your* definitions of "active customer" or "attrition".

## Failure modes
`wrong-metric-definition` · `wrong-join-or-filter` (double counting after a join) · `silent-empty-result` · `should-have-asked` ("last quarter": fiscal or calendar?) · wrong time zone or date boundary · row-level security bypass · correct SQL with a wrong narrative ("revenue grew" when it fell)

## Metrics

| Question | Metric | Grader | How |
|---|---|---|---|
| Right | Schema linking accuracy | Code | Tables/columns used vs gold set |
| Right | Semantic-layer adherence | Code | Uses certified metric definitions/views instead of re-deriving from raw tables |
| Right | **Execution accuracy (EX)** | Code | Run predicted and gold SQL; compare result sets (order-insensitive, tolerance for floats) |
| Right | Relaxed EX | Code | Allows extra columns, as Spider 2.0 does; use for exploratory UX |
| Right | Clarification correctness | Judge | On ambiguous questions, asks the right clarifying question instead of guessing |
| Right | Narrative faithfulness | Code + judge | Every number in the text appears in the result set (code); direction words (up/down, highest) are correct (judge) |
| Right | Chart correctness | Code | Chart type and axes match the result shape |
| Safe | RLS enforcement | Code | Same question as two users with different row access returns different, correct rows |
| Safe | Destructive SQL blocked | Code | No DDL/DML executed; read-only role verified |
| Worth it | Query cost and runtime | Telemetry | Bytes scanned, warehouse credits, timeouts |

## Dataset design
- **Source questions** from real analyst Slack threads, dashboard filters and BI search logs.
- **Gold SQL written by the data team** against the semantic layer, reviewed by the metric owner.
- Slices: simple aggregate · time comparison · multi-join · cohort/retention · ambiguous (expects clarification) · unanswerable with available data (expects "no data") · RLS-sensitive.
- **Metric definition cases:** for each certified metric, at least 3 phrasings that should map to it, and 1 near-miss that should not.
- Keep a frozen snapshot database for eval so results are reproducible while production data changes.

## Pass bars (Medium stakes default)
- EX >= 90% on certified-metric slice; >= 75% on multi-join slice (report, improve over time)
- Narrative number fidelity 100%
- RLS and read-only checks: 0 violations
- Clarification asked on >= 80% of ambiguous slice; over-clarification on clear questions <= 10%

## Borrow from
Spider 2.0 and BIRD for task design and evaluation scripts; your dbt/semantic-layer tests as a source of ground truth.
